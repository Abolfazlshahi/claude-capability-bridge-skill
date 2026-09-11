#!/usr/bin/env python3
"""Build a Claude Code plugin that bundles the Skill payload and host hooks.

The Skill payload is identical to the standalone package (same files, same
version); the plugin only adds the host-owned hook runtime and manifests.

SKILL.md at the plugin root is intentional: current Claude Code supports a
single-skill plugin with no `skills/` directory and no `skills` manifest field.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bridgelib.frontmatter import FrontmatterError  # noqa: E402
from bridgelib.payload import BuildError, build_plugin_package  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="output directory (default: dist/<skill-name>-plugin)",
    )
    args = parser.parse_args()

    try:
        result = build_plugin_package(ROOT, args.out)
    except (BuildError, FrontmatterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"Built Claude Code plugin: {result.out}")
    print(f"Plugin: {result.name}@{result.version}")
    print(f"Files: {result.file_count}")
    print("Hooks: SessionStart + UserPromptSubmit + PostToolUseFailure")
    print("Local reference closure: verified inside the built package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
