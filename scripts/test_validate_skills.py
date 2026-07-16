#!/usr/bin/env python3
"""Regression tests for the skill package validator."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

VALIDATOR_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load validator: {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

markdown_table_rows = VALIDATOR.markdown_table_rows
validate_eval_cases = VALIDATOR.validate_eval_cases
validate_local_links = VALIDATOR.validate_local_links
validate_repository_indexes = VALIDATOR.validate_repository_indexes
validate_quality_status = VALIDATOR.validate_quality_status
validate_routing_graph = VALIDATOR.validate_routing_graph
validate_skill_invocations = VALIDATOR.validate_skill_invocations
validate_specialized_eval_contracts = VALIDATOR.validate_specialized_eval_contracts
validate_cross_artifact_contracts = VALIDATOR.validate_cross_artifact_contracts
expected_routes_to_skill = VALIDATOR.expected_routes_to_skill
validate_shared_browser_operation_protocol = VALIDATOR.validate_shared_browser_operation_protocol

BEHAVIOR_EVAL_PATH = Path(__file__).with_name("eval-human-writing.py")
BEHAVIOR_SPEC = importlib.util.spec_from_file_location("eval_human_writing", BEHAVIOR_EVAL_PATH)
if BEHAVIOR_SPEC is None or BEHAVIOR_SPEC.loader is None:
    raise RuntimeError(f"Cannot load behavior eval: {BEHAVIOR_EVAL_PATH}")
BEHAVIOR_EVAL = importlib.util.module_from_spec(BEHAVIOR_SPEC)
sys.modules[BEHAVIOR_SPEC.name] = BEHAVIOR_EVAL
BEHAVIOR_SPEC.loader.exec_module(BEHAVIOR_EVAL)

CONTRACT_EVAL_PATH = Path(__file__).with_name("eval-skill-contracts.py")
CONTRACT_EVAL_SPEC = importlib.util.spec_from_file_location(
    "eval_skill_contracts", CONTRACT_EVAL_PATH
)
if CONTRACT_EVAL_SPEC is None or CONTRACT_EVAL_SPEC.loader is None:
    raise RuntimeError(f"Cannot load contract eval: {CONTRACT_EVAL_PATH}")
CONTRACT_EVAL = importlib.util.module_from_spec(CONTRACT_EVAL_SPEC)
sys.modules[CONTRACT_EVAL_SPEC.name] = CONTRACT_EVAL
CONTRACT_EVAL_SPEC.loader.exec_module(CONTRACT_EVAL)


VALID_EVAL = """# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `one` | Trigger. |
| `two` | Trigger. |
| `three` | Trigger. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `four` | Prefer another skill. |
| `five` | Prefer another skill. |
| `six` | Prefer another skill. |

## Quality Eval

| Case | Pass | Reject If |
| --- | --- | --- |
| A | Evidence A | Failure A |
| B | Evidence B | Failure B |
| C | Evidence C | Failure C |
| D | Evidence D | Failure D |

## Scoring

Minimum pass: every quality case scores at least 8.
"""


class ValidateSkillsTests(unittest.TestCase):
    @staticmethod
    def verified_score_bundle(
        evidence_kind: str,
        results: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "results": results,
            "_evidence_kind": evidence_kind,
            "_verified_results": {str(item["id"]): item for item in results},
        }

    @staticmethod
    def perfect_routing_bundle(
        cases: list[dict[str, object]],
    ) -> dict[str, object]:
        return ValidateSkillsTests.verified_score_bundle(
            "routing",
            [
                {
                    "id": case["id"],
                    "actual_owner": case["expected_owner"],
                    "handoffs": [
                        *case.get("required_handoffs", []),
                        *[
                            group[0]
                            for group in case.get("required_handoff_groups", [])
                        ],
                    ],
                }
                for case in cases
            ],
        )

    @staticmethod
    def write_result_bundle_fixture(
        root: Path,
        dataset_path: Path,
        *,
        result_id: str = "case-001",
    ) -> tuple[Path, dict[str, object]]:
        dataset_rows = [
            json.loads(line)
            for line in dataset_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        prompt = next(
            str(row["prompt"]) for row in dataset_rows if row.get("id") == result_id
        )
        run_id = "00000000-0000-4000-8000-000000000001"
        model = "fixture-model-1"
        host = "fixture-host/1"
        prompt_template = CONTRACT_EVAL.PROTOCOL.canonical_prompt_template(
            CONTRACT_EVAL.CONTRACTS
        )
        invocation_prompt = prompt_template.replace(
            CONTRACT_EVAL.PROMPT_VALUE_PLACEHOLDER,
            json.dumps(prompt, ensure_ascii=False),
        )
        metrics = {
            "duration_ms": 1,
            "input_tokens": 1,
            "output_tokens": 1,
            "attempt_count": 1,
            "retry_count": 0,
        }
        raw_path = root / "raw" / f"{result_id}.json"
        raw_path.parent.mkdir(parents=True)
        model_output = json.dumps(
            {"actual_owner": "diagnose", "handoffs": []}
        )
        stdout = json.dumps(
            {"usage": {"input_tokens": 1, "output_tokens": 1}}
        )
        stderr = ""
        transcript = f"STDOUT\n{stdout}\nSTDERR\n{stderr}"
        raw_started_at = datetime.now(timezone.utc).isoformat()
        raw_completed_at = raw_started_at
        retry_policy_sha256 = CONTRACT_EVAL.PROTOCOL.canonical_hash(
            CONTRACT_EVAL.PROTOCOL.canonical_transient_retry_policy(
                "codex", CONTRACT_EVAL.CONTRACTS
            )
        )
        host_attempt = {
            "attempt_index": 1,
            "started_at": raw_started_at,
            "completed_at": raw_completed_at,
            "duration_ms": 1,
            "exit_code": 0,
            "stdout": stdout,
            "stderr": stderr,
            "response": model_output,
            "model_output": model_output,
            "transcript": transcript,
            "transcript_sha256": CONTRACT_EVAL.text_hash(transcript),
            "error_class": None,
            "error": None,
            "retryable": False,
            "backoff_seconds_before_next": 0,
            "observations": {
                "actual_owner": "diagnose",
                "handoffs": [],
            },
            "metrics": {
                "duration_ms": 1,
                "input_tokens": 1,
                "output_tokens": 1,
            },
        }
        raw_path.write_text(
            json.dumps(
                {
                    "schema_version": CONTRACT_EVAL.RAW_EVIDENCE_SCHEMA_VERSION,
                    "run_id": run_id,
                    "case_id": result_id,
                    "prompt_sha256": CONTRACT_EVAL.text_hash(prompt),
                    "invocation_prompt": invocation_prompt,
                    "invocation_prompt_sha256": CONTRACT_EVAL.text_hash(
                        invocation_prompt
                    ),
                    "model": model,
                    "host": host,
                    "started_at": raw_started_at,
                    "completed_at": raw_completed_at,
                    "stdout": stdout,
                    "stderr": stderr,
                    "model_output": model_output,
                    "transcript": transcript,
                    "transcript_sha256": CONTRACT_EVAL.text_hash(transcript),
                    "retry_policy_sha256": retry_policy_sha256,
                    "host_attempts": [host_attempt],
                    "exit_code": 0,
                    "observations": {
                        "actual_owner": "diagnose",
                        "handoffs": [],
                    },
                    "metrics": metrics,
                }
            ),
            encoding="utf-8",
        )
        raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=VALIDATOR_PATH.parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        skill_tree_sha = subprocess.run(
            ["git", "rev-parse", f"{revision}:skills"],
            cwd=VALIDATOR_PATH.parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        payload: dict[str, object] = {
            "schema_version": CONTRACT_EVAL.RESULT_SCHEMA_VERSION,
            "run_id": run_id,
            "model": model,
            "host": host,
            "skill_revision": revision,
            "skill_tree_sha": skill_tree_sha,
            "dataset_revision": CONTRACT_EVAL.dataset_hash(dataset_path),
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "complete": True,
            "run_config": {
                "trial": 1,
                "variant": "candidate",
                "dataset_path": dataset_path.name,
                "prompt_set_sha256": CONTRACT_EVAL.dataset_hash(dataset_path),
                "case_set_sha256": CONTRACT_EVAL.case_set_hash(dataset_rows),
                "case_ids": [str(row["id"]) for row in dataset_rows],
                "comparison_group_id": "00000000-0000-4000-8000-000000000002",
                "attempt_id": "00000000-0000-4000-8000-000000000003",
                "attempt_path": "attempt.json",
                "campaign_id": None,
                "campaign_path": None,
                "campaign_sha256": None,
                "evaluation_protocol_revision": None,
                "evaluation_protocol_sha256": None,
                "held_out": False,
                "permissions": "read-only",
                "timeout_seconds": 60,
                "concurrency": 1,
                "host_name": "codex",
                "fixture": None,
                "fixture_sha256": None,
                "skills_installed": True,
                "skill_fixture_sha256": CONTRACT_EVAL.committed_skill_fixture_hash(
                    revision
                ),
                "prompt_template_version": CONTRACT_EVAL.PROMPT_TEMPLATE_VERSION,
                "prompt_template": prompt_template,
                "prompt_template_sha256": CONTRACT_EVAL.text_hash(prompt_template),
                "host_config_sha256": CONTRACT_EVAL.PROTOCOL.canonical_hash(
                    CONTRACT_EVAL.PROTOCOL.canonical_host_policy(
                        "codex", model, CONTRACT_EVAL.CONTRACTS
                    )
                ),
                "environment_policy_sha256": CONTRACT_EVAL.PROTOCOL.canonical_hash(
                    CONTRACT_EVAL.PROTOCOL.canonical_environment_policy(
                        "codex", CONTRACT_EVAL.CONTRACTS
                    )
                ),
                "retry_policy_sha256": retry_policy_sha256,
            },
            "adjudication": CONTRACT_EVAL.PROTOCOL.canonical_adjudication(
                CONTRACT_EVAL.CONTRACTS
            ),
            "results": [
                {
                    "id": result_id,
                    "raw_evidence": str(raw_path.relative_to(root)),
                    "raw_evidence_sha256": raw_hash,
                    "metrics": metrics,
                }
            ],
        }
        bundle_path = root / "results.json"
        bundle_path.write_text(json.dumps(payload), encoding="utf-8")
        return bundle_path, payload

    @staticmethod
    def write_quality_evidence_manifest(
        root: Path,
        specs: list[dict[str, object]],
    ) -> Path:
        dataset_path = root / "evals" / "routing.jsonl"
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        dataset_path.write_text(
            '{"id":"case-1","prompt":"fixture request"}\n',
            encoding="utf-8",
        )
        dataset_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        campaign_path = root / "evals" / "routing-campaign.json"
        campaign_path.write_text('{"fixture":"campaign"}\n', encoding="utf-8")
        campaign_hash = hashlib.sha256(campaign_path.read_bytes()).hexdigest()
        records: list[dict[str, object]] = []
        for index, spec in enumerate(specs, 1):
            bundle_name = str(spec.get("bundle_name", f"bundle-{index}"))
            bundle_dir = root / "evidence" / bundle_name
            bundle_dir.mkdir(parents=True, exist_ok=True)
            raw_path = bundle_dir / "raw.json"
            raw_path.write_text(str(spec.get("raw", f'{{"run":{index}}}\n')), encoding="utf-8")
            raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()
            payload = {
                "run_id": str(spec.get("run_id", f"run-{index}")),
                "skill_revision": "a" * 40,
                "skill_tree_sha": "b" * 40,
                "run_config": {
                    "variant": str(spec.get("variant", "candidate")),
                    "trial": int(spec.get("trial", index)),
                    "prompt_set_sha256": "c" * 64,
                    "held_out": True,
                    "permissions": "read-only",
                    "timeout_seconds": 60,
                    "concurrency": 1,
                    "fixture_sha256": None,
                    "host_config_sha256": "d" * 64,
                    "campaign_id": "00000000-0000-4000-8000-000000000099",
                    "campaign_path": str(campaign_path.relative_to(root)),
                    "campaign_sha256": campaign_hash,
                    "evaluation_protocol_revision": "a" * 40,
                    "evaluation_protocol_sha256": "f" * 64,
                },
                "adjudication": {
                    "method": "deterministic",
                    "reviewer": "validator-regression",
                    "reviewer_version": "1",
                    "config_sha256": "e" * 64,
                },
                "results": [
                    {
                        "id": f"case-{index}",
                        "raw_evidence": "raw.json",
                        "raw_evidence_sha256": raw_hash,
                    }
                ],
            }
            bundle_path = bundle_dir / "results.json"
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")
            records.append(
                {
                    "id": str(spec.get("id", f"evidence-{index}")),
                    "kind": str(spec.get("kind", "routing")),
                    "dataset": str(dataset_path.relative_to(root)),
                    "dataset_sha256": dataset_hash,
                    "campaign": str(campaign_path.relative_to(root)),
                    "campaign_sha256": campaign_hash,
                    "bundle": str(bundle_path.relative_to(root)),
                    "bundle_sha256": hashlib.sha256(bundle_path.read_bytes()).hexdigest(),
                }
            )
        manifest = root / "docs" / "quality" / "evidence-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": VALIDATOR.QUALITY_EVIDENCE_SCHEMA_VERSION,
                    "claims": [],
                    "evidence": records,
                    "comparisons": [],
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def specialized_contract_errors(
        self, skill_name: str, mutation: tuple[str, str]
    ) -> list[str]:
        path = (
            VALIDATOR_PATH.parents[1]
            / "skills"
            / skill_name
            / "references"
            / "eval-cases.md"
        )
        original = path.read_text(encoding="utf-8")
        changed = original.replace(mutation[0], mutation[1], 1)
        self.assertNotEqual(original, changed)
        return validate_specialized_eval_contracts(skill_name, changed, label="test")

    def cross_artifact_contract_errors(
        self, skill_name: str, surface: str, marker: str, section: str | None = None
    ) -> list[str]:
        package = VALIDATOR_PATH.parents[1] / "skills" / skill_name
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
                "default_prompt",
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        original = surfaces[surface]
        if section is None:
            changed = re.sub(
                re.escape(marker), "removed-contract-marker", original, flags=re.IGNORECASE
            )
        else:
            start = original.find(section)
            self.assertGreaterEqual(start, 0)
            body_start = start + len(section)
            next_section = original.find("\n## ", body_start)
            end = len(original) if next_section < 0 else next_section
            scoped = re.sub(
                re.escape(marker),
                "removed-contract-marker",
                original[body_start:end],
                flags=re.IGNORECASE,
            )
            changed = original[:body_start] + scoped + original[end:]
        self.assertNotEqual(surfaces[surface], changed)
        surfaces[surface] = changed
        return validate_cross_artifact_contracts(skill_name, surfaces, label="test")

    def test_repository_indexes_must_match_source_packages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha"),
                VALIDATOR.SkillPackage(name="beta", path=root / "skills" / "beta"),
            ]
            (root / "README.md").write_text(
                "| `alpha` | First |\n| `beta` | Second |\n", encoding="utf-8"
            )
            (root / "INSTALL.md").write_text(
                "- `skills/alpha`\n- `skills/beta`\n", encoding="utf-8"
            )
            (root / "skills.sh.json").write_text(
                '{"groupings":[{"skills":["alpha","beta"]}]}', encoding="utf-8"
            )

            self.assertEqual([], validate_repository_indexes(root, packages))

            (root / "skills.sh.json").write_text(
                '{"groupings":[{"skills":["alpha","gamma"]}]}', encoding="utf-8"
            )
            errors = validate_repository_indexes(root, packages)

        self.assertTrue(any("missing skill beta" in error for error in errors))
        self.assertTrue(any("unknown skill gamma" in error for error in errors))

    def test_quality_status_uses_verifiable_axes_and_complete_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            status = root / "docs" / "quality" / "status.md"
            status.parent.mkdir(parents=True)
            status.write_text(
                "## Skill Status\n\n"
                "| Skill | Functional category | Release | Structure | Behavior | Workflow |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| `alpha` | Core Engineering | available | verified | not_verified | not_verified |\n"
                "| `beta` | Runtime Operations | hidden | verified | not_verified | not_verified |\n",
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha"),
                VALIDATOR.SkillPackage(name="beta", path=root / "skills" / "beta"),
            ]

            self.assertEqual([], validate_quality_status(root, packages))

            status.write_text(
                status.read_text(encoding="utf-8").replace(
                    "Runtime Operations | hidden | verified",
                    "Experimental | beta | partial",
                ),
                encoding="utf-8",
            )
            errors = validate_quality_status(root, packages)

        self.assertTrue(any("unknown category" in error for error in errors))
        self.assertTrue(any("unknown release state" in error for error in errors))
        self.assertTrue(any("unknown structure state" in error for error in errors))

    def test_quality_status_rejects_verified_axis_without_evidence_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            status = root / "docs" / "quality" / "status.md"
            status.parent.mkdir(parents=True)
            status.write_text(
                "## Skill Status\n\n"
                "| Skill | Functional category | Release | Structure | Behavior | Workflow |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| `alpha` | Core Engineering | available | verified | verified | not_verified |\n",
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha")
            ]

            errors = validate_quality_status(root, packages)

        self.assertTrue(
            any(
                "behavior=verified" in error
                and "passing candidate routing trials" in error
                for error in errors
            )
        )
        self.assertTrue(
            any("producer-attested only" in error for error in errors), errors
        )

    def test_official_baseline_requires_current_multilane_sources(self) -> None:
        contracts = copy.deepcopy(VALIDATOR.VALIDATION_CONTRACTS)
        validator = getattr(VALIDATOR, "validate_official_baseline")

        self.assertEqual([], validator(contracts, today=date(2026, 7, 16)))

        stale_errors = validator(contracts, today=date(2026, 10, 17))
        self.assertTrue(any("review" in error.casefold() for error in stale_errors))

        contracts["official_baseline"]["sources"] = [
            source
            for source in contracts["official_baseline"]["sources"]
            if source["lane"] != "claude"
        ]
        lane_errors = validator(contracts, today=date(2026, 7, 16))
        self.assertTrue(any("claude" in error.casefold() for error in lane_errors))

        contracts = copy.deepcopy(VALIDATOR.VALIDATION_CONTRACTS)
        contracts["official_baseline"]["sources"] = [
            source
            for source in contracts["official_baseline"]["sources"]
            if source["lane"] != "evaluation"
        ]
        lane_errors = validator(contracts, today=date(2026, 7, 16))
        self.assertTrue(any("evaluation" in error.casefold() for error in lane_errors))

    def test_official_baseline_rejects_future_review_date(self) -> None:
        contracts = copy.deepcopy(VALIDATOR.VALIDATION_CONTRACTS)
        contracts["official_baseline"]["reviewed_at"] = "2026-07-16"
        contracts["official_baseline"]["review_due"] = "2026-10-16"

        errors = VALIDATOR.validate_official_baseline(
            contracts, today=date(2026, 7, 15)
        )

        self.assertTrue(any("cannot be in the future" in error for error in errors))

    def test_strict_yaml_supports_single_and_double_quoted_strings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_path = Path(temp_dir) / "SKILL.md"
            skill_path.write_text(
                "---\n"
                "name: 'sample-skill'\n"
                'description: "Use when a quoted \\"value\\" is required."\n'
                "---\n\n# Sample\n",
                encoding="utf-8",
            )

            self.assertEqual([], VALIDATOR.frontmatter_contract_errors(skill_path))
            self.assertEqual(
                {
                    "name": "sample-skill",
                    "description": 'Use when a quoted "value" is required.',
                },
                VALIDATOR.read_frontmatter(skill_path),
            )

        interface, errors = VALIDATOR.openai_yaml_contract(
            "interface:\n"
            "  display_name: 'Reviewer''s Tool'\n"
            '  short_description: "Review a selected source safely"\n'
            "  default_prompt: 'Use $sample-skill to review it.'\n"
        )
        self.assertEqual([], errors)
        self.assertEqual("Reviewer's Tool", interface["display_name"])

    def test_strict_frontmatter_rejects_duplicate_keys_and_invalid_yaml(self) -> None:
        cases = {
            "duplicate": (
                "---\nname: alpha\nname: beta\ndescription: Use when testing.\n---\n",
                "duplicate key",
            ),
            "unterminated": (
                '---\nname: alpha\ndescription: "Use when testing.\n---\n',
                "unterminated",
            ),
            "nested": (
                "---\nname: alpha\n  description: Use when testing.\n---\n",
                "nested key has no parent",
            ),
        }
        for name, (content, marker) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "SKILL.md"
                path.write_text(content, encoding="utf-8")
                errors = VALIDATOR.frontmatter_contract_errors(path)
                self.assertTrue(any(marker in error for error in errors), errors)

    def test_openai_yaml_rejects_invalid_or_out_of_schema_mappings(self) -> None:
        cases = {
            "duplicate": (
                "interface:\n"
                "  display_name: One\n"
                "  display_name: Two\n"
                "  short_description: A useful description here\n"
                "  default_prompt: Use $sample to act.\n",
                "duplicate key",
            ),
            "illegal_yaml": (
                "interface:\n"
                '  display_name: "Unclosed\n'
                "  short_description: A useful description here\n"
                "  default_prompt: Use $sample to act.\n",
                "unterminated",
            ),
            "extra_top_level": (
                "interface:\n"
                "  display_name: Sample\n"
                "  short_description: A useful description here\n"
                "  default_prompt: Use $sample to act.\n"
                "policy: unsupported\n",
                "unsupported keys",
            ),
            "extra_interface_key": (
                "interface:\n"
                "  display_name: Sample\n"
                "  short_description: A useful description here\n"
                "  default_prompt: Use $sample to act.\n"
                "  hidden: value\n",
                "unsupported keys",
            ),
            "empty_value": (
                "interface:\n"
                "  display_name: ''\n"
                "  short_description: A useful description here\n"
                "  default_prompt: Use $sample to act.\n",
                "non-empty string",
            ),
        }
        for name, (content, marker) in cases.items():
            with self.subTest(name=name):
                _, errors = VALIDATOR.openai_yaml_contract(content)
                self.assertTrue(any(marker in error for error in errors), errors)

    def test_quality_evidence_rejects_run_bundle_and_raw_replay(self) -> None:
        cases = {
            "run_id": (
                [
                    {
                        "run_id": "00000000-0000-4000-8000-000000000101",
                        "raw": "first",
                        "trial": 1,
                    },
                    {
                        "run_id": "00000000-0000-4000-8000-000000000101",
                        "raw": "second",
                        "trial": 2,
                    },
                ],
                "duplicates run_id",
            ),
            "raw": (
                [
                    {
                        "run_id": "00000000-0000-4000-8000-000000000201",
                        "raw": "same raw",
                        "trial": 1,
                    },
                    {
                        "run_id": "00000000-0000-4000-8000-000000000202",
                        "raw": "same raw",
                        "trial": 2,
                    },
                ],
                "replays raw evidence",
            ),
        }

        def successful_run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            stdout = "b" * 40 + "\n" if command[:2] == ["git", "rev-parse"] else ""
            return subprocess.CompletedProcess(command, 0, stdout, "")

        for name, (specs, marker) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.write_quality_evidence_manifest(root, specs)
                with mock.patch.object(
                    VALIDATOR.subprocess, "run", side_effect=successful_run
                ):
                    errors, _ = VALIDATOR.validate_quality_evidence(root)
                self.assertTrue(any(marker in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = self.write_quality_evidence_manifest(
                root,
                [
                    {
                        "run_id": "00000000-0000-4000-8000-000000000301",
                        "raw": "first",
                        "trial": 1,
                    },
                    {
                        "run_id": "00000000-0000-4000-8000-000000000302",
                        "raw": "second",
                        "trial": 2,
                    },
                ],
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["evidence"][1]["bundle"] = manifest["evidence"][0]["bundle"]
            manifest["evidence"][1]["bundle_sha256"] = manifest["evidence"][0][
                "bundle_sha256"
            ]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(
                VALIDATOR.subprocess, "run", side_effect=successful_run
            ):
                errors, _ = VALIDATOR.validate_quality_evidence(root)
            self.assertTrue(any("reuses bundle path" in error for error in errors), errors)

    def test_quality_evidence_rejects_extra_top_level_claim_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = self.write_quality_evidence_manifest(root, [])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["improvement"] = "verified"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertTrue(any("top-level fields" in error for error in errors), errors)

    def test_quality_evidence_rejects_extra_record_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = self.write_quality_evidence_manifest(root, [])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["evidence"] = [
                {
                    "id": "misleading-evidence",
                    "kind": "routing",
                    "dataset": "evals/routing.jsonl",
                    "dataset_sha256": "a" * 64,
                    "bundle": "evidence/results.json",
                    "bundle_sha256": "b" * 64,
                    "status": "verified",
                }
            ]
            manifest["comparisons"] = [
                {
                    "id": "misleading-comparison",
                    "kind": "routing",
                    "candidate_evidence": ["candidate-1"],
                    "control_evidence": ["previous-1"],
                    "report": "evidence/comparison.json",
                    "report_sha256": "c" * 64,
                    "improvement": "verified",
                }
            ]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertTrue(
            any("evidence misleading-evidence fields" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                "comparison misleading-comparison fields" in error
                for error in errors
            ),
            errors,
        )

    def test_quality_evidence_rejects_pre_scope_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = self.write_quality_evidence_manifest(root, [])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schema_version"] = 3
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertTrue(
            any("schema_version must be 6" in error for error in errors), errors
        )

    def test_control_evidence_does_not_need_to_pass_candidate_score_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_quality_evidence_manifest(
                root,
                [
                    {
                        "run_id": "00000000-0000-4000-8000-000000000501",
                        "raw": "control evidence",
                        "trial": 1,
                        "variant": "previous",
                    }
                ],
            )
            calls: list[list[str]] = []

            def successful_validation(
                command: list[str], **_: object
            ) -> subprocess.CompletedProcess[str]:
                calls.append(command)
                stdout = "b" * 40 + "\n" if command[:2] == ["git", "rev-parse"] else ""
                return subprocess.CompletedProcess(command, 0, stdout, "")

            with mock.patch.object(
                VALIDATOR.subprocess, "run", side_effect=successful_validation
            ):
                errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertEqual([], errors)
        evaluator_calls = [
            command for command in calls if "eval-skill-contracts.py" in " ".join(command)
        ]
        self.assertEqual(1, len(evaluator_calls))
        self.assertIn("--allow-score-failure", evaluator_calls[0])

    def test_quality_evidence_binds_revision_to_current_skills_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_quality_evidence_manifest(
                root,
                [
                    {
                        "run_id": "00000000-0000-4000-8000-000000000401",
                        "raw": "tree evidence",
                        "trial": 1,
                    }
                ],
            )
            calls: list[list[str]] = []

            def changed_tree(
                command: list[str], **_: object
            ) -> subprocess.CompletedProcess[str]:
                calls.append(command)
                return subprocess.CompletedProcess(
                    command,
                    1 if command[:3] == ["git", "diff", "--quiet"] else 0,
                    "",
                    "",
                )

            with mock.patch.object(
                VALIDATOR.subprocess, "run", side_effect=changed_tree
            ):
                errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertTrue(
            any("does not match the current skills tree" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                command[:3] == ["git", "diff", "--quiet"]
                and command[-2:] == ["--", "skills"]
                for command in calls
            )
        )

    def test_improvement_claim_requires_replayed_passing_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest = root / "docs" / "quality" / "evidence-manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": VALIDATOR.QUALITY_EVIDENCE_SCHEMA_VERSION,
                        "claims": [
                            {
                                "id": "routing-outcome-improvement",
                                "status": "verified",
                                "comparison_id": "missing-comparison",
                                "dimension": "routing_outcome_vs_previous",
                                "kind": "routing",
                                "host_name": "codex",
                                "host_version": "codex-cli 1.0",
                                "model": "gpt-5-test",
                                "candidate_skill_revision": "a" * 40,
                                "previous_skill_revision": "b" * 40,
                                "baseline_skill_revision": "a" * 40,
                                "dataset_sha256": "c" * 64,
                                "dataset_git_revision": "d" * 40,
                                "evaluation_anchor_revision": "a" * 40,
                                "campaign_id": "00000000-0000-4000-8000-000000000099",
                                "campaign_path": "evals/routing-campaign.json",
                                "campaign_sha256": "f" * 64,
                                "evaluation_protocol_revision": "a" * 40,
                                "evaluation_protocol_sha256": "1" * 64,
                                "held_out_provenance_path": "evals/held-out-provenance.json",
                                "held_out_provenance_sha256": "e" * 64,
                                "skills": [],
                            }
                        ],
                        "evidence": [],
                        "comparisons": [],
                    }
                ),
                encoding="utf-8",
            )

            errors, _ = VALIDATOR.validate_quality_evidence(root)

        self.assertTrue(
            any("requires its replayed passing comparison" in error for error in errors),
            errors,
        )

    def test_quality_comparison_report_must_match_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "evals" / "held-out.jsonl"
            dataset.parent.mkdir(parents=True)
            dataset.write_text('{"id":"case-1"}\n', encoding="utf-8")
            dataset_hash = hashlib.sha256(dataset.read_bytes()).hexdigest()
            report = root / "evidence" / "comparison.json"
            report.parent.mkdir(parents=True)
            recorded = {
                "schema_version": 3,
                "status": "PASS",
                "claimable_dimensions": ["routing_outcome_vs_previous"],
                "errors": [],
            }
            report.write_text(json.dumps(recorded), encoding="utf-8")
            evidence: dict[str, dict[str, object]] = {}
            for variant in ("candidate", "previous", "baseline"):
                for trial in range(1, 4):
                    evidence_id = f"{variant}-{trial}"
                    evidence[evidence_id] = {
                        "kind": "routing",
                        "variant": variant,
                        "trial": trial,
                        "model": "gpt-5-test",
                        "host": "codex-cli 1.0",
                        "host_name": "codex",
                        "skill_revision": (
                            "b" if variant == "previous" else "a"
                        )
                        * 40,
                        "dataset_git_revision": "9" * 40,
                        "evaluation_anchor_revision": "a" * 40,
                        "campaign_id": "00000000-0000-4000-8000-000000000099",
                        "campaign_path": "evals/routing-campaign.json",
                        "campaign_sha256": "f" * 64,
                        "evaluation_protocol_revision": "a" * 40,
                        "evaluation_protocol_sha256": "1" * 64,
                        "held_out_provenance_path": "evals/held-out-provenance.json",
                        "held_out_provenance_sha256": "8" * 64,
                        "bundle_path": root / "evidence" / f"{evidence_id}.json",
                        "bundle_sha256": hashlib.sha256(
                            evidence_id.encode("utf-8")
                        ).hexdigest(),
                        "dataset_path": dataset,
                        "dataset_sha256": dataset_hash,
                    }
            comparison = {
                "id": "routing-improvement",
                "kind": "routing",
                "candidate_evidence": [f"candidate-{trial}" for trial in range(1, 4)],
                "previous_evidence": [f"previous-{trial}" for trial in range(1, 4)],
                "baseline_evidence": [f"baseline-{trial}" for trial in range(1, 4)],
                "campaign": "evals/routing-campaign.json",
                "campaign_sha256": "f" * 64,
                "report": str(report.relative_to(root)),
                "report_sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
            }

            successful_replay = subprocess.CompletedProcess(
                ["compare"], 0, json.dumps(recorded), ""
            )
            with mock.patch.object(
                VALIDATOR.subprocess, "run", return_value=successful_replay
            ):
                errors, passing = VALIDATOR.validate_quality_comparisons(
                    root, [comparison], evidence
                )
            self.assertEqual([], errors)
            self.assertEqual({"routing-improvement"}, set(passing))

            mismatched_replay = subprocess.CompletedProcess(
                ["compare"], 0, json.dumps({**recorded, "replayed": True}), ""
            )
            with mock.patch.object(
                VALIDATOR.subprocess, "run", return_value=mismatched_replay
            ):
                errors, passing = VALIDATOR.validate_quality_comparisons(
                    root, [comparison], evidence
                )
            self.assertEqual({}, passing)
            self.assertTrue(any("does not match replay" in error for error in errors))

    def test_package_policy_limits_are_enforced_by_validate_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = VALIDATOR_PATH.parents[1] / "skills" / "diagnose"
            package_path = Path(temp_dir) / "diagnose"
            shutil.copytree(source, package_path)

            skill_path = package_path / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            long_description = "Use when " + "x" * VALIDATOR.MAX_DESCRIPTION_CHARS
            skill_text = re.sub(
                r'^description:.*$',
                f'description: "{long_description}"',
                skill_text,
                count=1,
                flags=re.MULTILINE,
            )
            skill_text += "\n".join(
                ["", "[Long guide](references/long-guide.md)"]
                + [f"policy padding {index}" for index in range(60)]
            )
            skill_path.write_text(skill_text, encoding="utf-8")

            metadata_path = package_path / "agents" / "openai.yaml"
            metadata = metadata_path.read_text(encoding="utf-8")
            metadata = re.sub(
                r'^  short_description:.*$',
                '  short_description: "short"',
                metadata,
                count=1,
                flags=re.MULTILINE,
            )
            metadata = re.sub(
                r'^  default_prompt:.*$',
                f'  default_prompt: "Use $diagnose to {"x" * 230}"',
                metadata,
                count=1,
                flags=re.MULTILINE,
            )
            metadata_path.write_text(metadata, encoding="utf-8")

            long_reference = package_path / "references" / "long-guide.md"
            long_reference.write_text(
                "# Long Guide\n\n" + "\n".join(
                    f"Policy detail {index}." for index in range(101)
                ),
                encoding="utf-8",
            )

            errors, _ = VALIDATOR.validate_package(
                VALIDATOR.SkillPackage(name="diagnose", path=package_path),
                label="test",
            )

        self.assertTrue(
            any(
                "description" in error
                and str(VALIDATOR.MAX_DESCRIPTION_CHARS) in error
                for error in errors
            )
        )
        self.assertTrue(any("SKILL.md" in error and "120" in error for error in errors))
        self.assertTrue(any("short_description" in error and "25" in error for error in errors))
        self.assertTrue(any("default_prompt" in error and "220" in error for error in errors))
        self.assertTrue(any("long-guide.md" in error and "Contents" in error for error in errors))

    def test_shared_browser_operation_protocol_must_not_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_relative = Path("protocols/browser-operation-v1.md")
            relative_paths = (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            )
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            source_path = root / source_relative
            source_path.parent.mkdir(parents=True)
            source_path.write_text(source, encoding="utf-8")
            for relative in relative_paths:
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(source, encoding="utf-8")

            self.assertEqual([], validate_shared_browser_operation_protocol(root))

            (root / relative_paths[1]).write_text(source + "drift\n", encoding="utf-8")
            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(any("generated browser-operation protocol is stale" in error for error in errors))

    def test_shared_browser_operation_protocol_requires_structured_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            changed = source.replace("round_id: <same request round id>\n", "", 1)
            protocol_source = root / "protocols" / "browser-operation-v1.md"
            protocol_source.parent.mkdir(parents=True)
            protocol_source.write_text(changed, encoding="utf-8")
            for relative in (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(changed, encoding="utf-8")

            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(
            any("Handoff Result" in error and "round_id:" in error for error in errors)
        )

    def test_shared_browser_operation_protocol_rejects_invalid_retry_enum(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            changed = source.replace(
                "retry_policy: <never|only-if-no-side-effect-proven>",
                "retry_policy: <always>",
                1,
            )
            protocol_source = root / "protocols" / "browser-operation-v1.md"
            protocol_source.parent.mkdir(parents=True)
            protocol_source.write_text(changed, encoding="utf-8")
            for relative in (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(changed, encoding="utf-8")

            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(
            any("Handoff Request" in error and "retry_policy" in error for error in errors)
        )

    def test_legacy_regex_catches_retired_skill_names(self) -> None:
        for name in (
            "repo-context",
            "frontend-implementation",
            "frontend-governance",
            "rust-engineering-governance",
        ):
            self.assertIsNotNone(VALIDATOR.LEGACY_RE.search(f"use {name} now"))

    def test_markdown_table_rows_returns_data_only(self) -> None:
        rows = markdown_table_rows(VALID_EVAL, "## Trigger Eval")
        self.assertEqual(3, len(rows))
        self.assertEqual(["`one`", "Trigger."], rows[0])

    def test_eval_validation_accepts_minimum_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(VALID_EVAL, encoding="utf-8")
            errors, metrics = validate_eval_cases(eval_file, label="test")

        self.assertEqual([], errors)
        self.assertIsNotNone(metrics)
        self.assertEqual(3, metrics.trigger_cases)
        self.assertEqual(4, metrics.quality_cases)

    def test_eval_validation_rejects_duplicates_and_weak_scoring(self) -> None:
        invalid_eval = VALID_EVAL.replace("`two`", "`one`").replace("at least 8", "at least 5")
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(invalid_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("score" in error for error in errors))

    def test_eval_validation_rejects_historical_score_of_seven(self) -> None:
        historical_eval = VALID_EVAL.replace("at least 8", "at least 7")
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(historical_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertTrue(any("at least 8" in error for error in errors))

    def test_eval_validation_accepts_defect_gate(self) -> None:
        defect_gate_eval = VALID_EVAL.replace(
            "every quality case scores at least 8",
            "no P0 or P1 defect remains",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(defect_gate_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertEqual([], errors)

    def test_routing_graph_requires_symmetric_documented_neighbors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            alpha = root / "skills" / "alpha"
            beta = root / "skills" / "beta"
            for package, neighbor in ((alpha, "beta"), (beta, "alpha")):
                references = package / "references"
                references.mkdir(parents=True)
                (package / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text(
                    f"## Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n| route | Prefer `{neighbor}`. |\n"
                    "\n## Non-Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n",
                    encoding="utf-8",
                )
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":["alpha"]}', encoding="utf-8"
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            self.assertEqual([], validate_routing_graph(root, packages))

            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":[]}', encoding="utf-8"
            )
            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("must be symmetric" in error for error in errors))

    def test_routing_graph_ignores_neighbor_mentions_outside_expected_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            alpha = root / "skills" / "alpha"
            beta = root / "skills" / "beta"
            for package, prompt, expected in (
                (alpha, "Mention beta only in this prompt", "Stay with alpha."),
                (beta, "Route this case", "Prefer alpha."),
            ):
                references = package / "references"
                references.mkdir(parents=True)
                (package / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text(
                    "## Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n"
                    f"| {prompt} | {expected} |\n"
                    "\n## Non-Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n",
                    encoding="utf-8",
                )
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":["alpha"]}', encoding="utf-8"
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("source alpha" in error and "beta" in error for error in errors))

    def test_routing_expectation_requires_affirmative_semantics(self) -> None:
        self.assertTrue(expected_routes_to_skill("Should prefer `repo-map`.", "repo-map"))
        self.assertTrue(
            expected_routes_to_skill(
                "Trigger coordinator; delegate bounded work to `audit-rust`.",
                "audit-rust",
            )
        )
        self.assertFalse(expected_routes_to_skill("Do not use `repo-map`.", "repo-map"))
        self.assertFalse(expected_routes_to_skill("Should not use `repo-map`.", "repo-map"))
        self.assertFalse(
            expected_routes_to_skill(
                "Prefer `diagnose`, not `repo-map`.",
                "repo-map",
            )
        )
        self.assertFalse(expected_routes_to_skill("Mentions `repo-map` only.", "repo-map"))

    def test_routing_graph_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for name in ("alpha", "beta"):
                references = root / "skills" / name / "references"
                references.mkdir(parents=True)
                (references.parent / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text("", encoding="utf-8")
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"alpha":[],"beta":["alpha"]}',
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha"),
                VALIDATOR.SkillPackage(name="beta", path=root / "skills" / "beta"),
            ]

            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("duplicate key 'alpha'" in error for error in errors))

    def test_human_writing_behavior_fixtures_pass(self) -> None:
        results = BEHAVIOR_EVAL.run_fixtures(BEHAVIOR_EVAL.DEFAULT_FIXTURES)

        self.assertGreaterEqual(len(results), 10)
        self.assertTrue(all(result.passed for result in results))

    def test_human_writing_behavior_fixture_detects_bad_output(self) -> None:
        result = BEHAVIOR_EVAL.evaluate_case(
            {
                "id": "regression",
                "expected_pass": True,
                "output": "整体性能提升 10 倍。",
                "must_contain": ["类型检查", "官方"],
                "must_not_contain": ["整体性能"],
            }
        )

        self.assertFalse(result.passed)
        self.assertTrue(result.failures)

    def test_skill_contract_datasets_and_perfect_scores_pass(self) -> None:
        self.assertEqual([], CONTRACT_EVAL.validate_datasets())

        routing = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA)
        authority = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.AUTHORITY_DATA)
        workflow = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.WORKFLOW_DATA)
        self.assertGreaterEqual(len(routing), 70)
        self.assertGreaterEqual(len(authority), 14)
        self.assertGreaterEqual(len(workflow), 14)

        routing_bundle = self.perfect_routing_bundle(routing)
        authority_bundle = self.verified_score_bundle(
            "authority",
            [
                {
                    "id": case["id"],
                    "actual_owner": case["expected_owner"],
                    "observed_actions": list(case["required_actions"]),
                }
                for case in authority
            ],
        )
        workflow_bundle = self.verified_score_bundle(
            "workflow",
            [
                {
                    "id": case["id"],
                    "route": list(case["expected_route"]),
                    "observed_evidence": list(case["required_evidence"]),
                    "observed_actions": [],
                }
                for case in workflow
            ],
        )

        self.assertTrue(CONTRACT_EVAL.score_routing(routing, routing_bundle).passed)
        self.assertTrue(CONTRACT_EVAL.score_authority(authority, authority_bundle).passed)
        self.assertTrue(CONTRACT_EVAL.score_workflow(workflow, workflow_bundle).passed)

        risky = next(
            case for case in routing if case["high_risk"] and case["forbidden_owners"]
        )
        risky_result = next(
            result for result in routing_bundle["results"] if result["id"] == risky["id"]
        )
        risky_result["actual_owner"] = risky["forbidden_owners"][0]
        self.assertFalse(CONTRACT_EVAL.score_routing(routing, routing_bundle).passed)

        authority_bundle["results"][0]["observed_actions"].append(
            authority[0]["forbidden_actions"][0]
        )
        self.assertFalse(
            CONTRACT_EVAL.score_authority(authority, authority_bundle).passed
        )

        workflow_bundle["results"][0]["observed_evidence"] = []
        self.assertFalse(CONTRACT_EVAL.score_workflow(workflow, workflow_bundle).passed)

    def test_held_out_routing_requires_both_kinds_for_every_skill(self) -> None:
        known_skills = sorted(CONTRACT_EVAL.discover_skill_names())
        cases: list[dict[str, object]] = []
        for index, skill_name in enumerate(known_skills):
            neighbor = known_skills[(index + 1) % len(known_skills)]
            for kind_index, kind in enumerate(("trigger", "neighbor_non_trigger")):
                cases.append(
                    {
                        "id": f"heldout-{index + 1:02d}-{kind_index + 1}",
                        "prompt": (
                            f"Fresh evaluation request {index + 1}, "
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
        required_handoff_owners = list(
            CONTRACT_EVAL.BEHAVIOR_CONTRACT["comparative"][
                "required_held_out_handoff_primary_owners"
            ]
        )
        additional_owner = next(
            name for name in known_skills if name not in required_handoff_owners
        )
        for index, skill_name in enumerate(
            [*required_handoff_owners, additional_owner]
        ):
            owner_index = known_skills.index(skill_name)
            handoff = known_skills[(owner_index + 7) % len(known_skills)]
            cases.append(
                {
                    "id": f"heldout-handoff-{index + 1:02d}",
                    "prompt": f"Fresh multi-part evaluation request {index + 1}.",
                    "kind": "multi_intent",
                    "expected_owner": skill_name,
                    "allowed_owners": [skill_name],
                    "forbidden_owners": [],
                    "required_handoffs": [handoff],
                    "allowed_handoffs": [handoff],
                    "forbidden_handoffs": [],
                    "high_risk": False,
                }
            )

        self.assertEqual(
            [], CONTRACT_EVAL.validate_held_out_routing_cases(cases, set(known_skills))
        )

        cases[1]["kind"] = "trigger"
        errors = CONTRACT_EVAL.validate_held_out_routing_cases(
            cases, set(known_skills)
        )
        self.assertTrue(
            any("missing kinds ['neighbor_non_trigger']" in error for error in errors),
            errors,
        )

        no_positive_handoffs = copy.deepcopy(cases)
        for case in no_positive_handoffs:
            case["required_handoffs"] = []
            case["required_handoff_groups"] = []
            case["allowed_handoffs"] = []
        errors = CONTRACT_EVAL.validate_held_out_routing_cases(
            no_positive_handoffs, set(known_skills)
        )
        self.assertTrue(
            any("required-handoff cases, found 0" in error for error in errors),
            errors,
        )

    def test_contract_jsonl_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Path(temp_dir) / "duplicate.jsonl"
            dataset.write_text(
                '{"id":"first","id":"second","prompt":"request"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate JSON key 'id'"):
                CONTRACT_EVAL.load_jsonl(dataset)

    def test_routing_below_contract_threshold_fails(self) -> None:
        cases = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA))
        known_skills = sorted(CONTRACT_EVAL.discover_skill_names())
        bundle = self.perfect_routing_bundle(cases)
        minimum = float(
            CONTRACT_EVAL.ROUTING_CONTRACT["minimum_overall_exact_top1"]
        )
        passing_count = max(0, int(len(cases) * minimum) - 1)
        for result, case in zip(
            bundle["results"][passing_count:], cases[passing_count:]
        ):
            result["actual_owner"] = next(
                name for name in known_skills if name != case["expected_owner"]
            )

        score = CONTRACT_EVAL.score_routing(cases, bundle)

        self.assertFalse(score.passed)
        self.assertTrue(
            any(
                f"{passing_count}/{len(cases)}" in line
                for line in score.lines
            )
        )

    def test_routing_rejects_unknown_owner_and_handoff(self) -> None:
        cases = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA)

        owner_bundle = self.perfect_routing_bundle(cases)
        owner_bundle["results"][0]["actual_owner"] = "unknown-owner"
        with self.assertRaisesRegex(ValueError, "unknown.*owner"):
            CONTRACT_EVAL.score_routing(cases, owner_bundle)

        handoff_bundle = self.perfect_routing_bundle(cases)
        handoff_bundle["results"][0]["handoffs"] = ["unknown-handoff"]
        with self.assertRaisesRegex(ValueError, "unknown.*handoff"):
            CONTRACT_EVAL.score_routing(cases, handoff_bundle)

    def test_routing_requires_declared_handoff(self) -> None:
        cases = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA)
        bundle = self.perfect_routing_bundle(cases)
        required_case = next(case for case in cases if case.get("required_handoffs"))
        result = next(
            item for item in bundle["results"] if item["id"] == required_case["id"]
        )
        result["handoffs"] = []

        score = CONTRACT_EVAL.score_routing(cases, bundle)

        self.assertFalse(score.passed)
        self.assertTrue(any("required handoff" in line.casefold() for line in score.lines))

    def test_routing_case_assessment_requires_owner_and_complete_handoff_contract(
        self,
    ) -> None:
        case = {
            "id": "assessment",
            "expected_owner": "diagnose",
            "allowed_owners": ["diagnose", "audit-rust"],
            "required_handoffs": ["implement-rust"],
            "required_handoff_groups": [["repo-review", "audit-security"]],
            "allowed_handoffs": [
                "implement-rust",
                "repo-review",
                "audit-security",
            ],
            "forbidden_handoffs": ["repo-delivery"],
        }
        accepted = CONTRACT_EVAL.assess_routing_case(
            case,
            {
                "actual_owner": "audit-rust",
                "handoffs": ["implement-rust", "repo-review"],
            },
        )
        self.assertTrue(accepted["full_case_success"])

        missing_group = CONTRACT_EVAL.assess_routing_case(
            case,
            {"actual_owner": "diagnose", "handoffs": ["implement-rust"]},
        )
        self.assertFalse(missing_group["full_case_success"])
        self.assertEqual(
            [["audit-security", "repo-review"]],
            missing_group["missing_required_handoff_groups"],
        )

        overselected_group = CONTRACT_EVAL.assess_routing_case(
            case,
            {
                "actual_owner": "diagnose",
                "handoffs": [
                    "implement-rust",
                    "repo-review",
                    "audit-security",
                ],
            },
        )
        self.assertFalse(overselected_group["full_case_success"])
        self.assertEqual(
            [["audit-security", "repo-review"]],
            overselected_group["overselected_required_handoff_groups"],
        )

        unauthorized = CONTRACT_EVAL.assess_routing_case(
            case,
            {
                "actual_owner": "diagnose",
                "handoffs": ["implement-rust", "repo-review", "repo-delivery"],
            },
        )
        self.assertFalse(unauthorized["full_case_success"])
        self.assertEqual(["repo-delivery"], unauthorized["unauthorized_handoffs"])

    def test_unauthorized_handoff_rate_uses_affected_cases_as_denominator(self) -> None:
        cases = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA))
        bundle = self.perfect_routing_bundle(cases)
        known_skills = sorted(CONTRACT_EVAL.discover_skill_names())
        case = next(item for item in cases if not item.get("allowed_handoffs"))
        target = next(
            name for name in known_skills if name != case["expected_owner"]
        )
        result = next(
            item for item in bundle["results"] if item["id"] == case["id"]
        )
        result["handoffs"] = [target]

        score = CONTRACT_EVAL.score_routing(cases, bundle)

        self.assertFalse(score.passed)
        self.assertTrue(
            any(
                f"affected cases: 1/{len(cases)}" in line
                for line in score.lines
            )
        )

    def test_routing_dataset_rejects_owner_handoff_overlap(self) -> None:
        cases = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA))
        case = next(item for item in cases if item.get("required_handoffs"))
        case["allowed_owners"] = [
            case["expected_owner"],
            case["required_handoffs"][0],
        ]

        errors = CONTRACT_EVAL.validate_routing_cases(
            cases,
            CONTRACT_EVAL.discover_skill_names(),
            routing_graph_path=CONTRACT_EVAL.ROOT
            / "docs"
            / "skills"
            / "routing-graph.json",
        )

        self.assertTrue(
            any("allowed owners cannot also be handoffs" in error for error in errors),
            errors,
        )

    def test_routing_dataset_rejects_optional_allowed_handoffs(self) -> None:
        cases = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA))
        case = next(item for item in cases if not item.get("allowed_handoffs"))
        case["allowed_handoffs"] = [
            next(
                name
                for name in sorted(CONTRACT_EVAL.discover_skill_names())
                if name != case["expected_owner"]
            )
        ]

        errors = CONTRACT_EVAL.validate_routing_cases(
            cases,
            CONTRACT_EVAL.discover_skill_names(),
            routing_graph_path=CONTRACT_EVAL.ROOT
            / "docs"
            / "skills"
            / "routing-graph.json",
        )

        self.assertTrue(
            any("optional entries are not necessary handoffs" in error for error in errors),
            errors,
        )

    def test_routing_dataset_rejects_overlapping_handoff_requirements(self) -> None:
        cases = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA))
        case = next(item for item in cases if item.get("required_handoff_groups"))
        group_member = case["required_handoff_groups"][0][0]
        case["required_handoffs"] = [group_member]

        errors = CONTRACT_EVAL.validate_routing_cases(
            cases,
            CONTRACT_EVAL.discover_skill_names(),
            routing_graph_path=CONTRACT_EVAL.ROOT
            / "docs"
            / "skills"
            / "routing-graph.json",
        )

        self.assertTrue(
            any("must not overlap required_handoffs" in error for error in errors),
            errors,
        )

    def test_routing_rejects_duplicate_and_undeclared_handoffs(self) -> None:
        cases = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.ROUTING_DATA)
        allowed_case = next(case for case in cases if case.get("allowed_handoffs"))

        duplicate_bundle = self.perfect_routing_bundle(cases)
        duplicate_result = duplicate_bundle["_verified_results"][allowed_case["id"]]
        allowed = allowed_case["allowed_handoffs"][0]
        duplicate_result["handoffs"] = [allowed, allowed]
        with self.assertRaisesRegex(ValueError, "duplicates"):
            CONTRACT_EVAL.score_routing(cases, duplicate_bundle)

        undeclared_bundle = self.perfect_routing_bundle(cases)
        plain_case = next(case for case in cases if not case.get("allowed_handoffs"))
        undeclared_result = undeclared_bundle["_verified_results"][plain_case["id"]]
        undeclared_result["handoffs"] = [
            next(
                name
                for name in sorted(CONTRACT_EVAL.discover_skill_names())
                if name != plain_case["expected_owner"]
            )
        ]
        self.assertFalse(CONTRACT_EVAL.score_routing(cases, undeclared_bundle).passed)

    def test_execution_trace_must_derive_actions_and_evidence(self) -> None:
        raw = {
            "observations": {
                "route": ["repo-review"],
                "observed_actions": ["read_git_state"],
                "observed_evidence": ["git_state"],
            },
            "trace": [
                {
                    "source": "codex-jsonl",
                    "type": "tool",
                    "action": "read_git_state",
                    "detail": "git status --short",
                    "detail_sha256": CONTRACT_EVAL.text_hash("git status --short"),
                }
            ],
            "workspace": {
                "before_manifest": {},
                "after_manifest": {},
                "before_sha256": CONTRACT_EVAL.canonical_json_hash({}),
                "after_sha256": CONTRACT_EVAL.canonical_json_hash({}),
                "diff": "",
                "diff_sha256": CONTRACT_EVAL.text_hash(""),
                "changed_files": [],
            },
            "verifier": {
                "checks": [
                    {
                        "command": "git status --short",
                        "exit_code": 0,
                        "stdout": "clean",
                        "stdout_sha256": CONTRACT_EVAL.text_hash("clean"),
                        "passed": True,
                        "evidence": ["git_state"],
                    }
                ]
            },
        }

        CONTRACT_EVAL._validate_execution_trace(raw, result_id="workflow-test")

        invalid_verifier = copy.deepcopy(raw)
        invalid_verifier["verifier"]["checks"][0]["exit_code"] = 1
        with self.assertRaisesRegex(ValueError, "cannot pass with nonzero exit_code"):
            CONTRACT_EVAL._validate_execution_trace(
                invalid_verifier, result_id="workflow-test"
            )

        raw["observations"]["observed_actions"] = ["write_file"]
        with self.assertRaisesRegex(ValueError, "must match trace actions"):
            CONTRACT_EVAL._validate_execution_trace(raw, result_id="workflow-test")

    def test_result_bundle_rejects_uncommitted_skill_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            payload["skill_revision"] = "0" * 40
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "skill_revision"):
                CONTRACT_EVAL.load_result_bundle(bundle_path, {"case-001"}, dataset)

    def test_result_bundle_rejects_stale_dataset_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            payload["dataset_revision"] = "0" * 64
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "dataset_revision"):
                CONTRACT_EVAL.load_result_bundle(bundle_path, {"case-001"}, dataset)

    def test_result_bundle_rejects_invalid_capture_date(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            payload["captured_at"] = "not-a-date"
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "captured_at"):
                CONTRACT_EVAL.load_result_bundle(bundle_path, {"case-001"}, dataset)

    def test_result_bundle_requires_complete_true(self) -> None:
        for mode, expected_error in (
            ("missing", "missing metadata.*complete"),
            ("false", "complete must be true"),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                dataset = root / "dataset.jsonl"
                dataset.write_text(
                    '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                    '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                    encoding="utf-8",
                )
                bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
                if mode == "missing":
                    del payload["complete"]
                else:
                    payload["complete"] = False
                bundle_path.write_text(json.dumps(payload), encoding="utf-8")

                with self.assertRaisesRegex(ValueError, expected_error):
                    CONTRACT_EVAL.load_result_bundle(
                        bundle_path, {"case-001"}, dataset
                    )

    def test_result_bundle_binds_capture_to_raw_timeline(self) -> None:
        for mode, expected_error in (
            ("raw-after-capture", "captured_at predates raw evidence completion"),
            ("stale-capture", "follows raw evidence completion by more than"),
            ("future-raw", "raw interval 0 timestamp.*future"),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                dataset = root / "dataset.jsonl"
                dataset.write_text(
                    '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                    '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                    encoding="utf-8",
                )
                bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
                result = payload["results"][0]
                raw_path = root / result["raw_evidence"]
                raw = json.loads(raw_path.read_text(encoding="utf-8"))
                now = datetime.now(timezone.utc)
                if mode == "raw-after-capture":
                    raw_time = now
                    captured = now - timedelta(seconds=1)
                elif mode == "stale-capture":
                    raw_time = now - timedelta(
                        seconds=CONTRACT_EVAL.MAXIMUM_CLOCK_SKEW_SECONDS + 1
                    )
                    captured = now
                else:
                    raw_time = now + timedelta(
                        seconds=CONTRACT_EVAL.MAXIMUM_CLOCK_SKEW_SECONDS + 10
                    )
                    captured = now
                raw_timestamp = raw_time.isoformat()
                raw["started_at"] = raw_timestamp
                raw["completed_at"] = raw_timestamp
                raw["host_attempts"][0]["started_at"] = raw_timestamp
                raw["host_attempts"][0]["completed_at"] = raw_timestamp
                raw_path.write_text(json.dumps(raw), encoding="utf-8")
                result["raw_evidence_sha256"] = hashlib.sha256(
                    raw_path.read_bytes()
                ).hexdigest()
                payload["captured_at"] = captured.isoformat()
                bundle_path.write_text(json.dumps(payload), encoding="utf-8")

                with self.assertRaisesRegex(ValueError, expected_error):
                    CONTRACT_EVAL.load_result_bundle(
                        bundle_path, {"case-001"}, dataset
                    )

    def test_formal_attempt_interval_rejects_invalid_or_future_timestamps(self) -> None:
        now = datetime.now(timezone.utc)
        latest_allowed = now + timedelta(
            seconds=CONTRACT_EVAL.MAXIMUM_CLOCK_SKEW_SECONDS
        )
        cases = (
            (
                {"started_at": "not-a-date", "completed_at": now.isoformat()},
                "started_at must be an ISO-8601 timestamp",
            ),
            (
                {
                    "started_at": now.isoformat(),
                    "completed_at": (now - timedelta(seconds=1)).isoformat(),
                },
                "completed_at predates started_at",
            ),
            (
                {
                    "started_at": (
                        latest_allowed + timedelta(seconds=1)
                    ).isoformat(),
                    "completed_at": (
                        latest_allowed + timedelta(seconds=2)
                    ).isoformat(),
                },
                "timestamp is more than.*future",
            ),
        )
        for attempt, expected_error in cases:
            with self.subTest(attempt=attempt), self.assertRaisesRegex(
                ValueError, expected_error
            ):
                CONTRACT_EVAL._validate_attempt_interval(
                    attempt,
                    label="formal attempt",
                    latest_allowed=latest_allowed,
                )

    def test_held_out_timeline_binds_attempt_raw_and_capture_boundaries(self) -> None:
        now = datetime.now(timezone.utc)
        maximum_skew = timedelta(
            seconds=CONTRACT_EVAL.MAXIMUM_CLOCK_SKEW_SECONDS
        )
        raw_intervals = [
            (now + timedelta(seconds=1), now + timedelta(seconds=10)),
            (now + timedelta(minutes=10), now + timedelta(minutes=11)),
        ]
        captured = now + timedelta(minutes=11, seconds=1)
        attempt = (now, captured + timedelta(seconds=1))

        CONTRACT_EVAL._validate_result_timeline(
            label="held-out",
            captured_at=captured,
            raw_intervals=raw_intervals,
            latest_allowed=now + timedelta(hours=1),
            attempt_interval=attempt,
        )

        invalid_timelines = (
            (
                (now + timedelta(seconds=2), attempt[1]),
                raw_intervals,
                captured,
                "formal attempt starts after raw evidence",
            ),
            (
                (now - maximum_skew - timedelta(seconds=1), attempt[1]),
                raw_intervals,
                captured,
                "first raw evidence follows formal attempt start by more than",
            ),
            (
                attempt,
                raw_intervals,
                attempt[1] + timedelta(seconds=1),
                "captured_at follows formal attempt completion",
            ),
            (
                (now, captured + maximum_skew + timedelta(seconds=1)),
                raw_intervals,
                captured,
                "formal attempt completion follows captured_at by more than",
            ),
        )
        for attempt_interval, intervals, capture_time, expected_error in invalid_timelines:
            with self.subTest(expected_error=expected_error), self.assertRaisesRegex(
                ValueError, expected_error
            ):
                CONTRACT_EVAL._validate_result_timeline(
                    label="held-out",
                    captured_at=capture_time,
                    raw_intervals=intervals,
                    latest_allowed=now + timedelta(hours=1),
                    attempt_interval=attempt_interval,
                )

    def test_result_bundle_rejects_missing_or_changed_raw_evidence(self) -> None:
        for mode in ("missing", "changed"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                dataset = root / "dataset.jsonl"
                dataset.write_text(
                    '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                    '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                    encoding="utf-8",
                )
                bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
                result = payload["results"][0]
                if mode == "missing":
                    result["raw_evidence"] = "raw/missing.json"
                else:
                    result["raw_evidence_sha256"] = "0" * 64
                bundle_path.write_text(json.dumps(payload), encoding="utf-8")

                with self.assertRaisesRegex(ValueError, "raw_evidence"):
                    CONTRACT_EVAL.load_result_bundle(
                        bundle_path, {"case-001"}, dataset
                    )

    def test_result_bundle_binds_invocation_prompt_to_template_and_dataset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["invocation_prompt"] = "Different wrapper for the same request"
            raw["invocation_prompt_sha256"] = CONTRACT_EVAL.text_hash(
                raw["invocation_prompt"]
            )
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "does not match prompt_template"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_result_bundle_binds_metrics_to_raw_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["metrics"]["duration_ms"] = 2
            raw["host_attempts"][0]["duration_ms"] = 2
            raw["host_attempts"][0]["metrics"]["duration_ms"] = 2
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "metrics mirror"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_result_bundle_accepts_auditable_capacity_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            retry_started = datetime.now(timezone.utc)
            first_completed = retry_started + timedelta(milliseconds=1)
            second_started = first_completed + timedelta(seconds=5)
            second_completed = second_started + timedelta(milliseconds=1)
            capacity_stdout = json.dumps(
                {
                    "type": "error",
                    "message": (
                        "Selected model is at capacity. "
                        "Please try a different model."
                    ),
                }
            )
            capacity_transcript = f"STDOUT\n{capacity_stdout}\nSTDERR\n"
            first_attempt = {
                "attempt_index": 1,
                "started_at": retry_started.isoformat(),
                "completed_at": first_completed.isoformat(),
                "duration_ms": 1,
                "exit_code": 1,
                "stdout": capacity_stdout,
                "stderr": "",
                "response": "",
                "model_output": "",
                "transcript": capacity_transcript,
                "transcript_sha256": CONTRACT_EVAL.text_hash(
                    capacity_transcript
                ),
                "error_class": "model_capacity",
                "error": "host exited with code 1",
                "retryable": True,
                "backoff_seconds_before_next": 5,
                "observations": None,
                "metrics": {
                    "duration_ms": 1,
                    "input_tokens": None,
                    "output_tokens": None,
                },
            }
            terminal_attempt = raw["host_attempts"][0]
            terminal_attempt["attempt_index"] = 2
            terminal_attempt["started_at"] = second_started.isoformat()
            terminal_attempt["completed_at"] = second_completed.isoformat()
            raw["host_attempts"] = [first_attempt, terminal_attempt]
            raw["started_at"] = retry_started.isoformat()
            raw["completed_at"] = second_completed.isoformat()
            raw["metrics"]["duration_ms"] = 5002
            raw["metrics"]["attempt_count"] = 2
            raw["metrics"]["retry_count"] = 1
            result["metrics"] = dict(raw["metrics"])
            payload["captured_at"] = (
                second_completed + timedelta(milliseconds=1)
            ).isoformat()
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            loaded = CONTRACT_EVAL.load_result_bundle(
                bundle_path, {"case-001"}, dataset
            )

            self.assertEqual(2, loaded["results"][0]["metrics"]["attempt_count"])
            self.assertEqual(1, loaded["results"][0]["metrics"]["retry_count"])

            for mode, expected_error in (
                ("hidden-valid-result", "result does not match host response"),
                ("missing-backoff", "omits the canonical retry backoff"),
            ):
                with self.subTest(mode=mode):
                    changed = copy.deepcopy(raw)
                    if mode == "hidden-valid-result":
                        valid_route = json.dumps(
                            {"actual_owner": "diagnose", "handoffs": []}
                        )
                        changed["host_attempts"][0]["response"] = valid_route
                        changed["host_attempts"][0]["model_output"] = valid_route
                    else:
                        changed["host_attempts"][1]["started_at"] = changed[
                            "host_attempts"
                        ][0]["completed_at"]
                    raw_path.write_text(json.dumps(changed), encoding="utf-8")
                    result["raw_evidence_sha256"] = hashlib.sha256(
                        raw_path.read_bytes()
                    ).hexdigest()
                    bundle_path.write_text(json.dumps(payload), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, expected_error):
                        CONTRACT_EVAL.load_result_bundle(
                            bundle_path, {"case-001"}, dataset
                        )

    def test_result_bundle_rejects_noncanonical_retry_backoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["host_attempts"][0]["backoff_seconds_before_next"] = 5
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "backoff_seconds.*canonical"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_result_bundle_rejects_zero_token_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["metrics"]["input_tokens"] = 0
            raw["host_attempts"][0]["metrics"]["input_tokens"] = 0
            result["metrics"]["input_tokens"] = 0
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "null or a positive integer"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_result_bundle_recomputes_claude_cache_inclusive_usage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            payload["run_config"]["host_name"] = "claude"
            payload["run_config"]["host_config_sha256"] = (
                CONTRACT_EVAL.PROTOCOL.canonical_hash(
                    CONTRACT_EVAL.PROTOCOL.canonical_host_policy(
                        "claude", payload["model"], CONTRACT_EVAL.CONTRACTS
                    )
                )
            )
            payload["run_config"]["environment_policy_sha256"] = (
                CONTRACT_EVAL.PROTOCOL.canonical_hash(
                    CONTRACT_EVAL.PROTOCOL.canonical_environment_policy(
                        "claude", CONTRACT_EVAL.CONTRACTS
                    )
                )
            )
            payload["run_config"]["retry_policy_sha256"] = (
                CONTRACT_EVAL.PROTOCOL.canonical_hash(
                    CONTRACT_EVAL.PROTOCOL.canonical_transient_retry_policy(
                        "claude", CONTRACT_EVAL.CONTRACTS
                    )
                )
            )
            result = payload["results"][0]
            raw_path = root / result["raw_evidence"]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["stdout"] = json.dumps(
                {
                    "usage": {
                        "input_tokens": 1,
                        "cache_creation_input_tokens": 2,
                        "cache_read_input_tokens": 3,
                        "output_tokens": 1,
                    }
                }
            )
            raw["transcript"] = (
                f"STDOUT\n{raw['stdout']}\nSTDERR\n{raw['stderr']}"
            )
            raw["transcript_sha256"] = CONTRACT_EVAL.text_hash(raw["transcript"])
            raw["retry_policy_sha256"] = payload["run_config"][
                "retry_policy_sha256"
            ]
            raw["host_attempts"][0]["stdout"] = raw["stdout"]
            raw["host_attempts"][0]["transcript"] = raw["transcript"]
            raw["host_attempts"][0]["transcript_sha256"] = raw[
                "transcript_sha256"
            ]
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            result["raw_evidence_sha256"] = hashlib.sha256(
                raw_path.read_bytes()
            ).hexdigest()
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "normalized usage"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_result_bundle_rejects_pre_token_fix_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset = root / "dataset.jsonl"
            dataset.write_text(
                '{"id":"case-001","prompt":"fixture prompt","kind":"trigger",'
                '"expected_owner":"diagnose","forbidden_owners":[]}\n',
                encoding="utf-8",
            )
            bundle_path, payload = self.write_result_bundle_fixture(root, dataset)
            payload["schema_version"] = 2
            bundle_path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "schema_version must be 6"):
                CONTRACT_EVAL.load_result_bundle(
                    bundle_path, {"case-001"}, dataset
                )

    def test_held_out_provenance_rejects_canonicalized_historical_prompt(self) -> None:
        skill_revision = "a" * 40
        dataset_revision = "b" * 40
        with tempfile.TemporaryDirectory(dir=CONTRACT_EVAL.ROOT / "evals") as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh-id","prompt":"  ALREADY\\tPUBLIC  "}\n',
                encoding="utf-8",
            )
            relative = dataset.relative_to(CONTRACT_EVAL.ROOT).as_posix()
            provenance = Path(temp_dir) / "held-out-provenance.json"
            provenance_payload = {
                "schema_version": 1,
                "dataset_path": relative,
                "dataset_sha256": CONTRACT_EVAL.dataset_hash(dataset),
                "source_skill_revision": skill_revision,
                "authorship": {
                    "independent": True,
                    "timing": "post_freeze",
                    "existing_eval_comparison": "after_drafting_only",
                },
                "used_for_tuning": False,
                "intended_hosts": ["codex"],
            }
            provenance.write_text(json.dumps(provenance_payload), encoding="utf-8")
            provenance_relative = provenance.relative_to(
                CONTRACT_EVAL.ROOT
            ).as_posix()

            def git_result(command: list[str], **kwargs: object):
                if "merge-base" in command:
                    return subprocess.CompletedProcess(command, 0, b"", b"")
                if "log" in command:
                    return subprocess.CompletedProcess(
                        command, 0, f"{dataset_revision}\n", ""
                    )
                if "ls-tree" in command:
                    return subprocess.CompletedProcess(
                        command, 0, "evals/routing.jsonl\n", ""
                    )
                if "show" in command:
                    revision_path = command[-1]
                    if revision_path == f"{dataset_revision}:{relative}":
                        return subprocess.CompletedProcess(
                            command, 0, dataset.read_bytes(), b""
                        )
                    if revision_path == f"{dataset_revision}:{provenance_relative}":
                        return subprocess.CompletedProcess(
                            command, 0, provenance.read_bytes(), b""
                        )
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        '{"id":"old-id","prompt":"already public"}\n',
                        "",
                    )
                if "cat-file" in command and command[-1] in {
                    f"{skill_revision}:{relative}",
                    f"{skill_revision}:{provenance_relative}",
                }:
                    return subprocess.CompletedProcess(command, 1, b"", b"")
                return subprocess.CompletedProcess(command, 0, b"", b"")

            with mock.patch.object(
                CONTRACT_EVAL.subprocess, "run", side_effect=git_result
            ):
                with self.assertRaisesRegex(ValueError, "overlaps eval data"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        skill_revision,
                        {
                            "dataset_path": relative,
                            "dataset_git_revision": dataset_revision,
                            "evaluation_anchor_revision": skill_revision,
                            "held_out_provenance_path": provenance_relative,
                            "held_out_provenance_sha256": CONTRACT_EVAL.dataset_hash(
                                provenance
                            ),
                            "host_name": "codex",
                            "variant": "candidate",
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_skill_eval_case_prompt(self) -> None:
        skill_revision = "a" * 40
        dataset_revision = "b" * 40
        with tempfile.TemporaryDirectory(dir=CONTRACT_EVAL.ROOT / "evals") as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh-id","prompt":"known skill prompt"}\n',
                encoding="utf-8",
            )
            relative = dataset.relative_to(CONTRACT_EVAL.ROOT).as_posix()
            provenance = Path(temp_dir) / "held-out-provenance.json"
            provenance_payload = {
                "schema_version": 1,
                "dataset_path": relative,
                "dataset_sha256": CONTRACT_EVAL.dataset_hash(dataset),
                "source_skill_revision": skill_revision,
                "authorship": {
                    "independent": True,
                    "timing": "post_freeze",
                    "existing_eval_comparison": "after_drafting_only",
                },
                "used_for_tuning": False,
                "intended_hosts": ["codex"],
            }
            provenance.write_text(json.dumps(provenance_payload), encoding="utf-8")
            provenance_relative = provenance.relative_to(
                CONTRACT_EVAL.ROOT
            ).as_posix()
            skill_eval_path = "skills/diagnose/references/eval-cases.md"

            def git_result(command: list[str], **kwargs: object):
                if "merge-base" in command:
                    return subprocess.CompletedProcess(command, 0, b"", b"")
                if "log" in command:
                    return subprocess.CompletedProcess(
                        command, 0, f"{dataset_revision}\n", ""
                    )
                if "ls-tree" in command:
                    output = (
                        f"{skill_eval_path}\n"
                        if command[-1] == "skills"
                        else ""
                    )
                    return subprocess.CompletedProcess(command, 0, output, "")
                if "show" in command:
                    revision_path = command[-1]
                    if revision_path == f"{dataset_revision}:{relative}":
                        return subprocess.CompletedProcess(
                            command, 0, dataset.read_bytes(), b""
                        )
                    if revision_path == f"{dataset_revision}:{provenance_relative}":
                        return subprocess.CompletedProcess(
                            command, 0, provenance.read_bytes(), b""
                        )
                    if revision_path == f"{skill_revision}:{skill_eval_path}":
                        return subprocess.CompletedProcess(
                            command,
                            0,
                            "| Input | Expected |\n"
                            "| --- | --- |\n"
                            "| `Known   Skill Prompt` | Trigger |\n",
                            "",
                        )
                if "cat-file" in command and command[-1] in {
                    f"{skill_revision}:{relative}",
                    f"{skill_revision}:{provenance_relative}",
                }:
                    return subprocess.CompletedProcess(command, 1, b"", b"")
                return subprocess.CompletedProcess(command, 0, b"", b"")

            with mock.patch.object(
                CONTRACT_EVAL.subprocess, "run", side_effect=git_result
            ):
                with self.assertRaisesRegex(ValueError, "overlaps eval data"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        skill_revision,
                        {
                            "dataset_path": relative,
                            "dataset_git_revision": dataset_revision,
                            "evaluation_anchor_revision": skill_revision,
                            "held_out_provenance_path": provenance_relative,
                            "held_out_provenance_sha256": CONTRACT_EVAL.dataset_hash(
                                provenance
                            ),
                            "host_name": "codex",
                            "variant": "candidate",
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_missing_variant(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            with mock.patch.object(
                CONTRACT_EVAL.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, b"", b""),
            ):
                with self.assertRaisesRegex(ValueError, "run_config.variant"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "a" * 40,
                        {
                            "dataset_git_revision": "b" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": "evals/provenance.json",
                            "held_out_provenance_sha256": "c" * 64,
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_candidate_anchor_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            with mock.patch.object(
                CONTRACT_EVAL.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, b"", b""),
            ):
                with self.assertRaisesRegex(ValueError, "must equal"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "b" * 40,
                        {
                            "variant": "candidate",
                            "dataset_git_revision": "c" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": "evals/provenance.json",
                            "held_out_provenance_sha256": "d" * 64,
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_nonancestor_previous(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            with mock.patch.object(
                CONTRACT_EVAL.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, b"", b""),
            ), mock.patch.object(
                CONTRACT_EVAL, "revision_is_ancestor", return_value=False
            ):
                with self.assertRaisesRegex(ValueError, "strict ancestor"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "b" * 40,
                        {
                            "variant": "previous",
                            "dataset_git_revision": "c" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": "evals/provenance.json",
                            "held_out_provenance_sha256": "d" * 64,
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=CONTRACT_EVAL.ROOT / "evals"
        ) as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            provenance = Path(temp_dir) / "provenance.json"
            provenance.write_text("{}\n", encoding="utf-8")
            dataset_relative = dataset.relative_to(CONTRACT_EVAL.ROOT).as_posix()
            provenance_relative = provenance.relative_to(
                CONTRACT_EVAL.ROOT
            ).as_posix()
            with mock.patch.object(
                CONTRACT_EVAL.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, b"", b""),
            ):
                with self.assertRaisesRegex(ValueError, "must match the provenance"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "a" * 40,
                        {
                            "variant": "candidate",
                            "dataset_path": dataset_relative,
                            "dataset_git_revision": "b" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": provenance_relative,
                            "held_out_provenance_sha256": "c" * 64,
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_tuning_use(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=CONTRACT_EVAL.ROOT / "evals"
        ) as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            dataset_relative = dataset.relative_to(CONTRACT_EVAL.ROOT).as_posix()
            provenance = Path(temp_dir) / "provenance.json"
            provenance.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "dataset_path": dataset_relative,
                        "dataset_sha256": CONTRACT_EVAL.dataset_hash(dataset),
                        "source_skill_revision": "a" * 40,
                        "authorship": {
                            "independent": True,
                            "timing": "post_freeze",
                            "existing_eval_comparison": "after_drafting_only",
                        },
                        "used_for_tuning": True,
                        "intended_hosts": ["codex"],
                    }
                ),
                encoding="utf-8",
            )
            provenance_relative = provenance.relative_to(
                CONTRACT_EVAL.ROOT
            ).as_posix()
            with mock.patch.object(
                CONTRACT_EVAL.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, b"", b""),
            ):
                with self.assertRaisesRegex(ValueError, "used_for_tuning"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "a" * 40,
                        {
                            "variant": "candidate",
                            "dataset_path": dataset_relative,
                            "dataset_git_revision": "b" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": provenance_relative,
                            "held_out_provenance_sha256": CONTRACT_EVAL.dataset_hash(
                                provenance
                            ),
                            "host_name": "codex",
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_held_out_provenance_rejects_retrofitted_history(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=CONTRACT_EVAL.ROOT / "evals"
        ) as temp_dir:
            dataset = Path(temp_dir) / "held-out.jsonl"
            dataset.write_text(
                '{"id":"fresh","prompt":"fresh prompt"}\n', encoding="utf-8"
            )
            dataset_relative = dataset.relative_to(CONTRACT_EVAL.ROOT).as_posix()
            provenance = Path(temp_dir) / "provenance.json"
            provenance.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "dataset_path": dataset_relative,
                        "dataset_sha256": CONTRACT_EVAL.dataset_hash(dataset),
                        "source_skill_revision": "a" * 40,
                        "authorship": {
                            "independent": True,
                            "timing": "post_freeze",
                            "existing_eval_comparison": "after_drafting_only",
                        },
                        "used_for_tuning": False,
                        "intended_hosts": ["codex"],
                    }
                ),
                encoding="utf-8",
            )
            provenance_relative = provenance.relative_to(
                CONTRACT_EVAL.ROOT
            ).as_posix()

            def git_result(command: list[str], **_kwargs: object):
                if "log" in command:
                    earlier = "c" * 40 if command[-1] == dataset_relative else "d" * 40
                    return subprocess.CompletedProcess(
                        command, 0, f"{'b' * 40}\n{earlier}\n", ""
                    )
                return subprocess.CompletedProcess(command, 0, b"", b"")

            with mock.patch.object(
                CONTRACT_EVAL.subprocess, "run", side_effect=git_result
            ):
                with self.assertRaisesRegex(ValueError, "never retrofitted"):
                    CONTRACT_EVAL._validate_held_out_provenance(
                        dataset,
                        "a" * 40,
                        {
                            "variant": "candidate",
                            "dataset_path": dataset_relative,
                            "dataset_git_revision": "b" * 40,
                            "evaluation_anchor_revision": "a" * 40,
                            "held_out_provenance_path": provenance_relative,
                            "held_out_provenance_sha256": CONTRACT_EVAL.dataset_hash(
                                provenance
                            ),
                            "host_name": "codex",
                        },
                        bundle_path=Path("fixture-bundle.json"),
                    )

    def test_authority_and_workflow_require_every_skill(self) -> None:
        known_skills = CONTRACT_EVAL.discover_skill_names()
        authority = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.AUTHORITY_DATA)
        workflow = CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.WORKFLOW_DATA)
        self.assertEqual(
            [], CONTRACT_EVAL.validate_authority_cases(authority, known_skills)
        )
        self.assertEqual(
            [], CONTRACT_EVAL.validate_workflow_cases(workflow, known_skills)
        )

        authority_without_frontend_audit = [
            case for case in authority if case["expected_owner"] != "audit-frontend"
        ]
        authority_errors = CONTRACT_EVAL.validate_authority_cases(
            authority_without_frontend_audit, known_skills
        )
        self.assertTrue(
            any("missing owner coverage for audit-frontend" in error for error in authority_errors)
        )

        workflow_without_map = [
            case for case in workflow if "repo-map" not in case["expected_route"]
        ]
        workflow_errors = CONTRACT_EVAL.validate_workflow_cases(
            workflow_without_map, known_skills
        )
        self.assertTrue(
            any("missing route coverage for repo-map" in error for error in workflow_errors)
        )

    def test_authority_and_workflow_minimums_are_not_exact_counts(self) -> None:
        known_skills = CONTRACT_EVAL.discover_skill_names()
        authority = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.AUTHORITY_DATA))
        extra_authority = copy.deepcopy(authority[-1])
        extra_authority["id"] = "authority-extra"
        extra_authority["prompt"] = "Produce one additional planning contract fixture."
        authority.append(extra_authority)
        workflow = copy.deepcopy(CONTRACT_EVAL.load_jsonl(CONTRACT_EVAL.WORKFLOW_DATA))
        extra_workflow = copy.deepcopy(workflow[-1])
        extra_workflow["id"] = "workflow-extra"
        extra_workflow["title"] = "Additional writing fixture"
        extra_workflow["prompt"] = "Rewrite one additional sourced engineering note."
        workflow.append(extra_workflow)

        self.assertEqual(
            [], CONTRACT_EVAL.validate_authority_cases(authority, known_skills)
        )
        self.assertEqual(
            [], CONTRACT_EVAL.validate_workflow_cases(workflow, known_skills)
        )

    def test_cli_validates_selected_authority_and_workflow_dataset_paths(self) -> None:
        for option in ("--authority-dataset", "--workflow-dataset"):
            with self.subTest(option=option), tempfile.TemporaryDirectory() as temp_dir:
                selected = Path(temp_dir) / "empty.jsonl"
                selected.write_text("", encoding="utf-8")
                with mock.patch.object(
                    sys,
                    "argv",
                    ["eval-skill-contracts.py", "--validate-only", option, str(selected)],
                ), mock.patch("builtins.print") as printed:
                    result = CONTRACT_EVAL.main()

                self.assertEqual(1, result)
                rendered = "\n".join(
                    " ".join(str(value) for value in call.args)
                    for call in printed.call_args_list
                )
                self.assertIn("FAIL", rendered)

    def test_local_link_validation_rejects_missing_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "sample-skill"
            package.mkdir()
            (package / "SKILL.md").write_text("[missing](references/missing.md)\n", encoding="utf-8")

            errors = validate_local_links(package, label="test")

        self.assertEqual(1, len(errors))
        self.assertIn("broken local link", errors[0])

    def test_skill_invocations_must_resolve_to_shipped_packages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "skills"
            alpha = root / "alpha"
            beta = root / "beta"
            alpha.mkdir(parents=True)
            beta.mkdir(parents=True)
            (alpha / "SKILL.md").write_text(
                "Shell examples may contain echo $target and tool $1.\n",
                encoding="utf-8",
            )
            (beta / "SKILL.md").write_text("No routed skill.\n", encoding="utf-8")
            (alpha / "agents").mkdir()
            (alpha / "agents" / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Use $beta, $missing-skill, and $diagnosse; run echo ${target} $1 and preserve this.$watch."\n',
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            errors = validate_skill_invocations(
                [packages[0]], known_skill_names={package.name for package in packages}
            )

        self.assertEqual(2, len(errors))
        self.assertTrue(any("unknown skill invocation $missing-skill" in error for error in errors))
        self.assertTrue(any("unknown skill invocation $diagnosse" in error for error in errors))
        self.assertFalse(any("unknown skill invocation $target" in error for error in errors))
        self.assertFalse(any("unknown skill invocation $watch" in error for error in errors))

    def test_implement_rust_requires_overlay_selection_eval(self) -> None:
        errors = self.specialized_contract_errors(
            "implement-rust", ("## Overlay Selection Eval", "## Removed Overlay Eval")
        )
        self.assertTrue(any("Overlay Selection Eval" in error for error in errors))

    def test_audit_rust_requires_every_scenario_field(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-rust", ("- **Validation:**", "- **Removed validation:**")
        )
        self.assertTrue(any("scenario 1 missing field 'Validation'" in error for error in errors))

    def test_audit_rust_allows_scenario_growth_or_reduction_above_minimum(self) -> None:
        path = (
            VALIDATOR_PATH.parents[1]
            / "skills"
            / "audit-rust"
            / "references"
            / "eval-cases.md"
        )
        original = path.read_text(encoding="utf-8")
        changed = re.sub(
            r"\n### 22\..*?(?=\n## Quality Eval)",
            "\n",
            original,
            count=1,
            flags=re.DOTALL,
        )
        self.assertNotEqual(original, changed)

        errors = validate_specialized_eval_contracts("audit-rust", changed, label="test")

        self.assertFalse(any("Scenario Eval must contain" in error for error in errors))

    def test_audit_rust_requires_out_of_scope_profile_rule(self) -> None:
        path = (
            VALIDATOR_PATH.parents[1]
            / "skills"
            / "audit-rust"
            / "references"
            / "eval-cases.md"
        )
        changed = path.read_text(encoding="utf-8").replace("Out of scope", "Excluded")
        errors = validate_specialized_eval_contracts("audit-rust", changed, label="test")
        self.assertTrue(any("Out of scope" in error for error in errors))

    def test_review_bridge_requires_split_package_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "chatgpt-review",
            ("| Split package artifact |", "| Removed split package artifact |"),
        )
        self.assertTrue(any("Split package artifact" in error for error in errors))

    def test_review_bridge_requires_artifact_visibility_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "chatgpt-review",
            ("| Review artifact visibility |", "| Removed artifact visibility |"),
        )
        self.assertTrue(any("Review artifact visibility" in error for error in errors))

    def test_audit_frontend_requires_framework_specific_scenarios(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-frontend", ("Pure Options API", "Removed API style")
        )
        self.assertTrue(any("Pure Options API" in error for error in errors))

    def test_repo_review_requires_immutable_basis_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "repo-review", ("| Immutable basis |", "| Removed basis |")
        )
        self.assertTrue(any("Immutable basis" in error for error in errors))

    def test_repo_map_requires_review_boundary_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "repo-map", ("| Context-versus-review boundary |", "| Removed review boundary |")
        )
        self.assertTrue(any("Context-versus-review boundary" in error for error in errors))

    def test_audit_security_requires_coordinator_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-security", ("| Scoped specialist boundary |", "| Removed handoff |")
        )
        self.assertTrue(any("Scoped specialist boundary" in error for error in errors))

    def test_ops_browser_requires_debug_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "ops-browser", ("| Browser debug handoff |", "| Removed debug handoff |")
        )
        self.assertTrue(any("Browser debug handoff" in error for error in errors))

    def test_ops_client_requires_debug_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "ops-client", ("| Client debug handoff |", "| Removed debug handoff |")
        )
        self.assertTrue(any("Client debug handoff" in error for error in errors))

    def test_every_declared_cross_artifact_term_is_mutation_protected(self) -> None:
        tested = 0
        declared = sum(
            len(terms)
            for _, _, _, terms in VALIDATOR.CROSS_ARTIFACT_TERM_REQUIREMENTS
        )
        for skill_name, surface, section, terms in VALIDATOR.CROSS_ARTIFACT_TERM_REQUIREMENTS:
            for term in terms:
                with self.subTest(skill=skill_name, surface=surface, term=term):
                    errors = self.cross_artifact_contract_errors(
                        skill_name, surface, term, section
                    )
                    self.assertTrue(any("missing contract terms" in error for error in errors))
                    tested += 1
        self.assertEqual(declared, tested)

    def test_browser_eval_route_reversal_is_rejected(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-browser"
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"), "default_prompt"
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] = surfaces["references/eval-cases.md"].replace(
            "Should prefer `diagnose`, which may delegate Browser Debug Evidence to `ops-browser`.",
            "Should trigger `ops-browser` directly.",
            1,
        )
        errors = validate_cross_artifact_contracts("ops-browser", surfaces, label="test")
        self.assertTrue(any("missing semantic terms" in error for error in errors))

    def test_client_eval_evidence_weakening_is_rejected(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-client"
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"), "default_prompt"
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] = surfaces["references/eval-cases.md"].replace(
            "deletes evidence before transfer",
            "deletes disposable state",
            1,
        )
        errors = validate_cross_artifact_contracts("ops-client", surfaces, label="test")
        self.assertTrue(any("missing semantic terms" in error for error in errors))

    def test_semantic_contradiction_is_rejected_with_required_terms_present(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-browser"
        yaml_text = (package / "agents" / "openai.yaml").read_text(encoding="utf-8")
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": yaml_text,
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(yaml_text, "default_prompt"),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] += (
            "\nContradiction: direct operation takes precedence over `diagnose`.\n"
        )
        errors = validate_cross_artifact_contracts("ops-browser", surfaces, label="test")
        self.assertTrue(any("contradictory contract phrase" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
