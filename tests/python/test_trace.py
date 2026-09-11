"""Tests for the offline trace analyser.

SCOPE: these prove the analyser reports honestly on hand-written fixtures.
They are not cache benchmarks. No provider is contacted, no token count here
was measured, and a passing run says nothing about real cache behaviour.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import bridge_test_utils as util

FIXTURES = util.ROOT / "benchmarks" / "fixtures"
STABLE = FIXTURES / "trace-stable-prefix.json"
REWRITTEN = FIXTURES / "trace-rewritten-prefix.json"
TOOL = "analyze_trace.py"


class TraceToolTestCase(unittest.TestCase):
    def run_tool(self, *args):
        return util.run_script(TOOL, *args, check=False)

    def report(self, path):
        proc = self.run_tool(str(path), "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr[:400])
        return json.loads(proc.stdout)


class ToolContractTestCase(TraceToolTestCase):
    def test_selftest_passes(self):
        proc = self.run_tool("--selftest")
        self.assertEqual(proc.returncode, 0, (proc.stdout + proc.stderr)[:400])
        self.assertIn("OK", proc.stdout)

    def test_no_arguments_is_a_clean_error(self):
        proc = self.run_tool()
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)

    def test_malformed_trace_fails_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("{not json at all", encoding="utf-8")
            proc = self.run_tool(str(bad))
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertIn("valid JSON", proc.stderr)

    def test_missing_file_fails_without_a_traceback(self):
        proc = self.run_tool("/nonexistent/trace.json")
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)

    def test_single_request_reports_that_it_cannot_compare(self):
        with tempfile.TemporaryDirectory() as tmp:
            one = Path(tmp) / "one.json"
            one.write_text(
                json.dumps({"request": {"tools": [], "system": "x", "messages": []}}),
                encoding="utf-8",
            )
            proc = self.run_tool(str(one))
        self.assertEqual(proc.returncode, 0, proc.stderr[:400])
        self.assertIn("nothing to compare", proc.stdout)
        self.assertIn("not comparable", proc.stdout)

    def test_jsonl_input_is_accepted(self):
        record = {
            "request": {
                "tools": [],
                "system": "stable",
                "messages": [{"role": "user", "content": "a"}],
            }
        }
        second = json.loads(json.dumps(record))
        second["request"]["messages"].append({"role": "user", "content": "b"})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            path.write_text(
                json.dumps(record) + "\n" + json.dumps(second) + "\n", encoding="utf-8"
            )
            proc = self.run_tool(str(path), "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr[:400])
        report = json.loads(proc.stdout)
        self.assertTrue(report["verdict"]["prefix_preserved"])


class StableTraceTestCase(TraceToolTestCase):
    def test_appended_messages_count_as_a_preserved_prefix(self):
        report = self.report(STABLE)
        self.assertTrue(report["verdict"]["prefix_preserved"])
        kinds = {item["divergence"]["kind"] for item in report["comparisons"]}
        self.assertEqual(kinds, {"appended"})
        sections = {item["divergence"]["section"] for item in report["comparisons"]}
        self.assertEqual(sections, {"messages"})

    def test_hook_text_is_reported_as_stable(self):
        report = self.report(STABLE)
        self.assertEqual(report["hook_text"]["variants"], 1)
        self.assertTrue(report["hook_text"]["stable"])

    def test_absent_usage_is_unknown_and_reported_zero_is_kept(self):
        report = self.report(STABLE)
        values = [row["values"]["cache_read_input_tokens"] for row in report["usage"]]
        self.assertIn(None, values, "an absent usage field must stay unknown")
        self.assertIn(0, values, "a provider-reported zero must survive as zero")

    def test_text_output_distinguishes_unknown_from_zero(self):
        proc = self.run_tool(str(STABLE))
        self.assertEqual(proc.returncode, 0, proc.stderr[:400])
        self.assertIn("unknown is not zero", proc.stdout)
        self.assertIn("cache_read_input_tokens=unknown", proc.stdout)
        self.assertIn("cache_read_input_tokens=0", proc.stdout)

    def test_gate_passes_for_a_stable_trace(self):
        proc = self.run_tool(str(STABLE), "--fail-on-rewrite")
        self.assertEqual(proc.returncode, 0, proc.stderr[:400])


class RewrittenTraceTestCase(TraceToolTestCase):
    def test_first_divergent_region_is_located_in_prefix_order(self):
        report = self.report(REWRITTEN)
        sections = [item["divergence"]["section"] for item in report["comparisons"]]
        self.assertEqual(sections[0], "system", "rewritten system block must be found")
        self.assertIn("tools", sections, "reordered tools must be found")
        self.assertFalse(report["verdict"]["prefix_preserved"])

    def test_divergence_carries_a_before_and_after_preview(self):
        report = self.report(REWRITTEN)
        first = report["comparisons"][0]["divergence"]
        self.assertEqual(first["kind"], "rewritten")
        self.assertTrue(first["left_preview"])
        self.assertTrue(first["right_preview"])
        self.assertNotEqual(first["left_preview"], first["right_preview"])

    def test_unstable_hook_text_is_flagged(self):
        report = self.report(REWRITTEN)
        self.assertGreater(report["hook_text"]["variants"], 1)
        self.assertFalse(report["hook_text"]["stable"])

    def test_gate_fails_for_a_rewritten_trace(self):
        proc = self.run_tool(str(REWRITTEN), "--fail-on-rewrite")
        self.assertEqual(proc.returncode, 1)

    def test_text_output_names_the_rewritten_region(self):
        proc = self.run_tool(str(REWRITTEN))
        self.assertIn("PREFIX REWRITTEN at system[1]", proc.stdout)


class HonestyTestCase(TraceToolTestCase):
    def test_scope_disclaimer_is_always_printed(self):
        proc = self.run_tool(str(STABLE))
        lowered = proc.stdout.lower()
        self.assertIn("not a provider cache simulator", lowered)
        self.assertIn("after translation", lowered)
        self.assertIn("only live usage fields can show that", lowered)

    def test_synthetic_input_is_labelled_in_the_report(self):
        proc = self.run_tool(str(STABLE))
        self.assertIn("SYNTHETIC FIXTURE", proc.stdout)
        for path in (STABLE, REWRITTEN):
            data = json.loads(util.read_text(path))
            self.assertTrue(data.get("synthetic"), f"{path.name} must declare itself")

    def test_tool_never_invents_a_hit_rate_or_a_saving(self):
        text = util.read_text(util.ROOT / "scripts" / TOOL).lower()
        for forbidden in ("hit_rate", "hit rate", "savings", "cost_saved", "estimated cost"):
            self.assertTrue(forbidden not in text, f"analyser must not compute {forbidden}")

    def test_output_is_deterministic(self):
        first = self.run_tool(str(STABLE), "--json").stdout
        second = self.run_tool(str(STABLE), "--json").stdout
        self.assertEqual(first, second)

    def test_analyser_is_not_shipped_inside_the_packages(self):
        util.build_packages()
        for package in (util.SKILL_PACKAGE, util.PLUGIN_PACKAGE):
            self.assertFalse(
                (package / "scripts" / TOOL).exists(),
                f"dev tooling must stay out of {package.name}",
            )


if __name__ == "__main__":
    unittest.main()
