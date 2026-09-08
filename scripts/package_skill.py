#!/usr/bin/env python3
"""Build a spec-shaped distributable Skill directory from this repository."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "claude-capability-bridge"
OUT = ROOT / "dist" / NAME

# Repository-only material stays outside the installable Skill. The package keeps
# the actual Skill contract (SKILL.md, references, scripts, assets if added).
INCLUDE = ["SKILL.md", "references", "scripts", "LICENSE"]
EXCLUDE_SCRIPT_NAMES = {Path(__file__).name, "package_skill.py"}


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for item in INCLUDE:
        src = ROOT / item
        dst = OUT / item
        if item == "scripts":
            dst.mkdir()
            for child in src.iterdir():
                if child.name in EXCLUDE_SCRIPT_NAMES:
                    continue
                if child.is_file():
                    shutil.copy2(child, dst / child.name)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    print(f"Packaged Skill: {OUT}")
    print(f"Install directory name: {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
