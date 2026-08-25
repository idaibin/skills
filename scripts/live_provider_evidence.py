#!/usr/bin/env python3
"""Fail-closed verification for provider-owned live-evaluation events.

Shared by the runner and standalone result validator.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


PROVIDER_REQUESTED_ALIAS = "Flash"
PROVIDER_MODEL = "gemini-3.7-flash-high"
PROVIDER_IDENTITY = "google-antigravity"
INTERMEDIATE_EVENTS = frozenset({"assistant", "message", "progress", "tool_call", "tool_result"})
FAILED_TERMINAL_EVENTS = frozenset({"error", "cancelled", "failed"})


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _absolute_realpath(value: object) -> str | None:
    return os.path.realpath(value) if isinstance(value, str) and os.path.isabs(value) else None


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _provider_events(path: Path) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Read a fail-closed AGY stream: known intermediates, then one successful result."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    init = result = None
    terminal_seen = False
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return None
        if not isinstance(event, dict) or not isinstance(event.get("event"), str):
            return None
        event_name = event["event"]
        if event_name == "init":
            if init is not None or terminal_seen or not isinstance(event.get("init"), dict):
                return None
            init = event
        elif event_name == "result":
            if init is None or terminal_seen or not isinstance(event.get("result"), dict):
                return None
            result = event
            terminal_seen = True
        elif event_name in FAILED_TERMINAL_EVENTS:
            # A trailing provider failure must not be hidden by an earlier success.
            return None
        elif event_name not in INTERMEDIATE_EVENTS or init is None or terminal_seen:
            return None
    return (init, result) if init is not None and result is not None and terminal_seen else None


def verify_provider_evidence(
    evidence: dict[str, Any] | None,
    *,
    case_id: str,
    source_diff_sha256: str,
    selected_repository_root: str,
) -> tuple[dict[str, str] | None, str]:
    """Cross-check a host receipt against independently parsed provider JSONL events."""
    if not isinstance(evidence, dict) or evidence.get("channel") != "AGY":
        return None, "missing provider evidence"
    paths = {
        key: Path(evidence[key])
        for key in ("artifact_path", "events_path", "execution_receipt_path")
        if isinstance(evidence.get(key), str)
    }
    if len(paths) != 3 or not all(path.is_file() for path in paths.values()):
        return None, "missing provider artifact, events, or receipt"
    receipt = _load_json(paths["execution_receipt_path"])
    event_pair = _provider_events(paths["events_path"])
    if receipt is None or event_pair is None:
        return None, "provider events must be complete JSONL init/result records"
    init_event, result_event = event_pair
    init = init_event["init"]
    result = result_event["result"]
    event_conversation = init_event.get("conversation_id")
    result_event_conversation = result_event.get("conversation_id")
    nested_result_conversation = result.get("conversation_id")
    result_conversation = result_event_conversation if _string(result_event_conversation) else nested_result_conversation
    event_model = init.get("model")
    terminal = result.get("terminal", result.get("status"))
    event_basis = result.get("basis")
    final_artifact = result.get("final_artifact")
    expected_basis = {"case_id": case_id, "source_diff_sha256": source_diff_sha256}
    artifact_sha256 = sha256_file(paths["artifact_path"])
    artifact_bytes = paths["artifact_path"].stat().st_size
    if not (
        init_event.get("provider_identity") == PROVIDER_IDENTITY
        and result_event.get("provider_identity") == PROVIDER_IDENTITY
        and _string(event_conversation)
        and event_conversation == result_conversation
        and (not _string(result_event_conversation) or not _string(nested_result_conversation) or nested_result_conversation == result_event_conversation)
        and event_model == PROVIDER_MODEL
        and terminal in {"SUCCESS", "completed", "succeeded"}
        and _string(init.get("cwd"))
        and isinstance(init.get("tools"), list)
        and _string(result.get("operation_id"))
        and _string(result.get("prompt_or_basis_digest"))
        and isinstance(event_basis, dict) and event_basis == expected_basis
        and isinstance(final_artifact, dict)
        and artifact_bytes > 0
        and final_artifact.get("sha256") == artifact_sha256
        and final_artifact.get("bytes") == artifact_bytes
    ):
        return None, "provider event fields are incomplete or do not match the requested case"
    events_hash = sha256_file(paths["events_path"])
    receipt_provider = receipt.get("provider")
    receipt_invocation = receipt.get("invocation")
    receipt_basis = receipt.get("basis")
    receipt_artifacts = receipt.get("artifacts")
    runtime = {
        "executable_fingerprint": receipt_provider.get("executable_fingerprint") if isinstance(receipt_provider, dict) else None,
        "executable_version": receipt_provider.get("executable_version") if isinstance(receipt_provider, dict) else None,
        "profile": receipt_provider.get("profile") if isinstance(receipt_provider, dict) else None,
        "native_mode": receipt_provider.get("native_mode") if isinstance(receipt_provider, dict) else None,
        "model_evidence_locator": receipt_provider.get("model_evidence_locator") if isinstance(receipt_provider, dict) else None,
    }
    receipt_claims = {
        "requested_alias": receipt.get("requested_alias"),
        "process_exit_code": receipt.get("process_exit_code"),
        "terminal": receipt_provider.get("terminal") if isinstance(receipt_provider, dict) else None,
        "init_model": receipt_provider.get("init_model") if isinstance(receipt_provider, dict) else None,
        "effective_model": receipt_provider.get("effective_model") if isinstance(receipt_provider, dict) else None,
        "conversation_id": receipt_provider.get("conversation_id") if isinstance(receipt_provider, dict) else None,
        "cwd": receipt_provider.get("cwd") if isinstance(receipt_provider, dict) else None,
        "identity": receipt_provider.get("identity") if isinstance(receipt_provider, dict) else None,
    }
    selected_root = _absolute_realpath(selected_repository_root)
    invocation_argv = receipt_invocation.get("argv") if isinstance(receipt_invocation, dict) else None
    process_cwd = receipt_invocation.get("process_cwd") if isinstance(receipt_invocation, dict) else None
    add_dir_values: list[str] = []
    if isinstance(invocation_argv, list) and all(isinstance(item, str) for item in invocation_argv):
        for index, item in enumerate(invocation_argv):
            if item == "--add-dir" and index + 1 < len(invocation_argv):
                value = _absolute_realpath(invocation_argv[index + 1])
                add_dir_values.append(value if value is not None else "")
    invocation_matches = bool(
        selected_root is not None
        and isinstance(invocation_argv, list)
        and all(isinstance(item, str) for item in invocation_argv)
        and _absolute_realpath(process_cwd) == selected_root
    )
    invocation_matches = bool(
        invocation_matches
        and add_dir_values == [selected_root]
        and "--dangerously-skip-permissions" in invocation_argv
        and _absolute_realpath(init.get("cwd")) == selected_root
        and _absolute_realpath(receipt_claims["cwd"]) == selected_root
    )
    if not (
        evidence.get("execution_receipt_sha256") == sha256_file(paths["execution_receipt_path"])
        and receipt_claims == {
            "requested_alias": PROVIDER_REQUESTED_ALIAS,
            "process_exit_code": 0,
            "terminal": terminal,
            "init_model": event_model,
            "effective_model": event_model,
            "conversation_id": event_conversation,
            "cwd": init["cwd"],
            "identity": PROVIDER_IDENTITY,
        }
        and all(_string(value) for value in runtime.values())
        and runtime["executable_fingerprint"].startswith("sha256:")
        and runtime["model_evidence_locator"] == "init.model"
        and receipt.get("operation_id") == result.get("operation_id")
        and receipt.get("prompt_or_basis_digest") == result.get("prompt_or_basis_digest")
        and isinstance(receipt_basis, dict) and receipt_basis == event_basis
        and isinstance(receipt_artifacts, dict)
        and receipt_basis.get("case_id") == case_id
        and receipt_basis.get("source_diff_sha256") == source_diff_sha256
        and receipt_artifacts.get("artifact_sha256") == artifact_sha256
        and receipt_artifacts.get("artifact_bytes") == artifact_bytes
        and receipt_artifacts.get("events_sha256") == events_hash
        and invocation_matches
    ):
        return None, "execution receipt does not match provider-owned events"
    return {
        "requested_alias": PROVIDER_REQUESTED_ALIAS,
        "init_model": event_model,
        "effective_model": event_model,
        "conversation_id": event_conversation,
        **runtime,
    }, "verified"
