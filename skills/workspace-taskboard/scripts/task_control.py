#!/usr/bin/env python3
"""Deterministic project-root routing and projection for workspace-taskboard."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = PACKAGE / "assets" / "control-manifest.v1.schema.json"
TERMINATED = {"delivered", "archived", "deleted", "unavailable"}
RESUMABLE = {"active", "idle", "notLoaded", "queued", "blocked", "waiting", "completed"}
DISCUSSION_INTENTS = {"discussion", "planning", "architecture", "scope", "prioritization", "decision", "question"}
EXECUTION_INTENTS = {"implementation", "testing", "investigation", "review", "monitoring", "external-ai", "git-delivery"}
WAITING_STATES = {"waiting-dependency", "awaiting-human-approval", "decision-needed", "blocked"}
FINISHED_STATES = {"finished", "ready-for-delivery", "delivered"}
SECRET_PATTERNS = (
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{8,}|sk-[A-Za-z0-9_-]{8,})\b", re.IGNORECASE),
    re.compile(r"\b(?:password|passwd|token|secret|api[_-]?key)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)"),
)


def canonical_path(value: object) -> str | None:
    """Resolve an existing directory and normalize it for the host platform."""
    if not isinstance(value, str) or not value.strip() or "\0" in value:
        return None
    try:
        resolved = os.path.realpath(os.path.abspath(value))
        if not os.path.isdir(resolved):
            return None
        return os.path.normcase(os.path.normpath(resolved))
    except (OSError, ValueError):
        return None


canonical_cwd = canonical_path


def stored_canonical_path(value: object) -> str | None:
    """Validate an already-resolved absolute path without requiring it to still exist."""
    if not isinstance(value, str) or not value or "\0" in value or not os.path.isabs(value):
        return None
    normalized = os.path.normcase(os.path.normpath(value))
    return normalized if normalized == value else None


def path_within(path: str | None, root: str | None) -> bool:
    """Return true only for equality or component-aware descendant containment."""
    if not path or not root:
        return False
    try:
        return os.path.commonpath((path, root)) == root
    except ValueError:
        return False


def digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _safe_display(value: object, limit: int = 180) -> str:
    if not isinstance(value, str) or not value.strip():
        return "Not verified"
    text = " ".join(re.sub(r"[\x00-\x1f\x7f-\x9f]", "", value).split())
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    text = text.translate(str.maketrans({"`": "ˋ", "<": "‹", ">": "›", "[": "［", "]": "］"}))
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _is_archived(task: dict[str, Any]) -> bool:
    return task.get("status") == "archived" or task.get("archived") is True


def _is_terminated(task: dict[str, Any]) -> bool:
    return _is_archived(task) or task.get("status") in TERMINATED


def _schema_validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected = schema.get("type")
    allowed = expected if isinstance(expected, list) else [expected] if expected else []
    type_ok = not allowed or any(
        (kind == "object" and isinstance(instance, dict))
        or (kind == "array" and isinstance(instance, list))
        or (kind == "string" and isinstance(instance, str))
        or (kind == "integer" and isinstance(instance, int) and not isinstance(instance, bool))
        or (kind == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool))
        or (kind == "boolean" and isinstance(instance, bool))
        or (kind == "null" and instance is None)
        for kind in allowed
    )
    if not type_ok:
        return [f"{path}: expected {allowed}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value is not allowed")
    if isinstance(instance, str) and len(instance) < schema.get("minLength", 0):
        errors.append(f"{path}: string is too short")
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in instance:
                errors.append(f"{path}: missing {name}")
        if schema.get("additionalProperties") is False:
            for name in instance.keys() - properties.keys():
                errors.append(f"{path}: unexpected {name}")
        for name, value in instance.items():
            if name in properties:
                errors.extend(_schema_validate(value, properties[name], f"{path}.{name}"))
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems"):
            seen: set[str] = set()
            for item in instance:
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker in seen:
                    errors.append(f"{path}: duplicate item")
                seen.add(marker)
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(instance):
                errors.extend(_schema_validate(item, schema["items"], f"{path}[{index}]"))
    return errors


def _canonical_roots(manifest: dict[str, Any]) -> tuple[str | None, list[str], list[str]]:
    errors: list[str] = []
    project_root = stored_canonical_path(manifest.get("canonical_project_root"))
    if project_root != manifest.get("canonical_project_root"):
        errors.append("$.canonical_project_root: must already be canonical")
    roots: list[str] = []
    for index, item in enumerate(manifest.get("allowed_roots", [])):
        resolved = stored_canonical_path(item)
        if resolved != item:
            errors.append(f"$.allowed_roots[{index}]: must already be canonical")
        elif resolved not in roots:
            roots.append(resolved)
    if project_root and project_root not in roots:
        errors.append("$.allowed_roots: must include canonical_project_root")
    return project_root, roots, errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    schema = json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))
    errors = _schema_validate(manifest, schema)
    if errors or not isinstance(manifest, dict):
        return errors or ["$: expected object"]
    project_root, roots, path_errors = _canonical_roots(manifest)
    errors.extend(path_errors)
    mappings = manifest.get("worker_mappings", [])
    edges = manifest.get("dependency_edges", [])
    if not isinstance(mappings, list) or not all(isinstance(item, dict) for item in mappings):
        return errors + ["$.worker_mappings: expected object items"]
    if not isinstance(edges, list) or not all(isinstance(item, dict) for item in edges):
        return errors + ["$.dependency_edges: expected object items"]
    reuse_keys = [item.get("reuse_key") for item in mappings]
    thread_ids = [item.get("thread_id") for item in mappings]
    if len(reuse_keys) != len(set(reuse_keys)):
        errors.append("$.worker_mappings: reuse_key must be unique")
    if len(thread_ids) != len(set(thread_ids)):
        errors.append("$.worker_mappings: thread_id must be unique")
    for index, mapping in enumerate(mappings):
        worker_cwd = stored_canonical_path(mapping.get("canonical_cwd"))
        if worker_cwd != mapping.get("canonical_cwd") or not any(path_within(worker_cwd, root) for root in roots):
            errors.append(f"$.worker_mappings[{index}]: canonical_cwd must be inside a verified allowed root")
        expected = f"{mapping.get('project_identity')}:{worker_cwd}:{mapping.get('responsibility')}"
        if mapping.get("reuse_key") != expected:
            errors.append(f"$.worker_mappings[{index}]: reuse_key must derive from project, worker cwd, and responsibility")
    known = set(reuse_keys)
    for index, edge in enumerate(edges):
        if edge.get("producer_reuse_key") not in known or edge.get("consumer_reuse_key") not in known:
            errors.append(f"$.dependency_edges[{index}]: endpoints must reference worker mappings")
    return errors


def _registry_snapshot_stop(payload: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any] | None:
    computed = digest(manifest)
    if payload.get("manifest_digest") != computed or payload.get("current_registry_digest") != computed:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    return None


def _verified_scope(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str], dict[str, Any] | None]:
    project = payload.get("project_readback")
    if not isinstance(project, dict):
        return None, [], {"action": "blocked", "stop_state": "project-unverified", "failure_code": "PLACEMENT_UNVERIFIED"}
    root = canonical_path(payload.get("controller_project_root"))
    controller_cwd = canonical_path(payload.get("controller_cwd"))
    readback_root = canonical_path(project.get("canonical_project_root") or project.get("path"))
    roots = [stored_canonical_path(item) for item in project.get("allowed_roots", [])]
    roots = [item for item in roots if item]
    evidence = project.get("allowed_root_membership")
    proven_roots = {
        stored_canonical_path(item.get("canonical_root"))
        for item in evidence
        if isinstance(item, dict)
        and item.get("source") == "host-project-readback"
        and item.get("version") == project.get("allowed_roots_version")
    } if isinstance(evidence, list) else set()
    if (
        not root
        or not controller_cwd
        or root != readback_root
        or root not in roots
        or not any(path_within(controller_cwd, allowed) for allowed in roots)
        or project.get("project_kind", "local") != "local"
        or not project.get("project_id")
        or not project.get("membership_verified")
        or not project.get("allowed_roots_version")
        or set(roots) != proven_roots
    ):
        return None, [], {"action": "blocked", "stop_state": "project-unverified", "failure_code": "PLACEMENT_UNVERIFIED"}
    return project, roots, None


def _is_local_codex_task(candidate: dict[str, Any], project_id: str) -> bool:
    return (
        candidate.get("kind") == "codex"
        and candidate.get("project_id") == project_id
        and candidate.get("project_kind", "local") == "local"
        and not candidate.get("projectless", False)
        and not candidate.get("remote", False)
    )


def _candidate_cwd(candidate: dict[str, Any]) -> str | None:
    return canonical_path(candidate.get("cwd"))


def _in_scope(candidate: dict[str, Any], project_id: str, roots: list[str]) -> bool:
    cwd = _candidate_cwd(candidate)
    return _is_local_codex_task(candidate, project_id) and any(path_within(cwd, root) for root in roots)


def _reuse_key(project_identity: str, cwd: str, responsibility: str) -> str:
    return f"{project_identity}:{cwd}:{responsibility}"


def _create_placement_proven(project: dict[str, Any], target_cwd: str, environment: str) -> bool:
    """Require exact pre-create placement evidence; post-create discovery is too late."""
    project_root = canonical_path(project.get("canonical_project_root") or project.get("path"))
    if environment == "local" and target_cwd == project_root:
        return True
    receipts = project.get("create_placement_receipts")
    if not isinstance(receipts, list):
        return False
    return any(
        isinstance(item, dict)
        and canonical_path(item.get("canonical_cwd")) == target_cwd
        and item.get("source") == "host-create-adapter"
        and item.get("version") == project.get("allowed_roots_version")
        for item in receipts
    )


def _view(candidate: dict[str, Any], sequence: int) -> dict[str, Any]:
    return {
        "sequence": sequence,
        "title": _safe_display(candidate.get("title")),
        "thread_id": candidate.get("thread_id"),
        "canonical_cwd": _candidate_cwd(candidate) or "Not verified",
        "responsibility": candidate.get("responsibility", "Not verified"),
        "status": candidate.get("status", "unknown"),
        "recent_goal": _safe_display(candidate.get("recent_goal")),
    }


def _blocked_workspace(**extra: Any) -> dict[str, Any]:
    return {"action": "blocked", "stop_state": "out-of-scope-workspace", "failure_code": "OUT_OF_SCOPE_WORKSPACE", **extra}


def route(payload: dict[str, Any]) -> dict[str, Any]:
    request = payload.get("request", {})
    capabilities = payload.get("host_capabilities", {})
    missing = [name for name in ("list_projects", "list_threads", "read_thread") if not capabilities.get(name)]
    if missing:
        return {"action": "blocked", "stop_state": "capability-unavailable", "failure_code": "CAPABILITY_MISSING", "missing": missing}
    project, roots, stop = _verified_scope(payload)
    if stop:
        return stop
    assert project is not None
    project_id = project["project_id"]
    project_identity = project.get("project_identity") or project_id
    intent = request.get("intent")
    if intent in DISCUSSION_INTENTS and not request.get("explicit_thread_id"):
        return {"action": "handle-in-controller", "reason": "discussion-only", "create": False, "dispatch": False}
    if intent not in EXECUTION_INTENTS and intent not in DISCUSSION_INTENTS:
        return {"action": "decision-needed", "stop_state": "intent-uncertain", "create": False, "dispatch": False}
    if not capabilities.get("send_message_to_thread"):
        return {"action": "blocked", "stop_state": "capability-unavailable", "failure_code": "CAPABILITY_MISSING", "missing": ["send_message_to_thread"]}

    all_candidates = [item for item in payload.get("candidates", []) if isinstance(item, dict)]
    in_scope = [item for item in all_candidates if _in_scope(item, project_id, roots)]
    mappings_by_thread = {item.get("thread_id"): item for item in payload.get("worker_mappings", []) if isinstance(item, dict)}
    explicit_id = request.get("explicit_thread_id")
    if explicit_id:
        target = next((item for item in all_candidates if item.get("thread_id") == explicit_id), None)
        if target is None or _candidate_cwd(target) is None:
            return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED", "thread_id": explicit_id}
        if not _in_scope(target, project_id, roots):
            return _blocked_workspace(thread_id=explicit_id)
        if mappings_by_thread.get(explicit_id, {}).get("closed"):
            return {"action": "blocked", "stop_state": "closed-candidate", "failure_code": "CLOSED_TASK", "thread_id": explicit_id}
        if _is_terminated(target):
            return {"action": "decision-needed", "stop_state": "archived-candidate", "thread_id": explicit_id, "options": ["restore", "new-task"]}
        return {"action": "queue-existing", "thread_id": explicit_id, "canonical_cwd": _candidate_cwd(target), "create": False, "execute_locally": False}

    responsibility = request.get("responsibility")
    target_cwd = canonical_path(request.get("worker_cwd"))
    if not responsibility or not target_cwd or not any(path_within(target_cwd, root) for root in roots):
        choices = [_view(item, index + 1) for index, item in enumerate(in_scope)]
        choices.append({"sequence": len(choices) + 1, "choice": "new-task"})
        return {"action": "decision-needed", "stop_state": "identity-incomplete", "choices": choices, "create": False}
    reuse_key = _reuse_key(project_identity, target_cwd, responsibility)
    mappings = {item.get("reuse_key"): item for item in payload.get("worker_mappings", []) if isinstance(item, dict)}
    closed_thread_ids = {item.get("thread_id") for item in mappings.values() if item.get("closed")}
    mapped = mappings.get(reuse_key)
    if mapped and mapped.get("closed"):
        mapped = None
    elif mapped:
        match = next((item for item in in_scope if item.get("thread_id") == mapped.get("thread_id")), None)
        if match is None or _candidate_cwd(match) != target_cwd or match.get("responsibility") != responsibility:
            return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT", "reuse_key": reuse_key}
        if _is_terminated(match) or match.get("status") not in RESUMABLE or match.get("goal_compatibility") != "compatible":
            mapped = None

    same_identity = [
        item for item in in_scope
        if _candidate_cwd(item) == target_cwd and item.get("responsibility") == responsibility
        and not _is_terminated(item)
        and not item.get("closed", False)
        and item.get("thread_id") not in closed_thread_ids
    ]
    live = [item for item in same_identity if item.get("goal_compatibility") == "compatible"]
    uncertain = [item for item in same_identity if item.get("goal_compatibility") != "compatible"]
    if uncertain or len(live) > 1:
        choices = [_view(item, index + 1) for index, item in enumerate([*live, *uncertain])]
        choices.append({"sequence": len(choices) + 1, "choice": "new-task"})
        return {"action": "decision-needed", "stop_state": "candidate-ambiguous", "reuse_key": reuse_key, "choices": choices, "create": False}
    if mapped and len(live) == 1 and live[0].get("thread_id") == mapped.get("thread_id"):
        return {"action": "reuse-existing", "reuse_key": reuse_key, "thread_id": live[0]["thread_id"], "reason": "verified-mapping", "execute_locally": False}
    if len(live) == 1:
        return {"action": "reuse-existing", "reuse_key": reuse_key, "thread_id": live[0]["thread_id"], "reason": "unique-compatible-candidate", "execute_locally": False}

    if not capabilities.get("persistent_registry"):
        return {"action": "blocked", "stop_state": "registry-unavailable", "failure_code": "REGISTRY_UNAVAILABLE", "persistence": "Not verified"}
    if not capabilities.get("create_thread"):
        return {"action": "blocked", "stop_state": "capability-unavailable", "failure_code": "CAPABILITY_MISSING", "missing": ["create_thread"]}
    environment = project.get("creation_environment")
    if environment not in {"local", "worktree"} or project.get("is_git_repository") != (environment == "worktree"):
        return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED", "reuse_key": reuse_key}
    if project.get("placement_readback") != "required":
        return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED", "reuse_key": reuse_key}
    if not _create_placement_proven(project, target_cwd, environment):
        return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED", "reuse_key": reuse_key, "create": False}
    manifest_digest = payload.get("manifest_digest")
    control_id = payload.get("control_id")
    if not manifest_digest or not control_id:
        return {"action": "blocked", "stop_state": "identity-incomplete", "missing": [name for name, value in (("manifest_digest", manifest_digest), ("control_id", control_id)) if not value]}
    operation_id = "create:" + hashlib.sha256(f"{control_id}:{manifest_digest}:{reuse_key}".encode()).hexdigest()
    reservation = payload.get("create_reservation")
    if not isinstance(reservation, dict) or reservation.get("operation_id") != operation_id:
        return {"action": "reserve-create", "control_id": control_id, "reuse_key": reuse_key, "operation_id": operation_id, "expected_manifest_digest": manifest_digest, "create": False}
    if reservation.get("state") in {"invoking", "submission-uncertain"}:
        return {"action": "reconcile-create", "reuse_key": reuse_key, "operation_id": operation_id, "create": False, "enumerate_and_read": True}
    claim = payload.get("create_claim_token")
    if not (reservation.get("control_id") == control_id and reservation.get("state") == "reserved" and reservation.get("manifest_digest") == manifest_digest and reservation.get("acquired") and claim and claim == reservation.get("claim_token")):
        return {"action": "reconcile-create", "reuse_key": reuse_key, "operation_id": operation_id, "create": False, "enumerate_and_read": True}
    return {
        "action": "invoke-create-via-adapter",
        "operation_id": operation_id,
        "direct_host_create": False,
        "adapter_transition": "reserved-to-invoking-and-call-once",
        "reuse_key": reuse_key,
        "title": f"{request.get('project_label', Path(project['canonical_project_root']).name)}｜{responsibility}",
        "project_id": project_id,
        "environment": environment,
        "requested_worker_cwd": target_cwd,
        "readback_required": True,
        "post_create_scope_check": "verified-allowed-roots",
        "execute_locally": False,
    }


def create_readback_plan(payload: dict[str, Any]) -> dict[str, Any]:
    """Finalize a create only after host identity, placement, and operation readback."""
    project, roots, stop = _verified_scope(payload)
    if stop:
        return stop
    operation = payload.get("create_operation")
    task = payload.get("created_task")
    request = payload.get("request", {})
    control_id = payload.get("control_id")
    manifest_digest = payload.get("manifest_digest")
    requested_cwd = canonical_path(request.get("worker_cwd"))
    responsibility = request.get("responsibility")
    project_identity = project.get("project_identity") or project["project_id"] if project else None
    if not control_id or not manifest_digest or not requested_cwd or not responsibility or not any(path_within(requested_cwd, root) for root in roots):
        return {"action": "blocked", "stop_state": "identity-incomplete", "failure_code": "BASIS_DRIFT"}
    expected_key = _reuse_key(project_identity, requested_cwd, responsibility)
    expected_operation_id = "create:" + hashlib.sha256(f"{control_id}:{manifest_digest}:{expected_key}".encode()).hexdigest()
    if not isinstance(operation, dict) or operation.get("state") != "completed" or operation.get("operation_id") != expected_operation_id or operation.get("control_id") != control_id or operation.get("manifest_digest") != manifest_digest or operation.get("reuse_key") != expected_key:
        return {"action": "blocked", "stop_state": "submission-uncertain", "failure_code": "SUBMISSION_UNCERTAIN"}
    if not isinstance(task, dict) or not task.get("thread_id") or not task.get("host_id") or task.get("thread_id") != operation.get("thread_id"):
        return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED"}
    assert project is not None
    if not _in_scope(task, project["project_id"], roots):
        return {"action": "blocked", "stop_state": "placement-unverified", "failure_code": "PLACEMENT_UNVERIFIED", "orphan_reconciliation_required": True}
    cwd = _candidate_cwd(task)
    if not cwd or cwd != requested_cwd or task.get("responsibility") not in {None, responsibility} or _is_terminated(task) or task.get("status") not in RESUMABLE:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    reuse_key = _reuse_key(project_identity, cwd, responsibility)
    return {
        "action": "finalize-created-worker", "operation_id": operation["operation_id"],
        "mapping": {"reuse_key": reuse_key, "thread_id": task["thread_id"], "canonical_cwd": cwd, "project_identity": project_identity, "responsibility": responsibility, "rank": request.get("rank", 0), "closed": False},
        "host_id": task["host_id"], "expected_manifest_digest": payload.get("manifest_digest"), "cas_required": True,
    }


def resume_plan(payload: dict[str, Any]) -> dict[str, Any]:
    capabilities = payload.get("host_capabilities", {})
    required = ("persistent_registry", "list_projects", "list_threads", "read_thread", "send_message_to_thread")
    missing = [name for name in required if not capabilities.get(name)]
    if missing:
        return {"action": "blocked", "stop_state": "registry-unavailable" if "persistent_registry" in missing else "capability-unavailable", "failure_code": "CAPABILITY_MISSING", "missing": missing}
    manifest = payload.get("manifest", {})
    errors = validate_manifest(manifest)
    if errors:
        return {"action": "blocked", "stop_state": "manifest-invalid", "errors": errors}
    computed = digest(manifest)
    if payload.get("manifest_digest") != computed or payload.get("current_registry_digest") != computed:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    project, roots, stop = _verified_scope({
        "project_readback": payload.get("project_readback"),
        "controller_project_root": manifest["canonical_project_root"],
        "controller_cwd": payload.get("new_controller_cwd"),
    })
    if stop or project is None or project.get("project_id") != manifest.get("project_id") or roots != manifest.get("allowed_roots") or project.get("allowed_roots_version") != manifest.get("allowed_roots_version"):
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    new_controller = payload.get("new_controller_thread_id")
    observed_controller = payload.get("observed_new_controller")
    if not new_controller or not isinstance(observed_controller, dict) or observed_controller.get("thread_id") != new_controller:
        return {"action": "blocked", "stop_state": "controller-unresolved", "failure_code": "CONTROLLER_UNRESOLVED"}
    if not _in_scope(observed_controller, manifest["project_id"], roots):
        return _blocked_workspace()
    effective = payload.get("effective_authorization_profile")
    configured = manifest.get("default_authorization_profile")
    if effective not in {None, "implementation", "controlled-delivery"}:
        return {"action": "blocked", "stop_state": "authorization-profile-required", "reason": "unknown-profile"}
    if configured == "controlled-delivery" and effective != "controlled-delivery":
        return {"action": "blocked", "stop_state": "authorization-profile-required", "reason": "current-authority-narrower-than-manifest"}
    if effective == "controlled-delivery" and configured != "controlled-delivery" and not payload.get("explicit_controlled_delivery_authorization"):
        return {"action": "blocked", "stop_state": "authorization-profile-required", "reason": "authority-elevation-unproven"}
    observed = {item.get("thread_id"): item for item in payload.get("observed_workers", []) if isinstance(item, dict)}
    live: list[dict[str, Any]] = []
    terminated: list[dict[str, Any]] = []
    unresolved: list[str] = []
    for mapping in manifest["worker_mappings"]:
        state = observed.get(mapping["thread_id"])
        if mapping.get("closed"):
            terminated.append({"thread_id": mapping["thread_id"], "status": "closed"})
        elif not state or not _in_scope(state, manifest["project_id"], roots) or _candidate_cwd(state) != mapping["canonical_cwd"] or state.get("responsibility") != mapping["responsibility"] or state.get("goal_compatibility") != "compatible":
            unresolved.append(mapping["thread_id"])
        elif _is_terminated(state):
            terminated.append({"thread_id": mapping["thread_id"], "status": "archived" if _is_archived(state) else state.get("status")})
        elif state.get("status") in RESUMABLE:
            live.append(mapping)
        else:
            unresolved.append(mapping["thread_id"])
    if unresolved:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT", "unresolved_workers": unresolved}
    updated = json.loads(json.dumps(manifest))
    old = updated["current_controller_thread_id"]
    if old != new_controller and old not in updated["predecessor_thread_ids"]:
        updated["predecessor_thread_ids"].append(old)
    updated["current_controller_thread_id"] = new_controller
    new_digest = digest(updated)
    messages = [{
        "thread_id": item["thread_id"], "type": "controller-rebind", "control_id": updated["control_id"],
        "previous_controller_thread_id": old, "current_controller_thread_id": new_controller,
        "canonical_project_root": updated["canonical_project_root"], "allowed_roots_version": updated["allowed_roots_version"],
        "reuse_key": item["reuse_key"], "authorization_profile": effective, "manifest_digest": new_digest,
    } for item in live]
    return {"action": "resume-rebind", "expected_manifest_digest": computed, "updated_manifest": updated, "updated_manifest_digest": new_digest, "messages": messages, "terminated_workers": terminated, "readback_required": True}


def notification_plan(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = payload.get("manifest", {})
    errors = validate_manifest(manifest)
    if errors:
        return {"action": "blocked", "stop_state": "manifest-invalid", "errors": errors}
    snapshot_stop = _registry_snapshot_stop(payload, manifest)
    if snapshot_stop:
        return snapshot_stop
    project, roots, stop = _verified_scope({"project_readback": payload.get("project_readback"), "controller_project_root": manifest["canonical_project_root"], "controller_cwd": payload.get("controller_cwd")})
    if stop or project is None or project.get("project_id") != manifest["project_id"] or roots != manifest["allowed_roots"] or project.get("allowed_roots_version") != manifest["allowed_roots_version"]:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    controller = payload.get("observed_controller", {})
    worker = payload.get("observed_worker", {})
    if not isinstance(controller, dict) or controller.get("thread_id") != manifest["current_controller_thread_id"]:
        return {"action": "blocked", "stop_state": "controller-unresolved", "failure_code": "CONTROLLER_UNRESOLVED"}
    if not _in_scope(controller, manifest["project_id"], roots):
        return _blocked_workspace()
    mapping = next((item for item in manifest["worker_mappings"] if item.get("thread_id") == worker.get("thread_id")), None) if isinstance(worker, dict) else None
    if not mapping or mapping.get("closed") or _is_terminated(worker) or not _in_scope(worker, manifest["project_id"], roots) or _candidate_cwd(worker) != mapping.get("canonical_cwd") or worker.get("responsibility") != mapping.get("responsibility"):
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    event_sequence = payload.get("event_sequence")
    if not isinstance(event_sequence, int) or event_sequence < 0:
        return {"action": "blocked", "stop_state": "identity-incomplete", "missing": ["event_sequence"]}
    operation_id = "notify:" + hashlib.sha256(f"{manifest['control_id']}:{worker['thread_id']}:{event_sequence}".encode()).hexdigest()
    return {
        "action": "notify-via-adapter", "operation_id": operation_id,
        "expected_registry_digest": digest(manifest), "expected_controller_thread_id": controller["thread_id"],
        "worker_thread_id": worker["thread_id"], "event_sequence": event_sequence,
        "adapter_transition": "read-current-resolve-controller-and-send-once",
        "direct_host_send": False, "send": False,
    }


def close_plan(payload: dict[str, Any]) -> dict[str, Any]:
    """Close only after explicit user intent and host archive readback."""
    manifest = payload.get("manifest", {})
    errors = validate_manifest(manifest)
    if errors:
        return {"action": "blocked", "stop_state": "manifest-invalid", "errors": errors}
    snapshot_stop = _registry_snapshot_stop(payload, manifest)
    if snapshot_stop:
        return snapshot_stop
    project, roots, stop = _verified_scope({"project_readback": payload.get("project_readback"), "controller_project_root": manifest["canonical_project_root"], "controller_cwd": payload.get("controller_cwd")})
    if stop or project is None or project.get("project_id") != manifest["project_id"] or roots != manifest["allowed_roots"] or project.get("allowed_roots_version") != manifest["allowed_roots_version"]:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    thread_id = payload.get("thread_id")
    mapping = next((item for item in manifest["worker_mappings"] if item.get("thread_id") == thread_id), None)
    if not mapping:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    if not payload.get("explicit_user_close_authorization"):
        return {"action": "dry-run-close", "thread_id": thread_id, "archive": False, "registry_write": False}
    observed = payload.get("archive_readback")
    archived = isinstance(observed, dict) and (observed.get("status") == "archived" or observed.get("archived") is True)
    if not archived or observed.get("thread_id") != thread_id:
        return {"action": "blocked", "stop_state": "archive-unverified", "failure_code": "ARCHIVE_UNVERIFIED"}
    if not observed.get("kind") or not observed.get("project_id") or _candidate_cwd(observed) is None:
        return {"action": "blocked", "stop_state": "archive-unverified", "failure_code": "ARCHIVE_UNVERIFIED"}
    if not _in_scope(observed, manifest["project_id"], manifest["allowed_roots"]):
        return _blocked_workspace(thread_id=thread_id)
    updated = json.loads(json.dumps(manifest))
    for item in updated["worker_mappings"]:
        if item["thread_id"] == thread_id:
            item["closed"] = True
    return {"action": "close-card", "expected_manifest_digest": digest(manifest), "updated_manifest": updated, "updated_manifest_digest": digest(updated), "cas_required": True}


def worker_status_basis(manifest: dict[str, Any], mapping: dict[str, Any]) -> str:
    return digest({
        "schema_version": "workspace-taskboard-worker-basis/v1",
        "control_id": manifest["control_id"],
        "project_id": manifest["project_id"],
        "canonical_project_root": manifest["canonical_project_root"],
        "allowed_roots_version": manifest["allowed_roots_version"],
        "allowed_roots": manifest["allowed_roots"],
        "reuse_key": mapping["reuse_key"],
        "thread_id": mapping["thread_id"],
        "canonical_cwd": mapping["canonical_cwd"],
        "project_identity": mapping["project_identity"],
        "responsibility": mapping["responsibility"],
    })


def _valid_envelope(envelope: dict[str, Any], manifest: dict[str, Any], mapping: dict[str, Any]) -> bool:
    return (
        envelope.get("type") == "worker-status"
        and envelope.get("schema_version") == "workspace-taskboard-worker-status/v1"
        and envelope.get("control_id") == manifest["control_id"]
        and envelope.get("worker_thread_id") == mapping["thread_id"]
        and envelope.get("reuse_key") == mapping["reuse_key"]
        and isinstance(envelope.get("event_sequence"), int)
        and isinstance(envelope.get("observed_at"), str) and bool(envelope.get("observed_at"))
        and envelope.get("worker_basis_digest") == worker_status_basis(manifest, mapping)
        and envelope.get("allowed_roots_version") == manifest["allowed_roots_version"]
        and canonical_path(envelope.get("canonical_cwd")) == mapping["canonical_cwd"]
        and envelope.get("status") in {"queued", "active", *WAITING_STATES, *FINISHED_STATES}
    )


def _host_status(state: dict[str, Any] | None) -> str:
    if not state:
        return "unreachable"
    if _is_archived(state):
        return "archived"
    if state.get("status") in TERMINATED:
        return "unreachable"
    if state.get("status") in {"active", "running"}:
        return "running"
    return "idle"


def _live_status_projection(payload: dict[str, Any]) -> dict[str, Any]:
    project, roots, stop = _verified_scope(payload)
    if stop or project is None:
        return stop or {"action": "blocked", "stop_state": "project-unverified", "failure_code": "PLACEMENT_UNVERIFIED"}
    states = [item for item in payload.get("observed_threads", []) if isinstance(item, dict) and _in_scope(item, project["project_id"], roots)]
    cards = []
    for state in states:
        host_status = _host_status(state)
        worker_status = "active" if host_status == "running" else "blocked" if host_status in {"archived", "unreachable"} else "queued"
        cards.append({
            "title": _safe_display(state.get("title")), "thread_id": state.get("thread_id"), "host_id": state.get("host_id"),
            "canonical_cwd": _candidate_cwd(state), "cwd_label": os.path.relpath(_candidate_cwd(state), project["canonical_project_root"]),
            "responsibility": _safe_display(state.get("responsibility")), "host_status": host_status, "worker_status": worker_status,
            "board_status": "unmapped", "recent_goal": _safe_display(state.get("recent_goal")),
            "recommended_next_action": "Restore or create a successor" if host_status == "archived" else "Read current task",
            "route": state.get("route"), "rank": 0, "group": "等待" if worker_status == "blocked" else "执行中",
        })
    cards.sort(key=lambda item: (item["group"], item["title"], item["thread_id"] or ""))
    return {
        "action": "status-projection", "project": {"project_id": project["project_id"], "project_identity": project.get("project_identity") or project["project_id"], "canonical_project_root": project["canonical_project_root"], "allowed_roots": roots},
        "cards": cards, "latest_single_panel": True, "updates_existing_message": False, "registry_mode": "live-only",
        "capability_note": "Live-only projection; rank, closed policy, controller mapping, and semantic terminal status require a verified registry manifest.",
    }


def status_projection(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = payload.get("manifest")
    if manifest is None or manifest == {}:
        return _live_status_projection(payload)
    errors = validate_manifest(manifest)
    if errors:
        return {"action": "blocked", "stop_state": "manifest-invalid", "errors": errors}
    snapshot_stop = _registry_snapshot_stop(payload, manifest)
    if snapshot_stop:
        return snapshot_stop
    project, roots, stop = _verified_scope({"project_readback": payload.get("project_readback"), "controller_project_root": manifest["canonical_project_root"], "controller_cwd": payload.get("controller_cwd")})
    if stop or project is None or project.get("project_id") != manifest["project_id"] or roots != manifest["allowed_roots"] or project.get("allowed_roots_version") != manifest["allowed_roots_version"]:
        return {"action": "blocked", "stop_state": "basis-drift", "failure_code": "BASIS_DRIFT"}
    observed = {item.get("thread_id"): item for item in payload.get("observed_threads", []) if isinstance(item, dict)}
    cards: list[dict[str, Any]] = []
    for mapping in manifest["worker_mappings"]:
        state = observed.get(mapping["thread_id"])
        if state and not _in_scope(state, manifest["project_id"], manifest["allowed_roots"]):
            state = None
        valid_envelopes = [item for item in payload.get("worker_envelopes", []) if isinstance(item, dict) and _valid_envelope(item, manifest, mapping)]
        envelope = max(valid_envelopes, key=lambda item: item["event_sequence"], default={})
        host_status = _host_status(state)
        semantic = envelope.get("status") if _valid_envelope(envelope, manifest, mapping) else "blocked" if host_status in {"unreachable", "archived"} else "queued"
        closed = bool(mapping.get("closed"))
        group = "已关闭" if closed else "已结束" if semantic in FINISHED_STATES else "等待" if semantic in WAITING_STATES else "执行中"
        cards.append({
            "title": _safe_display(state.get("title")) if state else "Not verified", "thread_id": mapping["thread_id"], "host_id": state.get("host_id") if state else None,
            "canonical_cwd": mapping["canonical_cwd"], "cwd_label": os.path.relpath(mapping["canonical_cwd"], manifest["canonical_project_root"]),
            "responsibility": _safe_display(mapping["responsibility"]), "host_status": host_status, "worker_status": semantic,
            "board_status": "closed" if closed else "open", "recent_goal": _safe_display(state.get("recent_goal")) if state else "Not verified",
            "recommended_next_action": envelope.get("recommended_next_action", "Read current task" if state else "Reconcile task reachability"),
            "route": state.get("route") if state else None, "rank": mapping.get("rank", 0), "group": group,
        })
    cards.sort(key=lambda item: (item["group"], item["rank"], item["title"], item["thread_id"]))
    return {
        "action": "status-projection", "project": {"project_id": manifest["project_id"], "project_identity": manifest["project_identity"], "canonical_project_root": manifest["canonical_project_root"], "allowed_roots": manifest["allowed_roots"]},
        "cards": cards, "latest_single_panel": True, "updates_existing_message": False,
        "capability_note": "The host has not exposed in-place message refresh; each status call returns a new current projection.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("route", "create-readback", "resume", "notify", "close", "status", "validate-manifest"))
    parser.add_argument("input", nargs="?", default="-")
    args = parser.parse_args()
    text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    payload = json.loads(text)
    if args.command == "route": result = route(payload)
    elif args.command == "create-readback": result = create_readback_plan(payload)
    elif args.command == "resume": result = resume_plan(payload)
    elif args.command == "notify": result = notification_plan(payload)
    elif args.command == "close": result = close_plan(payload)
    elif args.command == "status": result = status_projection(payload)
    else:
        errors = validate_manifest(payload)
        result = {"valid": not errors, "errors": errors, "digest": digest(payload) if not errors else None}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("valid", result.get("action") != "blocked") else 1


if __name__ == "__main__":
    raise SystemExit(main())
