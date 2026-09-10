"""Content-contract tests.

These guard the *structure and honesty* of the guidance layer:

* the kernel keeps the rules that must never be optimized away;
* the card index is generated, fresh, and only points at real cards;
* profiles describe contracts and never assert live capability or permission;
* the status vocabulary is one vocabulary, shared by prose and runtime;
* content budgets are enforced and are honestly labelled as characters.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

import bridge_test_utils as util

sys.path.insert(0, str(util.ROOT / "scripts"))

from bridgelib import load_skill_metadata  # noqa: E402
from bridgelib.cards import REQUIRED_SECTIONS, load_card, verify_index  # noqa: E402
from bridgelib.refs import missing_references  # noqa: E402

STATUS_VALUES = (
    "ANNOUNCED",
    "SCHEMA_SEEN",
    "USED_OK",
    "PERMISSION_BLOCKED",
    "UNAVAILABLE",
    "STALE",
    "UNKNOWN",
)


class KernelContractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.meta = load_skill_metadata(util.ROOT / "SKILL.md")
        cls.body = cls.meta.body
        cls.lower = cls.body.lower()

    def test_skill_name_is_unchanged(self) -> None:
        """Renaming the Skill breaks every existing install and reference."""
        self.assertEqual(self.meta.name, "claude-capability-bridge")

    def test_version_is_not_downgraded_below_baseline(self) -> None:
        parts = [int(p) for p in self.meta.version.split("-")[0].split(".")]
        self.assertGreaterEqual(
            tuple(parts), (0, 9, 0), "baseline was 0.8.0; this work is a minor bump"
        )

    def test_kernel_keeps_critical_rules(self) -> None:
        required = {
            "fast path": "answer directly",
            "no invention": "never invent",
            "conceptual vs callable": "is not a callable tool name",
            "permission boundary": "permission is not availability",
            "tool vs task success": "tool success is not task success",
            "stale state": "stale",
            "evidence-based retry": "retry needs a changed variable",
            "unknown stays unknown": "unknown stays unknown",
            "untrusted content": "data, not instruction",
            "security over cache": "security outranks cache",
            "delegation": "specialized skill",
        }
        for label, needle in required.items():
            self.assertIn(needle.lower(), self.lower, f"kernel lost rule: {label}")

    def test_kernel_has_a_self_check_checklist(self) -> None:
        self.assertIn("- [ ]", self.body)

    def test_kernel_carries_no_live_state(self) -> None:
        """Anything volatile in the kernel would change a would-be stable prefix."""
        volatile = re.compile(
            r"(19|20)\d{2}-\d{2}-\d{2}"
            r"|\b\d{2}:\d{2}:\d{2}\b"
            r"|session[_-]?id\s*[:=]"
            r"|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            re.IGNORECASE,
        )
        self.assertIsNone(volatile.search(self.body))

    def test_kernel_makes_no_unsupportable_cache_claim(self) -> None:
        for claim in (
            "guaranteed cache",
            "guarantees a cache",
            "enables prompt caching",
            "cache hit rate improved",
            "always available",
        ):
            self.assertNotIn(claim, self.lower, f"unsupportable claim: {claim}")

    def test_kernel_routes_to_every_card(self) -> None:
        """A card nobody can find is dead weight in the package."""
        for path in sorted((util.ROOT / "cards").glob("*.md")):
            self.assertIn(
                path.name,
                self.body,
                f"cards/{path.name} is not reachable from the kernel routing table",
            )

    def test_kernel_points_at_the_generated_index(self) -> None:
        self.assertIn("cards/index.json", self.body)


class CardContractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cards_dir = util.ROOT / "cards"
        cls.card_paths = sorted(cls.cards_dir.glob("*.md"))

    def test_cards_exist(self) -> None:
        self.assertGreaterEqual(len(self.card_paths), 8)

    def test_every_card_has_the_required_sections(self) -> None:
        for path in self.card_paths:
            body = util.read_text(path)
            for section in REQUIRED_SECTIONS:
                self.assertIn(section, body, f"{path.name} is missing {section}")

    def test_every_card_has_an_anti_pattern_and_a_done_criterion(self) -> None:
        for path in self.card_paths:
            lowered = util.read_text(path).lower()
            self.assertIn("anti-pattern", lowered, f"{path.name} has no anti-pattern")
            self.assertIn("done means", lowered, f"{path.name} has no definition of done")

    def test_committed_index_is_fresh(self) -> None:
        """The index is a build artifact; a stale one silently misroutes work."""
        index = verify_index(self.cards_dir)
        self.assertEqual(index["index_version"], 1)

    def test_index_only_points_at_existing_cards(self) -> None:
        index = json.loads(util.read_text(self.cards_dir / "index.json"))
        for card in index["cards"]:
            self.assertTrue(
                (util.ROOT / card["path"]).is_file(), f"missing {card['path']}"
            )

    def test_index_is_not_a_tool_registry(self) -> None:
        """The catalog must not read as proof that tools exist."""
        index = json.loads(util.read_text(self.cards_dir / "index.json"))
        note = index["note"].lower()
        self.assertIn("not callable tool names", note)
        self.assertIn("nothing here proves", note)

    def test_routing_signals_are_unambiguous(self) -> None:
        index = json.loads(util.read_text(self.cards_dir / "index.json"))
        owner: dict[str, str] = {}
        clashes: list[str] = []
        for card in index["cards"]:
            for signal in card["signals"]:
                if signal in owner:
                    clashes.append(f"{signal}: {owner[signal]} vs {card['id']}")
                owner[signal] = card["id"]
        self.assertEqual(clashes, [], "shared signals make routing ambiguous")

    def test_card_related_references_resolve(self) -> None:
        for path in self.card_paths:
            card = load_card(path)
            for ref in card["related_references"]:
                self.assertTrue(
                    (util.ROOT / ref).is_file(),
                    f"{path.name} points at missing reference {ref}",
                )

    def test_cards_do_not_promise_that_a_tool_exists(self) -> None:
        for path in self.card_paths:
            lowered = util.read_text(path).lower()
            for claim in ("is always available", "will always exist", "is guaranteed to"):
                self.assertNotIn(claim, lowered, f"{path.name} asserts {claim!r}")


class ProfileContractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = sorted((util.ROOT / "profiles").glob("*.md"))

    def test_expected_profiles_exist(self) -> None:
        names = {p.stem for p in self.paths}
        self.assertTrue({"claude-code", "desktop", "cowork", "generic"} <= names)

    def test_profiles_declare_they_are_not_live_state(self) -> None:
        for path in self.paths:
            self.assertIn(
                "not live state",
                util.read_text(path).lower(),
                f"{path.name} must say it describes contracts, not live state",
            )

    def test_profiles_do_not_guarantee_capabilities(self) -> None:
        banned = (
            "a browser is available",
            "mcp is connected",
            "network is available",
            "tools are permitted",
        )
        for path in self.paths:
            text = util.read_text(path).lower()
            for claim in banned:
                if claim not in text:
                    continue
                # allowed only as an explicit denial
                for line in text.splitlines():
                    if claim in line:
                        self.assertTrue(
                            any(
                                marker in line
                                for marker in (
                                    "not",
                                    "never",
                                    "nothing",
                                    "no ",
                                    "assume",
                                    "unknown",
                                    "proof",
                                )
                            ),
                            f"{path.name} asserts {claim!r}: {line.strip()!r}",
                        )

    def test_generic_profile_documents_the_status_vocabulary(self) -> None:
        text = util.read_text(util.ROOT / "profiles" / "generic.md")
        for status in STATUS_VALUES:
            self.assertIn(status, text, f"generic profile omits status {status}")


class SharedVocabularyTestCase(unittest.TestCase):
    def test_status_vocabulary_matches_the_runtime(self) -> None:
        """Prose and hook engine must not drift into two different enums."""
        engine = util.read_text(util.ROOT / "bootstrap" / "bridge_hook.py")
        match = re.search(r"STATUS_VALUES\s*=\s*\(([^)]*)\)", engine, re.DOTALL)
        self.assertIsNotNone(match, "bridge_hook.py must define STATUS_VALUES")
        runtime = tuple(re.findall(r"\"([A-Z_]+)\"", match.group(1)))
        self.assertEqual(set(runtime), set(STATUS_VALUES))

    def test_kernel_documents_the_same_statuses(self) -> None:
        body = load_skill_metadata(util.ROOT / "SKILL.md").body
        for status in STATUS_VALUES:
            self.assertIn(status, body, f"kernel omits status {status}")

    def test_failure_card_hints_point_at_real_cards(self) -> None:
        engine = util.read_text(util.ROOT / "bootstrap" / "bridge_hook.py")
        match = re.search(r"FAILURE_CARD_HINTS\s*=\s*\{([^}]*)\}", engine, re.DOTALL)
        self.assertIsNotNone(match)
        for card_id in re.findall(r":\s*\"([a-z0-9-]+)\"", match.group(1)):
            self.assertTrue(
                (util.ROOT / "cards" / f"{card_id}.md").is_file(),
                f"hook hints at a card that does not exist: {card_id}",
            )


class ReferenceGraphTestCase(unittest.TestCase):
    def test_no_broken_local_references_in_source(self) -> None:
        self.assertEqual(missing_references(util.ROOT), [])

    def test_legacy_reference_entrypoint_still_exists(self) -> None:
        """Old paths must keep working or explicitly redirect."""
        readme = util.ROOT / "references" / "README.md"
        self.assertTrue(readme.is_file())
        lowered = util.read_text(readme).lower()
        self.assertTrue(
            "cards/" in lowered and "profiles/" in lowered,
            "references/README.md must map legacy routing onto the new structure",
        )


class BudgetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(
            util.read_text(util.ROOT / "config" / "content-budgets.json")
        )
        cls.budgets = cls.config["budgets"]

    def test_budget_unit_is_honestly_labelled(self) -> None:
        self.assertEqual(self.config["unit"], "characters")
        note = self.config["unit_note"].lower()
        self.assertIn("not token counts", note)

    def test_kernel_is_within_budget(self) -> None:
        body = load_skill_metadata(util.ROOT / "SKILL.md").body
        self.assertLessEqual(len(body), self.budgets["skill_body_chars"])

    def test_cards_are_within_budget(self) -> None:
        for path in sorted((util.ROOT / "cards").glob("*.md")):
            self.assertLessEqual(
                len(util.read_text(path)),
                self.budgets["card_chars"],
                f"{path.name} exceeds the card budget",
            )

    def test_profiles_are_within_budget(self) -> None:
        for path in sorted((util.ROOT / "profiles").glob("*.md")):
            self.assertLessEqual(
                len(util.read_text(path)),
                self.budgets["profile_chars"],
                f"{path.name} exceeds the profile budget",
            )

    def test_hook_output_budget_matches_the_runtime_default(self) -> None:
        engine = util.read_text(util.ROOT / "bootstrap" / "bridge_hook.py")
        match = re.search(r"DEFAULT_MAX_CONTEXT_CHARS\s*=\s*(\d+)", engine)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group(1)), self.budgets["hook_output_chars"])


if __name__ == "__main__":
    unittest.main()
