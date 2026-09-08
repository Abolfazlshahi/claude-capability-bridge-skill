#!/usr/bin/env python3
"""Offline structural validator for the Claude Capability Bridge Skill tree."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"

REQUIRED_REFS = {
    "activation-and-memory.md",
    "browser-workflows.md",
    "capability-catalog.md",
    "capability-model.md",
    "code-and-shell.md",
    "computer-use.md",
    "desktop-workflows.md",
    "failure-recovery.md",
    "mcp-and-connectors.md",
    "mcp-deep-dive.md",
    "projects-and-files.md",
    "provider-adaptation.md",
    "security-and-permissions.md",
    "skills-and-plugins.md",
    "task-recipes.md",
    "tool-use-patterns.md",
    "verification.md",
    "webapp-verification.md",
    "README.md",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not SKILL.is_file():
        fail("SKILL.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")

    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("YAML frontmatter closing delimiter is missing")

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match:
        fail("frontmatter name is missing")
    if not desc_match:
        fail("frontmatter description is missing")

    name = name_match.group(1).strip().strip("\"")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(f"invalid Skill name: {name!r}")

    description = desc_match.group(1).strip()
    if not description or len(description) > 1024:
        fail("description must be non-empty and <= 1024 characters")

    if not REFS.is_dir():
        fail("references directory is missing")

    missing = sorted(ref for ref in REQUIRED_REFS if not (REFS / ref).is_file())
    if missing:
        fail("missing references: " + ", ".join(missing))

    referenced_names = set(re.findall(r"`references/([^`]+)`", text))
    unknown = sorted(referenced_names - REQUIRED_REFS)
    if unknown:
        fail("SKILL.md references files that do not exist in the required map: " + ", ".join(unknown))

    print("PASS: Skill structure and frontmatter checks passed")
    print(f"Skill: {name}")
    print(f"References: {len(REQUIRED_REFS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
