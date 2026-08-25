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


def _observed_tab_ids(values: Any) -> set[str]:
    if not isinstance(values, list):
        raise ValueError("observations.target_tabs must be a list")
    result: set[str] = set()
    for index, value in enumerate(values):
        if isinstance(value, str) and value:
            result.add(value)
        elif isinstance(value, dict) and isinstance(value.get("tab_id"), str) and value["tab_id"]:
            result.add(value["tab_id"])
        else:
            raise ValueError(
                f"observations.target_tabs[{index}] must be a tab id or object with tab_id"
            )
    return result


def _required_binding(record: dict[str, Any], key: str) -> dict[str, Any]:
    value = record.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def _required_string(value: dict[str, Any], key: str, *, label: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result:
        raise ValueError(f"{label}.{key} must be a non-empty string")
    return result


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

    connector = _required_binding(record, "extension_connector")
    connector_id = _required_string(connector, "connector_id", label="extension_connector")
    if connector.get("connected") is not True:
        raise ValueError("extension_connector.connected must be true")
    if _required_string(connector, "browser_id", label="extension_connector") != selected_browser_id:
        raise ValueError("extension_connector.browser_id must match selected_browser_id")

    profile = _required_binding(record, "browser_profile")
    profile_id = _required_string(profile, "profile_id", label="browser_profile")
    if profile.get("existing_user_profile") is not True:
        raise ValueError("browser_profile.existing_user_profile must be true")
    if _required_string(profile, "browser_id", label="browser_profile") != selected_browser_id:
        raise ValueError("browser_profile.browser_id must match selected_browser_id")

    account_session = _required_binding(record, "account_session")
    account_session_id = _required_string(
        account_session, "account_session_id", label="account_session"
    )
    if account_session.get("verified") is not True:
        raise ValueError("account_session.verified must be true")
    if _required_string(account_session, "browser_id", label="account_session") != selected_browser_id:
        raise ValueError("account_session.browser_id must match selected_browser_id")
    if _required_string(account_session, "profile_id", label="account_session") != profile_id:
        raise ValueError("account_session.profile_id must match browser_profile.profile_id")

    target = _required_binding(record, "target")
    _required_string(target, "target_kind", label="target")
    target_id_or_url = _required_string(target, "target_id_or_url", label="target")
    target_fingerprint = _required_string(target, "target_fingerprint", label="target")
    if _required_string(target, "browser_id", label="target") != selected_browser_id:
        raise ValueError("target.browser_id must match selected_browser_id")
    if _required_string(target, "profile_id", label="target") != profile_id:
        raise ValueError("target.profile_id must match browser_profile.profile_id")
    if _required_string(target, "account_session_id", label="target") != account_session_id:
        raise ValueError("target.account_session_id must match verified account_session")

    target_tab_state = record.get("target_tab_state", "present")
    if target_tab_state not in {"present", "absent"}:
        raise ValueError("target_tab_state must be present or absent")
    tab_id: str | None = None
    tab_group_id: str | None = None
    if target_tab_state == "present":
        tab = _required_binding(record, "tab")
        tab_id = _required_string(tab, "tab_id", label="tab")
        if _required_string(tab, "browser_id", label="tab") != selected_browser_id:
            raise ValueError("tab.browser_id must match selected_browser_id")
        if _required_string(tab, "profile_id", label="tab") != profile_id:
            raise ValueError("tab.profile_id must match browser_profile.profile_id")
        if _required_string(tab, "account_session_id", label="tab") != account_session_id:
            raise ValueError("tab.account_session_id must match verified account_session")
        if _required_string(tab, "target_fingerprint", label="tab") != target_fingerprint:
            raise ValueError("tab.target_fingerprint must match target.target_fingerprint")
        tab_group_id = _required_string(tab, "native_group_id", label="tab")
    elif record.get("tab") is not None:
        raise ValueError("tab must be omitted or null when target_tab_state is absent")

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
    observed_target_tab_ids = _observed_tab_ids(observations.get("target_tabs"))
    if target_tab_state == "present" and tab_id not in observed_target_tab_ids:
        reasons.append("target tab identity is not proven by current enumeration")

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
    if execution_mode != "existing-user-profile":
        raise ValueError("execution_profile.mode must be existing-user-profile")
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
    if group_enabled and not isinstance(
        group_policy.get("create_tab_if_target_missing", False), bool
    ):
        raise ValueError(
            "tab_grouping.create_tab_if_target_missing must be a boolean when enabled"
        )

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
        if lock_policy.get("prohibit_debug_enablement") is not True:
            reasons.append("locked-session policy must prohibit browser debugging enablement")
        prepared_control = capabilities.get("preconnected_browser_control") == AVAILABLE
        reconnect_allowed = lock_policy.get("allow_transport_reconnect") is True
        prepared_reconnect = reconnect_allowed and all(
            capabilities.get(capability) == AVAILABLE
            for capability in (
                "prepared_endpoint_available",
                "background_safe_transport_reconnect",
            )
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
            if value and (key == "requires_debug_enablement" or lock_policy.get(policy_key) is not False):
                reasons.append(reason)

        if selected_browser_available:
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

    if not selected_browser_available:
        reasons.append("selected browser identity is not uniquely available")

    sessions: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    create_session = False
    create_group = False
    create_tab = False

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
            if target_tab_state == "present":
                if tab_group_id != groups[0]["group_id"]:
                    reasons.append("tab native group is not bound to the verified group identity")
            else:
                if observed_target_tab_ids:
                    reasons.append("target tab absence is not proven by current enumeration")
                if group_policy.get("create_tab_if_target_missing") is not True:
                    reasons.append("target tab is absent and creation is disabled")
                for capability in (
                    "tab_enumeration",
                    "tab_creation",
                    "stable_tab_identity",
                    "group_placement",
                ):
                    if capabilities.get(capability) != AVAILABLE:
                        reasons.append(f"required capability unavailable: {capability}")
                if not reasons:
                    create_tab = True

    if screen_session == "locked" and (create_session or create_group or create_tab):
        reasons.append("locked session requires an existing configured session, group, and tab")

    creation_required = not reasons and (create_session or create_group or create_tab)
    ready = not reasons and not creation_required
    state = "ready" if ready else "creation-required" if creation_required else "capability-unavailable"
    return {
        "schema_version": "local-browser-workspace-preflight-result/v1",
        "state": state,
        "selected_browser_id": selected_browser_id,
        "screen_session": screen_session,
        "selected_backend": selected_backend,
        "connector_id": connector_id,
        "profile_id": profile_id,
        "account_session_id": account_session_id,
        "target_id_or_url": target_id_or_url,
        "target_fingerprint": target_fingerprint,
        "tab_id": tab_id,
        "execution_profile_mode": execution_mode,
        "lock_safe_ready": ready and screen_session == "locked",
        "resolved_session_id": sessions[0]["session_id"] if ready and session_enabled else None,
        "resolved_group_id": groups[0]["group_id"] if ready and group_enabled else None,
        "permitted_actions": {
            "claim_verified_tab": ready,
            "name_session": False,
            "create_tab": creation_required and create_tab,
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
    return CAPABILITY_UNAVAILABLE


if __name__ == "__main__":
    raise SystemExit(main())
