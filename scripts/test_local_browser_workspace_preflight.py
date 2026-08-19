#!/usr/bin/env python3
"""Regression tests for strict local-browser workspace reuse."""

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
                "allowed_backends": [
                    "browser-native-control",
                    "browser-extension-control",
                    "direct-cdp",
                ],
                "allow_transport_reconnect": True,
                "prohibit_browser_launch": True,
                "prohibit_debug_enablement": True,
                "prohibit_profile_import": True,
                "prohibit_window_activation": True,
                "prohibit_keyboard_pointer": True,
                "cdp": {
                    "require_loopback_only": True,
                    "require_dedicated_profile": True,
                    "require_prelock_roundtrip": True,
                },
            },
        },
        "selected_backend": "browser-native-control",
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
                {"session_id": "session-shared", "name": "Shared Workspace", "browser_id": "chrome-new"}
            ],
            "groups": [
                {"group_id": "group-shared", "name": "Shared Workspace", "browser_id": "chrome-new"}
            ],
            "selected_session_id": "session-shared",
            "selected_group_id": "group-shared",
            "placement_target_group_id": "group-shared",
        },
    }


class LocalBrowserWorkspacePreflightTests(unittest.TestCase):
    def test_two_chrome_instances_reconnect_and_reuse_stable_workspace(self) -> None:
        result = PREFLIGHT.evaluate(ready_fixture())
        self.assertEqual("ready", result["state"])
        self.assertEqual("session-shared", result["resolved_session_id"])
        self.assertEqual("group-shared", result["resolved_group_id"])
        self.assertFalse(result["permitted_actions"]["name_session"])
        self.assertFalse(result["permitted_actions"]["create_tab"])

    def test_non_local_surface_cannot_receive_chrome_grouping_policy(self) -> None:
        fixture = ready_fixture()
        fixture["browser_surface"] = "codex-in-app-browser"
        with self.assertRaisesRegex(ValueError, "only to user-local-browser"):
            PREFLIGHT.evaluate(fixture)

    def test_dedicated_profile_is_ready_without_session_or_group(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir"
        }
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["capabilities"] = {
            "dedicated_profile_identity": "available",
            "loopback_endpoint_ready": "available",
        }
        fixture["observations"] = {}
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertEqual(
            "dedicated-user-data-dir", result["execution_profile_mode"]
        )
        self.assertIsNone(result["resolved_session_id"])
        self.assertIsNone(result["resolved_group_id"])

    def test_dedicated_profile_rejects_task_grouping(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir"
        }
        fixture["capabilities"].update(
            {
                "dedicated_profile_identity": "available",
                "loopback_endpoint_ready": "available",
            }
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "dedicated profile mode requires control session and grouping disabled",
            result["reasons"],
        )

    def test_controller_required_task_name_stops_before_browser_action(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["control_session"]["allow_name_session"] = False
        fixture["policy"]["tab_grouping"]["allow_group_creation"] = False
        fixture["controller_constraints"] = {
            "requires_task_specific_session_name": True,
        }
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "controller task-specific session naming conflicts with configured workspace",
            result["reasons"],
        )
        self.assertFalse(result["permitted_actions"]["name_session"])
        self.assertFalse(result["permitted_actions"]["create_group"])

    def test_disabled_session_creation_cannot_be_reenabled_by_capability(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["control_session"]["allow_name_session"] = False
        fixture["observations"]["sessions"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("configured session creation is disabled", result["reasons"])
        self.assertFalse(result["permitted_actions"]["create_session"])

    def test_disabled_group_creation_cannot_be_reenabled_by_capability(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["tab_grouping"]["allow_group_creation"] = False
        fixture["observations"]["groups"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("configured group creation is disabled", result["reasons"])
        self.assertFalse(result["permitted_actions"]["create_group"])

    def test_locked_session_reuses_preconnected_background_safe_workspace(self) -> None:
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

    def test_locked_session_can_reconnect_prepared_loopback_cdp(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["lock_safe_required"] = True
        fixture["selected_backend"] = "direct-cdp"
        fixture["capabilities"].update(
            {
                "prepared_endpoint_available": "available",
                "background_safe_transport_reconnect": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
                "cdp_loopback_only": "available",
                "cdp_dedicated_profile": "available",
                "cdp_prelock_roundtrip_verified": "available",
            }
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertTrue(result["lock_safe_ready"])
        self.assertEqual("direct-cdp", result["selected_backend"])

    def test_locked_cdp_without_prelock_roundtrip_continues_when_not_required(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["selected_backend"] = "direct-cdp"
        fixture["capabilities"].update(
            {
                "prepared_endpoint_available": "available",
                "background_safe_transport_reconnect": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
                "cdp_loopback_only": "available",
                "cdp_dedicated_profile": "available",
                "cdp_prelock_roundtrip_verified": "unknown",
            }
        )
        fixture["policy"]["locked_session"]["cdp"]["require_prelock_roundtrip"] = False
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])

    def test_locked_session_cannot_launch_browser_or_import_profile(self) -> None:
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
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("locked-session policy prohibits browser launch", result["reasons"])
        self.assertIn(
            "locked-session policy prohibits browser profile import", result["reasons"]
        )

    def test_locked_session_allows_one_background_setup_when_policy_permits(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["selected_backend"] = "direct-cdp"
        fixture["browser_instances"][1]["available"] = False
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir",
            "require_existing_when_locked": False,
        }
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["policy"]["locked_session"]["prohibit_browser_launch"] = False
        fixture["policy"]["locked_session"]["prohibit_debug_enablement"] = False
        fixture["policy"]["locked_session"]["require_prepared_control"] = False
        fixture["policy"]["locked_session"]["cdp"]["require_prelock_roundtrip"] = False
        fixture["capabilities"] = {"background_safe_browser_setup": "available"}
        fixture["observations"] = {}
        fixture["controller_constraints"] = {
            "requires_browser_launch": True,
            "requires_debug_enablement": True,
        }
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("setup-required", result["state"])
        self.assertTrue(result["permitted_actions"]["background_browser_setup"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_locked_session_does_not_retry_failed_background_setup(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["selected_backend"] = "direct-cdp"
        fixture["background_setup_attempted"] = True
        fixture["browser_instances"][1]["available"] = False
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir",
            "require_existing_when_locked": False,
        }
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["policy"]["locked_session"]["prohibit_browser_launch"] = False
        fixture["policy"]["locked_session"]["prohibit_debug_enablement"] = False
        fixture["policy"]["locked_session"]["require_prepared_control"] = False
        fixture["policy"]["locked_session"]["cdp"]["require_prelock_roundtrip"] = False
        fixture["capabilities"] = {"background_safe_browser_setup": "available"}
        fixture["observations"] = {}
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["background_browser_setup"])
        self.assertIn(
            "background browser setup already attempted without a verified endpoint",
            result["reasons"],
        )

    def test_locked_background_setup_requires_window_activation_to_remain_prohibited(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["selected_backend"] = "direct-cdp"
        fixture["browser_instances"][1]["available"] = False
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir",
            "require_existing_when_locked": False,
        }
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["policy"]["locked_session"]["prohibit_browser_launch"] = False
        fixture["policy"]["locked_session"]["prohibit_debug_enablement"] = False
        fixture["policy"]["locked_session"]["require_prepared_control"] = False
        fixture["policy"]["locked_session"]["prohibit_window_activation"] = False
        fixture["policy"]["locked_session"]["cdp"]["require_prelock_roundtrip"] = False
        fixture["capabilities"] = {"background_safe_browser_setup": "available"}
        fixture["observations"] = {}
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["background_browser_setup"])

    def test_locked_background_setup_rejects_gui_automation(self) -> None:
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
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn("locked-session policy prohibits GUI automation", result["reasons"])

    def test_locked_session_ready_after_background_setup_revalidation(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["selected_backend"] = "direct-cdp"
        fixture["background_setup_attempted"] = True
        fixture["policy"]["execution_profile"] = {
            "mode": "dedicated-user-data-dir",
            "require_existing_when_locked": False,
        }
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["policy"]["locked_session"]["prohibit_browser_launch"] = False
        fixture["policy"]["locked_session"]["prohibit_debug_enablement"] = False
        fixture["policy"]["locked_session"]["require_prepared_control"] = False
        fixture["policy"]["locked_session"]["cdp"]["require_prelock_roundtrip"] = False
        fixture["capabilities"] = {
            "preconnected_browser_control": "available",
            "background_safe_tab_enumeration": "available",
            "background_safe_page_control": "available",
            "cdp_loopback_only": "available",
            "cdp_dedicated_profile": "available",
            "dedicated_profile_identity": "available",
            "loopback_endpoint_ready": "available",
        }
        fixture["observations"] = {}
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertTrue(result["lock_safe_ready"])

    def test_locked_session_without_background_page_control_stops(self) -> None:
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
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "required locked-session capability unavailable: background_safe_page_control",
            result["reasons"],
        )

    def test_locked_session_never_creates_missing_workspace(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "locked"
        fixture["observations"]["groups"] = []
        fixture["capabilities"].update(
            {
                "preconnected_browser_control": "available",
                "background_safe_tab_enumeration": "available",
                "background_safe_page_control": "available",
            }
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "locked session requires an existing configured session and group",
            result["reasons"],
        )
        self.assertFalse(result["permitted_actions"]["create_group"])

    def test_required_lock_safety_with_unknown_screen_state_stops(self) -> None:
        fixture = ready_fixture()
        fixture["screen_session"] = "unknown"
        fixture["lock_safe_required"] = True
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "lock-safe operation requires a known screen-session state", result["reasons"]
        )

    def test_reconnect_rejects_observations_from_stale_browser_id(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"][0]["browser_id"] = "chrome-old"
        fixture["observations"]["groups"][0]["browser_id"] = "chrome-old"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIsNone(result["resolved_session_id"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_tab_group_name_without_stable_group_identity_stops(self) -> None:
        fixture = ready_fixture()
        fixture["capabilities"]["stable_group_identity"] = "unavailable"
        fixture["observations"]["groups"] = [
            {"name": "Shared Workspace", "browser_id": "chrome-new", "source": "tabGroup"}
        ]
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "required capability unavailable: stable_group_identity", result["reasons"]
        )
        self.assertFalse(result["permitted_actions"]["name_session"])
        self.assertFalse(result["permitted_actions"]["create_tab"])

    def test_duplicate_same_name_groups_are_ambiguous_and_stop(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"].append(
            {"group_id": "group-shared-duplicate", "name": "Shared Workspace", "browser_id": "chrome-new"}
        )
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertIn(
            "configured group is not uniquely identified on the selected browser",
            result["reasons"],
        )

    def test_missing_session_enumeration_stops_before_any_browser_action(self) -> None:
        fixture = ready_fixture()
        fixture["capabilities"]["session_enumeration"] = "unknown"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertEqual(
            {
                "background_browser_setup": False,
                "claim_verified_tab": False,
                "name_session": False,
                "create_tab": False,
                "create_session": False,
                "create_group": False,
            },
            result["permitted_actions"],
        )

    def test_missing_session_requires_exact_creation_before_group_resolution(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("creation-required", result["state"])
        self.assertTrue(result["permitted_actions"]["create_session"])
        self.assertFalse(result["permitted_actions"]["create_group"])
        self.assertFalse(result["permitted_actions"]["create_tab"])

    def test_missing_group_requires_exact_creation_then_reenumeration(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("creation-required", result["state"])
        self.assertFalse(result["permitted_actions"]["create_session"])
        self.assertTrue(result["permitted_actions"]["create_group"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_label_only_session_is_ambiguous_not_missing(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"] = [
            {"name": "Shared Workspace", "browser_id": "chrome-new", "source": "sessionLabel"}
        ]
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["create_session"])

    def test_disabled_session_policy_allows_group_only_ready(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["control_session"] = {"enabled": False}
        fixture["capabilities"]["session_enumeration"] = "unavailable"
        fixture["capabilities"]["session_selection"] = "unavailable"
        fixture["capabilities"]["stable_session_identity"] = "unavailable"
        fixture["observations"]["sessions"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertIsNone(result["resolved_session_id"])
        self.assertEqual("group-shared", result["resolved_group_id"])

    def test_disabled_group_policy_allows_session_only_ready(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["tab_grouping"] = {"enabled": False}
        fixture["capabilities"]["group_enumeration"] = "unavailable"
        fixture["capabilities"]["group_selection"] = "unavailable"
        fixture["capabilities"]["stable_group_identity"] = "unavailable"
        fixture["capabilities"]["group_placement"] = "unavailable"
        fixture["observations"]["groups"] = []
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertEqual("session-shared", result["resolved_session_id"])
        self.assertIsNone(result["resolved_group_id"])

    def test_both_workspace_policies_disabled_allow_ordinary_browser_route(self) -> None:
        fixture = ready_fixture()
        fixture["policy"] = {
            "control_session": {"enabled": False},
            "tab_grouping": {"enabled": False},
        }
        fixture["capabilities"] = {}
        fixture["observations"] = {}
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("ready", result["state"])
        self.assertTrue(result["permitted_actions"]["claim_verified_tab"])

    def test_missing_creation_capability_stops_instead_of_creating(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"] = []
        fixture["capabilities"]["group_creation"] = "unknown"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["create_group"])

    def test_session_creation_requires_future_stable_selection(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"] = []
        fixture["capabilities"]["session_selection"] = "unavailable"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["create_session"])

    def test_session_creation_requires_enabled_grouping_to_be_feasible(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"] = []
        fixture["capabilities"]["group_placement"] = "unavailable"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["create_session"])

    def test_group_creation_requires_future_selection_and_placement(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"] = []
        fixture["capabilities"]["group_placement"] = "unknown"
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["create_group"])

    def test_missing_enabled_observation_list_is_invalid_not_absent(self) -> None:
        fixture = ready_fixture()
        fixture["observations"].pop("groups")
        with self.assertRaisesRegex(ValueError, "observations.groups must be a list"):
            PREFLIGHT.evaluate(fixture)

    def test_non_object_group_observation_is_invalid_not_absent(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["groups"] = ["enumeration failed"]
        with self.assertRaisesRegex(ValueError, r"observations.groups\[0\] must be an object"):
            PREFLIGHT.evaluate(fixture)

    def test_incomplete_session_observation_is_invalid_not_absent(self) -> None:
        fixture = ready_fixture()
        fixture["observations"]["sessions"] = [{"name": "Shared Workspace"}]
        with self.assertRaisesRegex(
            ValueError, r"observations.sessions\[0\].browser_id must be a non-empty string"
        ):
            PREFLIGHT.evaluate(fixture)

    def test_conflicting_selected_browser_records_stop(self) -> None:
        fixture = ready_fixture()
        fixture["browser_instances"].append({"browser_id": "chrome-new", "available": False})
        result = PREFLIGHT.evaluate(fixture)
        self.assertEqual("capability-unavailable", result["state"])
        self.assertFalse(result["permitted_actions"]["claim_verified_tab"])

    def test_enabled_must_be_an_explicit_boolean(self) -> None:
        fixture = ready_fixture()
        fixture["policy"]["tab_grouping"]["enabled"] = "false"
        with self.assertRaisesRegex(ValueError, "tab_grouping.enabled must be a boolean"):
            PREFLIGHT.evaluate(fixture)


if __name__ == "__main__":
    unittest.main()
