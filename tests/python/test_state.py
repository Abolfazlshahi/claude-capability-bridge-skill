"""State handling tests.

State is best-effort bookkeeping for the hook engine. It must never block a
turn, never escape its directory, and never be trusted as a permission cache.
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import bridge_test_utils as util


class StateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.state_dir = self.root / "state"
        self.state_dir.mkdir()
        self.addCleanup(self._tmp.cleanup)

    def env(self, **extra):
        env = {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(self.state_dir)}
        env.update(extra)
        return env

    def run_event(self, event: str, payload: dict, **extra):
        proc = util.run_engine(event, json.dumps(payload), self.env(**extra))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc

    def state_files(self):
        return sorted(p.name for p in self.state_dir.glob("session-*.json"))

    def load(self, key: str) -> dict:
        return json.loads((self.state_dir / f"session-{key}.json").read_text("utf-8"))


class StateLifecycleTestCase(StateTestCase):
    def test_session_start_creates_one_state_file(self) -> None:
        self.run_event("SessionStart", {"session_id": "abc", "source": "startup"})
        self.assertEqual(self.state_files(), ["session-abc.json"])
        state = self.load("abc")
        for key in ("schema", "engine", "session", "epoch_id", "cards", "failures"):
            self.assertIn(key, state)

    def test_state_file_is_private(self) -> None:
        self.run_event("SessionStart", {"session_id": "abc"})
        mode = (self.state_dir / "session-abc.json").stat().st_mode
        self.assertEqual(stat.S_IMODE(mode) & 0o077, 0, "state must not be group/world readable")

    def test_missing_state_is_not_an_error(self) -> None:
        proc = self.run_event("UserPromptSubmit", {"session_id": "fresh", "prompt": "hi"})
        self.assertEqual(proc.returncode, 0)

    def test_corrupt_state_recovers_and_flags_itself(self) -> None:
        (self.state_dir / "session-c1.json").write_text("{{{not json", encoding="utf-8")
        self.run_event("SessionStart", {"session_id": "c1", "source": "startup"})
        state = self.load("c1")
        self.assertTrue(state["recovered_from_corruption"])
        self.assertEqual(state["session"], "c1")

    def test_state_from_a_future_schema_is_discarded_not_trusted(self) -> None:
        (self.state_dir / "session-c2.json").write_text(
            json.dumps({"schema": 999, "cards": {"browser-webapp": "USED_OK"}}),
            encoding="utf-8",
        )
        self.run_event("SessionStart", {"session_id": "c2"})
        state = self.load("c2")
        self.assertTrue(state["recovered_from_corruption"])
        self.assertEqual(state["cards"], {})

    def test_uncreatable_state_directory_never_blocks_the_turn(self) -> None:
        """State that cannot be created must degrade, not fail the turn.

        A regular file is used as the parent so the failure is filesystem
        independent: chmod bits are not honoured on every sandbox.
        """
        blocker = self.root / "blocker"
        blocker.write_text("not a directory", encoding="utf-8")
        proc = util.run_engine(
            "SessionStart",
            json.dumps({"session_id": "ro", "source": "startup"}),
            {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(blocker / "state")},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIsNotNone(
            util.hook_context(proc), "guidance must survive an unwritable state dir"
        )
        self.assertEqual(blocker.read_text("utf-8"), "not a directory")

    def test_read_only_state_directory_never_blocks_the_turn(self) -> None:
        locked = self.root / "locked"
        locked.mkdir()
        os.chmod(locked, 0o500)
        self.addCleanup(os.chmod, locked, 0o700)
        probe = locked / ".probe"
        try:
            probe.write_text("x", encoding="utf-8")
            probe.unlink()
            self.skipTest("filesystem ignores directory mode bits")
        except OSError:
            pass
        proc = util.run_engine(
            "SessionStart",
            json.dumps({"session_id": "ro2", "source": "startup"}),
            {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(locked)},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIsNotNone(util.hook_context(proc))
        self.assertEqual(list(locked.glob("*")), [])

    def test_no_temporary_files_are_left_behind(self) -> None:
        for index in range(3):
            self.run_event("SessionStart", {"session_id": f"t{index}"})
        self.assertEqual(list(self.state_dir.glob(".tmp-state-*")), [])


class StateIsolationTestCase(StateTestCase):
    def test_independent_sessions_get_independent_files(self) -> None:
        self.run_event("SessionStart", {"session_id": "one"})
        self.run_event("SessionStart", {"session_id": "two"})
        self.assertEqual(self.state_files(), ["session-one.json", "session-two.json"])

    def test_one_corrupt_session_does_not_damage_another(self) -> None:
        self.run_event("SessionStart", {"session_id": "good"})
        (self.state_dir / "session-bad.json").write_text("garbage", encoding="utf-8")
        self.run_event("SessionStart", {"session_id": "bad"})
        self.assertFalse(self.load("good")["recovered_from_corruption"])

    def test_concurrent_hooks_keep_the_file_parseable(self) -> None:
        self.run_event("SessionStart", {"session_id": "race"})
        payloads = [
            json.dumps({"session_id": "race", "prompt": f"commit the repo change {i}"})
            for i in range(10)
        ]
        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(
                pool.map(
                    lambda body: util.run_engine("UserPromptSubmit", body, self.env()),
                    payloads,
                )
            )
        for proc in results:
            self.assertEqual(proc.returncode, 0, proc.stderr)
        state = self.load("race")  # must still be valid JSON
        self.assertEqual(state["session"], "race")
        self.assertEqual(list(self.state_dir.glob(".tmp-state-*")), [])

    def test_session_key_is_sanitised(self) -> None:
        self.run_event("SessionStart", {"session_id": "../../evil id!@#"})
        names = self.state_files()
        self.assertEqual(len(names), 1)
        self.assertNotIn("/", names[0])
        self.assertNotIn("..", names[0])

    def test_absent_session_id_uses_a_stable_placeholder(self) -> None:
        self.run_event("SessionStart", {"source": "startup"})
        self.assertEqual(self.state_files(), ["session-no-session.json"])

    def test_state_is_never_written_inside_the_package(self) -> None:
        """A state dir pointing into the install directory must be refused."""
        forbidden = util.ROOT / ".state-must-not-exist"
        fake_home = self.root / "home"
        fake_home.mkdir()
        proc = util.run_engine(
            "SessionStart",
            json.dumps({"session_id": "inside", "source": "startup"}),
            {
                "CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(forbidden),
                "HOME": str(fake_home),
            },
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(forbidden.exists(), "engine wrote state into the package tree")
        fallback = fake_home / ".local" / "state" / "claude-capability-bridge"
        self.assertTrue(fallback.exists(), "expected an OS-appropriate fallback location")


class ContextEpochStateTestCase(StateTestCase):
    def test_compaction_is_recorded_as_a_context_boundary(self) -> None:
        self.run_event("SessionStart", {"session_id": "e1", "source": "startup"})
        before = self.load("e1")
        self.run_event(
            "UserPromptSubmit",
            {"session_id": "e1", "prompt": "start the dev server and test the webapp in a browser"},
        )
        self.assertTrue(self.load("e1")["cards"], "card delivery should be recorded")
        self.run_event("SessionStart", {"session_id": "e1", "source": "compact"})
        after = self.load("e1")
        self.assertGreater(after["epoch_id"], before["epoch_id"])
        self.assertEqual(after["epoch_source"], "compact")
        self.assertEqual(after["cards"], {}, "card delivery must not survive compaction")

    def test_delivery_confirmation_is_never_claimed(self) -> None:
        self.run_event("SessionStart", {"session_id": "d1"})
        self.assertEqual(self.load("d1")["delivery_confirmation"], "unavailable")

    def test_repeated_failures_are_counted_not_accumulated_as_text(self) -> None:
        for _ in range(4):
            self.run_event(
                "PostToolUseFailure",
                {
                    "session_id": "f1",
                    "tool_name": "Bash",
                    "tool_response": {"error": "connection refused on port 3000"},
                },
            )
        failures = self.load("f1")["failures"]
        self.assertTrue(failures)
        for value in failures.values():
            self.assertIsInstance(value, int)


class TelemetryTestCase(StateTestCase):
    def telemetry_lines(self):
        path = self.state_dir / "telemetry.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]

    def test_telemetry_is_off_by_default(self) -> None:
        self.run_event("SessionStart", {"session_id": "tel"})
        self.assertFalse((self.state_dir / "telemetry.jsonl").exists())

    def test_telemetry_is_opt_in_and_marked_redacted(self) -> None:
        self.run_event(
            "SessionStart",
            {"session_id": "tel", "source": "startup"},
            CLAUDE_CAPABILITY_BRIDGE_TELEMETRY="1",
        )
        lines = self.telemetry_lines()
        self.assertTrue(lines, "opt-in telemetry should record something")
        for record in lines:
            self.assertTrue(record.get("redacted"))

    def test_telemetry_never_fabricates_cache_numbers(self) -> None:
        self.run_event(
            "UserPromptSubmit",
            {"session_id": "tel2", "prompt": "commit the repository changes"},
            CLAUDE_CAPABILITY_BRIDGE_TELEMETRY="on",
        )
        for record in self.telemetry_lines():
            for key in (
                "cache_read_input_tokens",
                "cache_creation_input_tokens",
                "input_tokens",
                "ttft_ms",
            ):
                if key in record:
                    self.assertIsNone(
                        record[key], f"{key} must stay null, never a fake zero"
                    )

    def test_telemetry_does_not_store_prompt_text(self) -> None:
        secret = "ZZTOPSECRETPROMPT"
        self.run_event(
            "UserPromptSubmit",
            {"session_id": "tel3", "prompt": f"deploy the {secret} service"},
            CLAUDE_CAPABILITY_BRIDGE_TELEMETRY="true",
        )
        raw = (self.state_dir / "telemetry.jsonl").read_text("utf-8")
        self.assertNotIn(secret, raw)


if __name__ == "__main__":
    unittest.main()
