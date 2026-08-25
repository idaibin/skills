#!/usr/bin/env python3
"""Validate portable live-Agent case definitions and captured result records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_provider_evidence import verify_provider_evidence

CASE_SCHEMA_VERSION = "skill-live-agent-cases/v1"
RESULT_SCHEMA_VERSION = "skill-live-agent-results/v1"
RESULT_STATES = {"passed", "failed", "blocked", "not-verified"}
CASE_MODES = {"explicit", "implicit"}
STOP_STATES = {"completed", "evidence-incomplete", "missing-authorization"}
OBSERVATIONS = {
    "skill-selection", "source-owner", "process", "artifact", "effect",
    "stop-honesty", "efficiency", "provider",
}


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be an object")
    return value


def strings(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def portable_relative_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and not value.startswith(("/", "\\"))
        and ".." not in value.split("/")
        and "\\" not in value
    )


def case_errors(cases: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if cases.get("schema_version") != CASE_SCHEMA_VERSION:
        errors.append("invalid live-agent case schema version")
    if cases.get("fixture_root") != "evals/fixtures/live-agent-dev-frontend":
        errors.append("live-agent cases must use the synthetic fixture root")
    entries = cases.get("cases")
    if not isinstance(entries, list) or not entries:
        return errors + ["live-agent cases must be a non-empty array"]
    modes = set()
    expected_ids = {
        "dev-frontend-explicit-source-change",
        "dev-frontend-implicit-source-change",
        "dev-frontend-nearest-negative",
        "dev-frontend-valid-no-op",
        "dev-frontend-critical-stop",
        "dev-frontend-independent-provider",
    }
    actual_ids = set()
    for case in entries:
        if not isinstance(case, dict):
            errors.append("each live-agent case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"dev-frontend-[a-z0-9-]+", case_id):
            errors.append("live-agent case IDs must use the neutral dev-frontend namespace")
            continue
        actual_ids.add(case_id)
        mode = case.get("mode")
        if mode not in CASE_MODES:
            errors.append(f"{case_id}: mode must be explicit or implicit")
        else:
            modes.add(mode)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{case_id}: prompt is required")
        if not isinstance(case.get("expected_skill"), str):
            errors.append(f"{case_id}: expected_skill is required")
        for key in ("excluded_skills", "required_observations", "required_process", "required_source_owners", "allowed_changed_paths", "required_changed_paths", "required_effects", "forbidden_effects", "required_artifacts"):
            if not strings(case.get(key)):
                errors.append(f"{case_id}: {key} must be a string array")
        observations = case.get("required_observations", [])
        if isinstance(observations, list) and not set(observations).issubset(OBSERVATIONS):
            errors.append(f"{case_id}: unknown required observation")
        if case.get("expected_stop") not in STOP_STATES:
            errors.append(f"{case_id}: invalid expected stop")
        if not isinstance(case.get("max_tool_calls"), int) or case["max_tool_calls"] < 1:
            errors.append(f"{case_id}: max_tool_calls must be positive")
        for owner in case.get("required_source_owners", []):
            path, separator, symbol = owner.partition(":") if isinstance(owner, str) else ("", "", "")
            if not separator or not symbol or not portable_relative_path(path):
                errors.append(f"{case_id}: source owner must be a relative path and symbol")
        for path in case.get("allowed_changed_paths", []) + case.get("required_changed_paths", []):
            if not portable_relative_path(path):
                errors.append(f"{case_id}: changed path must be portable and relative")
        if isinstance(case.get("required_changed_paths"), list) and isinstance(case.get("allowed_changed_paths"), list) and not set(case["required_changed_paths"]).issubset(case["allowed_changed_paths"]):
            errors.append(f"{case_id}: required changed paths must be allowed")
        provider = case.get("required_provider")
        if provider is not None and (
            not isinstance(provider, dict)
            or provider.get("channel") != "AGY"
            or provider.get("model") != "Flash"
        ):
            errors.append(f"{case_id}: independent provider must be AGY Flash")
    if actual_ids != expected_ids:
        errors.append("live-agent cases must keep the fixed explicit/implicit/negative/no-op/stop/provider set")
    if modes != CASE_MODES:
        errors.append("live-agent cases must cover explicit and implicit invocation")
    return errors


def result_errors(cases: dict[str, object], results: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if results.get("schema_version") != RESULT_SCHEMA_VERSION:
        return ["invalid live-agent result schema version"]
    entries = results.get("case_results")
    if not isinstance(entries, list):
        return ["live-agent results must include case_results"]
    cases_by_id = {case["id"]: case for case in cases["cases"] if isinstance(case, dict)}
    selected_case_ids = results.get("selected_case_ids")
    if selected_case_ids is None:
        expected_case_ids = set(cases_by_id)
    elif strings(selected_case_ids) and selected_case_ids:
        expected_case_ids = set(selected_case_ids)
        if not expected_case_ids.issubset(cases_by_id):
            errors.append("live-agent results select an unknown case")
    else:
        errors.append("selected_case_ids must be a non-empty string array when present")
        expected_case_ids = set()
    seen: set[str] = set()
    for result in entries:
        if not isinstance(result, dict):
            errors.append("each live-agent result must be an object")
            continue
        case_id = result.get("case_id")
        case = cases_by_id.get(case_id)
        if case is None or case_id in seen:
            errors.append("live-agent result must identify one unique declared case")
            continue
        seen.add(case_id)
        status = result.get("status")
        if status not in RESULT_STATES:
            errors.append(f"{case_id}: invalid result status")
            continue
        if status != "passed":
            continue
        if result.get("selected_skill") != case["expected_skill"]:
            errors.append(f"{case_id}: selected skill does not match the case")
        for key in ("observations", "process", "source_owners", "artifacts", "effects"):
            if not strings(result.get(key)):
                errors.append(f"{case_id}: passed result needs {key}")
        if isinstance(result.get("observations"), list) and not set(case["required_observations"]).issubset(result["observations"]):
            errors.append(f"{case_id}: missing required observation")
        if isinstance(result.get("process"), list) and not set(case["required_process"]).issubset(result["process"]):
            errors.append(f"{case_id}: missing required process step")
        if isinstance(result.get("source_owners"), list) and not set(case["required_source_owners"]).issubset(result["source_owners"]):
            errors.append(f"{case_id}: missing required source owner")
        if isinstance(result.get("artifacts"), list) and not set(case["required_artifacts"]).issubset(result["artifacts"]):
            errors.append(f"{case_id}: missing required artifact")
        effects = result.get("effects", [])
        if isinstance(effects, list):
            if not set(case["required_effects"]).issubset(effects):
                errors.append(f"{case_id}: missing required effect")
            if set(case["forbidden_effects"]) & set(effects):
                errors.append(f"{case_id}: contains forbidden effect")
        stop = result.get("stop")
        if not isinstance(stop, dict) or stop.get("state") != case["expected_stop"]:
            errors.append(f"{case_id}: stop state is not honest")
        efficiency = result.get("efficiency")
        if not isinstance(efficiency, dict) or not isinstance(efficiency.get("tool_calls"), int) or not isinstance(efficiency.get("successful_tool_calls"), int):
            errors.append(f"{case_id}: missing efficiency evidence")
        elif efficiency["tool_calls"] > case["max_tool_calls"]:
            errors.append(f"{case_id}: tool-call budget exceeded")
        elif efficiency["successful_tool_calls"] > efficiency["tool_calls"]:
            errors.append(f"{case_id}: successful tool-call count exceeds total")
        provider_requirement = case.get("required_provider")
        if provider_requirement is not None:
            provider = result.get("provider")
            trace = result.get("trace")
            expected_diff_hash = trace.get("source_diff_sha256") if isinstance(trace, dict) else None
            selected_repository_root = trace.get("selected_repository_root") if isinstance(trace, dict) else None
            if (
                not isinstance(provider, dict)
                or not isinstance(expected_diff_hash, str)
                or not re.fullmatch(r"[0-9a-f]{64}", expected_diff_hash)
                or not isinstance(selected_repository_root, str)
                or verify_provider_evidence(
                    provider,
                    case_id=case_id,
                    source_diff_sha256=expected_diff_hash,
                    selected_repository_root=selected_repository_root,
                )[0] is None
            ):
                errors.append(f"{case_id}: requested independent provider is not verified")
    if seen != expected_case_ids:
        errors.append("live-agent results must record every selected case; missing cases are not verified")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate portable live-Agent evaluation cases and results.")
    parser.add_argument("--cases", type=Path, default=ROOT / "evals/live-agent-cases.json")
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    cases = load_json(args.cases)
    errors = case_errors(cases)
    if args.results:
        errors.extend(result_errors(cases, load_json(args.results)))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated live-agent cases" + (" and results" if args.results else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
