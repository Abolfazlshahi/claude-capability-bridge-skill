#!/usr/bin/env python3
"""Offline structural validator for the Claude Capability Bridge Skill."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
BOOTSTRAP = ROOT / "bootstrap"
EVALS = ROOT / "evals" / "evals.json"
BENCHMARKS = ROOT / "benchmarks" / "scenarios.yaml"
BEHAVIORAL = ROOT / "benchmarks" / "behavioral-benchmark.md"

REQUIRED_REFS = {
    "activation-and-memory.md", "async-subagents-and-remote.md", "browser-workflows.md",
    "capability-catalog.md", "capability-handshake.md", "capability-model.md",
    "capability-probing.md", "claude-desktop-current-map.md", "code-and-shell.md",
    "computer-use.md", "desktop-extensions.md", "desktop-workflows.md",
    "evaluation-and-attribution.md", "failure-recovery.md", "interactive-surfaces.md",
    "mcp-and-connectors.md", "mcp-deep-dive.md", "projects-and-files.md",
    "provider-adaptation.md", "custom-provider-transport.md", "project-recognition-and-launch.md",
    "runtime-boundaries.md", "runtime-boundary-matrix.md", "security-and-permissions.md",
    "session-memory.md", "skills-and-plugins.md", "source-notes.md", "task-recipes.md",
    "tool-routing-matrix.md", "tool-schema-literacy.md", "tool-use-patterns.md",
    "verification.md", "webapp-verification.md", "workspace-map.md", "artifact-lifecycle.md",
    "claude-code-native-mechanisms.md", "claude-code-cli-operating-model.md",
    "claude-code-bootstrap-kit.md", "office-and-collaboration-surfaces.md",
    "runtime-detection-and-profiles.md", "capability-remediation.md", "always-on-bootstrap.md",
    "README.md",
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

    for phrase in (
        "go read the documentation", "visit the documentation", "read this URL",
        "follow this link to learn", "open this URL to learn",
    ):
        if phrase in text.lower():
            fail(f"SKILL.md contains forbidden external-dependency instruction: {phrase!r}")

    for required_phrase, label in (
        ("never invent", "no-fabrication tool rule"),
        ("file://", "server-backed template anti-pattern"),
        ("browser operating kernel", "browser operating kernel"),
        ("smallest safe probe", "capability probing rule"),
        ("authoritative", "authoritative routing/verification rule"),
        ("runtime detection", "runtime detection rule"),
        ("remediation", "capability remediation rule"),
    ):
        if required_phrase not in text.lower():
            fail(f"SKILL.md must contain the {label}")

    if not BOOTSTRAP.is_dir():
        fail("bootstrap directory is missing")
    bootstrap_files = ("session-start.sh", "session-start.ps1", "settings.json.example")
    missing_bootstrap = sorted(item for item in bootstrap_files if not (BOOTSTRAP / item).is_file())
    if missing_bootstrap:
        fail("missing bootstrap files: " + ", ".join(missing_bootstrap))
    try:
        subprocess.run(["bash", "-n", str(BOOTSTRAP / "session-start.sh")], check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        fail(f"bootstrap/session-start.sh failed syntax validation: {exc}")
    try:
        json.loads((BOOTSTRAP / "settings.json.example").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid bootstrap/settings.json.example: {exc}")

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

    if not BEHAVIORAL.is_file():
        fail("benchmarks/behavioral-benchmark.md is missing")
    behavioral_text = BEHAVIORAL.read_text(encoding="utf-8").lower()
    for required in ("control", "treatment", "trajectory", "grading"):
        if required not in behavioral_text:
            fail(f"behavioral benchmark is missing: {required}")

    required_tests = {
        "custom-provider-transport.md", "project-recognition.md",
        "browser-operating-protocol.md", "capability-operating-kernel.md",
        "claude-code-native-mechanisms.md", "claude-code-cli-operating-model.md",
        "claude-code-bootstrap-kit.md", "office-and-collaboration-surfaces.md",
        "runtime-detection-and-remediation.md",
    }
    missing_tests = sorted(test for test in required_tests if not (ROOT / "tests" / test).is_file())
    if missing_tests:
        fail("missing regression tests: " + ", ".join(missing_tests))

    print("PASS: Skill structure, runtime detection, CLI operating model, bootstrap, capability remediation, probing, routing, browser/project/provider/native/collaboration references, external-dependency guard, bootstrap examples, evals, behavioral benchmark, and regression tests passed")
    print(f"Skill: {name}")
    print(f"SKILL.md body lines: {len(body_lines)}")
    print(f"References: {len(REQUIRED_REFS)}")
    print(f"Evals: {len(payload['evals'])}")
    print("Behavioral benchmark: present")
    print(f"Regression tests: {len(required_tests)}")
    print("Bootstrap examples: shell syntax + JSON validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
