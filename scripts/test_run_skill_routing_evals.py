#!/usr/bin/env python3
"""Regressions for the deterministic Skill routing evaluator."""

from __future__ import annotations

import importlib.util
import copy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run-skill-routing-evals.py"
SPEC = importlib.util.spec_from_file_location("run_skill_routing_evals", SCRIPT)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class SkillRoutingEvalTests(unittest.TestCase):
    def test_current_matrix_covers_and_passes_every_catalog_skill(self) -> None:
        index = RUNNER.load_json(RUNNER.DEFAULT_INDEX)
        cases = RUNNER.load_json(RUNNER.DEFAULT_CASES)
        schema = RUNNER.load_json(RUNNER.DEFAULT_SCHEMA)
        self.assertEqual([], RUNNER.validate_case_contract(index, cases, schema))
        evaluated = RUNNER.evaluate(index, cases)
        self.assertEqual(52, len(evaluated))
        self.assertTrue(all(case["status"] == "passed" for case in evaluated))

    def test_published_baseline_covers_every_current_case(self) -> None:
        cases = RUNNER.load_json(RUNNER.DEFAULT_CASES)
        baseline = RUNNER.load_json(ROOT / "evals" / "skill-routing-baseline.json")
        self.assertEqual(
            {case["id"] for case in cases["cases"]},
            {case["id"] for case in baseline["cases"]},
        )

    def test_baseline_pass_cannot_disappear_change_definition_or_change_owner(self) -> None:
        current = [
            {
                "id": "sample-normal",
                "case_fingerprint": "sha256:new",
                "status": "passed",
                "observed_owner": "sample-skill",
            },
            {
                "id": "owner-normal",
                "case_fingerprint": "sha256:same",
                "status": "passed",
                "observed_owner": "new-owner",
            }
        ]
        baseline = {
            "cases": [
                {
                    "id": "sample-normal",
                    "case_fingerprint": "sha256:old",
                    "status": "passed",
                    "observed_owner": "different-skill",
                },
                {
                    "id": "owner-normal",
                    "case_fingerprint": "sha256:same",
                    "status": "passed",
                    "observed_owner": "old-owner",
                },
                {
                    "id": "removed-normal",
                    "case_fingerprint": "sha256:removed",
                    "status": "passed",
                    "observed_owner": "sample-skill",
                },
            ]
        }
        errors = RUNNER.regression_errors(current, baseline)
        self.assertTrue(any("definition changed" in error for error in errors))
        self.assertTrue(any("owner changed" in error for error in errors))
        self.assertTrue(any("case removed" in error for error in errors))

    def test_retired_skill_cases_may_leave_the_baseline(self) -> None:
        baseline = {
            "cases": [
                {
                    "id": "retired-normal",
                    "skill": "retired-skill",
                    "case_fingerprint": "sha256:retired",
                    "status": "passed",
                    "observed_owner": "retired-skill",
                }
            ]
        }
        self.assertEqual(
            [],
            RUNNER.regression_errors([], baseline, retired_skills={"retired-skill"}),
        )

    def test_unrelated_critical_stop_prompt_fails_execution_signal(self) -> None:
        index = RUNNER.load_json(RUNNER.DEFAULT_INDEX)
        cases = RUNNER.load_json(RUNNER.DEFAULT_CASES)
        mutated = copy.deepcopy(cases)
        critical = next(case for case in mutated["cases"] if case["class"] == "critical-stop")
        critical["prompt"] = "unrelated calendar text with no stop instruction"
        result = next(case for case in RUNNER.evaluate(index, mutated) if case["id"] == critical["id"])
        self.assertEqual("failed", result["status"])
        self.assertIn("owning-skill signal", result["failures"][0])

    def test_authorized_condition_does_not_classify_as_missing_authorization(self) -> None:
        index = RUNNER.load_json(RUNNER.DEFAULT_INDEX)
        cases = RUNNER.load_json(RUNNER.DEFAULT_CASES)
        mutated = copy.deepcopy(cases)
        critical = next(case for case in mutated["cases"] if case["id"] == "repo-delivery-critical-stop")
        critical["prompt"] = "Commit this reviewed branch; authorization is granted; continue."
        result = next(case for case in RUNNER.evaluate(index, mutated) if case["id"] == critical["id"])
        self.assertEqual("failed", result["status"])
        self.assertIsNone(result["observed_stop"])

    def test_empty_or_malformed_baseline_is_rejected(self) -> None:
        current = [{"id": "case", "status": "passed", "observed_owner": "owner"}]
        self.assertIn("non-empty", RUNNER.regression_errors(current, {})[0])
        errors = RUNNER.regression_errors(current, {"cases": [{"id": "case"}]})
        self.assertIn("missing required", errors[0])


if __name__ == "__main__":
    unittest.main()
