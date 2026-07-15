#!/usr/bin/env python3
"""Regression tests for compare-skill-evals.py."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("compare-skill-evals.py")
SPEC = importlib.util.spec_from_file_location("compare_skill_evals_test", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
COMPARE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = COMPARE
SPEC.loader.exec_module(COMPARE)


class FakeScore:
    def __init__(self, passed: bool) -> None:
        self.passed = passed
        self.lines = ("fixture scorer",)


class FakeEvaluator(types.ModuleType):
    def __init__(self) -> None:
        super().__init__("fake_evaluator")
        self.CONTRACTS = {
            "behavior_eval": {
                "comparative": {
                    "minimum_trials_per_variant": 3,
                    "candidate_variant": "candidate",
                    "control_variants": ["baseline", "previous"],
                    "require_held_out_cases": True,
                    "maximum_outcome_regression": 0.0,
                    "minimum_absolute_outcome_improvement": 0.1,
                    "minimum_relative_efficiency_improvement": 0.15,
                    "allow_duration_efficiency_gate": False,
                    "maximum_pair_capture_gap_seconds": 3600,
                }
            }
        }

    @staticmethod
    def load_jsonl(path: Path) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    @staticmethod
    def discover_skill_names() -> set[str]:
        return {"repo-map", "repo-review"}

    @staticmethod
    def revision_is_ancestor(_ancestor, _descendant, *, strict=False):
        return True

    @staticmethod
    def validate_routing_cases(cases, known_skills, *, routing_graph_path):
        del cases, known_skills, routing_graph_path
        return []

    @staticmethod
    def validate_held_out_routing_cases(cases, known_skills):
        del cases, known_skills
        return []

    @staticmethod
    def validate_authority_cases(cases, known_skills):
        del cases, known_skills
        return []

    validate_workflow_cases = validate_authority_cases

    @staticmethod
    def load_result_bundle(
        path: Path,
        expected_ids: set[str],
        dataset_path: Path,
        prompts: dict[str, str],
        *,
        evidence_kind: str,
    ) -> dict[str, object]:
        del dataset_path, prompts, evidence_kind
        payload = json.loads(path.read_text(encoding="utf-8"))
        results = payload["results"]
        if {row["id"] for row in results} != expected_ids:
            raise ValueError("fixture result coverage mismatch")
        payload["_verified_results"] = {
            row["id"]: row["observations"] for row in results
        }
        return payload

    @staticmethod
    def score_routing(cases, bundle) -> FakeScore:
        del cases
        return FakeScore(bool(bundle.get("formal_pass", True)))

    score_authority = score_routing
    score_workflow = score_routing


class CompareSkillEvalsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.dataset = self.root / "routing-held-out.jsonl"
        self.cases = [
            {
                "id": f"case-{index}",
                "prompt": f"prompt {index}",
                "expected_owner": "repo-map",
            }
            for index in range(10)
        ]
        self.dataset.write_text(
            "\n".join(json.dumps(case) for case in self.cases) + "\n",
            encoding="utf-8",
        )
        self.evaluator = FakeEvaluator()
        self.bundle_sequence = 0

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_bundle(
        self,
        *,
        variant: str,
        trial: int,
        correct: int = 10,
        duration_ms: int = 100,
        held_out: bool = True,
        host: str = "fixture-host",
        raw_seed: str | None = None,
        tokens: int | None = 100,
    ) -> Path:
        self.bundle_sequence += 1
        bundle_dir = self.root / f"{variant}-{trial}-{self.bundle_sequence}"
        bundle_dir.mkdir()
        results = []
        for index, case in enumerate(self.cases):
            result_tokens = (
                None
                if tokens is None
                else tokens // len(self.cases) + int(index < tokens % len(self.cases))
            )
            result_duration = duration_ms // len(self.cases) + int(
                index < duration_ms % len(self.cases)
            )
            seed = raw_seed or f"{variant}-{trial}"
            results.append(
                {
                    "id": case["id"],
                    "observations": {
                        "actual_owner": (
                            "repo-map" if index < correct else "repo-review"
                        ),
                        "handoffs": [],
                    },
                    "raw_evidence_sha256": f"{seed}-{index:02d}".encode().hex().ljust(64, "0")[:64],
                    "metrics": {
                        "duration_ms": result_duration,
                        "input_tokens": result_tokens,
                        "output_tokens": 0 if result_tokens is not None else None,
                    },
                }
            )
        payload = {
            "run_id": f"run-{variant}-{trial}-{bundle_dir.name}",
            "captured_at": f"2026-07-15T00:{trial:02d}:00+00:00",
            "model": "fixture-model",
            "host": host,
            "skill_revision": "d" * 40 if variant == "candidate" else "e" * 40,
            "skill_tree_sha": "f" * 40 if variant == "candidate" else "1" * 40,
            "dataset_revision": "a" * 64,
            "run_config": {
                "variant": variant,
                "trial": trial,
                "pair_id": f"00000000-0000-4000-8000-{trial:012d}",
                "dataset_path": str(self.dataset),
                "dataset_git_revision": "9" * 40,
                "evaluation_anchor_revision": "d" * 40,
                "held_out_provenance_path": "evals/routing-held-out-provenance.json",
                "held_out_provenance_sha256": "5" * 64,
                "prompt_set_sha256": "a" * 64,
                "case_set_sha256": "7" * 64,
                "held_out": held_out,
                "permissions": "read-only",
                "timeout_seconds": 60,
                "concurrency": 1,
                "host_name": "codex",
                "fixture_sha256": "b" * 64,
                "skills_installed": variant in {"candidate", "previous"},
                "skill_fixture_sha256": (
                    ("3" if variant == "candidate" else "4") * 64
                    if variant in {"candidate", "previous"}
                    else None
                ),
                "host_config_sha256": "c" * 64,
                "prompt_template_version": 1,
                "prompt_template_sha256": "6" * 64,
            },
            "adjudication": {
                "method": "deterministic",
                "reviewer": "fixture-reviewer",
                "reviewer_version": "1",
                "config_sha256": "2" * 64,
            },
            "formal_pass": True,
            "results": results,
        }
        path = bundle_dir / "results.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def report(self, candidates: list[Path], controls: list[Path]):
        return COMPARE.generate_report(
            kind="routing",
            candidate_paths=candidates,
            control_paths=controls,
            dataset=self.dataset,
            evaluator=self.evaluator,
        )

    def matched(
        self,
        *,
        candidate_correct=10,
        control_correct=10,
        candidate_ms=100,
        control_ms=100,
    ):
        candidates = [
            self.write_bundle(
                variant="candidate",
                trial=trial,
                correct=candidate_correct,
                duration_ms=candidate_ms,
            )
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(
                variant="previous",
                trial=trial,
                correct=control_correct,
                duration_ms=control_ms,
            )
            for trial in range(1, 4)
        ]
        return candidates, controls

    def test_missing_control_fails(self) -> None:
        candidates, _ = self.matched()
        report = self.report(candidates, [])
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("--control", report["errors"][0])

    def test_contract_minimum_trials_is_enforced(self) -> None:
        candidates, controls = self.matched()
        report = self.report(candidates[:2], controls[:2])
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("at least 3 trials", report["errors"][0])

    def test_replayed_raw_evidence_fails(self) -> None:
        candidates, controls = self.matched()
        replay = json.loads(controls[0].read_text(encoding="utf-8"))
        original = json.loads(candidates[0].read_text(encoding="utf-8"))
        replay["results"][0]["raw_evidence_sha256"] = original["results"][0][
            "raw_evidence_sha256"
        ]
        controls[0].write_text(json.dumps(replay), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("raw evidence", report["errors"][0])

    def test_replayed_run_id_fails(self) -> None:
        candidates, controls = self.matched()
        replay = json.loads(controls[0].read_text(encoding="utf-8"))
        original = json.loads(candidates[0].read_text(encoding="utf-8"))
        replay["run_id"] = original["run_id"]
        controls[0].write_text(json.dumps(replay), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("run_id", report["errors"][0])

    def test_duplicate_trial_fails(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(candidates[2].read_text(encoding="utf-8"))
        changed["run_config"]["trial"] = 2
        candidates[2].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("duplicate trial", report["errors"][0])

    def test_condition_mismatch_fails(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(controls[1].read_text(encoding="utf-8"))
        changed["host"] = "different-host"
        controls[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("condition differs", report["errors"][0])

    def test_host_name_mismatch_fails_even_when_host_version_matches(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["run_config"]["host_name"] = "claude"
        controls[0].write_text(json.dumps(changed), encoding="utf-8")

        report = self.report(candidates, controls)

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("condition differs", report["errors"][0])

    def test_previous_control_must_be_candidate_ancestor(self) -> None:
        candidates, controls = self.matched()
        with mock.patch.object(
            self.evaluator, "revision_is_ancestor", return_value=False
        ):
            report = self.report(candidates, controls)

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("strict ancestor", report["errors"][0])

    def test_trial_pair_id_and_capture_window_are_enforced(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["run_config"]["pair_id"] = "00000000-0000-4000-8000-999999999999"
        controls[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("pair_id", report["errors"][0])

        candidates, controls = self.matched()
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["captured_at"] = "2026-07-15T04:00:00+00:00"
        controls[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("capture gap", report["errors"][0])

    def test_adjudication_mismatch_fails(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(controls[1].read_text(encoding="utf-8"))
        changed["adjudication"]["config_sha256"] = "9" * 64
        controls[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("adjudication", report["errors"][0])

    def test_previous_control_must_use_a_different_skill_revision(self) -> None:
        candidates, controls = self.matched()
        candidate = json.loads(candidates[0].read_text(encoding="utf-8"))
        for path in controls:
            changed = json.loads(path.read_text(encoding="utf-8"))
            changed["skill_revision"] = candidate["skill_revision"]
            changed["skill_tree_sha"] = candidate["skill_tree_sha"]
            path.write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("different Skill revision", report["errors"][0])

    def test_candidate_requires_installed_skills_and_skill_fixture(self) -> None:
        candidates, controls = self.matched(candidate_correct=10, control_correct=9)
        changed = json.loads(candidates[0].read_text(encoding="utf-8"))
        changed["run_config"]["skills_installed"] = False
        candidates[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skills_installed=true", report["errors"][0])

    def test_previous_requires_a_skill_fixture_sha(self) -> None:
        candidates, controls = self.matched(candidate_correct=10, control_correct=9)
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["run_config"]["skill_fixture_sha256"] = None
        controls[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skill_fixture_sha256", report["errors"][0])

    def test_baseline_requires_no_installed_skills_and_reports_the_fixture(self) -> None:
        candidates = [
            self.write_bundle(
                variant="candidate", trial=trial, correct=10
            )
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(variant="baseline", trial=trial, correct=9)
            for trial in range(1, 4)
        ]
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["candidate"]["trials"][0]["skills_installed"])
        self.assertEqual(
            report["candidate"]["trials"][0]["skill_fixture_sha256"],
            "3" * 64,
        )
        self.assertFalse(report["control"]["trials"][0]["skills_installed"])
        self.assertIsNone(
            report["control"]["trials"][0]["skill_fixture_sha256"]
        )

    def test_baseline_rejects_a_skill_fixture(self) -> None:
        candidates = [
            self.write_bundle(variant="candidate", trial=trial, correct=10)
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(variant="baseline", trial=trial, correct=9)
            for trial in range(1, 4)
        ]
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["run_config"]["skill_fixture_sha256"] = "8" * 64
        controls[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skill_fixture_sha256 must be null", report["errors"][0])

    def test_baseline_rejects_installed_skills(self) -> None:
        candidates = [
            self.write_bundle(variant="candidate", trial=trial, correct=10)
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(variant="baseline", trial=trial, correct=9)
            for trial in range(1, 4)
        ]
        changed = json.loads(controls[0].read_text(encoding="utf-8"))
        changed["run_config"]["skills_installed"] = True
        controls[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skills_installed=false", report["errors"][0])

    def test_held_out_is_required_for_every_variant(self) -> None:
        candidates, controls = self.matched()
        changed = json.loads(controls[2].read_text(encoding="utf-8"))
        changed["run_config"]["held_out"] = False
        controls[2].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("held_out=true", report["errors"][0])

    def test_non_held_out_condition_allows_null_provenance_fields(self) -> None:
        path = self.write_bundle(variant="candidate", trial=1, held_out=False)
        bundle = json.loads(path.read_text(encoding="utf-8"))
        for field in (
            "dataset_git_revision",
            "evaluation_anchor_revision",
            "held_out_provenance_path",
            "held_out_provenance_sha256",
        ):
            bundle["run_config"][field] = None

        condition = COMPARE._condition(bundle, path=path)

        self.assertEqual((None, None, None, None), condition[-4:])

    def test_held_out_routing_uses_its_28_case_two_kind_coverage(self) -> None:
        evaluator = COMPARE.load_evaluator()
        known_skills = sorted(evaluator.discover_skill_names())
        cases = []
        for index, skill_name in enumerate(known_skills):
            neighbor = known_skills[(index + 1) % len(known_skills)]
            for kind_index, kind in enumerate(("trigger", "neighbor_non_trigger")):
                cases.append(
                    {
                        "id": f"heldout-{index + 1:02d}-{kind_index + 1}",
                        "prompt": (
                            f"Fresh held-out request {index + 1}, "
                            f"boundary form {kind_index + 1}."
                        ),
                        "kind": kind,
                        "expected_owner": skill_name,
                        "allowed_owners": [skill_name],
                        "forbidden_owners": [neighbor],
                        "required_handoffs": [],
                        "allowed_handoffs": [],
                        "forbidden_handoffs": [],
                        "high_risk": False,
                    }
                )

        self.assertEqual(len(cases), 28)
        COMPARE._validate_dataset_cases(
            evaluator,
            "routing",
            cases,
            dataset_path=self.dataset,
            held_out=True,
        )

        cases[1]["kind"] = "trigger"
        with self.assertRaisesRegex(
            COMPARE.ComparisonError,
            "missing kinds.*neighbor_non_trigger",
        ):
            COMPARE._validate_dataset_cases(
                evaluator,
                "routing",
                cases,
                dataset_path=self.dataset,
                held_out=True,
            )

    def test_outcome_regression_fails(self) -> None:
        candidates, controls = self.matched(candidate_correct=9, control_correct=10)
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["comparison"]["outcome_non_regression"])

    def test_every_candidate_trial_must_pass_the_contract(self) -> None:
        candidates, controls = self.matched(candidate_correct=10, control_correct=9)
        changed = json.loads(candidates[1].read_text(encoding="utf-8"))
        changed["formal_pass"] = False
        candidates[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["comparison"]["candidate_contracts_passed"])

    def test_ten_percentage_point_outcome_gain_passes(self) -> None:
        candidates, controls = self.matched(candidate_correct=10, control_correct=9)
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "PASS")
        self.assertAlmostEqual(
            report["comparison"]["outcome_absolute_improvement"], 0.1
        )
        self.assertTrue(report["comparison"]["outcome_threshold_met"])

    def test_bundle_dataset_path_is_used_without_cli_override(self) -> None:
        candidates, controls = self.matched(candidate_correct=10, control_correct=9)
        report = COMPARE.generate_report(
            kind="routing",
            candidate_paths=candidates,
            control_paths=controls,
            dataset=None,
            evaluator=self.evaluator,
        )
        self.assertEqual(report["status"], "PASS")

    def test_duration_gain_is_reported_but_not_used_as_a_gate(self) -> None:
        candidates, controls = self.matched(candidate_ms=85, control_ms=100)
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertAlmostEqual(
            report["comparison"]["duration_relative_improvement"], 0.15
        )
        self.assertFalse(report["comparison"]["duration_threshold_met"])
        self.assertEqual(
            report["comparison"]["duration_gate_status"],
            "disabled-unpaired-load-risk",
        )

    def test_unavailable_tokens_are_not_used_for_efficiency_gate(self) -> None:
        candidates = [
            self.write_bundle(
                variant="candidate", trial=trial, duration_ms=85, tokens=None
            )
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(
                variant="previous", trial=trial, duration_ms=100, tokens=None
            )
            for trial in range(1, 4)
        ]
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["candidate"]["tokens"]["availability"], "unavailable")
        self.assertEqual(report["comparison"]["token_comparison"], "unavailable")
        self.assertIsNone(report["comparison"]["token_relative_improvement"])

    def test_fifteen_percent_token_gain_passes(self) -> None:
        candidates = [
            self.write_bundle(variant="candidate", trial=trial, tokens=85)
            for trial in range(1, 4)
        ]
        controls = [
            self.write_bundle(variant="previous", trial=trial, tokens=100)
            for trial in range(1, 4)
        ]
        report = self.report(candidates, controls)
        self.assertEqual(report["status"], "PASS")
        self.assertAlmostEqual(
            report["comparison"]["token_relative_improvement"], 0.15
        )
        self.assertTrue(report["comparison"]["token_threshold_met"])


if __name__ == "__main__":
    unittest.main()
