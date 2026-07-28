#!/usr/bin/env python3
"""Regressions for the frontend visual evidence protocol and fixture."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-frontend-visual-evidence.py"
SPEC = importlib.util.spec_from_file_location("validate_frontend_visual_evidence", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

SCHEMA_PATH = ROOT / "protocols" / "frontend-visual-evidence-v1.schema.json"
FIXTURE_PATH = (
    ROOT / "skills" / "dev-frontend" / "assets" / "frontend-visual-evidence.example.json"
)


class FrontendVisualEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def errors(self, payload: dict[str, object]) -> list[str]:
        return VALIDATOR.schema_errors(payload, self.schema)

    def stage_payload(self, stage: str) -> dict[str, object]:
        payload = copy.deepcopy(self.fixture)
        payload["stage"] = stage
        if stage == "spec-ready":
            for key in (
                "implementation_mapping",
                "visual_reviews",
                "runtime_coverage",
                "final_verdict",
            ):
                payload.pop(key)
        elif stage == "mapped":
            for key in ("visual_reviews", "runtime_coverage", "final_verdict"):
                payload.pop(key)
        elif stage == "pass-1":
            payload["visual_reviews"] = payload["visual_reviews"][:1]
            for key in ("runtime_coverage", "final_verdict"):
                payload.pop(key)
        return payload

    def complete_payload(self) -> dict[str, object]:
        payload = copy.deepcopy(self.fixture)
        payload["final_verdict"]["status"] = "Complete"
        payload["final_verdict"]["remaining_gaps"] = []
        payload["final_verdict"]["not_verified"] = []
        evidence_by_category = {
            "real_assets": "FIXTURE-PASS-2-ASSETS",
            "font_fallback": "FIXTURE-PASS-2-FONT",
            "contrast": "FIXTURE-PASS-2-CONTRAST",
            "section_alignment": "FIXTURE-PASS-2-ALIGNMENT",
            "card_dimensions": "FIXTURE-PASS-2-GEOMETRY",
        }
        template = next(
            item
            for item in payload["evidence"]
            if item["id"] == "FIXTURE-PASS-2-GEOMETRY"
        )
        for category in payload["runtime_coverage"]:
            if category not in evidence_by_category:
                evidence_id = f"FIXTURE-PASS-2-{category.upper()}"
                item = copy.deepcopy(template)
                item["id"] = evidence_id
                item["claim"] = f"Synthetic complete-case evidence for {category}"
                item["categories"] = [category]
                payload["evidence"].append(item)
                payload["visual_reviews"][-1]["computed_checks"].append(
                    {"category": category, "evidence_ids": [evidence_id]}
                )
                evidence_by_category[category] = evidence_id
        for category, record in payload["runtime_coverage"].items():
            record["status"] = "verified"
            record["evidence_ids"] = [evidence_by_category[category]]
        return payload

    def test_example_fixture_is_valid(self) -> None:
        self.assertEqual([], self.errors(self.fixture))
        self.assertEqual([], VALIDATOR.semantic_errors(self.fixture))
        VALIDATOR.validate_artifact(FIXTURE_PATH, SCHEMA_PATH)

    def test_all_four_stages_are_valid_without_future_fields(self) -> None:
        for stage in ("spec-ready", "mapped", "pass-1", "final"):
            with self.subTest(stage=stage):
                payload = self.stage_payload(stage)
                self.assertEqual([], self.errors(payload))
                self.assertEqual([], VALIDATOR.semantic_errors(payload))

    def test_ready_requires_approved_selected_source(self) -> None:
        for approval_status in ("pending", "rejected", "Not verified"):
            with self.subTest(approval_status=approval_status):
                payload = self.stage_payload("spec-ready")
                payload["selected_source"]["approval"]["status"] = approval_status
                self.assertTrue(self.errors(payload))
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_ready_rejects_blockers(self) -> None:
        payload = self.stage_payload("spec-ready")
        payload["readiness"]["blockers"] = ["asset ownership unresolved"]
        self.assertTrue(self.errors(payload))
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_non_ready_requires_a_blocker(self) -> None:
        for readiness_status in ("Partial", "Not Ready"):
            with self.subTest(readiness_status=readiness_status):
                payload = self.stage_payload("spec-ready")
                payload["readiness"]["status"] = readiness_status
                self.assertTrue(self.errors(payload))
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_implementation_stages_require_ready(self) -> None:
        for stage in ("mapped", "pass-1", "final"):
            for readiness_status in ("Partial", "Not Ready"):
                with self.subTest(stage=stage, readiness_status=readiness_status):
                    payload = self.stage_payload(stage)
                    payload["readiness"] = {
                        "status": readiness_status,
                        "blockers": ["selected source is not implementation-ready"],
                    }
                    self.assertTrue(self.errors(payload))
                    self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_spec_ready_rejects_future_stage_evidence(self) -> None:
        payload = self.stage_payload("spec-ready")
        payload["visual_reviews"] = copy.deepcopy(self.fixture["visual_reviews"])
        self.assertTrue(self.errors(payload))

    def test_two_visual_passes_are_required(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"] = payload["visual_reviews"][:1]
        self.assertTrue(self.errors(payload))

    def test_pass_order_is_fixed(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"][1]["pass"] = 3
        self.assertTrue(self.errors(payload))

    def test_source_and_runtime_columns_are_both_required(self) -> None:
        payload = copy.deepcopy(self.fixture)
        del payload["delta_table"][0]["current_runtime"]
        self.assertTrue(self.errors(payload))

    def test_runtime_value_cannot_use_an_unknown_evidence_label(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["delta_table"][0]["current_runtime"]["evidence_level"] = "already-aligned"
        self.assertTrue(self.errors(payload))

    def test_all_runtime_coverage_categories_are_required(self) -> None:
        payload = copy.deepcopy(self.fixture)
        del payload["runtime_coverage"]["font_fallback"]
        self.assertTrue(self.errors(payload))

    def test_visual_passes_must_use_same_viewport_and_state(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"][0]["same_viewport"] = False
        self.assertTrue(self.errors(payload))

    def test_semantics_require_mapping_for_every_delta(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["implementation_mapping"] = payload["implementation_mapping"][:-1]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_semantics_reject_unknown_evidence_references(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["delta_table"][0]["selected_source"]["evidence_ids"] = ["MISSING"]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_delta_declared_level_must_match_referenced_evidence(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["delta_table"][0]["selected_source"]["evidence_ids"] = [
            "RUNTIME-DESKTOP-GEOMETRY"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_source_and_target_columns_reject_runtime_evidence(self) -> None:
        for column in ("selected_source", "target_contract"):
            with self.subTest(column=column):
                payload = copy.deepcopy(self.fixture)
                payload["delta_table"][0][column]["evidence_level"] = "browser-computed"
                payload["delta_table"][0][column]["evidence_ids"] = [
                    "RUNTIME-DESKTOP-GEOMETRY"
                ]
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_semantics_compare_capture_viewports(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"][0]["runtime_capture"]["viewport"]["height"] = 1080
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_verdict_rejects_not_verified_coverage(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["final_verdict"]["status"] = "Complete"
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_verdict_accepts_closed_evidence(self) -> None:
        self.assertEqual([], VALIDATOR.semantic_errors(self.complete_payload()))

    def test_complete_rejects_pending_source(self) -> None:
        payload = self.complete_payload()
        payload["selected_source"]["approval"]["status"] = "pending"
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_verified_coverage_requires_evidence(self) -> None:
        payload = self.complete_payload()
        payload["runtime_coverage"]["real_assets"]["evidence_ids"] = []
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_failed_final_pass(self) -> None:
        payload = self.complete_payload()
        payload["visual_reviews"][-1]["verdict"] = "fail"
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_not_verified_list(self) -> None:
        payload = self.complete_payload()
        payload["final_verdict"]["not_verified"] = ["responsive"]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_proposed_evidence_cannot_verify_runtime_coverage(self) -> None:
        payload = self.complete_payload()
        payload["runtime_coverage"]["real_assets"]["evidence_ids"] = [
            "TARGET-TYPOGRAPHY"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_runtime_coverage_requires_matching_evidence_category(self) -> None:
        payload = self.complete_payload()
        payload["runtime_coverage"]["real_assets"]["evidence_ids"] = [
            "FIXTURE-PASS-2-GEOMETRY"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_computed_check_requires_matching_evidence_category(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"][-1]["computed_checks"][0]["category"] = (
            "responsive_breakpoints"
        )
        self.assertTrue(VALIDATOR.semantic_errors(payload))


if __name__ == "__main__":
    unittest.main()
