#!/usr/bin/env python3
"""Canonical campaign and protocol primitives for formal routing evaluations.

This module is deliberately small and dependency-free. Formal held-out runs,
scoring, comparison, and evidence replay all rebuild the same prompt,
adjudication, host, environment, and protocol identities from these functions.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unicodedata
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence


CONTRACT_PATH = "contracts/skill-validation.json"
OWNER_ENUM = (
    "audit-frontend",
    "audit-rust",
    "audit-security",
    "chatgpt-review",
    "code-planner",
    "design-ui",
    "diagnose",
    "domain-modeling",
    "human-writing",
    "implement-frontend",
    "implement-rust",
    "ops-browser",
    "ops-client",
    "repo-delivery",
    "repo-map",
    "repo-review",
)
PROMPT_VALUE_PLACEHOLDER = "<NATURAL_REQUEST_JSON>"


class ProtocolError(ValueError):
    """Raised when a campaign or frozen evaluation protocol is invalid."""


@dataclass(frozen=True)
class Campaign:
    payload: dict[str, object]
    path: Path
    relative_path: str
    sha256: str
    commit: str

    @property
    def campaign_id(self) -> str:
        return str(self.payload["campaign_id"])

    @property
    def anchor_revision(self) -> str:
        return str(self.payload["evaluation_anchor_revision"])

    @property
    def previous_revision(self) -> str:
        return str(self.payload["previous_skill_revision"])

    @property
    def artifact_root(self) -> str:
        return str(self.payload["artifact_root"])

    @property
    def trial_groups(self) -> dict[int, str]:
        return {
            int(item["trial"]): str(item["comparison_group_id"])
            for item in self.payload["trials"]
        }


def reject_duplicate_json_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def canonical_json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def canonical_prompt_fingerprint(value: str) -> str:
    """Fingerprint prompts after low-level textual normalization.

    This catches case, Unicode compatibility, and whitespace-only rewrites. It
    deliberately does not claim semantic paraphrase detection.
    """

    normalized = unicodedata.normalize("NFKC", value)
    normalized = " ".join(normalized.strip().split()).casefold()
    return sha256_text(normalized)


def canonical_hash(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_contract(root: Path) -> dict[str, object]:
    path = root / CONTRACT_PATH
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ProtocolError(f"cannot read evaluation contract: {error}") from error
    if not isinstance(payload, dict):
        raise ProtocolError("evaluation contract must contain an object")
    return payload


def _behavior(contract: Mapping[str, object]) -> Mapping[str, object]:
    value = contract.get("behavior_eval")
    if not isinstance(value, dict):
        raise ProtocolError("contract.behavior_eval must be an object")
    return value


def _protocol_contract(contract: Mapping[str, object]) -> Mapping[str, object]:
    value = _behavior(contract).get("evaluation_protocol")
    if not isinstance(value, dict):
        raise ProtocolError("contract evaluation_protocol must be an object")
    return value


def routing_response_schema() -> dict[str, object]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "actual_owner": {"type": "string", "enum": list(OWNER_ENUM)},
            "handoffs": {
                "type": "array",
                "items": {"type": "string", "enum": list(OWNER_ENUM)},
            },
        },
        "required": ["actual_owner", "handoffs"],
    }


def routing_observation(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict) or set(value) != {"actual_owner", "handoffs"}:
        return None
    owner = value.get("actual_owner")
    handoffs = value.get("handoffs")
    if owner not in OWNER_ENUM:
        return None
    if (
        not isinstance(handoffs, list)
        or any(item not in OWNER_ENUM for item in handoffs)
        or len(handoffs) != len(set(handoffs))
        or owner in handoffs
    ):
        return None
    return {"actual_owner": owner, "handoffs": handoffs}


def _routing_response_candidates(
    value: object,
) -> list[tuple[str, dict[str, object]]]:
    candidates: list[tuple[str, dict[str, object]]] = []
    routed = routing_observation(value)
    if routed is not None:
        candidates.append((canonical_json(routed), routed))
    if isinstance(value, dict):
        for key in ("structured_output", "result", "text"):
            child = value.get(key)
            if isinstance(child, str):
                try:
                    parsed = json.loads(
                        child, object_pairs_hook=reject_duplicate_json_keys
                    )
                except (json.JSONDecodeError, ProtocolError):
                    parsed = None
                routed_child = routing_observation(parsed)
                if routed_child is not None:
                    candidates.append((child, routed_child))
            elif child is not None:
                candidates.extend(_routing_response_candidates(child))
        for key, child in value.items():
            if key not in {"structured_output", "result", "text"}:
                candidates.extend(_routing_response_candidates(child))
    elif isinstance(value, list):
        for child in value:
            candidates.extend(_routing_response_candidates(child))
    return candidates


def extract_routing_result(
    stdout: str, response: str
) -> tuple[str, dict[str, object]] | None:
    """Rebuild the same strict routing result used by runner and validator."""

    if not isinstance(stdout, str) or not isinstance(response, str):
        raise ProtocolError("routing stdout and response must be strings")
    if response:
        try:
            parsed_response = json.loads(
                response, object_pairs_hook=reject_duplicate_json_keys
            )
        except (json.JSONDecodeError, ProtocolError):
            parsed_response = None
        routed = routing_observation(parsed_response)
        if routed is not None:
            return response, routed

    parsed_values, valid = _parse_json_or_jsonl(stdout)
    if not valid:
        return None
    candidates: list[tuple[str, dict[str, object]]] = []
    for value in parsed_values:
        candidates.extend(_routing_response_candidates(value))
    return candidates[-1] if candidates else None


def canonical_prompt_template(contract: Mapping[str, object]) -> str:
    del contract
    owners = canonical_json(list(OWNER_ENUM))
    return (
        "Route this natural request to one primary owner and zero or more necessary "
        "handoff owners.\n"
        "Primary owner: the published Skill responsible for the requested outcome, "
        "including its authorization boundary and next externally meaningful state.\n"
        "Handoff owner: another published Skill that must actually execute a bounded "
        "part of this current request or own a clearly requested subsequent phase.\n"
        "Do not list optional recommendations, alternatives, internal support the "
        "primary owner can perform, or unrequested future work as handoffs. If the "
        "primary owner can complete the requested outcome alone, return an empty "
        "handoffs array.\n"
        f"Natural request: {PROMPT_VALUE_PLACEHOLDER}\n"
        f"Owner enum: {owners}\n"
        "Return only JSON with keys actual_owner and handoffs."
    )


def canonical_adjudication(contract: Mapping[str, object]) -> dict[str, object]:
    routing = _protocol_contract(contract).get("canonical_routing")
    if not isinstance(routing, dict):
        raise ProtocolError("canonical_routing must be an object")
    config = {
        "schema_version": 1,
        "response_schema": routing_response_schema(),
        "parser": "strict JSON; reject duplicate keys and extra fields",
        "mapping": {
            "actual_owner": "observations.actual_owner",
            "handoffs": "observations.handoffs",
        },
        "reject_primary_owner_handoff": True,
    }
    return {
        "method": "deterministic",
        "reviewer": routing.get("reviewer"),
        "reviewer_version": routing.get("reviewer_version"),
        "config_sha256": canonical_hash(config),
    }


def canonical_environment_policy(
    host: str, contract: Mapping[str, object]
) -> dict[str, object]:
    routing = _protocol_contract(contract).get("canonical_routing")
    if not isinstance(routing, dict):
        raise ProtocolError("canonical_routing must be an object")
    allowlist = routing.get("environment_source_allowlist")
    if not isinstance(allowlist, list) or any(
        not isinstance(item, str) or not item for item in allowlist
    ):
        raise ProtocolError("environment_source_allowlist must be a string list")
    if len(allowlist) != len(set(allowlist)) or allowlist != sorted(allowlist):
        raise ProtocolError("environment_source_allowlist must be sorted and unique")
    if host not in {"codex", "claude"}:
        raise ProtocolError(f"unsupported host {host!r}")
    return {
        "schema_version": routing.get("environment_policy_version"),
        "source_allowlist": list(allowlist),
        "fixed_overrides": {
            "CI": "1",
            "HOME": "<ISOLATED_HOME>",
            "NO_COLOR": "1",
            "TERM": "dumb",
            "XDG_CACHE_HOME": "<ISOLATED_XDG_CACHE>",
            "XDG_CONFIG_HOME": "<ISOLATED_XDG_CONFIG>",
            "XDG_DATA_HOME": "<ISOLATED_XDG_DATA>",
            **(
                {"CODEX_HOME": "<ISOLATED_CODEX_HOME>"}
                if host == "codex"
                else {
                    "CLAUDE_CONFIG_DIR": "<ISOLATED_CLAUDE_HOME>",
                    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
                }
            ),
        },
        "credentials": (
            "copy CODEX_HOME/auth.json only"
            if host == "codex"
            else "copy CLAUDE_CONFIG_DIR/.credentials.json only"
        ),
        "record_values": False,
    }


def canonical_transient_retry_policy(
    host: str, contract: Mapping[str, object]
) -> dict[str, object]:
    """Return the frozen host-specific transient retry policy.

    This deliberately accepts one narrowly defined transient class.  Any
    change to the retry count, backoff, or classifier entries must change the
    canonical host policy hash and therefore invalidate an existing campaign.
    """

    if host not in {"codex", "claude"}:
        raise ProtocolError(f"unsupported host {host!r}")
    routing = _protocol_contract(contract).get("canonical_routing")
    if not isinstance(routing, dict):
        raise ProtocolError("canonical_routing must be an object")
    policy = routing.get("transient_retry_policy")
    if not isinstance(policy, dict):
        raise ProtocolError("transient_retry_policy must be an object")
    required_fields = {
        "schema_version",
        "maximum_attempts_per_case",
        "backoff_seconds",
        "retryable_errors",
    }
    if set(policy) != required_fields:
        raise ProtocolError(
            "transient_retry_policy fields must be "
            f"{sorted(required_fields)}"
        )

    schema_version = policy["schema_version"]
    if isinstance(schema_version, bool) or schema_version != 1:
        raise ProtocolError("transient_retry_policy schema_version must be 1")
    maximum_attempts = policy["maximum_attempts_per_case"]
    if isinstance(maximum_attempts, bool) or maximum_attempts != 2:
        raise ProtocolError(
            "transient_retry_policy maximum_attempts_per_case must be 2"
        )
    backoff_seconds = policy["backoff_seconds"]
    if (
        not isinstance(backoff_seconds, list)
        or any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in backoff_seconds
        )
        or backoff_seconds != [5]
    ):
        raise ProtocolError(
            "transient_retry_policy backoff_seconds must be [5]"
        )

    expected_entries: dict[str, list[dict[str, object]]] = {
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
    }
    retryable_errors = policy["retryable_errors"]
    if not isinstance(retryable_errors, dict) or set(retryable_errors) != set(
        expected_entries
    ):
        raise ProtocolError(
            "transient_retry_policy retryable_errors must contain exactly "
            "claude and codex entries"
        )
    entry_fields = {
        "error_class",
        "exit_codes",
        "json_fields",
        "normalized_values",
    }
    for host_name, entries in retryable_errors.items():
        if not isinstance(entries, list):
            raise ProtocolError(
                f"transient_retry_policy retryable_errors[{host_name!r}] "
                "must be a list"
            )
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != entry_fields:
                raise ProtocolError(
                    "transient_retry_policy retryable error fields must be "
                    f"{sorted(entry_fields)}"
                )
            if not isinstance(entry["error_class"], str) or not entry["error_class"]:
                raise ProtocolError(
                    "transient_retry_policy error_class must be a non-empty string"
                )
            exit_codes = entry["exit_codes"]
            if (
                not isinstance(exit_codes, list)
                or not exit_codes
                or any(
                    isinstance(code, bool) or not isinstance(code, int) or code < 1
                    for code in exit_codes
                )
                or len(exit_codes) != len(set(exit_codes))
            ):
                raise ProtocolError(
                    "transient_retry_policy exit_codes must be unique positive integers"
                )
            for field in ("json_fields", "normalized_values"):
                value = entry[field]
                if not isinstance(value, list) or any(
                    not isinstance(item, str) or not item for item in value
                ):
                    raise ProtocolError(
                        f"transient_retry_policy {field} must be a string list"
                    )
    if retryable_errors != expected_entries:
        raise ProtocolError(
            "transient_retry_policy retryable_errors are not canonical"
        )

    return {
        "schema_version": 1,
        "maximum_attempts_per_case": 2,
        "backoff_seconds": [5],
        "retryable_errors": [dict(entry) for entry in expected_entries[host]],
    }


def _normalized_retry_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    return " ".join(normalized.strip().split()).casefold()


def _parse_json_or_jsonl(text: str) -> tuple[list[object], bool]:
    """Parse a JSON value or JSONL stream, rejecting duplicate-key payloads."""

    if not text.strip():
        return [], True
    try:
        return [json.loads(text, object_pairs_hook=reject_duplicate_json_keys)], True
    except json.JSONDecodeError:
        values: list[object] = []
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                values.append(
                    json.loads(line, object_pairs_hook=reject_duplicate_json_keys)
                )
            except json.JSONDecodeError:
                return [], False
            except ProtocolError:
                return [], False
        return values, True
    except ProtocolError:
        return [], False


def _iter_retry_field_values(value: object, json_fields: set[str]):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in json_fields and isinstance(child, str):
                yield child
            yield from _iter_retry_field_values(child, json_fields)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_retry_field_values(child, json_fields)


def _contains_exposed_token_count(value: object) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"input_tokens", "output_tokens"} and child is not None:
                return True
            if _contains_exposed_token_count(child):
                return True
    elif isinstance(value, list):
        return any(_contains_exposed_token_count(child) for child in value)
    return False


def classify_transient_host_failure(
    host: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    has_valid_result: bool,
    input_tokens: int | None,
    output_tokens: int | None,
    contract: Mapping[str, object],
) -> str | None:
    """Classify only a policy-approved, retryable host failure.

    The classifier fails closed: invalid JSON, duplicate keys, token-bearing
    failures, valid routing output, and all non-canonical messages return
    ``None``.
    """

    if isinstance(exit_code, bool) or not isinstance(exit_code, int):
        raise ProtocolError("host exit_code must be an integer")
    if not isinstance(has_valid_result, bool):
        raise ProtocolError("has_valid_result must be boolean")
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        raise ProtocolError("host stdout and stderr must be strings")
    if exit_code == 0 or has_valid_result:
        return None
    if input_tokens is not None or output_tokens is not None:
        return None

    policy = canonical_transient_retry_policy(host, contract)
    streams: list[object] = []
    for text in (stdout, stderr):
        parsed, valid = _parse_json_or_jsonl(text)
        if not valid:
            return None
        streams.extend(parsed)
    if any(_contains_exposed_token_count(parsed) for parsed in streams):
        return None
    for rule in policy["retryable_errors"]:
        if exit_code not in rule["exit_codes"]:
            continue
        json_fields = set(rule["json_fields"])
        normalized_values = set(rule["normalized_values"])
        for parsed in streams:
            for value in _iter_retry_field_values(parsed, json_fields):
                if _normalized_retry_text(value) in normalized_values:
                    return str(rule["error_class"])
    return None


def canonical_host_policy(
    host: str, model: str, contract: Mapping[str, object]
) -> dict[str, object]:
    behavior = _behavior(contract)
    prompt = canonical_prompt_template(contract)
    environment = canonical_environment_policy(host, contract)
    common: dict[str, object] = {
        "schema_version": 2,
        "host": host,
        "model": model,
        "prompt_template_version": behavior.get("prompt_template_version"),
        "prompt_template_sha256": sha256_text(prompt),
        "owner_enum": list(OWNER_ENUM),
        "response_schema": routing_response_schema(),
        "environment_policy_sha256": canonical_hash(environment),
        "transient_retry_policy": canonical_transient_retry_policy(host, contract),
        "environment_isolation": {
            "home": "unique temporary directory per host attempt",
            "xdg_roots": "unique temporary directories per host attempt",
            "global_skill_roots": "excluded",
            "remote_plugin": (
                "disabled by explicit Codex CLI feature override"
                if host == "codex"
                else "not applicable; strict empty MCP configuration enforced"
            ),
            "credentials": "auth files only; no user config or Skill packages",
            "project_skill_root": (
                ".agents/skills" if host == "codex" else ".claude/skills"
            ),
        },
    }
    if host == "codex":
        common["command_template"] = [
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
            "<CASE_REPO>",
            "--model",
            "<MODEL>",
            "--output-schema",
            "<SCHEMA_PATH>",
            "--output-last-message",
            "<RESPONSE_PATH>",
            "<LABEL_FREE_PROMPT>",
        ]
        common["permissions"] = (
            "read-only; never-approve; ephemeral; ignore-user-config; "
            "remote-plugin-disabled"
        )
    else:
        common["command_template"] = [
            "claude",
            "--print",
            "--model",
            "<MODEL>",
            "--output-format",
            "json",
            "--json-schema",
            "<RESPONSE_SCHEMA>",
            "--tools",
            "<EMPTY>",
            "--no-session-persistence",
            "--setting-sources",
            "project",
            "--permission-mode",
            "dontAsk",
            "--no-chrome",
            "--strict-mcp-config",
            "--mcp-config",
            "{}",
            "<LABEL_FREE_PROMPT>",
        ]
        common["permissions"] = (
            "tools-disabled; no-session-persistence; project-settings-only"
        )
    return common


def protocol_files(contract: Mapping[str, object]) -> tuple[str, ...]:
    values = _protocol_contract(contract).get("files")
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise ProtocolError("evaluation_protocol.files must be a string list")
    if len(values) != len(set(values)) or values != sorted(values):
        raise ProtocolError("evaluation_protocol.files must be sorted and unique")
    for value in values:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
            raise ProtocolError(f"unsafe evaluation protocol path {value!r}")
    return tuple(values)


def _git(root: Path, arguments: Sequence[str], *, binary: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=not binary,
    )
    if completed.returncode != 0:
        stderr = (
            completed.stderr.decode("utf-8", errors="replace")
            if binary
            else completed.stderr
        )
        stdout = (
            completed.stdout.decode("utf-8", errors="replace")
            if binary
            else completed.stdout
        )
        raise ProtocolError((stderr or stdout or "git command failed").strip())
    return completed.stdout


def resolve_commit(root: Path, revision: str) -> str:
    value = str(_git(root, ["rev-parse", "--verify", f"{revision}^{{commit}}"])).strip()
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise ProtocolError(f"revision is not a full Git commit: {value!r}")
    return value


def revision_is_ancestor(
    root: Path, ancestor: str, descendant: str, *, strict: bool
) -> bool:
    ancestor = resolve_commit(root, ancestor)
    descendant = resolve_commit(root, descendant)
    if strict and ancestor == descendant:
        return False
    completed = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
        check=False,
        capture_output=True,
    )
    if completed.returncode not in {0, 1}:
        raise ProtocolError("cannot verify Git ancestry")
    return completed.returncode == 0


def protocol_manifest_from_revision(
    root: Path, revision: str, contract: Mapping[str, object]
) -> list[dict[str, str]]:
    revision = resolve_commit(root, revision)
    manifest: list[dict[str, str]] = []
    for path in protocol_files(contract):
        content = _git(root, ["show", f"{revision}:{path}"], binary=True)
        manifest.append({"path": path, "sha256": sha256_bytes(content)})
    return manifest


def protocol_manifest_from_worktree(
    root: Path, contract: Mapping[str, object]
) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    for path in protocol_files(contract):
        absolute = root / path
        if not absolute.is_file():
            raise ProtocolError(f"evaluation protocol file does not exist: {path}")
        manifest.append({"path": path, "sha256": sha256_bytes(absolute.read_bytes())})
    return manifest


def evaluation_protocol_hash(manifest: Sequence[Mapping[str, str]]) -> str:
    return canonical_hash(list(manifest))


def assert_protocol_matches_anchor(
    root: Path,
    anchor_revision: str,
    expected_sha256: str,
    expected_files: object,
    contract: Mapping[str, object],
) -> list[dict[str, str]]:
    anchor = resolve_commit(root, anchor_revision)
    anchor_manifest = protocol_manifest_from_revision(root, anchor, contract)
    worktree_manifest = protocol_manifest_from_worktree(root, contract)
    if worktree_manifest != anchor_manifest:
        changed = [
            current["path"]
            for current, frozen in zip(worktree_manifest, anchor_manifest, strict=True)
            if current != frozen
        ]
        raise ProtocolError(
            f"evaluation protocol differs from anchor {anchor}: {changed}"
        )
    actual_hash = evaluation_protocol_hash(anchor_manifest)
    if expected_sha256 != actual_hash:
        raise ProtocolError("evaluation_protocol.sha256 does not match anchor blobs")
    if expected_files != anchor_manifest:
        raise ProtocolError("evaluation_protocol.files does not match anchor blobs")
    return anchor_manifest


def _normalized_relative_path(root: Path, value: object, *, label: str) -> tuple[Path, str]:
    if not isinstance(value, str) or not value:
        raise ProtocolError(f"{label} must be a non-empty relative path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != value:
        raise ProtocolError(f"{label} must be a normalized relative POSIX path")
    resolved = (root / value).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ProtocolError(f"{label} escapes repository") from error
    return resolved, value


def _require_sha(value: object, *, label: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ProtocolError(f"{label} must be a lowercase sha256")
    return value


def _require_full_revision(value: object, *, label: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise ProtocolError(f"{label} must be a full Git revision")
    return value


def _read_campaign_payload(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ProtocolError(f"cannot read campaign: {error}") from error
    if not isinstance(payload, dict):
        raise ProtocolError("campaign must contain an object")
    return payload


def load_campaign(
    root: Path,
    campaign_path: Path,
    contract: Mapping[str, object] | None = None,
    *,
    require_committed: bool = True,
) -> Campaign:
    contract = dict(contract or load_contract(root))
    campaign_path = campaign_path.resolve()
    try:
        relative = campaign_path.relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ProtocolError("campaign must be inside the repository") from error
    payload = _read_campaign_payload(campaign_path)
    behavior = _behavior(contract)
    required = behavior.get("campaign_required_fields")
    if not isinstance(required, list) or set(payload) != set(required):
        raise ProtocolError(f"campaign fields must be {sorted(required or [])}")
    if payload.get("schema_version") != behavior.get("campaign_schema_version"):
        raise ProtocolError("campaign schema_version does not match contract")
    campaign_id = payload.get("campaign_id")
    try:
        if not isinstance(campaign_id, str):
            raise ValueError
        uuid.UUID(campaign_id)
    except ValueError as error:
        raise ProtocolError("campaign_id must be a UUID") from error
    artifact_root = payload.get("artifact_root")
    expected_artifact_root = f"eval-results/routing/campaigns/{campaign_id}"
    _normalized_relative_path(
        root, artifact_root, label="campaign artifact_root"
    )
    if artifact_root != expected_artifact_root:
        raise ProtocolError(
            f"campaign artifact_root must equal {expected_artifact_root!r}"
        )

    candidate = _require_full_revision(
        payload.get("candidate_skill_revision"), label="candidate_skill_revision"
    )
    anchor = _require_full_revision(
        payload.get("evaluation_anchor_revision"), label="evaluation_anchor_revision"
    )
    previous = _require_full_revision(
        payload.get("previous_skill_revision"), label="previous_skill_revision"
    )
    baseline = _require_full_revision(
        payload.get("baseline_skill_revision"), label="baseline_skill_revision"
    )
    if candidate != anchor or baseline != anchor:
        raise ProtocolError("candidate and baseline revisions must equal evaluation anchor")
    for revision in (anchor, previous):
        if resolve_commit(root, revision) != revision:
            raise ProtocolError("campaign revisions must be canonical full commits")
    if not revision_is_ancestor(root, previous, anchor, strict=True):
        raise ProtocolError("campaign previous revision must be a strict anchor ancestor")

    artifacts: dict[str, tuple[Path, str, str]] = {}
    for label in ("dataset", "provenance"):
        value = payload.get(label)
        if not isinstance(value, dict) or set(value) != {"path", "sha256", "git_revision"}:
            raise ProtocolError(f"campaign {label} fields must be path, sha256, git_revision")
        absolute, path_text = _normalized_relative_path(
            root, value.get("path"), label=f"campaign {label}.path"
        )
        expected_hash = _require_sha(
            value.get("sha256"), label=f"campaign {label}.sha256"
        )
        revision = _require_full_revision(
            value.get("git_revision"), label=f"campaign {label}.git_revision"
        )
        if not absolute.is_file() or sha256_bytes(absolute.read_bytes()) != expected_hash:
            raise ProtocolError(f"campaign {label} content hash mismatch")
        committed = _git(root, ["show", f"{revision}:{path_text}"], binary=True)
        if committed != absolute.read_bytes():
            raise ProtocolError(f"campaign {label} does not match its committed blob")
        if not revision_is_ancestor(root, anchor, revision, strict=True):
            raise ProtocolError(f"campaign {label} must be committed after the anchor")
        artifacts[label] = (absolute, path_text, revision)
    if artifacts["dataset"][2] != artifacts["provenance"][2]:
        raise ProtocolError(
            "campaign dataset and provenance must use the same Git revision"
        )

    condition = payload.get("condition")
    condition_fields = {
        "host_name",
        "model",
        "timeout_seconds",
        "concurrency",
        "prompt_template_version",
        "prompt_template_sha256",
        "adjudication",
        "host_config_sha256",
        "environment_policy_sha256",
        "retry_policy_sha256",
    }
    if not isinstance(condition, dict) or set(condition) != condition_fields:
        raise ProtocolError(f"campaign condition fields must be {sorted(condition_fields)}")
    host = condition.get("host_name")
    model = condition.get("model")
    if host not in {"codex", "claude"} or not isinstance(model, str) or not model:
        raise ProtocolError("campaign condition host/model is invalid")
    if model.casefold() in {"auto", "default", "latest", "opus", "sonnet", "haiku", "fable"} or not any(
        character.isdigit() for character in model
    ):
        raise ProtocolError("campaign model must be a versioned identifier")
    for key in ("timeout_seconds", "concurrency"):
        number = condition.get(key)
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            raise ProtocolError(f"campaign condition {key} must be a positive integer")
    prompt = canonical_prompt_template(contract)
    if condition.get("prompt_template_version") != behavior.get("prompt_template_version"):
        raise ProtocolError("campaign prompt_template_version is not canonical")
    if condition.get("prompt_template_sha256") != sha256_text(prompt):
        raise ProtocolError("campaign prompt_template_sha256 is not canonical")
    adjudication = canonical_adjudication(contract)
    if condition.get("adjudication") != adjudication:
        raise ProtocolError("campaign adjudication is not canonical")
    environment = canonical_environment_policy(str(host), contract)
    environment_hash = canonical_hash(environment)
    if condition.get("environment_policy_sha256") != environment_hash:
        raise ProtocolError("campaign environment policy is not canonical")
    retry_policy = canonical_transient_retry_policy(str(host), contract)
    retry_policy_hash = canonical_hash(retry_policy)
    if condition.get("retry_policy_sha256") != retry_policy_hash:
        raise ProtocolError("campaign transient retry policy is not canonical")
    host_policy = canonical_host_policy(str(host), str(model), contract)
    if condition.get("host_config_sha256") != canonical_hash(host_policy):
        raise ProtocolError("campaign host policy is not canonical")

    trials = payload.get("trials")
    minimum_trials = int(
        behavior["comparative"]["minimum_trials_per_variant"]
    )
    if not isinstance(trials, list) or len(trials) < minimum_trials:
        raise ProtocolError(f"campaign must declare at least {minimum_trials} trials")
    expected_trials = list(range(1, len(trials) + 1))
    observed_trials: list[int] = []
    group_ids: list[str] = []
    for item in trials:
        if not isinstance(item, dict) or set(item) != {"trial", "comparison_group_id"}:
            raise ProtocolError("campaign trial fields must be trial and comparison_group_id")
        trial = item.get("trial")
        group_id = item.get("comparison_group_id")
        if isinstance(trial, bool) or not isinstance(trial, int):
            raise ProtocolError("campaign trial must be an integer")
        try:
            if not isinstance(group_id, str):
                raise ValueError
            uuid.UUID(group_id)
        except ValueError as error:
            raise ProtocolError("campaign comparison_group_id must be a UUID") from error
        observed_trials.append(trial)
        group_ids.append(group_id)
    if observed_trials != expected_trials or len(group_ids) != len(set(group_ids)):
        raise ProtocolError("campaign trials must be ordered 1..N with unique group IDs")

    protocol = payload.get("evaluation_protocol")
    if not isinstance(protocol, dict) or set(protocol) != {"revision", "sha256", "files"}:
        raise ProtocolError("campaign evaluation_protocol fields are invalid")
    protocol_revision = _require_full_revision(
        protocol.get("revision"), label="evaluation_protocol.revision"
    )
    if protocol_revision != anchor:
        raise ProtocolError("evaluation protocol revision must equal anchor")
    protocol_hash = _require_sha(
        protocol.get("sha256"), label="evaluation_protocol.sha256"
    )
    assert_protocol_matches_anchor(
        root, anchor, protocol_hash, protocol.get("files"), contract
    )

    campaign_commit = ""
    if require_committed:
        campaign_commit = str(
            _git(root, ["log", "-1", "--format=%H", "--", relative])
        ).strip()
        if re.fullmatch(r"[0-9a-f]{40}", campaign_commit) is None:
            raise ProtocolError("campaign must be committed")
        committed = _git(root, ["show", f"{campaign_commit}:{relative}"], binary=True)
        if committed != campaign_path.read_bytes():
            raise ProtocolError("campaign must exactly match its committed blob")
        if not revision_is_ancestor(root, anchor, campaign_commit, strict=True):
            raise ProtocolError("campaign must be committed after the evaluation anchor")
        for label, (_, _, revision) in artifacts.items():
            if not revision_is_ancestor(root, revision, campaign_commit, strict=False):
                raise ProtocolError(f"campaign {label} revision must precede the campaign")

    return Campaign(
        payload=payload,
        path=campaign_path,
        relative_path=relative,
        sha256=sha256_bytes(campaign_path.read_bytes()),
        commit=campaign_commit,
    )


def expected_revision_for_variant(campaign: Campaign, variant: str) -> str:
    if variant in {"candidate", "baseline"}:
        return campaign.anchor_revision
    if variant == "previous":
        return campaign.previous_revision
    raise ProtocolError(f"unsupported campaign variant {variant!r}")
