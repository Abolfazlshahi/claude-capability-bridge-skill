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
import tempfile
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


IS_WINDOWS = os.name == "nt"
SHELL_WRAPPERS = (
    "session-start.sh",
    "user-prompt-submit.sh",
    "post-tool-use-failure.sh",
)

_SHELL_PROBE: list = []


def _dedupe(items) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _shell_candidates() -> list[str]:
    """Every bash worth trying, best first.

    On Windows the bash on PATH is frequently the WSL launcher in System32. It
    starts fine, so a naive "bash -c" probe answers yes, yet it cannot open the
    drive-letter path the tests hand it and exits 127. Git for Windows ships a
    bash that can, so it is preferred when present. Set BRIDGE_TEST_BASH to
    force a specific interpreter.
    """
    candidates = [os.environ.get("BRIDGE_TEST_BASH", "")]
    if IS_WINDOWS:
        roots = []
        git = shutil.which("git")
        if git:
            roots.append(Path(git).resolve().parent.parent)
        for variable in (
            "ProgramFiles",
            "ProgramW6432",
            "ProgramFiles(x86)",
            "LOCALAPPDATA",
        ):
            base = os.environ.get(variable)
            if base:
                roots.append(Path(base) / "Git")
                roots.append(Path(base) / "Programs" / "Git")
        for root in roots:
            for relative in ("bin/bash.exe", "usr/bin/bash.exe"):
                candidate = root / relative
                if candidate.exists():
                    candidates.append(str(candidate))
    candidates.append(shutil.which("bash") or "")
    return _dedupe(candidates)


def _can_execute_a_script(exe: str) -> bool:
    """Probe the way a host really invokes a wrapper: a script file by path."""
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe.sh"
        probe.write_bytes(b"#!/usr/bin/env bash\nprintf ok\n")
        try:
            proc = subprocess.run(
                [exe, str(probe)], capture_output=True, text=True, timeout=60
            )
        except OSError:
            return False
    return proc.returncode == 0 and proc.stdout.strip() == "ok"


def posix_shell() -> str | None:
    """A bash that can execute a script by path here, or None. Cached."""
    if _SHELL_PROBE:
        return _SHELL_PROBE[0]
    chosen = next(
        (exe for exe in _shell_candidates() if _can_execute_a_script(exe)), None
    )
    _SHELL_PROBE.append(chosen)
    return chosen


def has_crlf(path: Path) -> bool:
    return b"\r\n" in path.read_bytes()


def shell_scripts() -> list[Path]:
    """Every tracked-source .sh file, excluding build output and git internals."""
    return sorted(
        path
        for path in ROOT.rglob("*.sh")
        if DIST not in path.parents and ".git" not in path.parts
    )


def require_posix_shell(test, scripts=()) -> str:
    """Skip a test that must execute a .sh wrapper when that cannot work here."""
    exe = posix_shell()
    if exe is None:
        test.skipTest(
            "no bash on this host can execute a script by path (on Windows the "
            "System32 bash.exe is the WSL launcher and cannot open a drive-letter "
            "path); install Git for Windows or point BRIDGE_TEST_BASH at a bash"
        )
    broken = sorted(path.name for path in scripts if has_crlf(path))
    if broken:
        test.skipTest(
            "checkout has CRLF line endings in "
            + ", ".join(broken)
            + "; bash cannot run those. Fix with: git add --renormalize ."
        )
    return exe


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
    interpreter = (posix_shell() or "bash") if script.suffix == ".sh" else sys.executable
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
