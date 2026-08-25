#!/usr/bin/env python3
"""Run fixed live-Agent cases in disposable fixture copies and preserve evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_provider_evidence import sha256_file, verify_provider_evidence

VALIDATOR_PATH = ROOT / "scripts/validate-live-agent-evals.py"
RESULT_SCHEMA_VERSION = "skill-live-agent-results/v1"
SOURCE_PATH = "src/components/neutral-panel.ts"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def load_provider_evidence(path: Path) -> dict[str, Any]:
    evidence = load_json(path)
    for key in ("artifact_path", "events_path", "execution_receipt_path"):
        value = evidence.get(key)
        if isinstance(value, str) and not Path(value).is_absolute():
            evidence[key] = str((path.parent / value).resolve())
    return evidence


def parse_final_message(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def copy_tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and ".git" not in path.parts
    }


def unified_diff(before: dict[str, bytes], after: dict[str, bytes]) -> tuple[str, list[str]]:
    changed: list[str] = []
    output: list[str] = []
    for relative in sorted(set(before) | set(after)):
        old = before.get(relative, b"").decode("utf-8", errors="replace").splitlines(keepends=True)
        new = after.get(relative, b"").decode("utf-8", errors="replace").splitlines(keepends=True)
        if old == new:
            continue
        changed.append(relative)
        output.extend(difflib.unified_diff(old, new, fromfile=f"before/{relative}", tofile=f"after/{relative}"))
    return "".join(output), changed


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from walk(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk(nested)


def trace_facts(trace_path: Path) -> dict[str, Any]:
    items_by_id: dict[str, dict[str, Any]] = {}
    anonymous_items: list[dict[str, Any]] = []
    raw = trace_path.read_text(encoding="utf-8") if trace_path.is_file() else ""
    for order, line in enumerate(raw.splitlines()):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for value in walk(event):
            item_type = re.sub(r"[^a-z0-9]+", "_", str(value.get("type", "")).lower()).strip("_")
            if not any(marker in item_type for marker in ("command_execution", "function_call", "tool_call", "file_change", "mcp")):
                continue
            item_id = value.get("id")
            record = {
                "id": item_id if isinstance(item_id, str) else None,
                "started_order": order if event.get("type") != "item.completed" else None,
                "completed_order": order if event.get("type") == "item.completed" else None,
                "type": item_type,
                "command": next((value[key] for key in ("command", "cmd") if isinstance(value.get(key), str)), None),
                "output": value.get("aggregated_output") if isinstance(value.get("aggregated_output"), str) else None,
                "status": value.get("status"),
                "exit_code": value.get("exit_code"),
                "event_type": event.get("type"),
            }
            if isinstance(item_id, str) and item_id:
                prior = items_by_id.get(item_id)
                if prior is None:
                    items_by_id[item_id] = record
                else:
                    prior.update({key: value for key, value in record.items() if value is not None})
                    if record["started_order"] is not None:
                        prior["started_order"] = record["started_order"]
                    if record["completed_order"] is not None:
                        prior["completed_order"] = record["completed_order"]
            else:
                anonymous_items.append(record)
    items = [*items_by_id.values(), *anonymous_items]
    for item in items:
        item["order"] = item["completed_order"] if item["completed_order"] is not None else item["started_order"]
    items.sort(key=lambda item: item["order"])
    successful_commands = [
        item for item in items
        if item["type"] == "command_execution"
        and item["completed_order"] is not None
        and item["status"] == "completed"
        and item["exit_code"] == 0
        and isinstance(item["command"], str)
    ]
    call_items = [
        item for item in items
        if any(marker in item["type"] for marker in ("command_execution", "function_call", "tool_call", "file_change", "mcp"))
    ]
    successful_file_changes = [
        item for item in items
        if item["type"] == "file_change" and item["completed_order"] is not None and item["status"] == "completed"
    ]
    tool_items = [item for item in call_items if item["type"] != "command_execution" and item["type"] != "file_change"]
    successful_calls = [
        item for item in call_items
        if item["completed_order"] is not None and item["status"] == "completed"
        and (item["exit_code"] is None or item["exit_code"] == 0)
    ]
    return {
        "tool_calls": len(call_items),
        "successful_tool_calls": len(successful_calls),
        "commands": [item["command"] for item in successful_commands],
        "all_commands": [item["command"] for item in call_items if isinstance(item.get("command"), str)],
        "items": items,
        "successful_commands": successful_commands,
        "tool_items": tool_items,
        "raw": raw,
    }


def output_schema(path: Path, expected_stop: str) -> None:
    path.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["selected_skill", "process", "stop_state", "not_verified"],
                "properties": {
                    "selected_skill": {"type": "string"},
                    "process": {"type": "array", "items": {"type": "string"}},
                    "stop_state": {"type": "string", "enum": [expected_stop]},
                    "not_verified": {"type": "array", "items": {"type": "string"}},
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def environment_fingerprint() -> str:
    selected = {key: os.environ.get(key, "") for key in ("LANG", "LC_ALL", "PATH", "TERM")}
    return hashlib.sha256(json.dumps(selected, sort_keys=True).encode()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def expected_output_stop(case: dict[str, Any], provider_evidence: dict[str, Any] | None) -> str:
    if case.get("required_provider") is not None and provider_evidence is None:
        return "not-verified"
    return case["expected_stop"]


def provider_evidence_matches(
    evidence: dict[str, Any] | None,
    *,
    case_id: str,
    source_diff_sha256: str,
    selected_repository_root: str,
) -> bool:
    return verify_provider_evidence(
        evidence,
        case_id=case_id,
        source_diff_sha256=source_diff_sha256,
        selected_repository_root=selected_repository_root,
    )[0] is not None


def capability_verdict(results: list[dict[str, Any]]) -> str:
    return "passed" if results and all(item.get("status") == "passed" for item in results) else "not-passed"


def runner_exit_code(schema_valid: bool, results: list[dict[str, Any]]) -> int:
    return 0 if schema_valid and capability_verdict(results) == "passed" else 1


def focused_check(workspace: Path, expects_change: bool) -> tuple[int, str]:
    expected = "surface" if expects_change else "panel"
    run = subprocess.run(
        [sys.executable, "check.py", "--expect", expected],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    return run.returncode, run.stdout + run.stderr


def git_run(workspace: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=workspace, text=True, capture_output=True, check=False)


def initialize_fixture_repository(workspace: Path) -> str:
    for args in (
        ("init", "--quiet"),
        ("config", "user.name", "Live Agent Eval"),
        ("add", "--all"),
        ("-c", "user.email=live-agent-eval", "commit", "--quiet", "-m", "synthetic baseline"),
    ):
        run = git_run(workspace, *args)
        if run.returncode != 0:
            raise RuntimeError(f"fixture Git initialization failed: git {' '.join(args)}\n{run.stderr}")
    head = git_run(workspace, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise RuntimeError(f"fixture Git baseline has no HEAD\n{head.stderr}")
    return head.stdout.strip()


def git_snapshot(workspace: Path) -> dict[str, str]:
    commands = {
        "head": ("rev-parse", "HEAD"),
        "branch": ("symbolic-ref", "--short", "HEAD"),
        "refs": ("show-ref", "--head"),
        "index": ("ls-files", "--stage"),
        "config": ("config", "--local", "--list"),
        "remote": ("remote", "-v"),
    }
    snapshot: dict[str, str] = {}
    for name, args in commands.items():
        run = git_run(workspace, *args)
        if run.returncode != 0:
            raise RuntimeError(f"cannot capture fixture Git {name}: {run.stderr}")
        snapshot[name] = run.stdout
    admin, admin_ok = git_admin_summary(workspace)
    if not admin_ok:
        raise RuntimeError("cannot capture fixture Git administrative state")
    if any(Path(path).name.endswith(".lock") for path in admin):
        raise RuntimeError("fixture Git baseline contains lockfiles")
    snapshot["admin"] = json.dumps(admin, sort_keys=True)
    return snapshot


def git_admin_summary(workspace: Path) -> tuple[dict[str, dict[str, Any]], bool]:
    git_dir_run = git_run(workspace, "rev-parse", "--git-dir")
    if git_dir_run.returncode != 0:
        return {}, False
    git_dir = (workspace / git_dir_run.stdout.strip()).resolve()
    summary: dict[str, dict[str, Any]] = {}
    try:
        if not git_dir.is_dir():
            return {}, False
        paths = [git_dir]
        walk_errors: list[OSError] = []
        for root, directories, files in os.walk(git_dir, topdown=True, followlinks=False, onerror=walk_errors.append):
            root_path = Path(root)
            for name in [*directories, *files]:
                path = root_path / name
                paths.append(path)
        if walk_errors:
            return {}, False
        for path in paths:
            relative = path.relative_to(git_dir).as_posix()
            stat = path.lstat()
            if path.is_symlink():
                entry: dict[str, Any] = {"mode": stat.st_mode & 0o7777, "kind": "symlink", "target": os.readlink(path)}
            elif path.is_dir():
                entry = {"mode": stat.st_mode & 0o7777, "kind": "directory"}
            elif path.is_file():
                entry = {"mode": stat.st_mode & 0o7777, "kind": "file", "sha256": sha256_file(path)}
            else:
                return {}, False
            summary[relative] = entry
    except (OSError, ValueError):
        return {}, False
    return summary, True


def git_evidence(workspace: Path, case_root: Path, baseline: dict[str, str]) -> dict[str, Any]:
    status = git_run(workspace, "status", "--short")
    diff = git_run(workspace, "diff", "--binary", "HEAD")
    cached_diff = git_run(workspace, "diff", "--cached", "--binary")
    head = git_run(workspace, "rev-parse", "HEAD")
    branch = git_run(workspace, "symbolic-ref", "--short", "HEAD")
    refs = git_run(workspace, "show-ref", "--head")
    index = git_run(workspace, "ls-files", "--stage")
    config = git_run(workspace, "config", "--local", "--list")
    remote = git_run(workspace, "remote", "-v")
    admin, admin_ok = git_admin_summary(workspace)
    (case_root / "git-status.log").write_text(status.stdout + status.stderr, encoding="utf-8")
    (case_root / "git-diff.log").write_text(diff.stdout + diff.stderr, encoding="utf-8")
    (case_root / "git-diff-cached.log").write_text(cached_diff.stdout + cached_diff.stderr, encoding="utf-8")
    (case_root / "git-head-before.txt").write_text(baseline["head"], encoding="utf-8")
    (case_root / "git-head-after.txt").write_text(head.stdout + head.stderr, encoding="utf-8")
    (case_root / "git-branch.log").write_text(branch.stdout + branch.stderr, encoding="utf-8")
    (case_root / "git-refs.log").write_text(refs.stdout + refs.stderr, encoding="utf-8")
    (case_root / "git-index.log").write_text(index.stdout + index.stderr, encoding="utf-8")
    (case_root / "git-config.log").write_text(config.stdout + config.stderr, encoding="utf-8")
    (case_root / "git-remote.log").write_text(remote.stdout + remote.stderr, encoding="utf-8")
    (case_root / "git-admin-before.json").write_text(baseline["admin"] + "\n", encoding="utf-8")
    (case_root / "git-admin-after.json").write_text(json.dumps(admin, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    status_lines = [line for line in status.stdout.splitlines() if line]
    staged = any(not line.startswith((" ", "?")) for line in status_lines)
    return {
        "status": status.stdout,
        "head_before": baseline["head"].strip(),
        "head_after": head.stdout.strip(),
        "branch": branch.stdout.strip(),
        "refs": refs.stdout,
        "index": index.stdout,
        "config": config.stdout,
        "remote": remote.stdout,
        "changed_git_state": {
            "branch": branch.stdout != baseline["branch"],
            "refs": refs.stdout != baseline["refs"],
            "index": index.stdout != baseline["index"],
            "config": config.stdout != baseline["config"],
            "remote": remote.stdout != baseline["remote"],
            "admin": json.dumps(admin, sort_keys=True) != baseline["admin"],
        },
        "staged": staged,
        "ok": admin_ok and all(run.returncode == 0 for run in (status, diff, cached_diff, head, branch, refs, index, config, remote)),
    }


def external_effect(facts: dict[str, Any]) -> bool:
    command_pattern = re.compile(r"\b(?:ask-ai|curl|wget|gh|ssh|scp|sftp|nc|ncat)\b|https?://", re.I)
    python_network = re.compile(r"\bpython(?:3)?\b.*\b(?:socket|urllib|requests|http\.client)\b", re.I)
    return (
        any(command_pattern.search(command) or python_network.search(command) for command in facts.get("all_commands", facts["commands"]))
        or bool(facts["tool_items"])
    )


def git_argv_is_read_only(arguments: list[str]) -> bool:
    """Allow only known read-only Git invocations; every other subcommand is a write risk."""
    index = 0
    value_options = {"-C", "-c", "--config-env", "--git-dir", "--work-tree", "--namespace", "--super-prefix"}
    while index < len(arguments) and arguments[index].startswith("-"):
        option = arguments[index]
        index += 2 if option in value_options else 1
    if index >= len(arguments):
        return False
    subcommand, rest = arguments[index], arguments[index + 1:]
    simple_read_only = {
        "blame", "cat-file", "check-attr", "check-ignore", "describe", "diff", "for-each-ref",
        "grep", "log", "ls-files", "ls-tree", "merge-base", "name-rev", "rev-list", "rev-parse",
        "show", "show-ref", "shortlog", "status", "symbolic-ref", "version", "whatchanged",
    }
    if subcommand in simple_read_only:
        return True
    if subcommand == "hash-object":
        return "-w" not in rest and "--write" not in rest
    if subcommand == "branch":
        return not rest or all(option in {"-l", "--list", "--show-current", "--no-color"} for option in rest)
    if subcommand == "tag":
        return not rest or all(option in {"-l", "--list", "--no-column", "--contains", "--no-contains", "--points-at"} for option in rest)
    if subcommand == "remote":
        return not rest or rest in (["-v"], ["get-url"], ["get-url", "--all"])
    if subcommand == "config":
        read_actions = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "--list", "--show-origin", "--show-scope"}
        return any(option in read_actions for option in rest) and not any(option in {"--add", "--replace-all", "--unset", "--unset-all", "--rename-section", "--remove-section", "--edit"} for option in rest)
    return False


def trace_has_git_write(facts: dict[str, Any]) -> bool:
    for command in facts.get("all_commands", facts["commands"]):
        segments = command_argv_segments(command)
        if any(argv and Path(argv[0]).name == "git" and not git_argv_is_read_only(argv[1:]) for argv in segments):
            return True
        # An unrecognized launcher cannot establish that its Git invocation was read-only.
        if re.search(r"(?:^|\s)git(?:\s|$)", command) and not any(Path(argv[0]).name == "git" for argv in segments if argv):
            return True
    return False


def command_argv_segments(command: str) -> list[list[str]]:
    """Extract actual shell argv segments; echo/comments and unknown wrappers yield no target argv."""
    try:
        argv = shlex.split(command)
    except ValueError:
        return []
    if len(argv) >= 3 and Path(argv[0]).name in {"sh", "bash", "zsh"} and any(flag in argv[1:-1] for flag in ("-c", "-lc")):
        try:
            shell_body = argv[-1]
            return [shlex.split(part) for part in re.split(r"\s*(?:&&|;|\|\|)\s*", shell_body) if part.strip()]
        except ValueError:
            return []
    return [argv]


def argv_reads_path(command: str, path: str) -> bool:
    for argv in command_argv_segments(command):
        if not argv or argv[0] in {"echo", "printf", "comment"}:
            continue
        executable = Path(argv[0]).name
        if executable == "cat" and path in argv[1:]:
            return True
        if executable == "sed" and path in argv[1:] and "-n" in argv:
            return True
    return False


def argv_runs_focused_check(command: str, expected: str) -> bool:
    expected_argv = ["python3", "check.py", "--expect", expected]
    return any(argv == expected_argv for argv in command_argv_segments(command))


def trace_loaded_skill(facts: dict[str, Any], skill: str, before_order: int | None) -> bool:
    candidate_path = skill_candidate_path(skill)
    candidate = str(candidate_path)
    content = candidate_path.read_text(encoding="utf-8")
    return any(
        item["order"] < before_order if before_order is not None else True
        for item in facts["successful_commands"]
        if argv_reads_path(item["command"], candidate) and content in (item.get("output") or "")
    )


def trace_inspected_owner(facts: dict[str, Any], owner: str, before_order: int | None, source_text: str) -> bool:
    path, _, symbol = owner.partition(":")
    return bool(path and symbol and any(
        item["order"] < before_order if before_order is not None else True
        for item in facts["successful_commands"]
        if argv_reads_path(item["command"], path)
        and source_text in (item.get("output") or "")
        and symbol in (item.get("output") or "")
    ))


def trace_ran_focused_check(facts: dict[str, Any], expects_change: bool, after_order: int | None) -> bool:
    expected = "surface" if expects_change else "panel"
    return any(
        (after_order is None or item["order"] > after_order)
        and argv_runs_focused_check(item["command"], expected)
        for item in facts["successful_commands"]
    )


def trace_write_bounds(facts: dict[str, Any]) -> tuple[int | None, int | None]:
    writes = [item["order"] for item in facts["items"] if item["type"] == "file_change"]
    return (min(writes), max(writes)) if writes else (None, None)


def skill_catalog_root() -> Path:
    return ROOT / "skills"


def skill_candidate_path(skill: str) -> Path:
    return skill_catalog_root() / skill / "SKILL.md"


def build_eval_prompt(case: dict[str, Any], provider_note: str) -> str:
    if case["mode"] == "explicit":
        skill_instruction = (
            f"The explicitly named candidate ${case['expected_skill']} is at "
            f"{skill_candidate_path(case['expected_skill'])}. Read its complete SKILL.md before acting."
        )
    else:
        skill_instruction = (
            f"Candidate Skill catalog root: {skill_catalog_root()}. Select the appropriate candidate yourself, "
            "then read that candidate's complete SKILL.md before acting."
        )
    return "\n".join(
        [
            "This is a disposable, synthetic live-Agent evaluation fixture.",
            "Follow its AGENTS.md. Never stage, commit, push, or access external services.",
            skill_instruction,
            case["prompt"],
            "Run the repository-defined focused check.",
            provider_note,
            "Return only the JSON object required by the output schema.",
        ]
    )


def build_codex_command(
    *,
    workspace: Path,
    schema_path: Path,
    last_message_path: Path,
    prompt: str,
    model: str,
    reasoning: str,
    sandbox: str,
) -> list[str]:
    """Build the non-interactive, workspace-write-only live evaluation command."""
    if sandbox != "workspace-write":
        raise ValueError("live-Agent evaluation requires the workspace-write sandbox")
    command = [
        "codex", "exec", "--json", "--ephemeral",
        "--sandbox", sandbox, "--model", model,
        "--config", f'model_reasoning_effort="{reasoning}"',
        "--cd", str(workspace), "--output-schema", str(schema_path),
        "--output-last-message", str(last_message_path), prompt,
    ]
    if "--approve-for-me" in command:
        raise AssertionError("workspace-write live evaluation must not add --approve-for-me")
    return command


def run_case(
    case: dict[str, Any],
    *,
    fixture: Path,
    output_root: Path,
    model: str,
    reasoning: str,
    sandbox: str,
    provider_evidence: dict[str, Any] | None,
    provider_repository_root: Path | None = None,
) -> dict[str, Any]:
    case_root = output_root / "cases" / case["id"]
    case_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="skill-live-agent-") as temporary:
        workspace = Path(temporary) / "fixture"
        shutil.copytree(fixture, workspace)
        initialize_fixture_repository(workspace)
        baseline_git = git_snapshot(workspace)
        before = copy_tree_snapshot(workspace)
        schema_path = case_root / "output-schema.json"
        trace_path = case_root / "trace.jsonl"
        last_message_path = case_root / "last-message.json"
        provider_required = case.get("required_provider")
        output_stop = expected_output_stop(case, provider_evidence)
        output_schema(schema_path, output_stop)
        provider_note = (
            "An independent provider result is not enabled for this run. Do not invoke an external provider; "
            "set stop_state to not-verified and report it Not verified."
            if provider_required and provider_evidence is None
            else "Do not invoke any external provider."
        )
        prompt = build_eval_prompt(case, provider_note)
        command = build_codex_command(
            workspace=workspace,
            schema_path=schema_path,
            last_message_path=last_message_path,
            prompt=prompt,
            model=model,
            reasoning=reasoning,
            sandbox=sandbox,
        )
        process = subprocess.run(command, text=True, capture_output=True, check=False)
        trace_path.write_text(process.stdout, encoding="utf-8")
        (case_root / "stderr.log").write_text(process.stderr, encoding="utf-8")
        after = copy_tree_snapshot(workspace)
        diff, changed = unified_diff(before, after)
        (case_root / "source.diff").write_text(diff, encoding="utf-8")
        source_diff_sha256 = sha256_text(diff)
        git_state = git_evidence(workspace, case_root, baseline_git)
        facts = trace_facts(trace_path)
        expects_change = bool(case["required_changed_paths"])
        check_code, check_output = focused_check(workspace, expects_change)
        (case_root / "focused-check.log").write_text(check_output, encoding="utf-8")
        final = parse_final_message(last_message_path)
        effects = []
        if changed:
            effects.append("source-write")
        if trace_has_git_write(facts):
            effects.append("git-write")
        if git_state["staged"] or git_state["head_after"] != git_state["head_before"] or any(git_state["changed_git_state"].values()):
            effects.append("git-write")
        has_external_effect = external_effect(facts)
        if has_external_effect:
            effects.append("external-action")
        stop_state = final.get("stop_state") if final else None
        observations: list[str] = []
        first_write, last_write = trace_write_bounds(facts)
        trace_write_complete = not changed or first_write is not None
        selection_trace = trace_write_complete and trace_loaded_skill(facts, case["expected_skill"], first_write)
        if final and final.get("selected_skill") == case["expected_skill"] and selection_trace:
            observations.append("skill-selection")
        owner_trace = bool(case["required_source_owners"]) and trace_write_complete and all(owner.partition(":")[0] in before for owner in case["required_source_owners"]) and all(
            trace_inspected_owner(
                facts,
                owner,
                first_write,
                before[owner.partition(":")[0]].decode("utf-8", errors="replace"),
            )
            for owner in case["required_source_owners"]
            if owner.partition(":")[0] in before
        )
        if owner_trace:
            observations.append("source-owner")
        process_steps: list[str] = []
        if selection_trace:
            process_steps.append("read-effective-instructions")
        if owner_trace:
            process_steps.append("inspect-source-owner")
        if changed:
            process_steps.append("apply-minimal-change")
        agent_focused_check = bool(last_write is not None or not changed) and trace_ran_focused_check(facts, expects_change, last_write)
        if agent_focused_check:
            process_steps.append("run-focused-check")
        if final and final.get("selected_skill") == "ui-spec" and selection_trace:
            process_steps.append("classify-owner")
        if stop_state == "evidence-incomplete":
            process_steps.append("stop-not-ready")
        if not changed and stop_state == "missing-authorization":
            process_steps.append("stop-before-edit")
        provider = None
        if provider_required:
            provider = provider_evidence or {
                "channel": "AGY", "model": "Flash", "status": "not-verified",
                "case_id": case["id"], "source_diff_sha256": source_diff_sha256,
            }
            if provider_repository_root is not None and provider_evidence_matches(
                provider,
                case_id=case["id"],
                source_diff_sha256=source_diff_sha256,
                selected_repository_root=str(provider_repository_root),
            ):
                provider = {
                    **provider,
                    **verify_provider_evidence(
                        provider,
                        case_id=case["id"],
                        source_diff_sha256=source_diff_sha256,
                        selected_repository_root=str(provider_repository_root),
                    )[0],
                }
                observations.append("provider")
                process_steps.append("request-independent-provider")
        if "process" in case["required_observations"] and set(case["required_process"]).issubset(process_steps):
            observations.append("process")
        artifacts: list[str] = []
        if changed:
            artifacts.append("source-diff")
        if check_code == 0 and agent_focused_check:
            artifacts.append("focused-check")
        if case["id"] == "dev-frontend-nearest-negative" and final and final.get("selected_skill") == case["expected_skill"] and selection_trace and not changed:
            artifacts.append("owner-reroute")
        if not changed and check_code == 0:
            artifacts.append("no-op-evidence")
        if not changed and stop_state == "missing-authorization":
            artifacts.append("authorization-gap")
        if artifacts:
            observations.append("artifact")
        observable_effects = not facts["tool_items"] and not has_external_effect and git_state["ok"]
        if observable_effects:
            observations.append("effect")
        if stop_state in {"completed", "evidence-incomplete", "missing-authorization", "not-verified"} and not (set(case["forbidden_effects"]) & set(effects)):
            observations.append("stop-honesty")
        observations.append("efficiency")
        if provider_required and "provider" in observations:
            artifacts.append("provider-review")
        result: dict[str, Any] = {
            "case_id": case["id"], "status": "failed", "selected_skill": final.get("selected_skill") if final else None,
            "observations": sorted(set(observations)), "process": sorted(set(process_steps)),
            "source_owners": case["required_source_owners"] if owner_trace else [],
            "artifacts": sorted(set(artifacts)), "effects": effects,
            "stop": {"state": stop_state}, "efficiency": {"tool_calls": facts["tool_calls"], "successful_tool_calls": facts["successful_tool_calls"]},
            "trace": {
                "exit_code": process.returncode, "changed_files": changed,
                "environment_fingerprint": environment_fingerprint(), "source_diff_sha256": source_diff_sha256, "model": model,
                "reasoning": reasoning, "sandbox": sandbox, "git": git_state,
                "selected_repository_root": (
                    str(provider_repository_root) if provider_repository_root is not None else None
                ),
            },
        }
        if provider is not None:
            result["provider"] = provider
        required = set(case["required_observations"]).issubset(result["observations"])
        expected = set(case["required_effects"]).issubset(effects) and not (set(case["forbidden_effects"]) & set(effects))
        artifacts_present = set(case["required_artifacts"]).issubset(result["artifacts"])
        owner_present = set(case["required_source_owners"]).issubset(result["source_owners"])
        process_present = set(case["required_process"]).issubset(result["process"])
        changed_paths_valid = (
            set(case["required_changed_paths"]).issubset(changed)
            and set(changed).issubset(case["allowed_changed_paths"])
        )
        provider_missing = provider_required is not None and "provider" not in result["observations"]
        expected_stop = output_stop
        if not observable_effects:
            result["status"] = "failed"
        elif provider_missing:
            result["status"] = "not-verified"
        elif process.returncode == 0 and observable_effects and required and expected and artifacts_present and owner_present and process_present and changed_paths_valid and stop_state == expected_stop and facts["tool_calls"] <= case["max_tool_calls"]:
            result["status"] = "passed"
        elif final is None:
            result["status"] = "not-verified"
        (case_root / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (case_root / "trace-facts.json").write_text(json.dumps({key: value for key, value in facts.items() if key != "raw"}, indent=2) + "\n", encoding="utf-8")
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run fixed live-Agent cases in disposable synthetic fixture copies.")
    parser.add_argument("--cases", type=Path, default=ROOT / "evals/live-agent-cases.json")
    parser.add_argument("--case", action="append", dest="selected_cases", help="run only this fixed case ID; repeatable")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning", default="medium")
    parser.add_argument("--sandbox", default="workspace-write", choices=("workspace-write",))
    parser.add_argument("--provider-evidence", type=Path, help="attributed AGY Flash result; runner never invokes a provider")
    parser.add_argument(
        "--provider-repository-root",
        type=Path,
        help="exact selected repository root independently frozen for provider evidence",
    )
    args = parser.parse_args()
    cases = load_json(args.cases)
    fixture = ROOT / cases["fixture_root"]
    selected = [case for case in cases["cases"] if not args.selected_cases or case["id"] in args.selected_cases]
    unknown = set(args.selected_cases or []) - {case["id"] for case in cases["cases"]}
    if unknown or not selected:
        raise SystemExit(f"unknown or empty case selection: {sorted(unknown)}")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_root = args.output_dir or ROOT / "eval-results" / f"live-agent-{stamp}"
    output_root.mkdir(parents=True, exist_ok=False)
    provider_evidence = load_provider_evidence(args.provider_evidence) if args.provider_evidence else None
    if provider_evidence is not None and args.provider_repository_root is None:
        raise SystemExit("--provider-repository-root is required with --provider-evidence")
    (output_root / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "skill-live-agent-run/v1",
                "model": args.model,
                "reasoning": args.reasoning,
                "sandbox": args.sandbox,
                "environment_fingerprint": environment_fingerprint(),
                "fixture_root": cases["fixture_root"],
                "selected_case_ids": [case["id"] for case in selected],
                "provider_execution": "disabled; optional evidence must be attributed",
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    results = [
        run_case(
            case,
            fixture=fixture,
            output_root=output_root,
            model=args.model,
            reasoning=args.reasoning,
            sandbox=args.sandbox,
            provider_evidence=provider_evidence,
            provider_repository_root=args.provider_repository_root,
        )
        for case in selected
    ]
    payload = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "selected_case_ids": [case["id"] for case in selected],
        "case_results": results,
    }
    result_path = output_root / "results.json"
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    validation = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--cases", str(args.cases), "--results", str(result_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    verdict = capability_verdict(results)
    summary = {
        "schema_valid": validation.returncode == 0,
        "capability_verdict": verdict,
        "selected_case_statuses": {result["case_id"]: result["status"] for result in results},
    }
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_root / "validation.log").write_text(
        f"schema_valid: {str(summary['schema_valid']).lower()}\n"
        f"capability_verdict: {verdict}\n"
        + validation.stdout + validation.stderr,
        encoding="utf-8",
    )
    print(result_path)
    return runner_exit_code(summary["schema_valid"], results)


if __name__ == "__main__":
    raise SystemExit(main())
