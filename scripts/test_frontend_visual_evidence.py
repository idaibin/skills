#!/usr/bin/env python3
"""Regressions for the frontend visual evidence protocol and fixture."""

from __future__ import annotations

import copy
import base64
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-frontend-visual-evidence.py"
SPEC = importlib.util.spec_from_file_location("validate_frontend_visual_evidence", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
SYNC_SCRIPT = ROOT / "scripts" / "sync-shared-protocols.py"
SYNC_SPEC = importlib.util.spec_from_file_location("sync_shared_protocols", SYNC_SCRIPT)
assert SYNC_SPEC and SYNC_SPEC.loader
SYNC = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC)

SCHEMA_PATH = ROOT / "protocols" / "frontend-visual-evidence-v1.schema.json"
FIXTURE_PATH = (
    ROOT / "skills" / "dev-frontend" / "assets" / "frontend-visual-evidence.example.json"
)

def scalar_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for entry in value for item in scalar_strings(entry)]
    if isinstance(value, dict):
        return [item for entry in value.values() for item in scalar_strings(entry)]
    return []


def portable_fixture_errors(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if payload.get("task_id") != "synthetic-visual-evidence-example":
        errors.append("task ID must use the fixed synthetic identity")
    selected_source = payload["selected_source"]
    if selected_source.get("identity") != "Synthetic selected visual reference":
        errors.append("selected source must use the fixed synthetic identity")
    if selected_source.get("revision") != "synthetic-source-001":
        errors.append("selected source must use the fixed synthetic revision")
    acceptance_ids = [item.get("acceptance_id") for item in payload["delta_table"]]
    if any(not isinstance(item, str) or not re.fullmatch(r"ACCEPTANCE-\d{3}", item) for item in acceptance_ids):
        errors.append("acceptance IDs must use the synthetic ACCEPTANCE-### form")
    for mapping in payload["implementation_mapping"]:
        owner_file = mapping.get("owner_file")
        if not isinstance(owner_file, str) or not re.fullmatch(
            r"components/neutral-[a-z0-9-]+\.component", owner_file
        ):
            errors.append("implementation mappings must use a neutral component namespace")
    artifact_locators = [
        review[capture]["artifact"]
        for review in payload["visual_reviews"]
        for capture in ("design_capture", "runtime_capture")
    ] + [review["comparison"]["artifact"] for review in payload["visual_reviews"]]
    if any(
        not isinstance(locator, str) or not locator.startswith("artifact://synthetic/")
        for locator in artifact_locators
    ):
        errors.append("artifacts must use the synthetic artifact locator namespace")
    for value in scalar_strings(payload):
        if value.startswith("/") or ".." in value.split("/"):
            errors.append(f"committed fixture contains a non-portable path: {value}")
        if "://" in value and not value.startswith("artifact://synthetic/"):
            errors.append(f"committed fixture contains a non-synthetic locator: {value}")
    return errors


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
            "card_dimensions": "RUNTIME-PASS-2-GEOMETRY",
        }
        template = next(
            item
            for item in payload["evidence"]
            if item["id"] == "RUNTIME-PASS-2-GEOMETRY"
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
        target_viewport = payload["visual_reviews"][-1]["runtime_capture"]["viewport"]
        target_state = payload["visual_reviews"][-1]["runtime_capture"]["state"]
        target_fingerprint = VALIDATOR._canonical_sha256({"viewport": target_viewport, "state": target_state})
        captures = []
        artifact_contents = []
        runtime_by_pass = {}
        for review in payload["visual_reviews"]:
            for role, capture_name in (("design", "design_capture"), ("runtime", "runtime_capture")):
                capture = review[capture_name]
                capture_id = f"synthetic-pass-{review['pass']}-{role}"
                capture["artifact"] = f"artifact://task/{payload['task_id']}/pass-{review['pass']}-{role}"
                artifact_bytes = f"synthetic {capture_id} bytes".encode("utf-8")
                artifact_sha256 = VALIDATOR._bytes_sha256(artifact_bytes)
                manifest = {
                    "capture_id": capture_id,
                    "pass": review["pass"],
                    "role": role,
                    "artifact": capture["artifact"],
                    "artifact_sha256": artifact_sha256,
                    "artifact_bytes": len(artifact_bytes),
                    "viewport": capture["viewport"],
                    "state": capture["state"],
                    "target_fingerprint": target_fingerprint,
                }
                summary = {"capture_id": capture_id, "artifact": capture["artifact"], "artifact_sha256": artifact_sha256, "artifact_bytes": len(artifact_bytes), "summary": f"Synthetic {role} capture summary"}
                capture.update({
                    "capture_id": capture_id,
                    "artifact_sha256": artifact_sha256,
                    "artifact_bytes": len(artifact_bytes),
                    "capture_manifest_sha256": VALIDATOR._canonical_sha256(manifest),
                    "content_summary_sha256": VALIDATOR._canonical_sha256(summary),
                    "target_fingerprint": target_fingerprint,
                })
                record = {"capture_id": capture_id, "pass": review["pass"], "role": role, "artifact": capture["artifact"], "artifact_sha256": artifact_sha256, "artifact_bytes": len(artifact_bytes), "capture_manifest": manifest, "capture_manifest_sha256": VALIDATOR._canonical_sha256(manifest), "content_summary": summary, "content_summary_sha256": VALIDATOR._canonical_sha256(summary), "viewport": capture["viewport"], "state": capture["state"], "target_fingerprint": target_fingerprint}
                captures.append(record)
                artifact_contents.append({"artifact": capture["artifact"], "bytes_base64": base64.b64encode(artifact_bytes).decode("ascii")})
                if role == "runtime":
                    runtime_by_pass[review["pass"]] = record
        for item in payload["evidence"]:
            if item["level"] == "browser-computed":
                runtime = runtime_by_pass[item["review_pass"]]
                item.update({key: runtime[key] for key in ("capture_id", "artifact_sha256", "artifact_bytes", "capture_manifest_sha256", "content_summary_sha256", "target_fingerprint")})
                if "responsive_breakpoints" in item.get("categories", []):
                    item["matrix_target_id"] = payload["required_runtime_matrix"][0]["id"]
                    item["source"] = runtime["artifact"]
        final_runtime = runtime_by_pass[payload["visual_reviews"][-1]["pass"]]
        before_browser_state = {"tab_id": "synthetic-user-tab", "url": "https://synthetic.invalid/original", "viewport": {"width": 1280, "height": 720, "zoom": 1}, "scroll": {"x": 0, "y": 96}}
        final_receipt = {"receipt_id": "synthetic-final-restoration", "status": "final", "operation_id": "synthetic-restoration-operation", "before_state": before_browser_state, "authorized_restoration_actions": [{"action_id": "synthetic-restoration-action", "action": "restore synthetic target", "authorized": True}], "post_readback": {"operation_id": "synthetic-restoration-operation", "browser_state": copy.deepcopy(before_browser_state)}, "final_pass": payload["visual_reviews"][-1]["pass"], "target_fingerprint": target_fingerprint, "artifact_sha256": final_runtime["artifact_sha256"], "artifact_bytes": final_runtime["artifact_bytes"], "capture_manifest_sha256": final_runtime["capture_manifest_sha256"], "content_summary_sha256": final_runtime["content_summary_sha256"]}
        final_receipt["receipt_canonical_sha256"] = VALIDATOR._canonical_sha256(final_receipt)
        payload["capture_closure"] = {
            "target": {"viewport": final_runtime["viewport"], "state": final_runtime["state"], "target_fingerprint": target_fingerprint},
            "artifact_contents": artifact_contents,
            "captures": captures,
            "restoration_receipts": [final_receipt],
            "canonical_final_receipt_id": "synthetic-final-restoration",
        }
        return payload

    def test_example_fixture_is_valid(self) -> None:
        self.assertEqual([], self.errors(self.fixture))
        self.assertEqual([], VALIDATOR.semantic_errors(self.fixture))
        VALIDATOR.validate_artifact(FIXTURE_PATH, SCHEMA_PATH)

    def test_committed_fixture_is_portable(self) -> None:
        self.assertEqual([], portable_fixture_errors(self.fixture))

    def test_portability_hygiene_rejects_nonportable_structure(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["delta_table"][0]["acceptance_id"] = "ACCEPTANCE-ONE"
        payload["implementation_mapping"][0]["owner_file"] = "../neutral.component"
        payload["evidence"][0]["source"] = "https://example.invalid/synthetic"
        payload["visual_reviews"][0]["design_capture"]["artifact"] = "artifact://other/source"
        errors = portable_fixture_errors(payload)
        self.assertGreaterEqual(len(errors), 4)

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
            "RUNTIME-PASS-1"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_source_and_target_columns_reject_runtime_evidence(self) -> None:
        for column in ("selected_source", "target_contract"):
            with self.subTest(column=column):
                payload = copy.deepcopy(self.fixture)
                payload["delta_table"][0][column]["evidence_level"] = "browser-computed"
                payload["delta_table"][0][column]["evidence_ids"] = [
                    "RUNTIME-PASS-1"
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

    def test_complete_rejects_capture_manifest_or_summary_drift(self) -> None:
        payload = self.complete_payload()
        payload["visual_reviews"][-1]["runtime_capture"]["content_summary_sha256"] = "sha256:" + "f" * 64
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_schema_rejects_non_sha256_closure_values(self) -> None:
        payload = self.complete_payload()
        payload["capture_closure"]["captures"][0]["capture_manifest_sha256"] = "not-a-digest"
        self.assertTrue(self.errors(payload))

    def test_complete_rejects_manifest_bytes_or_summary_replacement(self) -> None:
        for field, value in (
            ("capture_manifest", {"capture_id": "replaced"}),
            ("content_summary", {"capture_id": "replaced", "artifact": "artifact://task/synthetic-visual-evidence-example/replaced", "summary": "replaced"}),
        ):
            with self.subTest(field=field):
                payload = self.complete_payload()
                payload["capture_closure"]["captures"][0][field] = value
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_replaced_artifact_bytes(self) -> None:
        payload = self.complete_payload()
        payload["capture_closure"]["artifact_contents"][0]["bytes_base64"] = base64.b64encode(b"replaced").decode("ascii")
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_local_capture_hash_refresh_without_downstream_regeneration(self) -> None:
        payload = self.complete_payload()
        replacement = b"synthetic replacement capture bytes"
        record = payload["capture_closure"]["captures"][0]
        payload["capture_closure"]["artifact_contents"][0]["bytes_base64"] = base64.b64encode(replacement).decode("ascii")
        record["artifact_sha256"] = VALIDATOR._bytes_sha256(replacement)
        record["artifact_bytes"] = len(replacement)
        capture = payload["visual_reviews"][0]["design_capture"]
        capture["artifact_sha256"] = record["artifact_sha256"]
        capture["artifact_bytes"] = record["artifact_bytes"]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_restoration_receipt_operation_or_hash_drift(self) -> None:
        for mutate in (
            lambda receipt: receipt.update({"operation_id": "replaced-operation"}),
            lambda receipt: receipt.update({"receipt_canonical_sha256": "sha256:" + "0" * 64}),
        ):
            payload = self.complete_payload()
            mutate(payload["capture_closure"]["restoration_receipts"][0])
            self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_restoration_to_capture_target_instead_of_before_state(self) -> None:
        payload = self.complete_payload()
        receipt = payload["capture_closure"]["restoration_receipts"][0]
        target = payload["capture_closure"]["target"]
        receipt["post_readback"]["browser_state"]["viewport"] = target["viewport"]
        receipt["post_readback"]["browser_state"]["url"] = "https://synthetic.invalid/capture-target"
        receipt["receipt_canonical_sha256"] = VALIDATOR._canonical_sha256(
            {key: value for key, value in receipt.items() if key != "receipt_canonical_sha256"}
        )
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_accepts_restoration_to_distinct_before_browser_state(self) -> None:
        payload = self.complete_payload()
        receipt = payload["capture_closure"]["restoration_receipts"][0]
        self.assertNotEqual(receipt["before_state"]["viewport"], payload["capture_closure"]["target"]["viewport"])
        self.assertEqual([], self.errors(payload))
        self.assertEqual([], VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_target_viewport_state_or_fingerprint_mismatch(self) -> None:
        for field, mismatch in (
            ("viewport", {"width": 1440, "height": 900, "zoom": 1}),
            ("state", "synthetic mismatched state"),
            ("target_fingerprint", "sha256:" + "f" * 64),
        ):
            with self.subTest(field=field):
                payload = self.complete_payload()
                payload["capture_closure"]["target"][field] = mismatch
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_browser_evidence_with_wrong_closure_viewport_or_state(self) -> None:
        for field, mismatch in (
            ("viewport", {"width": 1440, "height": 900, "zoom": 1}),
            ("state", "synthetic wrong runtime state"),
        ):
            with self.subTest(field=field):
                payload = self.complete_payload()
                payload["evidence"][-1][field] = mismatch
                self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_complete_rejects_conflicting_final_restoration_receipts(self) -> None:
        payload = self.complete_payload()
        payload["capture_closure"]["restoration_receipts"].append({
            **payload["capture_closure"]["restoration_receipts"][0],
            "receipt_id": "synthetic-conflicting-restoration",
        })
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_shared_protocol_sync_detects_cross_file_drift(self) -> None:
        original_protocols = SYNC.PROTOCOLS
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "protocols" / "source.md"
                target = root / "skills" / "neutral" / "reference.md"
                source.parent.mkdir(parents=True)
                target.parent.mkdir(parents=True)
                source.write_text("authoritative\n", encoding="utf-8")
                target.write_text("stale\n", encoding="utf-8")
                SYNC.PROTOCOLS = {Path("protocols/source.md"): (Path("skills/neutral/reference.md"),)}
                self.assertEqual(["skills/neutral/reference.md"], SYNC.synchronize(root, check=True))
        finally:
            SYNC.PROTOCOLS = original_protocols

    def test_proposed_evidence_cannot_verify_runtime_coverage(self) -> None:
        payload = self.complete_payload()
        payload["runtime_coverage"]["real_assets"]["evidence_ids"] = [
            "TARGET-TYPOGRAPHY"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_runtime_coverage_requires_matching_evidence_category(self) -> None:
        payload = self.complete_payload()
        payload["runtime_coverage"]["real_assets"]["evidence_ids"] = [
            "RUNTIME-PASS-2-GEOMETRY"
        ]
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_computed_check_requires_matching_evidence_category(self) -> None:
        payload = copy.deepcopy(self.fixture)
        payload["visual_reviews"][-1]["computed_checks"][0]["category"] = (
            "responsive_breakpoints"
        )
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def add_mobile_runtime_target(self, payload: dict[str, object]) -> None:
        viewport = {"width": 390, "height": 844, "zoom": 1}
        state = "synthetic mobile populated state at scroll origin"
        target_fingerprint = VALIDATOR._canonical_sha256(
            {"viewport": viewport, "state": state}
        )
        payload["required_runtime_matrix"].append(
            {
                "id": "synthetic-mobile-populated",
                "viewport": viewport,
                "state": state,
                "target_fingerprint": target_fingerprint,
            }
        )
        artifact = f"artifact://task/{payload['task_id']}/responsive-mobile"
        artifact_bytes = b"synthetic responsive mobile capture"
        evidence = copy.deepcopy(
            next(
                item
                for item in payload["evidence"]
                if "responsive_breakpoints" in item.get("categories", [])
            )
        )
        evidence.update(
            {
                "id": "FIXTURE-MOBILE-RESPONSIVE",
                "claim": "Synthetic mobile responsive evidence",
                "source": artifact,
                "matrix_target_id": "synthetic-mobile-populated",
                "viewport": viewport,
                "state": state,
                "target_fingerprint": target_fingerprint,
                "artifact_sha256": VALIDATOR._bytes_sha256(artifact_bytes),
                "artifact_bytes": len(artifact_bytes),
            }
        )
        payload["evidence"].append(evidence)
        payload["runtime_coverage"]["responsive_breakpoints"]["evidence_ids"].append(
            evidence["id"]
        )
        payload["capture_closure"]["artifact_contents"].append(
            {
                "artifact": artifact,
                "bytes_base64": base64.b64encode(artifact_bytes).decode("ascii"),
            }
        )

    def test_verified_responsive_coverage_requires_every_frozen_target(self) -> None:
        payload = self.complete_payload()
        self.add_mobile_runtime_target(payload)
        self.assertEqual([], VALIDATOR.semantic_errors(payload))

        missing_mobile = self.complete_payload()
        target = copy.deepcopy(payload["required_runtime_matrix"][-1])
        missing_mobile["required_runtime_matrix"].append(target)
        self.assertTrue(VALIDATOR.semantic_errors(missing_mobile))

    def test_runtime_matrix_rejects_duplicate_targets_and_fingerprint_drift(self) -> None:
        duplicate = self.complete_payload()
        duplicate_target = copy.deepcopy(duplicate["required_runtime_matrix"][0])
        duplicate_target["id"] = "duplicate-desktop"
        duplicate["required_runtime_matrix"].append(duplicate_target)
        self.assertTrue(VALIDATOR.semantic_errors(duplicate))

        stale = self.complete_payload()
        stale["required_runtime_matrix"][0]["target_fingerprint"] = "sha256:" + "f" * 64
        self.assertTrue(VALIDATOR.semantic_errors(stale))

    def test_responsive_matrix_evidence_rejects_viewport_or_artifact_mismatch(self) -> None:
        payload = self.complete_payload()
        self.add_mobile_runtime_target(payload)
        mobile = next(
            item for item in payload["evidence"] if item["id"] == "FIXTURE-MOBILE-RESPONSIVE"
        )
        mobile["viewport"] = {"width": 391, "height": 844, "zoom": 1}
        self.assertTrue(VALIDATOR.semantic_errors(payload))

        payload = self.complete_payload()
        self.add_mobile_runtime_target(payload)
        mobile = next(
            item for item in payload["evidence"] if item["id"] == "FIXTURE-MOBILE-RESPONSIVE"
        )
        mobile["artifact_sha256"] = "sha256:" + "0" * 64
        self.assertTrue(VALIDATOR.semantic_errors(payload))

    def test_responsive_matrix_rejects_uncited_duplicate_that_masks_bad_evidence(self) -> None:
        payload = self.complete_payload()
        self.add_mobile_runtime_target(payload)
        cited = next(
            item for item in payload["evidence"] if item["id"] == "FIXTURE-MOBILE-RESPONSIVE"
        )
        valid_duplicate = copy.deepcopy(cited)
        valid_duplicate["id"] = "FIXTURE-MOBILE-RESPONSIVE-UNCITED"
        cited["artifact_sha256"] = "sha256:" + "0" * 64
        payload["evidence"].append(valid_duplicate)
        self.assertTrue(VALIDATOR.semantic_errors(payload))


if __name__ == "__main__":
    unittest.main()
