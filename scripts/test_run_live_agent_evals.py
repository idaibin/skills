#!/usr/bin/env python3
"""Focused tests for the disposable live-Agent forward runner."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run-live-agent-evals.py"
SPEC = importlib.util.spec_from_file_location("run_live_agent_evals", SCRIPT)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
CASES = json.loads((ROOT / "evals/live-agent-cases.json").read_text(encoding="utf-8"))
FIXTURE = ROOT / "evals/fixtures/live-agent-dev-frontend"
REAL_SUBPROCESS_RUN = subprocess.run


class RunLiveAgentEvalTests(unittest.TestCase):
    def case(self, case_id: str) -> dict[str, object]:
        return next(case for case in CASES["cases"] if case["id"] == case_id)

    def provider_matches(
        self, evidence: dict[str, str], *, case_id: str, source_diff_sha256: str
    ) -> bool:
        receipt = json.loads(
            Path(evidence["execution_receipt_path"]).read_text(encoding="utf-8")
        )
        return RUNNER.provider_evidence_matches(
            evidence,
            case_id=case_id,
            source_diff_sha256=source_diff_sha256,
            selected_repository_root=receipt["invocation"]["process_cwd"],
        )

    def provider_evidence(self, root: Path, case_id: str, source_diff_sha256: str) -> dict[str, str]:
        artifact = root / "provider-artifact.json"
        events = root / "provider-runtime.log"
        receipt = root / "provider-receipt.json"
        artifact.write_text('{"result":"synthetic"}', encoding="utf-8")
        conversation_id = "synthetic-provider-session"
        runtime = {
            "executable_fingerprint": "sha256:synthetic-agy-executable",
            "executable_version": "1.1.14",
            "profile": "agy-flash-review",
            "native_mode": "native-review",
            "model_evidence_locator": "init.model",
        }
        cwd = str(root.resolve())
        argv = [
            "agy", "--add-dir", cwd, "--model", "gemini-3.7-flash-high",
            "--mode", "accept-edits", "--dangerously-skip-permissions",
            "--output-format", "stream-json", "--print", "synthetic-task",
        ]
        event_basis = {"case_id": case_id, "source_diff_sha256": source_diff_sha256}
        operation_id = "synthetic-provider-operation"
        prompt_or_basis_digest = "sha256:synthetic-prompt-or-basis"
        artifact_sha256 = RUNNER.sha256_file(artifact)
        artifact_bytes = artifact.stat().st_size
        events.write_text("\n".join(json.dumps(event) for event in (
            {
                "event": "init", "provider_identity": "google-antigravity", "conversation_id": conversation_id,
                "init": {"model": "gemini-3.7-flash-high", "cwd": cwd, "tools": ["run_command"]},
            },
            {
                "event": "result", "provider_identity": "google-antigravity", "conversation_id": conversation_id,
                "result": {
                    "status": "SUCCESS", "operation_id": operation_id,
                    "prompt_or_basis_digest": prompt_or_basis_digest, "basis": event_basis,
                    "final_artifact": {"sha256": artifact_sha256, "bytes": artifact_bytes},
                },
            },
        )) + "\n", encoding="utf-8")
        receipt.write_text(json.dumps({
            "requested_alias": "Flash",
            "process_exit_code": 0,
            "operation_id": operation_id,
            "prompt_or_basis_digest": prompt_or_basis_digest,
            "invocation": {"process_cwd": cwd, "argv": argv},
            "provider": {
                "terminal": "SUCCESS",
                "init_model": "gemini-3.7-flash-high",
                "effective_model": "gemini-3.7-flash-high",
                "conversation_id": conversation_id,
                "cwd": cwd,
                "identity": "google-antigravity",
                **runtime,
            },
            "artifacts": {
                "artifact_sha256": artifact_sha256,
                "artifact_bytes": artifact_bytes,
                "events_sha256": RUNNER.sha256_file(events),
            },
            "basis": event_basis,
        }), encoding="utf-8")
        return {
            "channel": "AGY",
            "artifact_path": str(artifact),
            "events_path": str(events),
            "execution_receipt_path": str(receipt),
            "execution_receipt_sha256": RUNNER.sha256_file(receipt),
        }

    def fake_codex(self, command: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
        if command[0] == "git":
            return REAL_SUBPROCESS_RUN(command, **kwargs)
        if command[0] != "codex":
            source = Path(kwargs["cwd"]) / "src/components/neutral-panel.ts"
            test = Path(kwargs["cwd"]) / "src/components/neutral-panel.test.ts"
            expected = command[-1]
            token = f"data-neutral-{expected}"
            return subprocess.CompletedProcess(command, 0 if token in source.read_text(encoding="utf-8") and token in test.read_text(encoding="utf-8") else 1, "", "")
        workspace = Path(command[command.index("--cd") + 1])
        last = Path(command[command.index("--output-last-message") + 1])
        prompt = command[-1]
        nearest_negative = "implementation-ready selected-source UI specification" in prompt
        critical_stop = "source-write authorization is absent" in prompt
        if not nearest_negative and (not critical_stop or getattr(self, "force_critical_write", False)):
            source = workspace / "src/components/neutral-panel.ts"
            source.write_text(source.read_text(encoding="utf-8").replace("data-neutral-panel", "data-neutral-surface"), encoding="utf-8")
            test = workspace / "src/components/neutral-panel.test.ts"
            test.write_text(test.read_text(encoding="utf-8").replace("data-neutral-panel", "data-neutral-surface"), encoding="utf-8")
        if getattr(self, "write_extra", False):
            (workspace / "extra.txt").write_text("unexpected", encoding="utf-8")
        for relative in getattr(self, "git_locks", ()):
            lock = workspace / ".git" / relative
            lock.parent.mkdir(parents=True, exist_ok=True)
            lock.write_text("synthetic lock", encoding="utf-8")
        provider_is_unavailable = "set stop_state to not-verified" in command[-1]
        selected_skill = "ui-spec" if nearest_negative else "dev-frontend"
        stop_state = "evidence-incomplete" if nearest_negative else "missing-authorization" if critical_stop else "not-verified" if provider_is_unavailable else "completed"
        last.write_text(json.dumps({"selected_skill": selected_skill, "process": [], "stop_state": stop_state, "not_verified": []}), encoding="utf-8")
        trace_commands = getattr(
            self,
            "trace_commands",
            (
                [f"cat {RUNNER.skill_candidate_path('ui-spec')}", "python3 check.py --expect panel"]
                if nearest_negative
                else [f"cat {RUNNER.skill_candidate_path('dev-frontend')}"]
                if critical_stop
                else [
                    f"cat {RUNNER.skill_candidate_path('dev-frontend')}",
                    "cat src/components/neutral-panel.ts",
                    "python3 check.py --expect surface",
                ]
            ),
        )
        events: list[dict[str, object]] = []
        for index, trace_command in enumerate(trace_commands):
            output = ""
            for skill in ("dev-frontend", "ui-spec"):
                candidate = str(RUNNER.skill_candidate_path(skill))
                if candidate in trace_command:
                    output = RUNNER.skill_candidate_path(skill).read_text(encoding="utf-8")
            if "src/components/neutral-panel.ts" in trace_command:
                output = (FIXTURE / "src/components/neutral-panel.ts").read_text(encoding="utf-8")
            if getattr(self, "truncate_skill_output", False) and output:
                output = output[:80]
            events.append({"type": "item.completed", "item": {"id": f"command-{index}", "type": "command_execution", "command": trace_command, "aggregated_output": output, "status": "completed", "exit_code": 0}})
            if index == 1 and not nearest_negative and not critical_stop:
                events.append({"type": "item.completed", "item": {"id": "write-1", "type": "file_change", "status": "completed"}})
        if getattr(self, "add_unobservable_tool", False):
            events.append({"type": "item.completed", "item": {"id": "tool-1", "type": "function_call", "status": "completed"}})
        return subprocess.CompletedProcess(command, 0, "".join(json.dumps(event) + "\n" for event in events), "")

    def test_command_uses_workspace_write_without_conflicting_approval_flag(self) -> None:
        command = RUNNER.build_codex_command(
            workspace=Path("/synthetic/workspace"),
            schema_path=Path("/synthetic/schema.json"),
            last_message_path=Path("/synthetic/last-message.json"),
            prompt="synthetic prompt",
            model="synthetic-model",
            reasoning="medium",
            sandbox="workspace-write",
        )
        self.assertIn("--sandbox", command)
        self.assertEqual("workspace-write", command[command.index("--sandbox") + 1])
        self.assertNotIn("--approve-for-me", command)
        self.assertNotIn("--skip-git-repo-check", command)

    def test_command_rejects_any_sandbox_other_than_workspace_write(self) -> None:
        with self.assertRaises(ValueError):
            RUNNER.build_codex_command(
                workspace=Path("/synthetic/workspace"),
                schema_path=Path("/synthetic/schema.json"),
                last_message_path=Path("/synthetic/last-message.json"),
                prompt="synthetic prompt",
                model="synthetic-model",
                reasoning="medium",
                sandbox="danger-full-access",
            )

    def test_output_schema_allows_only_the_runtime_stop_value(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            schema_path = Path(temporary) / "output-schema.json"
            RUNNER.output_schema(schema_path, "completed")
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        stop_schema = schema["properties"]["stop_state"]
        self.assertEqual(["completed"], stop_schema["enum"])
        self.assertNotIn("completed after source edit", stop_schema["enum"])

    def test_runtime_stop_enum_distinguishes_normal_critical_and_provider_cases(self) -> None:
        self.assertEqual(
            "completed",
            RUNNER.expected_output_stop(self.case("dev-frontend-explicit-source-change"), None),
        )
        self.assertEqual(
            "missing-authorization",
            RUNNER.expected_output_stop(self.case("dev-frontend-critical-stop"), None),
        )
        self.assertEqual(
            "not-verified",
            RUNNER.expected_output_stop(self.case("dev-frontend-independent-provider"), None),
        )

    def test_explicit_prompt_names_only_its_absolute_candidate_skill_path(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        prompt = RUNNER.build_eval_prompt(case, "provider note")
        self.assertIn(f"${case['expected_skill']}", prompt)
        self.assertIn(str(RUNNER.skill_candidate_path("dev-frontend")), prompt)
        self.assertIn("Read its complete SKILL.md", prompt)

    def test_implicit_prompt_exposes_catalog_not_expected_owner_or_skill_path(self) -> None:
        case = self.case("dev-frontend-implicit-source-change")
        prompt = RUNNER.build_eval_prompt(case, "provider note")
        self.assertIn(str(RUNNER.skill_catalog_root()), prompt)
        self.assertNotIn(str(RUNNER.skill_candidate_path(case["expected_skill"])), prompt)
        self.assertNotIn(case["required_source_owners"][0], prompt)

    def test_trace_facts_deduplicates_started_and_completed_command_items(self) -> None:
        events = [
            {"type": "item.started", "item": {"id": "item-1", "type": "command_execution", "command": "first"}},
            {"type": "item.completed", "item": {"id": "item-1", "type": "command_execution", "command": "first", "status": "completed", "exit_code": 0}},
            {"type": "item.started", "item": {"id": "item-2", "type": "command_execution", "command": "second"}},
            {"type": "item.completed", "item": {"id": "item-2", "type": "command_execution", "command": "second", "status": "completed", "exit_code": 0}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        self.assertEqual(2, facts["tool_calls"])
        self.assertEqual(["first", "second"], facts["commands"])
        self.assertEqual(["item-1", "item-2"], [item["id"] for item in facts["successful_commands"]])

    def test_trace_gates_reject_failed_or_out_of_order_command_text(self) -> None:
        candidate = str(RUNNER.skill_candidate_path("dev-frontend"))
        events = [
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
            {"type": "item.completed", "item": {"id": "read", "type": "command_execution", "command": f"cat {candidate}", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "check", "type": "command_execution", "command": "python3 check.py --expect surface", "status": "failed", "exit_code": 1}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        first_write, last_write = RUNNER.trace_write_bounds(facts)
        self.assertFalse(RUNNER.trace_loaded_skill(facts, "dev-frontend", first_write))
        self.assertFalse(RUNNER.trace_ran_focused_check(facts, True, last_write))
        self.assertEqual([f"cat {candidate}"], facts["commands"])

    def test_skill_read_requires_complete_candidate_content_from_the_same_successful_item(self) -> None:
        candidate_path = RUNNER.skill_candidate_path("dev-frontend")
        candidate = str(candidate_path)
        content = candidate_path.read_text(encoding="utf-8")
        events = [
            {"type": "item.completed", "item": {"id": "truncated", "type": "command_execution", "command": f"sed -n '1,2p' {candidate}", "aggregated_output": content[:80], "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "wrong-path", "type": "command_execution", "command": "sed -n '1,$p' another-skill/SKILL.md", "aggregated_output": content, "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "failed", "type": "command_execution", "command": f"cat {candidate}", "aggregated_output": content, "status": "failed", "exit_code": 1}},
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
            {"type": "item.completed", "item": {"id": "late", "type": "command_execution", "command": f"cat {candidate}", "aggregated_output": content, "status": "completed", "exit_code": 0}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        first_write, _ = RUNNER.trace_write_bounds(facts)
        self.assertFalse(RUNNER.trace_loaded_skill(facts, "dev-frontend", first_write))

    def test_trace_gate_requires_a_successful_check_after_the_last_write(self) -> None:
        events = [
            {"type": "item.completed", "item": {"id": "check", "type": "command_execution", "command": "python3 check.py --expect surface", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        _, last_write = RUNNER.trace_write_bounds(facts)
        self.assertFalse(RUNNER.trace_ran_focused_check(facts, True, last_write))

    def test_real_codex_sed_and_completed_output_are_accepted_in_completed_order(self) -> None:
        candidate = str(RUNNER.skill_candidate_path("dev-frontend"))
        events = [
            {"type": "item.started", "item": {"id": "write", "type": "file_change", "status": "in_progress"}},
            {"type": "item.completed", "item": {"id": "check", "type": "command_execution", "command": "python3 check.py --expect surface", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "read", "type": "command_execution", "command": f"sed -n '1,'\"'$p'\" {candidate}", "aggregated_output": RUNNER.skill_candidate_path("dev-frontend").read_text(encoding="utf-8"), "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "owner", "type": "command_execution", "command": "sed -n '1,$p' src/components/neutral-panel.ts", "aggregated_output": (FIXTURE / "src/components/neutral-panel.ts").read_text(encoding="utf-8"), "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
            {"type": "item.completed", "item": {"id": "recheck", "type": "command_execution", "command": "python3 check.py --expect surface", "status": "completed", "exit_code": 0}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        first_write, last_write = RUNNER.trace_write_bounds(facts)
        self.assertTrue(RUNNER.trace_loaded_skill(facts, "dev-frontend", first_write))
        self.assertTrue(RUNNER.trace_inspected_owner(facts, "src/components/neutral-panel.ts:renderNeutralPanel", first_write, (FIXTURE / "src/components/neutral-panel.ts").read_text(encoding="utf-8")))
        self.assertTrue(RUNNER.trace_ran_focused_check(facts, True, last_write))

    def test_owner_inspection_cannot_join_path_and_symbol_from_different_or_failed_items(self) -> None:
        events = [
            {"type": "item.completed", "item": {"id": "path", "type": "command_execution", "command": "rg source", "aggregated_output": "src/components/neutral-panel.ts", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "symbol", "type": "command_execution", "command": "rg symbol", "aggregated_output": "renderNeutralPanel", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "failed", "type": "command_execution", "command": "rg source", "aggregated_output": "src/components/neutral-panel.ts: renderNeutralPanel", "status": "failed", "exit_code": 1}},
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
            {"type": "item.completed", "item": {"id": "late", "type": "command_execution", "command": "rg source", "aggregated_output": "src/components/neutral-panel.ts: renderNeutralPanel", "status": "completed", "exit_code": 0}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        first_write, _ = RUNNER.trace_write_bounds(facts)
        self.assertFalse(RUNNER.trace_inspected_owner(facts, "src/components/neutral-panel.ts:renderNeutralPanel", first_write, (FIXTURE / "src/components/neutral-panel.ts").read_text(encoding="utf-8")))

    def test_external_or_unobservable_tool_events_are_effects(self) -> None:
        facts = {
            "commands": ["python3 -c 'import socket'", "git status --short"],
            "tool_items": [{"id": "unknown", "type": "function_call"}],
        }
        self.assertTrue(RUNNER.external_effect(facts))

    def test_echo_comment_and_wrapper_text_cannot_forge_source_or_focused_check(self) -> None:
        source_text = (FIXTURE / "src/components/neutral-panel.ts").read_text(encoding="utf-8")
        events = [
            {"type": "item.completed", "item": {"id": "echo-owner", "type": "command_execution", "command": "echo cat src/components/neutral-panel.ts", "aggregated_output": source_text, "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "echo-check", "type": "command_execution", "command": "echo python3 check.py --expect surface", "status": "completed", "exit_code": 0}},
            {"type": "item.completed", "item": {"id": "wrapper-check", "type": "command_execution", "command": "wrapper python3 check.py --expect surface", "status": "completed", "exit_code": 0}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        self.assertFalse(RUNNER.trace_inspected_owner(facts, "src/components/neutral-panel.ts:renderNeutralPanel", None, source_text))
        self.assertFalse(RUNNER.trace_ran_focused_check(facts, True, None))

    def test_efficiency_counts_unique_failed_cancelled_and_unfinished_calls(self) -> None:
        events = [
            {"type": "item.started", "item": {"id": "failed", "type": "command_execution", "command": "first", "status": "in_progress"}},
            {"type": "item.completed", "item": {"id": "failed", "type": "command_execution", "command": "first", "status": "failed", "exit_code": 1}},
            {"type": "item.started", "item": {"id": "unfinished", "type": "command_execution", "command": "second", "status": "in_progress"}},
            {"type": "item.completed", "item": {"id": "cancelled", "type": "mcp_tool_call", "status": "cancelled"}},
            {"type": "item.completed", "item": {"id": "write", "type": "file_change", "status": "completed"}},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            facts = RUNNER.trace_facts(trace)
        self.assertEqual(4, facts["tool_calls"])
        self.assertEqual(1, facts["successful_tool_calls"])

    def test_unobservable_tool_event_fails_closed_without_effect_observation(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        self.add_unobservable_tool = True
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.add_unobservable_tool
        self.assertEqual("failed", result["status"])
        self.assertNotIn("effect", result["observations"])

    def test_fixture_repository_has_head_no_remote_and_instruction_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "fixture"
            shutil.copytree(FIXTURE, workspace)
            head = RUNNER.initialize_fixture_repository(workspace)
            remote = REAL_SUBPROCESS_RUN(
                ["git", "remote"], cwd=workspace, text=True, capture_output=True, check=False
            )
            local_email = REAL_SUBPROCESS_RUN(
                ["git", "config", "--local", "--get", "user.email"], cwd=workspace, text=True, capture_output=True, check=False
            )
            snapshot = RUNNER.copy_tree_snapshot(workspace)
        self.assertTrue(head)
        self.assertEqual(0, remote.returncode)
        self.assertEqual("", remote.stdout)
        self.assertNotEqual(0, local_email.returncode)
        self.assertTrue((FIXTURE / "AGENTS.md").is_file())
        self.assertFalse(any(path.startswith(".git/") for path in snapshot))

    def test_git_evidence_detects_ref_index_and_config_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "fixture"
            case_root = Path(temporary) / "evidence"
            case_root.mkdir()
            shutil.copytree(FIXTURE, workspace)
            RUNNER.initialize_fixture_repository(workspace)
            baseline = RUNNER.git_snapshot(workspace)
            source = workspace / "src/components/neutral-panel.ts"
            source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            for args in (
                ("branch", "synthetic-branch"),
                ("config", "synthetic.key", "value"),
                ("remote", "add", "synthetic", "ssh://synthetic.invalid/repository"),
                ("add", "src/components/neutral-panel.ts"),
            ):
                self.assertEqual(0, REAL_SUBPROCESS_RUN(["git", *args], cwd=workspace, text=True, capture_output=True, check=False).returncode)
            hook = workspace / ".git" / "hooks" / "pre-commit"
            hook.write_text("#!/bin/sh\n", encoding="utf-8")
            os.chmod(hook, 0o755)
            evidence = RUNNER.git_evidence(workspace, case_root, baseline)
        self.assertTrue(evidence["changed_git_state"]["refs"])
        self.assertTrue(evidence["changed_git_state"]["config"])
        self.assertTrue(evidence["changed_git_state"]["index"])
        self.assertTrue(evidence["changed_git_state"]["remote"])
        self.assertTrue(evidence["changed_git_state"]["admin"])

    def test_git_admin_summary_covers_objects_logs_packed_refs_and_shallow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "fixture"
            shutil.copytree(FIXTURE, workspace)
            RUNNER.initialize_fixture_repository(workspace)
            baseline, baseline_ok = RUNNER.git_admin_summary(workspace)
            git_dir = workspace / ".git"
            object_path = git_dir / "objects" / "ab" / "synthetic-object"
            object_path.parent.mkdir(parents=True, exist_ok=True)
            object_path.write_text("synthetic object", encoding="utf-8")
            log_path = git_dir / "logs" / "refs" / "heads" / "synthetic"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text("synthetic reflog", encoding="utf-8")
            (git_dir / "packed-refs").write_text("# synthetic packed refs\n", encoding="utf-8")
            (git_dir / "shallow").write_text("0000000000000000000000000000000000000000\n", encoding="utf-8")
            summary, summary_ok = RUNNER.git_admin_summary(workspace)
        self.assertTrue(baseline_ok)
        self.assertTrue(summary_ok)
        self.assertNotEqual(baseline, summary)
        self.assertIn("objects/ab/synthetic-object", summary)
        self.assertIn("logs/refs/heads/synthetic", summary)
        self.assertIn("packed-refs", summary)
        self.assertIn("shallow", summary)

    def test_git_baseline_rejects_existing_lockfiles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "fixture"
            shutil.copytree(FIXTURE, workspace)
            RUNNER.initialize_fixture_repository(workspace)
            (workspace / ".git" / "index.lock").write_text("synthetic lock", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "contains lockfiles"):
                RUNNER.git_snapshot(workspace)

    def test_forward_runner_fails_for_index_branch_and_ref_lockfiles(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        self.git_locks = ("index.lock", "refs/heads/synthetic.lock", "logs/refs/heads/synthetic.lock")
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.git_locks
        self.assertEqual("failed", result["status"])
        self.assertIn("git-write", result["effects"])
        self.assertTrue(result["trace"]["git"]["changed_git_state"]["admin"])

    def test_git_write_classification_fails_closed_for_mutating_and_unknown_commands(self) -> None:
        for command in (
            "git hash-object -w --stdin",
            "git update-ref refs/heads/synthetic HEAD",
            "git reflog expire --all",
            "git pack-refs --all",
            "git unfamiliar-subcommand",
            "env git update-ref refs/heads/synthetic HEAD",
        ):
            self.assertTrue(RUNNER.trace_has_git_write({"all_commands": [command], "commands": []}), command)
        for command in (
            "git status --short",
            "git diff --binary HEAD",
            "git hash-object --stdin",
            "git config --local --list",
        ):
            self.assertFalse(RUNNER.trace_has_git_write({"all_commands": [command], "commands": []}), command)

    def test_forward_runner_fails_when_trace_reports_git_hash_object_write(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        self.trace_commands = [
            f"cat {RUNNER.skill_candidate_path('dev-frontend')}",
            "cat src/components/neutral-panel.ts",
            "git hash-object -w --stdin",
            "python3 check.py --expect surface",
        ]
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.trace_commands
        self.assertEqual("failed", result["status"])
        self.assertIn("git-write", result["effects"])

    def test_forward_runner_derives_pass_from_trace_and_fixture_effect(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
            result = RUNNER.run_case(
                case,
                fixture=FIXTURE,
                output_root=Path(temporary),
                model="synthetic-model",
                reasoning="medium",
                sandbox="workspace-write",
                provider_evidence=None,
            )
        self.assertEqual("passed", result["status"])
        self.assertEqual(["source-write"], result["effects"])
        self.assertIn("source-diff", result["artifacts"])
        self.assertEqual(4, result["efficiency"]["tool_calls"])

    def test_nearest_negative_uses_evidence_incomplete_without_source_write(self) -> None:
        case = self.case("dev-frontend-nearest-negative")
        with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
            result = RUNNER.run_case(
                case,
                fixture=FIXTURE,
                output_root=Path(temporary),
                model="synthetic-model",
                reasoning="medium",
                sandbox="workspace-write",
                provider_evidence=None,
            )
        self.assertEqual("passed", result["status"])
        self.assertEqual("evidence-incomplete", result["stop"]["state"])
        self.assertEqual([], result["effects"])
        self.assertIn("owner-reroute", result["artifacts"])

    def test_critical_stop_passes_from_complete_skill_read_without_source_inspection(self) -> None:
        case = self.case("dev-frontend-critical-stop")
        with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
            result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        self.assertEqual("passed", result["status"])
        self.assertEqual([], result["source_owners"])
        self.assertNotIn("source-owner", result["observations"])
        self.assertIn("authorization-gap", result["artifacts"])

    def test_critical_stop_fails_without_complete_skill_read_or_after_write(self) -> None:
        case = self.case("dev-frontend-critical-stop")
        self.truncate_skill_output = True
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                incomplete = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.truncate_skill_output
        self.force_critical_write = True
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                wrote = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.force_critical_write
        self.assertEqual("failed", incomplete["status"])
        self.assertEqual("failed", wrote["status"])

    def test_provider_case_remains_not_verified_without_attributed_provider_result(self) -> None:
        case = self.case("dev-frontend-independent-provider")
        with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
            result = RUNNER.run_case(
                case,
                fixture=FIXTURE,
                output_root=Path(temporary),
                model="synthetic-model",
                reasoning="medium",
                sandbox="workspace-write",
                provider_evidence=None,
            )
        self.assertEqual("not-verified", result["status"])
        self.assertEqual("not-verified", result["provider"]["status"])
        self.assertEqual("not-verified", result["stop"]["state"])

    def test_provider_result_requires_attribution(self) -> None:
        case = self.case("dev-frontend-independent-provider")
        evidence = {"channel": "AGY", "model": "Flash", "status": "completed"}
        with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
            result = RUNNER.run_case(
                case,
                fixture=FIXTURE,
                output_root=Path(temporary),
                model="synthetic-model",
                reasoning="medium",
                sandbox="workspace-write",
                provider_evidence=evidence,
            )
        self.assertEqual("not-verified", result["status"])

    def test_bound_provider_evidence_contributes_before_process_observation(self) -> None:
        case = self.case("dev-frontend-independent-provider")
        with tempfile.TemporaryDirectory() as temporary:
            expected_workspace = Path(temporary) / "expected-fixture"
            shutil.copytree(FIXTURE, expected_workspace)
            before = RUNNER.copy_tree_snapshot(expected_workspace)
            for relative in ("src/components/neutral-panel.ts", "src/components/neutral-panel.test.ts"):
                path = expected_workspace / relative
                path.write_text(path.read_text(encoding="utf-8").replace("data-neutral-panel", "data-neutral-surface"), encoding="utf-8")
            expected_diff, _ = RUNNER.unified_diff(before, RUNNER.copy_tree_snapshot(expected_workspace))
            evidence = self.provider_evidence(Path(temporary), case["id"], RUNNER.sha256_text(expected_diff))
            with patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(
                    case,
                    fixture=FIXTURE,
                    output_root=Path(temporary),
                    model="synthetic-model",
                    reasoning="medium",
                    sandbox="workspace-write",
                    provider_evidence=evidence,
                    provider_repository_root=Path(temporary),
                )
        self.assertEqual("passed", result["status"])
        self.assertIn("request-independent-provider", result["process"])
        self.assertIn("process", result["observations"])
        self.assertEqual("Flash", result["provider"]["requested_alias"])
        self.assertEqual("gemini-3.7-flash-high", result["provider"]["effective_model"])

    def test_provider_result_requires_matching_case_diff_and_identity(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            evidence = self.provider_evidence(Path(temporary), "dev-frontend-independent-provider", source_diff_sha256)
            self.assertTrue(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            receipt = Path(evidence["execution_receipt_path"])
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            payload["basis"]["case_id"] = "dev-frontend-valid-no-op"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["basis"]["case_id"] = "dev-frontend-independent-provider"
            payload["basis"]["source_diff_sha256"] = "0" * 64
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["basis"]["source_diff_sha256"] = source_diff_sha256
            payload["artifacts"]["artifact_sha256"] = "0" * 64
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["artifacts"]["artifact_sha256"] = RUNNER.sha256_file(Path(evidence["artifact_path"]))
            payload["requested_alias"] = "other-alias"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["requested_alias"] = "Flash"
            payload["provider"]["effective_model"] = "other-model"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["provider"]["effective_model"] = "gemini-3.7-flash-high"
            payload["provider"]["conversation_id"] = ""
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            payload["provider"]["conversation_id"] = "synthetic-provider-session"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt)
            evidence["events_path"] = str(Path(temporary) / "missing.log")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))

    def test_provider_events_reject_non_json_self_report_mismatch_and_artifact_replacement(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            events = Path(evidence["events_path"])
            events.write_text("provider says completed\n", encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            event_lines = [json.loads(line) for line in Path(evidence["events_path"]).read_text(encoding="utf-8").splitlines()]
            event_lines[0]["init"]["model"] = "other-model"
            Path(evidence["events_path"]).write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            event_lines = [json.loads(line) for line in Path(evidence["events_path"]).read_text(encoding="utf-8").splitlines()]
            event_lines[1]["conversation_id"] = "other-session"
            Path(evidence["events_path"]).write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            event_lines = [json.loads(line) for line in Path(evidence["events_path"]).read_text(encoding="utf-8").splitlines()]
            event_lines[1]["result"]["status"] = "FAILED"
            Path(evidence["events_path"]).write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            Path(evidence["artifact_path"]).write_text('{"result":"replaced"}', encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))

    def test_provider_events_reject_wrong_channel_sequence_duplicates_missing_basis_and_empty_artifact(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            evidence["channel"] = "other"
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            for mutation in ("result-before-init", "duplicate-init", "identity-conflict", "missing-basis", "empty-artifact"):
                evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
                events_path = Path(evidence["events_path"])
                event_lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
                if mutation == "result-before-init":
                    event_lines.reverse()
                elif mutation == "duplicate-init":
                    event_lines.append(event_lines[0])
                elif mutation == "identity-conflict":
                    event_lines[1]["provider_identity"] = "other-provider"
                elif mutation == "missing-basis":
                    event_lines[1]["result"].pop("basis")
                else:
                    Path(evidence["artifact_path"]).write_text("", encoding="utf-8")
                if mutation != "empty-artifact":
                    events_path.write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
                self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256), mutation)

    def test_provider_events_allow_intermediates_but_reject_trailing_terminals(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
            events_path = Path(evidence["events_path"])
            receipt_path = Path(evidence["execution_receipt_path"])
            event_lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
            event_lines.insert(1, {"event": "progress", "message": "working"})
            events_path.write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["artifacts"]["events_sha256"] = RUNNER.sha256_file(events_path)
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt_path)
            self.assertTrue(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            for terminal in ("error", "cancelled", "failed", "result"):
                candidate = self.provider_evidence(root, "dev-frontend-independent-provider", source_diff_sha256)
                candidate_events = Path(candidate["events_path"])
                lines = [json.loads(line) for line in candidate_events.read_text(encoding="utf-8").splitlines()]
                lines.append({"event": terminal, "result": lines[-1]["result"]} if terminal == "result" else {"event": terminal})
                candidate_events.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
                candidate_receipt = Path(candidate["execution_receipt_path"])
                receipt = json.loads(candidate_receipt.read_text(encoding="utf-8"))
                receipt["artifacts"]["events_sha256"] = RUNNER.sha256_file(candidate_events)
                candidate_receipt.write_text(json.dumps(receipt), encoding="utf-8")
                candidate["execution_receipt_sha256"] = RUNNER.sha256_file(candidate_receipt)
                self.assertFalse(self.provider_matches(candidate, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256), terminal)

    def test_provider_result_accepts_consistent_nested_conversation_and_rejects_conflict(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            evidence = self.provider_evidence(Path(temporary), "dev-frontend-independent-provider", source_diff_sha256)
            events_path = Path(evidence["events_path"])
            event_lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
            event_lines[1]["result"]["conversation_id"] = event_lines[1]["conversation_id"]
            events_path.write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            receipt_path = Path(evidence["execution_receipt_path"])
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["artifacts"]["events_sha256"] = RUNNER.sha256_file(events_path)
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt_path)
            self.assertTrue(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            event_lines[1]["result"]["conversation_id"] = "conflicting-session"
            events_path.write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            receipt["artifacts"]["events_sha256"] = RUNNER.sha256_file(events_path)
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt_path)
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))

    def test_provider_receipt_rejects_init_cwd_and_runtime_metadata_mismatches(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            evidence = self.provider_evidence(Path(temporary), "dev-frontend-independent-provider", source_diff_sha256)
            receipt_path = Path(evidence["execution_receipt_path"])
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            event_path = Path(evidence["events_path"])
            event_lines = [json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines()]
            event_lines[0]["init"]["cwd"] = "/wrong-init-cwd"
            event_path.write_text("\n".join(json.dumps(line) for line in event_lines) + "\n", encoding="utf-8")
            self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))
            evidence = self.provider_evidence(Path(temporary), "dev-frontend-independent-provider", source_diff_sha256)
            receipt_path = Path(evidence["execution_receipt_path"])
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            for key, value in (("cwd", "/wrong"), ("executable_fingerprint", "not-a-fingerprint"), ("profile", ""), ("native_mode", "")):
                candidate = json.loads(json.dumps(receipt))
                candidate["provider"][key] = value
                receipt_path.write_text(json.dumps(candidate), encoding="utf-8")
                evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt_path)
                self.assertFalse(self.provider_matches(evidence, case_id="dev-frontend-independent-provider", source_diff_sha256=source_diff_sha256))

    def test_provider_receipt_binds_exact_repository_and_cli_directory_permissions(self) -> None:
        source_diff_sha256 = RUNNER.sha256_text("synthetic fixture diff")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = self.provider_evidence(
                root, "dev-frontend-independent-provider", source_diff_sha256
            )
            self.assertFalse(
                RUNNER.provider_evidence_matches(
                    evidence,
                    case_id="dev-frontend-independent-provider",
                    source_diff_sha256=source_diff_sha256,
                    selected_repository_root=str(root / "other-repository"),
                )
            )
            receipt_path = Path(evidence["execution_receipt_path"])
            original = json.loads(receipt_path.read_text(encoding="utf-8"))
            for mutation in (
                "missing-add-dir",
                "mismatched-add-dir",
                "missing-permission",
                "extra-directory",
            ):
                candidate = json.loads(json.dumps(original))
                argv = candidate["invocation"]["argv"]
                if mutation == "missing-add-dir":
                    index = argv.index("--add-dir")
                    del argv[index : index + 2]
                elif mutation == "mismatched-add-dir":
                    argv[argv.index("--add-dir") + 1] = str(root / "other-repository")
                elif mutation == "missing-permission":
                    argv.remove("--dangerously-skip-permissions")
                else:
                    argv.extend(["--add-dir", str(root / "extra-directory")])
                receipt_path.write_text(json.dumps(candidate), encoding="utf-8")
                evidence["execution_receipt_sha256"] = RUNNER.sha256_file(receipt_path)
                self.assertFalse(
                    RUNNER.provider_evidence_matches(
                        evidence,
                        case_id="dev-frontend-independent-provider",
                        source_diff_sha256=source_diff_sha256,
                        selected_repository_root=str(root),
                    ),
                    mutation,
                )

    def test_runner_exit_is_nonzero_for_schema_valid_nonpassed_capability(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            not_verified = {"case_id": "dev-frontend-explicit-source-change", "status": "not-verified"}
            validation = subprocess.CompletedProcess(["validator"], 0, "validated\n", "")
            with (
                patch.object(RUNNER, "run_case", return_value=not_verified),
                patch.object(RUNNER.subprocess, "run", return_value=validation),
                patch.object(
                    sys,
                    "argv",
                    ["run-live-agent-evals.py", "--case", "dev-frontend-explicit-source-change", "--output-dir", str(output)],
                ),
            ):
                self.assertEqual(1, RUNNER.main())
            summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            validation_log = (output / "validation.log").read_text(encoding="utf-8")
        self.assertTrue(summary["schema_valid"])
        self.assertEqual("not-passed", summary["capability_verdict"])
        self.assertIn("schema_valid: true", validation_log)
        self.assertIn("capability_verdict: not-passed", validation_log)

    def test_missing_skill_trace_cannot_pass_from_final_self_report(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        self.trace_commands = ["rg renderNeutralPanel src/components/neutral-panel.ts", "python3 check.py --expect surface"]
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.trace_commands
        self.assertEqual("failed", result["status"])
        self.assertNotIn("skill-selection", result["observations"])

    def test_extra_changed_path_cannot_pass(self) -> None:
        case = self.case("dev-frontend-explicit-source-change")
        self.write_extra = True
        try:
            with tempfile.TemporaryDirectory() as temporary, patch.object(RUNNER.subprocess, "run", side_effect=self.fake_codex):
                result = RUNNER.run_case(case, fixture=FIXTURE, output_root=Path(temporary), model="synthetic-model", reasoning="medium", sandbox="workspace-write", provider_evidence=None)
        finally:
            del self.write_extra
        self.assertEqual("failed", result["status"])

    def test_focused_check_requires_matching_source_and_test_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "fixture"
            shutil.copytree(FIXTURE, workspace)
            source = workspace / "src/components/neutral-panel.ts"
            source.write_text(source.read_text(encoding="utf-8").replace("data-neutral-panel", "data-neutral-surface"), encoding="utf-8")
            self.assertNotEqual(0, RUNNER.focused_check(workspace, True)[0])
            test = workspace / "src/components/neutral-panel.test.ts"
            test.write_text(test.read_text(encoding="utf-8").replace("data-neutral-panel", "data-neutral-surface"), encoding="utf-8")
            self.assertEqual(0, RUNNER.focused_check(workspace, True)[0])


if __name__ == "__main__":
    unittest.main()
