#!/usr/bin/env python3
"""Compare matched candidate, previous, and no-Skill evaluation bundles."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import statistics
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR_PATH = ROOT / "scripts" / "eval-skill-contracts.py"
PROTOCOL_PATH = ROOT / "scripts" / "evaluation_protocol.py"
_PROTOCOL_SPEC = importlib.util.spec_from_file_location(
    "aicraft_evaluation_protocol_for_comparator", PROTOCOL_PATH
)
if _PROTOCOL_SPEC is None or _PROTOCOL_SPEC.loader is None:
    raise RuntimeError(f"cannot load evaluation protocol from {PROTOCOL_PATH}")
PROTOCOL = importlib.util.module_from_spec(_PROTOCOL_SPEC)
sys.modules[_PROTOCOL_SPEC.name] = PROTOCOL
_PROTOCOL_SPEC.loader.exec_module(PROTOCOL)
REPORT_SCHEMA_VERSION = int(
    json.loads(
        (ROOT / "contracts" / "skill-validation.json").read_text(encoding="utf-8")
    )["behavior_eval"]["comparison_report_schema_version"]
)


class ComparisonError(ValueError):
    """Raised when bundles do not form a valid controlled comparison."""


def _reject_duplicate_json_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ComparisonError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


@dataclass(frozen=True)
class Trial:
    path: Path
    bundle_sha256: str
    dataset_path: Path
    dataset_sha256: str
    trial: int
    variant: str
    run_id: str
    skill_revision: str
    skill_tree_sha: str
    skills_installed: bool
    skill_fixture_sha256: str | None
    comparison_group_id: str
    attempt_id: str
    attempt_path: str
    campaign_id: str
    campaign_path: str
    campaign_sha256: str
    evaluation_protocol_revision: str
    evaluation_protocol_sha256: str
    environment_policy_sha256: str
    captured_at: datetime
    condition: tuple[object, ...]
    score_passed: bool
    score_lines: tuple[str, ...]
    outcome: float
    duration_ms: int
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    unavailable_input_token_results: tuple[str, ...]
    unavailable_output_token_results: tuple[str, ...]
    unavailable_total_token_results: tuple[str, ...]
    raw_hashes: tuple[str, ...]
    case_count: int


def load_evaluator(path: Path = EVALUATOR_PATH) -> ModuleType:
    """Load the scorer without requiring its hyphenated filename to be importable."""

    module_name = "aicraft_eval_skill_contracts_for_comparison"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ComparisonError(f"cannot load evaluator from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _read_object(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ComparisonError(f"{path}: cannot read bundle header: {error}") from error
    if not isinstance(payload, dict):
        raise ComparisonError(f"{path}: bundle root must be an object")
    return payload


def _resolve_dataset_path(
    bundle_path: Path,
    bundle_header: dict[str, object],
    override: Path | None,
) -> Path:
    if override is not None:
        dataset_path = override.resolve()
    else:
        run_config = bundle_header.get("run_config")
        if not isinstance(run_config, dict):
            raise ComparisonError(f"{bundle_path}: run_config must be an object")
        configured = run_config.get("dataset_path")
        if not isinstance(configured, str) or not configured.strip():
            raise ComparisonError(
                f"{bundle_path}: run_config.dataset_path is required when --dataset is omitted"
            )
        configured_path = Path(configured)
        dataset_path = (
            configured_path if configured_path.is_absolute() else ROOT / configured_path
        ).resolve()
    if not dataset_path.is_file():
        raise ComparisonError(f"{bundle_path}: dataset does not exist: {dataset_path}")
    return dataset_path


def _score_function(evaluator: ModuleType, kind: str):
    scorer = getattr(evaluator, f"score_{kind}", None)
    if not callable(scorer):
        raise ComparisonError(f"evaluator does not provide score_{kind}()")
    return scorer


def _verified_results(
    bundle: dict[str, object], *, path: Path
) -> dict[str, dict[str, object]]:
    results = bundle.get("_verified_results")
    if not isinstance(results, dict) or any(
        not isinstance(case_id, str) or not isinstance(value, dict)
        for case_id, value in results.items()
    ):
        raise ComparisonError(f"{path}: loader did not provide verified results")
    return results


def _outcome(
    evaluator: ModuleType,
    kind: str,
    cases: list[dict[str, object]],
    bundle: dict[str, object],
    *,
    path: Path,
) -> float:
    if not cases:
        raise ComparisonError(f"{path}: dataset must contain at least one case")
    results = _verified_results(bundle, path=path)
    routing_assessor = getattr(evaluator, "assess_routing_case", None)
    if kind == "routing" and not callable(routing_assessor):
        raise ComparisonError("evaluator does not provide assess_routing_case()")

    passed = 0
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        if kind == "routing":
            assessment = routing_assessor(case, result)
            if not isinstance(assessment, dict) or not isinstance(
                assessment.get("full_case_success"), bool
            ):
                raise ComparisonError(
                    "evaluator assess_routing_case() must return boolean "
                    "full_case_success"
                )
            case_passed = assessment["full_case_success"]
        elif kind == "authority":
            observed = set(result.get("observed_actions", []))
            case_passed = (
                result.get("actual_owner") == case.get("expected_owner")
                and not (set(case.get("forbidden_actions", [])) & observed)
                and set(case.get("required_actions", [])) <= observed
            )
        elif kind == "workflow":
            route = result.get("route", [])
            accepted_routes = [
                case.get("expected_route", []),
                *case.get("allowed_routes", []),
            ]
            observed_evidence = set(result.get("observed_evidence", []))
            observed_actions = set(result.get("observed_actions", []))
            case_passed = (
                route in accepted_routes
                and set(case.get("required_evidence", [])) <= observed_evidence
                and not (set(case.get("forbidden_actions", [])) & observed_actions)
            )
        else:
            raise ComparisonError(f"unknown comparison kind {kind!r}")
        passed += int(case_passed)
    return passed / len(cases)


def _condition(bundle: dict[str, object], *, path: Path) -> tuple[object, ...]:
    run_config = bundle.get("run_config")
    if not isinstance(run_config, dict):
        raise ComparisonError(f"{path}: run_config must be an object")
    adjudication = bundle.get("adjudication")
    if not isinstance(adjudication, dict):
        raise ComparisonError(f"{path}: adjudication must be an object")
    required_fields = (
        bundle.get("dataset_revision"),
        run_config.get("prompt_set_sha256"),
        bundle.get("model"),
        bundle.get("host"),
        run_config.get("host_name"),
        run_config.get("permissions"),
        run_config.get("timeout_seconds"),
        run_config.get("concurrency"),
        run_config.get("case_set_sha256"),
        run_config.get("prompt_template_version"),
        run_config.get("prompt_template_sha256"),
        run_config.get("fixture_sha256"),
        run_config.get("host_config_sha256"),
        run_config.get("environment_policy_sha256"),
        run_config.get("campaign_id"),
        run_config.get("campaign_path"),
        run_config.get("campaign_sha256"),
        run_config.get("evaluation_protocol_revision"),
        run_config.get("evaluation_protocol_sha256"),
        adjudication.get("method"),
        adjudication.get("reviewer"),
        adjudication.get("reviewer_version"),
        adjudication.get("config_sha256"),
    )
    if any(value is None for value in required_fields):
        raise ComparisonError(f"{path}: comparison condition metadata is incomplete")
    provenance_fields = (
        run_config.get("dataset_git_revision"),
        run_config.get("evaluation_anchor_revision"),
        run_config.get("held_out_provenance_path"),
        run_config.get("held_out_provenance_sha256"),
    )
    if run_config.get("held_out") is True and any(
        value is None for value in provenance_fields
    ):
        raise ComparisonError(
            f"{path}: held-out comparison provenance metadata is incomplete"
        )
    return required_fields + provenance_fields


def _validate_dataset_cases(
    evaluator: ModuleType,
    kind: str,
    cases: list[dict[str, object]],
    *,
    dataset_path: Path,
    held_out: bool,
) -> None:
    discover = getattr(evaluator, "discover_skill_names", None)
    if not callable(discover):
        raise ComparisonError(
            "evaluator does not provide Skill discovery for dataset coverage validation"
        )
    known_skills = discover()
    if kind == "routing" and held_out:
        validator = getattr(evaluator, "validate_held_out_routing_cases", None)
        if not callable(validator):
            raise ComparisonError(
                "evaluator does not provide held-out routing coverage validation"
            )
        errors = validator(cases, known_skills)
    elif kind == "routing":
        validator = getattr(evaluator, "validate_routing_cases", None)
        if not callable(validator):
            raise ComparisonError(
                "evaluator does not provide routing dataset coverage validation"
            )
        evaluator_root = Path(getattr(evaluator, "ROOT", ROOT))
        errors = validator(
            cases,
            known_skills,
            routing_graph_path=evaluator_root / "docs" / "skills" / "routing-graph.json",
        )
    else:
        validator = getattr(evaluator, f"validate_{kind}_cases", None)
        if not callable(validator):
            raise ComparisonError(
                f"evaluator does not provide {kind} dataset coverage validation"
            )
        errors = validator(cases, known_skills)
    if errors:
        rendered = "; ".join(str(error) for error in errors)
        raise ComparisonError(f"{dataset_path}: invalid {kind} coverage: {rendered}")


def _optional_positive_int(
    value: object, *, path: Path, result_id: str, field: str
) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ComparisonError(
            f"{path}: result {result_id!r} metrics.{field} must be a positive "
            "integer or null"
        )
    return value


def _load_trial(
    path: Path,
    *,
    kind: str,
    dataset_override: Path | None,
    evaluator: ModuleType,
) -> Trial:
    path = path.resolve()
    header = _read_object(path)
    dataset_path = _resolve_dataset_path(path, header, dataset_override)
    cases = evaluator.load_jsonl(dataset_path)
    header_run_config = header.get("run_config")
    held_out = (
        isinstance(header_run_config, dict)
        and header_run_config.get("held_out") is True
    )
    _validate_dataset_cases(
        evaluator,
        kind,
        cases,
        dataset_path=dataset_path,
        held_out=held_out,
    )
    expected_ids = {str(case["id"]) for case in cases}
    prompts = {str(case["id"]): str(case["prompt"]) for case in cases}
    bundle = evaluator.load_result_bundle(
        path,
        expected_ids,
        dataset_path,
        prompts,
        evidence_kind=kind,
    )
    score = _score_function(evaluator, kind)(cases, bundle)

    run_config = bundle.get("run_config")
    if not isinstance(run_config, dict):
        raise ComparisonError(f"{path}: run_config must be an object")
    trial = run_config.get("trial")
    variant = run_config.get("variant")
    if isinstance(trial, bool) or not isinstance(trial, int):
        raise ComparisonError(f"{path}: run_config.trial must be an integer")
    if not isinstance(variant, str):
        raise ComparisonError(f"{path}: run_config.variant must be a string")

    comparison_group_id = run_config.get("comparison_group_id")
    if not isinstance(comparison_group_id, str):
        raise ComparisonError(
            f"{path}: run_config.comparison_group_id must be a UUID"
        )
    try:
        uuid.UUID(comparison_group_id)
    except ValueError as error:
        raise ComparisonError(
            f"{path}: run_config.comparison_group_id must be a UUID"
        ) from error

    skills_installed = run_config.get("skills_installed")
    skill_fixture_sha256 = run_config.get("skill_fixture_sha256")
    if variant in {"candidate", "previous"}:
        if skills_installed is not True:
            raise ComparisonError(
                f"{path}: {variant} must set run_config.skills_installed=true"
            )
        if not isinstance(skill_fixture_sha256, str) or re.fullmatch(
            r"[0-9a-f]{64}", skill_fixture_sha256
        ) is None:
            raise ComparisonError(
                f"{path}: {variant} run_config.skill_fixture_sha256 must be a "
                "lowercase sha256"
            )
    elif variant == "baseline":
        if skills_installed is not False:
            raise ComparisonError(
                f"{path}: baseline must set run_config.skills_installed=false"
            )
        if skill_fixture_sha256 is not None:
            raise ComparisonError(
                f"{path}: baseline run_config.skill_fixture_sha256 must be null"
            )
    else:
        raise ComparisonError(f"{path}: unsupported comparison variant {variant!r}")

    captured_value = bundle.get("captured_at")
    if not isinstance(captured_value, str):
        raise ComparisonError(f"{path}: captured_at must be an ISO-8601 timestamp")
    try:
        captured_at = datetime.fromisoformat(captured_value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ComparisonError(
            f"{path}: captured_at must be an ISO-8601 timestamp"
        ) from error
    if captured_at.tzinfo is None:
        raise ComparisonError(f"{path}: captured_at must include a timezone")

    result_rows = bundle.get("results")
    if not isinstance(result_rows, list):
        raise ComparisonError(f"{path}: results must be a list")
    duration_ms = 0
    input_tokens = 0
    output_tokens = 0
    unavailable_input_tokens: list[str] = []
    unavailable_output_tokens: list[str] = []
    raw_hashes: list[str] = []
    for row in result_rows:
        if not isinstance(row, dict):
            raise ComparisonError(f"{path}: result rows must be objects")
        result_id = str(row.get("id", ""))
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            raise ComparisonError(f"{path}: result {result_id!r} has no metrics")
        duration = _optional_positive_int(
            metrics.get("duration_ms"),
            path=path,
            result_id=result_id,
            field="duration_ms",
        )
        if duration is None:
            raise ComparisonError(
                f"{path}: result {result_id!r} metrics.duration_ms cannot be null"
            )
        duration_ms += duration
        result_input = _optional_positive_int(
            metrics.get("input_tokens"),
            path=path,
            result_id=result_id,
            field="input_tokens",
        )
        result_output = _optional_positive_int(
            metrics.get("output_tokens"),
            path=path,
            result_id=result_id,
            field="output_tokens",
        )
        if result_input is None:
            unavailable_input_tokens.append(result_id)
        else:
            input_tokens += result_input
        if result_output is None:
            unavailable_output_tokens.append(result_id)
        else:
            output_tokens += result_output
        raw_hash = row.get("raw_evidence_sha256")
        if not isinstance(raw_hash, str):
            raise ComparisonError(
                f"{path}: result {result_id!r} has no raw_evidence_sha256"
            )
        raw_hashes.append(raw_hash)

    unavailable_total_tokens = sorted(
        set(unavailable_input_tokens) | set(unavailable_output_tokens)
    )
    complete_input = None if unavailable_input_tokens else input_tokens
    complete_output = None if unavailable_output_tokens else output_tokens
    complete_total = (
        None
        if unavailable_total_tokens
        else int(complete_input or 0) + int(complete_output or 0)
    )

    return Trial(
        path=path,
        bundle_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        dataset_path=dataset_path,
        dataset_sha256=str(bundle["dataset_revision"]),
        trial=trial,
        variant=variant,
        run_id=str(bundle["run_id"]),
        skill_revision=str(bundle["skill_revision"]),
        skill_tree_sha=str(bundle["skill_tree_sha"]),
        skills_installed=skills_installed,
        skill_fixture_sha256=skill_fixture_sha256,
        comparison_group_id=comparison_group_id,
        attempt_id=str(run_config.get("attempt_id")),
        attempt_path=str(run_config.get("attempt_path")),
        campaign_id=str(run_config.get("campaign_id")),
        campaign_path=str(run_config.get("campaign_path")),
        campaign_sha256=str(run_config.get("campaign_sha256")),
        evaluation_protocol_revision=str(
            run_config.get("evaluation_protocol_revision")
        ),
        evaluation_protocol_sha256=str(
            run_config.get("evaluation_protocol_sha256")
        ),
        environment_policy_sha256=str(
            run_config.get("environment_policy_sha256")
        ),
        captured_at=captured_at.astimezone(timezone.utc),
        condition=_condition(bundle, path=path),
        score_passed=bool(score.passed),
        score_lines=tuple(str(line) for line in score.lines),
        outcome=_outcome(evaluator, kind, cases, bundle, path=path),
        duration_ms=duration_ms,
        input_tokens=complete_input,
        output_tokens=complete_output,
        total_tokens=complete_total,
        unavailable_input_token_results=tuple(unavailable_input_tokens),
        unavailable_output_token_results=tuple(unavailable_output_tokens),
        unavailable_total_token_results=tuple(unavailable_total_tokens),
        raw_hashes=tuple(raw_hashes),
        case_count=len(cases),
    )


def _unique_trials(records: Sequence[Trial], *, label: str) -> dict[int, Trial]:
    indexed: dict[int, Trial] = {}
    for record in records:
        if record.trial in indexed:
            raise ComparisonError(
                f"{label}: duplicate trial {record.trial} in "
                f"{indexed[record.trial].path} and {record.path}"
            )
        indexed[record.trial] = record
    return indexed


def _validate_campaign_attempt_ledger(
    campaign, records: Sequence[Trial]
) -> dict[str, object]:
    artifact_root = (ROOT / campaign.artifact_root).resolve()
    try:
        artifact_root.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ComparisonError("campaign artifact_root escapes repository") from error
    planned = {
        (trial, variant, group_id)
        for trial, group_id in campaign.trial_groups.items()
        for variant in ("candidate", "previous", "baseline")
    }
    attempt_paths = sorted(artifact_root.glob("*/attempt.json"))
    attempts: dict[tuple[int, str, str], dict[str, object]] = {}
    for attempt_path in attempt_paths:
        try:
            payload = json.loads(
                attempt_path.read_text(encoding="utf-8"),
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise ComparisonError(
                f"cannot read campaign attempt ledger {attempt_path}: {error}"
            ) from error
        if not isinstance(payload, dict):
            raise ComparisonError(f"campaign attempt ledger must be an object: {attempt_path}")
        if payload.get("campaign_id") != campaign.campaign_id:
            raise ComparisonError(
                f"artifact_root contains an attempt for another campaign: {attempt_path}"
            )
        slot = (
            payload.get("trial"),
            payload.get("variant"),
            payload.get("comparison_group_id"),
        )
        if slot not in planned:
            raise ComparisonError(f"campaign attempt ledger has an unplanned slot: {slot}")
        if slot in attempts:
            raise ComparisonError(f"campaign attempt ledger duplicates slot: {slot}")
        if payload.get("status") != "success":
            raise ComparisonError(
                f"campaign slot {slot} has non-success attempt status "
                f"{payload.get('status')!r}"
            )
        attempts[slot] = payload
    if set(attempts) != planned:
        missing = sorted(planned - set(attempts))
        extra = sorted(set(attempts) - planned)
        raise ComparisonError(
            f"campaign attempt ledger must exactly match planned slots; "
            f"missing={missing}, extra={extra}"
        )
    by_slot = {
        (record.trial, record.variant, record.comparison_group_id): record
        for record in records
    }
    if set(by_slot) != planned:
        raise ComparisonError("bundle slots do not exactly match the campaign attempt ledger")
    for slot, record in by_slot.items():
        attempt = attempts[slot]
        expected_attempt_path = record.path.parent / record.attempt_path
        if (
            expected_attempt_path.parent != record.path.parent
            or expected_attempt_path not in attempt_paths
            or record.path.parent.parent != artifact_root
            or attempt.get("attempt_id") != record.attempt_id
            or attempt.get("run_id") != record.run_id
            or attempt.get("artifact") != record.path.name
            or attempt.get("artifact_sha256") != record.bundle_sha256
        ):
            raise ComparisonError(
                f"campaign attempt ledger does not bind bundle for slot {slot}"
            )
    return {
        "planned_slots": len(planned),
        "observed_successful_attempts": len(attempts),
        "failed_or_extra_attempts": 0,
    }


def _metric_summary(values: Sequence[float | int]) -> dict[str, float | int]:
    numeric = [float(value) for value in values]
    return {
        "trials": len(numeric),
        "mean": statistics.fmean(numeric),
        "standard_deviation": statistics.stdev(numeric) if len(numeric) > 1 else 0.0,
    }


def _token_dimension_summary(
    records: Sequence[Trial], attribute: str
) -> dict[str, object]:
    available = [
        getattr(record, attribute)
        for record in records
        if getattr(record, attribute) is not None
    ]
    unavailable = [
        record.trial for record in records if getattr(record, attribute) is None
    ]
    if not available:
        availability = "unavailable"
    elif unavailable:
        availability = "partial"
    else:
        availability = "available"
    summary: dict[str, object] = {
        "availability": availability,
        "available_trials": len(available),
        "unavailable_trials": unavailable,
        "mean": None,
        "standard_deviation": None,
    }
    if available:
        metric = _metric_summary(available)
        summary["mean"] = metric["mean"]
        summary["standard_deviation"] = metric["standard_deviation"]
    return summary


def _token_summary(records: Sequence[Trial]) -> dict[str, object]:
    return {
        "input": _token_dimension_summary(records, "input_tokens"),
        "output": _token_dimension_summary(records, "output_tokens"),
        "total": _token_dimension_summary(records, "total_tokens"),
    }


def _trial_report(record: Trial) -> dict[str, object]:
    return {
        "trial": record.trial,
        "bundle_sha256": record.bundle_sha256,
        "run_id": record.run_id,
        "comparison_group_id": record.comparison_group_id,
        "captured_at": record.captured_at.isoformat(),
        "skill_revision": record.skill_revision,
        "skill_tree_sha": record.skill_tree_sha,
        "skills_installed": record.skills_installed,
        "skill_fixture_sha256": record.skill_fixture_sha256,
        "contract_passed": record.score_passed,
        "score": list(record.score_lines),
        "outcome": record.outcome,
        "duration_ms": record.duration_ms,
        "input_tokens": record.input_tokens,
        "output_tokens": record.output_tokens,
        "total_tokens": record.total_tokens,
        "token_availability": {
            "input": "available" if record.input_tokens is not None else "unavailable",
            "output": (
                "available" if record.output_tokens is not None else "unavailable"
            ),
            "total": "available" if record.total_tokens is not None else "unavailable",
        },
        "unavailable_token_results": {
            "input": list(record.unavailable_input_token_results),
            "output": list(record.unavailable_output_token_results),
            "total": list(record.unavailable_total_token_results),
        },
    }


def _variant_report(records: Sequence[Trial]) -> dict[str, object]:
    ordered = sorted(records, key=lambda record: record.trial)
    return {
        "all_contract_passed": all(record.score_passed for record in ordered),
        "outcome": _metric_summary([record.outcome for record in ordered]),
        "duration_ms": _metric_summary([record.duration_ms for record in ordered]),
        "tokens": _token_summary(ordered),
        "trials": [_trial_report(record) for record in ordered],
    }


def _relative_reduction(candidate: float, control: float) -> float | None:
    if control <= 0:
        return None
    return (control - candidate) / control


def _available_mean(report: dict[str, object], dimension: str) -> float | None:
    tokens = report["tokens"]
    summary = tokens[dimension]
    if summary["availability"] != "available":
        return None
    return float(summary["mean"])


def _pair_comparison(
    candidate: dict[str, object],
    control: dict[str, object],
    *,
    minimum_outcome_improvement: float,
    maximum_outcome_regression: float | None,
) -> dict[str, object]:
    epsilon = 1e-12
    candidate_outcome = float(candidate["outcome"]["mean"])
    control_outcome = float(control["outcome"]["mean"])
    outcome_delta = candidate_outcome - control_outcome
    non_regression = (
        None
        if maximum_outcome_regression is None
        else outcome_delta + epsilon >= -maximum_outcome_regression
    )
    candidate_duration = float(candidate["duration_ms"]["mean"])
    control_duration = float(control["duration_ms"]["mean"])

    token_reductions: dict[str, float | None] = {}
    for dimension in ("input", "output", "total"):
        candidate_mean = _available_mean(candidate, dimension)
        control_mean = _available_mean(control, dimension)
        token_reductions[dimension] = (
            None
            if candidate_mean is None or control_mean is None
            else _relative_reduction(candidate_mean, control_mean)
        )

    return {
        "outcome_absolute_improvement": outcome_delta,
        "outcome_non_regression": non_regression,
        "outcome_threshold_met": (
            outcome_delta + epsilon >= minimum_outcome_improvement
        ),
        "full_case_absolute_improvement": outcome_delta,
        "full_case_non_regression": non_regression,
        "full_case_improvement_threshold": minimum_outcome_improvement,
        "full_case_improvement_threshold_met": (
            outcome_delta + epsilon >= minimum_outcome_improvement
        ),
        "duration_relative_reduction": _relative_reduction(
            candidate_duration, control_duration
        ),
        "input_token_relative_reduction": token_reductions["input"],
        "output_token_relative_reduction": token_reductions["output"],
        "total_token_relative_reduction": token_reductions["total"],
        "duration_and_total_tokens_gate_status": "reported-only",
    }


def _marginal_input_overhead(
    candidate_by_trial: dict[int, Trial],
    previous_by_trial: dict[int, Trial],
    baseline_by_trial: dict[int, Trial],
    *,
    minimum_reduction: float,
    minimum_absolute_savings_per_case: float,
) -> dict[str, object]:
    groups: list[dict[str, object]] = []
    candidate_overheads: list[int] = []
    previous_overheads: list[int] = []
    incomplete_trials: list[int] = []
    for trial in sorted(candidate_by_trial):
        candidate = candidate_by_trial[trial]
        previous = previous_by_trial[trial]
        baseline = baseline_by_trial[trial]
        values = (candidate.input_tokens, previous.input_tokens, baseline.input_tokens)
        candidate_overhead: int | None = None
        previous_overhead: int | None = None
        if all(value is not None for value in values):
            candidate_overhead = int(candidate.input_tokens) - int(baseline.input_tokens)
            previous_overhead = int(previous.input_tokens) - int(baseline.input_tokens)
            candidate_overheads.append(candidate_overhead)
            previous_overheads.append(previous_overhead)
        else:
            incomplete_trials.append(trial)
        groups.append(
            {
                "trial": trial,
                "comparison_group_id": candidate.comparison_group_id,
                "candidate_input_tokens": candidate.input_tokens,
                "previous_input_tokens": previous.input_tokens,
                "no_skill_input_tokens": baseline.input_tokens,
                "candidate_overhead": candidate_overhead,
                "previous_overhead": previous_overhead,
            }
        )

    if not candidate_overheads:
        availability = "unavailable"
    elif incomplete_trials:
        availability = "partial"
    else:
        availability = "available"
    all_nonnegative = (
        availability == "available"
        and all(value >= 0 for value in candidate_overheads)
        and all(value >= 0 for value in previous_overheads)
    )
    candidate_not_greater_each_group = (
        availability == "available"
        and all(
            candidate <= previous
            for candidate, previous in zip(
                candidate_overheads, previous_overheads, strict=True
            )
        )
    )
    previous_mean = (
        statistics.fmean(previous_overheads) if previous_overheads else None
    )
    positive_previous_mean = previous_mean is not None and previous_mean > 0
    gate_eligible = (
        all_nonnegative
        and positive_previous_mean
        and candidate_not_greater_each_group
    )
    candidate_mean = (
        statistics.fmean(candidate_overheads) if candidate_overheads else None
    )
    relative_reduction = (
        (previous_mean - candidate_mean) / previous_mean
        if gate_eligible and candidate_mean is not None and previous_mean is not None
        else None
    )
    case_counts = {record.case_count for record in candidate_by_trial.values()}
    if len(case_counts) != 1:
        raise ComparisonError("campaign trials must use one complete case count")
    case_count = next(iter(case_counts))
    absolute_savings_per_case = (
        (previous_mean - candidate_mean) / case_count
        if gate_eligible and candidate_mean is not None and previous_mean is not None
        else None
    )
    threshold_met = bool(
        relative_reduction is not None
        and relative_reduction + 1e-12 >= minimum_reduction
        and absolute_savings_per_case is not None
        and absolute_savings_per_case + 1e-12
        >= minimum_absolute_savings_per_case
    )
    return {
        "availability": availability,
        "incomplete_trials": incomplete_trials,
        "groups": groups,
        "candidate_overhead": (
            _metric_summary(candidate_overheads) if candidate_overheads else None
        ),
        "previous_overhead": (
            _metric_summary(previous_overheads) if previous_overheads else None
        ),
        "all_group_overheads_nonnegative": all_nonnegative,
        "candidate_overhead_not_greater_each_group": (
            candidate_not_greater_each_group
        ),
        "previous_mean_overhead_positive": positive_previous_mean,
        "gate_eligible": gate_eligible,
        "relative_reduction": relative_reduction,
        "minimum_relative_reduction": minimum_reduction,
        "absolute_savings_tokens_per_case": absolute_savings_per_case,
        "minimum_absolute_savings_tokens_per_case": (
            minimum_absolute_savings_per_case
        ),
        "threshold_met": threshold_met,
    }


def _variant_identity(records: Sequence[Trial], *, label: str) -> tuple[str, str]:
    revisions = {record.skill_revision for record in records}
    trees = {record.skill_tree_sha for record in records}
    if len(revisions) != 1 or len(trees) != 1:
        raise ComparisonError(f"{label} trials must use one Skill revision and skills tree")
    if len({record.skill_fixture_sha256 for record in records}) != 1:
        raise ComparisonError(f"{label} trials must use one Skill fixture")
    return next(iter(revisions)), next(iter(trees))


def compare_bundles(
    *,
    kind: str,
    candidate_paths: Sequence[Path],
    previous_paths: Sequence[Path],
    baseline_paths: Sequence[Path],
    dataset: Path | None,
    evaluator: ModuleType,
    campaign,
) -> dict[str, object]:
    if kind not in {"routing", "authority", "workflow"}:
        raise ComparisonError(f"unknown comparison kind {kind!r}")
    for option, paths in (
        ("--candidate", candidate_paths),
        ("--previous", previous_paths),
        ("--baseline", baseline_paths),
    ):
        if not paths:
            raise ComparisonError(f"at least one {option} bundle is required")

    all_paths = [
        path.resolve()
        for path in [*candidate_paths, *previous_paths, *baseline_paths]
    ]
    if len(all_paths) != len(set(all_paths)):
        raise ComparisonError("bundle paths must not be reused")

    comparative = evaluator.CONTRACTS["behavior_eval"]["comparative"]
    if comparative.get("require_candidate_overhead_not_greater_per_group") is not True:
        raise ComparisonError(
            "comparative.require_candidate_overhead_not_greater_per_group must be true"
        )
    if comparative.get("allow_duration_efficiency_gate") is not False:
        raise ComparisonError(
            "comparative.allow_duration_efficiency_gate must be false"
        )
    minimum_trials = int(comparative["minimum_trials_per_variant"])
    candidate_variant = str(comparative["candidate_variant"])
    required_controls = set(comparative["required_control_variants"])
    if required_controls != {"previous", "baseline"}:
        raise ComparisonError(
            "comparative.required_control_variants must require previous and baseline"
        )
    contract_claimable_dimensions = comparative["claimable_dimensions"]
    expected_claimable_dimensions = {
        "routing_outcome_vs_previous",
        "routing_outcome_vs_no_skill",
        "marginal_skill_input_efficiency",
    }
    if (
        not isinstance(contract_claimable_dimensions, list)
        or any(not isinstance(item, str) for item in contract_claimable_dimensions)
        or len(contract_claimable_dimensions) != len(expected_claimable_dimensions)
        or set(contract_claimable_dimensions) != expected_claimable_dimensions
    ):
        raise ComparisonError(
            "comparative.claimable_dimensions must define the three supported "
            "routing claim dimensions"
        )

    candidates = [
        _load_trial(
            path, kind=kind, dataset_override=dataset, evaluator=evaluator
        )
        for path in candidate_paths
    ]
    previous = [
        _load_trial(
            path, kind=kind, dataset_override=dataset, evaluator=evaluator
        )
        for path in previous_paths
    ]
    baseline = [
        _load_trial(
            path, kind=kind, dataset_override=dataset, evaluator=evaluator
        )
        for path in baseline_paths
    ]
    variants = (
        ("candidate", candidates, candidate_variant),
        ("previous", previous, "previous"),
        ("baseline", baseline, "baseline"),
    )
    for label, records, expected_variant in variants:
        if len(records) < minimum_trials:
            raise ComparisonError(
                f"{label} requires at least {minimum_trials} trials; found {len(records)}"
            )
        unexpected = sorted(
            {record.variant for record in records} - {expected_variant}
        )
        if unexpected:
            raise ComparisonError(
                f"{label} bundles must use variant {expected_variant!r}; found {unexpected}"
            )

    candidate_by_trial = _unique_trials(candidates, label="candidate")
    previous_by_trial = _unique_trials(previous, label="previous")
    baseline_by_trial = _unique_trials(baseline, label="baseline")
    trial_sets = {
        "candidate": set(candidate_by_trial),
        "previous": set(previous_by_trial),
        "baseline": set(baseline_by_trial),
    }
    campaign_trial_groups = campaign.trial_groups
    if any(set(values) != set(campaign_trial_groups) for values in trial_sets.values()):
        raise ComparisonError(
            "candidate, previous, and baseline must contain the complete campaign "
            f"trial set {sorted(campaign_trial_groups)}"
        )
    if len({frozenset(value) for value in trial_sets.values()}) != 1:
        raise ComparisonError(
            "candidate, previous, and baseline trial sets must match; "
            + ", ".join(
                f"{label}={sorted(values)}" for label, values in trial_sets.items()
            )
        )

    maximum_group_gap = int(comparative["maximum_group_capture_gap_seconds"])
    observed_group_ids: set[str] = set()
    group_gaps: dict[int, float] = {}
    for trial in sorted(candidate_by_trial):
        group = (
            candidate_by_trial[trial],
            previous_by_trial[trial],
            baseline_by_trial[trial],
        )
        group_ids = {record.comparison_group_id for record in group}
        if len(group_ids) != 1:
            raise ComparisonError(
                f"trial {trial}: candidate/previous/baseline comparison_group_id "
                "values must match"
            )
        group_id = next(iter(group_ids))
        if group_id != campaign_trial_groups[trial]:
            raise ComparisonError(
                f"trial {trial}: comparison_group_id does not match the campaign"
            )
        if group_id in observed_group_ids:
            raise ComparisonError(
                f"trial {trial}: comparison_group_id must be unique across trial groups"
            )
        observed_group_ids.add(group_id)
        timestamps = [record.captured_at for record in group]
        gap = (max(timestamps) - min(timestamps)).total_seconds()
        if gap > maximum_group_gap:
            raise ComparisonError(
                f"trial {trial}: three-way capture gap {gap:.0f}s exceeds "
                f"{maximum_group_gap}s"
            )
        group_gaps[trial] = gap

    all_records = [*candidates, *previous, *baseline]
    for record in all_records:
        if (
            record.campaign_id != campaign.campaign_id
            or record.campaign_path != campaign.relative_path
            or record.campaign_sha256 != campaign.sha256
            or record.evaluation_protocol_revision != campaign.anchor_revision
            or record.evaluation_protocol_sha256
            != campaign.payload["evaluation_protocol"]["sha256"]
        ):
            raise ComparisonError(
                f"trial {record.trial} ({record.variant}) campaign/protocol binding "
                "does not match --campaign"
            )
    attempt_ledger = _validate_campaign_attempt_ledger(campaign, all_records)
    run_ids = [record.run_id for record in all_records]
    if len(run_ids) != len(set(run_ids)):
        raise ComparisonError("run_id values must be unique across all trials")
    raw_hashes = [raw_hash for record in all_records for raw_hash in record.raw_hashes]
    if len(raw_hashes) != len(set(raw_hashes)):
        raise ComparisonError(
            "raw evidence content must not be reused across cases or trials"
        )

    candidate_revision, candidate_tree = _variant_identity(
        candidates, label="candidate"
    )
    previous_revision, previous_tree = _variant_identity(previous, label="previous")
    baseline_revision, baseline_tree = _variant_identity(baseline, label="baseline")
    if previous_tree == candidate_tree:
        raise ComparisonError(
            "previous must use a different skills tree from the candidate"
        )
    ancestry_check = getattr(evaluator, "revision_is_ancestor", None)
    if not callable(ancestry_check) or not ancestry_check(
        previous_revision, candidate_revision, strict=True
    ):
        raise ComparisonError(
            "previous revision must be a strict ancestor of the candidate revision"
        )
    if (
        candidate_revision != campaign.anchor_revision
        or previous_revision != campaign.previous_revision
        or baseline_revision != campaign.anchor_revision
    ):
        raise ComparisonError(
            "candidate, previous, and baseline revisions must exactly match the campaign"
        )
    if baseline_revision != candidate_revision or baseline_tree != candidate_tree:
        raise ComparisonError(
            "baseline must use the candidate revision and skills tree while disabling Skills"
        )

    first_condition = candidates[0].condition
    first_dataset_path = candidates[0].dataset_path
    for record in all_records:
        if (
            record.dataset_path != first_dataset_path
            or record.condition != first_condition
        ):
            raise ComparisonError(
                f"trial {record.trial} ({record.variant}) condition differs from the "
                "matched dataset, prompt, model, host, permissions, timeout, concurrency, "
                "fixture, host configuration, provenance, or adjudication"
            )

    if bool(comparative.get("require_held_out_cases")):
        for record in all_records:
            header = _read_object(record.path)
            run_config = header.get("run_config")
            if not isinstance(run_config, dict) or run_config.get("held_out") is not True:
                raise ComparisonError(
                    f"trial {record.trial} ({record.variant}) must set "
                    "run_config.held_out=true"
                )

    candidate_report = _variant_report(candidates)
    previous_report = _variant_report(previous)
    baseline_report = _variant_report(baseline)
    maximum_regression = float(
        comparative["maximum_full_case_regression_vs_previous"]
    )
    minimum_previous_gain = float(
        comparative["minimum_full_case_improvement_vs_previous"]
    )
    minimum_no_skill_gain = float(
        comparative["minimum_full_case_improvement_vs_no_skill"]
    )
    minimum_marginal_reduction = float(
        comparative["minimum_relative_marginal_skill_input_reduction"]
    )
    minimum_absolute_savings = float(
        comparative["minimum_absolute_marginal_input_savings_tokens_per_case"]
    )
    candidate_vs_previous = _pair_comparison(
        candidate_report,
        previous_report,
        minimum_outcome_improvement=minimum_previous_gain,
        maximum_outcome_regression=maximum_regression,
    )
    candidate_vs_no_skill = _pair_comparison(
        candidate_report,
        baseline_report,
        minimum_outcome_improvement=minimum_no_skill_gain,
        maximum_outcome_regression=None,
    )
    marginal = _marginal_input_overhead(
        candidate_by_trial,
        previous_by_trial,
        baseline_by_trial,
        minimum_reduction=minimum_marginal_reduction,
        minimum_absolute_savings_per_case=minimum_absolute_savings,
    )

    candidate_contracts_passed = bool(candidate_report["all_contract_passed"])
    previous_non_regression = bool(candidate_vs_previous["outcome_non_regression"])
    common_claim_gate = candidate_contracts_passed and previous_non_regression
    claimable_dimension_status = {
        "routing_outcome_vs_previous": (
            common_claim_gate
            and bool(candidate_vs_previous["outcome_threshold_met"])
        ),
        "routing_outcome_vs_no_skill": (
            common_claim_gate
            and bool(candidate_vs_no_skill["outcome_threshold_met"])
        ),
        "marginal_skill_input_efficiency": (
            common_claim_gate and bool(marginal["threshold_met"])
        ),
    }
    claimable_dimensions = [
        dimension
        for dimension in contract_claimable_dimensions
        if claimable_dimension_status[dimension]
    ]
    candidate_vs_previous["claimable"] = claimable_dimension_status[
        "routing_outcome_vs_previous"
    ]
    candidate_vs_no_skill["claimable"] = claimable_dimension_status[
        "routing_outcome_vs_no_skill"
    ]
    marginal["claimable"] = claimable_dimension_status[
        "marginal_skill_input_efficiency"
    ]
    passed = common_claim_gate and bool(claimable_dimensions)

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "campaign": {
            "campaign_id": campaign.campaign_id,
            "campaign_path": campaign.relative_path,
            "campaign_sha256": campaign.sha256,
            "evaluation_protocol_revision": campaign.anchor_revision,
            "evaluation_protocol_sha256": campaign.payload["evaluation_protocol"][
                "sha256"
            ],
        },
        "attempt_ledger": attempt_ledger,
        "kind": kind,
        "status": "PASS" if passed else "FAIL",
        "candidate_variant": candidate_variant,
        "previous_variant": "previous",
        "no_skill_variant": "baseline",
        "skill_revision_relation": {
            "candidate_revision": candidate_revision,
            "candidate_skill_tree_sha": candidate_tree,
            "previous_revision": previous_revision,
            "previous_skill_tree_sha": previous_tree,
            "no_skill_revision": baseline_revision,
            "no_skill_skill_tree_sha": baseline_tree,
            "previous_is_strict_ancestor": True,
            "no_skill_uses_candidate_revision_and_tree": True,
        },
        "dataset_sha256": candidates[0].dataset_sha256,
        "trial_ids": sorted(candidate_by_trial),
        "contract": {
            "minimum_trials_per_variant": minimum_trials,
            "maximum_full_case_regression_vs_previous": maximum_regression,
            "minimum_full_case_improvement_vs_previous": minimum_previous_gain,
            "minimum_full_case_improvement_vs_no_skill": minimum_no_skill_gain,
            "minimum_relative_marginal_skill_input_reduction": (
                minimum_marginal_reduction
            ),
            "minimum_absolute_marginal_input_savings_tokens_per_case": (
                minimum_absolute_savings
            ),
            "require_candidate_overhead_not_greater_per_group": True,
            "allow_duration_efficiency_gate": False,
            "maximum_group_capture_gap_seconds": maximum_group_gap,
            "claimable_dimensions": list(contract_claimable_dimensions),
            "require_held_out_cases": bool(
                comparative.get("require_held_out_cases")
            ),
        },
        "comparison_group_capture_gaps_seconds": {
            str(trial): group_gaps[trial] for trial in sorted(group_gaps)
        },
        "candidate_contracts_passed": candidate_contracts_passed,
        "candidate": candidate_report,
        "previous": previous_report,
        "no_skill": baseline_report,
        "candidate_vs_previous": candidate_vs_previous,
        "candidate_vs_no_skill": candidate_vs_no_skill,
        "marginal_skill_input_overhead": marginal,
        "claimable_dimensions": claimable_dimensions,
        "claimable_dimension_status": claimable_dimension_status,
        "errors": [],
    }


def _with_report_hash(report: dict[str, object]) -> dict[str, object]:
    unhashed = dict(report)
    unhashed.pop("report_sha256", None)
    canonical = json.dumps(
        unhashed,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    report = dict(unhashed)
    report["report_sha256"] = hashlib.sha256(canonical).hexdigest()
    return report


def generate_report(
    *,
    kind: str,
    candidate_paths: Sequence[Path],
    previous_paths: Sequence[Path],
    baseline_paths: Sequence[Path],
    dataset: Path | None,
    evaluator: ModuleType,
    campaign,
) -> dict[str, object]:
    try:
        report = compare_bundles(
            kind=kind,
            candidate_paths=candidate_paths,
            previous_paths=previous_paths,
            baseline_paths=baseline_paths,
            dataset=dataset,
            evaluator=evaluator,
            campaign=campaign,
        )
    except (ComparisonError, KeyError, OSError, TypeError, ValueError) as error:
        report = {
            "schema_version": REPORT_SCHEMA_VERSION,
            "kind": kind,
            "status": "FAIL",
            "errors": [str(error)],
        }
    return _with_report_hash(report)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare matched candidate, previous, and no-Skill routing trials."
        )
    )
    parser.add_argument(
        "--kind", required=True, choices=("routing", "authority", "workflow")
    )
    parser.add_argument("--candidate", action="append", type=Path, default=[])
    parser.add_argument("--previous", action="append", type=Path, default=[])
    parser.add_argument("--baseline", action="append", type=Path, default=[])
    parser.add_argument(
        "--campaign",
        type=Path,
        required=True,
        help="Committed campaign JSON that preregisters the complete comparison.",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        help=(
            "Dataset used for every bundle. If omitted, each bundle's "
            "repository-relative run_config.dataset_path is resolved from the "
            "AICraft repository root."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Also write the self-hashed JSON report to this file.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        evaluator = load_evaluator()
        campaign = PROTOCOL.load_campaign(ROOT, args.campaign, evaluator.CONTRACTS)
        report = generate_report(
            kind=args.kind,
            candidate_paths=args.candidate,
            previous_paths=args.previous,
            baseline_paths=args.baseline,
            dataset=args.dataset,
            evaluator=evaluator,
            campaign=campaign,
        )
    except Exception as error:
        report = _with_report_hash(
            {
                "schema_version": REPORT_SCHEMA_VERSION,
                "kind": args.kind,
                "status": "FAIL",
                "errors": [f"cannot initialize evaluator: {error}"],
            }
        )
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output is not None:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered + "\n", encoding="utf-8")
        except OSError as error:
            print(f"cannot write comparison report: {error}", file=sys.stderr)
            return 2
    print(rendered)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
