#!/usr/bin/env python3
"""Run the repository's executable test suite.

This runner intentionally uses only the Python standard library so it works in
CI and in offline sandboxes. Live-integration checks that need a real Claude
Code install or a real provider are reported as skipped, never as passing.
"""

from __future__ import annotations

import argparse
import io
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests" / "python"


def failure_reason(traceback_text: str) -> str:
    """The last meaningful line of a traceback: the assertion, not the frames."""
    lines = [
        line.strip()
        for line in traceback_text.strip().splitlines()
        if line.strip()
    ]
    return lines[-1][:300] if lines else "no traceback"


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
    parser.add_argument(
        "--summary",
        action="store_true",
        help=(
            "print only the host facts, the failing test ids with their "
            "assertion, the grouped skip reasons, and the counts"
        ),
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
    # --summary keeps the per-test log out of the way so a run can be
    # reported in a few lines instead of a few hundred.
    swallowed = io.StringIO()
    result = unittest.TextTestRunner(
        stream=swallowed if args.summary else sys.stderr,
        verbosity=0 if args.summary else args.verbosity,
        failfast=args.failfast,
    ).run(suite)

    if args.summary:
        print()
        for label, entries in (("FAIL", result.failures), ("ERROR", result.errors)):
            for case, traceback_text in entries:
                print(f"{label}: {case.id()}")
                print(f"      {failure_reason(traceback_text)}")
        reasons = Counter(reason for _case, reason in result.skipped)
        for reason, count in sorted(reasons.items()):
            print(f"SKIP x{count}: {reason}")

    print()
    print(
        f"tests={result.testsRun} failures={len(result.failures)} "
        f"errors={len(result.errors)} skipped={len(result.skipped)}"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
