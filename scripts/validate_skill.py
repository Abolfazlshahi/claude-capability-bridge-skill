#!/usr/bin/env python3
"""Offline structural validator for the Claude Capability Bridge Skill.

This does not replace the official skills-ref validator. It adds repository-specific
checks for reference routing, evaluations, benchmark files, and critical regression scenarios.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
EVALS = ROOT / "evals" / "evals.json"
BENCHMARKS = ROOT / "benchmarks" / "scenarios.yaml"

REQUIRED_REFS = {
    "activation-and-memory.md", "async-subagents-and-remote.md", "browser-workflows.md",
    "capability-catalog.md", "capability-handshake.md", "capability-model.md",
    "claude-desktop-current-map.md", "code-and-shell.md", "computer-use.md",
    "desktop-extensions.md", "desktop-workflows.md", "evaluation-and-attribution.md",
    "failure-recovery.md", "interactive-surfaces.md", "mcp-and-connectors.md",
    "mcp-deep-dive.md", "projects-and-files.md", "provider-adaptation.md",
    "custom-provider-transport.md", "project-recognition-and-launch.md", "runtime-boundaries.md",
    "security-and-permissions.md", "session-memory.md", "skills-and-plugins.md",
    "source-notes.md", "task-recipes.md", "tool-schema-literacy.md", "tool-use-patterns.md",
    "verification.md", "webapp-verification.md", "workspace-map.md", "README.md",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARN: {message}")


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
    compatibility_match = re.search(r"^compatibility:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match:
        fail("frontmatter name is missing")
    if not desc_match:
        fail("frontmatter description is missing")

    name = name_match.group(1).strip().strip('"')
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(f"invalid Skill name: {name!r}")

    description = desc_match.group(1).strip().strip('"')
    if not description or len(description) > 1024:
        fail("description must be non-empty and <= 1024 characters")

    if compatibility_match:
        compatibility = compatibility_match.group(1).strip().strip('"')
        if len(compatibility) > 500:
            fail("compatibility must be <= 500 characters")

    body_lines = text[match.end():].splitlines()
    if len(body_lines) > 500:
        fail(f"SKILL.md body is {len(body_lines)} lines; keep the main file under 500 lines")

    root_name = ROOT.name
    if root_name != name:
        warn(f"install directory name '{root_name}' differs from Skill name '{name}'; package into a directory named '{name}' for strict spec conformance")

    if not REFS.is_dir():
        fail("references directory is missing")

    missing = sorted(ref for ref in REQUIRED_REFS if not (REFS / ref).is_file())
    if missing:
        fail("missing references: " + ", ".join(missing))

    referenced_names = set(re.findall(r"`references/([^`]+)`", text))
    unknown = sorted(referenced_names - REQUIRED_REFS)
    if unknown:
        fail("SKILL.md references files not tracked by validator: " + ", ".join(unknown))

    forbidden_external_dependency_phrases = (
        "go read the documentation",
        "visit the documentation",
        "read this URL",
        "follow this link to learn",
        "open this URL to learn",
    )
    lowered = text.lower()
    for phrase in forbidden_external_dependency_phrases:
        if phrase in lowered:
            fail(f"SKILL.md contains forbidden external-dependency instruction: {phrase!r}")

    if "never invent" not in lowered:
        fail("SKILL.md must contain the no-fabrication tool rule")
    if "file://" not in lowered or "server-backed" not in lowered:
        fail("SKILL.md must contain the server-backed template anti-pattern")
    if "browser operating kernel" not in lowered:
        fail("SKILL.md must contain the browser operating kernel")

    if not EVALS.is_file():
        fail("evals/evals.json is missing")
    try:
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid evals/evals.json: {exc}")

    if payload.get("skill_name") != name:
        fail("evals/evals.json skill_name does not match SKILL.md name")
    if not isinstance(payload.get("evals"), list) or not payload["evals"]:
        fail("evals/evals.json must contain a non-empty evals list")

    for index, item in enumerate(payload["evals"], start=1):
        for field in ("id", "prompt", "expected_output", "expectations"):
            if field not in item:
                fail(f"eval {index} is missing '{field}'")
        if not isinstance(item["expectations"], list) or not item["expectations"]:
            fail(f"eval {index} expectations must be a non-empty list")

    if not BENCHMARKS.is_file():
        fail("benchmarks/scenarios.yaml is missing")
    benchmark_text = BENCHMARKS.read_text(encoding="utf-8")
    for required in ("version:", "skill_name:", "evals:"):
        if required not in benchmark_text:
            fail(f"benchmark scenario file is missing top-level field: {required}")

    required_tests = {
        "custom-provider-transport.md",
        "project-recognition.md",
        "browser-operating-protocol.md",
        "capability-operating-kernel.md",
    }
    missing_tests = sorted(name for name in required_tests if not (ROOT / "tests" / name).is_file())
    if missing_tests:
        fail("missing regression tests: " + ", ".join(missing_tests))

    print("PASS: Skill structure, browser/project/provider references, external-dependency guard, evals, benchmarks, and regression tests passed")
    print(f"Skill: {name}")
    print(f"SKILL.md body lines: {len(body_lines)}")
    print(f"References: {len(REQUIRED_REFS)}")
    print(f"Evals: {len(payload['evals'])}")
    print(f"Regression tests: {len(required_tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
