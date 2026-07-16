#!/usr/bin/env python3
"""Regression tests for compare-skill-evals.py."""

from __future__ import annotations

import hashlib
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
                    "required_control_variants": ["previous", "baseline"],
                    "require_held_out_cases": True,
                    "maximum_full_case_regression_vs_previous": 0.0,
                    "minimum_full_case_improvement_vs_previous": 0.1,
                    "minimum_full_case_improvement_vs_no_skill": 0.1,
                    "minimum_relative_marginal_skill_input_reduction": 0.15,
                    "minimum_absolute_marginal_input_savings_tokens_per_case": 50,
                    "require_candidate_overhead_not_greater_per_group": True,
                    "allow_duration_efficiency_gate": False,
                    "claimable_dimensions": [
                        "routing_outcome_vs_previous",
                        "routing_outcome_vs_no_skill",
                        "marginal_skill_input_efficiency",
                    ],
                    "maximum_group_capture_gap_seconds": 3600,
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
        return strict

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
    def assess_routing_case(case, result) -> dict[str, bool]:
        accepted_owners = {
            case["expected_owner"],
            *case.get("allowed_owners", []),
        }
        observed_handoffs = set(result.get("handoffs", []))
        required_handoffs = set(case.get("required_handoffs", []))
        allowed_handoffs = required_handoffs | set(
            case.get("allowed_handoffs", [])
        )
        forbidden_handoffs = set(case.get("forbidden_handoffs", []))
        return {
            "full_case_success": (
                result.get("actual_owner") in accepted_owners
                and required_handoffs <= observed_handoffs
                and not (forbidden_handoffs & observed_handoffs)
                and observed_handoffs <= allowed_handoffs
            )
        }

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
                "allowed_owners": ["repo-map"],
                "required_handoffs": [],
                "allowed_handoffs": [],
                "forbidden_handoffs": [],
            }
            for index in range(10)
        ]
        self.dataset.write_text(
            "\n".join(json.dumps(case) for case in self.cases) + "\n",
            encoding="utf-8",
        )
        self.evaluator = FakeEvaluator()
        self.bundle_sequence = 0
        self.campaign = types.SimpleNamespace(
            campaign_id="00000000-0000-4000-8000-000000000099",
            artifact_root="eval-results/routing/campaigns/00000000-0000-4000-8000-000000000099",
            relative_path="evals/routing-campaign.json",
            sha256="9" * 64,
            anchor_revision="d" * 40,
            previous_revision="e" * 40,
            trial_groups={
                trial: f"00000000-0000-4000-8000-{trial:012d}"
                for trial in range(1, 4)
            },
            payload={"evaluation_protocol": {"sha256": "8" * 64}},
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    @staticmethod
    def _split(total: int, count: int, index: int) -> int:
        return total // count + int(index < total % count)

    def write_bundle(
        self,
        *,
        variant: str,
        trial: int,
        correct: int = 10,
        unauthorized_handoffs: int = 0,
        duration_ms: int = 100,
        input_tokens: int | None = 120,
        output_tokens: int | None = 10,
        held_out: bool = True,
        host: str = "fixture-host",
        raw_seed: str | None = None,
        comparison_group_id: str | None = None,
        captured_at: str | None = None,
        skill_revision: str | None = None,
        skill_tree_sha: str | None = None,
        formal_pass: bool = True,
        retried_results: int = 0,
    ) -> Path:
        self.bundle_sequence += 1
        bundle_dir = self.root / f"{variant}-{trial}-{self.bundle_sequence}"
        bundle_dir.mkdir()
        results = []
        seed = raw_seed or bundle_dir.name
        for index, case in enumerate(self.cases):
            result_input = (
                None
                if input_tokens is None
                else self._split(input_tokens, len(self.cases), index)
            )
            result_output = (
                None
                if output_tokens is None
                else self._split(output_tokens, len(self.cases), index)
            )
            results.append(
                {
                    "id": case["id"],
                    "observations": {
                        "actual_owner": (
                            "repo-map" if index < correct else "repo-review"
                        ),
                        "handoffs": (
                            ["repo-review"]
                            if index < unauthorized_handoffs
                            else []
                        ),
                    },
                    "raw_evidence_sha256": hashlib.sha256(
                        f"{seed}-{index}".encode()
                    ).hexdigest(),
                    "metrics": {
                        "duration_ms": self._split(
                            duration_ms, len(self.cases), index
                        ),
                        "input_tokens": result_input,
                        "output_tokens": result_output,
                        "attempt_count": 2 if index < retried_results else 1,
                        "retry_count": 1 if index < retried_results else 0,
                    },
                }
            )

        if comparison_group_id is None:
            comparison_group_id = f"00000000-0000-4000-8000-{trial:012d}"
        if captured_at is None:
            variant_offset = {"candidate": 0, "previous": 1, "baseline": 2}[variant]
            minute = trial * 5 + variant_offset
            captured_at = f"2026-07-15T00:{minute:02d}:00+00:00"
        candidate_revision = "d" * 40
        candidate_tree = "f" * 40
        if skill_revision is None:
            skill_revision = "e" * 40 if variant == "previous" else candidate_revision
        if skill_tree_sha is None:
            skill_tree_sha = "1" * 40 if variant == "previous" else candidate_tree

        payload = {
            "run_id": f"00000000-0000-4001-8000-{self.bundle_sequence:012d}",
            "captured_at": captured_at,
            "model": "fixture-model",
            "host": host,
            "skill_revision": skill_revision,
            "skill_tree_sha": skill_tree_sha,
            "dataset_revision": "a" * 64,
            "run_config": {
                "variant": variant,
                "trial": trial,
                "comparison_group_id": comparison_group_id,
                "campaign_id": self.campaign.campaign_id,
                "campaign_path": self.campaign.relative_path,
                "campaign_sha256": self.campaign.sha256,
                "evaluation_protocol_revision": self.campaign.anchor_revision,
                "evaluation_protocol_sha256": self.campaign.payload[
                    "evaluation_protocol"
                ]["sha256"],
                "dataset_path": str(self.dataset),
                "dataset_git_revision": "9" * 40,
                "evaluation_anchor_revision": "d" * 40,
                "held_out_provenance_path": (
                    "evals/routing-held-out-provenance.json"
                ),
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
                "environment_policy_sha256": "d" * 64,
                "retry_policy_sha256": "e" * 64,
                "prompt_template_version": 2,
                "prompt_template_sha256": "6" * 64,
            },
            "adjudication": {
                "method": "deterministic",
                "reviewer": "fixture-reviewer",
                "reviewer_version": "1",
                "config_sha256": "2" * 64,
            },
            "formal_pass": formal_pass,
            "results": results,
        }
        path = bundle_dir / "results.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def report(
        self,
        candidates: list[Path],
        previous: list[Path],
        baseline: list[Path],
        *,
        dataset: Path | None = None,
    ) -> dict[str, object]:
        with mock.patch.object(
            COMPARE,
            "_validate_campaign_attempt_ledger",
            return_value={
                "planned_slots": 9,
                "observed_successful_attempts": 9,
                "failed_or_extra_attempts": 0,
            },
        ):
            return COMPARE.generate_report(
                kind="routing",
                candidate_paths=candidates,
                previous_paths=previous,
                baseline_paths=baseline,
                dataset=self.dataset if dataset is None else dataset,
                evaluator=self.evaluator,
                campaign=self.campaign,
            )

    def matched(
        self,
        *,
        candidate_correct: int = 10,
        previous_correct: int = 10,
        baseline_correct: int = 10,
        candidate_handoffs: int = 0,
        candidate_ms: int = 100,
        previous_ms: int = 100,
        baseline_ms: int = 100,
        candidate_input: int | None = 120,
        previous_input: int | None = 120,
        baseline_input: int | None = 100,
        candidate_retried_results: int = 0,
    ) -> tuple[list[Path], list[Path], list[Path]]:
        candidates = [
            self.write_bundle(
                variant="candidate",
                trial=trial,
                correct=candidate_correct,
                unauthorized_handoffs=candidate_handoffs,
                duration_ms=candidate_ms,
                input_tokens=candidate_input,
                retried_results=candidate_retried_results,
            )
            for trial in range(1, 4)
        ]
        previous = [
            self.write_bundle(
                variant="previous",
                trial=trial,
                correct=previous_correct,
                duration_ms=previous_ms,
                input_tokens=previous_input,
            )
            for trial in range(1, 4)
        ]
        baseline = [
            self.write_bundle(
                variant="baseline",
                trial=trial,
                correct=baseline_correct,
                duration_ms=baseline_ms,
                input_tokens=baseline_input,
            )
            for trial in range(1, 4)
        ]
        return candidates, previous, baseline

    def test_all_three_variants_are_required(self) -> None:
        candidates, previous, baseline = self.matched()
        for missing, expected in (
            (([], previous, baseline), "--candidate"),
            ((candidates, [], baseline), "--previous"),
            ((candidates, previous, []), "--baseline"),
        ):
            report = self.report(*missing)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn(expected, report["errors"][0])

    def test_contract_minimum_trials_is_enforced_per_variant(self) -> None:
        candidates, previous, baseline = self.matched()
        report = self.report(candidates[:2], previous[:2], baseline[:2])
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("candidate requires at least 3 trials", report["errors"][0])

    def test_trial_sets_must_match(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[2].read_text(encoding="utf-8"))
        changed["run_config"]["trial"] = 4
        baseline[2].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("complete campaign trial set", report["errors"][0])

    def test_duplicate_trial_fails(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(candidates[2].read_text(encoding="utf-8"))
        changed["run_config"]["trial"] = 2
        candidates[2].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("duplicate trial", report["errors"][0])

    def test_three_way_group_id_and_capture_window_are_enforced(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(previous[0].read_text(encoding="utf-8"))
        changed["run_config"]["comparison_group_id"] = (
            "00000000-0000-4000-8000-999999999999"
        )
        previous[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("comparison_group_id values must match", report["errors"][0])

        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[0].read_text(encoding="utf-8"))
        changed["captured_at"] = "2026-07-15T03:00:00+00:00"
        baseline[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("three-way capture gap", report["errors"][0])

    def test_group_id_must_be_unique_across_trials(self) -> None:
        candidates, previous, baseline = self.matched()
        first = json.loads(candidates[0].read_text(encoding="utf-8"))["run_config"][
            "comparison_group_id"
        ]
        for path in (candidates[1], previous[1], baseline[1]):
            changed = json.loads(path.read_text(encoding="utf-8"))
            changed["run_config"]["comparison_group_id"] = first
            path.write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("does not match the campaign", report["errors"][0])

    def test_replayed_run_or_raw_evidence_fails(self) -> None:
        candidates, previous, baseline = self.matched()
        replay = json.loads(previous[0].read_text(encoding="utf-8"))
        original = json.loads(candidates[0].read_text(encoding="utf-8"))
        replay["run_id"] = original["run_id"]
        previous[0].write_text(json.dumps(replay), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("run_id", report["errors"][0])

        candidates, previous, baseline = self.matched()
        replay = json.loads(previous[0].read_text(encoding="utf-8"))
        original = json.loads(candidates[0].read_text(encoding="utf-8"))
        replay["results"][0]["raw_evidence_sha256"] = original["results"][0][
            "raw_evidence_sha256"
        ]
        previous[0].write_text(json.dumps(replay), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("raw evidence", report["errors"][0])

    def test_condition_and_adjudication_must_match(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(previous[1].read_text(encoding="utf-8"))
        changed["host"] = "different-host"
        previous[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("condition differs", report["errors"][0])

        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[1].read_text(encoding="utf-8"))
        changed["adjudication"]["config_sha256"] = "8" * 64
        baseline[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("adjudication", report["errors"][0])

        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[1].read_text(encoding="utf-8"))
        changed["run_config"]["retry_policy_sha256"] = "0" * 64
        baseline[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("condition differs", report["errors"][0])

    def test_previous_must_be_strict_ancestor_with_different_tree(self) -> None:
        candidates, previous, baseline = self.matched()
        with mock.patch.object(
            self.evaluator, "revision_is_ancestor", return_value=False
        ):
            report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("strict ancestor", report["errors"][0])

        candidates, previous, baseline = self.matched()
        candidate_tree = json.loads(candidates[0].read_text(encoding="utf-8"))[
            "skill_tree_sha"
        ]
        for path in previous:
            changed = json.loads(path.read_text(encoding="utf-8"))
            changed["skill_tree_sha"] = candidate_tree
            path.write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("different skills tree", report["errors"][0])

    def test_baseline_uses_candidate_revision_and_tree_without_skills(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_correct=10, previous_correct=9
        )
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["no_skill"]["trials"][0]["skills_installed"])
        self.assertIsNone(
            report["no_skill"]["trials"][0]["skill_fixture_sha256"]
        )

        for path in baseline:
            changed = json.loads(path.read_text(encoding="utf-8"))
            changed["skill_tree_sha"] = "8" * 40
            path.write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("candidate revision and skills tree", report["errors"][0])

    def test_baseline_rejects_installed_skills_or_skill_fixture(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[0].read_text(encoding="utf-8"))
        changed["run_config"]["skills_installed"] = True
        baseline[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skills_installed=false", report["errors"][0])

        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[0].read_text(encoding="utf-8"))
        changed["run_config"]["skill_fixture_sha256"] = "8" * 64
        baseline[0].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("skill_fixture_sha256 must be null", report["errors"][0])

    def test_routing_outcome_uses_full_case_success(self) -> None:
        candidates, previous, baseline = self.matched(candidate_handoffs=1)
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["candidate"]["outcome"]["mean"], 0.9)
        self.assertFalse(report["candidate_vs_previous"]["outcome_non_regression"])
        self.assertEqual(report["status"], "FAIL")

    def test_candidate_contract_failure_blocks_every_claim(self) -> None:
        candidates, previous, baseline = self.matched(previous_correct=9)
        changed = json.loads(candidates[1].read_text(encoding="utf-8"))
        changed["formal_pass"] = False
        candidates[1].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["candidate_contracts_passed"])
        self.assertEqual(report["claimable_dimensions"], [])

    def test_previous_outcome_improvement_can_pass(self) -> None:
        candidates, previous, baseline = self.matched(previous_correct=9)
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "PASS")
        self.assertAlmostEqual(
            report["candidate_vs_previous"]["outcome_absolute_improvement"],
            0.1,
        )
        self.assertTrue(report["candidate_vs_previous"]["outcome_threshold_met"])
        self.assertEqual(
            report["claimable_dimensions"], ["routing_outcome_vs_previous"]
        )

    def test_no_skill_outcome_improvement_can_pass(self) -> None:
        candidates, previous, baseline = self.matched(baseline_correct=9)
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["candidate_vs_no_skill"]["outcome_threshold_met"])
        self.assertEqual(
            report["claimable_dimensions"], ["routing_outcome_vs_no_skill"]
        )

    def test_marginal_skill_input_reduction_can_pass(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_input=600,
            previous_input=1200,
            baseline_input=100,
        )
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(marginal["gate_eligible"])
        self.assertGreater(marginal["relative_reduction"], 0.5)
        self.assertGreaterEqual(marginal["absolute_savings_tokens_per_case"], 50)
        self.assertTrue(marginal["threshold_met"])
        self.assertEqual(
            report["claimable_dimensions"],
            ["marginal_skill_input_efficiency"],
        )

    def test_marginal_gate_rejects_small_absolute_savings(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_input=110,
            previous_input=120,
            baseline_input=100,
        )
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertTrue(marginal["gate_eligible"])
        self.assertAlmostEqual(marginal["relative_reduction"], 0.5)
        self.assertEqual(marginal["absolute_savings_tokens_per_case"], 1)
        self.assertFalse(marginal["threshold_met"])

    def test_marginal_gate_requires_every_group_to_be_noninferior(self) -> None:
        candidate_totals = (1300, 300, 300)
        candidates = [
            self.write_bundle(
                variant="candidate", trial=trial, input_tokens=candidate_totals[trial - 1]
            )
            for trial in range(1, 4)
        ]
        previous = [
            self.write_bundle(variant="previous", trial=trial, input_tokens=1200)
            for trial in range(1, 4)
        ]
        baseline = [
            self.write_bundle(variant="baseline", trial=trial, input_tokens=100)
            for trial in range(1, 4)
        ]
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertFalse(marginal["candidate_overhead_not_greater_each_group"])
        self.assertFalse(marginal["gate_eligible"])
        self.assertFalse(marginal["threshold_met"])

    def test_marginal_gate_requires_complete_nonnegative_input_overhead(self) -> None:
        candidates, previous, baseline = self.matched(candidate_input=None)
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertEqual(marginal["availability"], "unavailable")
        self.assertFalse(marginal["gate_eligible"])
        self.assertFalse(marginal["threshold_met"])

        candidates, previous, baseline = self.matched(
            candidate_input=90,
            previous_input=120,
            baseline_input=100,
        )
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertFalse(marginal["all_group_overheads_nonnegative"])
        self.assertFalse(marginal["gate_eligible"])
        self.assertIsNone(marginal["relative_reduction"])

    def test_zero_token_metrics_are_rejected_not_counted(self) -> None:
        candidates, previous, baseline = self.matched(candidate_input=0)
        report = self.report(candidates, previous, baseline)
        self.assertEqual("FAIL", report["status"])
        self.assertIn("must be a positive integer or null", report["errors"][0])

    def test_marginal_gate_requires_positive_previous_mean(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_input=100,
            previous_input=100,
            baseline_input=100,
        )
        report = self.report(candidates, previous, baseline)
        marginal = report["marginal_skill_input_overhead"]
        self.assertFalse(marginal["previous_mean_overhead_positive"])
        self.assertFalse(marginal["gate_eligible"])
        self.assertIsNone(marginal["relative_reduction"])

    def test_previous_regression_blocks_otherwise_met_dimensions(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_correct=9,
            previous_correct=10,
            baseline_correct=8,
            candidate_input=110,
            previous_input=1200,
            baseline_input=100,
        )
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["candidate_vs_previous"]["outcome_non_regression"])
        self.assertTrue(report["candidate_vs_no_skill"]["outcome_threshold_met"])
        self.assertTrue(report["marginal_skill_input_overhead"]["threshold_met"])
        self.assertEqual(report["claimable_dimensions"], [])
        self.assertFalse(any(report["claimable_dimension_status"].values()))

    def test_duration_is_reported_but_never_gates(self) -> None:
        candidates, previous, baseline = self.matched(
            candidate_ms=85,
            previous_ms=100,
            baseline_ms=100,
        )
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertAlmostEqual(
            report["candidate_vs_previous"]["duration_relative_reduction"],
            0.15,
        )
        self.assertEqual(
            report["candidate_vs_previous"][
                "duration_and_total_tokens_gate_status"
            ],
            "reported-only",
        )

    def test_input_output_and_total_tokens_are_aggregated_separately(self) -> None:
        candidates = [
            self.write_bundle(
                variant="candidate",
                trial=trial,
                input_tokens=110,
                output_tokens=20,
            )
            for trial in range(1, 4)
        ]
        previous = [
            self.write_bundle(
                variant="previous",
                trial=trial,
                input_tokens=120,
                output_tokens=30,
            )
            for trial in range(1, 4)
        ]
        baseline = [
            self.write_bundle(
                variant="baseline",
                trial=trial,
                input_tokens=100,
                output_tokens=10,
            )
            for trial in range(1, 4)
        ]
        report = self.report(candidates, previous, baseline)
        first = report["candidate"]["trials"][0]
        self.assertEqual(first["input_tokens"], 110)
        self.assertEqual(first["output_tokens"], 20)
        self.assertEqual(first["total_tokens"], 130)
        self.assertEqual(report["candidate"]["tokens"]["input"]["mean"], 110)
        self.assertEqual(report["candidate"]["tokens"]["output"]["mean"], 20)
        self.assertEqual(report["candidate"]["tokens"]["total"]["mean"], 130)

    def test_retry_metrics_are_aggregated_without_changing_score_or_tokens(self) -> None:
        candidates = [
            self.write_bundle(
                variant="candidate",
                trial=trial,
                retried_results=retried,
            )
            for trial, retried in enumerate((2, 0, 1), start=1)
        ]
        previous = [
            self.write_bundle(variant="previous", trial=trial, correct=9)
            for trial in range(1, 4)
        ]
        baseline = [
            self.write_bundle(variant="baseline", trial=trial)
            for trial in range(1, 4)
        ]

        report = self.report(candidates, previous, baseline)

        first = report["candidate"]["trials"][0]
        self.assertEqual(first["attempt_count"], 12)
        self.assertEqual(first["retry_count"], 2)
        self.assertEqual(report["candidate"]["attempt_count"]["total"], 33)
        self.assertEqual(report["candidate"]["retry_count"]["total"], 3)
        self.assertEqual(report["candidate"]["outcome"]["mean"], 1.0)
        self.assertEqual(report["candidate"]["tokens"]["input"]["mean"], 120)
        self.assertEqual(report["campaign"]["retry_policy_sha256"], "e" * 64)

    def test_retry_metrics_are_required_and_consistent(self) -> None:
        mutations = (
            ("attempt_count", None, "attempt_count cannot be null"),
            ("attempt_count", True, "positive integer or null"),
            ("retry_count", None, "non-negative integer"),
            ("retry_count", 1, "must equal metrics.attempt_count - 1"),
        )
        for field, value, expected_error in mutations:
            with self.subTest(field=field, value=value):
                candidates, previous, baseline = self.matched()
                changed = json.loads(candidates[0].read_text(encoding="utf-8"))
                changed["results"][0]["metrics"][field] = value
                candidates[0].write_text(json.dumps(changed), encoding="utf-8")

                report = self.report(candidates, previous, baseline)

                self.assertEqual(report["status"], "FAIL")
                self.assertIn(expected_error, report["errors"][0])

    def test_held_out_is_required_for_every_variant(self) -> None:
        candidates, previous, baseline = self.matched()
        changed = json.loads(baseline[2].read_text(encoding="utf-8"))
        changed["run_config"]["held_out"] = False
        baseline[2].write_text(json.dumps(changed), encoding="utf-8")
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("held_out=true", report["errors"][0])

    def test_bundle_dataset_path_is_used_without_cli_override(self) -> None:
        candidates, previous, baseline = self.matched(previous_correct=9)
        with mock.patch.object(
            COMPARE,
            "_validate_campaign_attempt_ledger",
            return_value={
                "planned_slots": 9,
                "observed_successful_attempts": 9,
                "failed_or_extra_attempts": 0,
            },
        ):
            report = COMPARE.generate_report(
                kind="routing",
                candidate_paths=candidates,
                previous_paths=previous,
                baseline_paths=baseline,
                dataset=None,
                evaluator=self.evaluator,
                campaign=self.campaign,
            )
        self.assertEqual(report["status"], "PASS")

    def test_schema_four_report_exposes_stable_manifest_keys(self) -> None:
        candidates, previous, baseline = self.matched(previous_correct=9)
        report = self.report(candidates, previous, baseline)
        self.assertEqual(report["schema_version"], 4)
        for key in (
            "candidate",
            "previous",
            "no_skill",
            "candidate_vs_previous",
            "candidate_vs_no_skill",
            "marginal_skill_input_overhead",
        ):
            self.assertIn(key, report)
        self.assertIsInstance(
            report["candidate_vs_previous"]["outcome_threshold_met"], bool
        )
        self.assertIsInstance(
            report["candidate_vs_previous"]["outcome_non_regression"], bool
        )
        self.assertIsInstance(
            report["candidate_vs_no_skill"]["outcome_threshold_met"], bool
        )
        self.assertIsInstance(
            report["marginal_skill_input_overhead"]["threshold_met"], bool
        )
        self.assertEqual(
            set(report["claimable_dimension_status"]),
            {
                "routing_outcome_vs_previous",
                "routing_outcome_vs_no_skill",
                "marginal_skill_input_efficiency",
            },
        )

    def test_cli_accepts_repeated_three_way_bundle_options(self) -> None:
        args = COMPARE.parse_args(
            [
                "--kind",
                "routing",
                "--candidate",
                "candidate-1.json",
                "--candidate",
                "candidate-2.json",
                "--previous",
                "previous-1.json",
                "--baseline",
                "baseline-1.json",
                "--campaign",
                "campaign.json",
            ]
        )
        self.assertEqual(len(args.candidate), 2)
        self.assertEqual(len(args.previous), 1)
        self.assertEqual(len(args.baseline), 1)

    def test_campaign_attempt_ledger_requires_exact_successful_slots(self) -> None:
        campaigns_root = COMPARE.ROOT / "eval-results" / "routing" / "campaigns"
        campaigns_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=campaigns_root) as temporary:
            artifact_root = Path(temporary)
            relative = artifact_root.relative_to(COMPARE.ROOT).as_posix()
            campaign = types.SimpleNamespace(
                campaign_id="00000000-0000-4000-8000-000000000077",
                artifact_root=relative,
                trial_groups={
                    trial: f"00000000-0000-4000-8000-{trial:012d}"
                    for trial in range(1, 4)
                },
            )
            records = []
            sequence = 0
            for trial, group_id in campaign.trial_groups.items():
                for variant in ("candidate", "previous", "baseline"):
                    sequence += 1
                    run_id = f"00000000-0000-4001-8000-{sequence:012d}"
                    attempt_id = f"00000000-0000-4002-8000-{sequence:012d}"
                    run_dir = artifact_root / run_id
                    run_dir.mkdir()
                    bundle = run_dir / "results.json"
                    bundle.write_text(f"bundle-{sequence}", encoding="utf-8")
                    bundle_hash = hashlib.sha256(bundle.read_bytes()).hexdigest()
                    attempt = {
                        "campaign_id": campaign.campaign_id,
                        "trial": trial,
                        "variant": variant,
                        "comparison_group_id": group_id,
                        "status": "success",
                        "attempt_id": attempt_id,
                        "run_id": run_id,
                        "artifact": bundle.name,
                        "artifact_sha256": bundle_hash,
                    }
                    (run_dir / "attempt.json").write_text(
                        json.dumps(attempt), encoding="utf-8"
                    )
                    records.append(
                        types.SimpleNamespace(
                            trial=trial,
                            variant=variant,
                            comparison_group_id=group_id,
                            path=bundle,
                            attempt_path="attempt.json",
                            attempt_id=attempt_id,
                            run_id=run_id,
                            bundle_sha256=bundle_hash,
                        )
                    )

            summary = COMPARE._validate_campaign_attempt_ledger(campaign, records)
            self.assertEqual(9, summary["observed_successful_attempts"])

            first_attempt = artifact_root / records[0].run_id / "attempt.json"
            changed = json.loads(first_attempt.read_text(encoding="utf-8"))
            changed["status"] = "failure"
            first_attempt.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaisesRegex(COMPARE.ComparisonError, "non-success"):
                COMPARE._validate_campaign_attempt_ledger(campaign, records)


if __name__ == "__main__":
    unittest.main()
