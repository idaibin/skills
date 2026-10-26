#!/usr/bin/env python3
"""Regressions for the deterministic Skill routing evaluator."""

from __future__ import annotations

import importlib.util
import copy
import contextlib
import io
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run-skill-routing-evals.py"
SPEC = importlib.util.spec_from_file_location("run_skill_routing_evals", SCRIPT)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class SkillRoutingEvalTests(unittest.TestCase):
    def test_baseline_status_is_explicit_in_console_and_json(self) -> None:
        paths = {
            str(ROOT / "skills-index.json"): {"packages": []},
            str(ROOT / "evals" / "skill-routing-cases.json"): {"cases": []},
            str(ROOT / "docs" / "skills" / "skill-routing-cases.schema.json"): {},
            str(ROOT / "evals" / "skill-routing-baseline.json"): {"cases": []},
        }
        for baseline, errors, checked in (
            (None, [], False),
            ({"cases": []}, [], True),
            ({"cases": []}, ["invalid current contract"], False),
        ):
            for as_json in (True, False):
                with self.subTest(checked=checked, errors=errors, json=as_json):
                    args = SimpleNamespace(
                        index=ROOT / "skills-index.json", cases=ROOT / "evals" / "skill-routing-cases.json",
                        schema=ROOT / "docs" / "skills" / "skill-routing-cases.schema.json",
                        migrations=Path("missing-migrations"), basis="synthetic", baseline_ref="baseline-ref" if baseline is not None else None,
                        write_report=None, json=as_json,
                    )
                    stdout = io.StringIO()
                    with (
                        patch.object(RUNNER, "parse_args", return_value=args),
                        patch.object(RUNNER, "load_json", side_effect=lambda path: paths[str(path)]),
                        patch.object(RUNNER, "validate_case_contract", return_value=errors),
                        patch.object(RUNNER, "evaluate", return_value=[]),
                        patch.object(RUNNER, "load_baseline", return_value=baseline),
                        patch.object(RUNNER, "regression_errors", return_value=[]) as compare,
                        patch.object(RUNNER.SEARCH, "package_entries", return_value=[]),
                        contextlib.redirect_stdout(stdout),
                    ):
                        self.assertEqual(1 if errors else 0, RUNNER.main())
                    self.assertEqual(1 if checked else 0, compare.call_count)
                    if as_json:
                        report = json.loads(stdout.getvalue())
                        self.assertIs(checked, report["summary"]["baseline_checked"])
                    else:
                        self.assertEqual(not checked, "baseline unchecked" in stdout.getvalue())

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

    def test_rerouted_boundary_case_migrates_via_retired_observed_owner(self) -> None:
        baseline = {
            "cases": [
                {
                    "id": "dev-java-boundary",
                    "skill": "dev-java",
                    "case_fingerprint": "sha256:old",
                    "status": "passed",
                    "observed_owner": "audit-java",
                },
                {
                    "id": "repo-map-normal",
                    "skill": "repo-map",
                    "case_fingerprint": "sha256:same",
                    "status": "passed",
                    "observed_owner": "repo-map",
                },
            ]
        }
        current = [
            {
                "id": "dev-java-audit-reroute",
                "skill": "dev-java",
                "case_fingerprint": "sha256:new",
                "status": "passed",
                "observed_owner": "repo-audit",
            },
            {
                "id": "repo-map-normal",
                "skill": "repo-map",
                "case_fingerprint": "sha256:same",
                "status": "passed",
                "observed_owner": "repo-map",
            },
        ]
        self.assertEqual(
            [],
            RUNNER.regression_errors(current, baseline, retired_skills={"audit-java"}),
        )

    def test_active_case_removal_definition_change_and_owner_drift_still_fail(self) -> None:
        baseline = {
            "cases": [
                {
                    "id": "keep-normal",
                    "skill": "repo-map",
                    "case_fingerprint": "sha256:same",
                    "status": "passed",
                    "observed_owner": "repo-map",
                },
                {
                    "id": "drift-normal",
                    "skill": "repo-map",
                    "case_fingerprint": "sha256:fp",
                    "status": "passed",
                    "observed_owner": "repo-map",
                },
                {
                    "id": "active-removed-normal",
                    "skill": "repo-map",
                    "case_fingerprint": "sha256:x",
                    "status": "passed",
                    "observed_owner": "repo-map",
                },
            ]
        }
        current = [
            {
                "id": "keep-normal",
                "skill": "repo-map",
                "case_fingerprint": "sha256:changed",
                "status": "passed",
                "observed_owner": "repo-map",
            },
            {
                "id": "drift-normal",
                "skill": "repo-map",
                "case_fingerprint": "sha256:fp",
                "status": "passed",
                "observed_owner": "dev-frontend",
            },
        ]
        errors = RUNNER.regression_errors(current, baseline, retired_skills={"audit-java"})
        self.assertTrue(any("definition changed" in error for error in errors))
        self.assertTrue(any("owner changed" in error for error in errors))
        self.assertTrue(any("case removed" in error for error in errors))

    def test_approved_owner_migration_requires_exact_old_and_new_evidence(self) -> None:
        old = {
            "cases": [{
                "id": "device-owner", "skill": "ops-client",
                "case_fingerprint": "sha256:" + "a" * 64,
                "status": "passed", "observed_owner": "ops-client",
            }]
        }
        new = [{
            "id": "device-owner", "skill": "ops-client",
            "case_fingerprint": "sha256:" + "b" * 64,
            "status": "passed", "observed_owner": "ops-device",
        }]
        manifest = {
            "schema_version": "skill-routing-migrations/v1",
            "migrations": [{
                "case_id": "device-owner",
                "from_fingerprint": "sha256:" + "a" * 64,
                "from_owner": "ops-client",
                "to_fingerprint": "sha256:" + "b" * 64,
                "to_owner": "ops-device",
                "reason": "approved-mobile-device-owner-split",
                "approved_on": "2026-10-22",
            }],
        }
        self.assertEqual([], RUNNER.regression_errors(new, old, migrations=manifest))
        wrong = copy.deepcopy(manifest)
        wrong["migrations"][0]["to_owner"] = "ops-browser"
        self.assertTrue(any("migration evidence mismatch" in error for error in RUNNER.regression_errors(new, old, migrations=wrong)))
        failed = copy.deepcopy(new)
        failed[0]["status"] = "failed"
        self.assertTrue(any("migration evidence mismatch" in error for error in RUNNER.regression_errors(failed, old, migrations=manifest)))

        for field, value in (
            ("from_fingerprint", "sha256:" + "c" * 64),
            ("to_fingerprint", "sha256:" + "c" * 64),
            ("from_owner", "ops-browser"),
        ):
            with self.subTest(mismatch=field):
                changed = copy.deepcopy(manifest)
                changed["migrations"][0][field] = value
                self.assertTrue(any("migration evidence mismatch" in error for error in RUNNER.regression_errors(new, old, migrations=changed)))
        duplicate = copy.deepcopy(manifest)
        duplicate["migrations"].append(copy.deepcopy(duplicate["migrations"][0]))
        self.assertTrue(any("duplicate migration" in error for error in RUNNER.regression_errors(new, old, migrations=duplicate)))
        unused = copy.deepcopy(manifest)
        unused["migrations"][0]["case_id"] = "unrelated"
        self.assertTrue(any("migration not applicable" in error for error in RUNNER.regression_errors(new, old, migrations=unused)))
        unrelated_old = copy.deepcopy(old)
        extra = copy.deepcopy(old["cases"][0])
        extra["id"] = "unrelated"
        unrelated_old["cases"].append(extra)
        self.assertIn("baseline case removed: unrelated", RUNNER.regression_errors(new, unrelated_old, migrations=manifest))
        absorbed = {"cases": copy.deepcopy(new)}
        self.assertEqual([], RUNNER.regression_errors(new, absorbed, migrations=manifest))
        for field, value in (("case_fingerprint", "sha256:" + "c" * 64), ("observed_owner", "ops-browser"), ("status", "failed")):
            with self.subTest(absorbed_drift=field):
                changed = copy.deepcopy(new)
                changed[0][field] = value
                self.assertTrue(RUNNER.regression_errors(changed, absorbed, migrations=manifest))

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
