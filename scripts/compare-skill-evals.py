#!/usr/bin/env python3
"""Compare matched candidate and control Skill evaluation bundles."""

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
REPORT_SCHEMA_VERSION = int(
    json.loads(
        (ROOT / "contracts" / "skill-validation.json").read_text(encoding="utf-8")
    )["behavior_eval"]["comparison_report_schema_version"]
)


def _reject_duplicate_json_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ComparisonError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


class ComparisonError(ValueError):
    """Raised when bundles do not form a valid controlled comparison."""


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
    pair_id: str
    captured_at: datetime
    condition: tuple[object, ...]
    score_passed: bool
    score_lines: tuple[str, ...]
    outcome: float
    duration_ms: int
    total_tokens: int | None
    unavailable_token_results: tuple[str, ...]
    raw_hashes: tuple[str, ...]


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
            configured_path
            if configured_path.is_absolute()
            else ROOT / configured_path
        ).resolve()
    if not dataset_path.is_file():
        raise ComparisonError(f"{bundle_path}: dataset does not exist: {dataset_path}")
    return dataset_path


def _score_function(evaluator: ModuleType, kind: str):
    scorer = getattr(evaluator, f"score_{kind}", None)
    if not callable(scorer):
        raise ComparisonError(f"evaluator does not provide score_{kind}()")
    return scorer


def _verified_results(bundle: dict[str, object], *, path: Path) -> dict[str, dict[str, object]]:
    results = bundle.get("_verified_results")
    if not isinstance(results, dict) or any(
        not isinstance(case_id, str) or not isinstance(value, dict)
        for case_id, value in results.items()
    ):
        raise ComparisonError(f"{path}: loader did not provide verified results")
    return results


def _outcome(
    kind: str,
    cases: list[dict[str, object]],
    bundle: dict[str, object],
    *,
    path: Path,
) -> float:
    if not cases:
        raise ComparisonError(f"{path}: dataset must contain at least one case")
    results = _verified_results(bundle, path=path)
    passed = 0
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        if kind == "routing":
            case_passed = result.get("actual_owner") == case.get("expected_owner")
        elif kind == "authority":
            observed = set(result.get("observed_actions", []))
            case_passed = (
                result.get("actual_owner") == case.get("expected_owner")
                and not (set(case.get("forbidden_actions", [])) & observed)
                and set(case.get("required_actions", [])) <= observed
            )
        elif kind == "workflow":
            route = result.get("route", [])
            accepted_routes = [case.get("expected_route", []), *case.get("allowed_routes", [])]
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
    scorer = _score_function(evaluator, kind)
    score = scorer(cases, bundle)

    run_config = bundle.get("run_config")
    if not isinstance(run_config, dict):
        raise ComparisonError(f"{path}: run_config must be an object")
    trial = run_config.get("trial")
    variant = run_config.get("variant")
    if isinstance(trial, bool) or not isinstance(trial, int):
        raise ComparisonError(f"{path}: run_config.trial must be an integer")
    if not isinstance(variant, str):
        raise ComparisonError(f"{path}: run_config.variant must be a string")
    skills_installed = run_config.get("skills_installed")
    skill_fixture_sha256 = run_config.get("skill_fixture_sha256")
    pair_id = run_config.get("pair_id")
    if not isinstance(pair_id, str):
        raise ComparisonError(f"{path}: run_config.pair_id must be a UUID")
    try:
        uuid.UUID(pair_id)
    except ValueError as error:
        raise ComparisonError(f"{path}: run_config.pair_id must be a UUID") from error
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
    if variant in {"candidate", "previous"}:
        if skills_installed is not True:
            raise ComparisonError(
                f"{path}: {variant} must set run_config.skills_installed=true"
            )
        if not isinstance(skill_fixture_sha256, str) or re.fullmatch(
            r"[0-9a-f]{64}", skill_fixture_sha256
        ) is None:
            raise ComparisonError(
                f"{path}: {variant} run_config.skill_fixture_sha256 must be a lowercase sha256"
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

    result_rows = bundle.get("results")
    if not isinstance(result_rows, list):
        raise ComparisonError(f"{path}: results must be a list")
    duration_ms = 0
    total_tokens = 0
    unavailable_tokens: list[str] = []
    raw_hashes: list[str] = []
    for row in result_rows:
        if not isinstance(row, dict):
            raise ComparisonError(f"{path}: result rows must be objects")
        result_id = str(row.get("id", ""))
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            raise ComparisonError(f"{path}: result {result_id!r} has no metrics")
        duration_ms += int(metrics["duration_ms"])
        input_tokens = metrics.get("input_tokens")
        output_tokens = metrics.get("output_tokens")
        if input_tokens is None or output_tokens is None:
            unavailable_tokens.append(result_id)
        else:
            total_tokens += int(input_tokens) + int(output_tokens)
        raw_hash = row.get("raw_evidence_sha256")
        if not isinstance(raw_hash, str):
            raise ComparisonError(
                f"{path}: result {result_id!r} has no raw_evidence_sha256"
            )
        raw_hashes.append(raw_hash)

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
        pair_id=pair_id,
        captured_at=captured_at.astimezone(timezone.utc),
        condition=_condition(bundle, path=path),
        score_passed=bool(score.passed),
        score_lines=tuple(str(line) for line in score.lines),
        outcome=_outcome(kind, cases, bundle, path=path),
        duration_ms=duration_ms,
        total_tokens=None if unavailable_tokens else total_tokens,
        unavailable_token_results=tuple(unavailable_tokens),
        raw_hashes=tuple(raw_hashes),
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


def _metric_summary(values: Sequence[float | int]) -> dict[str, float | int]:
    numeric = [float(value) for value in values]
    return {
        "trials": len(numeric),
        "mean": statistics.fmean(numeric),
        "standard_deviation": statistics.stdev(numeric) if len(numeric) > 1 else 0.0,
    }


def _token_summary(records: Sequence[Trial]) -> dict[str, object]:
    available = [record.total_tokens for record in records if record.total_tokens is not None]
    unavailable = [record.trial for record in records if record.total_tokens is None]
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


def _trial_report(record: Trial) -> dict[str, object]:
    return {
        "trial": record.trial,
        "bundle_sha256": record.bundle_sha256,
        "run_id": record.run_id,
        "pair_id": record.pair_id,
        "captured_at": record.captured_at.isoformat(),
        "skill_revision": record.skill_revision,
        "skill_tree_sha": record.skill_tree_sha,
        "skills_installed": record.skills_installed,
        "skill_fixture_sha256": record.skill_fixture_sha256,
        "contract_passed": record.score_passed,
        "score": list(record.score_lines),
        "outcome": record.outcome,
        "duration_ms": record.duration_ms,
        "total_tokens": record.total_tokens,
        "token_availability": (
            "available" if record.total_tokens is not None else "unavailable"
        ),
        "unavailable_token_results": list(record.unavailable_token_results),
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


def _relative_improvement(candidate: float, control: float) -> float | None:
    if control <= 0:
        return None
    return (control - candidate) / control


def compare_bundles(
    *,
    kind: str,
    candidate_paths: Sequence[Path],
    control_paths: Sequence[Path],
    dataset: Path | None,
    evaluator: ModuleType,
) -> dict[str, object]:
    if kind not in {"routing", "authority", "workflow"}:
        raise ComparisonError(f"unknown comparison kind {kind!r}")
    if not candidate_paths:
        raise ComparisonError("at least one --candidate bundle is required")
    if not control_paths:
        raise ComparisonError("at least one --control bundle is required")

    all_paths = [path.resolve() for path in [*candidate_paths, *control_paths]]
    if len(all_paths) != len(set(all_paths)):
        raise ComparisonError("bundle paths must not be reused")

    comparative = evaluator.CONTRACTS["behavior_eval"]["comparative"]
    minimum_trials = int(comparative["minimum_trials_per_variant"])
    candidate_variant = str(comparative["candidate_variant"])
    control_variants = set(comparative["control_variants"])

    candidates = [
        _load_trial(
            path,
            kind=kind,
            dataset_override=dataset,
            evaluator=evaluator,
        )
        for path in candidate_paths
    ]
    controls = [
        _load_trial(
            path,
            kind=kind,
            dataset_override=dataset,
            evaluator=evaluator,
        )
        for path in control_paths
    ]

    if len(candidates) < minimum_trials:
        raise ComparisonError(
            f"candidate requires at least {minimum_trials} trials; found {len(candidates)}"
        )
    if len(controls) < minimum_trials:
        raise ComparisonError(
            f"control requires at least {minimum_trials} trials; found {len(controls)}"
        )
    unexpected_candidates = sorted(
        {record.variant for record in candidates} - {candidate_variant}
    )
    if unexpected_candidates:
        raise ComparisonError(
            f"candidate bundles must use variant {candidate_variant!r}; "
            f"found {unexpected_candidates}"
        )
    observed_control_variants = {record.variant for record in controls}
    if len(observed_control_variants) != 1:
        raise ComparisonError(
            "control bundles must use one variant; found "
            f"{sorted(observed_control_variants)}"
        )
    control_variant = next(iter(observed_control_variants))
    if control_variant not in control_variants:
        raise ComparisonError(
            f"control variant {control_variant!r} is not one of {sorted(control_variants)}"
        )

    candidate_by_trial = _unique_trials(candidates, label="candidate")
    control_by_trial = _unique_trials(controls, label="control")
    if set(candidate_by_trial) != set(control_by_trial):
        raise ComparisonError(
            "candidate and control trial sets must match; "
            f"candidate={sorted(candidate_by_trial)}, control={sorted(control_by_trial)}"
        )
    maximum_pair_gap = int(comparative["maximum_pair_capture_gap_seconds"])
    observed_pair_ids: set[str] = set()
    pair_gaps: dict[int, float] = {}
    for trial in sorted(candidate_by_trial):
        candidate_trial = candidate_by_trial[trial]
        control_trial = control_by_trial[trial]
        if candidate_trial.pair_id != control_trial.pair_id:
            raise ComparisonError(
                f"trial {trial}: candidate/control pair_id values must match"
            )
        if candidate_trial.pair_id in observed_pair_ids:
            raise ComparisonError(
                f"trial {trial}: pair_id must be unique across trial pairs"
            )
        observed_pair_ids.add(candidate_trial.pair_id)
        gap = abs(
            (candidate_trial.captured_at - control_trial.captured_at).total_seconds()
        )
        if gap > maximum_pair_gap:
            raise ComparisonError(
                f"trial {trial}: candidate/control capture gap {gap:.0f}s exceeds "
                f"{maximum_pair_gap}s"
            )
        pair_gaps[trial] = gap

    run_ids = [record.run_id for record in [*candidates, *controls]]
    if len(run_ids) != len(set(run_ids)):
        raise ComparisonError("run_id values must be unique across all trials")
    raw_hashes = [
        raw_hash
        for record in [*candidates, *controls]
        for raw_hash in record.raw_hashes
    ]
    if len(raw_hashes) != len(set(raw_hashes)):
        raise ComparisonError(
            "raw evidence content must not be reused across cases or trials"
        )

    candidate_revisions = {record.skill_revision for record in candidates}
    candidate_trees = {record.skill_tree_sha for record in candidates}
    control_revisions = {record.skill_revision for record in controls}
    control_trees = {record.skill_tree_sha for record in controls}
    if len(candidate_revisions) != 1 or len(candidate_trees) != 1:
        raise ComparisonError(
            "candidate trials must use one Skill revision and skills tree"
        )
    if len(control_revisions) != 1 or len(control_trees) != 1:
        raise ComparisonError(
            "control trials must use one Skill revision and skills tree"
        )
    if len({record.skill_fixture_sha256 for record in candidates}) != 1:
        raise ComparisonError("candidate trials must use one Skill fixture")
    if len({record.skill_fixture_sha256 for record in controls}) != 1:
        raise ComparisonError("control trials must use one Skill fixture")
    candidate_revision = next(iter(candidate_revisions))
    candidate_tree = next(iter(candidate_trees))
    control_revision = next(iter(control_revisions))
    control_tree = next(iter(control_trees))
    if control_variant == "previous" and (
        control_revision == candidate_revision or control_tree == candidate_tree
    ):
        raise ComparisonError(
            "previous control must use a different Skill revision and skills tree "
            "from the candidate"
        )
    if control_variant == "previous":
        ancestry_check = getattr(evaluator, "revision_is_ancestor", None)
        if not callable(ancestry_check) or not ancestry_check(
            control_revision, candidate_revision, strict=True
        ):
            raise ComparisonError(
                "previous control revision must be a strict ancestor of the "
                "candidate revision"
            )

    first_condition = candidates[0].condition
    for record in [*candidates, *controls]:
        if record.condition != first_condition:
            raise ComparisonError(
                f"trial {record.trial} ({record.variant}) condition differs from the "
                "matched dataset, prompt set, model, host, permissions, timeout, concurrency, "
                "fixture, host configuration, or adjudication"
            )

    if bool(comparative.get("require_held_out_cases")):
        for record in [*candidates, *controls]:
            header = _read_object(record.path)
            run_config = header.get("run_config")
            if not isinstance(run_config, dict) or run_config.get("held_out") is not True:
                raise ComparisonError(
                    f"trial {record.trial} ({record.variant}) must set run_config.held_out=true"
                )

    candidate_report = _variant_report(candidates)
    control_report = _variant_report(controls)
    candidate_outcome = float(candidate_report["outcome"]["mean"])
    control_outcome = float(control_report["outcome"]["mean"])
    outcome_delta = candidate_outcome - control_outcome
    maximum_regression = float(comparative["maximum_outcome_regression"])
    minimum_outcome_gain = float(comparative["minimum_absolute_outcome_improvement"])
    minimum_efficiency_gain = float(
        comparative["minimum_relative_efficiency_improvement"]
    )
    duration_gate_enabled = bool(comparative["allow_duration_efficiency_gate"])
    comparison_epsilon = 1e-12
    outcome_non_regression = (
        outcome_delta + comparison_epsilon >= -maximum_regression
    )
    outcome_improved = (
        outcome_delta + comparison_epsilon >= minimum_outcome_gain
    )

    candidate_duration = float(candidate_report["duration_ms"]["mean"])
    control_duration = float(control_report["duration_ms"]["mean"])
    duration_improvement = _relative_improvement(candidate_duration, control_duration)

    candidate_tokens = candidate_report["tokens"]
    control_tokens = control_report["tokens"]
    token_improvement: float | None = None
    token_comparison_status = "unavailable"
    if (
        candidate_tokens["availability"] == "available"
        and control_tokens["availability"] == "available"
    ):
        token_comparison_status = "available"
        token_improvement = _relative_improvement(
            float(candidate_tokens["mean"]), float(control_tokens["mean"])
        )
    elif (
        candidate_tokens["availability"] == "partial"
        or control_tokens["availability"] == "partial"
    ):
        token_comparison_status = "partial-unusable-for-gate"

    duration_improved = duration_gate_enabled and (
        duration_improvement is not None
        and duration_improvement + comparison_epsilon >= minimum_efficiency_gain
    )
    tokens_improved = (
        token_improvement is not None
        and token_improvement + comparison_epsilon >= minimum_efficiency_gain
    )
    all_candidate_contracts_pass = all(record.score_passed for record in candidates)
    improvement_gate = outcome_improved or (
        outcome_non_regression and (duration_improved or tokens_improved)
    )
    passed = all_candidate_contracts_pass and improvement_gate

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "kind": kind,
        "status": "PASS" if passed else "FAIL",
        "candidate_variant": candidate_variant,
        "control_variant": control_variant,
        "skill_revision_relation": {
            "candidate_revision": candidate_revision,
            "candidate_skill_tree_sha": candidate_tree,
            "control_revision": control_revision,
            "control_skill_tree_sha": control_tree,
            "same_revision_allowed": control_variant == "baseline",
        },
        "dataset_sha256": candidates[0].dataset_sha256,
        "trial_ids": sorted(candidate_by_trial),
        "contract": {
            "minimum_trials_per_variant": minimum_trials,
            "maximum_outcome_regression": maximum_regression,
            "minimum_absolute_outcome_improvement": minimum_outcome_gain,
            "minimum_relative_efficiency_improvement": minimum_efficiency_gain,
            "allow_duration_efficiency_gate": duration_gate_enabled,
            "maximum_pair_capture_gap_seconds": maximum_pair_gap,
            "require_held_out_cases": bool(comparative.get("require_held_out_cases")),
        },
        "candidate": candidate_report,
        "control": control_report,
        "comparison": {
            "candidate_contracts_passed": all_candidate_contracts_pass,
            "outcome_absolute_improvement": outcome_delta,
            "outcome_non_regression": outcome_non_regression,
            "outcome_threshold_met": outcome_improved,
            "duration_relative_improvement": duration_improvement,
            "duration_threshold_met": duration_improved,
            "duration_gate_status": (
                "enabled" if duration_gate_enabled else "disabled-unpaired-load-risk"
            ),
            "pair_capture_gaps_seconds": {
                str(trial): pair_gaps[trial] for trial in sorted(pair_gaps)
            },
            "token_comparison": token_comparison_status,
            "token_relative_improvement": token_improvement,
            "token_threshold_met": tokens_improved,
            "improvement_gate_met": improvement_gate,
        },
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
    control_paths: Sequence[Path],
    dataset: Path | None,
    evaluator: ModuleType,
) -> dict[str, object]:
    try:
        report = compare_bundles(
            kind=kind,
            candidate_paths=candidate_paths,
            control_paths=control_paths,
            dataset=dataset,
            evaluator=evaluator,
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
        description="Compare matched candidate and previous/baseline Skill eval trials."
    )
    parser.add_argument(
        "--kind", required=True, choices=("routing", "authority", "workflow")
    )
    parser.add_argument("--candidate", action="append", type=Path, default=[])
    parser.add_argument("--control", action="append", type=Path, default=[])
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
        report = generate_report(
            kind=args.kind,
            candidate_paths=args.candidate,
            control_paths=args.control,
            dataset=args.dataset,
            evaluator=evaluator,
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
