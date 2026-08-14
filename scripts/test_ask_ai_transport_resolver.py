#!/usr/bin/env python3
"""Offline regressions for provider-specific Ask AI browser transport resolution."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ask-ai" / "scripts" / "resolve_browser_transport.py"
SPEC = importlib.util.spec_from_file_location("resolve_browser_transport", SCRIPT)
assert SPEC and SPEC.loader
RESOLVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RESOLVER)


def payload(provider: str, *, targets=None, tabs=None) -> dict:
    return {
        "provider": provider,
        "route_id": "review",
        "defaults": {
            "schema_version": "ask-ai-defaults/v1",
            "browser_preference": {
                "primary": "codex-in-app-browser",
                "local_browser": "Google Chrome",
                "fallback": "user-local-browser",
            },
            "context_routes": {
                "review": {
                    "name": "generic route name must not win",
                    "policy": "require-verified-persistent",
                    "fallback": "package-only",
                    "conversation_policy": "new-per-task",
                    "provider_targets": {
                        "chatgpt": {"surface": "project", "name": "Configured Review"},
                        "gemini": {"surface": "notebook", "name": "Configured Review"},
                    },
                }
            },
        },
        "current_request": {"local_browser_authorized": False, "requires_local_state": False},
        "observations": {
            "transport_availability": {"codex-in-app-browser": "available"},
            "openTabs": [] if tabs is None else tabs,
            "provider_targets": [] if targets is None else targets,
        },
    }


def target(provider: str) -> dict:
    if provider == "chatgpt":
        return {"provider": "chatgpt", "surface": "project", "name": "Configured Review", "stable_id": "chatgpt-project-1", "url": "https://chatgpt.com/g/g-p-1", "account_id": "acct-chatgpt", "conversation_id": "conv-chatgpt"}
    return {"provider": "gemini", "surface": "notebook", "name": "Configured Review", "stable_id": "gemini-notebook-1", "url": "https://gemini.google.com/app/notebook-1", "account_id": "acct-gemini", "conversation_id": "conv-gemini"}


class AskAiTransportResolverTests(unittest.TestCase):
    def test_chatgpt_project_and_gemini_notebook_same_name_resolve_independently(self) -> None:
        chatgpt = RESOLVER.resolve(payload("chatgpt", targets=[target("chatgpt")]))
        gemini = RESOLVER.resolve(payload("gemini", targets=[target("gemini")]))
        self.assertEqual("ready", chatgpt["status"])
        self.assertEqual("project", chatgpt["resolved_target"]["surface"])
        self.assertEqual("notebook", gemini["resolved_target"]["surface"])
        self.assertNotEqual(chatgpt["verified_target"]["stable_id"], gemini["verified_target"]["stable_id"])

    def test_empty_tabs_keeps_codex_iab_and_never_calls_native(self) -> None:
        result = RESOLVER.resolve(payload("chatgpt"))
        self.assertEqual("codex-in-app-browser", result["selected_transport"])
        self.assertEqual("open-task-owned-tab", result["tab_disposition"])
        self.assertEqual(0, result["call_counts"]["chatgptWorkCloud"])
        self.assertEqual("target-discovery-required", result["status"])

    def test_provider_target_overrides_generic_route_name(self) -> None:
        result = RESOLVER.resolve(payload("chatgpt", targets=[target("chatgpt")]))
        self.assertEqual("Configured Review", result["resolved_target"]["name"])
        self.assertEqual("new-per-task", result["conversation_policy"])

    def test_cross_provider_identity_reuse_fails_closed(self) -> None:
        copied = target("gemini") | {"provider": "chatgpt", "stable_id": "chatgpt-project-1"}
        result = RESOLVER.resolve(payload("gemini", targets=[copied]))
        self.assertEqual("blocked", result["status"])
        self.assertIn("provider target evidence belongs to a different provider", result["errors"])

    def test_cross_provider_url_reuse_fails_closed(self) -> None:
        wrong = target("gemini") | {"url": "https://chatgpt.com/g/copied"}
        result = RESOLVER.resolve(payload("gemini", targets=[wrong]))
        self.assertEqual("blocked", result["status"])
        self.assertIn("provider target URL origin does not match selected provider", result["errors"])

    def test_same_stable_identity_across_provider_observations_fails_closed(self) -> None:
        gemini = target("gemini")
        copied = target("chatgpt") | {"stable_id": gemini["stable_id"]}
        result = RESOLVER.resolve(payload("gemini", targets=[gemini, copied]))
        self.assertEqual("blocked", result["status"])
        self.assertIn("provider target stable identity is reused by a different provider", result["errors"])

    def test_same_account_across_provider_observations_fails_closed(self) -> None:
        gemini = target("gemini")
        copied = target("chatgpt") | {"account_id": gemini["account_id"]}
        result = RESOLVER.resolve(payload("gemini", targets=[gemini, copied]))
        self.assertEqual("blocked", result["status"])
        self.assertIn("provider target stable identity is reused by a different provider", result["errors"])

    def test_gemini_forbids_chatgpt_native_and_agy(self) -> None:
        result = RESOLVER.resolve(payload("gemini", targets=[target("gemini")]))
        self.assertIn("chatgpt-app-native", result["forbidden_transports"])
        self.assertIn("agy-cli", result["forbidden_transports"])

    def test_chrome_fallback_requires_both_authorization_and_local_need(self) -> None:
        value = payload("chatgpt")
        value["observations"]["transport_availability"] = {
            "codex-in-app-browser": "unavailable", "user-local-browser": "available"
        }
        result = RESOLVER.resolve(value)
        self.assertEqual("package-only", result["selected_transport"])
        value["current_request"] = {"local_browser_authorized": True, "requires_local_state": True}
        result = RESOLVER.resolve(value)
        self.assertEqual("user-local-browser", result["selected_transport"])

    def test_explicit_iab_never_falls_back_to_chrome(self) -> None:
        value = payload("chatgpt")
        value["current_request"] = {
            "transport": "codex-in-app-browser",
            "local_browser_authorized": True,
            "requires_local_state": True,
        }
        value["observations"]["transport_availability"] = {
            "codex-in-app-browser": "unavailable", "user-local-browser": "available"
        }
        result = RESOLVER.resolve(value)
        self.assertEqual("package-only", result["selected_transport"])

    def test_saved_local_primary_can_fall_back_to_iab(self) -> None:
        value = payload("chatgpt")
        value["defaults"]["browser_preference"] = {
            "primary": "user-local-browser", "local_browser": "Example Browser",
            "fallback": "codex-in-app-browser",
        }
        value["current_request"] = {"local_browser_authorized": True, "requires_local_state": True}
        value["observations"]["transport_availability"] = {
            "user-local-browser": "unavailable", "codex-in-app-browser": "available"
        }
        self.assertEqual("codex-in-app-browser", RESOLVER.resolve(value)["selected_transport"])

    def test_saved_local_primary_available_needs_no_fallback_flags(self) -> None:
        value = payload("chatgpt")
        value["defaults"]["browser_preference"] = {
            "primary": "user-local-browser", "local_browser": "Example Browser",
            "fallback": "package-only",
        }
        value["current_request"] = {}
        value["observations"]["transport_availability"] = {"user-local-browser": "available"}
        result = RESOLVER.resolve(value)
        self.assertEqual("user-local-browser", result["selected_transport"])
        self.assertNotEqual("blocked", result["status"])

    def test_invalid_fallback_and_missing_local_product_block(self) -> None:
        value = payload("chatgpt")
        value["defaults"]["browser_preference"] = {
            "primary": "codex-in-app-browser", "fallback": "bogus"
        }
        self.assertEqual("blocked", RESOLVER.resolve(value)["status"])

    def test_invalid_defaults_schema_route_and_other_provider_target_block(self) -> None:
        mutations = []
        value = payload("chatgpt"); value["defaults"]["schema_version"] = "unknown"; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["policy"] = "bad"; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["fallback"] = "bad"; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["fallback"] = "new-standard-chat"; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["conversation_policy"] = "bad"; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["provider_targets"]["other"] = {"surface": "project", "name": "x"}; mutations.append(value)
        value = payload("chatgpt"); value["defaults"]["context_routes"]["review"]["provider_targets"]["gemini"]["surface"] = "project"; mutations.append(value)
        for item in mutations:
            with self.subTest(item=item):
                self.assertEqual("blocked", RESOLVER.resolve(item)["status"])
        value["defaults"]["browser_preference"] = {
            "primary": "user-local-browser", "fallback": "package-only"
        }
        self.assertEqual("blocked", RESOLVER.resolve(value)["status"])

    def test_invalid_explicit_transport_is_never_selected(self) -> None:
        value = payload("gemini")
        value["current_request"]["transport"] = "agy-cli"
        result = RESOLVER.resolve(value)
        self.assertEqual("blocked", result["status"])
        self.assertEqual("package-only", result["selected_transport"])
        self.assertNotIn(result["selected_transport"], result["forbidden_transports"])

    def test_review_requires_provider_targets_but_other_route_can_use_generic_name(self) -> None:
        value = payload("chatgpt")
        del value["defaults"]["context_routes"]["review"]["provider_targets"]
        self.assertEqual("blocked", RESOLVER.resolve(value)["status"])
        value["route_id"] = "design"
        value["defaults"]["context_routes"]["design"] = {
            "name": "Configured Design", "policy": "require-verified-persistent",
            "fallback": "package-only",
        }
        result = RESOLVER.resolve(value)
        self.assertEqual("Configured Design", result["resolved_target"]["name"])

    def test_unhashable_provider_route_and_transport_fail_closed(self) -> None:
        value = payload("chatgpt")
        value["provider"] = []
        value["route_id"] = {}
        value["current_request"]["transport"] = []
        result = RESOLVER.resolve(value)
        self.assertEqual("blocked", result["status"])
        self.assertEqual("package-only", result["selected_transport"])

    def test_noncanonical_origins_and_whitespace_identity_reuse_fail(self) -> None:
        for url in (
            "http://chatgpt.com/g/x", "https://chatgpt.com:444/g/x",
            "https://@chatgpt.com/g/x", "https://sub.chatgpt.com/g/x",
        ):
            wrong = target("chatgpt") | {"url": url}
            with self.subTest(url=url):
                self.assertEqual("blocked", RESOLVER.resolve(payload("chatgpt", targets=[wrong]))["status"])
        gemini = target("gemini")
        copied = target("chatgpt") | {"account_id": f" {gemini['account_id']} "}
        self.assertEqual("blocked", RESOLVER.resolve(payload("gemini", targets=[gemini, copied]))["status"])

    def test_json_cli_exit_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.json"
            path.write_text(json.dumps(payload("chatgpt")), encoding="utf-8")
            completed = subprocess.run(["python3", str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(0, completed.returncode)
            self.assertEqual(RESOLVER.SCHEMA_VERSION, json.loads(completed.stdout)["schema_version"])
            path.write_text("{broken", encoding="utf-8")
            completed = subprocess.run(["python3", str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(2, completed.returncode)
            self.assertEqual("invalid-input", json.loads(completed.stdout)["status"])
            blocked = payload("chatgpt"); blocked["defaults"]["schema_version"] = "bad"
            path.write_text(json.dumps(blocked), encoding="utf-8")
            completed = subprocess.run(["python3", str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(20, completed.returncode)
            self.assertEqual("blocked", json.loads(completed.stdout)["status"])


if __name__ == "__main__":
    unittest.main()
