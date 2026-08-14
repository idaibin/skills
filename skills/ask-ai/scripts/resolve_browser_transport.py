#!/usr/bin/env python3
"""Resolve one provider-specific Ask AI browser transport without external action."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = "ask-ai-transport-resolution/v1"
PROVIDERS = {
    "chatgpt": {"surface": "project", "host": "chatgpt.com"},
    "gemini": {"surface": "notebook", "host": "gemini.google.com"},
}
ALL_TRANSPORTS = {
    "codex-in-app-browser",
    "user-local-browser",
    "chatgpt-app-native",
    "agy-cli",
    "package-only",
}
ROUTE_POLICIES = {"prefer-verified-persistent", "require-verified-persistent"}
ROUTE_FALLBACKS = {"new-standard-chat", "package-only"}
CONVERSATION_POLICIES = {"reuse-verified", "new-per-task"}


def _mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _validate_defaults(defaults: dict[str, Any], errors: list[str]) -> None:
    if defaults.get("schema_version") != "ask-ai-defaults/v1":
        errors.append("schema_version must be ask-ai-defaults/v1")
    routes = _mapping(defaults.get("context_routes"), "context_routes", errors)
    for route_id, value in routes.items():
        if not isinstance(route_id, str) or not route_id.strip():
            errors.append("context route IDs must be non-empty strings")
            continue
        route = _mapping(value, f"context_routes.{route_id}", errors)
        if route.get("policy") not in ROUTE_POLICIES:
            errors.append(f"context_routes.{route_id}.policy is invalid")
        if route.get("fallback") not in ROUTE_FALLBACKS:
            errors.append(f"context_routes.{route_id}.fallback is invalid")
        if route.get("policy") == "require-verified-persistent" and route.get("fallback") != "package-only":
            errors.append(f"context_routes.{route_id} require policy must use package-only fallback")
        if route.get("conversation_policy", "reuse-verified") not in CONVERSATION_POLICIES:
            errors.append(f"context_routes.{route_id}.conversation_policy is invalid")
        targets = route.get("provider_targets")
        if targets is None:
            continue
        targets = _mapping(targets, f"context_routes.{route_id}.provider_targets", errors)
        for provider, target_value in targets.items():
            if provider not in PROVIDERS:
                errors.append(f"context_routes.{route_id} has unknown provider target")
                continue
            target = _mapping(target_value, f"provider_targets.{provider}", errors)
            if target.get("surface") != PROVIDERS[provider]["surface"]:
                errors.append(f"provider_targets.{provider} surface is invalid")
            if not isinstance(target.get("name"), str) or not target["name"].strip():
                errors.append(f"provider_targets.{provider} name is invalid")


def _provider_target(defaults: dict[str, Any], provider: str, route_id: str, errors: list[str]) -> dict[str, str]:
    routes = _mapping(defaults.get("context_routes"), "context_routes", errors)
    route = _mapping(routes.get(route_id), f"context_routes.{route_id}", errors)
    targets_value = route.get("provider_targets")
    if targets_value is None and route_id != "review":
        target = {"surface": PROVIDERS[provider]["surface"], "name": route.get("name")}
    else:
        targets = _mapping(targets_value, f"context_routes.{route_id}.provider_targets", errors)
        target = _mapping(targets.get(provider), f"provider_targets.{provider}", errors)
    expected = PROVIDERS[provider]
    surface = target.get("surface")
    name = target.get("name")
    if surface != expected["surface"]:
        errors.append(f"{provider} provider target must use surface {expected['surface']}")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{provider} provider target requires a non-empty name")
    return {"surface": surface, "name": name.strip() if isinstance(name, str) else ""}


def _verified_target(observations: dict[str, Any], provider: str, target: dict[str, str], errors: list[str]) -> dict[str, Any] | None:
    candidates = observations.get("provider_targets", [])
    if not isinstance(candidates, list) or any(not isinstance(item, dict) for item in candidates):
        errors.append("observations.provider_targets must be a list of objects")
        return None
    matches: list[dict[str, Any]] = []
    for item in candidates:
        if item.get("name") != target["name"] or item.get("surface") != target["surface"]:
            continue
        if item.get("provider") != provider:
            errors.append("provider target evidence belongs to a different provider")
            continue
        stable_id = item.get("stable_id")
        account_id = item.get("account_id")
        url = item.get("url")
        conversation_id = item.get("conversation_id")
        if not all(isinstance(value, str) and value.strip() for value in (stable_id, account_id, url, conversation_id)):
            errors.append("provider target evidence requires stable ID, URL, account, and conversation")
            continue
        parsed_url = urlparse(url)
        host = (parsed_url.hostname or "").lower()
        expected_host = PROVIDERS[provider]["host"]
        try:
            port = parsed_url.port
        except ValueError:
            port = -1
        if (
            parsed_url.scheme != "https"
            or port not in {None, 443}
            or host != expected_host
            or parsed_url.username is not None
            or parsed_url.password is not None
        ):
            errors.append("provider target URL origin does not match selected provider")
            continue
        matches.append(item)
    if len(matches) > 1:
        errors.append("provider target identity is ambiguous")
        return None
    if len(matches) == 1:
        selected = matches[0]
        identity_fields = ("stable_id", "url", "account_id", "conversation_id")
        for item in candidates:
            if item is selected or item.get("provider") == provider:
                continue
            if any(
                isinstance(item.get(field), str)
                and isinstance(selected.get(field), str)
                and item[field].strip().casefold() == selected[field].strip().casefold()
                for field in identity_fields
            ):
                errors.append("provider target stable identity is reused by a different provider")
                return None
        return selected
    return None


def resolve(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    provider = payload.get("provider")
    route_id = payload.get("route_id", "review")
    if not isinstance(provider, str) or provider not in PROVIDERS:
        errors.append("provider must be chatgpt or gemini")
        provider = "invalid"
    if not isinstance(route_id, str) or not route_id.strip():
        errors.append("route_id must be a non-empty string")
        route_id = "invalid"
    defaults = _mapping(payload.get("defaults"), "defaults", errors)
    _validate_defaults(defaults, errors)
    observations = _mapping(payload.get("observations"), "observations", errors)
    current = _mapping(payload.get("current_request", {}), "current_request", errors)
    target = _provider_target(defaults, provider, route_id, errors) if provider in PROVIDERS else {}

    preference = _mapping(defaults.get("browser_preference"), "browser_preference", errors)
    primary = preference.get("primary", "codex-in-app-browser")
    fallback = preference.get("fallback", "package-only")
    if primary not in {"codex-in-app-browser", "user-local-browser", "manual"}:
        errors.append("browser primary is invalid")
        primary = "manual"
    if fallback not in {"codex-in-app-browser", "user-local-browser", "package-only"}:
        errors.append("browser fallback is invalid")
        fallback = "package-only"
    if primary == fallback:
        errors.append("browser primary and fallback must differ")
    local_browser = preference.get("local_browser")
    if "user-local-browser" in {primary, fallback} and not (isinstance(local_browser, str) and local_browser.strip()):
        errors.append("user-local-browser requires a non-empty local_browser product")
    explicit = current.get("transport")
    if explicit is not None and (not isinstance(explicit, str) or explicit not in {"codex-in-app-browser", "user-local-browser", "package-only"}):
        errors.append("explicit transport is invalid")
        explicit = "package-only"
    selected = explicit or primary
    available = _mapping(observations.get("transport_availability", {}), "transport_availability", errors)
    local_allowed = current.get("local_browser_authorized") is True and current.get("requires_local_state") is True
    if selected == "manual":
        selected = "package-only"
    elif selected != "package-only" and available.get(selected) != "available":
        if explicit is not None:
            selected = "package-only"
        elif fallback == "user-local-browser" and local_allowed and available.get(fallback) == "available":
            selected = fallback
        elif fallback == "codex-in-app-browser" and available.get(fallback) == "available":
            selected = fallback
        else:
            selected = "package-only"
    saved_local_primary = explicit is None and primary == "user-local-browser" and selected == primary
    if selected == "user-local-browser" and not (explicit == selected or saved_local_primary or local_allowed):
        errors.append("user-local-browser requires explicit selection or authorized local-state need")

    tabs = observations.get("openTabs", [])
    if not isinstance(tabs, list) or any(not isinstance(item, dict) for item in tabs):
        errors.append("observations.openTabs must be a list of objects")
        tabs = []
    verified = _verified_target(observations, provider, target, errors) if target else None
    if selected not in ALL_TRANSPORTS:
        errors.append("resolved transport is invalid")
        selected = "package-only"
    forbidden = sorted(ALL_TRANSPORTS - {selected})
    if provider == "gemini" and "chatgpt-app-native" not in forbidden:
        forbidden.append("chatgpt-app-native")
    if provider == "gemini" and "agy-cli" not in forbidden:
        forbidden.append("agy-cli")

    status = "blocked" if errors else "ready" if verified or selected == "package-only" else "target-discovery-required"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "provider": provider,
        "route_id": route_id,
        "resolved_target": target,
        "conversation_policy": (
            _mapping(defaults.get("context_routes"), "context_routes", errors)
            .get(route_id, {})
            .get("conversation_policy", "reuse-verified")
        ),
        "selected_transport": selected,
        "forbidden_transports": sorted(set(forbidden)),
        "tab_disposition": (
            "package-only" if selected == "package-only" else
            "open-task-owned-tab" if not tabs else
            "reuse-only-after-provider-target-verification"
        ),
        "verified_target": verified,
        "external_action_allowed": False,
        "call_counts": {"chatgptWorkCloud": 0, "submit": 0, "create_conversation": 0},
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("input must be an object")
        result = resolve(payload)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"schema_version": SCHEMA_VERSION, "status": "invalid-input", "error": str(error)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] in {"ready", "target-discovery-required"} else 20


if __name__ == "__main__":
    raise SystemExit(main())
