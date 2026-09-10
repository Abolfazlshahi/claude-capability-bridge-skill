"""Shared installable-payload builder.

The standalone Skill and the Claude Code plugin are two packagings of ONE
payload. Keeping the file set and the version in a single place is what stops
the two outputs from drifting apart.
"""

from __future__ import annotations

import json
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path

from . import cards as cards_lib
from . import refs
from .frontmatter import SkillMetadata, load_skill_metadata

SKILL_FILE = "SKILL.md"
CONTENT_DIRS = ("profiles", "cards", "references")
EXTRA_FILES = ("LICENSE",)

# Runtime files that only the plugin needs. Source path -> package path.
HOOK_RUNTIME: dict[str, str] = {
    "bootstrap/bridge_hook.py": "scripts/bridge_hook.py",
    "bootstrap/session-start.sh": "scripts/session-start.sh",
    "bootstrap/user-prompt-submit.sh": "scripts/user-prompt-submit.sh",
    "bootstrap/post-tool-use-failure.sh": "scripts/post-tool-use-failure.sh",
    "bootstrap/session-start.ps1": "scripts/session-start.ps1",
    "bootstrap/user-prompt-submit.ps1": "scripts/user-prompt-submit.ps1",
    "bootstrap/post-tool-use-failure.ps1": "scripts/post-tool-use-failure.ps1",
}

EXECUTABLE_SUFFIXES = {".sh", ".ps1", ".py"}

PLUGIN_DESCRIPTION = (
    "Runtime-aware procedural bridge for Claude Code and compatible agent runtimes. "
    "Ships a small operating kernel, host profiles, capability cards, and adaptive "
    "session/prompt/failure hooks."
)
REPOSITORY = "https://github.com/Abolfazlshahi/claude-capability-bridge-skill"
AUTHOR = "Abolfazlshahi"
HOOK_TIMEOUT_SECONDS = 10


class BuildError(RuntimeError):
    pass


@dataclass(frozen=True)
class BuildResult:
    kind: str
    out: Path
    name: str
    version: str
    files: tuple[str, ...]

    @property
    def file_count(self) -> int:
        return len(self.files)


def safe_reset(out: Path, root: Path) -> None:
    """Delete a previous build output, but never anything else."""
    out = out.resolve()
    root = root.resolve()
    if out == root or out in root.parents:
        raise BuildError(f"refusing to delete {out}: it contains the source tree")
    if (out / ".git").exists() or (out / SKILL_FILE).exists() and (out / "bootstrap").exists():
        raise BuildError(f"refusing to delete {out}: looks like a source checkout")
    if out.exists():
        if not out.is_dir():
            raise BuildError(f"build output path is not a directory: {out}")
        shutil.rmtree(out)


def payload_entries(root: Path) -> list[tuple[str, str]]:
    """Deterministic (source-relative, package-relative) pairs for the Skill payload."""
    entries: list[tuple[str, str]] = []
    skill = root / SKILL_FILE
    if not skill.is_file():
        raise BuildError(f"{SKILL_FILE} is missing")
    entries.append((SKILL_FILE, SKILL_FILE))

    for directory in CONTENT_DIRS:
        source_dir = root / directory
        if not source_dir.is_dir():
            continue
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file() or path.name.startswith("."):
                continue
            if path.suffix not in {".md", ".json"}:
                continue
            rel = path.relative_to(root).as_posix()
            entries.append((rel, rel))

    for name in EXTRA_FILES:
        if (root / name).is_file():
            entries.append((name, name))

    return entries


def _copy(root: Path, out: Path, entries: list[tuple[str, str]]) -> list[str]:
    written: list[str] = []
    for source_rel, target_rel in entries:
        source = root / source_rel
        target = out / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        # copyfile (not copy2) keeps builds reproducible: no mtimes are carried over.
        shutil.copyfile(source, target)
        if target.suffix in EXECUTABLE_SUFFIXES:
            target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        written.append(target_rel)
    return written


def _validate_package(out: Path, kind: str) -> None:
    problems = refs.missing_references(out)
    if problems:
        listed = "\n  ".join(problems[:20])
        raise BuildError(
            f"{kind} package has {len(problems)} unresolved local reference(s):\n  {listed}"
        )


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def load_metadata(root: Path) -> SkillMetadata:
    meta = load_skill_metadata(root / SKILL_FILE)
    cards_dir = root / "cards"
    if cards_dir.is_dir():
        cards_lib.verify_index(cards_dir)
    return meta


def build_skill_package(root: Path, out: Path | None = None) -> BuildResult:
    meta = load_metadata(root)
    out = (out or root / "dist" / meta.name).resolve()
    safe_reset(out, root)
    out.mkdir(parents=True)
    written = _copy(root, out, payload_entries(root))
    _validate_package(out, "Skill")
    return BuildResult("skill", out, meta.name, meta.version, tuple(sorted(written)))


def plugin_manifest(meta: SkillMetadata) -> dict:
    return {
        "name": meta.name,
        "description": PLUGIN_DESCRIPTION,
        "version": meta.version,
        "author": {"name": AUTHOR},
        "repository": REPOSITORY,
        "license": meta.license or "MIT",
    }


def _hook_entry(script: str) -> dict:
    return {
        "hooks": [
            {
                "type": "command",
                "command": f'bash "${{CLAUDE_PLUGIN_ROOT}}/scripts/{script}"',
                "timeout": HOOK_TIMEOUT_SECONDS,
            }
        ]
    }


def plugin_hooks() -> dict:
    """Only events this repository has actually exercised are registered.

    Optional extra events live in bootstrap/settings.optional-events.json.example
    and stay opt-in because their availability is host-version dependent.
    """
    session = _hook_entry("session-start.sh")
    session["matcher"] = "startup|resume|clear|compact|fork"
    return {
        "description": (
            "Adaptive capability-bridge context: session bootstrap, targeted per-prompt "
            "rehydration or card routing, and failure-specific recovery guidance."
        ),
        "hooks": {
            "SessionStart": [session],
            "UserPromptSubmit": [_hook_entry("user-prompt-submit.sh")],
            "PostToolUseFailure": [_hook_entry("post-tool-use-failure.sh")],
        },
    }


def build_plugin_package(root: Path, out: Path | None = None) -> BuildResult:
    meta = load_metadata(root)
    out = (out or root / "dist" / f"{meta.name}-plugin").resolve()

    missing = [src for src in HOOK_RUNTIME if not (root / src).is_file()]
    if missing:
        raise BuildError("missing hook runtime files: " + ", ".join(sorted(missing)))

    safe_reset(out, root)
    out.mkdir(parents=True)

    entries = payload_entries(root) + sorted(HOOK_RUNTIME.items())
    written = _copy(root, out, entries)

    _write_json(out / ".claude-plugin" / "plugin.json", plugin_manifest(meta))
    _write_json(out / "hooks" / "hooks.json", plugin_hooks())
    written += [".claude-plugin/plugin.json", "hooks/hooks.json"]

    _validate_package(out, "plugin")
    return BuildResult("plugin", out, meta.name, meta.version, tuple(sorted(written)))
