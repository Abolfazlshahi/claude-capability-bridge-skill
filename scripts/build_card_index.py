#!/usr/bin/env python3
"""Generate cards/index.json from capability-card frontmatter.

The committed index is what the hook runtime reads, so routing needs no YAML
parser and no model call. Run this after editing any card; CI verifies the
committed file matches the cards byte for byte.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bridgelib.cards import INDEX_NAME, build_index, render_index  # noqa: E402
from bridgelib.frontmatter import FrontmatterError  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed index is current instead of rewriting it",
    )
    args = parser.parse_args()

    if not CARDS.is_dir():
        print("FAIL: cards/ directory is missing", file=sys.stderr)
        return 1

    try:
        rendered = render_index(build_index(CARDS))
    except FrontmatterError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    index_path = CARDS / INDEX_NAME
    current = index_path.read_text(encoding="utf-8") if index_path.is_file() else None

    if args.check:
        if current != rendered:
            print(
                "FAIL: cards/index.json is out of date; run scripts/build_card_index.py",
                file=sys.stderr,
            )
            return 1
        print("cards/index.json is up to date")
        return 0

    if current == rendered:
        print("cards/index.json already up to date")
        return 0

    index_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
