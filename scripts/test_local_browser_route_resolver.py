#!/usr/bin/env python3
"""Regression tests for deterministic local browser route selection."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ops-browser" / "scripts" / "resolve-local-browser-route.py"
SPEC = importlib.util.spec_from_file_location("local_browser_route_resolver", SCRIPT)
assert SPEC and SPEC.loader
RESOLVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RESOLVER)


def route_config() -> dict:
    return {
        "schema_version": "ops-browser-routes/v1",
        "fallback": "defaults",
        "rules": [
            {
                "id": "portal-ai-dev",
                "enabled": True,
                "priority": 100,
                "match": {
                    "any": [
                        {"origins": ["http://portal.example.test"]},
                        {
                            "project_roots": ["/workspace/portal"],
                            "keywords": ["门户"],
                        },
                    ]
                },
                "route": {
                    "surface": "user-local-browser",
                    "browser_product": "Google Chrome Beta",
                    "execution_profile": "AI-Exec",
                    "workspace": "AI_dev",
                    "cdp": {"address": "127.0.0.1", "port": 9224},
                    "reuse_existing": True,
                    "target_match_order": [
                        "profile",
                        "account-session",
                        "exact-origin",
                        "exact-url",
                    ],
                    "skip_default_surface_probe": True,
                },
            },
            {
                "id": "chatgpt-web-review",
                "enabled": True,
                "priority": 90,
                "match": {
                    "any": [
                        {"operation_types": ["chatgpt-web-chat-review"]},
                        {"hosts": ["chatgpt.com"], "keywords": ["review", "审查"]},
                    ]
                },
                "route": {
                    "surface": "codex-in-app-browser",
                    "reuse_existing": True,
                    "target_match_order": ["exact-conversation", "exact-url"],
                    "skip_default_surface_probe": True,
                },
            },
        ],
    }


def request(**overrides: str) -> dict:
    value = {"schema_version": "ops-browser-route-request/v1"}
    value.update(overrides)
    return value


class LocalBrowserRouteResolverTests(unittest.TestCase):
    def test_portal_origin_goes_directly_to_local_cdp(self) -> None:
        result = RESOLVER.resolve(
            route_config(), request(url="http://portal.example.test/manage")
        )
        self.assertEqual("matched", result["state"])
        self.assertEqual("portal-ai-dev", result["rule_id"])
        self.assertEqual("user-local-browser", result["surface"])
        self.assertEqual(9224, result["route"]["cdp"]["port"])
        self.assertTrue(result["route"]["skip_default_surface_probe"])

    def test_project_and_keyword_clause_requires_both(self) -> None:
        matched = RESOLVER.resolve(
            route_config(),
            request(cwd="/workspace/portal/app", text="验证门户管理端"),
        )
        missed = RESOLVER.resolve(
            route_config(), request(cwd="/workspace/other", text="验证门户管理端")
        )
        self.assertEqual("portal-ai-dev", matched["rule_id"])
        self.assertEqual("no-match", missed["state"])

    def test_chatgpt_web_review_uses_in_app_browser(self) -> None:
        result = RESOLVER.resolve(
            route_config(), request(operation_type="chatgpt-web-chat-review")
        )
        self.assertEqual("chatgpt-web-review", result["rule_id"])
        self.assertEqual("codex-in-app-browser", result["surface"])

    def test_higher_priority_rule_wins(self) -> None:
        config = route_config()
        config["rules"][1]["priority"] = 101
        result = RESOLVER.resolve(
            config,
            request(
                url="http://portal.example.test/manage",
                operation_type="chatgpt-web-chat-review",
            ),
        )
        self.assertEqual("chatgpt-web-review", result["rule_id"])

    def test_explicit_request_text_outranks_project_root(self) -> None:
        config = route_config()
        config["rules"][1]["priority"] = 200
        config["rules"][1]["match"]["any"].append({"keywords": ["ChatGPT 审查"]})
        result = RESOLVER.resolve(
            config,
            request(cwd="/workspace/portal/app", text="请执行 ChatGPT 审查"),
        )
        self.assertEqual("chatgpt-web-review", result["rule_id"])
        self.assertEqual(["keywords"], result["matched_fields"])

    def test_disabled_matching_rule_is_ignored(self) -> None:
        config = route_config()
        config["rules"][1]["enabled"] = False
        result = RESOLVER.resolve(
            config, request(operation_type="chatgpt-web-chat-review")
        )
        self.assertEqual("no-match", result["state"])

    def test_enabled_must_be_boolean(self) -> None:
        config = route_config()
        config["rules"][0]["enabled"] = "false"
        with self.assertRaisesRegex(ValueError, "enabled must be a boolean"):
            RESOLVER.resolve(config, request(url="http://portal.example.test"))

    def test_unmatched_request_uses_defaults(self) -> None:
        result = RESOLVER.resolve(
            route_config(), request(url="https://example.org/docs")
        )
        self.assertEqual("no-match", result["state"])
        self.assertEqual("defaults", result["fallback"])

    def test_local_route_rejects_non_loopback_cdp(self) -> None:
        config = route_config()
        config["rules"][0]["route"]["cdp"]["address"] = "192.0.2.10"
        with self.assertRaisesRegex(ValueError, "loopback-only"):
            RESOLVER.resolve(config, request(url="http://portal.example.test"))

    def test_target_match_order_rejects_unknown_or_missing_boundaries(self) -> None:
        config = route_config()
        config["rules"][0]["route"]["target_match_order"] = [
            "profile",
            "exact-url",
        ]
        with self.assertRaisesRegex(ValueError, "target_match_order must be"):
            RESOLVER.resolve(config, request(url="http://portal.example.test"))


if __name__ == "__main__":
    unittest.main()
