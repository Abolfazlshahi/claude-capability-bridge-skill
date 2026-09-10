"""Hook behaviour tests.

These run the real engine and the real shell wrappers the way a host does:
JSON on stdin, one `--event`, output on stdout, exit code always 0.

Scope note: this proves what the hook *emits*. It cannot prove that a host
accepted the output, or that a model obeyed it. Delivery stays best-effort.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import bridge_test_utils as util

BUDGET = json.loads(
    (util.ROOT / "config" / "content-budgets.json").read_text(encoding="utf-8")
)["budgets"]["hook_output_chars"]

WRAPPERS = util.SHELL_WRAPPERS


class HookTestCase(unittest.TestCase):
    """Base class: every test gets its own throwaway state directory."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.state_dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def env(self, **extra: str) -> dict:
        env = {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(self.state_dir)}
        env.update(extra)
        return env

    def engine(self, event, payload, **extra):
        body = payload if isinstance(payload, str) else json.dumps(payload)
        proc = util.run_engine(event, body, self.env(**extra))
        self.assertEqual(proc.returncode, 0, f"hook must never fail: {proc.stderr}")
        return util.hook_context(proc)

    def start(self, session: str = "s1", source: str = "startup"):
        return self.engine("SessionStart", {"session_id": session, "source": source})


class MalformedInputTestCase(HookTestCase):
    def test_empty_stdin_is_survivable(self) -> None:
        for event in ("SessionStart", "UserPromptSubmit", "PostToolUseFailure"):
            proc = util.run_engine(event, "", self.env())
            self.assertEqual(proc.returncode, 0, event)
            util.hook_context(proc)  # silent or a valid envelope

    def test_corrupt_json_does_not_crash_or_leak(self) -> None:
        context = self.engine("SessionStart", '{"session_id": "x", broken')
        self.assertIsNotNone(context)
        self.assertNotIn("Traceback", context or "")
        self.assertNotIn("broken", context or "")

    def test_unknown_event_is_silent(self) -> None:
        self.assertIsNone(self.engine("TotallyMadeUpEvent", {"session_id": "s"}))

    def test_missing_optional_fields_are_tolerated(self) -> None:
        self.assertIsNotNone(self.engine("SessionStart", {}))
        proc = util.run_engine("UserPromptSubmit", "{}", self.env())
        self.assertEqual(proc.returncode, 0)

    def test_non_object_json_is_tolerated(self) -> None:
        for payload in ("[]", '"just a string"', "12", "null"):
            proc = util.run_engine("UserPromptSubmit", payload, self.env())
            self.assertEqual(proc.returncode, 0, payload)
            util.hook_context(proc)


class AdaptiveQuietTestCase(HookTestCase):
    def test_session_start_delivers_the_kernel_protocol(self) -> None:
        context = self.start()
        self.assertIsNotNone(context)
        self.assertIn("CAPABILITY BRIDGE", context)
        self.assertIn("cards/", context)

    def test_ordinary_turn_is_silent_after_session_start(self) -> None:
        """The core regression this redesign exists for: no per-turn reminder."""
        self.start()
        for prompt in (
            "what is the capital of France?",
            "thanks, that was helpful",
            "rewrite that paragraph to be shorter",
        ):
            self.assertIsNone(
                self.engine("UserPromptSubmit", {"session_id": "s1", "prompt": prompt}),
                f"adaptive mode must stay silent for: {prompt}",
            )

    def test_off_mode_is_completely_silent(self) -> None:
        for event in ("SessionStart", "UserPromptSubmit", "PostToolUseFailure"):
            self.assertIsNone(
                self.engine(
                    event,
                    {"session_id": "s1", "prompt": "build and test the web app"},
                    CLAUDE_CAPABILITY_BRIDGE_MODE="off",
                ),
                event,
            )

    def test_session_only_mode_skips_prompt_events(self) -> None:
        self.assertIsNotNone(
            self.engine(
                "SessionStart",
                {"session_id": "s1", "source": "startup"},
                CLAUDE_CAPABILITY_BRIDGE_MODE="session-only",
            )
        )
        self.assertIsNone(
            self.engine(
                "UserPromptSubmit",
                {"session_id": "s1", "prompt": "run the dev server and test the app"},
                CLAUDE_CAPABILITY_BRIDGE_MODE="session-only",
            )
        )

    def test_legacy_mode_reproduces_baseline_every_turn_behaviour(self) -> None:
        """Kept so A/B comparison against the old behaviour is possible."""
        mode = {"CLAUDE_CAPABILITY_BRIDGE_MODE": "legacy-every-turn"}
        self.engine("SessionStart", {"session_id": "s1"}, **mode)
        first = self.engine(
            "UserPromptSubmit", {"session_id": "s1", "prompt": "hello there"}, **mode
        )
        second = self.engine(
            "UserPromptSubmit", {"session_id": "s1", "prompt": "and again"}, **mode
        )
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(first, second, "legacy mode is deliberately unconditional")

    def test_every_emission_respects_the_output_budget(self) -> None:
        contexts = [
            self.start(),
            self.engine(
                "UserPromptSubmit",
                {
                    "session_id": "s1",
                    "prompt": "start the dev server and test the webapp in a browser",
                },
            ),
            self.engine("SessionStart", {"session_id": "s1", "source": "compact"}),
            self.engine(
                "PostToolUseFailure",
                {
                    "session_id": "s1",
                    "tool_name": "Bash",
                    "tool_response": {"error": "command not found: pnpm"},
                },
            ),
        ]
        for context in contexts:
            if context is not None:
                self.assertLessEqual(len(context), BUDGET)


class RoutingTestCase(HookTestCase):
    def test_clear_signal_routes_to_one_card(self) -> None:
        self.start()
        context = self.engine(
            "UserPromptSubmit",
            {
                "session_id": "s1",
                "prompt": "start the dev server and test the webapp in a browser",
            },
        )
        self.assertIsNotNone(context)
        self.assertIn("cards/browser-webapp.md", context)

    def test_card_pointer_is_not_repeated_for_the_same_card(self) -> None:
        self.start()
        prompt = {
            "session_id": "s1",
            "prompt": "start the dev server and test the webapp in a browser",
        }
        self.assertIsNotNone(self.engine("UserPromptSubmit", prompt))
        self.assertIsNone(
            self.engine("UserPromptSubmit", prompt),
            "a card already pointed at must not be re-injected every turn",
        )

    def test_switching_task_family_delivers_the_other_card(self) -> None:
        self.start()
        first = self.engine(
            "UserPromptSubmit",
            {
                "session_id": "s1",
                "prompt": "start the dev server and test the webapp in a browser",
            },
        )
        second = self.engine(
            "UserPromptSubmit",
            {"session_id": "s1", "prompt": "commit the staged files to the git repository"},
        )
        self.assertIn("cards/browser-webapp.md", first or "")
        self.assertIn("cards/filesystem-git.md", second or "")

    def test_ambiguous_prompt_does_not_fabricate_a_choice(self) -> None:
        self.start()
        for prompt in ("can you help me with this", "do the thing we discussed", "go on"):
            context = self.engine(
                "UserPromptSubmit", {"session_id": "s1", "prompt": prompt}
            )
            if context is not None:
                self.assertNotIn("Capability card:", context, prompt)

    def test_card_pointer_is_labelled_as_keyword_routing(self) -> None:
        """Routing is keyword-based; it must not read as verified tool state."""
        self.start()
        context = self.engine(
            "UserPromptSubmit",
            {
                "session_id": "s1",
                "prompt": "connect to the mcp connector and fetch the issue",
            },
        )
        self.assertIsNotNone(context)
        self.assertIn("not by verified tool state", context.lower())


class ContextEpochTestCase(HookTestCase):
    def test_compaction_marks_earlier_observations_stale(self) -> None:
        self.start()
        context = self.engine("SessionStart", {"session_id": "s1", "source": "compact"})
        self.assertIsNotNone(context)
        self.assertIn("COMPACT", context.upper())
        self.assertIn("STALE", context.upper())

    def test_compaction_rehydrates_a_short_kernel_not_the_library(self) -> None:
        self.start()
        context = self.engine("SessionStart", {"session_id": "s1", "source": "compact"})
        self.assertLessEqual(len(context), BUDGET)
        self.assertNotIn("## Minimal workflow", context)

    def test_card_is_reoffered_after_a_context_reset(self) -> None:
        """Dedup must not silently drop guidance the context no longer holds."""
        self.start()
        prompt = {
            "session_id": "s1",
            "prompt": "start the dev server and test the webapp in a browser",
        }
        self.assertIsNotNone(self.engine("UserPromptSubmit", prompt))
        self.assertIsNone(self.engine("UserPromptSubmit", prompt))
        self.engine("SessionStart", {"session_id": "s1", "source": "compact"})
        self.assertIsNotNone(
            self.engine("UserPromptSubmit", prompt),
            "after compaction the card must be offered again",
        )

    def test_all_documented_session_sources_are_handled(self) -> None:
        for source in ("startup", "resume", "clear", "compact", "fork"):
            context = self.engine(
                "SessionStart", {"session_id": f"s-{source}", "source": source}
            )
            self.assertIsNotNone(context, source)
            self.assertLessEqual(len(context), BUDGET, source)

    def test_fork_does_not_assume_inherited_process_state(self) -> None:
        context = self.engine("SessionStart", {"session_id": "f1", "source": "fork"})
        lowered = (context or "").lower()
        self.assertTrue(
            "re-observe" in lowered or "stale" in lowered or "not inherit" in lowered,
            f"fork guidance must not imply inherited live state: {context}",
        )

    def test_independent_sessions_get_independent_delivery(self) -> None:
        self.start(session="a")
        self.start(session="b")
        prompt_a = {
            "session_id": "a",
            "prompt": "start the dev server and test the webapp in a browser",
        }
        prompt_b = dict(prompt_a, session_id="b")
        self.assertIsNotNone(self.engine("UserPromptSubmit", prompt_a))
        self.assertIsNotNone(
            self.engine("UserPromptSubmit", prompt_b),
            "session b must not inherit session a's delivery record",
        )


class FailureGuidanceTestCase(HookTestCase):
    def failure(self, error: str, tool: str = "Bash", session: str = "s1"):
        return self.engine(
            "PostToolUseFailure",
            {
                "session_id": session,
                "tool_name": tool,
                "tool_response": {"error": error},
            },
        )

    def test_permission_denial_is_its_own_class(self) -> None:
        context = self.failure("permission denied by user")
        self.assertIn("PERMISSION_DENIED", context)
        self.assertIn("not permission", context.lower())

    def test_user_cancellation_is_not_treated_as_a_failure_to_retry(self) -> None:
        for wording in (
            "the user interrupted the request",
            "operation cancelled",
            "user rejected the tool call",
            "KeyboardInterrupt",
        ):
            context = self.failure(wording, session=f"c-{abs(hash(wording)) % 997}")
            self.assertIn("USER_CANCELLED", context, wording)
            self.assertIn("do not retry", context.lower(), wording)

    def test_distinct_errors_get_distinct_guidance(self) -> None:
        """Bug D: the baseline emitted one fixed reminder for every failure."""
        cases = {
            "no such tool: WebFetcher": "UNKNOWN_TOOL",
            "invalid_request_error: missing required property 'path'": "SCHEMA_ARGUMENT",
            "401 unauthorized: token expired": "AUTH_SESSION",
            "429 rate limit exceeded": "RATE_QUOTA",
            "mcp server not connected": "INTEGRATION_NOT_CONNECTED",
            "connection refused on port 3000": "PROCESS_READINESS",
            "command not found: pnpm": "ENVIRONMENT_DEPENDENCY",
        }
        seen = set()
        for index, (error, expected) in enumerate(cases.items()):
            context = self.failure(error, session=f"case-{index}")
            self.assertIsNotNone(context, error)
            self.assertIn(expected, context, f"{error!r} misclassified: {context}")
            seen.add(context)
        self.assertEqual(len(seen), len(cases), "each class needs distinct guidance")

    def test_unrecognised_error_is_not_confidently_classified(self) -> None:
        context = self.failure("zzzq wibble 7", session="u1")
        self.assertIn("UNKNOWN", context)

    def test_failure_guidance_states_it_arrives_after_execution(self) -> None:
        """Honesty about hook timing: it cannot have fixed the tool choice."""
        context = self.failure("permission denied by user", session="t1")
        self.assertIn("already ran", context.lower())

    def test_connector_failure_points_at_the_matching_card(self) -> None:
        context = self.failure("mcp server not connected", tool="jira", session="m1")
        self.assertIn("cards/mcp-connectors.md", context)

    def test_repeated_identical_failure_stops_growing_context(self) -> None:
        outputs = [
            self.failure("connection refused on port 3000", session="r1")
            for _ in range(5)
        ]
        self.assertIsNotNone(outputs[0])
        self.assertIsNone(outputs[-1], "repeated failures must eventually go quiet")
        escalation = " ".join(o for o in outputs if o).lower()
        self.assertIn("stop retrying", escalation)
        self.assertTrue(
            "report" in escalation or "different interface" in escalation,
            "escalation must push toward reporting a concrete block",
        )

    def test_failure_guidance_never_echoes_raw_error_text(self) -> None:
        secretish = "token=sk-live-ABCDEF123456"
        context = self.failure(f"401 unauthorized {secretish}", session="s2")
        self.assertNotIn(secretish, context or "")
        self.assertNotIn("sk-live", context or "")


class WrapperTestCase(HookTestCase):
    """Tests that actually execute the POSIX wrappers.

    Skipped, never silently passed, on a host that cannot run them: an absent
    shell or a CRLF checkout is a fact about the machine, not about the code.
    """

    def setUp(self) -> None:
        super().setUp()
        util.require_posix_shell(self, [self.wrapper(name) for name in WRAPPERS])

    def wrapper(self, name: str) -> Path:
        return util.BOOTSTRAP / name

    def test_wrappers_always_exit_zero(self) -> None:
        for name in (
            "session-start.sh",
            "user-prompt-submit.sh",
            "post-tool-use-failure.sh",
        ):
            for payload in ("", "{}", "not json at all", '{"session_id":"w1"}'):
                proc = util.run_hook(self.wrapper(name), payload, self.env())
                self.assertEqual(proc.returncode, 0, f"{name} <- {payload!r}")

    def test_wrapper_output_is_a_valid_hook_envelope(self) -> None:
        proc = util.run_hook(
            self.wrapper("session-start.sh"),
            json.dumps({"session_id": "w2", "source": "startup"}),
            self.env(),
        )
        context = util.hook_context(proc)
        self.assertIsNotNone(context)
        self.assertIn("CAPABILITY BRIDGE", context)

    def test_off_mode_short_circuits_in_the_wrapper(self) -> None:
        for name in (
            "session-start.sh",
            "user-prompt-submit.sh",
            "post-tool-use-failure.sh",
        ):
            proc = util.run_hook(
                self.wrapper(name),
                json.dumps({"session_id": "w3"}),
                self.env(CLAUDE_CAPABILITY_BRIDGE_MODE="off"),
            )
            self.assertEqual(proc.stdout.strip(), "", name)

    def _bin_with_broken_python(self) -> str:
        """A PATH whose python3/python resolve but fail immediately.

        This is the Windows Store "python3" alias in miniature: discoverable,
        resolvable, and unable to run anything.
        """
        fake = self.state_dir / "brokenbin"
        fake.mkdir(exist_ok=True)
        for name in ("python3", "python"):
            shim = fake / name
            shim.write_text("#!/bin/sh\nexit 9009\n", encoding="utf-8")
            shim.chmod(0o755)
        path = str(fake) + os.pathsep + os.environ.get("PATH", "")
        probe = subprocess.run(
            [util.posix_shell() or "bash", "-c", "command -v python3 || true"],
            capture_output=True,
            text=True,
            env={**os.environ, "PATH": path},
            timeout=60,
        )
        if fake.name not in probe.stdout:
            self.skipTest("cannot put a broken interpreter first on PATH here")
        return path

    def test_broken_interpreter_still_delivers_the_session_start_fallback(self) -> None:
        """A found-but-broken Python must degrade, not silence the hook."""
        proc = util.run_hook(
            self.wrapper("session-start.sh"),
            json.dumps({"session_id": "w8", "source": "startup"}),
            self.env(PATH=self._bin_with_broken_python()),
        )
        self.assertEqual(proc.returncode, 0)
        context = util.hook_context(proc)
        self.assertIsNotNone(
            context, "a broken interpreter must not silence session start"
        )
        self.assertIn("static fallback", context.lower())

    def test_broken_interpreter_keeps_the_prompt_hook_silent_in_adaptive(self) -> None:
        proc = util.run_hook(
            self.wrapper("user-prompt-submit.sh"),
            json.dumps({"session_id": "w9", "prompt": "anything"}),
            self.env(PATH=self._bin_with_broken_python()),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def _mirrored_bin_without_python(self):
        """POSIX: mirror the tools the wrapper needs, leaving Python behind.

        On Linux and macOS the interpreters share a directory with cat and
        bash, so the only way to drop one without the others is to build a
        private directory of symlinks.
        """
        fake = self.state_dir / "bin"
        fake.mkdir(exist_ok=True)
        linked = 0
        for tool in ("bash", "sh", "cat", "dirname", "env"):
            for base in ("/usr/bin", "/bin", "/usr/local/bin"):
                source = Path(base) / tool
                if not source.exists() or (fake / tool).exists():
                    continue
                try:
                    (fake / tool).symlink_to(source)
                except OSError:
                    break
                linked += 1
        return str(fake) if linked else None

    def _path_without_python_dirs(self):
        """Windows: keep every PATH entry that holds no python executable.

        Windows refuses symlinks without a privilege, but it does not need
        them: the interpreters live in their own directories, including the
        Store alias under WindowsApps, so dropping those directories leaves
        the Git tools the wrapper actually calls intact.
        """
        kept = []
        for entry in os.environ.get("PATH", "").split(os.pathsep):
            if not entry:
                continue
            try:
                names = {item.name.lower() for item in Path(entry).iterdir()}
            except OSError:
                continue
            if any(
                stem + suffix in names
                for stem in ("python", "python3")
                for suffix in ("", ".exe", ".bat", ".cmd")
            ):
                continue
            kept.append(entry)
        return os.pathsep.join(kept) if kept else None

    def _bin_without_python(self) -> str:
        """A PATH that still has a shell but no Python at all.

        The result is verified before it is used: if python still resolves, or
        if the tools the wrapper needs stopped resolving, the test skips. A
        PATH we cannot control proves nothing.
        """
        candidate = (
            self._path_without_python_dirs()
            if util.IS_WINDOWS
            else self._mirrored_bin_without_python()
        )
        if candidate is None:
            self.skipTest("cannot build a Python-less PATH on this platform")
        probe = subprocess.run(
            [
                util.posix_shell() or "bash",
                "-c",
                "command -v python3 python; command -v cat",
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "PATH": candidate},
            timeout=60,
        )
        found = probe.stdout.lower()
        if "python" in found or "cat" not in found:
            self.skipTest("cannot build a Python-less PATH on this platform")
        return candidate

    def test_session_start_has_a_static_fallback_without_python(self) -> None:
        proc = util.run_hook(
            self.wrapper("session-start.sh"),
            json.dumps({"session_id": "w4", "source": "startup"}),
            self.env(PATH=str(self._bin_without_python())),
        )
        self.assertEqual(proc.returncode, 0)
        context = util.hook_context(proc)
        self.assertIsNotNone(context, "session start must still say something")
        self.assertIn("static fallback", context.lower())

    def test_prompt_wrapper_stays_silent_without_python_in_adaptive(self) -> None:
        proc = util.run_hook(
            self.wrapper("user-prompt-submit.sh"),
            json.dumps({"session_id": "w5", "prompt": "anything"}),
            self.env(PATH=str(self._bin_without_python())),
        )
        self.assertEqual(proc.stdout.strip(), "")

    def test_prompt_wrapper_has_a_legacy_fallback_without_python(self) -> None:
        proc = util.run_hook(
            self.wrapper("user-prompt-submit.sh"),
            json.dumps({"session_id": "w6", "prompt": "anything"}),
            self.env(
                PATH=str(self._bin_without_python()),
                CLAUDE_CAPABILITY_BRIDGE_MODE="legacy-every-turn",
            ),
        )
        self.assertIsNotNone(util.hook_context(proc))

    def test_failure_wrapper_stays_silent_without_python(self) -> None:
        proc = util.run_hook(
            self.wrapper("post-tool-use-failure.sh"),
            json.dumps({"session_id": "w7", "tool_name": "Bash"}),
            self.env(PATH=str(self._bin_without_python())),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(
            proc.stdout.strip(),
            "",
            "a generic reminder that cannot match the failure is worse than silence",
        )


class DiagnosticsTestCase(HookTestCase):
    def run_cli(self, *args: str):
        env = dict(os.environ)
        env.update(self.env())
        return subprocess.run(
            [sys.executable, str(util.ENGINE), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
        )

    def test_selftest_passes(self) -> None:
        proc = self.run_cli("--selftest")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_diagnose_reports_mode_budget_and_delivery_honestly(self) -> None:
        proc = self.run_cli("--diagnose")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout
        self.assertIn("adaptive", out)
        self.assertIn("not tokens", out)
        self.assertIn("best-effort", out)
        for mode in ("off", "session-only", "adaptive", "legacy-every-turn"):
            self.assertIn(mode, out)


class WrapperStaticTestCase(HookTestCase):
    """Checks on the wrapper *files*. These are platform-independent."""

    def wrapper(self, name: str) -> Path:
        return util.BOOTSTRAP / name

    def test_no_python_never_auto_installs_anything(self) -> None:
        for name in WRAPPERS:
            text = util.read_text(self.wrapper(name))
            for forbidden in ("pip ", "pip3 ", "apt-get", "dnf ", "brew ", "curl ", "wget "):
                self.assertNotIn(forbidden, text, f"{name} must not install anything")

    def test_shell_wrappers_are_checked_out_with_lf_endings(self) -> None:
        """CRLF makes bash die with exit 127 before the hook can emit anything."""
        offenders = sorted(p.name for p in util.shell_scripts() if util.has_crlf(p))
        self.assertEqual(
            offenders,
            [],
            "CRLF line endings break the shell wrappers. .gitattributes pins *.sh "
            "to LF; repair an existing checkout with: git add --renormalize . "
            "&& git checkout -- .",
        )


if __name__ == "__main__":
    unittest.main()
