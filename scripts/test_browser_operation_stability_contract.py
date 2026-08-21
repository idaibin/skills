#!/usr/bin/env python3
"""Offline regressions for browser attachment and stable-response evidence."""

from __future__ import annotations

import re
import unittest
from math import isfinite
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def attachment_retryable(evidence: dict[str, object]) -> bool:
    """Evaluate the synthetic before-selection evidence required by the contract."""
    return all(
        evidence.get(field) is expected
        for field, expected in (
            ("before_file_selection", True),
            ("same_binding_reverified", True),
            ("file_selected_or_uploaded", False),
            ("composer_unchanged_or_empty", True),
            ("submit_postcondition", False),
            ("other_side_effect", False),
        )
    )


def stable_response_acceptable(evidence: dict[str, object]) -> bool:
    """Evaluate synthetic evidence; a lingering control is intentionally separate."""
    hashes = evidence.get("hashes")
    observation_window = evidence.get("observation_window")
    sampling_cadence = evidence.get("sampling_cadence")
    return (
        evidence.get("same_conversation_and_container") is True
        and isinstance(observation_window, (int, float))
        and not isinstance(observation_window, bool)
        and isfinite(observation_window)
        and observation_window > 0
        and isinstance(sampling_cadence, (int, float))
        and not isinstance(sampling_cadence, bool)
        and isfinite(sampling_cadence)
        and sampling_cadence > 0
        and evidence.get("samples_span_window") is True
        and isinstance(hashes, list)
        and len(hashes) >= 2
        and len(set(hashes)) == 1
        and evidence.get("nonempty_nontruncated") is True
        and evidence.get("material_mutation") is False
    )


def persisted_capture_acceptable(receipt: dict[str, object]) -> bool:
    content = receipt.get("content")
    artifact = receipt.get("artifact")
    return (
        isinstance(receipt.get("conversation_id"), str)
        and bool(receipt["conversation_id"])
        and isinstance(receipt.get("response_container_id"), str)
        and bool(receipt["response_container_id"])
        and isinstance(content, dict)
        and content.get("complete") is True
        and content.get("truncated") is False
        and isinstance(content.get("character_count"), int)
        and not isinstance(content.get("character_count"), bool)
        and content["character_count"] >= 0
        and isinstance(content.get("sha256"), str)
        and len(content["sha256"]) == 64
        and isinstance(artifact, dict)
        and isinstance(artifact.get("path"), str)
        and bool(artifact["path"])
        and isinstance(artifact.get("file_sha256"), str)
        and len(artifact["file_sha256"]) == 64
        and artifact.get("atomic_write") == "verified"
        and artifact.get("readback_verified") is True
    )


class BrowserOperationStabilityContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def normalized(self, relative: str) -> str:
        return re.sub(r"\s+", " ", self.read(relative))

    def test_attachment_failure_requires_complete_negative_evidence(self) -> None:
        complete = {
            "before_file_selection": True,
            "same_binding_reverified": True,
            "file_selected_or_uploaded": False,
            "composer_unchanged_or_empty": True,
            "submit_postcondition": False,
            "other_side_effect": False,
        }
        self.assertTrue(attachment_retryable(complete))
        for field in complete:
            incomplete = dict(complete)
            incomplete.pop(field)
            with self.subTest(missing=field):
                self.assertFalse(attachment_retryable(incomplete))

        self.assertFalse(
            attachment_retryable(dict(complete, file_selected_or_uploaded=None))
        )
        self.assertFalse(
            attachment_retryable(dict(complete, same_binding_reverified=False))
        )

    def test_stable_response_allows_a_separate_lingering_control_gap(self) -> None:
        stable = {
            "same_conversation_and_container": True,
            "observation_window": 2,
            "sampling_cadence": 1,
            "samples_span_window": True,
            "hashes": ["sha256:one", "sha256:one"],
            "nonempty_nontruncated": True,
            "material_mutation": False,
            "stop_control_visible": True,
        }
        self.assertTrue(stable_response_acceptable(stable))
        self.assertTrue(stable["stop_control_visible"])
        self.assertFalse(
            stable_response_acceptable({**stable, "hashes": ["sha256:one"]})
        )
        for invalid_window in (None, 0):
            with self.subTest(observation_window=invalid_window):
                self.assertFalse(
                    stable_response_acceptable(
                        {**stable, "observation_window": invalid_window}
                    )
                )
        self.assertFalse(
            stable_response_acceptable({**stable, "samples_span_window": False})
        )
        self.assertFalse(
            stable_response_acceptable(
                {**stable, "hashes": ["sha256:one", "sha256:two"]}
            )
        )
        self.assertFalse(
            stable_response_acceptable(
                {**stable, "same_conversation_and_container": False}
            )
        )

    def test_persisted_capture_requires_every_receipt_field(self) -> None:
        receipt = {
            "conversation_id": "conversation-1",
            "response_container_id": "response-1",
            "content": {
                "complete": True,
                "truncated": False,
                "character_count": 4,
                "sha256": "a" * 64,
            },
            "artifact": {
                "path": ".codex/reviews/review-response.final.md",
                "file_sha256": "b" * 64,
                "atomic_write": "verified",
                "readback_verified": True,
            },
        }
        self.assertTrue(persisted_capture_acceptable(receipt))
        for field in ("conversation_id", "response_container_id", "content", "artifact"):
            with self.subTest(missing=field):
                incomplete = dict(receipt)
                incomplete.pop(field)
                self.assertFalse(persisted_capture_acceptable(incomplete))
        self.assertFalse(
            persisted_capture_acceptable(
                {**receipt, "content": {**receipt["content"], "truncated": True}}
            )
        )
        self.assertFalse(
            persisted_capture_acceptable(
                {**receipt, "artifact": {**receipt["artifact"], "readback_verified": False}}
            )
        )

    def test_canonical_contract_and_generated_owners_keep_the_rules(self) -> None:
        canonical = self.normalized("protocols/browser-operation-v1.md")
        for token in (
            "before file selection",
            "no file was selected or uploaded",
            "same reverified browser/session, tab, target, and composer",
            "finite observation window and sampling cadence",
            "including one at the end of the window",
            "immediate consecutive snapshots do not qualify",
            "same sanitized content hash",
            "lingering control remains a separate `Not verified` terminal-UI gap",
            "Capture the accepted response once and stop",
            "fixed package, invocation, events, response-partial, and response-final paths",
            "atomic_write: verified",
            "completion-not-verified",
        ):
            with self.subTest(token=token):
                self.assertIn(token, canonical)

        source = self.read("protocols/browser-operation-v1.md")
        for relative in (
            "skills/ask-ai/references/browser-operation-protocol.md",
            "skills/ops-browser/references/browser-operation-protocol.md",
        ):
            self.assertEqual(source, self.read(relative))

    def test_provider_and_owner_evals_cover_both_confirmed_gaps(self) -> None:
        ask_eval = self.read("skills/ask-ai/references/eval-cases.md")
        ops_eval = self.read("skills/ops-browser/references/eval-cases.md")
        self.assertIn("Attachment chooser failure", ask_eval)
        self.assertIn("Stable ChatGPT response with lingering stop control", ask_eval)
        self.assertIn("Attachment phase evidence", ops_eval)
        self.assertIn("Stable response with lingering control", ops_eval)


if __name__ == "__main__":
    unittest.main()
