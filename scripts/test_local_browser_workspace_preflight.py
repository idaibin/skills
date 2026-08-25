#!/usr/bin/env python3
"""Regression tests for strict existing-Chrome workspace reuse."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ops-browser" / "scripts" / "preflight-local-browser-workspace.py"
SPEC = importlib.util.spec_from_file_location("local_browser_workspace_preflight", SCRIPT)
assert SPEC and SPEC.loader
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


def ready_fixture() -> dict:
    return {
        "schema_version": "local-browser-workspace-preflight/v1",
        "browser_surface": "user-local-browser",
        "selected_browser_id": "chrome-new",
        "reconnected_from_browser_id": "chrome-old",
        "browser_instances": [
            {"browser_id": "chrome-old", "available": False},
            {"browser_id": "chrome-new", "available": True},
        ],
        "extension_connector": {
            "connector_id": "chrome-extension",
            "connected": True,
            "browser_id": "chrome-new",
        },
        "browser_profile": {
            "profile_id": "Default",
            "existing_user_profile": True,
            "browser_id": "chrome-new",
        },
        "account_session": {
            "account_session_id": "account-session-verified",
            "verified": True,
            "browser_id": "chrome-new",
            "profile_id": "Default",
        },
        "target": {
            "target_kind": "url",
            "target_id_or_url": "https://example.test/target",
            "target_fingerprint": "target-fingerprint",
            "browser_id": "chrome-new",
            "profile_id": "Default",
            "account_session_id": "account-session-verified",
        },
        "tab": {
            "tab_id": "tab-target",
            "native_group_id": "group-shared",
            "target_fingerprint": "target-fingerprint",
            "browser_id": "chrome-new",
            "profile_id": "Default",
            "account_session_id": "account-session-verified",
        },
        "screen_session": "unlocked",
        "lock_safe_required": False,
        "policy": {
            "execution_profile": {"mode": "existing-user-profile"},
            "control_session": {
                "enabled": True,
                "name": "Shared Workspace",
                "require_verified_reuse": True,
                "create_if_missing": True,
                "allow_name_session": True,
            },
            "tab_grouping": {
                "enabled": True,
                "name": "Shared Workspace",
                "require_verified_placement": True,
                "create_if_missing": True,
                "allow_group_creation": True,
            },
            "locked_session": {
                "enabled": True,
                "require_prepared_control": True,
                "allowed_backends": ["browser-extension-control"],
                "allow_transport_reconnect": True,
                "prohibit_browser_launch": True,
                "prohibit_debug_enablement": True,
                "prohibit_profile_import": True,
                "prohibit_window_activation": True,
                "prohibit_keyboard_pointer": True,
            },
        },
        "selected_backend": "browser-extension-control",
        "capabilities": {
            "session_enumeration": "available",
            "session_selection": "available",
            "stable_session_identity": "available",
            "group_enumeration": "available",
            "group_selection": "available",
            "stable_group_identity": "available",
            "group_creation": "available",
            "group_placement": "available",
            "managed_session_creation": "available",
        },
        "observations": {
            "sessions": [
                {
                    "session_id": "session-shared",
                    "name": "Shared Workspace",
                    "browser_id": "chrome-new",
                }
            ],
            "groups": [
                {
                    "group_id": "group-shared",
                    "name": "Shared Workspace",
                    "browser_id": "chrome-new",
                }
            ],
            "selected_session_id": "session-shared",
            "selected_group_id": "group-shared",
            "placement_target_group_id": "group-shared",
        },
    }


class LocalBrowserWorkspacePreflightTests(unittest.TestCase):
    def test_reconnect_and_reuse_stable_workspace(self) -> None:
        result = PREFLIGHT.evaluate(ready_fixture())
        self.assertEqual("ready", result["state"])
        self.assertEqual("session-shared", result["resolved_session_id"])
        self.assertEqual("group-shared", result["resolved_group_id"])
        self.assertTrue(result["permitted_actions"]["claim_verified_tab"])

    def test_non_local_surface_rejects_grouping_policy(self) -> None:
        fixture = ready_fixture()
        fixture["browser_surface"] = "codex-in-app-browser"
        with self.assertRaisesRegex(ValueError, "only to user-local-browser"):
            PREFLIGHT.evaluate(fixture)

    def test_non_existing_profile_mode_is_invalid(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["execution_profile"]["mode"] = "isolated-profile"
        with self.assertRaisesRegex(ValueError, "must be existing-user-profile"):
            PREFLIGHT.evaluate(fixture)

    def test_controller_task_name_conflict_stops(self) -> None:
        fixture = ready_fixture()
        fixture["controller_constraints"] = {
            "requires_task_specific_session_name": True
        }
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "controller task-specific session naming conflicts with configured workspace",
            result["reasons"],
        )

    def test_disabled_session_creation_stops(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["control_session"]["allow_name_session"] = False
        fixture["observations"]["sessions"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("configured session creation is disabled", result["reasons"])

    def test_disabled_group_creation_stops(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["tab_grouping"]["allow_group_creation"] = False
        fixture["observations"]["groups"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("configured group creation is disabled", result["reasons"])

    def test_missing_group_can_request_exact_creation(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("creation-required", result["state"])
        self.assertTrue(result["permitted_actions"]["create_group"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_locked_session_reuses_prepared_extension(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["lock_safe_required"] = True
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertTrue(result["lock_safe_ready"])

    def test_locked_session_rejects_unavailable_browser(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["browser_instances"][1]["available"] = False
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "selected browser identity is not uniquely available", result["reasons"]
        )

    def test_locked_session_rejects_browser_launch_and_profile_import(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        fixture["controller_constraints"] = {
            "requires_browser_launch": True,
            "requires_profile_import": True,
        }
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn("locked-session policy prohibits browser launch", result["reasons"])
        self.assertIn(
            "locked-session policy prohibits browser profile import", result["reasons"]
        )

    def test_locked_session_always_rejects_debug_enablement(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        fixture["controller_constraints"] = {"requires_debug_enablement": True}
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "locked-session policy prohibits browser debugging enablement",
            result["reasons"],
        )

    def test_locked_session_requires_debug_enablement_prohibition(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        fixture["policy"]["locked_session"]["prohibit_debug_enablement"] = False
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "locked-session policy must prohibit browser debugging enablement",
            result["reasons"],
        )

    def test_locked_session_rejects_gui_automation(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        fixture["controller_constraints"] = {"requires_gui_automation": True}
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn("locked-session policy prohibits GUI automation", result["reasons"])

    def test_locked_session_requires_background_page_control(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "unavailable",
            }
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "required locked-session capability unavailable: background_safe_page_control",
            result["reasons"],
        )

    def test_unknown_screen_state_stops_when_lock_safety_required(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "unknown"
        fixture["lock_safe_required"] = True
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "lock-safe operation requires a known screen-session state", result["reasons"]
        )

    def test_stale_browser_observations_stop(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"][0]["browser_id"] = "chrome-old"
        fixture["observations"]["groups"][0]["browser_id"] = "chrome-old"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_group_label_without_stable_identity_stops(self) -> None:
        fixture = ready_fixture()
        fixture["capabilities"]["stable_group_identity"] = "unavailable"
        fixture["observations"]["groups"] = [
            {"name": "Shared Workspace", "browser_id": "chrome-new"}
        ]
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "required capability unavailable: stable_group_identity", result["reasons"]
        )

    def test_group_placement_must_match_verified_group(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["placement_target_group_id"] = "group-other"
        result = PREFLIGHT.evaluate(fixture)
        self.assertIn(
            "tab placement target is not bound to the verified group identity",
            result["reasons"],
        )

    def test_missing_identity_binding_is_invalid_input(self) -> None:
        for field in (
            "extension_connector",
            "browser_profile",
            "account_session",
            "target",
            "tab",
        ):
            fixture = ready_fixture()
            fixture.pop(field)
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, f"{field} must be an object"):
                    PREFLIGHT.evaluate(fixture)

    def test_tab_must_bind_to_verified_native_group(self) -> None:
        fixture = ready_fixture()
        fixture["tab"]["native_group_id"] = "group-other"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])
        self.assertIn(
            "tab native group is not bound to the verified group identity",
            result["reasons"],
        )


if __name__ == "__main__":
    unittest.main()
