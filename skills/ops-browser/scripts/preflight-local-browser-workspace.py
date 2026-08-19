#!/usr/bin/env python3
"""Fail-closed preflight for configured local-browser session/group reuse."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


READY = 0
INVALID_INPUT = 2
CREATION_REQUIRED = 10
SETUP_REQUIRED = 11
CAPABILITY_UNAVAILABLE = 20
AVAILABLE = "available"


def _read_record(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("preflight input must be a JSON object")
    return value


def _matching(
    values: Any, *, name: str, browser_id: str, stable_id_key: str
) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    return [
        value
        for value in values
        if isinstance(value, dict)
        and value.get("name") == name
        and value.get("browser_id") == browser_id
        and isinstance(value.get(stable_id_key), str)
        and bool(value[stable_id_key])
    ]


def _named(values: Any, *, name: str, browser_id: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    return [
        value
        for value in values
        if isinstance(value, dict)
        and value.get("name") == name
        and value.get("browser_id") == browser_id
    ]


def _validate_observations(values: Any, *, label: str, stable_id_key: str) -> None:
    if not isinstance(values, list):
        raise ValueError(f"observations.{label} must be a list when its policy is enabled")
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ValueError(f"observations.{label}[{index}] must be an object")
        for key in ("name", "browser_id"):
            if not isinstance(value.get(key), str) or not value[key]:
                raise ValueError(
                    f"observations.{label}[{index}].{key} must be a non-empty string"
                )
        if stable_id_key in value and (
            not isinstance(value[stable_id_key], str) or not value[stable_id_key]
        ):
            raise ValueError(
                f"observations.{label}[{index}].{stable_id_key} must be a non-empty string"
            )


def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if record.get("schema_version") != "local-browser-workspace-preflight/v1":
        raise ValueError("unsupported schema_version")

    if record.get("browser_surface") != "user-local-browser":
        raise ValueError(
            "local-browser workspace policy applies only to user-local-browser"
        )

    selected_browser_id = record.get("selected_browser_id")
    if not isinstance(selected_browser_id, str) or not selected_browser_id:
        raise ValueError("selected_browser_id must be a non-empty string")

    instances = record.get("browser_instances")
    if not isinstance(instances, list):
        raise ValueError("browser_instances must be a list")
    selected_instances = [
        item
        for item in instances
        if isinstance(item, dict) and item.get("browser_id") == selected_browser_id
    ]
    selected_browser_available = (
        len(selected_instances) == 1 and selected_instances[0].get("available") is True
    )

    reconnected_from = record.get("reconnected_from_browser_id")
    if reconnected_from is not None:
        if not isinstance(reconnected_from, str) or not reconnected_from:
            raise ValueError("reconnected_from_browser_id must be a non-empty string")
        if reconnected_from == selected_browser_id:
            reasons.append("reconnect did not produce a fresh browser identity")
        stale_instances = [
            item
            for item in instances
            if isinstance(item, dict) and item.get("browser_id") == reconnected_from
        ]
        if not stale_instances or any(item.get("available") is not False for item in stale_instances):
            reasons.append("stale browser identity is not proven unavailable")

    policy = record.get("policy")
    capabilities = record.get("capabilities")
    observations = record.get("observations")
    if not isinstance(policy, dict):
        raise ValueError("policy must be an object")
    if not isinstance(capabilities, dict):
        raise ValueError("capabilities must be an object")
    if not isinstance(observations, dict):
        raise ValueError("observations must be an object")

    screen_session = record.get("screen_session", "unknown")
    if screen_session not in {"unlocked", "locked", "unknown"}:
        raise ValueError("screen_session must be unlocked, locked, or unknown")
    lock_safe_required = record.get("lock_safe_required", False)
    if not isinstance(lock_safe_required, bool):
        raise ValueError("lock_safe_required must be a boolean")
    if lock_safe_required and screen_session == "unknown":
        reasons.append("lock-safe operation requires a known screen-session state")

    session_policy = policy.get("control_session")
    group_policy = policy.get("tab_grouping")
    if not isinstance(session_policy, dict) or not isinstance(group_policy, dict):
        raise ValueError("control_session and tab_grouping policies are required")

    if not isinstance(session_policy.get("enabled"), bool):
        raise ValueError("control_session.enabled must be a boolean")
    if not isinstance(group_policy.get("enabled"), bool):
        raise ValueError("tab_grouping.enabled must be a boolean")
    session_enabled = session_policy["enabled"]
    group_enabled = group_policy["enabled"]
    execution_profile = policy.get(
        "execution_profile", {"mode": "existing-user-profile"}
    )
    if not isinstance(execution_profile, dict):
        raise ValueError("execution_profile must be an object")
    execution_mode = execution_profile.get("mode")
    if execution_mode not in {"existing-user-profile", "dedicated-user-data-dir"}:
        raise ValueError("unsupported execution_profile.mode")
    if execution_mode == "dedicated-user-data-dir":
        if session_enabled or group_enabled:
            reasons.append(
                "dedicated profile mode requires control session and grouping disabled"
            )
    session_name = session_policy.get("name") if session_enabled else None
    group_name = group_policy.get("name") if group_enabled else None
    if session_enabled and (not isinstance(session_name, str) or not session_name):
        raise ValueError("control_session.name must be a non-empty string when enabled")
    if group_enabled and (not isinstance(group_name, str) or not group_name):
        raise ValueError("tab_grouping.name must be a non-empty string when enabled")
    if session_enabled and not isinstance(session_policy.get("allow_name_session"), bool):
        raise ValueError("control_session.allow_name_session must be a boolean when enabled")
    if group_enabled and not isinstance(group_policy.get("allow_group_creation"), bool):
        raise ValueError("tab_grouping.allow_group_creation must be a boolean when enabled")

    controller_constraints = record.get("controller_constraints", {})
    if not isinstance(controller_constraints, dict):
        raise ValueError("controller_constraints must be an object")
    requires_task_name = controller_constraints.get(
        "requires_task_specific_session_name", False
    )
    if not isinstance(requires_task_name, bool):
        raise ValueError(
            "controller_constraints.requires_task_specific_session_name must be a boolean"
        )
    if session_enabled and requires_task_name:
        reasons.append(
            "controller task-specific session naming conflicts with configured workspace"
        )

    selected_backend = record.get("selected_backend", "not-applicable")
    if not isinstance(selected_backend, str) or not selected_backend:
        raise ValueError("selected_backend must be a non-empty string")
    background_setup_attempted = record.get("background_setup_attempted", False)
    if not isinstance(background_setup_attempted, bool):
        raise ValueError("background_setup_attempted must be a boolean")
    background_setup_required = False
    if screen_session == "locked":
        lock_policy = policy.get("locked_session")
        if not isinstance(lock_policy, dict):
            raise ValueError("locked_session policy is required while locked")
        if lock_policy.get("enabled") is not True:
            reasons.append("locked-session local control is disabled")
        allowed_backends = lock_policy.get("allowed_backends")
        if not isinstance(allowed_backends, list) or not all(
            isinstance(item, str) and item for item in allowed_backends
        ):
            raise ValueError("locked_session.allowed_backends must be a string list")
        if selected_backend not in allowed_backends:
            reasons.append("selected backend is not allowed while locked")
        prepared_control = capabilities.get("preconnected_browser_control") == AVAILABLE
        reconnect_allowed = lock_policy.get("allow_transport_reconnect") is True
        prepared_reconnect = reconnect_allowed and all(
            capabilities.get(capability) == AVAILABLE
            for capability in (
                "prepared_endpoint_available",
                "background_safe_transport_reconnect",
            )
        )
        background_setup_allowed = (
            execution_mode == "dedicated-user-data-dir"
            and execution_profile.get("require_existing_when_locked") is False
            and lock_policy.get("require_prepared_control") is False
            and capabilities.get("background_safe_browser_setup") == AVAILABLE
            and lock_policy.get("prohibit_browser_launch") is False
            and lock_policy.get("prohibit_debug_enablement") is False
            and lock_policy.get("prohibit_window_activation") is True
            and lock_policy.get("prohibit_keyboard_pointer") is True
            and lock_policy.get("prohibit_profile_import") is True
        )

        prohibited_constraints = {
            "requires_browser_launch": (
                "prohibit_browser_launch",
                "locked-session policy prohibits browser launch",
            ),
            "requires_debug_enablement": (
                "prohibit_debug_enablement",
                "locked-session policy prohibits browser debugging enablement",
            ),
            "requires_gui_automation": (
                "prohibit_keyboard_pointer",
                "locked-session policy prohibits GUI automation",
            ),
            "requires_profile_import": (
                "prohibit_profile_import",
                "locked-session policy prohibits browser profile import",
            ),
        }
        for key, (policy_key, reason) in prohibited_constraints.items():
            value = controller_constraints.get(key, False)
            if not isinstance(value, bool):
                raise ValueError(f"controller_constraints.{key} must be a boolean")
            if value and lock_policy.get(policy_key) is not False:
                reasons.append(reason)

        if selected_backend == "direct-cdp" and selected_browser_available:
            cdp_policy = lock_policy.get("cdp")
            if not isinstance(cdp_policy, dict):
                raise ValueError("locked_session.cdp policy is required for direct-cdp")
            cdp_requirements = {
                "require_loopback_only": "cdp_loopback_only",
                "require_dedicated_profile": "cdp_dedicated_profile",
                "require_prelock_roundtrip": "cdp_prelock_roundtrip_verified",
            }
            for policy_key, capability in cdp_requirements.items():
                if cdp_policy.get(policy_key) is True and capabilities.get(capability) != AVAILABLE:
                    reasons.append(
                        f"required locked-session capability unavailable: {capability}"
                    )

        if not selected_browser_available:
            if background_setup_attempted:
                reasons.append("background browser setup already attempted without a verified endpoint")
            elif not background_setup_allowed:
                reasons.append("no policy-authorized background browser setup path is available")
            elif selected_backend != "direct-cdp":
                reasons.append("background browser setup requires direct-cdp")
            else:
                cdp_policy = lock_policy.get("cdp")
                if not isinstance(cdp_policy, dict):
                    raise ValueError("locked_session.cdp policy is required for direct-cdp")
                if cdp_policy.get("require_loopback_only") is not True:
                    reasons.append("background browser setup requires loopback-only CDP")
                if cdp_policy.get("require_dedicated_profile") is not True:
                    reasons.append("background browser setup requires a dedicated profile")
                if cdp_policy.get("require_prelock_roundtrip") is not False:
                    reasons.append("background browser setup requires pre-lock roundtrip disabled")
                if not reasons:
                    background_setup_required = True
        else:
            for capability in (
                "background_safe_tab_enumeration",
                "background_safe_page_control",
            ):
                if capabilities.get(capability) != AVAILABLE:
                    reasons.append(
                        f"required locked-session capability unavailable: {capability}"
                    )
            if not prepared_control and not prepared_reconnect:
                reasons.append("no current lock-safe browser control path is available")

    if not selected_browser_available and not background_setup_required:
        reasons.append("selected browser identity is not uniquely available")

    if background_setup_required:
        return {
            "schema_version": "local-browser-workspace-preflight-result/v1",
            "state": "setup-required",
            "selected_browser_id": selected_browser_id,
            "screen_session": screen_session,
            "selected_backend": selected_backend,
            "execution_profile_mode": execution_mode,
            "lock_safe_ready": False,
            "resolved_session_id": None,
            "resolved_group_id": None,
            "permitted_actions": {
                "background_browser_setup": True,
                "claim_verified_tab": False,
                "name_session": False,
                "create_tab": False,
                "create_session": False,
                "create_group": False,
            },
            "reasons": [],
        }

    if execution_mode == "dedicated-user-data-dir":
        for capability in (
            "dedicated_profile_identity",
            "loopback_endpoint_ready",
        ):
            if capabilities.get(capability) != AVAILABLE:
                reasons.append(f"required capability unavailable: {capability}")

    sessions: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    create_session = False
    create_group = False

    if session_enabled:
        _validate_observations(
            observations.get("sessions"), label="sessions", stable_id_key="session_id"
        )
        for capability in ("session_enumeration", "stable_session_identity"):
            if capabilities.get(capability) != AVAILABLE:
                reasons.append(f"required capability unavailable: {capability}")
        if session_policy.get("require_verified_reuse") is not True:
            reasons.append("require_verified_reuse must be true")
        named_sessions = _named(
            observations.get("sessions"), name=session_name, browser_id=selected_browser_id
        )
        stale_named_sessions = (
            _named(observations.get("sessions"), name=session_name, browser_id=reconnected_from)
            if reconnected_from is not None
            else []
        )
        sessions = _matching(
            observations.get("sessions"),
            name=session_name,
            browser_id=selected_browser_id,
            stable_id_key="session_id",
        )
        if stale_named_sessions:
            reasons.append("configured session observation is bound to the stale browser identity")
        elif len(named_sessions) == 0:
            if session_policy.get("create_if_missing") is True:
                if session_policy.get("allow_name_session") is not True:
                    reasons.append("configured session creation is disabled")
                else:
                    creation_capabilities = ("managed_session_creation", "session_selection")
                    missing = [
                        capability
                        for capability in creation_capabilities
                        if capabilities.get(capability) != AVAILABLE
                    ]
                    if not missing:
                        create_session = True
                    else:
                        reasons.extend(
                            f"required capability unavailable: {capability}" for capability in missing
                        )
            else:
                reasons.append("configured session is absent and creation is disabled")
        elif len(named_sessions) != 1 or len(sessions) != 1:
            reasons.append("configured session is not uniquely identified on the selected browser")
        else:
            if capabilities.get("session_selection") != AVAILABLE:
                reasons.append("required capability unavailable: session_selection")
            if observations.get("selected_session_id") != sessions[0]["session_id"]:
                reasons.append("configured session selection is not proven")

    # Do not create a session that cannot support the enabled grouping policy.
    if group_enabled and create_session:
        _validate_observations(
            observations.get("groups"), label="groups", stable_id_key="group_id"
        )
        for capability in (
            "group_enumeration",
            "stable_group_identity",
            "group_selection",
            "group_placement",
        ):
            if capabilities.get(capability) != AVAILABLE:
                reasons.append(f"required capability unavailable: {capability}")
        if group_policy.get("require_verified_placement") is not True:
            reasons.append("require_verified_placement must be true")
        named_groups = _named(
            observations.get("groups"), name=group_name, browser_id=selected_browser_id
        )
        stale_named_groups = (
            _named(observations.get("groups"), name=group_name, browser_id=reconnected_from)
            if reconnected_from is not None
            else []
        )
        stable_groups = _matching(
            observations.get("groups"),
            name=group_name,
            browser_id=selected_browser_id,
            stable_id_key="group_id",
        )
        if stale_named_groups:
            reasons.append("configured group observation is bound to the stale browser identity")
        elif len(named_groups) == 0:
            if group_policy.get("create_if_missing") is not True:
                reasons.append("configured group is absent and creation is disabled")
            elif capabilities.get("group_creation") != AVAILABLE:
                reasons.append("required capability unavailable: group_creation")
        elif len(named_groups) != 1 or len(stable_groups) != 1:
            reasons.append("configured group is not uniquely identified on the selected browser")

    # Session creation must complete and be re-enumerated before group resolution.
    if group_enabled and not create_session:
        _validate_observations(
            observations.get("groups"), label="groups", stable_id_key="group_id"
        )
        for capability in ("group_enumeration", "stable_group_identity"):
            if capabilities.get(capability) != AVAILABLE:
                reasons.append(f"required capability unavailable: {capability}")
        if group_policy.get("require_verified_placement") is not True:
            reasons.append("require_verified_placement must be true")
        named_groups = _named(
            observations.get("groups"), name=group_name, browser_id=selected_browser_id
        )
        stale_named_groups = (
            _named(observations.get("groups"), name=group_name, browser_id=reconnected_from)
            if reconnected_from is not None
            else []
        )
        groups = _matching(
            observations.get("groups"),
            name=group_name,
            browser_id=selected_browser_id,
            stable_id_key="group_id",
        )
        if stale_named_groups:
            reasons.append("configured group observation is bound to the stale browser identity")
        elif len(named_groups) == 0:
            if group_policy.get("create_if_missing") is True:
                if group_policy.get("allow_group_creation") is not True:
                    reasons.append("configured group creation is disabled")
                else:
                    creation_capabilities = ("group_creation", "group_selection", "group_placement")
                    missing = [
                        capability
                        for capability in creation_capabilities
                        if capabilities.get(capability) != AVAILABLE
                    ]
                    if not missing:
                        create_group = True
                    else:
                        reasons.extend(
                            f"required capability unavailable: {capability}" for capability in missing
                        )
            else:
                reasons.append("configured group is absent and creation is disabled")
        elif len(named_groups) != 1 or len(groups) != 1:
            reasons.append("configured group is not uniquely identified on the selected browser")
        else:
            for capability in ("group_selection", "group_placement"):
                if capabilities.get(capability) != AVAILABLE:
                    reasons.append(f"required capability unavailable: {capability}")
            if observations.get("selected_group_id") != groups[0]["group_id"]:
                reasons.append("configured group selection is not proven")
            if observations.get("placement_target_group_id") != groups[0]["group_id"]:
                reasons.append("tab placement target is not bound to the verified group identity")

    if screen_session == "locked" and (create_session or create_group):
        reasons.append("locked session requires an existing configured session and group")

    creation_required = not reasons and (create_session or create_group)
    ready = not reasons and not creation_required
    state = "ready" if ready else "creation-required" if creation_required else "capability-unavailable"
    return {
        "schema_version": "local-browser-workspace-preflight-result/v1",
        "state": state,
        "selected_browser_id": selected_browser_id,
        "screen_session": screen_session,
        "selected_backend": selected_backend,
        "execution_profile_mode": execution_mode,
        "lock_safe_ready": ready and screen_session == "locked",
        "resolved_session_id": sessions[0]["session_id"] if ready and session_enabled else None,
        "resolved_group_id": groups[0]["group_id"] if ready and group_enabled else None,
        "permitted_actions": {
            "background_browser_setup": False,
            "claim_verified_tab": ready,
            "name_session": False,
            "create_tab": False,
            "create_session": creation_required and create_session,
            "create_group": creation_required and create_group,
        },
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify stable local-browser session and group reuse before page action."
    )
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(_read_record(args.input))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"state": "invalid-input", "error": str(error)}))
        return INVALID_INPUT
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if result["state"] == "ready":
        return READY
    if result["state"] == "creation-required":
        return CREATION_REQUIRED
    if result["state"] == "setup-required":
        return SETUP_REQUIRED
    return CAPABILITY_UNAVAILABLE


if __name__ == "__main__":
    raise SystemExit(main())
