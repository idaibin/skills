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
                    "browser_product": "Google Chrome",
                    "execution_profile": "extension-connected-current",
                    "workspace": "AI_Dev",
                    "connector": "plugin://chrome@openai-bundled",
                    "browser_selector": "chrome",
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
    def test_origin_default_ports_preserve_exact_origin_boundaries(self) -> None:
        cases = (
            ("https://example.test:443", "https://example.test/page", True),
            ("https://example.test:443", "https://example.test:443/page", True),
            ("http://example.test:80", "http://example.test/page", True),
            ("http://example.test:80", "http://example.test:80/page", True),
            ("https://example.test", "https://example.test:443/page", True),
            ("http://example.test", "http://example.test:80/page", True),
            ("https://example.test:8443", "https://example.test:8443/page", True),
            ("https://example.test:8443", "https://example.test/page", False),
            ("https://example.test", "https://example.test:8443/page", False),
            ("http://example.test", "https://example.test/page", False),
            ("https://example.test", "https://sub.example.test/page", False),
            ("https://example.test", "https://notexample.test/page", False),
            ("https://user:pass@localhost", "https://localhost/page", False),
            ("https://example.test/path", "https://example.test/path", False),
            ("https://example.test?x=1", "https://example.test/page", False),
            ("https://example.test#fragment", "https://example.test/page", False),
            ("HTTPS://EXAMPLE.TEST/", "https://example.test/page", True),
            ("https://example.test", "https://other.test/page", False),
            ("https://user:pass@localhost:443", "https://localhost/page", False),
            ("https://example.test:443/path", "https://example.test/page", False),
            ("https://example.test/path:443", "https://example.test/page", False),
            ("https://example.test:443?x=1", "https://example.test/page", False),
            ("https://example.test:443#x", "https://example.test/page", False),
            ("https://example.test:443?", "https://example.test/page", False),
            ("https://example.test:443#", "https://example.test/page", False),
            ("http://example.test:443", "http://example.test/page", False),
            ("https://example.test:80", "https://example.test/page", False),
            ("https://example.test:443/", "https://example.test/page", True),
        )
        for origin, url, matched in cases:
            with self.subTest(origin=origin, url=url):
                config = route_config()
                config["rules"] = config["rules"][:1]
                rule = config["rules"][0]
                rule["match"] = {"any": [{"origins": [origin]}]}
                expected = {"schema_version": "ops-browser-route-resolution/v1"}
                if matched:
                    expected.update(
                        state="matched", rule_id=rule["id"], priority=rule["priority"],
                        matched_clause=0, matched_fields=["origins"],
                        surface="user-local-browser", route=rule["route"],
                    )
                else:
                    expected.update(state="no-match", fallback="defaults")
                self.assertEqual(expected, RESOLVER.resolve(config, request(url=url)))

    def test_origin_normalization_preserves_rule_and_clause_precedence(self) -> None:
        for case in ("priority", "tie", "any", "and-match", "and-miss"):
            with self.subTest(case=case):
                config = route_config()
                first, second = config["rules"]
                first["match"] = {"any": [{"origins": ["https://example.test:443"]}]}
                second["match"] = {"any": [{"origins": ["https://example.test"]}]}
                winner, clause, fields = first, 0, ["origins"]
                if case in {"priority", "tie"}:
                    second["priority"] = 101 if case == "priority" else 100
                    if case == "priority":
                        winner = second
                else:
                    config["rules"] = [first]
                    if case == "any":
                        first["match"]["any"].insert(0, {"origins": ["https://other.test"]})
                        clause = 1
                    else:
                        first["match"]["any"][0]["keywords"] = ["accepted"]
                        fields = ["origins", "keywords"]
                expected = {"schema_version": "ops-browser-route-resolution/v1"}
                if case == "and-miss":
                    expected.update(state="no-match", fallback="defaults")
                else:
                    expected.update(
                        state="matched", rule_id=winner["id"], priority=winner["priority"],
                        matched_clause=clause, matched_fields=fields,
                        surface=winner["route"]["surface"], route=winner["route"],
                    )
                supplied = request(url="https://example.test/page", text="absent" if case == "and-miss" else "accepted")
                self.assertEqual(expected, RESOLVER.resolve(config, supplied))

    def test_portal_origin_goes_directly_to_chrome_extension(self) -> None:
        result = RESOLVER.resolve(
            route_config(), request(url="http://portal.example.test/manage")
        )
        self.assertEqual("matched", result["state"])
        self.assertEqual("portal-ai-dev", result["rule_id"])
        self.assertEqual("user-local-browser", result["surface"])
        self.assertEqual("chrome", result["route"]["browser_selector"])
        self.assertEqual(
            "plugin://chrome@openai-bundled", result["route"]["connector"]
        )
        self.assertTrue(result["route"]["skip_default_surface_probe"])
        self.assertEqual(
            "extension-connected-current", result["route"]["execution_profile"]
        )

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

    def test_local_route_rejects_non_chrome_connector(self) -> None:
        config = route_config()
        config["rules"][0]["route"]["connector"] = "plugin://browser@example"
        with self.assertRaisesRegex(ValueError, "Chrome plugin"):
            RESOLVER.resolve(config, request(url="http://portal.example.test"))

    def test_local_route_rejects_unsupported_cdp_field(self) -> None:
        config = route_config()
        config["rules"][0]["route"]["cdp"] = {
            "address": "127.0.0.1",
            "port": 9000,
        }
        with self.assertRaisesRegex(ValueError, "cdp is unsupported"):
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
