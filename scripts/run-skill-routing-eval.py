#!/usr/bin/env python3
"""Run reproducible, prompt-only native Skill routing evaluations.

The runner is dry-run by default. It invokes Codex or Claude only when
``--execute`` is present, and it never sends evaluator labels to the host.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "evals" / "routing.jsonl"
DEFAULT_OUTPUT_ROOT = ROOT / "eval-results" / "routing"
PROTOCOL_PATH = ROOT / "scripts" / "evaluation_protocol.py"
_PROTOCOL_SPEC = importlib.util.spec_from_file_location(
    "aicraft_evaluation_protocol_for_runner", PROTOCOL_PATH
)
if _PROTOCOL_SPEC is None or _PROTOCOL_SPEC.loader is None:
    raise RuntimeError(f"cannot load evaluation protocol from {PROTOCOL_PATH}")
PROTOCOL = importlib.util.module_from_spec(_PROTOCOL_SPEC)
sys.modules[_PROTOCOL_SPEC.name] = PROTOCOL
_PROTOCOL_SPEC.loader.exec_module(PROTOCOL)
CONTRACTS = PROTOCOL.load_contract(ROOT)
BEHAVIOR_CONTRACT = CONTRACTS["behavior_eval"]
RESULT_SCHEMA_VERSION = int(BEHAVIOR_CONTRACT["result_schema_version"])
RAW_SCHEMA_VERSION = int(BEHAVIOR_CONTRACT["raw_evidence_schema_version"])
PROMPT_TEMPLATE_VERSION = int(BEHAVIOR_CONTRACT["prompt_template_version"])
PROMPT_VALUE_PLACEHOLDER = "<NATURAL_REQUEST_JSON>"
RUNNER_VERSION = str(
    BEHAVIOR_CONTRACT["evaluation_protocol"]["canonical_routing"][
        "reviewer_version"
    ]
)
OWNER_ENUM = PROTOCOL.OWNER_ENUM
VARIANTS = ("candidate", "previous", "baseline")
HOSTS = ("codex", "claude")
TASK_FIXTURE_DESCRIPTOR = {
    "schema_version": 1,
    "repository": "empty isolated Git repository",
    "tracked_files": [],
    "task": "prompt-only routing selection",
    "skill_packages_excluded": True,
}

ROUTING_RESPONSE_SCHEMA: dict[str, object] = PROTOCOL.routing_response_schema()


class RunnerError(ValueError):
    """Raised for invalid configuration or an unsafe/incomplete run."""


@dataclass(frozen=True)
class GitRevision:
    commit: str
    skills_tree: str


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str


@dataclass(frozen=True)
class RunConfig:
    host: str
    variant: str
    trial: int
    comparison_group_id: str
    campaign_id: str | None
    campaign_path_relative: str | None
    campaign_sha256: str | None
    evaluation_protocol_revision: str | None
    evaluation_protocol_sha256: str | None
    held_out: bool
    model: str
    timeout_seconds: int
    concurrency: int
    output_root: Path
    dataset_path: Path
    dataset_path_relative: str
    dataset_sha256: str
    dataset_git_revision: str | None
    evaluation_anchor_revision: str | None
    held_out_provenance_path_relative: str | None
    held_out_provenance_sha256: str | None
    revision: GitRevision
    cases: tuple[EvalCase, ...]


@dataclass(frozen=True)
class CaseOutcome:
    case_id: str
    raw_path: Path
    raw_sha256: str
    prompt_sha256: str
    observations: dict[str, object] | None
    duration_ms: int
    input_tokens: int | None
    output_tokens: int | None
    attempt_count: int
    retry_count: int
    exit_code: int
    error: str | None

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0 and self.error is None and self.observations is not None


@dataclass(frozen=True)
class RunOutcome:
    run_id: str
    run_dir: Path
    bundle_path: Path | None
    failure_path: Path | None

    @property
    def succeeded(self) -> bool:
        return self.bundle_path is not None


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _reject_duplicate_json_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise RunnerError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _git_text(arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise RunnerError(detail)
    return completed.stdout.strip()


def _git_bytes(arguments: Sequence[str]) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RunnerError(stderr or "git command failed")
    return completed.stdout


def resolve_revision(revision_spec: str) -> GitRevision:
    commit = _git_text(["rev-parse", "--verify", f"{revision_spec}^{{commit}}"])
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RunnerError(f"resolved Skill revision is not a full Git commit: {commit!r}")
    skills_tree = _git_text(["rev-parse", "--verify", f"{commit}:skills"])
    if re.fullmatch(r"[0-9a-f]{40}", skills_tree) is None:
        raise RunnerError(f"resolved skills tree is not a Git tree: {skills_tree!r}")
    tracked = _git_text(["ls-tree", "-r", "--name-only", commit, "--", "skills"])
    discovered = {
        parts[1]
        for line in tracked.splitlines()
        if (parts := PurePosixPath(line).parts)
        and len(parts) == 3
        and parts[0] == "skills"
        and parts[2] == "SKILL.md"
    }
    if discovered != set(OWNER_ENUM):
        missing = sorted(set(OWNER_ENUM) - discovered)
        extra = sorted(discovered - set(OWNER_ENUM))
        raise RunnerError(
            f"Skill revision must contain the fixed 14-package inventory; "
            f"missing={missing}, extra={extra}"
        )
    return GitRevision(commit=commit, skills_tree=skills_tree)


def _repository_dataset_path(value: str) -> tuple[Path, str]:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RunnerError("--dataset must resolve inside the current repository") from error
    if not resolved.is_file():
        raise RunnerError(f"dataset does not exist: {resolved}")
    return resolved, relative.as_posix()


def _cli_path(value: str | Path) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else ROOT / path).resolve()


def _repository_provenance_path(value: str) -> tuple[Path, str]:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RunnerError("--provenance must resolve inside the current repository") from error
    if not resolved.is_file():
        raise RunnerError(f"provenance does not exist: {resolved}")
    return resolved, relative.as_posix()


def _committed_dataset_revision(dataset_path: Path, relative_path: str) -> str:
    revision = _git_text(["log", "-1", "--format=%H", "--", relative_path])
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise RunnerError(
            "held-out dataset must be added in a committed repository revision"
        )
    committed = _git_bytes(["show", f"{revision}:{relative_path}"])
    if committed != dataset_path.read_bytes():
        raise RunnerError(
            "held-out dataset content must exactly match its latest committed revision"
        )
    return revision


def _load_cases(dataset_path: Path, requested_ids: Sequence[str]) -> tuple[EvalCase, ...]:
    rows: list[EvalCase] = []
    seen_ids: set[str] = set()
    for line_number, raw in enumerate(dataset_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw, object_pairs_hook=_reject_duplicate_json_keys)
        except (json.JSONDecodeError, RunnerError) as error:
            raise RunnerError(f"{dataset_path}:{line_number}: invalid JSON: {error}") from error
        if not isinstance(item, dict):
            raise RunnerError(f"{dataset_path}:{line_number}: row must be an object")
        case_id = item.get("id")
        prompt = item.get("prompt")
        if not isinstance(case_id, str) or re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*", case_id
        ) is None:
            raise RunnerError(f"{dataset_path}:{line_number}: unsafe or missing case id")
        if case_id in seen_ids:
            raise RunnerError(f"{dataset_path}:{line_number}: duplicate case id {case_id}")
        if not isinstance(prompt, str) or not prompt.strip():
            raise RunnerError(f"{dataset_path}:{line_number}: prompt must be non-empty")
        leaked = [owner for owner in OWNER_ENUM if owner.casefold() in prompt.casefold()]
        if leaked:
            raise RunnerError(f"{case_id}: natural request leaks Skill name(s) {leaked}")
        seen_ids.add(case_id)
        rows.append(EvalCase(case_id=case_id, prompt=prompt))

    explicit = list(requested_ids)
    if len(explicit) != len(set(explicit)):
        raise RunnerError("explicit case list must not contain duplicates")
    if explicit:
        unknown = sorted(set(explicit) - seen_ids)
        if unknown:
            raise RunnerError(f"unknown case id(s): {unknown}")
        selected = set(explicit)
        rows = [case for case in rows if case.case_id in selected]
    if not rows:
        raise RunnerError("no routing cases selected")
    return tuple(rows)


def _load_dataset_rows(dataset_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, raw in enumerate(
        dataset_path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw, object_pairs_hook=_reject_duplicate_json_keys)
        except (json.JSONDecodeError, RunnerError) as error:
            raise RunnerError(
                f"{dataset_path}:{line_number}: invalid JSON: {error}"
            ) from error
        if not isinstance(item, dict):
            raise RunnerError(f"{dataset_path}:{line_number}: row must be an object")
        rows.append(item)
    return rows


def _contract_validator_module():
    module_name = "_aicraft_eval_skill_contracts"
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    path = ROOT / "scripts" / "eval-skill-contracts.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RunnerError(f"cannot load contract validator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _validate_dataset_contract(
    dataset_path: Path,
    rows: list[dict[str, object]],
    *,
    held_out: bool,
) -> None:
    validator = _contract_validator_module()
    known_skills = set(OWNER_ENUM)
    if held_out:
        errors = validator.validate_held_out_routing_cases(rows, known_skills)
    else:
        errors = validator.validate_routing_cases(
            rows,
            known_skills,
            routing_graph_path=ROOT / "docs" / "skills" / "routing-graph.json",
        )
    if errors:
        rendered = "\n".join(f"- {error}" for error in errors)
        raise RunnerError(f"routing dataset contract failed for {dataset_path}:\n{rendered}")


def build_prompt(natural_request: str) -> str:
    """Build the label-free prompt sent identically to either host."""

    request = json.dumps(natural_request, ensure_ascii=False)
    return _prompt_template().replace(PROMPT_VALUE_PLACEHOLDER, request)


def _prompt_template() -> str:
    return PROTOCOL.canonical_prompt_template(CONTRACTS)


def _host_policy(host: str, model: str) -> dict[str, object]:
    return PROTOCOL.canonical_host_policy(host, model, CONTRACTS)


def _response_schema_hash() -> str:
    return str(PROTOCOL.canonical_adjudication(CONTRACTS)["config_sha256"])


def _task_fixture_hash() -> str:
    return _sha256_text(_canonical_json(TASK_FIXTURE_DESCRIPTOR))


def _case_set_hash(cases: Sequence[EvalCase]) -> str:
    value = [{"id": case.case_id, "prompt_sha256": _sha256_text(case.prompt)} for case in cases]
    return _sha256_text(_canonical_json(value))


def _parse_case_options(case_values: Sequence[str], cases_value: str | None) -> list[str]:
    parsed = list(case_values)
    if cases_value:
        parsed.extend(part.strip() for part in cases_value.split(",") if part.strip())
    return parsed


def _materialize_skill_fixture(revision: GitRevision, destination: Path) -> str:
    """Export tracked Skill blobs from one committed tree without reading the worktree."""

    raw_tree = _git_bytes(["ls-tree", "-r", "-z", revision.commit, "--", "skills"])
    digest = hashlib.sha256()
    seen_skill_docs: set[str] = set()
    for record in raw_tree.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode, object_type, object_sha = metadata.decode("ascii").split(" ")
            path_text = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise RunnerError("cannot parse committed skills tree") from error
        path = PurePosixPath(path_text)
        if path.parts in {("skills", "AGENTS.md"), ("skills", "CLAUDE.md")}:
            # Repository authoring policies do not belong in installed packages.
            continue
        if (
            object_type != "blob"
            or mode not in {"100644", "100755"}
            or path.is_absolute()
            or len(path.parts) < 3
            or path.parts[0] != "skills"
            or path.parts[1] not in OWNER_ENUM
            or ".." in path.parts
            or path.as_posix() != path_text
        ):
            raise RunnerError(f"unsupported or unsafe committed Skill entry: {path_text!r}")
        if path.name == "SKILL.md" and len(path.parts) == 3:
            seen_skill_docs.add(path.parts[1])
        content = _git_bytes(["cat-file", "blob", object_sha])
        relative = Path(*path.parts[1:])
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        target.chmod(0o755 if mode == "100755" else 0o644)
        digest.update(path_text.encode("utf-8") + b"\0")
        digest.update(mode.encode("ascii") + b"\0")
        digest.update(content)
        digest.update(b"\0")
    if seen_skill_docs != set(OWNER_ENUM):
        raise RunnerError("exported fixture does not contain the fixed 14-package inventory")
    return digest.hexdigest()


def _prepare_case_repo(
    repo: Path,
    *,
    host: str,
    variant: str,
    skill_fixture: Path | None,
) -> Path:
    repo.mkdir(parents=True, exist_ok=False)
    initialized = subprocess.run(
        ["git", "init", "--quiet", "--template=", str(repo)],
        check=False,
        capture_output=True,
        text=True,
    )
    if initialized.returncode != 0:
        raise RunnerError(initialized.stderr.strip() or "cannot initialize isolated Git fixture")
    skill_root = repo / (".agents/skills" if host == "codex" else ".claude/skills")
    if variant in {"candidate", "previous"}:
        if skill_fixture is None:
            raise RunnerError("candidate/previous run requires a committed Skill fixture")
        skill_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_fixture, skill_root)
    return skill_root


def _copy_auth_file(source: Path, destination: Path) -> None:
    """Copy one credential file without carrying user configuration or Skills."""

    if not source.is_file():
        return
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    destination.parent.chmod(0o700)
    shutil.copyfile(source, destination)
    destination.chmod(0o600)


def _isolated_host_environment(host: str, isolated_home: Path) -> dict[str, str]:
    """Return a host environment whose global config and Skill roots are empty."""

    source_environment = os.environ.copy()
    source_home = Path(source_environment.get("HOME", str(Path.home()))).expanduser()
    source_codex_home = Path(
        source_environment.get("CODEX_HOME", str(source_home / ".codex"))
    ).expanduser()
    source_claude_home = Path(
        source_environment.get("CLAUDE_CONFIG_DIR", str(source_home / ".claude"))
    ).expanduser()

    isolated_home.mkdir(parents=True, exist_ok=False, mode=0o700)
    isolated_home.chmod(0o700)
    xdg_root = isolated_home / ".xdg"
    for name in ("config", "data", "cache"):
        (xdg_root / name).mkdir(parents=True, mode=0o700)

    environment_policy = PROTOCOL.canonical_environment_policy(host, CONTRACTS)
    environment = {
        key: source_environment[key]
        for key in environment_policy["source_allowlist"]
        if key in source_environment
    }
    environment.update(
        {
            "CI": "1",
            "HOME": str(isolated_home),
            "NO_COLOR": "1",
            "TERM": "dumb",
            "XDG_CACHE_HOME": str(xdg_root / "cache"),
            "XDG_CONFIG_HOME": str(xdg_root / "config"),
            "XDG_DATA_HOME": str(xdg_root / "data"),
        }
    )

    if host == "codex":
        codex_home = isolated_home / ".codex"
        codex_home.mkdir(mode=0o700)
        _copy_auth_file(source_codex_home / "auth.json", codex_home / "auth.json")
        environment["CODEX_HOME"] = str(codex_home)
    else:
        claude_home = isolated_home / ".claude"
        claude_home.mkdir(mode=0o700)
        _copy_auth_file(
            source_claude_home / ".credentials.json",
            claude_home / ".credentials.json",
        )
        environment["CLAUDE_CONFIG_DIR"] = str(claude_home)
        environment["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    return environment


def _host_command(
    config: RunConfig,
    *,
    repo: Path,
    schema_path: Path,
    response_path: Path,
    prompt: str,
) -> list[str]:
    if config.host == "codex":
        return [
            "codex",
            "exec",
            "--disable",
            "remote_plugin",
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--json",
            "--color",
            "never",
            "--config",
            'approval_policy="never"',
            "--cd",
            str(repo),
            "--model",
            config.model,
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(response_path),
            prompt,
        ]
    return [
        "claude",
        "--print",
        "--model",
        config.model,
        "--output-format",
        "json",
        "--json-schema",
        _canonical_json(ROUTING_RESPONSE_SCHEMA),
        "--tools",
        "",
        "--no-session-persistence",
        "--setting-sources",
        "project",
        "--permission-mode",
        "dontAsk",
        "--no-chrome",
        "--strict-mcp-config",
        "--mcp-config",
        "{}",
        prompt,
    ]


def _routing_object(value: object) -> dict[str, object] | None:
    return PROTOCOL.routing_observation(value)


def _json_value(text: str) -> object | None:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_json_keys)
    except (TypeError, json.JSONDecodeError, RunnerError):
        return None


def _extract_model_output(stdout: str, response_path: Path) -> tuple[str, dict[str, object]]:
    response = (
        response_path.read_text(encoding="utf-8")
        if response_path.is_file()
        else ""
    )
    extracted = PROTOCOL.extract_routing_result(stdout, response)
    if extracted is None:
        raise RunnerError("host response did not contain valid structured routing JSON")
    return extracted


def _extract_usage(stdout: str, *, host: str) -> tuple[int | None, int | None]:
    values: list[object] = []
    whole = _json_value(stdout)
    if whole is not None:
        values.append(whole)
    else:
        values.extend(
            parsed
            for line in stdout.splitlines()
            if (parsed := _json_value(line)) is not None
        )
    usages: list[tuple[int | None, int | None]] = []

    def visit(value: object) -> None:
        if isinstance(value, dict):
            input_tokens = value.get("input_tokens")
            output_tokens = value.get("output_tokens")
            if (
                isinstance(input_tokens, int)
                and not isinstance(input_tokens, bool)
                and input_tokens > 0
                and isinstance(output_tokens, int)
                and not isinstance(output_tokens, bool)
                and output_tokens > 0
            ):
                normalized_input_tokens = input_tokens
                if host == "claude":
                    cache_tokens = 0
                    for field in (
                        "cache_creation_input_tokens",
                        "cache_read_input_tokens",
                    ):
                        value_for_field = value.get(field)
                        if value_for_field is None:
                            continue
                        if (
                            isinstance(value_for_field, bool)
                            or not isinstance(value_for_field, int)
                            or value_for_field < 0
                        ):
                            usages.append((None, None))
                            break
                        cache_tokens += value_for_field
                    else:
                        usages.append(
                            (normalized_input_tokens + cache_tokens, output_tokens)
                        )
                else:
                    # OpenAI cached-input fields are subsets of input_tokens and
                    # must not be added a second time.
                    usages.append((normalized_input_tokens, output_tokens))
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for value in values:
        visit(value)
    return usages[-1] if usages else (None, None)


def _transcript(stdout: str, stderr: str) -> str:
    return f"STDOUT\n{stdout}\nSTDERR\n{stderr}"


def _retryable_error_class(
    host: str,
    *,
    exit_code: int,
    stdout: str,
    stderr: str,
    observations: dict[str, object] | None,
    input_tokens: int | None,
    output_tokens: int | None,
) -> str | None:
    return PROTOCOL.classify_transient_host_failure(
        host,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        has_valid_result=observations is not None,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        contract=CONTRACTS,
    )


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_bytes(encoded)
    os.replace(temporary, path)


def _invoke_case(
    config: RunConfig,
    case: EvalCase,
    *,
    run_id: str,
    host_version: str,
    temp_root: Path,
    skill_fixture: Path | None,
    raw_root: Path,
) -> CaseOutcome:
    started_at = _utc_now()
    start = time.monotonic()
    stdout = ""
    stderr = ""
    model_output = ""
    observations: dict[str, object] | None = None
    exit_code = 1
    error: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    prompt = build_prompt(case.prompt)
    retry_policy = PROTOCOL.canonical_transient_retry_policy(config.host, CONTRACTS)
    retry_policy_sha256 = PROTOCOL.canonical_hash(retry_policy)
    maximum_attempts = int(retry_policy["maximum_attempts_per_case"])
    backoff_seconds = list(retry_policy["backoff_seconds"])
    host_attempts: list[dict[str, object]] = []
    raw_path = raw_root / f"{case.case_id}.json"

    def raw_snapshot(
        *, snapshot_completed_at: str, snapshot_duration_ms: int
    ) -> dict[str, object]:
        transcript = _transcript(stdout, stderr)
        return {
            "schema_version": RAW_SCHEMA_VERSION,
            "run_id": run_id,
            "case_id": case.case_id,
            "prompt_sha256": _sha256_text(case.prompt),
            "invocation_prompt": prompt,
            "invocation_prompt_sha256": _sha256_text(prompt),
            "model": config.model,
            "host": host_version,
            "started_at": started_at,
            "completed_at": snapshot_completed_at,
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "response": model_output,
            "model_output": model_output,
            "transcript": transcript,
            "transcript_sha256": _sha256_text(transcript),
            "retry_policy_sha256": retry_policy_sha256,
            "host_attempts": host_attempts,
            "observations": observations or {"actual_owner": "", "handoffs": []},
            "metrics": {
                "duration_ms": snapshot_duration_ms,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "attempt_count": len(host_attempts),
                "retry_count": len(host_attempts) - 1,
            },
            **({"error": error} if error is not None else {}),
        }

    for attempt_index in range(1, maximum_attempts + 1):
        attempt_started_at = _utc_now()
        attempt_start = time.monotonic()
        attempt_stdout = ""
        attempt_stderr = ""
        attempt_response = ""
        attempt_model_output = ""
        attempt_observations: dict[str, object] | None = None
        attempt_exit_code = 1
        attempt_error: str | None = None
        attempt_input_tokens: int | None = None
        attempt_output_tokens: int | None = None
        attempt_root = temp_root / "cases" / case.case_id / f"attempt-{attempt_index}"
        try:
            _prepare_case_repo(
                attempt_root,
                host=config.host,
                variant=config.variant,
                skill_fixture=skill_fixture,
            )
            schema_path = attempt_root / ".routing-response-schema.json"
            response_path = attempt_root / ".routing-response.json"
            _write_json(schema_path, ROUTING_RESPONSE_SCHEMA)
            command = _host_command(
                config,
                repo=attempt_root,
                schema_path=schema_path,
                response_path=response_path,
                prompt=prompt,
            )
            environment = _isolated_host_environment(
                config.host,
                temp_root / "homes" / case.case_id / f"attempt-{attempt_index}",
            )
            completed = subprocess.run(
                command,
                cwd=attempt_root,
                check=False,
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                timeout=config.timeout_seconds,
                env=environment,
            )
            attempt_stdout = completed.stdout or ""
            attempt_stderr = completed.stderr or ""
            attempt_exit_code = completed.returncode
            if response_path.is_file():
                attempt_response = response_path.read_text(encoding="utf-8")
            try:
                attempt_model_output, attempt_observations = _extract_model_output(
                    attempt_stdout, response_path
                )
            except (OSError, UnicodeDecodeError, RunnerError) as caught:
                attempt_error = str(caught)
            attempt_input_tokens, attempt_output_tokens = _extract_usage(
                attempt_stdout, host=config.host
            )
            if attempt_exit_code != 0:
                attempt_error = f"host exited with code {attempt_exit_code}"
        except subprocess.TimeoutExpired as timeout:
            attempt_exit_code = 124
            attempt_stdout = (
                timeout.stdout.decode("utf-8", errors="replace")
                if isinstance(timeout.stdout, bytes)
                else (timeout.stdout or "")
            )
            attempt_stderr = (
                timeout.stderr.decode("utf-8", errors="replace")
                if isinstance(timeout.stderr, bytes)
                else (timeout.stderr or "")
            )
            attempt_error = f"host timed out after {config.timeout_seconds} seconds"
        except (OSError, UnicodeDecodeError, RunnerError) as caught:
            attempt_error = str(caught)

        error_class = _retryable_error_class(
            config.host,
            exit_code=attempt_exit_code,
            stdout=attempt_stdout,
            stderr=attempt_stderr,
            observations=attempt_observations,
            input_tokens=attempt_input_tokens,
            output_tokens=attempt_output_tokens,
        )
        retryable = error_class is not None
        will_retry = retryable and attempt_index < maximum_attempts
        backoff_before_next = (
            int(backoff_seconds[attempt_index - 1]) if will_retry else 0
        )
        attempt_duration_ms = max(
            1, round((time.monotonic() - attempt_start) * 1000)
        )
        attempt_completed_at = _utc_now()
        attempt_transcript = _transcript(attempt_stdout, attempt_stderr)
        host_attempts.append(
            {
                "attempt_index": attempt_index,
                "started_at": attempt_started_at,
                "completed_at": attempt_completed_at,
                "duration_ms": attempt_duration_ms,
                "exit_code": attempt_exit_code,
                "stdout": attempt_stdout,
                "stderr": attempt_stderr,
                "response": attempt_response,
                "model_output": attempt_model_output,
                "transcript": attempt_transcript,
                "transcript_sha256": _sha256_text(attempt_transcript),
                "error_class": error_class,
                "error": attempt_error,
                "retryable": retryable,
                "backoff_seconds_before_next": backoff_before_next,
                "observations": attempt_observations,
                "metrics": {
                    "duration_ms": attempt_duration_ms,
                    "input_tokens": attempt_input_tokens,
                    "output_tokens": attempt_output_tokens,
                },
            }
        )
        stdout = attempt_stdout
        stderr = attempt_stderr
        model_output = attempt_model_output
        observations = attempt_observations
        exit_code = attempt_exit_code
        error = attempt_error
        input_tokens = attempt_input_tokens
        output_tokens = attempt_output_tokens
        checkpoint_duration_ms = max(
            1, round((time.monotonic() - start) * 1000)
        )
        _write_json(
            raw_path,
            raw_snapshot(
                snapshot_completed_at=attempt_completed_at,
                snapshot_duration_ms=checkpoint_duration_ms,
            ),
        )
        if not will_retry:
            break
        time.sleep(backoff_before_next)

    duration_ms = max(1, round((time.monotonic() - start) * 1000))
    completed_at = _utc_now()
    raw = raw_snapshot(
        snapshot_completed_at=completed_at,
        snapshot_duration_ms=duration_ms,
    )
    _write_json(raw_path, raw)
    raw_hash = _sha256_bytes(raw_path.read_bytes())
    return CaseOutcome(
        case_id=case.case_id,
        raw_path=raw_path,
        raw_sha256=raw_hash,
        prompt_sha256=_sha256_text(case.prompt),
        observations=observations,
        duration_ms=duration_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        attempt_count=len(host_attempts),
        retry_count=len(host_attempts) - 1,
        exit_code=exit_code,
        error=error,
    )


def _host_version(host: str, timeout_seconds: int) -> str:
    try:
        completed = subprocess.run(
            [host, "--version"],
            check=False,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=min(timeout_seconds, 30),
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RunnerError(f"cannot read {host} version: {error}") from error
    if completed.returncode != 0:
        raise RunnerError(completed.stderr.strip() or f"cannot read {host} version")
    version = completed.stdout.strip() or completed.stderr.strip()
    if not version:
        raise RunnerError(f"{host} --version returned no version")
    return version


def _validate_written_bundle(bundle_path: Path, config: RunConfig) -> None:
    """Load and score the runner's own output through the production evaluator."""

    validator = _contract_validator_module()
    cases = validator.load_jsonl(config.dataset_path)
    expected_ids = {str(case["id"]) for case in cases}
    expected_prompts = {str(case["id"]): str(case["prompt"]) for case in cases}
    loaded = validator.load_result_bundle(
        bundle_path,
        expected_ids,
        config.dataset_path,
        expected_prompts,
        evidence_kind="routing",
    )
    validator.score_routing(cases, loaded)


def _run_evaluation_attempt(
    config: RunConfig,
    *,
    run_id: str,
    run_dir: Path,
    attempt_id: str,
    attempt_started_at: str,
) -> RunOutcome:
    """Execute one reserved campaign attempt."""

    raw_root = run_dir / "raw" / "routing"
    raw_root.mkdir(parents=True)
    host_version = _host_version(config.host, config.timeout_seconds)
    host_policy = _host_policy(config.host, config.model)
    host_config_sha256 = _sha256_text(_canonical_json(host_policy))
    skill_fixture: Path | None = None

    with tempfile.TemporaryDirectory(prefix="aicraft-routing-eval-") as temporary:
        temp_root = Path(temporary)
        if config.variant in {"candidate", "previous"}:
            skill_fixture = temp_root / "committed-skills"
            skill_fixture.mkdir()
            skill_fixture_sha256: str | None = _materialize_skill_fixture(
                config.revision, skill_fixture
            )
        else:
            skill_fixture_sha256 = None

        outcomes_by_id: dict[str, CaseOutcome] = {}
        with ThreadPoolExecutor(max_workers=config.concurrency) as executor:
            futures = {
                executor.submit(
                    _invoke_case,
                    config,
                    case,
                    run_id=run_id,
                    host_version=host_version,
                    temp_root=temp_root,
                    skill_fixture=skill_fixture,
                    raw_root=raw_root,
                ): case.case_id
                for case in config.cases
            }
            for future in as_completed(futures):
                case_id = futures[future]
                try:
                    outcomes_by_id[case_id] = future.result()
                except Exception as error:
                    # Preserve an unexpected worker failure without a bundle.
                    failure_path = run_dir / "run-failure.json"
                    _write_json(
                        failure_path,
                        {
                            "schema_version": 1,
                            "complete": False,
                            "run_id": run_id,
                            "failed_cases": [case_id],
                            "error": f"worker failed: {error}",
                        },
                    )
                    return RunOutcome(run_id, run_dir, None, failure_path)

    ordered = [outcomes_by_id[case.case_id] for case in config.cases]
    failed = [outcome for outcome in ordered if not outcome.succeeded]
    if failed:
        failure_path = run_dir / "run-failure.json"
        _write_json(
            failure_path,
            {
                "schema_version": 1,
                "complete": False,
                "run_id": run_id,
                "host": host_version,
                "model": config.model,
                "skill_revision": config.revision.commit,
                "skill_tree_sha": config.revision.skills_tree,
                "dataset_revision": config.dataset_sha256,
                "failed_cases": [
                    {
                        "id": outcome.case_id,
                        "exit_code": outcome.exit_code,
                        "error": outcome.error or "invalid structured response",
                        "raw_evidence": outcome.raw_path.relative_to(run_dir).as_posix(),
                        "raw_evidence_sha256": outcome.raw_sha256,
                    }
                    for outcome in failed
                ],
            },
        )
        return RunOutcome(run_id, run_dir, None, failure_path)

    permissions = str(host_policy["permissions"])
    bundle = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "complete": True,
        "run_id": run_id,
        "model": config.model,
        "host": host_version,
        "skill_revision": config.revision.commit,
        "skill_tree_sha": config.revision.skills_tree,
        "dataset_revision": config.dataset_sha256,
        "captured_at": _utc_now(),
        "run_config": {
            "variant": config.variant,
            "trial": config.trial,
            "comparison_group_id": config.comparison_group_id,
            "attempt_id": attempt_id,
            "attempt_path": "attempt.json",
            "campaign_id": config.campaign_id,
            "campaign_path": config.campaign_path_relative,
            "campaign_sha256": config.campaign_sha256,
            "evaluation_protocol_revision": config.evaluation_protocol_revision,
            "evaluation_protocol_sha256": config.evaluation_protocol_sha256,
            "held_out": config.held_out,
            "dataset_path": config.dataset_path_relative,
            "dataset_git_revision": config.dataset_git_revision,
            "evaluation_anchor_revision": config.evaluation_anchor_revision,
            "held_out_provenance_path": config.held_out_provenance_path_relative,
            "held_out_provenance_sha256": config.held_out_provenance_sha256,
            "prompt_set_sha256": config.dataset_sha256,
            "case_set_sha256": _case_set_hash(config.cases),
            "case_ids": [case.case_id for case in config.cases],
            "permissions": permissions,
            "timeout_seconds": config.timeout_seconds,
            "concurrency": config.concurrency,
            "fixture_sha256": _task_fixture_hash(),
            "fixture": TASK_FIXTURE_DESCRIPTOR,
            "skill_fixture_sha256": skill_fixture_sha256,
            "host_config_sha256": host_config_sha256,
            "environment_policy_sha256": PROTOCOL.canonical_hash(
                PROTOCOL.canonical_environment_policy(config.host, CONTRACTS)
            ),
            "retry_policy_sha256": PROTOCOL.canonical_hash(
                PROTOCOL.canonical_transient_retry_policy(config.host, CONTRACTS)
            ),
            "host_name": config.host,
            "prompt_template_version": PROMPT_TEMPLATE_VERSION,
            "prompt_template": _prompt_template(),
            "prompt_template_sha256": _sha256_text(_prompt_template()),
            "skills_installed": config.variant in {"candidate", "previous"},
            "skill_install_root": ".agents/skills" if config.host == "codex" else ".claude/skills",
            "isolation": (
                "committed export; unique repository and isolated HOME per host attempt; "
                "remote_plugin disabled"
                if config.host == "codex"
                else "committed export; unique repository and isolated HOME per host attempt; "
                "strict empty MCP configuration"
            ),
        },
        "adjudication": PROTOCOL.canonical_adjudication(CONTRACTS),
        "results": [
            {
                "id": outcome.case_id,
                "prompt_sha256": outcome.prompt_sha256,
                "observations": outcome.observations,
                "actual_owner": outcome.observations["actual_owner"],
                "handoffs": outcome.observations["handoffs"],
                "raw_evidence": outcome.raw_path.relative_to(run_dir).as_posix(),
                "raw_evidence_sha256": outcome.raw_sha256,
                "metrics": {
                    "duration_ms": outcome.duration_ms,
                    "input_tokens": outcome.input_tokens,
                    "output_tokens": outcome.output_tokens,
                    "attempt_count": outcome.attempt_count,
                    "retry_count": outcome.retry_count,
                },
            }
            for outcome in ordered
            if outcome.observations is not None
        ],
    }
    bundle_path = run_dir / "routing-results.json"
    _write_json(bundle_path, bundle)
    _write_attempt_ledger(
        run_dir / "attempt.json",
        config,
        attempt_id=attempt_id,
        run_id=run_id,
        started_at=attempt_started_at,
        status="success",
        artifact=bundle_path,
    )
    try:
        _validate_written_bundle(bundle_path, config)
    except (OSError, ValueError, RunnerError) as error:
        bundle_path.unlink(missing_ok=True)
        failure_path = run_dir / "run-failure.json"
        _write_json(
            failure_path,
            {
                "schema_version": 1,
                "complete": False,
                "run_id": run_id,
                "error": f"generated bundle failed self-validation: {error}",
            },
        )
        return RunOutcome(run_id, run_dir, None, failure_path)
    return RunOutcome(run_id, run_dir, bundle_path, None)


def _assert_campaign_attempt_unused(config: RunConfig) -> None:
    if config.campaign_id is None or not config.output_root.exists():
        return
    for path in config.output_root.resolve().glob("*/attempt.json"):
        try:
            payload = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise RunnerError(f"cannot audit existing attempt ledger {path}: {error}") from error
        if not isinstance(payload, dict):
            raise RunnerError(f"existing attempt ledger is not an object: {path}")
        if (
            payload.get("campaign_id") == config.campaign_id
            and payload.get("trial") == config.trial
            and payload.get("variant") == config.variant
        ):
            raise RunnerError(
                "campaign trial/variant already has an attempt; failed attempts consume "
                "the slot and require a new campaign"
            )


def _write_attempt_ledger(
    path: Path,
    config: RunConfig,
    *,
    attempt_id: str,
    run_id: str,
    started_at: str,
    status: str,
    artifact: Path | None,
) -> None:
    artifact_relative = artifact.relative_to(path.parent).as_posix() if artifact else None
    _write_json(
        path,
        {
            "schema_version": int(BEHAVIOR_CONTRACT["attempt_schema_version"]),
            "attempt_id": attempt_id,
            "campaign_id": config.campaign_id,
            "trial": config.trial,
            "variant": config.variant,
            "comparison_group_id": config.comparison_group_id,
            "started_at": started_at,
            "completed_at": _utc_now() if status != "running" else None,
            "status": status,
            "run_id": run_id,
            "artifact": artifact_relative,
            "artifact_sha256": (
                _sha256_bytes(artifact.read_bytes()) if artifact is not None else None
            ),
        },
    )


def run_evaluation(config: RunConfig) -> RunOutcome:
    """Reserve and execute one auditable campaign attempt."""

    _assert_campaign_attempt_unused(config)
    run_id = str(uuid.uuid4())
    attempt_id = str(uuid.uuid4())
    run_dir = config.output_root.resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    attempt_path = run_dir / "attempt.json"
    started_at = _utc_now()
    _write_attempt_ledger(
        attempt_path,
        config,
        attempt_id=attempt_id,
        run_id=run_id,
        started_at=started_at,
        status="running",
        artifact=None,
    )
    try:
        outcome = _run_evaluation_attempt(
            config,
            run_id=run_id,
            run_dir=run_dir,
            attempt_id=attempt_id,
            attempt_started_at=started_at,
        )
    except Exception as error:
        failure_path = run_dir / "run-failure.json"
        _write_json(
            failure_path,
            {
                "schema_version": 1,
                "complete": False,
                "run_id": run_id,
                "campaign_id": config.campaign_id,
                "trial": config.trial,
                "variant": config.variant,
                "comparison_group_id": config.comparison_group_id,
                "error": f"unhandled evaluation failure: {error}",
            },
        )
        outcome = RunOutcome(run_id, run_dir, None, failure_path)
    artifact = outcome.bundle_path or outcome.failure_path
    _write_attempt_ledger(
        attempt_path,
        config,
        attempt_id=attempt_id,
        run_id=run_id,
        started_at=started_at,
        status="success" if outcome.succeeded else "failure",
        artifact=artifact,
    )
    return outcome


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=HOSTS, required=True)
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    parser.add_argument("--trial", type=_positive_integer, default=1)
    parser.add_argument(
        "--comparison-group-id",
        help=(
            "UUID shared by every matched candidate, previous, and no-Skill "
            "baseline run for this trial."
        ),
    )
    parser.add_argument(
        "--campaign",
        help=(
            "Committed post-anchor campaign JSON required for formal held-out "
            "execution."
        ),
    )
    parser.add_argument("--held-out", action="store_true")
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=_positive_integer, default=120, dest="timeout_seconds")
    parser.add_argument("--concurrency", type=_positive_integer, default=1)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dataset")
    parser.add_argument(
        "--provenance",
        help="Committed provenance JSON required for a held-out execution.",
    )
    parser.add_argument(
        "--evaluation-anchor-revision",
        help="Frozen candidate Skill revision shared by every held-out variant.",
    )
    parser.add_argument("--case", action="append", default=[], dest="case_values")
    parser.add_argument("--cases", help="comma-separated explicit case ids")
    parser.add_argument("--skill-revision", "--skills-revision")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="invoke the selected model CLI; omitted means dry-run",
    )
    return parser


def _configuration_from_args(arguments: argparse.Namespace) -> RunConfig:
    campaign = None
    output_root = arguments.output_dir or DEFAULT_OUTPUT_ROOT
    if arguments.campaign:
        campaign_path, _ = _repository_provenance_path(arguments.campaign)
        try:
            campaign = PROTOCOL.load_campaign(ROOT, campaign_path, CONTRACTS)
        except PROTOCOL.ProtocolError as error:
            raise RunnerError(str(error)) from error
        if not arguments.held_out:
            raise RunnerError("--campaign requires --held-out")
        condition = campaign.payload["condition"]
        for key, actual in (
            ("host_name", arguments.host),
            ("model", arguments.model),
            ("timeout_seconds", arguments.timeout_seconds),
            ("concurrency", arguments.concurrency),
        ):
            if condition[key] != actual:
                raise RunnerError(
                    f"--{key.replace('_', '-')} must match the campaign value"
                )
        dataset_spec = str(campaign.payload["dataset"]["path"])
        provenance_spec = str(campaign.payload["provenance"]["path"])
        if (
            arguments.dataset is not None
            and _cli_path(arguments.dataset) != (ROOT / dataset_spec).resolve()
        ):
            raise RunnerError("--dataset must match the campaign dataset path")
        if arguments.provenance and _cli_path(arguments.provenance) != (
            ROOT / provenance_spec
        ).resolve():
            raise RunnerError("--provenance must match the campaign provenance path")
        arguments.dataset = dataset_spec
        arguments.provenance = provenance_spec
        arguments.evaluation_anchor_revision = campaign.anchor_revision
        expected_output_root = (ROOT / campaign.artifact_root).resolve()
        if (
            arguments.output_dir is not None
            and _cli_path(arguments.output_dir) != expected_output_root
        ):
            raise RunnerError("--output-dir must match the campaign artifact_root")
        output_root = expected_output_root
    elif arguments.held_out and arguments.execute:
        raise RunnerError("formal --held-out --execute requires --campaign")

    if arguments.dataset is None:
        arguments.dataset = str(DEFAULT_DATASET)

    dataset_path, dataset_relative = _repository_dataset_path(arguments.dataset)
    dataset_rows = _load_dataset_rows(dataset_path)
    _validate_dataset_contract(
        dataset_path,
        dataset_rows,
        held_out=arguments.held_out,
    )
    requested_ids = _parse_case_options(arguments.case_values, arguments.cases)
    if arguments.execute and requested_ids:
        raise RunnerError(
            "--execute requires the complete selected dataset; create a dedicated "
            "dataset file instead of using --case/--cases"
        )
    cases = _load_cases(dataset_path, requested_ids)
    revision_spec = arguments.skill_revision or "HEAD"
    if campaign is not None:
        expected_revision = PROTOCOL.expected_revision_for_variant(
            campaign, arguments.variant
        )
        if arguments.skill_revision is not None:
            supplied_revision = resolve_revision(arguments.skill_revision)
            if supplied_revision.commit != expected_revision:
                raise RunnerError("--skill-revision does not match the campaign variant")
        revision_spec = expected_revision
    revision = resolve_revision(revision_spec)
    comparison_group_id = arguments.comparison_group_id
    if campaign is not None:
        declared_groups = campaign.trial_groups
        if arguments.trial not in declared_groups:
            raise RunnerError("--trial is not declared by the campaign")
        declared_group = declared_groups[arguments.trial]
        if comparison_group_id is not None and comparison_group_id != declared_group:
            raise RunnerError("--comparison-group-id does not match the campaign trial")
        comparison_group_id = declared_group
    elif comparison_group_id is None:
        if arguments.execute:
            raise RunnerError(
                "--execute requires --comparison-group-id with a shared trial UUID"
            )
        comparison_group_id = "00000000-0000-4000-8000-000000000000"
    try:
        uuid.UUID(comparison_group_id)
    except ValueError as error:
        raise RunnerError("--comparison-group-id must be a UUID") from error
    if arguments.execute:
        aliases = {"auto", "default", "latest", "opus", "sonnet", "haiku", "fable"}
        if arguments.model.casefold() in aliases or not any(
            character.isdigit() for character in arguments.model
        ):
            raise RunnerError(
                "--execute requires a versioned model identifier, not a mutable alias"
            )
    dataset_git_revision: str | None = None
    evaluation_anchor_revision: str | None = None
    provenance_relative: str | None = None
    provenance_sha256: str | None = None
    if arguments.held_out:
        if not arguments.provenance:
            raise RunnerError("--held-out requires --provenance")
        if not arguments.evaluation_anchor_revision:
            raise RunnerError("--held-out requires --evaluation-anchor-revision")
        if dataset_path.resolve() == DEFAULT_DATASET.resolve():
            raise RunnerError("the public routing dataset cannot be marked held-out")
        provenance_path, provenance_relative = _repository_provenance_path(
            arguments.provenance
        )
        provenance_sha256 = _sha256_bytes(provenance_path.read_bytes())
        evaluation_anchor_revision = _git_text(
            [
                "rev-parse",
                "--verify",
                f"{arguments.evaluation_anchor_revision}^{{commit}}",
            ]
        )
        if re.fullmatch(r"[0-9a-f]{40}", evaluation_anchor_revision) is None:
            raise RunnerError("--evaluation-anchor-revision must resolve to a full commit")
        dataset_git_revision = _committed_dataset_revision(
            dataset_path, dataset_relative
        )
        if campaign is not None:
            expected_dataset = campaign.payload["dataset"]
            expected_provenance = campaign.payload["provenance"]
            if dataset_git_revision != expected_dataset["git_revision"]:
                raise RunnerError("dataset Git revision does not match the campaign")
            if _sha256_bytes(dataset_path.read_bytes()) != expected_dataset["sha256"]:
                raise RunnerError("dataset hash does not match the campaign")
            if provenance_sha256 != expected_provenance["sha256"]:
                raise RunnerError("provenance hash does not match the campaign")
        validator = _contract_validator_module()
        validator._validate_held_out_provenance(
            dataset_path,
            revision.commit,
            {
                "variant": arguments.variant,
                "dataset_path": dataset_relative,
                "dataset_git_revision": dataset_git_revision,
                "evaluation_anchor_revision": evaluation_anchor_revision,
                "held_out_provenance_path": provenance_relative,
                "held_out_provenance_sha256": provenance_sha256,
                "host_name": arguments.host,
            },
            bundle_path=Path("dry-run"),
        )
    elif arguments.provenance or arguments.evaluation_anchor_revision:
        raise RunnerError(
            "--provenance and --evaluation-anchor-revision are only valid with --held-out"
        )
    return RunConfig(
        host=arguments.host,
        variant=arguments.variant,
        trial=arguments.trial,
        comparison_group_id=comparison_group_id,
        campaign_id=campaign.campaign_id if campaign is not None else None,
        campaign_path_relative=(
            campaign.relative_path if campaign is not None else None
        ),
        campaign_sha256=campaign.sha256 if campaign is not None else None,
        evaluation_protocol_revision=(
            campaign.anchor_revision if campaign is not None else None
        ),
        evaluation_protocol_sha256=(
            str(campaign.payload["evaluation_protocol"]["sha256"])
            if campaign is not None
            else None
        ),
        held_out=arguments.held_out,
        model=arguments.model,
        timeout_seconds=arguments.timeout_seconds,
        concurrency=arguments.concurrency,
        output_root=output_root,
        dataset_path=dataset_path,
        dataset_path_relative=dataset_relative,
        dataset_sha256=_sha256_bytes(dataset_path.read_bytes()),
        dataset_git_revision=dataset_git_revision,
        evaluation_anchor_revision=evaluation_anchor_revision,
        held_out_provenance_path_relative=provenance_relative,
        held_out_provenance_sha256=provenance_sha256,
        revision=revision,
        cases=cases,
    )


def _dry_run_plan(config: RunConfig) -> dict[str, object]:
    policy = _host_policy(config.host, config.model)
    return {
        "execute": False,
        "host": config.host,
        "model": config.model,
        "variant": config.variant,
        "trial": config.trial,
        "comparison_group_id": config.comparison_group_id,
        "campaign_id": config.campaign_id,
        "campaign_path": config.campaign_path_relative,
        "campaign_sha256": config.campaign_sha256,
        "evaluation_protocol_revision": config.evaluation_protocol_revision,
        "evaluation_protocol_sha256": config.evaluation_protocol_sha256,
        "held_out": config.held_out,
        "dataset_path": config.dataset_path_relative,
        "dataset_revision": config.dataset_sha256,
        "dataset_git_revision": config.dataset_git_revision,
        "evaluation_anchor_revision": config.evaluation_anchor_revision,
        "held_out_provenance_path": config.held_out_provenance_path_relative,
        "held_out_provenance_sha256": config.held_out_provenance_sha256,
        "case_ids": [case.case_id for case in config.cases],
        "skill_revision": config.revision.commit,
        "skill_tree_sha": config.revision.skills_tree,
        "skills_installed": config.variant in {"candidate", "previous"},
        "fixture_sha256": _task_fixture_hash(),
        "host_config_sha256": _sha256_text(_canonical_json(policy)),
        "environment_policy_sha256": PROTOCOL.canonical_hash(
            PROTOCOL.canonical_environment_policy(config.host, CONTRACTS)
        ),
        "timeout_seconds": config.timeout_seconds,
        "concurrency": config.concurrency,
        "output_root": str(config.output_root.resolve()),
        "note": "dry-run only; no model CLI was invoked",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    try:
        arguments = parser.parse_args(argv)
        config = _configuration_from_args(arguments)
        if not arguments.execute:
            print(json.dumps(_dry_run_plan(config), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        outcome = run_evaluation(config)
        summary = {
            "complete": outcome.succeeded,
            "run_id": outcome.run_id,
            "run_dir": str(outcome.run_dir),
            "bundle": str(outcome.bundle_path) if outcome.bundle_path else None,
            "failure": str(outcome.failure_path) if outcome.failure_path else None,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if outcome.succeeded else 1
    except (RunnerError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
