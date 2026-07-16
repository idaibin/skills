#!/usr/bin/env python3
"""Regression tests for the deterministic routing campaign creator."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


SCRIPT = Path(__file__).with_name("create-skill-routing-campaign.py")
SPEC = importlib.util.spec_from_file_location(
    "create_skill_routing_campaign_test", SCRIPT
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
CREATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CREATOR
SPEC.loader.exec_module(CREATOR)


class CampaignCreatorTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    def _fixture(self, root: Path) -> dict[str, object]:
        self._git(root, "init", "--quiet")
        self._git(root, "config", "user.name", "AICraft Test")
        self._git(root, "config", "user.email", "test@example.invalid")
        initial_branch = self._git(root, "branch", "--show-current") or "master"
        (root / "README.md").write_text("previous\n", encoding="utf-8")
        self._git(root, "add", "README.md")
        self._git(root, "commit", "--quiet", "-m", "previous")
        previous = self._git(root, "rev-parse", "HEAD")

        protocol_files = [
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
                    "files": protocol_files,
                    "canonical_routing": {
                        "reviewer": "scripts/run-skill-routing-eval.py",
                        "reviewer_version": "6",
                        "environment_policy_version": 1,
                        "environment_source_allowlist": ["LANG", "PATH"],
                        "transient_retry_policy": {
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
                                            "selected model is at capacity. "
                                            "please try a different model."
                                        ],
                                    }
                                ],
                            },
                        },
                    },
                },
            }
        }
        for relative in protocol_files:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            content = json.dumps(contract) if relative.startswith("contracts/") else relative
            path.write_text(content + "\n", encoding="utf-8")
        self._git(root, "add", "contracts", "scripts")
        self._git(root, "commit", "--quiet", "-m", "candidate anchor")
        anchor = self._git(root, "rev-parse", "HEAD")

        evals = root / "evals"
        evals.mkdir()
        dataset = evals / "synthetic-routing.jsonl"
        provenance = evals / "synthetic-provenance.json"
        dataset.write_text(
            '{"id":"synthetic-001","prompt":"synthetic request"}\n',
            encoding="utf-8",
        )
        provenance.write_text('{"schema_version":1}\n', encoding="utf-8")
        self._git(root, "add", "evals")
        self._git(root, "commit", "--quiet", "-m", "post-anchor inputs")
        return {
            "contract": contract,
            "branch": initial_branch,
            "previous": previous,
            "anchor": anchor,
            "dataset": "evals/synthetic-routing.jsonl",
            "provenance": "evals/synthetic-provenance.json",
        }

    def _build(self, root: Path, fixture: dict[str, object], **changes):
        arguments = {
            "candidate_anchor": str(fixture["anchor"]),
            "previous_revision": str(fixture["previous"]),
            "dataset_path": str(fixture["dataset"]),
            "provenance_path": str(fixture["provenance"]),
            "host": "codex",
            "model": "gpt-5-test",
            "timeout_seconds": 120,
            "concurrency": 1,
            "trial_count": 3,
            "campaign_id": "b471fd65-795f-4df0-aa78-721e915a5797",
        }
        arguments.update(changes)
        return CREATOR.build_campaign(root, **arguments)

    def test_generate_then_load_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            first = self._build(root, fixture)
            second = self._build(root, fixture)
            self.assertEqual(first, second)
            self.assertEqual(3, len(first["trials"]))
            self.assertEqual(
                3,
                len(
                    {
                        item["comparison_group_id"]
                        for item in first["trials"]
                    }
                ),
            )

            output = root / "evals" / "campaign.json"
            CREATOR.create_campaign(root, output, first)
            loaded = CREATOR.PROTOCOL.load_campaign(
                root,
                output,
                fixture["contract"],
                require_committed=False,
            )
            self.assertEqual(first, loaded.payload)
            self.assertEqual(first["campaign_id"], loaded.campaign_id)

    def test_default_campaign_id_is_fresh_for_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            first = self._build(root, fixture, campaign_id=None)
            second = self._build(root, fixture, campaign_id=None)

            self.assertNotEqual(first["campaign_id"], second["campaign_id"])
            uuid.UUID(str(first["campaign_id"]))
            uuid.UUID(str(second["campaign_id"]))

    def test_previous_must_be_strict_anchor_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            head = self._git(root, "rev-parse", "HEAD")
            self._git(root, "checkout", "--quiet", "-b", "side", str(fixture["previous"]))
            (root / "side.txt").write_text("side\n", encoding="utf-8")
            self._git(root, "add", "side.txt")
            self._git(root, "commit", "--quiet", "-m", "side revision")
            side = self._git(root, "rev-parse", "HEAD")
            self._git(root, "checkout", "--quiet", str(fixture["branch"]))
            self.assertEqual(head, self._git(root, "rev-parse", "HEAD"))

            with self.assertRaisesRegex(
                CREATOR.CampaignCreationError, "strict ancestor"
            ):
                self._build(root, fixture, previous_revision=side)

    def test_existing_output_is_not_overwritten_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            payload = self._build(root, fixture)
            output = root / "evals" / "campaign.json"
            CREATOR.create_campaign(root, output, payload)
            original = output.read_bytes()

            with self.assertRaisesRegex(
                CREATOR.CampaignCreationError, "refusing to overwrite"
            ):
                CREATOR.create_campaign(root, output, payload)
            self.assertEqual(original, output.read_bytes())

    def test_uncommitted_or_non_post_anchor_dataset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            dataset = root / str(fixture["dataset"])
            dataset.write_text("changed after commit\n", encoding="utf-8")
            with self.assertRaisesRegex(
                CREATOR.CampaignCreationError, "committed blob"
            ):
                self._build(root, fixture)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            with self.assertRaisesRegex(
                CREATOR.CampaignCreationError, "committed after the anchor"
            ):
                self._build(root, fixture, dataset_path="README.md")

    def test_dataset_and_provenance_must_share_post_anchor_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            provenance = root / str(fixture["provenance"])
            provenance.write_text('{"schema_version":2}\n', encoding="utf-8")
            self._git(root, "add", str(fixture["provenance"]))
            self._git(root, "commit", "--quiet", "-m", "separate provenance update")

            with self.assertRaisesRegex(
                CREATOR.CampaignCreationError, "same post-anchor commit"
            ):
                self._build(root, fixture)

    def test_dry_run_self_validates_without_writing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self._fixture(root)
            payload = self._build(root, fixture)
            output = root / "evals" / "campaign.json"
            CREATOR.create_campaign(root, output, payload, dry_run=True)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
