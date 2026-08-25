#!/usr/bin/env python3
"""Focused regressions for portable live-Agent evaluation contracts."""

from __future__ import annotations

import copy
import importlib.util
import json
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-live-agent-evals.py"
SPEC = importlib.util.spec_from_file_location("validate_live_agent_evals", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
CASES_PATH = ROOT / "evals/live-agent-cases.json"


class LiveAgentEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        cls.provider_root = Path(tempfile.mkdtemp(prefix="live-provider-validator-"))

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.provider_root)

    def provider_evidence(self, case_id: str) -> dict[str, str]:
        root = self.provider_root / case_id
        root.mkdir(exist_ok=True)
        artifact, events, receipt = (root / "artifact.json", root / "events.jsonl", root / "receipt.json")
        artifact.write_text('{"result":"synthetic"}', encoding="utf-8")
        digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        basis = {"case_id": case_id, "source_diff_sha256": "a" * 64}
        runtime = {"executable_fingerprint": "sha256:synthetic-agy-executable", "executable_version": "1.1.14", "profile": "agy-flash-review", "native_mode": "native-review", "model_evidence_locator": "init.model"}
        cwd = str(root.resolve())
        argv = [
            "agy", "--add-dir", cwd, "--model", "gemini-3.7-flash-high",
            "--mode", "accept-edits", "--dangerously-skip-permissions",
            "--output-format", "stream-json", "--print", "synthetic-task",
        ]
        operation_id = "synthetic-provider-operation"
        prompt_or_basis_digest = "sha256:synthetic-prompt-or-basis"
        events.write_text("\n".join(json.dumps(event) for event in (
            {"event": "init", "provider_identity": "google-antigravity", "conversation_id": "synthetic-provider-session", "init": {"model": "gemini-3.7-flash-high", "cwd": cwd, "tools": ["run_command"]}},
            {"event": "result", "provider_identity": "google-antigravity", "conversation_id": "synthetic-provider-session", "result": {"status": "SUCCESS", "operation_id": operation_id, "prompt_or_basis_digest": prompt_or_basis_digest, "basis": basis, "final_artifact": {"sha256": digest(artifact), "bytes": artifact.stat().st_size}}},
        )) + "\n", encoding="utf-8")
        receipt.write_text(json.dumps({"requested_alias": "Flash", "process_exit_code": 0, "operation_id": operation_id, "prompt_or_basis_digest": prompt_or_basis_digest, "invocation": {"process_cwd": cwd, "argv": argv}, "provider": {"terminal": "SUCCESS", "init_model": "gemini-3.7-flash-high", "effective_model": "gemini-3.7-flash-high", "conversation_id": "synthetic-provider-session", "cwd": cwd, "identity": "google-antigravity", **runtime}, "basis": basis, "artifacts": {"artifact_sha256": digest(artifact), "artifact_bytes": artifact.stat().st_size, "events_sha256": digest(events)}}), encoding="utf-8")
        return {"channel": "AGY", "artifact_path": str(artifact), "events_path": str(events), "execution_receipt_path": str(receipt), "execution_receipt_sha256": digest(receipt)}

    def passed_results(self) -> dict[str, object]:
        results = []
        for case in self.cases["cases"]:
            result = {
                "case_id": case["id"],
                "status": "passed",
                "selected_skill": case["expected_skill"],
                "observations": case["required_observations"],
                "process": case["required_process"],
                "source_owners": case["required_source_owners"],
                "artifacts": case["required_artifacts"],
                "effects": case["required_effects"],
                "stop": {"state": case["expected_stop"]},
                "efficiency": {"tool_calls": case["max_tool_calls"], "successful_tool_calls": case["max_tool_calls"]},
                "trace": {
                    "source_diff_sha256": "a" * 64,
                    "selected_repository_root": str(
                        (self.provider_root / case["id"]).resolve()
                    ),
                },
            }
            if "required_provider" in case:
                result["provider"] = {
                    "channel": "AGY",
                    "model": "Flash",
                    "status": "completed",
                    "attributed_result": True,
                    "case_id": case["id"],
                    "source_diff_sha256": "a" * 64,
                    **self.provider_evidence(case["id"]),
                }
            results.append(result)
        return {"schema_version": VALIDATOR.RESULT_SCHEMA_VERSION, "case_results": results}

    def test_fixed_cases_are_valid(self) -> None:
        self.assertEqual([], VALIDATOR.case_errors(self.cases))

    def test_critical_stop_has_no_source_owner_requirement(self) -> None:
        critical = next(case for case in self.cases["cases"] if case["id"] == "dev-frontend-critical-stop")
        self.assertEqual([], critical["required_source_owners"])
        self.assertEqual(["read-effective-instructions", "stop-before-edit"], critical["required_process"])

    def test_complete_trace_can_pass_all_observable_gates(self) -> None:
        self.assertEqual([], VALIDATOR.result_errors(self.cases, self.passed_results()))

    def test_missing_requested_provider_cannot_pass(self) -> None:
        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"] if item["case_id"] == "dev-frontend-independent-provider"
        )
        provider_case.pop("provider")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_provider_evidence_must_bind_case_and_source_diff(self) -> None:
        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"] if item["case_id"] == "dev-frontend-independent-provider"
        )
        provider_case["provider"].pop("execution_receipt_path")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_standalone_validator_rejects_trailing_provider_terminals(self) -> None:
        for terminal in ("error", "cancelled", "failed", "result"):
            results = self.passed_results()
            provider_case = next(item for item in results["case_results"] if item["case_id"] == "dev-frontend-independent-provider")
            provider = provider_case["provider"]
            events_path = Path(provider["events_path"])
            lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
            lines.append({"event": terminal, "result": lines[-1]["result"]} if terminal == "result" else {"event": terminal})
            events_path.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
            receipt_path = Path(provider["execution_receipt_path"])
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["artifacts"]["events_sha256"] = hashlib.sha256(events_path.read_bytes()).hexdigest()
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            provider["execution_receipt_sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            self.assertIn(
                "dev-frontend-independent-provider: requested independent provider is not verified",
                VALIDATOR.result_errors(self.cases, results),
                terminal,
            )
        provider_case["provider"]["execution_receipt_path"] = "synthetic-provider-receipt.json"
        provider_case["provider"]["execution_receipt_sha256"] = "invalid"
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_provider_evidence_requires_a_provider_identity_or_artifact_hash(self) -> None:
        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"] if item["case_id"] == "dev-frontend-independent-provider"
        )
        provider_case["provider"].pop("execution_receipt_sha256")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_provider_receipt_model_claims_must_match_the_public_contract(self) -> None:
        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"] if item["case_id"] == "dev-frontend-independent-provider"
        )
        receipt_path = Path(provider_case["provider"]["execution_receipt_path"])
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["requested_alias"] = "other-alias"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )
        receipt["requested_alias"] = "Flash"
        receipt["provider"]["effective_model"] = "other-model"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )
        provider_case.pop("provider")
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_standalone_validator_rejects_wrong_root_or_missing_directory_permission(self) -> None:
        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"]
            if item["case_id"] == "dev-frontend-independent-provider"
        )
        provider_case["trace"]["selected_repository_root"] = str(
            self.provider_root / "other-repository"
        )
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

        results = self.passed_results()
        provider_case = next(
            item for item in results["case_results"]
            if item["case_id"] == "dev-frontend-independent-provider"
        )
        receipt_path = Path(provider_case["provider"]["execution_receipt_path"])
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        argv = receipt["invocation"]["argv"]
        index = argv.index("--add-dir")
        del argv[index : index + 2]
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        provider_case["provider"]["execution_receipt_sha256"] = hashlib.sha256(
            receipt_path.read_bytes()
        ).hexdigest()
        self.assertIn(
            "dev-frontend-independent-provider: requested independent provider is not verified",
            VALIDATOR.result_errors(self.cases, results),
        )

    def test_nonpassing_result_stays_not_verified_without_trace_fabrication(self) -> None:
        results = self.passed_results()
        results["case_results"][0] = {
            "case_id": "dev-frontend-explicit-source-change",
            "status": "not-verified",
        }
        self.assertEqual([], VALIDATOR.result_errors(self.cases, results))

    def test_selected_case_result_can_be_validated_independently(self) -> None:
        results = self.passed_results()
        results["selected_case_ids"] = ["dev-frontend-valid-no-op"]
        results["case_results"] = [
            item for item in results["case_results"] if item["case_id"] == "dev-frontend-valid-no-op"
        ]
        self.assertEqual([], VALIDATOR.result_errors(self.cases, results))

    def test_nonportable_source_owner_is_rejected(self) -> None:
        cases = copy.deepcopy(self.cases)
        cases["cases"][0]["required_source_owners"] = ["../neutral.ts:renderNeutralPanel"]
        self.assertTrue(VALIDATOR.case_errors(cases))

    def test_missing_process_step_cannot_pass(self) -> None:
        results = self.passed_results()
        results["case_results"][0]["process"] = ["read-effective-instructions"]
        self.assertIn(
            "dev-frontend-explicit-source-change: missing required process step",
            VALIDATOR.result_errors(self.cases, results),
        )


if __name__ == "__main__":
    unittest.main()
