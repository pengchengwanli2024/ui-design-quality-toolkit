import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "summarize.py"


def report():
    return {
        "lighthouseVersion": "13.6.0",
        "requestedUrl": "http://localhost/dashboard",
        "finalDisplayedUrl": "http://localhost/dashboard",
        "fetchTime": "2026-11-17T08:00:00.000Z",
        "gatherMode": "navigation",
        "configSettings": {
            "formFactor": "mobile", "throttlingMethod": "simulate",
            "screenEmulation": {"width": 412, "height": 823},
        },
        "categories": {"performance": {"score": 0.8}, "seo": {"score": None}},
        "audits": {
            "largest-contentful-paint": {
                "numericValue": 2400, "numericUnit": "millisecond", "score": 0.8,
            },
            "cumulative-layout-shift": {
                "numericValue": 0.04, "numericUnit": "unitless", "score": 1,
            },
        },
        "runWarnings": ["Synthetic fixture; not a measured page"],
    }


class SummarizeTests(unittest.TestCase):
    def run_report(self, current, before=None, expected_exit=0):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "current.json"
            path.write_text(json.dumps(current))
            args = [sys.executable, str(SCRIPT), str(path)]
            if before is not None:
                baseline = Path(directory) / "before.json"
                baseline.write_text(json.dumps(before))
                args += ["--compare", str(baseline)]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected_exit, result.stderr)
            self.assertTrue(result.stdout.strip(), result.stderr)
            return json.loads(result.stdout)

    def test_preserves_unavailable_scores_units_and_warnings(self):
        result = self.run_report(report())
        self.assertEqual(result["scores"], {"performance": 80, "seo": None})
        self.assertEqual(result["metrics"]["cumulative-layout-shift"]["unit"], "unitless")
        self.assertEqual(result["warnings"], report()["runWarnings"])

    def test_runtime_failure_is_reported_and_blocks_comparison(self):
        failed = report()
        failed["runtimeError"] = {"code": "NO_FCP", "message": "No page content"}
        result = self.run_report(failed, report(), expected_exit=1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["runtime_error"]["code"], "NO_FCP")
        self.assertFalse(result["comparison"]["settings_match"])
        self.assertNotIn("score_deltas", result["comparison"])

    def test_redirect_device_and_version_mismatches_block_deltas(self):
        after = report()
        after["finalDisplayedUrl"] = "http://localhost/login"
        after["configSettings"]["formFactor"] = "desktop"
        after["lighthouseVersion"] = "14.0.0"
        result = self.run_report(after, report())
        self.assertFalse(result["comparison"]["settings_match"])
        self.assertIn("final_url", result["comparison"]["mismatches"])
        self.assertIn("config.formFactor", result["comparison"]["mismatches"])
        self.assertIn("version", result["comparison"]["mismatches"])
        self.assertNotIn("metric_deltas", result["comparison"])

    def test_matching_settings_emit_deltas_with_manual_limits(self):
        after = report()
        after["categories"]["performance"]["score"] = 0.9
        after["audits"]["largest-contentful-paint"]["numericValue"] = 2100
        result = self.run_report(after, report())
        comparison = result["comparison"]
        self.assertTrue(comparison["settings_match"])
        self.assertEqual(comparison["score_deltas"]["performance"], 10)
        self.assertNotIn("seo", comparison["score_deltas"])
        self.assertEqual(comparison["metric_deltas"]["largest-contentful-paint"]["value"], -300)
        self.assertTrue(comparison["manual_checks"])

    def test_partial_audit_errors_are_visible(self):
        partial = report()
        partial["audits"]["image-alt"] = {
            "score": None, "scoreDisplayMode": "error", "errorMessage": "Audit failed",
        }
        result = self.run_report(partial)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["audit_errors"][0]["id"], "image-alt")

    def test_unknown_units_do_not_produce_metric_deltas(self):
        before = report()
        after = report()
        del before["audits"]["largest-contentful-paint"]["numericUnit"]
        del after["audits"]["largest-contentful-paint"]["numericUnit"]
        after["audits"]["largest-contentful-paint"]["numericValue"] = 2100
        comparison = self.run_report(after, before)["comparison"]
        self.assertNotIn("largest-contentful-paint", comparison["metric_deltas"])
        self.assertEqual(comparison["skipped_metric_deltas"]["largest-contentful-paint"], "unknown_unit")

    def test_changed_units_explain_why_a_metric_delta_is_skipped(self):
        before = report()
        after = report()
        after["audits"]["largest-contentful-paint"]["numericUnit"] = "second"
        after["audits"]["largest-contentful-paint"]["numericValue"] = 2.1
        comparison = self.run_report(after, before)["comparison"]
        self.assertNotIn("largest-contentful-paint", comparison["metric_deltas"])
        self.assertIn("skipped_metric_deltas", comparison)
        self.assertEqual(comparison["skipped_metric_deltas"]["largest-contentful-paint"], "unit_mismatch")

    def test_missing_measurement_context_blocks_comparison(self):
        incomplete = report()
        del incomplete["configSettings"]["throttlingMethod"]
        result = self.run_report(incomplete, copy.deepcopy(incomplete))
        self.assertFalse(result["comparison"]["settings_match"])

    def test_additional_recorded_config_changes_block_deltas(self):
        before = report()
        after = report()
        before["configSettings"]["clearStorageTypes"] = ["cache_storage"]
        after["configSettings"]["clearStorageTypes"] = []
        after["audits"]["largest-contentful-paint"]["numericValue"] = 2100
        comparison = self.run_report(after, before)["comparison"]
        self.assertFalse(comparison["settings_match"])
        self.assertIn("config.clearStorageTypes", comparison["mismatches"])
        self.assertNotIn("metric_deltas", comparison)

    def test_header_changes_block_comparison_without_echoing_credentials(self):
        before = report()
        after = report()
        before["configSettings"]["extraHeaders"] = {"Authorization": "synthetic-before-secret"}
        after["configSettings"]["extraHeaders"] = {"Authorization": "synthetic-after-secret"}
        result = self.run_report(after, before)
        self.assertFalse(result["comparison"]["settings_match"])
        self.assertIn("config.extraHeaders", result["comparison"]["mismatches"])
        output = json.dumps(result)
        self.assertNotIn("synthetic-before-secret", output)
        self.assertNotIn("synthetic-after-secret", output)

    def test_flow_container_is_rejected_instead_of_fabricating_scores(self):
        result = self.run_report({"steps": [{"lhr": report()}]}, expected_exit=2)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("step", result["error"].lower())


if __name__ == "__main__":
    unittest.main()
