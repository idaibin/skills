#!/usr/bin/env python3
"""Regression tests for frozen routing evaluation campaigns."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


SCRIPT = Path(__file__).with_name("evaluation_protocol.py")
SPEC = importlib.util.spec_from_file_location("evaluation_protocol_test", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
PROTOCOL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PROTOCOL
SPEC.loader.exec_module(PROTOCOL)


class EvaluationProtocolTests(unittest.TestCase):
    @staticmethod
    def _retry_policy() -> dict[str, object]:
        return {
            "schema_version": 1,
            "maximum_attempts_per_case": 2,
            "backoff_seconds": [5],
            "retryable_errors": {
                "claude": [],
                "codex": [
                    {
                        "error_class": "model_capacity",
                        "exit_codes": [1],
                        "json_fields": ["message"],
                        "normalized_values": [
                            "selected model is at capacity. please try a different model."
                        ],
                    }
                ],
            },
        }

    def _retry_contract(
        self, policy: dict[str, object] | None = None
    ) -> dict[str, object]:
        return {
            "behavior_eval": {
                "evaluation_protocol": {
                    "canonical_routing": {
                        "transient_retry_policy": (
                            self._retry_policy() if policy is None else policy
                        )
                    }
                }
            }
        }

    def _git(self, root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    def _fixture(self, root: Path):
        self._git(root, "init", "--quiet")
        self._git(root, "config", "user.name", "AICraft Test")
        self._git(root, "config", "user.email", "test@example.invalid")
        (root / "README.md").write_text("previous\n", encoding="utf-8")
        self._git(root, "add", "README.md")
        self._git(root, "commit", "--quiet", "-m", "previous")
        previous = self._git(root, "rev-parse", "HEAD")

        files = [
            "contracts/skill-validation.json",
            "scripts/compare-skill-evals.py",
            "scripts/eval-skill-contracts.py",
            "scripts/evaluation_protocol.py",
            "scripts/run-skill-routing-eval.py",
            "scripts/validate-skills.py",
        ]
        contract = {
            "behavior_eval": {
                "campaign_schema_version": 2,
                "campaign_required_fields": [
                    "schema_version",
                    "campaign_id",
                    "artifact_root",
                    "candidate_skill_revision",
                    "evaluation_anchor_revision",
                    "previous_skill_revision",
                    "baseline_skill_revision",
                    "dataset",
                    "provenance",
                    "condition",
                    "trials",
                    "evaluation_protocol",
                ],
                "prompt_template_version": 2,
                "comparative": {"minimum_trials_per_variant": 3},
                "evaluation_protocol": {
                    "schema_version": 1,
                    "files": files,
                    "canonical_routing": {
                        "reviewer": "scripts/run-skill-routing-eval.py",
                        "reviewer_version": "6",
                        "environment_policy_version": 1,
                        "environment_source_allowlist": ["LANG", "PATH"],
                        "transient_retry_policy": self._retry_policy(),
                    },
                },
            }
        }
        for relative in files:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == "contracts/skill-validation.json":
                path.write_text(json.dumps(contract), encoding="utf-8")
            else:
                path.write_text(f"# frozen {relative}\n", encoding="utf-8")
        self._git(root, "add", "contracts", "scripts")
        self._git(root, "commit", "--quiet", "-m", "evaluation anchor")
        anchor = self._git(root, "rev-parse", "HEAD")

        dataset = root / "evals" / "synthetic-routing.jsonl"
        provenance = root / "evals" / "synthetic-provenance.json"
        dataset.parent.mkdir()
        dataset.write_text('{"id":"case-001","prompt":"synthetic"}\n', encoding="utf-8")
        provenance.write_text('{"schema_version":1}\n', encoding="utf-8")
        self._git(root, "add", "evals")
        self._git(root, "commit", "--quiet", "-m", "blind dataset")
        dataset_revision = self._git(root, "rev-parse", "HEAD")

        manifest = PROTOCOL.protocol_manifest_from_revision(root, anchor, contract)
        host = "codex"
        model = "gpt-5-test"
        campaign_id = str(uuid.uuid4())
        campaign = {
            "schema_version": 2,
            "campaign_id": campaign_id,
            "artifact_root": f"eval-results/routing/campaigns/{campaign_id}",
            "candidate_skill_revision": anchor,
            "evaluation_anchor_revision": anchor,
            "previous_skill_revision": previous,
            "baseline_skill_revision": anchor,
            "dataset": {
                "path": "evals/synthetic-routing.jsonl",
                "sha256": PROTOCOL.sha256_bytes(dataset.read_bytes()),
                "git_revision": dataset_revision,
            },
            "provenance": {
                "path": "evals/synthetic-provenance.json",
                "sha256": PROTOCOL.sha256_bytes(provenance.read_bytes()),
                "git_revision": dataset_revision,
            },
            "condition": {
                "host_name": host,
                "model": model,
                "timeout_seconds": 120,
                "concurrency": 1,
                "prompt_template_version": 2,
                "prompt_template_sha256": PROTOCOL.sha256_text(
                    PROTOCOL.canonical_prompt_template(contract)
                ),
                "adjudication": PROTOCOL.canonical_adjudication(contract),
                "host_config_sha256": PROTOCOL.canonical_hash(
                    PROTOCOL.canonical_host_policy(host, model, contract)
                ),
                "environment_policy_sha256": PROTOCOL.canonical_hash(
                    PROTOCOL.canonical_environment_policy(host, contract)
                ),
                "retry_policy_sha256": PROTOCOL.canonical_hash(
                    PROTOCOL.canonical_transient_retry_policy(host, contract)
                ),
            },
            "trials": [
                {"trial": trial, "comparison_group_id": str(uuid.uuid4())}
                for trial in range(1, 4)
            ],
            "evaluation_protocol": {
                "revision": anchor,
                "sha256": PROTOCOL.evaluation_protocol_hash(manifest),
                "files": manifest,
            },
        }
        campaign_path = root / "evals" / "synthetic-campaign.json"
        campaign_path.write_text(json.dumps(campaign, indent=2), encoding="utf-8")
        self._git(root, "add", str(campaign_path.relative_to(root)))
        self._git(root, "commit", "--quiet", "-m", "preregister campaign")
        return contract, campaign, campaign_path

    def test_committed_post_anchor_campaign_binds_canonical_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, payload, path = self._fixture(root)
            campaign = PROTOCOL.load_campaign(root, path, contract)

            self.assertEqual(payload["campaign_id"], campaign.campaign_id)
            self.assertEqual({1, 2, 3}, set(campaign.trial_groups))
            self.assertEqual(
                payload["evaluation_anchor_revision"], campaign.anchor_revision
            )

    def test_protocol_worktree_change_after_anchor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, _payload, path = self._fixture(root)
            (root / "scripts" / "compare-skill-evals.py").write_text(
                "# post-result threshold edit\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "differs from anchor"
            ):
                PROTOCOL.load_campaign(root, path, contract)

    def test_arbitrary_self_consistent_host_hash_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, payload, path = self._fixture(root)
            payload["condition"]["host_config_sha256"] = "0" * 64
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "host policy is not canonical"
            ):
                PROTOCOL.load_campaign(
                    root, path, contract, require_committed=False
                )

    def test_canonical_transient_retry_policy_is_host_specific(self) -> None:
        contract = self._retry_contract()

        codex = PROTOCOL.canonical_transient_retry_policy("codex", contract)
        claude = PROTOCOL.canonical_transient_retry_policy("claude", contract)

        self.assertEqual(1, codex["schema_version"])
        self.assertEqual(2, codex["maximum_attempts_per_case"])
        self.assertEqual([5], codex["backoff_seconds"])
        self.assertEqual(
            self._retry_policy()["retryable_errors"]["codex"],
            codex["retryable_errors"],
        )
        self.assertEqual([], claude["retryable_errors"])

    def test_routing_result_extraction_is_shared_and_strict(self) -> None:
        route = {"actual_owner": "diagnose", "handoffs": []}
        response = json.dumps(route, ensure_ascii=False)
        self.assertEqual(
            (response, route), PROTOCOL.extract_routing_result("", response)
        )

        nested = json.dumps(
            {"type": "turn.completed", "structured_output": response}
        )
        self.assertEqual(
            (response, route), PROTOCOL.extract_routing_result(nested, "")
        )
        self.assertIsNone(
            PROTOCOL.extract_routing_result(
                '{"actual_owner":"diagnose","actual_owner":"repo-map",'
                '"handoffs":[]}',
                "",
            )
        )
        self.assertIsNone(
            PROTOCOL.extract_routing_result(
                json.dumps({**route, "reason": "extra"}), ""
            )
        )

    def test_transient_classifier_accepts_exact_codex_capacity_error(self) -> None:
        self.assertEqual(
            "model_capacity",
            PROTOCOL.classify_transient_host_failure(
                "codex",
                1,
                json.dumps(
                    {
                        "error": {
                            "message": (
                                " Selected   model is at capacity. "
                                "Please try a different model. "
                            )
                        }
                    }
                ),
                "",
                False,
                None,
                None,
                self._retry_contract(),
            ),
        )

    def test_transient_classifier_rejects_near_match_and_duplicate_json(self) -> None:
        contract = self._retry_contract()
        for stdout in (
            json.dumps(
                {
                    "message": "Selected model is at capacity; please try again."
                }
            ),
            '{"message":"Selected model is at capacity. Please try a different model.",'
            '"message":"Selected model is at capacity. Please try a different model."}',
            "not-json\n"
            + json.dumps(
                {
                    "message": (
                        "Selected model is at capacity. "
                        "Please try a different model."
                    )
                }
            ),
            json.dumps(
                {
                    "message": {
                        "nested": (
                            "Selected model is at capacity. "
                            "Please try a different model."
                        )
                    }
                }
            ),
        ):
            with self.subTest(stdout=stdout):
                self.assertIsNone(
                    PROTOCOL.classify_transient_host_failure(
                        "codex", 1, stdout, "", False, None, None, contract
                    )
                )

    def test_transient_classifier_rejects_valid_result_and_token_usage(self) -> None:
        contract = self._retry_contract()
        for has_valid_result, input_tokens, output_tokens in (
            (True, None, None),
            (False, 12, None),
            (False, None, 3),
        ):
            with self.subTest(
                has_valid_result=has_valid_result,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            ):
                self.assertIsNone(
                    PROTOCOL.classify_transient_host_failure(
                        "codex",
                        1,
                        json.dumps(
                            {
                                "message": (
                                    "Selected model is at capacity. "
                                    "Please try a different model."
                                )
                            }
                        ),
                        "",
                        has_valid_result,
                        input_tokens,
                        output_tokens,
                        contract,
                    )
                )

        self.assertIsNone(
            PROTOCOL.classify_transient_host_failure(
                "codex",
                1,
                json.dumps(
                    {
                        "message": (
                            "Selected model is at capacity. "
                            "Please try a different model."
                        )
                    }
                ),
                json.dumps({"usage": {"input_tokens": 1}}),
                False,
                None,
                None,
                contract,
            )
        )

    def test_transient_classifier_rejects_claude_and_success_exit(self) -> None:
        contract = self._retry_contract()
        message = json.dumps(
            {
                "message": (
                    "Selected model is at capacity. Please try a different model."
                )
            }
        )
        self.assertIsNone(
            PROTOCOL.classify_transient_host_failure(
                "claude", 1, message, "", False, None, None, contract
            )
        )
        self.assertIsNone(
            PROTOCOL.classify_transient_host_failure(
                "codex", 0, message, "", False, None, None, contract
            )
        )
        self.assertIsNone(
            PROTOCOL.classify_transient_host_failure(
                "codex", 124, message, "", False, None, None, contract
            )
        )

    def test_transient_retry_policy_requires_exact_canonical_values(self) -> None:
        invalid_policies = (
            ("schema_version", 2, "schema_version must be 1"),
            (
                "maximum_attempts_per_case",
                3,
                "maximum_attempts_per_case must be 2",
            ),
            ("backoff_seconds", [10], r"backoff_seconds must be \[5\]"),
            (
                "retryable_errors",
                {"claude": [], "codex": []},
                "retryable_errors are not canonical",
            ),
        )
        for field, value, message in invalid_policies:
            with self.subTest(field=field):
                policy = self._retry_policy()
                policy[field] = value
                with self.assertRaisesRegex(PROTOCOL.ProtocolError, message):
                    PROTOCOL.canonical_transient_retry_policy(
                        "codex", self._retry_contract(policy)
                    )

    def test_transient_retry_policy_is_included_in_host_policy_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, _payload, _path = self._fixture(root)
            policy = PROTOCOL.canonical_host_policy("codex", "gpt-5-test", contract)

            self.assertEqual(
                self._retry_policy()["retryable_errors"]["codex"],
                policy["transient_retry_policy"]["retryable_errors"],
            )
            self.assertIn(
                "per host attempt", policy["environment_isolation"]["home"]
            )
            mutated = json.loads(PROTOCOL.canonical_json(policy))
            mutated["transient_retry_policy"]["backoff_seconds"] = [6]
            self.assertNotEqual(
                PROTOCOL.canonical_hash(policy), PROTOCOL.canonical_hash(mutated)
            )

    def test_campaign_requires_canonical_retry_policy_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, payload, path = self._fixture(root)
            payload["condition"]["retry_policy_sha256"] = "0" * 64
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "transient retry policy is not canonical"
            ):
                PROTOCOL.load_campaign(root, path, contract, require_committed=False)

    def test_environment_policy_records_names_not_secret_values(self) -> None:
        contract = {
            "behavior_eval": {
                "prompt_template_version": 2,
                "evaluation_protocol": {
                    "canonical_routing": {
                        "environment_policy_version": 1,
                        "environment_source_allowlist": ["LANG", "PATH"],
                    }
                },
            }
        }
        policy = PROTOCOL.canonical_environment_policy("codex", contract)
        rendered = PROTOCOL.canonical_json(policy)
        self.assertEqual(["LANG", "PATH"], policy["source_allowlist"])
        self.assertNotIn("secret", rendered.casefold())
        self.assertFalse(policy["record_values"])

    def test_prompt_fingerprint_normalizes_unicode_case_and_whitespace(self) -> None:
        self.assertEqual(
            PROTOCOL.canonical_prompt_fingerprint("  Ｒoute\tTHIS\nrequest  "),
            PROTOCOL.canonical_prompt_fingerprint("route this request"),
        )

    def test_campaign_requires_dataset_and_provenance_same_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, payload, path = self._fixture(root)
            payload["provenance"]["git_revision"] = self._git(root, "rev-parse", "HEAD")
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(
                PROTOCOL.ProtocolError, "same Git revision"
            ):
                PROTOCOL.load_campaign(
                    root, path, contract, require_committed=False
                )


if __name__ == "__main__":
    unittest.main()
