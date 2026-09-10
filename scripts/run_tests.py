#!/usr/bin/env python3
"""Run the repository's executable test suite.

This runner intentionally uses only the Python standard library so it works in
CI and in offline sandboxes. Live-integration checks that need a real Claude
Code install or a real provider are reported as skipped, never as passing.
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests" / "python"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pattern",
        default="test_*.py",
        help="unittest discovery pattern (default: test_*.py)",
    )
    parser.add_argument("--verbosity", type=int, default=2)
    parser.add_argument(
        "--failfast", action="store_true", help="stop after the first failure"
    )
    args = parser.parse_args()

    if not TESTS.is_dir():
        print(f"missing test directory: {TESTS}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(TESTS))
    sys.path.insert(0, str(ROOT / "scripts"))

    # Report the host facts that decide which tests can run at all, so a
    # skip can be read as evidence instead of guessed at.
    try:
        import bridge_test_utils as util

        shell = util.posix_shell()
    except Exception:  # diagnostics must never decide a run
        shell = None
    print(f"python: {sys.version.split()[0]} on {sys.platform}")
    print(
        "posix shell for wrapper tests: "
        + (shell or "NONE (wrapper execution tests will skip, not pass)")
    )
    print()

    suite = unittest.TestLoader().discover(
        str(TESTS), pattern=args.pattern, top_level_dir=str(TESTS)
    )
    result = unittest.TextTestRunner(
        verbosity=args.verbosity, failfast=args.failfast
    ).run(suite)

    print()
    print(
        f"tests={result.testsRun} failures={len(result.failures)} "
        f"errors={len(result.errors)} skipped={len(result.skipped)}"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
