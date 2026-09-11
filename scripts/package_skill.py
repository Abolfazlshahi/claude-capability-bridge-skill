#!/usr/bin/env python3
"""Build the standalone, installable Skill directory.

The payload itself is defined once in scripts/bridgelib/payload.py and shared
with the Claude Code plugin build, so the two outputs cannot drift.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bridgelib.frontmatter import FrontmatterError  # noqa: E402
from bridgelib.payload import BuildError, build_skill_package  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="output directory (default: dist/<skill-name>)",
    )
    args = parser.parse_args()

    try:
        result = build_skill_package(ROOT, args.out)
    except (BuildError, FrontmatterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"Packaged Skill: {result.out}")
    print(f"Skill: {result.name}@{result.version}")
    print(f"Files: {result.file_count}")
    print("Local reference closure: verified inside the built package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
