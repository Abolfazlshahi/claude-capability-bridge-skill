#!/usr/bin/env python3
"""Build a Claude Code plugin that bundles the bridge Skill and host bootstrap hooks."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SESSION_BOOTSTRAP = ROOT / "bootstrap" / "session-start.sh"
TURN_BOOTSTRAP = ROOT / "bootstrap" / "user-prompt-submit.sh"
OUT = ROOT / "dist" / "claude-capability-bridge-plugin"


def skill_metadata() -> tuple[str, str, str]:
    text = SKILL.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md frontmatter is missing")
    frontmatter = match.group(1)

    def field(name: str, default: str = "") -> str:
        found = re.search(rf"^{re.escape(name)}:\s*(.+)$", frontmatter, re.MULTILINE)
        return found.group(1).strip().strip('"') if found else default

    return field("name", "claude-capability-bridge"), field("description"), field("version", "0.0.0")


def main() -> int:
    for required in (SKILL, SESSION_BOOTSTRAP, TURN_BOOTSTRAP):
        if not required.is_file():
            raise SystemExit(f"required file is missing: {required.relative_to(ROOT)}")

    name, description, version = skill_metadata()
    if not description:
        raise SystemExit("SKILL.md description is required")

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / ".claude-plugin").mkdir(parents=True)
    (OUT / "hooks").mkdir(parents=True)
    (OUT / "scripts").mkdir(parents=True)

    plugin_manifest = {
        "name": name,
        "description": "Runtime-aware procedural bridge for Claude Code and compatible agent runtimes, with session-start and per-turn capability reminders.",
        "version": version,
        "author": {"name": "Abolfazlshahi"},
        "repository": "https://github.com/Abolfazlshahi/claude-capability-bridge-skill",
        "license": "MIT",
    }
    (OUT / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin_manifest, indent=2) + "\n", encoding="utf-8")

    (OUT / "SKILL.md").write_text(SKILL.read_text(encoding="utf-8"), encoding="utf-8")
    shutil.copy2(SESSION_BOOTSTRAP, OUT / "scripts" / "session-start.sh")
    shutil.copy2(TURN_BOOTSTRAP, OUT / "scripts" / "user-prompt-submit.sh")

    hooks = {
        "description": "Keep the capability-bridge operating protocol present at session start and before each submitted prompt.",
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume|clear|compact|fork",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/scripts/session-start.sh\"",
                            "timeout": 5,
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/scripts/user-prompt-submit.sh\"",
                            "timeout": 5,
                        }
                    ]
                }
            ]
        },
    }
    (OUT / "hooks" / "hooks.json").write_text(json.dumps(hooks, indent=2) + "\n", encoding="utf-8")

    print(f"Built Claude Code plugin: {OUT}")
    print(f"Plugin: {name}@{version}")
    print("Bootstrap: SessionStart + UserPromptSubmit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
