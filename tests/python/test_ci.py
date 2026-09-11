"""Continuous-integration invariants.

Bug D - the "PowerShell wrapper syntax" step wrapped an undeclared variable in
[ref]:

    pwsh -NoProfile -Command "... ParseFile(..., [ref]$null, [ref]$errors) ..."

PowerShell rejects that at runtime with "[ref] cannot be applied to a variable
that does not exist", so the step failed on every runner that ships pwsh. The
machine that wrote the step had no pwsh, and the step's own guard turned that
absence into a silent success, so nothing ever executed it. These tests close
both halves of the hole: the [ref] contract is checked statically on any host,
and the checker itself is executed wherever a PowerShell exists - including the
Ubuntu runner, which runs this suite before it reaches the parse step.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import bridge_test_utils as util

CHECKER = util.SCRIPTS / "check_powershell_syntax.ps1"
WORKFLOWS = util.ROOT / ".github" / "workflows"

# [ref]$name in PowerShell, and [ref]\$name in a shell-escaped workflow line.
REF_ARGUMENT = re.compile(r"\[ref\]\s*\\?\$(\w+)")


def powershell() -> str | None:
    """Return a PowerShell interpreter on this host, or None."""
    for candidate in ("pwsh", "powershell"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def sources() -> list[Path]:
    """Every file that may pass a [ref] argument: wrappers plus workflows."""
    found = [
        path
        for path in sorted(util.ROOT.rglob("*.ps1"))
        if util.DIST not in path.parents
    ]
    found.extend(sorted(WORKFLOWS.glob("*.yml")))
    found.extend(sorted(WORKFLOWS.glob("*.yaml")))
    return found


class RefArgumentTestCase(unittest.TestCase):
    def test_sources_to_scan_were_actually_found(self) -> None:
        """A scan over an empty file list would pass while proving nothing."""
        paths = sources()
        self.assertTrue(
            any(path.suffix == ".ps1" for path in paths),
            "no PowerShell files found to scan",
        )
        self.assertTrue(
            any(path.parent == WORKFLOWS for path in paths),
            "no CI workflow files found to scan",
        )

    def test_every_ref_argument_names_a_variable_declared_first(self) -> None:
        for path in sources():
            text = util.read_text(path)
            for match in REF_ARGUMENT.finditer(text):
                name = match.group(1)
                if name == "null":
                    continue
                before = text[: match.start()]
                assigned = re.search(
                    r"\\?\$" + re.escape(name) + r"\s*=", before
                )
                line = text[: match.start()].count("\n") + 1
                self.assertIsNotNone(
                    assigned,
                    f"{path.relative_to(util.ROOT)}:{line} wraps [ref] around "
                    f"${name}, which is never assigned earlier in the file; "
                    "PowerShell answers '[ref] cannot be applied to a variable "
                    "that does not exist'",
                )


class PowerShellCheckerTestCase(unittest.TestCase):
    def test_the_checker_is_present_and_declares_its_out_parameters(self) -> None:
        self.assertTrue(CHECKER.is_file(), f"missing {CHECKER}")
        text = util.read_text(CHECKER)
        parse_at = text.find("ParseFile(")
        self.assertGreater(parse_at, -1, "the checker must call ParseFile")
        before = text[:parse_at]
        self.assertIn("$tokens = $null", before)
        self.assertIn("$errors = $null", before)

    def test_the_checker_states_that_parsing_is_not_execution(self) -> None:
        self.assertIn("parsing is not execution", util.read_text(CHECKER))

    def test_the_workflow_delegates_parsing_to_the_checked_in_script(self) -> None:
        text = util.read_text(WORKFLOWS / "validate.yml")
        self.assertIn("scripts/check_powershell_syntax.ps1", text)
        self.assertNotIn(
            "Parser]::ParseFile",
            text,
            "the workflow must not inline a parser one-liner; call the script "
            "so the tests can exercise the same code path",
        )

    def run_checker(self, *arguments: str) -> subprocess.CompletedProcess:
        interpreter = powershell()
        if interpreter is None:
            self.skipTest(
                "no PowerShell on this host; the parse check is exercised where "
                "pwsh exists, and stays UNVERIFIED here"
            )
        return subprocess.run(
            [interpreter, "-NoProfile", "-File", str(CHECKER), *arguments],
            cwd=str(util.ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )

    def test_the_checker_accepts_the_real_wrappers(self) -> None:
        done = self.run_checker("bootstrap")
        output = done.stdout + done.stderr
        self.assertEqual(done.returncode, 0, output)
        self.assertEqual(
            output.count("parse ok:"),
            len(sorted(util.BOOTSTRAP.glob("*.ps1"))),
            output,
        )

    def test_the_checker_rejects_a_file_it_cannot_parse(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            broken = Path(raw) / "broken.ps1"
            broken.write_text("if ($x -eq 1 {\n  Write-Host 'unclosed'\n", encoding="utf-8")
            done = self.run_checker(str(broken))
        output = done.stdout + done.stderr
        self.assertEqual(done.returncode, 1, output)
        self.assertIn("parse error:", output)

    def test_the_checker_reports_bad_usage_instead_of_passing(self) -> None:
        done = self.run_checker("no-such-directory-4c1f")
        output = done.stdout + done.stderr
        self.assertEqual(done.returncode, 2, output)
        self.assertIn("usage error:", output)


if __name__ == "__main__":
    unittest.main()
