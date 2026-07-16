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
            comparison_group_id="00000000-0000-4000-8000-000000000002",
            campaign_id="00000000-0000-4000-8000-000000000099",
            campaign_path_relative="evals/routing-campaign.json",
            campaign_sha256="f" * 64,
            evaluation_protocol_revision="a" * 40,
            evaluation_protocol_sha256="9" * 64,
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

    def _invoke_one_case_with_host_responses(
        self, root: Path, responses, *, sleep_side_effect=None
    ):
        """Invoke one case without a real host while retaining raw attempts."""

        config = self._config(root)
        case = config.cases[0]
        raw_root = root / "raw"
        raw_root.mkdir()
        invocations = []

        def fake_prepare(case_root: Path, **_kwargs):
            case_root.mkdir(parents=True)
            return case_root

        def fake_environment(_host: str, isolated_home: Path):
            isolated_home.mkdir(parents=True)
            return {"HOME": str(isolated_home)}

        def fake_subprocess(command, **kwargs):
            index = len(invocations)
            if index >= len(responses):
                self.fail("runner exceeded the expected host invocation count")
            response = responses[index]
            invocations.append(
                {
                    "cwd": Path(kwargs["cwd"]),
                    "home": Path(kwargs["env"]["HOME"]),
                }
            )
            model_response = response.get("response")
            if model_response is not None:
                response_path = Path(
                    command[command.index("--output-last-message") + 1]
                )
                response_path.write_text(
                    json.dumps(model_response), encoding="utf-8"
                )
            return subprocess.CompletedProcess(
                command,
                response.get("exit_code", 1),
                response.get("stdout", ""),
                response.get("stderr", ""),
            )

        sleep = mock.Mock(side_effect=sleep_side_effect)
        with mock.patch.object(
            RUNNER, "_prepare_case_repo", side_effect=fake_prepare
        ), mock.patch.object(
            RUNNER, "_isolated_host_environment", side_effect=fake_environment
        ), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=fake_subprocess
        ), mock.patch.object(
            RUNNER.time, "sleep", sleep
        ):
            outcome = RUNNER._invoke_case(
                config,
                case,
                run_id="00000000-0000-4000-8000-000000000123",
                host_version="codex-cli 9.9",
                temp_root=root / "temporary",
                skill_fixture=None,
                raw_root=raw_root,
            )

        raw = json.loads(outcome.raw_path.read_text(encoding="utf-8"))
        return outcome, raw, invocations, sleep

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
        self.assertIn("responsible for the requested outcome", prompt)
        self.assertIn("authorization boundary", prompt)
        self.assertIn("next externally meaningful state", prompt)
        self.assertIn("must actually execute a bounded part", prompt)
        self.assertIn("clearly requested subsequent phase", prompt)
        self.assertIn("optional recommendations", prompt)
        self.assertIn("alternatives", prompt)
        self.assertIn("unrequested future work", prompt)
        self.assertIn("return an empty handoffs array", prompt)

    def test_codex_policy_disables_remote_plugin_and_records_isolation(self) -> None:
        policy = RUNNER._host_policy("codex", "gpt-5-test")
        command = policy["command_template"]

        disable_index = command.index("--disable")
        self.assertEqual("remote_plugin", command[disable_index + 1])
        self.assertIn("remote-plugin-disabled", policy["permissions"])
        self.assertEqual(
            "disabled by explicit Codex CLI feature override",
            policy["environment_isolation"]["remote_plugin"],
        )

    def test_canonical_command_template_matches_executed_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for host in ("codex", "claude"):
                host_root = root / host
                host_root.mkdir()
                config = self._config(host_root, host=host)
                repo = root / f"{host}-repo"
                schema = root / f"{host}-schema.json"
                response = root / f"{host}-response.json"
                prompt = "label-free prompt"
                actual = RUNNER._host_command(
                    config,
                    repo=repo,
                    schema_path=schema,
                    response_path=response,
                    prompt=prompt,
                )
                replacements = {
                    "<CASE_REPO>": str(repo),
                    "<MODEL>": config.model,
                    "<SCHEMA_PATH>": str(schema),
                    "<RESPONSE_PATH>": str(response),
                    "<LABEL_FREE_PROMPT>": prompt,
                    "<RESPONSE_SCHEMA>": RUNNER._canonical_json(
                        RUNNER.ROUTING_RESPONSE_SCHEMA
                    ),
                    "<EMPTY>": "",
                }
                expected = [replacements.get(item, item) for item in RUNNER._host_policy(
                    host, config.model
                )["command_template"]]
                self.assertEqual(expected, actual)

    def test_response_schema_uses_openai_supported_subset_and_parser_enforces_uniqueness(
        self,
    ) -> None:
        encoded_schema = json.dumps(RUNNER.ROUTING_RESPONSE_SCHEMA)
        self.assertNotIn("uniqueItems", encoded_schema)
        self.assertNotIn('"$schema"', encoded_schema)
        self.assertIsNone(
            RUNNER._routing_object(
                {
                    "actual_owner": "repo-map",
                    "handoffs": ["repo-review", "repo-review"],
                }
            )
        )

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
        self.assertEqual(
            "00000000-0000-4000-8000-000000000000",
            plan["comparison_group_id"],
        )
        self.assertNotIn("pair_id", plan)
        self.assertEqual("dry-run only; no model CLI was invoked", plan["note"])

    def test_comparison_group_cli_accepts_only_v2_flag(self) -> None:
        group_id = "00000000-0000-4000-8000-000000000005"
        arguments = RUNNER._build_parser().parse_args(
            [
                "--host",
                "codex",
                "--variant",
                "candidate",
                "--model",
                "gpt-5-test",
                "--comparison-group-id",
                group_id,
            ]
        )

        self.assertEqual(group_id, arguments.comparison_group_id)
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            RUNNER._build_parser().parse_args(
                [
                    "--host",
                    "codex",
                    "--variant",
                    "candidate",
                    "--model",
                    "gpt-5-test",
                    "--pair-id",
                    group_id,
                ]
            )

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

    def test_usage_requires_positive_input_and_output_tokens(self) -> None:
        for usage in (
            {"input_tokens": 0, "output_tokens": 4},
            {"input_tokens": 10, "output_tokens": 0},
        ):
            with self.subTest(usage=usage):
                self.assertEqual(
                    (None, None),
                    RUNNER._extract_usage(json.dumps({"usage": usage}), host="codex"),
                )

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

    def test_success_writes_schema_v6_bundle_and_unique_hashed_raw_v3(self) -> None:
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
                disable_index = command.index("--disable")
                self.assertEqual("remote_plugin", command[disable_index + 1])
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
            self.assertEqual(6, bundle["schema_version"])
            self.assertTrue(bundle["complete"])
            self.assertEqual("evals/routing-held-out.jsonl", bundle["run_config"]["dataset_path"])
            self.assertEqual(
                config.comparison_group_id,
                bundle["run_config"]["comparison_group_id"],
            )
            self.assertNotIn("pair_id", bundle["run_config"])
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
            self.assertIn(
                "remote_plugin disabled", bundle["run_config"]["isolation"]
            )
            self.assertIn(
                "remote-plugin-disabled", bundle["run_config"]["permissions"]
            )
            self.assertRegex(bundle["run_config"]["host_config_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(
                bundle["run_config"]["retry_policy_sha256"], r"^[0-9a-f]{64}$"
            )
            self.assertEqual("deterministic", bundle["adjudication"]["method"])
            self.assertEqual("6", bundle["adjudication"]["reviewer_version"])
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
                self.assertEqual(3, raw["schema_version"])
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
                self.assertEqual(1, raw["metrics"]["attempt_count"])
                self.assertEqual(0, raw["metrics"]["retry_count"])
                self.assertEqual(1, result["metrics"]["attempt_count"])
                self.assertEqual(0, result["metrics"]["retry_count"])
                self.assertEqual(
                    bundle["run_config"]["retry_policy_sha256"],
                    raw["retry_policy_sha256"],
                )
                self.assertEqual(1, len(raw["host_attempts"]))
                host_attempt = raw["host_attempts"][0]
                self.assertEqual(1, host_attempt["attempt_index"])
                self.assertFalse(host_attempt["retryable"])
                self.assertEqual(0, host_attempt["backoff_seconds_before_next"])
                self.assertEqual(raw["stdout"], host_attempt["stdout"])
                self.assertEqual(raw["observations"], host_attempt["observations"])

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

    def test_exact_codex_capacity_then_success_retries_once_with_fresh_isolation(
        self,
    ) -> None:
        capacity = "\n".join(
            (
                json.dumps({"type": "thread.started"}),
                json.dumps(
                    {
                        "type": "error",
                        "message": (
                            "Selected model is at capacity. "
                            "Please try a different model."
                        ),
                    }
                ),
                json.dumps(
                    {
                        "type": "turn.failed",
                        "error": {
                            "message": (
                                "Selected model is at capacity. "
                                "Please try a different model."
                            )
                        },
                    }
                ),
            )
        )
        success_stdout = json.dumps(
            {
                "type": "turn.completed",
                "usage": {"input_tokens": 15, "output_tokens": 3},
            }
        )

        with tempfile.TemporaryDirectory() as temporary:
            outcome, raw, invocations, sleep = (
                self._invoke_one_case_with_host_responses(
                    Path(temporary),
                    (
                        {"exit_code": 1, "stdout": capacity},
                        {
                            "exit_code": 0,
                            "stdout": success_stdout,
                            "response": {
                                "actual_owner": "repo-map",
                                "handoffs": [],
                            },
                        },
                    ),
                )
            )

        self.assertTrue(outcome.succeeded)
        self.assertEqual(2, len(invocations))
        self.assertNotEqual(invocations[0]["cwd"], invocations[1]["cwd"])
        self.assertNotEqual(invocations[0]["home"], invocations[1]["home"])
        self.assertEqual("attempt-1", invocations[0]["cwd"].name)
        self.assertEqual("attempt-2", invocations[1]["cwd"].name)
        self.assertEqual("attempt-1", invocations[0]["home"].name)
        self.assertEqual("attempt-2", invocations[1]["home"].name)
        sleep.assert_called_once_with(5)
        self.assertEqual(2, raw["metrics"]["attempt_count"])
        self.assertEqual(1, raw["metrics"]["retry_count"])
        first, second = raw["host_attempts"]
        self.assertEqual("model_capacity", first["error_class"])
        self.assertTrue(first["retryable"])
        self.assertEqual(5, first["backoff_seconds_before_next"])
        self.assertIsNone(first["metrics"]["input_tokens"])
        self.assertIsNone(first["metrics"]["output_tokens"])
        self.assertIsNone(second["error_class"])
        self.assertFalse(second["retryable"])
        self.assertEqual(0, second["backoff_seconds_before_next"])
        self.assertEqual(15, raw["metrics"]["input_tokens"])
        self.assertEqual(3, raw["metrics"]["output_tokens"])

    def test_near_match_capacity_error_does_not_retry(self) -> None:
        near_match = json.dumps(
            {"message": "Selected model is at capacity; please try again."}
        )

        with tempfile.TemporaryDirectory() as temporary:
            outcome, raw, invocations, sleep = (
                self._invoke_one_case_with_host_responses(
                    Path(temporary),
                    ({"exit_code": 1, "stdout": near_match},),
                )
            )

        self.assertFalse(outcome.succeeded)
        self.assertEqual(1, len(invocations))
        sleep.assert_not_called()
        self.assertEqual(1, raw["metrics"]["attempt_count"])
        self.assertEqual(0, raw["metrics"]["retry_count"])
        self.assertIsNone(raw["host_attempts"][0]["error_class"])
        self.assertFalse(raw["host_attempts"][0]["retryable"])

    def test_two_capacity_failures_stop_after_exactly_two_attempts(self) -> None:
        capacity = json.dumps(
            {
                "message": (
                    "Selected model is at capacity. "
                    "Please try a different model."
                )
            }
        )

        with tempfile.TemporaryDirectory() as temporary:
            outcome, raw, invocations, sleep = (
                self._invoke_one_case_with_host_responses(
                    Path(temporary),
                    (
                        {"exit_code": 1, "stderr": capacity},
                        {"exit_code": 1, "stderr": capacity},
                    ),
                )
            )

        self.assertFalse(outcome.succeeded)
        self.assertEqual(2, len(invocations))
        sleep.assert_called_once_with(5)
        self.assertEqual(2, raw["metrics"]["attempt_count"])
        self.assertEqual(1, raw["metrics"]["retry_count"])
        self.assertEqual(
            ["model_capacity", "model_capacity"],
            [attempt["error_class"] for attempt in raw["host_attempts"]],
        )
        self.assertEqual(
            [5, 0],
            [
                attempt["backoff_seconds_before_next"]
                for attempt in raw["host_attempts"]
            ],
        )

    def test_completed_attempt_is_checkpointed_before_retry_backoff(self) -> None:
        capacity = json.dumps(
            {
                "message": (
                    "Selected model is at capacity. "
                    "Please try a different model."
                )
            }
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(InterruptedError, "interrupted backoff"):
                self._invoke_one_case_with_host_responses(
                    root,
                    ({"exit_code": 1, "stdout": capacity},),
                    sleep_side_effect=InterruptedError("interrupted backoff"),
                )
            raw_paths = list((root / "raw").glob("*.json"))
            self.assertEqual(1, len(raw_paths))
            raw = json.loads(raw_paths[0].read_text(encoding="utf-8"))

        self.assertEqual(1, len(raw["host_attempts"]))
        self.assertEqual("model_capacity", raw["host_attempts"][0]["error_class"])
        self.assertEqual(5, raw["host_attempts"][0]["backoff_seconds_before_next"])
        self.assertEqual(1, raw["metrics"]["attempt_count"])
        self.assertEqual(0, raw["metrics"]["retry_count"])

    def test_valid_route_or_token_bearing_capacity_failure_does_not_retry(
        self,
    ) -> None:
        capacity_message = (
            "Selected model is at capacity. Please try a different model."
        )
        scenarios = (
            {
                "name": "valid route",
                "response": {"actual_owner": "repo-map", "handoffs": []},
                "stdout": json.dumps({"message": capacity_message}),
            },
            {
                "name": "token-bearing",
                "stdout": "\n".join(
                    (
                        json.dumps({"message": capacity_message}),
                        json.dumps(
                            {
                                "usage": {
                                    "input_tokens": 12,
                                    "output_tokens": 3,
                                }
                            }
                        ),
                    )
                ),
            },
        )

        for scenario in scenarios:
            with self.subTest(scenario=scenario["name"]), tempfile.TemporaryDirectory() as temporary:
                outcome, raw, invocations, sleep = (
                    self._invoke_one_case_with_host_responses(
                        Path(temporary),
                        (
                            {
                                "exit_code": 1,
                                "stdout": scenario["stdout"],
                                "response": scenario.get("response"),
                            },
                        ),
                    )
                )

            self.assertFalse(outcome.succeeded)
            self.assertEqual(1, len(invocations))
            sleep.assert_not_called()
            self.assertEqual(1, raw["metrics"]["attempt_count"])
            self.assertEqual(0, raw["metrics"]["retry_count"])
            self.assertIsNone(raw["host_attempts"][0]["error_class"])
            self.assertFalse(raw["host_attempts"][0]["retryable"])

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
            attempt = json.loads((outcome.run_dir / "attempt.json").read_text())
            self.assertEqual("failure", attempt["status"])
            self.assertEqual(config.campaign_id, attempt["campaign_id"])

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
                "AICRAFT_TEST_SECRET": "must-not-propagate",
            }
            with mock.patch.dict(os.environ, environment, clear=False):
                codex_environment = RUNNER._isolated_host_environment(
                    "codex", root / "codex-isolated"
                )
                claude_environment = RUNNER._isolated_host_environment(
                    "claude", root / "claude-isolated"
                )
            self.assertNotIn("AICRAFT_TEST_SECRET", codex_environment)
            self.assertNotIn("AICRAFT_TEST_SECRET", claude_environment)

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

    def test_isolated_environment_preserves_allowlisted_volta_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_home = root / "source-home"
            codex_home = source_home / ".codex"
            volta_home = root / "volta-home"
            codex_home.mkdir(parents=True)
            volta_home.mkdir()
            (codex_home / "auth.json").write_text("codex-auth", encoding="utf-8")

            environment = {
                "HOME": str(source_home),
                "CODEX_HOME": str(codex_home),
                "VOLTA_HOME": str(volta_home),
                "AICRAFT_TEST_SECRET": "must-not-propagate",
            }
            with mock.patch.dict(os.environ, environment, clear=True):
                isolated = RUNNER._isolated_host_environment(
                    "codex", root / "codex-isolated"
                )

            self.assertEqual(str(volta_home), isolated["VOLTA_HOME"])
            self.assertNotIn("AICRAFT_TEST_SECRET", isolated)

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
                comparison_group_id="00000000-0000-4000-8000-000000000010",
                campaign_id=None,
                campaign_path_relative=None,
                campaign_sha256=None,
                evaluation_protocol_revision=None,
                evaluation_protocol_sha256=None,
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
