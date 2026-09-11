"""Prompt-cache *invariant* tests.

SCOPE, read this before quoting any result from this file:

These are offline structural invariants about what this project emits and
ships. They do NOT measure prompt cache hits, token counts, TTL behaviour,
billing, or provider routing. A green run here is not a cache benchmark and
must never be reported as one. Real cache behaviour can only be observed from
a live deployment's usage fields, and for a gateway, from the request that
leaves the gateway - not the one that enters it.

What these tests do prove: this project does not itself rewrite stable
content, does not inject volatile text into the fixed core, and produces
byte-stable output for identical input.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

import bridge_test_utils as util

VOLATILE_PATTERNS = (
    re.compile(r"\b20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}"),  # ISO timestamp
    re.compile(r"\bbuilt (?:at|on)\b", re.I),
    re.compile(r"\bgenerated (?:at|on)\b", re.I),
    re.compile(r"\bbuild[-_ ]?(?:time|id)\b", re.I),
    re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"),
)

STATE_KEYS = (
    "epoch_id",
    "kernel_epoch",
    "recovered_from_corruption",
    "delivery_confirmation",
)

# A document may quote a forbidden claim in order to reject it, so phrase checks
# have to be negation aware, like the validator's.
NEGATIONS = (
    "not ",
    "not:",
    "never",
    "cannot",
    "avoid",
    "don't",
    "instead of",
    "rather than",
    "no guarantee",
)


def negated(line: str) -> bool:
    return any(marker in line.lower() for marker in NEGATIONS)


def normalise(text: str) -> str:
    """Lowercase, drop Markdown decoration, and collapse wrapped lines."""
    stripped = re.sub(r"[*`>]", " ", text.lower())
    return re.sub(r"\s+", " ", stripped)

FIXED_CORE = ("SKILL.md",)
FIXED_DIRS = ("cards", "profiles")


class CacheInvariantTestCase(unittest.TestCase):
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

    def emit(self, event: str, payload: dict, **extra):
        proc = util.run_engine(event, json.dumps(payload), self.env(**extra))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout, util.hook_context(proc)


class StablePrefixContentTestCase(CacheInvariantTestCase):
    def fixed_files(self):
        files = [util.ROOT / name for name in FIXED_CORE]
        for directory in FIXED_DIRS:
            files.extend(sorted((util.ROOT / directory).glob("*.md")))
        files.append(util.ROOT / "cards" / "index.json")
        return files

    def test_fixed_core_has_no_volatile_content(self) -> None:
        """Timestamps or random ids in stable content would break reuse."""
        for path in self.fixed_files():
            text = util.read_text(path)
            for pattern in VOLATILE_PATTERNS:
                self.assertIsNone(
                    pattern.search(text),
                    f"{path.relative_to(util.ROOT)} contains volatile content",
                )

    def test_card_index_is_deterministic(self) -> None:
        """Regeneration must be byte-identical, so the build cannot churn."""
        proc = util.run_script("build_card_index.py", "--check", check=False)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

        source = util.copy_source_tree(self.root / "repo")
        index = source / "cards" / "index.json"
        first = index.read_bytes()
        util.run_script(
            "build_card_index.py", cwd=source, scripts_dir=source / "scripts"
        )
        second = index.read_bytes()
        util.run_script(
            "build_card_index.py", cwd=source, scripts_dir=source / "scripts"
        )
        third = index.read_bytes()
        self.assertEqual(first, second)
        self.assertEqual(second, third)

    def test_catalog_order_is_stable_and_sorted(self) -> None:
        index = json.loads(util.read_text(util.ROOT / "cards" / "index.json"))
        ids = [card["id"] for card in index["cards"]]
        self.assertEqual(ids, sorted(ids), "card order must not drift between builds")

    def test_two_builds_produce_identical_packages(self) -> None:
        source = util.copy_source_tree(self.root / "repo2")
        scripts = source / "scripts"
        first = self.root / "out-a"
        second = self.root / "out-b"
        for out in (first, second):
            util.run_script(
                "package_skill.py", "--out", str(out), cwd=source, scripts_dir=scripts
            )
        self.assertEqual(util.tree_snapshot(first), util.tree_snapshot(second))


class NoStateInStableContentTestCase(CacheInvariantTestCase):
    def test_emitted_context_never_carries_state_fields(self) -> None:
        """Live state belongs in a new message, never in reusable content."""
        emissions = []
        for event, payload in (
            ("SessionStart", {"session_id": "cache1", "source": "startup"}),
            (
                "UserPromptSubmit",
                {
                    "session_id": "cache1",
                    "prompt": "start the dev server and test the webapp in a browser",
                },
            ),
            ("SessionStart", {"session_id": "cache1", "source": "compact"}),
        ):
            _, context = self.emit(event, payload)
            if context:
                emissions.append(context)
        self.assertTrue(emissions)
        for context in emissions:
            self.assertTrue(
                "cache1" not in context, "session id must not leak into context"
            )
            for key in STATE_KEYS:
                self.assertTrue(
                    key not in context, f"{key} must stay in the state file"
                )
            for pattern in VOLATILE_PATTERNS:
                self.assertIsNone(pattern.search(context))

    def test_identical_input_produces_byte_identical_output(self) -> None:
        payload = {"session_id": "same", "source": "startup"}
        first_dir = self.root / "s1"
        second_dir = self.root / "s2"
        first_dir.mkdir()
        second_dir.mkdir()
        a = util.run_engine(
            "SessionStart",
            json.dumps(payload),
            {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(first_dir)},
        )
        b = util.run_engine(
            "SessionStart",
            json.dumps(payload),
            {"CLAUDE_CAPABILITY_BRIDGE_STATE_DIR": str(second_dir)},
        )
        self.assertEqual(a.stdout, b.stdout, "hook text must not vary run to run")

    def test_card_delivery_does_not_rewrite_the_kernel(self) -> None:
        """A card is appended context; it must not restate the whole kernel."""
        _, kernel = self.emit(
            "SessionStart", {"session_id": "k1", "source": "startup"}
        )
        _, card = self.emit(
            "UserPromptSubmit",
            {
                "session_id": "k1",
                "prompt": "start the dev server and test the webapp in a browser",
            },
        )
        self.assertIsNotNone(kernel)
        self.assertIsNotNone(card)
        self.assertNotIn("CAPABILITY BRIDGE PROTOCOL", card)
        self.assertLess(len(card), len(kernel) + 1200)

    def test_hook_runs_never_modify_packaged_content(self) -> None:
        watched = {}
        for name in FIXED_CORE:
            watched[name] = (util.ROOT / name).read_bytes()
        for directory in FIXED_DIRS + ("references", "bootstrap"):
            watched.update(
                {
                    str(path.relative_to(util.ROOT)): path.read_bytes()
                    for path in sorted((util.ROOT / directory).rglob("*"))
                    if path.is_file()
                }
            )
        sequence = (
            ("SessionStart", {"session_id": "imm", "source": "startup"}),
            ("UserPromptSubmit", {"session_id": "imm", "prompt": "commit the repo"}),
            (
                "PostToolUseFailure",
                {
                    "session_id": "imm",
                    "tool_name": "Bash",
                    "tool_response": {"error": "connection refused"},
                },
            ),
            ("SessionStart", {"session_id": "imm", "source": "compact"}),
        )
        for event, payload in sequence:
            self.emit(event, payload)
        for relative, before in watched.items():
            self.assertEqual(
                (util.ROOT / relative).read_bytes(),
                before,
                f"{relative} changed while hooks ran",
            )

    def test_compaction_is_the_only_thing_that_reissues_the_kernel(self) -> None:
        """Steady-state turns add nothing, so the prefix keeps growing linearly."""
        self.emit("SessionStart", {"session_id": "q1", "source": "startup"})
        quiet = [
            self.emit("UserPromptSubmit", {"session_id": "q1", "prompt": text})[1]
            for text in ("hello", "thanks", "what did you mean by that")
        ]
        self.assertEqual(quiet, [None, None, None])
        _, rehydrated = self.emit(
            "SessionStart", {"session_id": "q1", "source": "compact"}
        )
        self.assertIn("CAPABILITY BRIDGE PROTOCOL", rehydrated)


class HonestClaimsTestCase(CacheInvariantTestCase):
    FORBIDDEN = (
        "guaranteed cache",
        "guarantees a cache",
        "guaranteed prompt cache",
        "always hits the cache",
        "cache hit guaranteed",
        "improves cache hit",
    )

    def test_no_document_promises_a_cache_improvement(self) -> None:
        """Quoting a forbidden claim in order to reject it is allowed.

        The scope is the paragraph, not the line: a rejection frequently sits on
        the following wrapped line, so line scope produces false positives.
        """
        for path in util.markdown_files(util.ROOT):
            if "dist/" in path.as_posix():
                continue
            for block in re.split(r"\n\s*\n", util.read_text(path)):
                paragraph = normalise(block)
                for phrase in self.FORBIDDEN:
                    if phrase in paragraph and not negated(paragraph):
                        self.fail(
                            f"{path.name} oversells caching: {paragraph.strip()[:140]}"
                        )

    def test_cache_contract_states_who_controls_what(self) -> None:
        text = normalise(util.read_text(util.ROOT / "docs" / "cache-contract.md"))
        for expected in ("skill", "plugin", "host", "gateway", "provider"):
            self.assertTrue(expected in text, f"cache contract omits {expected}")
        self.assertTrue(
            "requires verification on a real deployment" in text,
            "cache contract must use the approved wording",
        )

    def test_cache_contract_refuses_markdown_level_cache_activation(self) -> None:
        text = normalise(util.read_text(util.ROOT / "docs" / "cache-contract.md"))
        self.assertTrue(
            "mark a block as cacheable" in text,
            "the contract must name what Markdown cannot do",
        )
        self.assertTrue(
            "messages api compatibility is not anthropic cache support" in text,
            "the contract must separate API compatibility from cache support",
        )
        self.assertTrue(
            "best-effort" in text or "best effort" in text,
            "the contract must call hook delivery best-effort",
        )


if __name__ == "__main__":
    unittest.main()
