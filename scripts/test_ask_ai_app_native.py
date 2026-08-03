#!/usr/bin/env python3
"""Offline contract regressions for ask-ai App-native routing."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ask-ai" / "scripts" / "app_native_canary.py"
SPEC = importlib.util.spec_from_file_location("app_native_canary", SCRIPT)
assert SPEC and SPEC.loader
CANARY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CANARY)


def snapshot(surface: str = "quick-chat") -> dict[str, object]:
    return {
        "schema_version": CANARY.SCHEMA_VERSION,
        "requested_surface": surface,
        "explicit_quick_chat": surface == "quick-chat",
        "project_id": "g-p-review" if surface == "project" else None,
        "tool_schema": {
            "operations": sorted(CANARY.REQUIRED_OPERATIONS),
            "create_thread_targets": [
                "project",
                "projectless",
                "chatgptWorkCloud",
            ],
        },
        "list_projects": {
            "projects": [
                {
                    "projectId": "g-p-review",
                    "projectKind": "chatgpt",
                    "isGitRepository": False,
                }
            ]
        },
        "list_threads": {
            "threads": [{"id": "chat-1", "kind": "chatgpt"}],
            "unavailableSources": [],
        },
    }


def reconciliation_expected(prompt: str = "line one\r\nline two") -> dict[str, object]:
    return {
        "prompt": CANARY.prompt_fingerprint(prompt),
        "started_at": "2026-07-28T08:00:00Z",
        "ended_at": "2026-07-28T08:01:00Z",
        "requested_surface": "project",
        "project_id": "g-p-review",
        "list_page_bound": 2,
        "candidate_bound": 4,
        "candidate_read_bound": 4,
        "list_bound_exhausted": False,
    }


def candidate(
    thread_id: str,
    prompt: str = "line one\nline two",
    *,
    truncated: bool = False,
) -> dict[str, object]:
    return {
        "thread_id": thread_id,
        "kind": "chatgpt",
        "projectId": "g-p-review",
        "initial_user_message_at": "2026-07-28T08:00:30Z",
        "initial_user_prompt": prompt,
        "truncated": truncated,
    }


class AppNativeCanaryTests(unittest.TestCase):
    def test_core_routes_chatgpt_native_rules_to_provider_reference(self) -> None:
        skill = (ROOT / "skills" / "ask-ai" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        routing = (
            ROOT
            / "skills"
            / "ask-ai"
            / "references"
            / "provider-chatgpt.md"
        ).read_text(encoding="utf-8")
        self.assertIn("provider-chatgpt.md", skill)
        self.assertIn("ChatGPT-only", skill)
        self.assertIn("an empty available source is", routing)
        self.assertIn("legal for a new Quick Chat", routing)

    def test_quick_chat_requires_explicit_request_and_omits_project_id(self) -> None:
        result = CANARY.classify(snapshot())
        self.assertEqual("ready", result["status"])
        self.assertEqual({"type": "chatgptWorkCloud"}, result["native_target"])

        implicit = snapshot()
        implicit["explicit_quick_chat"] = False
        result = CANARY.classify(implicit)
        self.assertEqual("blocked", result["status"])
        self.assertFalse(result["state_change_allowed"])

    def test_verified_chatgpt_project_maps_to_cloud_target(self) -> None:
        result = CANARY.classify(snapshot("project"))
        self.assertEqual("ready", result["status"])
        self.assertEqual(
            {"type": "chatgptWorkCloud", "projectId": "g-p-review"},
            result["native_target"],
        )

    def test_generic_standard_chat_never_maps_to_chatgpt_work_cloud(self) -> None:
        result = CANARY.classify(snapshot("standard-chat"))
        self.assertEqual("browser-fallback-required", result["status"])
        self.assertIsNone(result["native_target"])
        self.assertFalse(result["state_change_allowed"])

    def test_standard_chat_fallback_does_not_require_native_activation(self) -> None:
        value = snapshot("standard-chat")
        value["list_projects"] = {"projects": []}
        value["list_threads"] = {
            "threads": [],
            "unavailableSources": ["chatgpt"],
        }
        result = CANARY.classify(value)
        self.assertEqual("browser-fallback-required", result["status"])

    def test_unavailable_chatgpt_source_requires_one_time_activation(self) -> None:
        value = snapshot()
        value["list_projects"] = {"projects": []}
        value["list_threads"] = {
            "threads": [],
            "unavailableSources": ["chatgpt"],
        }
        result = CANARY.classify(value)
        self.assertEqual("activation-required", result["status"])
        self.assertFalse(result["state_change_allowed"])

    def test_empty_available_source_still_allows_explicit_quick_chat(self) -> None:
        value = snapshot()
        value["list_projects"] = {"projects": []}
        value["list_threads"] = {"threads": [], "unavailableSources": []}
        result = CANARY.classify(value)
        self.assertEqual("ready", result["status"])

    def test_missing_source_status_fails_closed(self) -> None:
        value = snapshot()
        value["list_threads"] = {"threads": []}
        result = CANARY.classify(value)
        self.assertEqual("blocked", result["status"])

    def test_codex_targets_do_not_satisfy_chatgpt_capability(self) -> None:
        value = snapshot()
        value["tool_schema"]["create_thread_targets"] = ["project", "projectless"]
        result = CANARY.classify(value)
        self.assertEqual("blocked", result["status"])
        self.assertEqual(
            "chatgpt-work-cloud-target-not-exposed",
            result["reason"],
        )

    def test_inconsistent_source_evidence_blocks_state_change(self) -> None:
        value = snapshot()
        value["list_threads"]["unavailableSources"] = ["chatgpt"]
        result = CANARY.classify(value)
        self.assertEqual("blocked", result["status"])
        self.assertFalse(result["state_change_allowed"])

    def test_attestation_html_is_submission_uncertain_and_never_retryable(self) -> None:
        result = CANARY.classify_create_result(
            "<html>/backend-api/ios/attestation_challenge</html>"
        )
        self.assertEqual(
            {
                "create-conversation": "submission-uncertain",
                "submit-initial": "submission-uncertain",
            },
            result["logical_write_states"],
        )
        self.assertFalse(result["state_change_allowed"])

    def test_atomic_create_result_projects_both_correlated_logical_writes(self) -> None:
        result = CANARY.classify_create_result({"clientThreadId": "client-1"})
        self.assertEqual(
            {
                "create-conversation": "submitted",
                "submit-initial": "submitted",
            },
            result["logical_write_states"],
        )
        self.assertEqual("client-pending", result["identity_state"])

    def test_v1_uncertain_ledger_resumes_read_only_with_same_operation(self) -> None:
        result = CANARY.recovery_directive(
            {
                "schema_version": "app-native-thread-operation/v1",
                "operation_id": "round-1-create",
                "state": "submission-uncertain",
                "call": {"count": 1},
            }
        )
        self.assertEqual("round-1-create", result["operation_id"])
        self.assertEqual(
            "app-native-thread-operation/v1",
            result["preserve_schema_version"],
        )
        self.assertFalse(result["state_change_allowed"])
        self.assertFalse(result["replacement_operation_allowed"])

    def test_v2_uncertain_ledger_preserves_its_own_schema(self) -> None:
        result = CANARY.recovery_directive(
            {
                "schema_version": "app-native-thread-operation/v2",
                "operation_id": "round-1-submit",
                "state": "invoking",
                "call": {"count": 1},
            }
        )
        self.assertEqual("app-native-thread-operation/v2", result["preserve_schema_version"])

    def test_legacy_v2_recovery_rejects_v3_host_call_shape(self) -> None:
        with self.assertRaises(CANARY.SnapshotError):
            CANARY.recovery_directive(
                {
                    "schema_version": "app-native-thread-operation/v2",
                    "operation_id": "round-1-submit",
                    "state": "invoking",
                    "host_call": {"count": 1},
                }
            )

    def test_unique_candidate_uses_versioned_prompt_hash_and_call_window(self) -> None:
        result = CANARY.reconcile_create_candidates(
            reconciliation_expected(),
            [candidate("chat-1")],
        )
        self.assertEqual("unique-match", result["status"])
        self.assertEqual("chat-1", result["thread_id"])
        self.assertFalse(result["state_change_allowed"])

    def test_zero_and_multiple_candidate_matches_remain_unresolved(self) -> None:
        no_match = CANARY.reconcile_create_candidates(
            reconciliation_expected(),
            [candidate("chat-1", "different")],
        )
        self.assertEqual("no-match", no_match["status"])
        self.assertIsNone(no_match["thread_id"])

        multiple = CANARY.reconcile_create_candidates(
            reconciliation_expected(),
            [candidate("chat-1"), candidate("chat-2")],
        )
        self.assertEqual("multiple-matches", multiple["status"])
        self.assertIsNone(multiple["thread_id"])
        self.assertFalse(multiple["state_change_allowed"])

    def test_truncated_candidate_never_matches(self) -> None:
        result = CANARY.reconcile_create_candidates(
            reconciliation_expected(),
            [candidate("chat-1", truncated=True)],
        )
        self.assertEqual("Not verified", result["status"])
        self.assertTrue(result["truncation_seen"])
        self.assertFalse(result["state_change_allowed"])

    def test_missing_or_non_boolean_completeness_never_matches(self) -> None:
        for invalid in (None, "false"):
            value = candidate("chat-1")
            if invalid is None:
                value.pop("truncated")
            else:
                value["truncated"] = invalid
            result = CANARY.reconcile_create_candidates(
                reconciliation_expected(),
                [value],
            )
            self.assertEqual("Not verified", result["status"])
            self.assertIsNone(result["thread_id"])
            self.assertTrue(result["completeness_unknown"])

    def test_quick_chat_reconciliation_excludes_project_threads(self) -> None:
        expected = reconciliation_expected()
        expected["requested_surface"] = "quick-chat"
        expected["project_id"] = None
        project_thread = candidate("project-chat")
        project_thread["projectId"] = "g-p-other"
        result = CANARY.reconcile_create_candidates(expected, [project_thread])
        self.assertEqual("no-match", result["status"])
        self.assertIsNone(result["thread_id"])

        quick_chat = candidate("quick-chat")
        quick_chat["projectId"] = None
        result = CANARY.reconcile_create_candidates(expected, [quick_chat])
        self.assertEqual("unique-match", result["status"])
        self.assertEqual("quick-chat", result["thread_id"])

    def test_exhausted_candidate_bound_never_claims_unique_match(self) -> None:
        expected = reconciliation_expected()
        expected["candidate_bound"] = 1
        expected["candidate_read_bound"] = 1
        result = CANARY.reconcile_create_candidates(
            expected,
            [candidate("chat-1"), candidate("chat-2")],
        )
        self.assertEqual("Not verified", result["status"])
        self.assertIsNone(result["thread_id"])
        self.assertTrue(result["candidate_bound_exhausted"])


if __name__ == "__main__":
    unittest.main()
