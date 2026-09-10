"""Packaging regression tests.

Every assertion here targets a bug that was reproduced on the baseline build:

* Bug A - the plugin package shipped without `references/`, so local links in the
  installed Skill were dangling.
* Bug B - `metadata.version` lives nested in the frontmatter, and the regex-based
  reader silently produced `0.0.0`.
* Bug C - the validator returned PASS while A and B were true.
* Packaging hygiene - dev-only scripts were shipped into the runtime package,
  builds were not verified as reproducible, and LICENSE was missing from the
  plugin.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

import bridge_test_utils as util


class PackagingTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        util.build_packages()
        cls.skill_pkg = util.SKILL_PACKAGE
        cls.plugin_pkg = util.PLUGIN_PACKAGE

    # ---------------------------------------------------------------- helpers
    def source_version(self) -> str:
        text = util.read_text(util.ROOT / "SKILL.md")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must start with YAML frontmatter")
        block = match.group(1)
        found = re.search(r"^\s+version:\s*[\"']?([^\"'\s]+)", block, re.MULTILINE)
        self.assertIsNotNone(found, "metadata.version must exist in SKILL.md")
        return found.group(1)

    def plugin_manifest(self) -> dict:
        manifest = self.plugin_pkg / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest.is_file(), "plugin manifest must exist")
        return json.loads(util.read_text(manifest))

    # ------------------------------------------------------------- bug B / C
    def test_plugin_manifest_version_matches_source(self) -> None:
        self.assertEqual(self.plugin_manifest()["version"], self.source_version())

    def test_plugin_manifest_version_is_not_placeholder(self) -> None:
        self.assertNotEqual(
            self.plugin_manifest()["version"],
            "0.0.0",
            "a silent 0.0.0 fallback hides the real Skill version",
        )

    def test_missing_version_fails_the_build(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = util.copy_source_tree(Path(tmp) / "repo")
            skill = src / "SKILL.md"
            text = util.read_text(skill)
            stripped = re.sub(r"^\s+version:.*\n", "", text, count=1, flags=re.MULTILINE)
            self.assertNotEqual(text, stripped, "test fixture failed to strip version")
            skill.write_text(stripped, encoding="utf-8")
            proc = util.run_script(
                "package_claude_code_plugin.py",
                cwd=src,
                check=False,
                scripts_dir=src / "scripts",
            )
            self.assertNotEqual(
                proc.returncode,
                0,
                "build must fail loudly when metadata.version is missing",
            )

    # ----------------------------------------------------------------- bug A
    def test_plugin_contains_referenced_content_files(self) -> None:
        missing: list[str] = []
        for md in util.markdown_files(self.plugin_pkg):
            for ref in util.packaged_references(util.read_text(md)):
                if not (self.plugin_pkg / ref).exists():
                    missing.append(f"{md.relative_to(self.plugin_pkg)} -> {ref}")
        self.assertEqual(missing, [], f"{len(missing)} dangling links in plugin package")

    def test_skill_package_contains_referenced_content_files(self) -> None:
        missing: list[str] = []
        for md in util.markdown_files(self.skill_pkg):
            for ref in util.packaged_references(util.read_text(md)):
                if not (self.skill_pkg / ref).exists():
                    missing.append(f"{md.relative_to(self.skill_pkg)} -> {ref}")
        self.assertEqual(missing, [], f"{len(missing)} dangling links in Skill package")

    def test_isolated_plugin_copy_resolves_all_references(self) -> None:
        """An installed plugin must not depend on the source checkout."""
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            installed = Path(tmp) / "installed-plugin"
            shutil.copytree(self.plugin_pkg, installed)
            missing: list[str] = []
            for md in util.markdown_files(installed):
                for ref in util.packaged_references(util.read_text(md)):
                    if not (installed / ref).exists():
                        missing.append(f"{md.relative_to(installed)} -> {ref}")
            self.assertEqual(missing, [], "isolated install has unresolved references")

    def test_both_packages_ship_the_same_content_set(self) -> None:
        def content_files(root: Path) -> set[str]:
            return {
                p.relative_to(root).as_posix()
                for p in root.rglob("*")
                if p.is_file()
                and p.relative_to(root).as_posix().startswith(
                    ("references/", "cards/", "profiles/")
                )
            }

        skill_set = content_files(self.skill_pkg)
        plugin_set = content_files(self.plugin_pkg)
        self.assertNotEqual(skill_set, set(), "Skill package has no content files")
        self.assertEqual(
            skill_set,
            plugin_set,
            "standalone Skill and plugin must ship an identical guidance set",
        )

    # ------------------------------------------------------- packaging hygiene
    def test_license_present_in_both_packages(self) -> None:
        self.assertTrue((self.skill_pkg / "LICENSE").is_file())
        self.assertTrue((self.plugin_pkg / "LICENSE").is_file())

    def test_runtime_packages_exclude_dev_only_scripts(self) -> None:
        """Dev scripts that need tests/ or benchmarks/ must not ship."""
        dev_only = {
            "validate_skill.py",
            "package_skill.py",
            "package_claude_code_plugin.py",
            "run_tests.py",
            "analyze_trace.py",
        }
        for pkg in (self.skill_pkg, self.plugin_pkg):
            shipped = {p.name for p in (pkg / "scripts").glob("*") if p.is_file()}
            leaked = sorted(shipped & dev_only)
            self.assertEqual(
                leaked, [], f"{pkg.name} ships dev-only scripts: {leaked}"
            )

    def test_builds_are_reproducible(self) -> None:
        first_skill = util.tree_snapshot(self.skill_pkg)
        first_plugin = util.tree_snapshot(self.plugin_pkg)
        util.build_packages()
        self.assertEqual(first_skill, util.tree_snapshot(self.skill_pkg))
        self.assertEqual(first_plugin, util.tree_snapshot(self.plugin_pkg))

    def test_generated_files_have_no_timestamps_or_random_ids(self) -> None:
        suspicious = re.compile(
            r"\b(19|20)\d{2}-\d{2}-\d{2}T\d{2}:\d{2}"  # ISO timestamp
            r"|\bbuilt_at\b|\bbuildTime\b|\bbuild_id\b"
            r"|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            re.IGNORECASE,
        )
        for pkg in (self.skill_pkg, self.plugin_pkg):
            for path in sorted(pkg.rglob("*.json")):
                text = util.read_text(path)
                self.assertIsNone(
                    suspicious.search(text),
                    f"{path.relative_to(pkg)} contains build-time or random content",
                )

    def test_build_only_writes_inside_dist(self) -> None:
        """A build must never delete or rewrite tracked source directories."""
        watched = ["SKILL.md", "references", "bootstrap", "scripts", "tests"]
        before = {
            name: util.tree_snapshot(util.ROOT / name)
            if (util.ROOT / name).is_dir()
            else {name: util.read_text(util.ROOT / name)}
            for name in watched
            if (util.ROOT / name).exists()
        }
        util.build_packages()
        after = {
            name: util.tree_snapshot(util.ROOT / name)
            if (util.ROOT / name).is_dir()
            else {name: util.read_text(util.ROOT / name)}
            for name in watched
            if (util.ROOT / name).exists()
        }
        self.assertEqual(before, after, "build mutated source files")

    # ------------------------------------------------------------ bug C guard
    def test_validator_detects_dangling_plugin_references(self) -> None:
        """Corrupt a built package; the validator must not report PASS."""
        with tempfile.TemporaryDirectory() as tmp:
            src = util.copy_source_tree(Path(tmp) / "repo")
            broken = src / "scripts" / "break_marker.txt"
            broken.write_text("marker\n", encoding="utf-8")
            skill = src / "SKILL.md"
            text = util.read_text(skill)
            skill.write_text(
                text + "\n\nSee [missing guide](references/this-file-does-not-exist.md).\n",
                encoding="utf-8",
            )
            proc = util.run_script(
                "validate_skill.py",
                cwd=src,
                check=False,
                scripts_dir=src / "scripts",
            )
            self.assertNotEqual(
                proc.returncode,
                0,
                "validator must fail when SKILL.md points at a missing reference",
            )


if __name__ == "__main__":
    unittest.main()
