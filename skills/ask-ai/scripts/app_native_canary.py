#!/usr/bin/env python3
"""Classify a sanitized Codex App-native ChatGPT capability snapshot.

This canary is deliberately read-only. The caller captures the exposed tool schema,
`list_projects`, and `list_threads` results, removes private labels/paths/content, and
passes the resulting JSON file here before any `create_thread` call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "ask-ai-app-native-canary/v1"
REQUIRED_OPERATIONS = {
    "list_projects",
    "list_threads",
    "create_thread",
    "read_thread",
    "send_message_to_thread",
}
CHATGPT_TARGET = "chatgptWorkCloud"
EXIT_CODES = {
    "ready": 0,
    "activation-required": 10,
    "browser-fallback-required": 20,
    "blocked": 30,
}


class SnapshotError(ValueError):
    """The canary snapshot is malformed or internally inconsistent."""


def canonical_prompt_bytes(prompt: str) -> bytes:
    """Return prompt-text/v1 bytes: exact Unicode text with LF line endings."""
    if not isinstance(prompt, str):
        raise SnapshotError("prompt must be a string")
    return prompt.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def prompt_fingerprint(prompt: str) -> dict[str, Any]:
    content = canonical_prompt_bytes(prompt)
    canonical_text = content.decode("utf-8")
    return {
        "hash_scheme": "prompt-text/v1",
        "sha256": hashlib.sha256(content).hexdigest(),
        "utf8_bytes": len(content),
        "characters": len(canonical_text),
    }


def classify_create_result(result: Any) -> dict[str, Any]:
    """Classify one atomic create call into its two correlated logical writes."""
    def states(state: str) -> dict[str, str]:
        return {
            "create-conversation": state,
            "submit-initial": state,
        }

    if isinstance(result, dict):
        thread_id = result.get("threadId")
        client_thread_id = result.get("clientThreadId")
        if isinstance(thread_id, str) and thread_id:
            return {
                "logical_write_states": states("submitted"),
                "identity_state": "resolved",
                "thread_id": thread_id,
                "state_change_allowed": False,
            }
        if isinstance(client_thread_id, str) and client_thread_id:
            return {
                "logical_write_states": states("submitted"),
                "identity_state": "client-pending",
                "client_thread_id": client_thread_id,
                "state_change_allowed": False,
            }
    return {
        "logical_write_states": states("submission-uncertain"),
        "identity_state": "identity-not-verified",
        "state_change_allowed": False,
    }


def recovery_directive(ledger: dict[str, Any]) -> dict[str, Any]:
    """Keep v1/v2 uncertain ledgers on the original read-only recovery path."""
    schema_version = ledger.get("schema_version")
    if schema_version not in {
        "app-native-thread-operation/v1",
        "app-native-thread-operation/v2",
    }:
        raise SnapshotError("unsupported app-native ledger schema")
    state = ledger.get("state")
    call = _mapping(ledger.get("call"), "ledger.call")
    if state not in {"invoking", "submission-uncertain"} or call.get("count") != 1:
        raise SnapshotError("ledger is not an uncertain possibly-submitted operation")
    operation_id = ledger.get("operation_id")
    if not isinstance(operation_id, str) or not operation_id:
        raise SnapshotError("ledger.operation_id is required")
    return {
        "mode": "read-only-reconciliation",
        "operation_id": operation_id,
        "preserve_schema_version": schema_version,
        "state_change_allowed": False,
        "replacement_operation_allowed": False,
    }


def _parse_timestamp(value: Any, name: str) -> datetime:
    if not isinstance(value, str):
        raise SnapshotError(f"{name} must be an ISO-8601 string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise SnapshotError(f"{name} must be an ISO-8601 string") from error


def reconcile_create_candidates(
    expected: dict[str, Any], candidates: list[dict[str, Any]]
) -> dict[str, Any]:
    """Reconcile only complete, bounded, content-attributed ChatGPT candidates."""
    prompt = _mapping(expected.get("prompt"), "expected.prompt")
    if prompt.get("hash_scheme") != "prompt-text/v1":
        raise SnapshotError("expected.prompt.hash_scheme must be prompt-text/v1")
    expected_hash = prompt.get("sha256")
    expected_bytes = prompt.get("utf8_bytes")
    expected_characters = prompt.get("characters")
    if (
        not isinstance(expected_hash, str)
        or not isinstance(expected_bytes, int)
        or not isinstance(expected_characters, int)
    ):
        raise SnapshotError("expected prompt fingerprint is incomplete")
    started_at = _parse_timestamp(expected.get("started_at"), "expected.started_at")
    ended_at = _parse_timestamp(expected.get("ended_at"), "expected.ended_at")
    if ended_at < started_at:
        raise SnapshotError("expected call window is reversed")
    requested_surface = expected.get("requested_surface")
    if requested_surface not in {"project", "quick-chat"}:
        raise SnapshotError("expected.requested_surface must be project or quick-chat")
    project_id = expected.get("project_id")
    if requested_surface == "project" and (
        not isinstance(project_id, str) or not project_id
    ):
        raise SnapshotError("project reconciliation requires a project_id")
    if requested_surface == "quick-chat" and project_id is not None:
        raise SnapshotError("quick-chat reconciliation requires project_id=null")
    list_page_bound = expected.get("list_page_bound")
    candidate_bound = expected.get("candidate_bound")
    candidate_read_bound = expected.get("candidate_read_bound")
    list_bound_exhausted = expected.get("list_bound_exhausted")
    for name, value in {
        "list_page_bound": list_page_bound,
        "candidate_bound": candidate_bound,
        "candidate_read_bound": candidate_read_bound,
    }.items():
        if not isinstance(value, int) or value < 1:
            raise SnapshotError(f"expected.{name} must be a positive integer")
    if not isinstance(list_bound_exhausted, bool):
        raise SnapshotError("expected.list_bound_exhausted must be boolean")

    matches: list[str] = []
    truncation_seen = False
    completeness_unknown = False
    considered = 0
    read_limit = min(candidate_bound, candidate_read_bound)
    for candidate in candidates[:read_limit]:
        considered += 1
        if candidate.get("kind") != "chatgpt":
            continue
        candidate_project_id = candidate.get("projectId")
        if requested_surface == "project" and candidate_project_id != project_id:
            continue
        if requested_surface == "quick-chat" and candidate_project_id is not None:
            continue
        created_at = _parse_timestamp(
            candidate.get("initial_user_message_at"),
            "candidate.initial_user_message_at",
        )
        if not started_at <= created_at <= ended_at:
            continue
        truncated = candidate.get("truncated")
        if truncated is True:
            truncation_seen = True
            continue
        if truncated is not False:
            completeness_unknown = True
            continue
        user_prompt = candidate.get("initial_user_prompt")
        if not isinstance(user_prompt, str):
            continue
        fingerprint = prompt_fingerprint(user_prompt)
        if (
            fingerprint["sha256"] == expected_hash
            and fingerprint["utf8_bytes"] == expected_bytes
            and fingerprint["characters"] == expected_characters
        ):
            thread_id = candidate.get("thread_id")
            if isinstance(thread_id, str) and thread_id:
                matches.append(thread_id)

    candidate_bound_exhausted = len(candidates) > read_limit
    if (
        list_bound_exhausted
        or candidate_bound_exhausted
        or truncation_seen
        or completeness_unknown
    ):
        status = "Not verified"
    else:
        status = (
            "unique-match"
            if len(matches) == 1
            else "multiple-matches"
            if len(matches) > 1
            else "no-match"
        )
    return {
        "status": status,
        "thread_id": matches[0] if status == "unique-match" else None,
        "list_page_bound": list_page_bound,
        "candidates_considered": considered,
        "candidate_bound": candidate_bound,
        "candidate_read_bound": candidate_read_bound,
        "list_bound_exhausted": list_bound_exhausted,
        "candidate_bound_exhausted": candidate_bound_exhausted,
        "truncation_seen": truncation_seen,
        "completeness_unknown": completeness_unknown,
        "state_change_allowed": False,
    }


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SnapshotError(f"{name} must be an object")
    return value


def _string_set(value: Any, name: str) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SnapshotError(f"{name} must be an array of strings")
    return set(value)


def classify(snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        raise SnapshotError(f"schema_version must be {SCHEMA_VERSION}")

    requested_surface = snapshot.get("requested_surface")
    if requested_surface not in {"project", "quick-chat", "standard-chat"}:
        raise SnapshotError(
            "requested_surface must be project, quick-chat, or standard-chat"
        )

    if requested_surface == "standard-chat":
        return {
            "status": "browser-fallback-required",
            "reason": "no-distinct-native-standard-chat-target",
            "native_target": None,
            "state_change_allowed": False,
        }

    tool_schema = _mapping(snapshot.get("tool_schema"), "tool_schema")
    operations = _string_set(tool_schema.get("operations"), "tool_schema.operations")
    targets = _string_set(
        tool_schema.get("create_thread_targets"),
        "tool_schema.create_thread_targets",
    )
    missing_operations = sorted(REQUIRED_OPERATIONS - operations)
    if missing_operations:
        return {
            "status": "blocked",
            "reason": "required-host-operations-missing",
            "missing_operations": missing_operations,
            "native_target": None,
            "state_change_allowed": False,
        }

    projects_result = _mapping(snapshot.get("list_projects"), "list_projects")
    threads_result = _mapping(snapshot.get("list_threads"), "list_threads")
    projects = projects_result.get("projects")
    threads = threads_result.get("threads")
    if "unavailableSources" not in threads_result:
        return {
            "status": "blocked",
            "reason": "chatgpt-source-status-not-exposed",
            "native_target": None,
            "state_change_allowed": False,
        }
    unavailable_sources = threads_result["unavailableSources"]
    if not isinstance(projects, list) or not all(isinstance(item, dict) for item in projects):
        raise SnapshotError("list_projects.projects must be an array of objects")
    if not isinstance(threads, list) or not all(isinstance(item, dict) for item in threads):
        raise SnapshotError("list_threads.threads must be an array of objects")
    unavailable = _string_set(unavailable_sources, "list_threads.unavailableSources")

    chatgpt_projects = [
        item for item in projects if item.get("projectKind") == "chatgpt"
    ]
    chatgpt_threads = [item for item in threads if item.get("kind") == "chatgpt"]
    source_evidence = bool(chatgpt_projects or chatgpt_threads)

    if "chatgpt" in unavailable and source_evidence:
        return {
            "status": "blocked",
            "reason": "inconsistent-chatgpt-source-evidence",
            "native_target": None,
            "state_change_allowed": False,
        }
    if "chatgpt" in unavailable:
        return {
            "status": "activation-required",
            "reason": "chatgpt-source-unavailable",
            "required_user_action": (
                "Open or switch to ChatGPT/Quick Chat once in the Codex App, then "
                "capture fresh list_projects and list_threads results."
            ),
            "native_target": None,
            "state_change_allowed": False,
        }

    if CHATGPT_TARGET not in targets:
        return {
            "status": "blocked",
            "reason": "chatgpt-work-cloud-target-not-exposed",
            "native_target": None,
            "state_change_allowed": False,
        }

    if requested_surface == "quick-chat":
        if snapshot.get("explicit_quick_chat") is not True:
            return {
                "status": "blocked",
                "reason": "quick-chat-not-explicitly-requested",
                "native_target": None,
                "state_change_allowed": False,
            }
        return {
            "status": "ready",
            "reason": "verified-projectless-chatgpt-work-cloud",
            "native_target": {"type": CHATGPT_TARGET},
            "state_change_allowed": True,
        }

    project_id = snapshot.get("project_id")
    if not isinstance(project_id, str) or not project_id:
        raise SnapshotError("project_id is required for requested_surface=project")
    matches = [item for item in chatgpt_projects if item.get("projectId") == project_id]
    if len(matches) != 1:
        return {
            "status": "blocked",
            "reason": "chatgpt-project-id-not-uniquely-verified",
            "native_target": None,
            "state_change_allowed": False,
        }
    return {
        "status": "ready",
        "reason": "verified-chatgpt-project",
        "native_target": {"type": CHATGPT_TARGET, "projectId": project_id},
        "state_change_allowed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "snapshot",
        help="Sanitized JSON snapshot path, or - to read JSON from stdin.",
    )
    args = parser.parse_args()
    try:
        if args.snapshot == "-":
            payload = json.load(sys.stdin)
        else:
            payload = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
        result = classify(_mapping(payload, "snapshot"))
    except (OSError, json.JSONDecodeError, SnapshotError) as error:
        result = {
            "status": "blocked",
            "reason": "invalid-canary-snapshot",
            "detail": str(error),
            "native_target": None,
            "state_change_allowed": False,
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return EXIT_CODES[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
