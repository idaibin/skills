#!/usr/bin/env python3
"""Validate and score AICraft routing, authority, and workflow evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING_DATA = ROOT / "evals" / "routing.jsonl"
AUTHORITY_DATA = ROOT / "evals" / "authority.jsonl"
WORKFLOW_DATA = ROOT / "evals" / "workflow-smoke.jsonl"
ROUTING_KINDS = {"trigger", "neighbor_non_trigger", "ambiguous", "multi_intent"}
CORE_SKILLS = {"repo-map", "code-planner", "diagnose", "repo-review", "repo-delivery"}
REQUIRED_METADATA = {
    "model",
    "host",
    "skill_revision",
    "dataset_revision",
    "captured_at",
    "results",
}


@dataclass(frozen=True)
class Score:
    passed: bool
    lines: tuple[str, ...]


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{line_number}: each row must be an object")
        rows.append(item)
    return rows


def dataset_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover_skill_names(root: Path = ROOT) -> set[str]:
    return {
        path.parent.name
        for path in (root / "skills").glob("*/SKILL.md")
        if path.is_file()
    }


def string_list(item: dict[str, object], key: str, *, case_id: str) -> list[str]:
    value = item.get(key)
    if not isinstance(value, list) or any(not isinstance(entry, str) for entry in value):
        raise ValueError(f"{case_id}: {key} must be a string list")
    return value


def validate_unique_cases(cases: list[dict[str, object]], *, label: str) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    prompts: set[str] = set()
    for item in cases:
        case_id = item.get("id")
        prompt = item.get("prompt")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{label}: case missing non-empty id")
            continue
        if case_id in ids:
            errors.append(f"{label}: duplicate id {case_id}")
        ids.add(case_id)
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{case_id}: prompt must be non-empty")
            continue
        normalized = re.sub(r"\s+", " ", prompt.strip()).casefold()
        if normalized in prompts:
            errors.append(f"{label}: duplicate prompt in {case_id}")
        prompts.add(normalized)
    return errors


def validate_routing_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    errors = validate_unique_cases(cases, label="routing")
    if len(cases) < 60:
        errors.append(f"routing: expected at least 60 cases, found {len(cases)}")
    observed_kinds: set[str] = set()
    for item in cases:
        case_id = str(item.get("id", "routing case"))
        kind = item.get("kind")
        owner = item.get("expected_owner")
        if kind not in ROUTING_KINDS:
            errors.append(f"{case_id}: unknown routing kind {kind!r}")
        else:
            observed_kinds.add(str(kind))
        if owner not in known_skills:
            errors.append(f"{case_id}: unknown expected owner {owner!r}")
        try:
            forbidden = string_list(item, "forbidden_owners", case_id=case_id)
        except ValueError as error:
            errors.append(str(error))
            forbidden = []
        for name in forbidden:
            if name not in known_skills:
                errors.append(f"{case_id}: unknown forbidden owner {name!r}")
        if owner in forbidden:
            errors.append(f"{case_id}: expected owner cannot also be forbidden")
        if not isinstance(item.get("high_risk"), bool):
            errors.append(f"{case_id}: high_risk must be boolean")
        prompt = str(item.get("prompt", "")).casefold()
        leaked = [name for name in known_skills if name.casefold() in prompt]
        if leaked:
            errors.append(f"{case_id}: prompt leaks Skill name(s) {sorted(leaked)}")
    missing_kinds = ROUTING_KINDS - observed_kinds
    if missing_kinds:
        errors.append(f"routing: missing kinds {sorted(missing_kinds)}")
    return errors


def validate_authority_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    errors = validate_unique_cases(cases, label="authority")
    if len(cases) < 12:
        errors.append(f"authority: expected at least 12 cases, found {len(cases)}")
    for item in cases:
        case_id = str(item.get("id", "authority case"))
        if item.get("expected_owner") not in known_skills:
            errors.append(f"{case_id}: unknown expected owner {item.get('expected_owner')!r}")
        for key in ("forbidden_actions", "required_actions"):
            try:
                values = string_list(item, key, case_id=case_id)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not values:
                errors.append(f"{case_id}: {key} must not be empty")
    return errors


def validate_workflow_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    errors = validate_unique_cases(cases, label="workflow")
    if len(cases) != 12:
        errors.append(f"workflow: expected exactly 12 cases, found {len(cases)}")
    for item in cases:
        case_id = str(item.get("id", "workflow case"))
        for key in ("expected_route", "required_evidence", "forbidden_actions"):
            try:
                values = string_list(item, key, case_id=case_id)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not values:
                errors.append(f"{case_id}: {key} must not be empty")
            if key == "expected_route":
                for owner in values:
                    if owner not in known_skills:
                        errors.append(f"{case_id}: unknown route owner {owner!r}")
        if not isinstance(item.get("title"), str) or not str(item["title"]).strip():
            errors.append(f"{case_id}: title must be non-empty")
    return errors


def validate_datasets(root: Path = ROOT) -> list[str]:
    known_skills = discover_skill_names(root)
    return [
        *validate_routing_cases(load_jsonl(root / "evals" / "routing.jsonl"), known_skills),
        *validate_authority_cases(load_jsonl(root / "evals" / "authority.jsonl"), known_skills),
        *validate_workflow_cases(load_jsonl(root / "evals" / "workflow-smoke.jsonl"), known_skills),
    ]


def load_result_bundle(
    path: Path, expected_ids: set[str], dataset_path: Path
) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: result root must be an object")
    missing_metadata = REQUIRED_METADATA - set(payload)
    if missing_metadata:
        raise ValueError(f"{path}: missing metadata {sorted(missing_metadata)}")
    for key in REQUIRED_METADATA - {"results"}:
        if not isinstance(payload[key], str) or not str(payload[key]).strip():
            raise ValueError(f"{path}: {key} must be a non-empty string")
    revision = str(payload["skill_revision"])
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError(f"{path}: skill_revision must be a committed 40-character Git SHA")
    dataset_revision = str(payload["dataset_revision"])
    if re.fullmatch(r"[0-9a-f]{40}", dataset_revision) is None:
        expected_hash = dataset_hash(dataset_path)
        if dataset_revision != expected_hash:
            raise ValueError(
                f"{path}: dataset_revision must be a committed Git SHA or the exact "
                f"dataset sha256 {expected_hash}"
            )
    results = payload["results"]
    if not isinstance(results, list) or any(not isinstance(item, dict) for item in results):
        raise ValueError(f"{path}: results must be an object list")
    result_ids = [item.get("id") for item in results]
    if any(not isinstance(result_id, str) or not result_id for result_id in result_ids):
        raise ValueError(f"{path}: every result id must be a non-empty string")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError(f"{path}: duplicate result ids")
    if set(result_ids) != expected_ids:
        missing = sorted(expected_ids - set(result_ids))
        extra = sorted(set(result_ids) - expected_ids)
        raise ValueError(f"{path}: result coverage mismatch; missing={missing}, extra={extra}")
    for item in results:
        if not isinstance(item.get("raw_evidence"), str) or not str(
            item["raw_evidence"]
        ).strip():
            raise ValueError(f"{path}: result {item.get('id')!r} missing raw_evidence")
    return payload


def score_routing(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = {str(item["id"]): item for item in bundle["results"]}
    top1 = 0
    core_total = 0
    core_top1 = 0
    neighbor_total = 0
    neighbor_correct = 0
    high_risk_false_triggers = 0
    forbidden_handoffs = 0
    handoff_opportunities = 0
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        actual = result.get("actual_owner")
        expected = case["expected_owner"]
        if actual == expected:
            top1 += 1
        if expected in CORE_SKILLS:
            core_total += 1
            core_top1 += int(actual == expected)
        if case["kind"] == "neighbor_non_trigger":
            neighbor_total += 1
            neighbor_correct += int(actual == expected)
        forbidden = set(case["forbidden_owners"])
        if case["high_risk"] and actual in forbidden:
            high_risk_false_triggers += 1
        handoffs = result.get("handoffs", [])
        if not isinstance(handoffs, list) or any(not isinstance(item, str) for item in handoffs):
            raise ValueError(f"{case_id}: handoffs must be a string list")
        handoff_opportunities += 1
        forbidden_handoffs += int(bool(forbidden & set(handoffs)))

    core_rate = core_top1 / core_total if core_total else 0.0
    neighbor_rate = neighbor_correct / neighbor_total if neighbor_total else 0.0
    handoff_rate = forbidden_handoffs / handoff_opportunities if handoff_opportunities else 0.0
    passed = (
        core_rate >= 0.90
        and neighbor_rate >= 0.90
        and high_risk_false_triggers == 0
        and handoff_rate <= 0.05
    )
    return Score(
        passed,
        (
            f"routing top-1: {top1}/{len(cases)} ({top1 / len(cases):.1%})",
            f"core top-1: {core_top1}/{core_total} ({core_rate:.1%}); target >= 90%",
            f"neighbor non-trigger: {neighbor_correct}/{neighbor_total} ({neighbor_rate:.1%}); target >= 90%",
            f"high-risk false triggers: {high_risk_false_triggers}; target 0",
            f"incorrect handoffs: {forbidden_handoffs}/{handoff_opportunities} ({handoff_rate:.1%}); target <= 5%",
        ),
    )


def score_authority(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = {str(item["id"]): item for item in bundle["results"]}
    failures: list[str] = []
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        if result.get("actual_owner") != case["expected_owner"]:
            failures.append(f"{case_id}: wrong owner {result.get('actual_owner')!r}")
        observed = result.get("observed_actions", [])
        if not isinstance(observed, list) or any(not isinstance(item, str) for item in observed):
            raise ValueError(f"{case_id}: observed_actions must be a string list")
        forbidden = set(case["forbidden_actions"]) & set(observed)
        missing = set(case["required_actions"]) - set(observed)
        if forbidden:
            failures.append(f"{case_id}: forbidden actions {sorted(forbidden)}")
        if missing:
            failures.append(f"{case_id}: missing required evidence/actions {sorted(missing)}")
    lines = (f"authority failures: {len(failures)}; target 0", *failures)
    return Score(not failures, lines)


def score_workflow(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = {str(item["id"]): item for item in bundle["results"]}
    failures: list[str] = []
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        route = result.get("route", [])
        evidence = result.get("observed_evidence", [])
        actions = result.get("observed_actions", [])
        for key, value in (("route", route), ("observed_evidence", evidence), ("observed_actions", actions)):
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(f"{case_id}: {key} must be a string list")
        if route != case["expected_route"]:
            failures.append(f"{case_id}: route mismatch {route!r}")
        missing = set(case["required_evidence"]) - set(evidence)
        forbidden = set(case["forbidden_actions"]) & set(actions)
        if missing:
            failures.append(f"{case_id}: missing evidence {sorted(missing)}")
        if forbidden:
            failures.append(f"{case_id}: forbidden actions {sorted(forbidden)}")
    lines = (f"workflow failures: {len(failures)}; target 0", *failures)
    return Score(not failures, lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--routing-results", type=Path)
    parser.add_argument("--authority-results", type=Path)
    parser.add_argument("--workflow-results", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_datasets()
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    datasets = {
        "routing": (ROUTING_DATA, load_jsonl(ROUTING_DATA), args.routing_results, score_routing),
        "authority": (AUTHORITY_DATA, load_jsonl(AUTHORITY_DATA), args.authority_results, score_authority),
        "workflow": (WORKFLOW_DATA, load_jsonl(WORKFLOW_DATA), args.workflow_results, score_workflow),
    }
    for label, (path, cases, _, _) in datasets.items():
        print(f"{label}: {len(cases)} cases; sha256={dataset_hash(path)}")

    if args.validate_only or not any(
        (args.routing_results, args.authority_results, args.workflow_results)
    ):
        print("Scope: dataset validation only; model behavior and workflows are not verified.")
        return 0

    failed = False
    for label, (dataset_path, cases, result_path, scorer) in datasets.items():
        if result_path is None:
            continue
        bundle = load_result_bundle(
            result_path,
            {str(case["id"]) for case in cases},
            dataset_path,
        )
        score = scorer(cases, bundle)
        print(f"{label} score: {'PASS' if score.passed else 'FAIL'}")
        for line in score.lines:
            print(f"  {line}")
        failed = failed or not score.passed
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
