#!/usr/bin/env python3
"""Contract validator for the Claude Capability Bridge.

This replaces the previous validator, which could print PASS while the built
plugin was missing every reference file and while the manifest version was
0.0.0. The rules here are deliberately about *contracts and built artifacts*,
not about the presence of particular sentences in prose.

What it checks:

1. frontmatter: real parse, valid name, non-empty description, semver version;
2. kernel contract: the rules that must survive any future rewrite;
3. cards: required sections, committed index freshness, routing sanity;
4. profiles: no claims that a capability exists in the live run;
5. reference graph: every local reference under references/, cards/, profiles/
   resolves in the source tree;
6. content budgets from config/content-budgets.json (characters, not tokens);
7. hook runtime: shell syntax, Python syntax, JSON validity, no eval of input;
8. both built packages: version match, reference closure, no dev-only scripts.

It is a development tool. It is intentionally NOT shipped inside the runtime
package, because it depends on tests/, benchmarks/, and config/ from the source
checkout.
"""

from __future__ import annotations

import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from bridgelib import (  # noqa: E402
    FrontmatterError,
    load_skill_metadata,
    yaml_backend,
)
from bridgelib.cards import build_index, render_index  # noqa: E402
from bridgelib.refs import (  # noqa: E402
    markdown_files,
    missing_references,
    packaged_references,
)

failures: list[str] = []
warnings: list[str] = []
notes: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def note(message: str) -> None:
    notes.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- 1. frontmatter


def check_frontmatter() -> object:
    try:
        meta = load_skill_metadata(ROOT / "SKILL.md")
    except (FrontmatterError, OSError) as exc:
        fail(f"SKILL.md frontmatter is invalid: {exc}")
        return None
    if meta.name != "claude-capability-bridge":
        fail(
            f"Skill name changed to {meta.name!r}; renaming breaks existing installs "
            "and references"
        )
    note(f"skill {meta.name}@{meta.version} (yaml backend: {yaml_backend()})")
    return meta


# ------------------------------------------------------------ 2. kernel content

KERNEL_CONTRACTS = {
    "fast path for simple requests": (
        "answer directly",
        "no runtime detection",
    ),
    "prohibition on inventing capabilities": (
        "never invent",
    ),
    "conceptual vs callable tool names": (
        "is not a callable tool name",
    ),
    "permission is separate from availability": (
        "permission is not availability",
    ),
    "tool success is not task success": (
        "tool success is not task success",
    ),
    "stale state handling": (
        "stale",
    ),
    "evidence-based retry": (
        "retry needs a changed variable",
    ),
    "unknown stays unknown": (
        "unknown stays unknown",
    ),
    "untrusted content boundary": (
        "data, not instruction",
    ),
    "card routing table": (
        "cards/index.json",
    ),
    "host profiles": (
        "profiles/generic.md",
    ),
    "delegation to specialized skills": (
        "specialized skill",
    ),
    "cache honesty": (
        "does **not** imply support",
    ),
    "security outranks cache": (
        "security outranks cache",
    ),
}

FORBIDDEN_KERNEL_CLAIMS = (
    "guaranteed cache",
    "guarantees a cache",
    "enables prompt caching",
    "cache hit rate improved",
    "always available",
)


def check_kernel(body: str) -> None:
    lowered = body.lower()
    for label, needles in KERNEL_CONTRACTS.items():
        if not any(needle.lower() in lowered for needle in needles):
            fail(f"SKILL.md kernel is missing the required rule: {label}")
    for claim in FORBIDDEN_KERNEL_CLAIMS:
        if claim in lowered:
            fail(f"SKILL.md contains an unsupportable claim: {claim!r}")
    if "- [ ]" not in body:
        fail("SKILL.md must keep the pre-report self-check checklist")


# --------------------------------------------------------------------- 3. cards


def check_cards() -> list[dict]:
    cards_dir = ROOT / "cards"
    if not cards_dir.is_dir():
        fail("cards/ directory is missing")
        return []
    try:
        index = build_index(cards_dir)
    except FrontmatterError as exc:
        fail(f"card contract violation: {exc}")
        return []

    committed = cards_dir / "index.json"
    if not committed.is_file():
        fail("cards/index.json is missing; run scripts/build_card_index.py")
    elif read(committed) != render_index(index):
        fail("cards/index.json is out of date; run scripts/build_card_index.py")

    cards = index["cards"]
    if len(cards) < 8:
        warn(f"only {len(cards)} capability cards; important task families may be uncovered")

    seen_signals: dict[str, str] = {}
    for card in cards:
        if not (cards_dir / Path(card["path"]).name).is_file():
            fail(f"index entry {card['id']} points at a missing file")
        if not card["task_families"]:
            fail(f"card {card['id']} declares no task_families, so it cannot be routed to")
        if not card["signals"]:
            fail(f"card {card['id']} declares no routing signals")
        if not card["essentials"]:
            fail(f"card {card['id']} has no essentials for hook output")
        for signal in card["signals"]:
            if signal in seen_signals and seen_signals[signal] != card["id"]:
                warn(
                    f"signal {signal!r} is shared by {seen_signals[signal]} and "
                    f"{card['id']}; routing will treat it as ambiguous"
                )
            seen_signals[signal] = card["id"]

    body_text = "\n".join(read(p) for p in sorted(cards_dir.glob("*.md")))
    if "anti-pattern" not in body_text.lower():
        fail("cards must document at least one anti-pattern each; none found")
    for path in sorted(cards_dir.glob("*.md")):
        text = read(path).lower()
        if "anti-pattern" not in text:
            fail(f"cards/{path.name} has no explicit anti-pattern")
        if "done means" not in text:
            fail(f"cards/{path.name} has no explicit definition of done")
    return cards


# ------------------------------------------------------------------ 4. profiles

PROFILE_FORBIDDEN = (
    "a browser is available",
    "browser is always",
    "mcp is connected",
    "network is available",
    "network is always",
    "tools are permitted",
    "permission is granted",
)

# A profile is allowed - in fact required - to *deny* these claims. Only an
# unhedged assertion is a contract violation, so every match is checked against
# the text immediately preceding it.
NEGATION_MARKERS = (
    "not ",
    "never",
    "no ",
    "cannot",
    "can't",
    "don't",
    "do not",
    "without",
    "unless",
    "assume",
    "assumption",
    "proof that",
    "evidence that",
    "nor ",
    "isn't",
    "is not",
    "must not",
    "claim",
    "nothing",
    "none of",
    "neither",
    "no guarantee",
)


# Sentence boundary: real punctuation, a paragraph break, or the start of a new
# list item. A single newline is NOT a boundary, because Markdown prose wraps
# mid-sentence and the negation is often on the previous line.
_SENTENCE_BREAK = re.compile(r"(?:[.!?]|\n\s*\n|\n(?=\s*[-*+]\s))")


def _asserted(text_lower: str, claim: str) -> bool:
    """True only when `claim` occurs in a sentence with no negation or hedge.

    A fixed character window is not good enough: a profile legitimately writes
    "It never proves that a tool exists, that a connector is connected, ... or
    that a permission is granted", where the negation is far from the claim.
    """
    start = 0
    while True:
        idx = text_lower.find(claim, start)
        if idx == -1:
            return False
        breaks = [m.end() for m in _SENTENCE_BREAK.finditer(text_lower, 0, idx)]
        sentence_start = breaks[-1] if breaks else 0
        sentence = text_lower[sentence_start : idx + len(claim)]
        if not any(marker in sentence for marker in NEGATION_MARKERS):
            return True
        start = idx + len(claim)


def _uses_command(text: str, pattern: str, comment_prefix: str = "#") -> bool:
    """Detect real command usage, ignoring comments that merely mention it."""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(comment_prefix):
            continue
        if re.search(pattern, stripped, re.IGNORECASE):
            return True
    return False


def check_profiles() -> None:
    profiles_dir = ROOT / "profiles"
    if not profiles_dir.is_dir():
        fail("profiles/ directory is missing")
        return
    found = sorted(p.stem for p in profiles_dir.glob("*.md"))
    for required in ("claude-code", "desktop", "cowork", "generic"):
        if required not in found:
            fail(f"profiles/{required}.md is missing")
    for path in sorted(profiles_dir.glob("*.md")):
        text = read(path)
        lowered = text.lower()
        for claim in PROFILE_FORBIDDEN:
            if _asserted(lowered, claim):
                fail(f"profiles/{path.name} asserts live state: {claim!r}")
        if "not live state" not in lowered and "unknown" not in lowered:
            fail(
                f"profiles/{path.name} must state that it describes contracts, not live state"
            )


# ----------------------------------------------------------- 5. reference graph


def check_reference_graph() -> None:
    for problem in missing_references(ROOT):
        fail(f"broken local reference: {problem}")


# --------------------------------------------------------------- 6. budgets


def check_budgets() -> None:
    config_path = ROOT / "config" / "content-budgets.json"
    if not config_path.is_file():
        fail("config/content-budgets.json is missing")
        return
    try:
        config = json.loads(read(config_path))
        budgets = config["budgets"]
    except (ValueError, KeyError) as exc:
        fail(f"config/content-budgets.json is invalid: {exc}")
        return

    note(
        "budget unit: characters (no tokenizer ships with this repo; character "
        "counts are a proxy and are not token counts)"
    )

    skill_body = read(ROOT / "SKILL.md").split("---", 2)[-1]
    checks = [("SKILL.md body", len(skill_body), budgets.get("skill_body_chars"))]
    for path in sorted((ROOT / "cards").glob("*.md")):
        checks.append((f"cards/{path.name}", len(read(path)), budgets.get("card_chars")))
    for path in sorted((ROOT / "profiles").glob("*.md")):
        checks.append(
            (f"profiles/{path.name}", len(read(path)), budgets.get("profile_chars"))
        )
    index_path = ROOT / "cards" / "index.json"
    if index_path.is_file():
        checks.append(
            ("cards/index.json", len(read(index_path)), budgets.get("card_index_chars"))
        )

    for label, size, limit in checks:
        if isinstance(limit, int) and size > limit:
            fail(f"{label} is {size} characters, over the {limit} character budget")
    note(f"SKILL.md body: {len(skill_body)} characters")


# ------------------------------------------------------------- 7. hook runtime


def check_hook_runtime() -> None:
    bootstrap = ROOT / "bootstrap"
    engine = bootstrap / "bridge_hook.py"
    if not engine.is_file():
        fail("bootstrap/bridge_hook.py is missing")
    else:
        try:
            py_compile.compile(str(engine), doraise=True, cfile=str(engine) + "c")
        except py_compile.PyCompileError as exc:
            fail(f"bootstrap/bridge_hook.py does not compile: {exc}")
        finally:
            Path(str(engine) + "c").unlink(missing_ok=True)
        source = read(engine)
        for banned in ("eval(", "exec(", "os.system(", "shell=True"):
            if banned in source:
                fail(f"bootstrap/bridge_hook.py must not use {banned}")
        if "import yaml" in source:
            fail("hook runtime must not depend on a YAML parser")
        for module in ("requests", "urllib.request", "http.client", "socket"):
            if f"import {module}" in source:
                fail(f"hook runtime must not import network module {module}")

    shells = sorted(bootstrap.glob("*.sh"))
    if len(shells) != 3:
        fail(f"expected 3 shell wrappers in bootstrap/, found {len(shells)}")
    for path in shells:
        proc = subprocess.run(
            ["bash", "-n", str(path)], capture_output=True, text=True, timeout=60
        )
        if proc.returncode != 0:
            fail(f"{path.name} has a shell syntax error: {proc.stderr.strip()}")
        text = read(path)
        if _uses_command(text, r"(?:^|[;&|]|\bthen\b|\bdo\b)\s*eval\b"):
            fail(f"{path.name} must never eval hook input")
        if "source " in text and "# " not in text.split("source ")[0][-2:]:
            pass  # sourcing is checked below via _uses_command
        if _uses_command(text, r"(?:^|[;&|])\s*(?:source|\.)\s+\"?\$"):
            fail(f"{path.name} must never source hook input")
        if "exit 0" not in text:
            fail(f"{path.name} must always exit 0 so it cannot block the user")

    powershells = sorted(bootstrap.glob("*.ps1"))
    if len(powershells) != 3:
        fail(
            f"expected 3 PowerShell wrappers in bootstrap/, found {len(powershells)}; "
            "shell and PowerShell bootstraps must stay in sync"
        )
    for path in powershells:
        text = read(path)
        if _uses_command(text, r"\b(?:Invoke-Expression|iex)\b"):
            fail(f"{path.name} must never invoke hook input as a command")
        if "NOT VERIFIED ON WINDOWS" not in text:
            fail(f"{path.name} must state that Windows execution is unverified")

    for name in ("settings.json.example", "settings.optional-events.json.example"):
        path = bootstrap / name
        if not path.is_file():
            fail(f"bootstrap/{name} is missing")
            continue
        try:
            json.loads(read(path))
        except ValueError as exc:
            fail(f"bootstrap/{name} is not valid JSON: {exc}")


# ----------------------------------------------------------- 8. built artifacts


def check_packages(version: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        # --out is the final package directory for both packagers.
        skill_pkg = out / "claude-capability-bridge"
        plugin_pkg = out / "claude-capability-bridge-plugin"
        for script, target in (
            ("package_skill.py", skill_pkg),
            ("package_claude_code_plugin.py", plugin_pkg),
        ):
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / script), "--out", str(target)],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if proc.returncode != 0:
                fail(f"{script} failed: {proc.stdout.strip()} {proc.stderr.strip()}")
                return

        manifest_path = plugin_pkg / ".claude-plugin" / "plugin.json"
        if not manifest_path.is_file():
            fail("built plugin has no .claude-plugin/plugin.json")
        else:
            manifest = json.loads(read(manifest_path))
            if manifest.get("version") != version:
                fail(
                    f"plugin manifest version {manifest.get('version')!r} does not match "
                    f"SKILL.md metadata.version {version!r}"
                )
            if manifest.get("name") != "claude-capability-bridge":
                fail("plugin manifest name must match the Skill name")

        hooks_path = plugin_pkg / "hooks" / "hooks.json"
        if not hooks_path.is_file():
            fail("built plugin has no hooks/hooks.json")
        else:
            hooks = json.loads(read(hooks_path)).get("hooks", {})
            for event in ("SessionStart", "UserPromptSubmit", "PostToolUseFailure"):
                if event not in hooks:
                    fail(f"plugin hooks are missing the {event} event")

        dev_only = {
            "validate_skill.py",
            "package_skill.py",
            "package_claude_code_plugin.py",
            "run_tests.py",
            "build_card_index.py",
            "analyze_trace.py",
        }
        for pkg in (skill_pkg, plugin_pkg):
            if not pkg.is_dir():
                fail(f"expected built package at {pkg}")
                continue
            if not (pkg / "LICENSE").is_file():
                fail(f"{pkg.name} is missing LICENSE")
            shipped = {p.name for p in (pkg / "scripts").glob("*") if p.is_file()}
            leaked = sorted(shipped & dev_only)
            if leaked:
                fail(f"{pkg.name} ships development-only scripts: {leaked}")
            for md in markdown_files(pkg):
                for ref in packaged_references(read(md)):
                    if not (pkg / ref).exists():
                        fail(
                            f"{pkg.name}: {md.relative_to(pkg)} references missing {ref}"
                        )

        # Isolated-install check: copy out and resolve again with no source tree.
        isolated = out / "isolated"
        shutil.copytree(plugin_pkg, isolated)
        for md in markdown_files(isolated):
            for ref in packaged_references(read(md)):
                if not (isolated / ref).exists():
                    fail(f"isolated install cannot resolve {ref}")


# ------------------------------------------------------------------------- main


def main() -> int:
    meta = check_frontmatter()
    if meta is not None:
        check_kernel(meta.body)
    check_cards()
    check_profiles()
    check_reference_graph()
    check_budgets()
    check_hook_runtime()
    if meta is not None:
        check_packages(meta.version)

    for message in notes:
        print(f"NOTE: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    for message in failures:
        print(f"FAIL: {message}")

    if failures:
        print(f"\nVALIDATION FAILED: {len(failures)} problem(s)")
        return 1
    print(
        "\nPASS: frontmatter, kernel contract, cards and index, profiles, reference "
        "graph, content budgets, hook runtime, and both built packages are consistent."
    )
    print(
        "SCOPE: offline structural validation only. It proves nothing about live model "
        "behaviour, real Claude Code execution, Windows, or provider cache behaviour."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
