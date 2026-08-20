#!/usr/bin/env python3
"""Resolve a user-owned browser route before probing browser surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


CONFIG_SCHEMA = "ops-browser-routes/v1"
REQUEST_SCHEMA = "ops-browser-route-request/v1"
RESULT_SCHEMA = "ops-browser-route-resolution/v1"
SURFACES = {"codex-in-app-browser", "user-local-browser"}
MATCH_FIELDS = {
    "project_roots",
    "origins",
    "hosts",
    "operation_types",
    "keywords",
}
LOOPBACK_ADDRESSES = {"127.0.0.1", "localhost", "::1"}
TARGET_MATCH_ORDERS = {
    "user-local-browser": (
        "profile",
        "account-session",
        "exact-origin",
        "exact-url",
    ),
    "codex-in-app-browser": ("exact-conversation", "exact-url"),
}


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _string_list(value: Any, *, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty string list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a non-empty string list")
    return [item.strip() for item in value]


def _request_string(request: dict[str, Any], field: str) -> str | None:
    value = request.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"request.{field} must be a string when present")
    value = value.strip()
    return value or None


def _url_parts(url: str | None) -> tuple[str | None, str | None]:
    if not url:
        return None, None
    parsed = urlsplit(url)
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("request.url must be an absolute URL")
    host = parsed.hostname.lower()
    port = parsed.port
    default_port = (parsed.scheme == "http" and port == 80) or (
        parsed.scheme == "https" and port == 443
    )
    authority = host if port is None or default_port else f"{host}:{port}"
    return f"{parsed.scheme.lower()}://{authority}", host


def _within_project(cwd: str | None, roots: list[str]) -> bool:
    if not cwd:
        return False
    cwd_path = Path(cwd).expanduser().resolve(strict=False)
    for root in roots:
        root_path = Path(root).expanduser()
        if not root_path.is_absolute():
            raise ValueError("project_roots entries must be absolute paths")
        root_path = root_path.resolve(strict=False)
        if cwd_path == root_path or root_path in cwd_path.parents:
            return True
    return False


def _matches_clause(
    clause: dict[str, Any], request: dict[str, Any]
) -> tuple[bool, list[str]]:
    unknown = set(clause) - MATCH_FIELDS
    if unknown:
        raise ValueError(f"unsupported match fields: {sorted(unknown)}")
    if not clause:
        raise ValueError("match clauses must not be empty")

    cwd = _request_string(request, "cwd")
    url = _request_string(request, "url")
    operation_type = _request_string(request, "operation_type")
    text = _request_string(request, "text")
    origin, host = _url_parts(url)
    matched_fields: list[str] = []

    for field, raw_values in clause.items():
        values = _string_list(raw_values, field=f"match.{field}")
        if field == "project_roots":
            matched = _within_project(cwd, values)
        elif field == "origins":
            normalized = {value.rstrip("/").lower() for value in values}
            matched = origin is not None and origin.lower() in normalized
        elif field == "hosts":
            normalized = {value.lower().lstrip(".") for value in values}
            matched = host is not None and any(
                host == value or host.endswith(f".{value}") for value in normalized
            )
        elif field == "operation_types":
            normalized = {value.casefold() for value in values}
            matched = operation_type is not None and operation_type.casefold() in normalized
        else:
            lowered = text.casefold() if text else ""
            matched = bool(lowered) and any(value.casefold() in lowered for value in values)
        if not matched:
            return False, []
        matched_fields.append(field)

    return True, matched_fields


def _validate_route(route: Any) -> dict[str, Any]:
    if not isinstance(route, dict):
        raise ValueError("rule.route must be an object")
    surface = route.get("surface")
    if surface not in SURFACES:
        raise ValueError(f"rule.route.surface must be one of {sorted(SURFACES)}")
    if route.get("skip_default_surface_probe") is not True:
        raise ValueError("rule.route.skip_default_surface_probe must be true")
    if not isinstance(route.get("reuse_existing"), bool):
        raise ValueError("rule.route.reuse_existing must be a boolean")
    order = _string_list(
        route.get("target_match_order"), field="rule.route.target_match_order"
    )
    expected_order = TARGET_MATCH_ORDERS[surface]
    if tuple(order) != expected_order:
        raise ValueError(
            "rule.route.target_match_order must be "
            f"{list(expected_order)} for {surface}"
        )

    cdp = route.get("cdp")
    if surface == "user-local-browser":
        for field in ("browser_product", "execution_profile", "workspace"):
            if not isinstance(route.get(field), str) or not route[field].strip():
                raise ValueError(f"rule.route.{field} is required for user-local-browser")
        if not isinstance(cdp, dict):
            raise ValueError("rule.route.cdp is required for user-local-browser")
        if cdp.get("address") not in LOOPBACK_ADDRESSES:
            raise ValueError("rule.route.cdp.address must be loopback-only")
        port = cdp.get("port")
        if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            raise ValueError("rule.route.cdp.port must be an integer from 1 to 65535")
    elif any(
        field in route
        for field in ("browser_product", "execution_profile", "workspace", "cdp")
    ):
        raise ValueError(
            "codex-in-app-browser routes must not declare local profile or CDP fields"
        )
    return route


def resolve(config: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    if config.get("schema_version") != CONFIG_SCHEMA:
        raise ValueError("unsupported route config schema_version")
    if request.get("schema_version") != REQUEST_SCHEMA:
        raise ValueError("unsupported route request schema_version")
    if config.get("fallback") != "defaults":
        raise ValueError("route config fallback must be defaults")
    rules = config.get("rules")
    if not isinstance(rules, list):
        raise ValueError("route config rules must be a list")

    candidates: list[tuple[int, int, str, dict[str, Any], int, list[str]]] = []
    seen_ids: set[str] = set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"rules[{index}] must be an object")
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise ValueError(f"rules[{index}].id must be a non-empty string")
        if rule_id in seen_ids:
            raise ValueError(f"duplicate route rule id: {rule_id}")
        seen_ids.add(rule_id)
        enabled = rule.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ValueError(f"rules[{index}].enabled must be a boolean")
        if not enabled:
            continue
        priority = rule.get("priority")
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise ValueError(f"rules[{index}].priority must be an integer")
        match = rule.get("match")
        if not isinstance(match, dict) or set(match) != {"any"}:
            raise ValueError(f"rules[{index}].match must contain only any")
        clauses = match["any"]
        if not isinstance(clauses, list) or not clauses:
            raise ValueError(f"rules[{index}].match.any must be a non-empty list")
        route = _validate_route(rule.get("route"))
        for clause_index, clause in enumerate(clauses):
            if not isinstance(clause, dict):
                raise ValueError(
                    f"rules[{index}].match.any[{clause_index}] must be an object"
                )
            matched, fields = _matches_clause(clause, request)
            if matched:
                candidates.append(
                    (priority, index, rule_id, route, clause_index, fields)
                )
                break

    if not candidates:
        return {
            "schema_version": RESULT_SCHEMA,
            "state": "no-match",
            "fallback": "defaults",
        }

    priority, _, rule_id, route, clause_index, fields = sorted(
        candidates, key=lambda item: (-item[0], item[1])
    )[0]
    return {
        "schema_version": RESULT_SCHEMA,
        "state": "matched",
        "rule_id": rule_id,
        "priority": priority,
        "matched_clause": clause_index,
        "matched_fields": fields,
        "surface": route["surface"],
        "route": route,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("request", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = resolve(_read_json(args.config), _read_json(args.request))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(
            json.dumps(
                {
                    "schema_version": RESULT_SCHEMA,
                    "state": "invalid",
                    "error": str(error),
                },
                ensure_ascii=False,
            )
        )
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=args.pretty,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
