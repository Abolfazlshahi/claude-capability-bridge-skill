"""Shared helpers for the executable test suite.

These helpers deliberately inspect *built artifacts* instead of build internals,
so the same assertions are meaningful before and after the packaging rewrite.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
BOOTSTRAP = ROOT / "bootstrap"
ENGINE = BOOTSTRAP / "bridge_hook.py"
DIST = ROOT / "dist"
SKILL_PACKAGE = DIST / "claude-capability-bridge"
PLUGIN_PACKAGE = DIST / "claude-capability-bridge-plugin"

# Only these prefixes are treated as "content routing" material that must travel
# inside every installable package. Everything else that is referenced is only
# checked for existence in the source tree.
PACKAGED_REFERENCE_PREFIXES = ("references/", "cards/", "profiles/")

_MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
_INLINE_CODE = re.compile(
    r"`([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|json|ya?ml|sh|ps1|py))`"
)
_BARE_CONTENT_PATH = re.compile(
    r"(?<![\w./$-])((?:references|cards|profiles)/[A-Za-z0-9_./-]+\.(?:md|json))"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def local_references(text: str) -> set[str]:
    """Extract relative local file references from Markdown-ish text."""
    found: set[str] = set()
    for match in _MD_LINK.finditer(text):
        target = match.group(1).strip()
        if not target or "://" in target or target.startswith(("#", "mailto:", "/")):
            continue
        if "${" in target or "$(" in target:
            continue
        found.add(target.split("#", 1)[0])
    for match in _INLINE_CODE.finditer(text):
        found.add(match.group(1))
    for match in _BARE_CONTENT_PATH.finditer(text):
        found.add(match.group(1))
    return {ref for ref in found if ref and not ref.startswith(("http", "/"))}


def packaged_references(text: str) -> set[str]:
    return {
        ref
        for ref in local_references(text)
        if ref.startswith(PACKAGED_REFERENCE_PREFIXES)
    }


def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def run_script(
    name: str,
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
    scripts_dir: Path | None = None,
) -> subprocess.CompletedProcess:
    script = (scripts_dir or SCRIPTS) / name
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd or ROOT),
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"{name} exited {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def run_hook(
    script: Path,
    payload: str,
    env_overrides: dict[str, str] | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess:
    """Run a bootstrap hook exactly like a host would: JSON on stdin."""
    env = dict(os.environ)
    env.pop("CLAUDE_CAPABILITY_BRIDGE_MODE", None)
    env.pop("CLAUDE_CAPABILITY_BRIDGE_STATE_DIR", None)
    env.update(env_overrides or {})
    interpreter = "bash" if script.suffix == ".sh" else sys.executable
    return subprocess.run(
        [interpreter, str(script)],
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )


def run_engine(
    event: str | None,
    payload: str,
    env_overrides: dict[str, str] | None = None,
    timeout: int = 30,
    engine: Path | None = None,
) -> subprocess.CompletedProcess:
    """Run the hook engine directly, the same way the wrappers do.

    The wrappers call `python bridge_hook.py --event <Event>` and pipe the raw
    host payload on stdin, so tests use the identical contract.
    """
    env = dict(os.environ)
    env.pop("CLAUDE_CAPABILITY_BRIDGE_MODE", None)
    env.pop("CLAUDE_CAPABILITY_BRIDGE_STATE_DIR", None)
    env.pop("CLAUDE_CAPABILITY_BRIDGE_TELEMETRY", None)
    env.update(env_overrides or {})
    command = [sys.executable, str(engine or ENGINE)]
    if event is not None:
        command += ["--event", event]
    return subprocess.run(
        command,
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )


def hook_context(proc: subprocess.CompletedProcess) -> str | None:
    """Return the additionalContext a host would receive, or None if silent.

    Raises if the hook printed something that is not a valid hook envelope,
    because a host would treat that as a broken hook.
    """
    out = proc.stdout.strip()
    if not out:
        return None
    data = json.loads(out)
    specific = data["hookSpecificOutput"]
    assert "hookEventName" in specific, "hook output must name its event"
    return specific.get("additionalContext")


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            snapshot[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def copy_source_tree(destination: Path) -> Path:
    """Copy the repository (without build output or VCS data) for isolated runs."""
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(
            ".git", "dist", "__pycache__", "*.pyc", ".pytest_cache", "assets"
        ),
    )
    return destination


def build_packages() -> None:
    run_script("package_skill.py")
    run_script("package_claude_code_plugin.py")
