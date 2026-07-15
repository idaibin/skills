#!/usr/bin/env python3
"""Regression tests for the prompt-only native Skill routing runner."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("run-skill-routing-eval.py")
SPEC = importlib.util.spec_from_file_location("run_skill_routing_eval", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {SCRIPT}")
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUNNER
SPEC.loader.exec_module(RUNNER)


class RoutingRunnerTests(unittest.TestCase):
    def _revision(self):
        return RUNNER.GitRevision(commit="a" * 40, skills_tree="b" * 40)

    def _cases(self):
        return (
            RUNNER.EvalCase("case-one", "Route the first natural request."),
            RUNNER.EvalCase("case-two", "Route the second natural request."),
        )

    def _config(
        self, root: Path, *, host: str = "codex", variant: str = "candidate"
    ):
        dataset = root / "routing.jsonl"
        dataset.write_text(
            "\n".join(
                json.dumps({"id": case.case_id, "prompt": case.prompt})
                for case in self._cases()
            )
            + "\n",
            encoding="utf-8",
        )
        return RUNNER.RunConfig(
            host=host,
            variant=variant,
            trial=2,
            pair_id="00000000-0000-4000-8000-000000000002",
            held_out=True,
            model="test-model",
            timeout_seconds=20,
            concurrency=1,
            output_root=root / "output",
            dataset_path=dataset,
            dataset_path_relative="evals/routing-held-out.jsonl",
            dataset_sha256=hashlib.sha256(dataset.read_bytes()).hexdigest(),
            dataset_git_revision="d" * 40,
            evaluation_anchor_revision="a" * 40,
            held_out_provenance_path_relative="evals/routing-held-out-provenance.json",
            held_out_provenance_sha256="e" * 64,
            revision=self._revision(),
            cases=self._cases(),
        )

    @staticmethod
    def _fake_fixture(_revision, destination: Path) -> str:
        for owner in RUNNER.OWNER_ENUM:
            package = destination / owner
            package.mkdir(parents=True)
            (package / "SKILL.md").write_text(f"# {owner}\n", encoding="utf-8")
        return "c" * 64

    def test_prompt_contains_only_natural_request_and_fixed_owner_enum(self) -> None:
        case = {
            "id": "secret-case-id",
            "prompt": "Inspect this natural request without changing files.",
            "expected_owner": "repo-review",
            "forbidden_owners": ["repo-delivery"],
            "high_risk": True,
        }
        prompt = RUNNER.build_prompt(case["prompt"])

        self.assertIn(case["prompt"], prompt)
        for owner in RUNNER.OWNER_ENUM:
            self.assertIn(owner, prompt)
        for evaluator_key in ("expected_owner", "forbidden_owners", "high_risk", case["id"]):
            self.assertNotIn(evaluator_key, prompt)
        self.assertNotIn("correct owner", prompt.casefold())

    def test_runner_schema_versions_match_the_repository_contract(self) -> None:
        contract = json.loads(
            (RUNNER.ROOT / "contracts" / "skill-validation.json").read_text(
                encoding="utf-8"
            )
        )["behavior_eval"]

        self.assertEqual(
            contract["result_schema_version"], RUNNER.RESULT_SCHEMA_VERSION
        )
        self.assertEqual(
            contract["raw_evidence_schema_version"], RUNNER.RAW_SCHEMA_VERSION
        )
        self.assertEqual(
            contract["prompt_template_version"], RUNNER.PROMPT_TEMPLATE_VERSION
        )

    def test_default_mode_does_not_invoke_any_model_cli(self) -> None:
        revision = self._revision()
        stdout = io.StringIO()
        with mock.patch.object(
            RUNNER, "resolve_revision", return_value=revision
        ), mock.patch.object(RUNNER.subprocess, "run") as mocked_run, redirect_stdout(
            stdout
        ):
            return_code = RUNNER.main(
                [
                    "--host",
                    "codex",
                    "--variant",
                    "candidate",
                    "--model",
                    "test-model",
                    "--case",
                    "route-001",
                ]
            )

        self.assertEqual(0, return_code)
        mocked_run.assert_not_called()
        plan = json.loads(stdout.getvalue())
        self.assertFalse(plan["execute"])
        self.assertEqual("dry-run only; no model CLI was invoked", plan["note"])

    def test_execute_rejects_case_subset_before_any_model_cli(self) -> None:
        stderr = io.StringIO()
        with mock.patch.object(RUNNER.subprocess, "run") as mocked_run, redirect_stderr(
            stderr
        ):
            return_code = RUNNER.main(
                [
                    "--host",
                    "codex",
                    "--variant",
                    "candidate",
                    "--model",
                    "test-model",
                    "--case",
                    "route-001",
                    "--execute",
                ]
            )

        self.assertEqual(2, return_code)
        mocked_run.assert_not_called()
        self.assertIn("complete selected dataset", stderr.getvalue())

    def test_dataset_and_model_output_reject_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            dataset = Path(temporary) / "routing.jsonl"
            dataset.write_text(
                '{"id":"one","id":"two","prompt":"request"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RUNNER.RunnerError, "duplicate JSON key"):
                RUNNER._load_dataset_rows(dataset)

        self.assertIsNone(
            RUNNER._json_value(
                '{"actual_owner":"repo-map","actual_owner":"repo-review",'
                '"handoffs":[]}'
            )
        )

    def test_claude_usage_includes_cache_creation_and_read_tokens(self) -> None:
        stdout = json.dumps(
            {
                "usage": {
                    "input_tokens": 10,
                    "cache_creation_input_tokens": 20,
                    "cache_read_input_tokens": 30,
                    "output_tokens": 4,
                }
            }
        )
        self.assertEqual((60, 4), RUNNER._extract_usage(stdout, host="claude"))

    def test_claude_usage_treats_missing_or_null_cache_tokens_as_zero(self) -> None:
        missing = json.dumps(
            {"usage": {"input_tokens": 10, "output_tokens": 4}}
        )
        null = json.dumps(
            {
                "usage": {
                    "input_tokens": 10,
                    "cache_creation_input_tokens": None,
                    "cache_read_input_tokens": None,
                    "output_tokens": 4,
                }
            }
        )
        self.assertEqual((10, 4), RUNNER._extract_usage(missing, host="claude"))
        self.assertEqual((10, 4), RUNNER._extract_usage(null, host="claude"))

    def test_claude_usage_fails_closed_for_invalid_cache_tokens(self) -> None:
        for invalid in (True, -1, 1.5, "5"):
            with self.subTest(invalid=invalid):
                stdout = json.dumps(
                    {
                        "usage": {
                            "input_tokens": 10,
                            "cache_creation_input_tokens": invalid,
                            "output_tokens": 4,
                        }
                    }
                )
                self.assertEqual(
                    (None, None), RUNNER._extract_usage(stdout, host="claude")
                )

    def test_codex_usage_does_not_double_count_cached_input_subset(self) -> None:
        stdout = json.dumps(
            {
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 4,
                    "input_tokens_details": {"cached_tokens": 7},
                    "cache_creation_input_tokens": 20,
                    "cache_read_input_tokens": 30,
                }
            }
        )
        self.assertEqual((10, 4), RUNNER._extract_usage(stdout, host="codex"))

    def test_dataset_contract_selects_held_out_validator(self) -> None:
        validator = mock.Mock()
        validator.validate_held_out_routing_cases.return_value = []
        with mock.patch.object(
            RUNNER, "_contract_validator_module", return_value=validator
        ):
            RUNNER._validate_dataset_contract(
                Path("held-out.jsonl"), [], held_out=True
            )

        validator.validate_held_out_routing_cases.assert_called_once_with(
            [], set(RUNNER.OWNER_ENUM)
        )
        validator.validate_routing_cases.assert_not_called()

    def test_held_out_preflight_binds_variant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset = root / "held-out.jsonl"
            dataset.write_text(
                '{"id":"held-out-one","prompt":"Route this request."}\n',
                encoding="utf-8",
            )
            provenance = root / "provenance.json"
            provenance.write_text("{}\n", encoding="utf-8")
            validator = mock.Mock()
            arguments = RUNNER._build_parser().parse_args(
                [
                    "--host",
                    "codex",
                    "--variant",
                    "previous",
                    "--model",
                    "gpt-5-test",
                    "--held-out",
                    "--dataset",
                    str(dataset),
                    "--provenance",
                    str(provenance),
                    "--evaluation-anchor-revision",
                    "anchor",
                    "--skill-revision",
                    "previous",
                ]
            )
            with mock.patch.object(
                RUNNER,
                "_repository_dataset_path",
                return_value=(dataset, "evals/held-out.jsonl"),
            ), mock.patch.object(
                RUNNER,
                "_repository_provenance_path",
                return_value=(provenance, "evals/provenance.json"),
            ), mock.patch.object(
                RUNNER, "_validate_dataset_contract"
            ), mock.patch.object(
                RUNNER,
                "resolve_revision",
                return_value=RUNNER.GitRevision("b" * 40, "c" * 40),
            ), mock.patch.object(
                RUNNER, "_git_text", return_value="a" * 40
            ), mock.patch.object(
                RUNNER, "_committed_dataset_revision", return_value="d" * 40
            ), mock.patch.object(
                RUNNER, "_contract_validator_module", return_value=validator
            ):
                RUNNER._configuration_from_args(arguments)

            run_config = validator._validate_held_out_provenance.call_args.args[2]
            self.assertEqual("previous", run_config["variant"])

    def test_success_writes_schema_v3_bundle_and_unique_hashed_raw_v2(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self._config(root)
            invocation = 0

            def fake_subprocess(command, **kwargs):
                nonlocal invocation
                if command[:2] == ["git", "init"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command == ["codex", "--version"]:
                    return subprocess.CompletedProcess(command, 0, "codex-cli 9.9\n", "")
                self.assertEqual("codex", command[0])
                self.assertIn("--sandbox", command)
                self.assertIn("read-only", command)
                self.assertIn("--ephemeral", command)
                self.assertIn("--ignore-user-config", command)
                environment = kwargs["env"]
                self.assertNotEqual(os.environ.get("HOME"), environment["HOME"])
                self.assertTrue(Path(environment["HOME"]).is_dir())
                self.assertFalse((Path(environment["HOME"]) / ".agents" / "skills").exists())
                response_path = Path(command[command.index("--output-last-message") + 1])
                owner = RUNNER.OWNER_ENUM[invocation]
                invocation += 1
                response = {"actual_owner": owner, "handoffs": []}
                response_path.write_text(json.dumps(response), encoding="utf-8")
                stdout_value = json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {"input_tokens": 10 + invocation, "output_tokens": 2},
                    }
                )
                return subprocess.CompletedProcess(command, 0, stdout_value, "")

            with mock.patch.object(
                RUNNER,
                "_materialize_skill_fixture",
                side_effect=self._fake_fixture,
            ), mock.patch.object(
                RUNNER.subprocess, "run", side_effect=fake_subprocess
            ), mock.patch.object(
                RUNNER, "_validate_written_bundle"
            ):
                outcome = RUNNER.run_evaluation(config)
                baseline_root = root / "baseline-condition"
                baseline_root.mkdir()
                baseline_outcome = RUNNER.run_evaluation(
                    self._config(baseline_root, variant="baseline")
                )

            self.assertTrue(outcome.succeeded)
            self.assertTrue(baseline_outcome.succeeded)
            self.assertNotEqual(outcome.run_id, baseline_outcome.run_id)
            self.assertIsNotNone(outcome.bundle_path)
            bundle = json.loads(outcome.bundle_path.read_text(encoding="utf-8"))
            uuid.UUID(bundle["run_id"])
            self.assertEqual(3, bundle["schema_version"])
            self.assertTrue(bundle["complete"])
            self.assertEqual("evals/routing-held-out.jsonl", bundle["run_config"]["dataset_path"])
            self.assertEqual(config.pair_id, bundle["run_config"]["pair_id"])
            self.assertEqual(
                config.dataset_git_revision,
                bundle["run_config"]["dataset_git_revision"],
            )
            self.assertEqual(
                config.evaluation_anchor_revision,
                bundle["run_config"]["evaluation_anchor_revision"],
            )
            self.assertEqual("a" * 40, bundle["skill_revision"])
            self.assertEqual("b" * 40, bundle["skill_tree_sha"])
            self.assertEqual(
                RUNNER._task_fixture_hash(),
                bundle["run_config"]["fixture_sha256"],
            )
            self.assertEqual(
                RUNNER.TASK_FIXTURE_DESCRIPTOR,
                bundle["run_config"]["fixture"],
            )
            self.assertEqual(
                RUNNER._prompt_template(),
                bundle["run_config"]["prompt_template"],
            )
            self.assertEqual(
                "c" * 64, bundle["run_config"]["skill_fixture_sha256"]
            )
            self.assertTrue(bundle["run_config"]["skills_installed"])
            self.assertRegex(bundle["run_config"]["host_config_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual("deterministic", bundle["adjudication"]["method"])
            self.assertEqual("2", bundle["adjudication"]["reviewer_version"])
            self.assertRegex(bundle["adjudication"]["config_sha256"], r"^[0-9a-f]{64}$")

            evidence_paths = [item["raw_evidence"] for item in bundle["results"]]
            evidence_hashes = [item["raw_evidence_sha256"] for item in bundle["results"]]
            self.assertEqual(len(evidence_paths), len(set(evidence_paths)))
            self.assertEqual(len(evidence_hashes), len(set(evidence_hashes)))
            for result in bundle["results"]:
                raw_path = outcome.run_dir / result["raw_evidence"]
                self.assertEqual(
                    result["raw_evidence_sha256"],
                    hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                )
                raw = json.loads(raw_path.read_text(encoding="utf-8"))
                self.assertEqual(2, raw["schema_version"])
                self.assertEqual(0, raw["exit_code"])
                self.assertTrue(raw["stdout"])
                self.assertIn("stderr", raw)
                self.assertTrue(raw["response"])
                self.assertTrue(raw["model_output"])
                self.assertTrue(raw["transcript"])
                self.assertEqual(
                    raw["transcript_sha256"],
                    hashlib.sha256(raw["transcript"].encode("utf-8")).hexdigest(),
                )
                self.assertEqual(raw["observations"], json.loads(raw["model_output"]))

            baseline_bundle = json.loads(
                baseline_outcome.bundle_path.read_text(encoding="utf-8")
            )
            self.assertEqual(
                bundle["run_config"]["fixture_sha256"],
                baseline_bundle["run_config"]["fixture_sha256"],
            )
            self.assertIsNone(
                baseline_bundle["run_config"]["skill_fixture_sha256"]
            )
            self.assertFalse(baseline_bundle["run_config"]["skills_installed"])

    def test_claude_bundle_records_normalized_cache_inclusive_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self._config(root, host="claude")
            invocation = 0

            def fake_subprocess(command, **_kwargs):
                nonlocal invocation
                if command[:2] == ["git", "init"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command == ["claude", "--version"]:
                    return subprocess.CompletedProcess(
                        command, 0, "claude-code 9.9\n", ""
                    )
                owner = RUNNER.OWNER_ENUM[invocation]
                invocation += 1
                return subprocess.CompletedProcess(
                    command,
                    0,
                    json.dumps(
                        {
                            "structured_output": {
                                "actual_owner": owner,
                                "handoffs": [],
                            },
                            "usage": {
                                "input_tokens": 10,
                                "cache_creation_input_tokens": 20,
                                "cache_read_input_tokens": 30,
                                "output_tokens": 4,
                            },
                        }
                    ),
                    "",
                )

            with mock.patch.object(
                RUNNER,
                "_materialize_skill_fixture",
                side_effect=self._fake_fixture,
            ), mock.patch.object(
                RUNNER.subprocess, "run", side_effect=fake_subprocess
            ), mock.patch.object(RUNNER, "_validate_written_bundle"):
                outcome = RUNNER.run_evaluation(config)

            self.assertTrue(outcome.succeeded)
            bundle = json.loads(outcome.bundle_path.read_text(encoding="utf-8"))
            self.assertEqual(
                [60, 60],
                [result["metrics"]["input_tokens"] for result in bundle["results"]],
            )
            raw = json.loads(
                (outcome.run_dir / bundle["results"][0]["raw_evidence"]).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(60, raw["metrics"]["input_tokens"])
            self.assertIn('"cache_creation_input_tokens": 20', raw["stdout"])
            self.assertIn('"cache_read_input_tokens": 30', raw["stdout"])

    def test_failed_case_retains_raw_but_never_writes_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self._config(root)
            invocation = 0

            def fake_subprocess(command, **_kwargs):
                nonlocal invocation
                if command[:2] == ["git", "init"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                if command == ["codex", "--version"]:
                    return subprocess.CompletedProcess(command, 0, "codex-cli 9.9\n", "")
                invocation += 1
                if invocation == 2:
                    return subprocess.CompletedProcess(command, 7, "partial", "host failure")
                response_path = Path(command[command.index("--output-last-message") + 1])
                response_path.write_text(
                    json.dumps({"actual_owner": "repo-map", "handoffs": []}),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, "{}", "")

            with mock.patch.object(
                RUNNER,
                "_materialize_skill_fixture",
                side_effect=self._fake_fixture,
            ), mock.patch.object(
                RUNNER.subprocess, "run", side_effect=fake_subprocess
            ):
                outcome = RUNNER.run_evaluation(config)

            self.assertFalse(outcome.succeeded)
            self.assertIsNone(outcome.bundle_path)
            self.assertFalse((outcome.run_dir / "routing-results.json").exists())
            self.assertTrue(outcome.failure_path.is_file())
            failure = json.loads(outcome.failure_path.read_text(encoding="utf-8"))
            self.assertFalse(failure["complete"])
            self.assertEqual(["case-two"], [item["id"] for item in failure["failed_cases"]])
            self.assertEqual(2, len(list((outcome.run_dir / "raw" / "routing").glob("*.json"))))

    def test_previous_installs_committed_fixture_and_baseline_stays_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / "fixture"
            self._fake_fixture(self._revision(), fixture)

            with mock.patch.object(
                RUNNER.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "", ""),
            ):
                previous_root = RUNNER._prepare_case_repo(
                    root / "previous",
                    host="claude",
                    variant="previous",
                    skill_fixture=fixture,
                )
                baseline_root = RUNNER._prepare_case_repo(
                    root / "baseline",
                    host="claude",
                    variant="baseline",
                    skill_fixture=None,
                )

            self.assertEqual(
                ".claude/skills",
                previous_root.relative_to(root / "previous").as_posix(),
            )
            self.assertEqual(
                set(RUNNER.OWNER_ENUM),
                {path.name for path in previous_root.iterdir()},
            )
            self.assertFalse(baseline_root.exists())

    def test_real_committed_fixture_hash_matches_production_loader(self) -> None:
        revision = RUNNER.resolve_revision("HEAD")
        validator = RUNNER._contract_validator_module()
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            destination.mkdir()
            runner_hash = RUNNER._materialize_skill_fixture(revision, destination)

        self.assertEqual(
            validator.committed_skill_fixture_hash(revision.commit), runner_hash
        )

    def test_isolated_environment_copies_only_host_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_home = root / "source-home"
            codex_home = source_home / ".codex"
            claude_home = source_home / ".claude"
            (source_home / ".agents" / "skills" / "global-skill").mkdir(
                parents=True
            )
            (codex_home / "skills" / "global-skill").mkdir(parents=True)
            (claude_home / "skills" / "global-skill").mkdir(parents=True)
            (codex_home / "auth.json").write_text("codex-auth", encoding="utf-8")
            (codex_home / "config.toml").write_text("model='global'", encoding="utf-8")
            (claude_home / ".credentials.json").write_text(
                "claude-auth", encoding="utf-8"
            )
            (claude_home / "settings.json").write_text("{}", encoding="utf-8")

            environment = {
                "HOME": str(source_home),
                "CODEX_HOME": str(codex_home),
                "CLAUDE_CONFIG_DIR": str(claude_home),
            }
            with mock.patch.dict(os.environ, environment, clear=False):
                codex_environment = RUNNER._isolated_host_environment(
                    "codex", root / "codex-isolated"
                )
                claude_environment = RUNNER._isolated_host_environment(
                    "claude", root / "claude-isolated"
                )

            isolated_codex = Path(codex_environment["CODEX_HOME"])
            isolated_claude = Path(claude_environment["CLAUDE_CONFIG_DIR"])
            self.assertEqual("codex-auth", (isolated_codex / "auth.json").read_text())
            self.assertFalse((isolated_codex / "config.toml").exists())
            self.assertFalse((isolated_codex / "skills").exists())
            self.assertFalse(
                (Path(codex_environment["HOME"]) / ".agents" / "skills").exists()
            )
            self.assertEqual(
                "claude-auth",
                (isolated_claude / ".credentials.json").read_text(),
            )
            self.assertFalse((isolated_claude / "settings.json").exists())
            self.assertFalse((isolated_claude / "skills").exists())

    def test_success_path_self_validates_with_real_evaluator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset = root / "routing-integration.jsonl"
            prompt = "Inspect the repository layout and identify the owning module."
            dataset.write_text(
                json.dumps(
                    {
                        "id": "integration-one",
                        "prompt": prompt,
                        "kind": "neighbor_non_trigger",
                        "expected_owner": "repo-map",
                        "allowed_owners": ["repo-map"],
                        "forbidden_owners": [],
                        "high_risk": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            revision = RUNNER.resolve_revision("HEAD")
            config = RUNNER.RunConfig(
                host="codex",
                variant="candidate",
                trial=1,
                pair_id="00000000-0000-4000-8000-000000000010",
                held_out=False,
                model="gpt-5-test",
                timeout_seconds=20,
                concurrency=1,
                output_root=root / "output",
                dataset_path=dataset,
                dataset_path_relative=dataset.name,
                dataset_sha256=hashlib.sha256(dataset.read_bytes()).hexdigest(),
                dataset_git_revision=None,
                evaluation_anchor_revision=None,
                held_out_provenance_path_relative=None,
                held_out_provenance_sha256=None,
                revision=revision,
                cases=(RUNNER.EvalCase("integration-one", prompt),),
            )
            real_run = subprocess.run

            def host_or_git(command, **kwargs):
                if command[0] == "git":
                    return real_run(command, **kwargs)
                if command == ["codex", "--version"]:
                    return subprocess.CompletedProcess(
                        command, 0, "codex-cli 9.9\n", ""
                    )
                response_path = Path(
                    command[command.index("--output-last-message") + 1]
                )
                response_path.write_text(
                    json.dumps({"actual_owner": "repo-map", "handoffs": []}),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(
                    command,
                    0,
                    json.dumps(
                        {
                            "type": "turn.completed",
                            "usage": {"input_tokens": 10, "output_tokens": 2},
                        }
                    ),
                    "",
                )

            with mock.patch.object(
                RUNNER.subprocess, "run", side_effect=host_or_git
            ), mock.patch.object(RUNNER, "_copy_auth_file"):
                outcome = RUNNER.run_evaluation(config)

            self.assertTrue(outcome.succeeded)
            self.assertTrue(outcome.bundle_path.is_file())


if __name__ == "__main__":
    unittest.main()
