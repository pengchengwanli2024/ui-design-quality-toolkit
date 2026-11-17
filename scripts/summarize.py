#!/usr/bin/env python3
"""Summarize a Lighthouse LHR JSON file; optionally compare recorded settings."""

import argparse
import json
import math
from pathlib import Path


METRICS = (
    "first-contentful-paint", "largest-contentful-paint", "speed-index",
    "total-blocking-time", "cumulative-layout-shift", "interaction-to-next-paint",
)
SETTINGS = (
    "formFactor", "screenEmulation", "emulatedUserAgent", "throttlingMethod",
    "throttling", "disableStorageReset", "onlyCategories", "onlyAudits",
    "skipAudits", "blockedUrlPatterns", "locale",
)


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def load_report(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "steps" in data:
        raise ValueError("User-flow container: select a single step's lhr JSON first.")
    if not isinstance(data, dict) or not data.get("lighthouseVersion"):
        raise ValueError("Expected a Lighthouse result (LHR) with lighthouseVersion.")
    for field in ("categories", "audits", "configSettings"):
        if not isinstance(data.get(field, {}), dict):
            raise ValueError(f"Expected {field} to be an object.")
    if not data.get("runtimeError") and ("categories" not in data or "audits" not in data):
        raise ValueError("LHR is missing categories or audits.")
    return data


def summarize(data):
    audits = data.get("audits", {})
    errors = [
        {"id": key, "message": audit.get("errorMessage")}
        for key, audit in audits.items()
        if audit.get("scoreDisplayMode") == "error" or audit.get("errorMessage")
    ]
    scores = {
        key: round(category["score"] * 100, 2) if number(category.get("score")) else None
        for key, category in data.get("categories", {}).items()
    }
    metrics = {
        key: {
            "value": audits[key]["numericValue"] if number(audits[key].get("numericValue")) else None,
            "unit": audits[key].get("numericUnit"),
            "display": audits[key].get("displayValue"),
        }
        for key in METRICS if key in audits
    }
    findings = [
        {"id": key, "title": audit.get("title"), "score": audit["score"],
         "display": audit.get("displayValue")}
        for key, audit in audits.items()
        if number(audit.get("score")) and audit["score"] < 1
    ]
    config = data.get("configSettings", {})
    return {
        "status": "failed" if data.get("runtimeError") else "partial" if errors else "valid",
        "requested_url": data.get("requestedUrl"),
        "final_url": data.get("finalDisplayedUrl") or data.get("finalUrl"),
        "version": data["lighthouseVersion"], "fetch_time": data.get("fetchTime"),
        "gather_mode": data.get("gatherMode"),
        "config": {key: config.get(key) for key in SETTINGS},
        "browser": data.get("environment", {}).get("hostUserAgent"),
        "runtime_error": data.get("runtimeError"),
        "warnings": data.get("runWarnings", []), "audit_errors": errors,
        "scores": scores, "metrics": metrics,
        "findings": findings,
        "interpretation": "Valid describes report execution, not site acceptance. Lab metrics do not prove field CWV, WCAG compliance, or visual quality.",
    }


def compare(before, after, before_settings, after_settings):
    mismatches = []
    for key in ("version", "final_url", "gather_mode", "browser"):
        if before[key] != after[key]:
            mismatches.append(key)
    for key in sorted(before_settings.keys() | after_settings.keys()):
        if key not in before_settings or key not in after_settings or before_settings[key] != after_settings[key]:
            mismatches.append("config." + key)
    for label, summary in (("before", before), ("after", after)):
        if summary["status"] != "valid":
            mismatches.append(label + "." + summary["status"])
        for key in ("version", "final_url", "gather_mode"):
            if not summary[key]:
                mismatches.append(label + ".missing_" + key)
        for key in ("formFactor", "throttlingMethod"):
            if not summary["config"][key]:
                mismatches.append(label + ".missing_config." + key)
    result = {
        "settings_match": not mismatches, "mismatches": mismatches,
        "manual_checks": [
            "Confirm the same authenticated state, page data, build mode, and cache policy.",
            "Confirm comparable machine/network load; collect repeated sequential runs before performance claims.",
            "Review warnings and verify the final URL is the intended page; settings_match alone does not establish comparability.",
        ],
    }
    if not mismatches:
        result["score_deltas"] = {
            key: round(value - before["scores"][key], 2)
            for key, value in after["scores"].items()
            if number(value) and number(before["scores"].get(key))
        }
        result["metric_deltas"] = {}
        result["skipped_metric_deltas"] = {}
        for key, metric in after["metrics"].items():
            previous = before["metrics"].get(key)
            if previous is None:
                reason = "missing_baseline_metric"
            elif not number(metric["value"]) or not number(previous["value"]):
                reason = "unavailable_value"
            elif not metric["unit"] or not previous["unit"]:
                reason = "unknown_unit"
            elif metric["unit"] != previous["unit"]:
                reason = "unit_mismatch"
            else:
                result["metric_deltas"][key] = {
                    "value": round(metric["value"] - previous["value"], 6),
                    "unit": metric["unit"],
                }
                continue
            result["skipped_metric_deltas"][key] = reason
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Current navigation/snapshot/timespan LHR JSON")
    parser.add_argument("--compare", metavar="BEFORE", help="Earlier LHR JSON")
    args = parser.parse_args()
    try:
        current_data = load_report(args.report)
        current = summarize(current_data)
        if args.compare:
            before_data = load_report(args.compare)
            before = summarize(before_data)
            current["comparison"] = compare(
                before, current, before_data.get("configSettings", {}),
                current_data.get("configSettings", {}),
            )
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(json.dumps({"status": "invalid", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(current, indent=2, ensure_ascii=False, allow_nan=False))
    return 1 if current["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
