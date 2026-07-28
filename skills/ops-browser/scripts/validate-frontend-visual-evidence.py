#!/usr/bin/env python3
"""Validate a frontend-visual-evidence/v1 JSON artifact offline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def default_schema() -> Path:
    script = Path(__file__).resolve()
    package_schema = script.parent.parent / "assets" / "frontend-visual-evidence.schema.json"
    if package_schema.is_file():
        return package_schema
    return script.parents[1] / "protocols" / "frontend-visual-evidence-v1.schema.json"


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {ref}")
    value: Any = root
    for part in ref[2:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or key not in value:
            raise ValueError(f"unresolved schema reference: {ref}")
        value = value[key]
    if not isinstance(value, dict):
        raise ValueError(f"schema reference is not an object: {ref}")
    return value


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"unsupported schema type: {expected}")


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any] | None = None,
    path: str = "$",
) -> list[str]:
    root = schema if root is None else root
    if "$ref" in schema:
        return schema_errors(value, _resolve_ref(root, schema["$ref"]), root, path)

    errors: list[str] = []
    if "allOf" in schema:
        for index, item in enumerate(schema["allOf"]):
            errors.extend(schema_errors(value, item, root, f"{path}.allOf[{index}]"))
    if "anyOf" in schema:
        variants = [schema_errors(value, item, root, path) for item in schema["anyOf"]]
        if all(variant for variant in variants):
            errors.append(f"{path}: must match at least one anyOf branch")
    if "oneOf" in schema:
        matches = sum(not schema_errors(value, item, root, path) for item in schema["oneOf"])
        if matches != 1:
            errors.append(f"{path}: must match exactly one oneOf branch")
    if "not" in schema and not schema_errors(value, schema["not"], root, path):
        errors.append(f"{path}: matches forbidden schema")
    if "if" in schema and not schema_errors(value, schema["if"], root, path):
        errors.extend(schema_errors(value, schema.get("then", {}), root, path))

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in enum {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type is not None and not _type_matches(value, expected_type):
        errors.append(f"{path}: expected {expected_type}")
        return errors

    if isinstance(value, dict):
        required = schema.get("required", [])
        for name in required:
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")
        properties = schema.get("properties", {})
        for name, child in properties.items():
            if name in value:
                errors.extend(schema_errors(value[name], child, root, f"{path}.{name}"))
        if schema.get("additionalProperties") is False:
            for name in sorted(set(value) - set(properties)):
                errors.append(f"{path}: unexpected property {name!r}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: needs at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: allows at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path}: items must be unique")
        prefixes = schema.get("prefixItems", [])
        for index, child in enumerate(prefixes):
            if index < len(value):
                errors.extend(schema_errors(value[index], child, root, f"{path}[{index}]"))
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index in range(len(prefixes), len(value)):
                errors.extend(schema_errors(value[index], item_schema, root, f"{path}[{index}]"))

    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{path}: string is shorter than {schema['minLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: must be >= {schema['minimum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: must be > {schema['exclusiveMinimum']}")
    return errors


def semantic_errors(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []
    stage = payload.get("stage")
    source = payload.get("selected_source", {})
    approval = source.get("approval", {}) if isinstance(source, dict) else {}
    approval_status = approval.get("status") if isinstance(approval, dict) else None
    readiness = payload.get("readiness", {})
    readiness_status = readiness.get("status") if isinstance(readiness, dict) else None
    blockers = readiness.get("blockers", []) if isinstance(readiness, dict) else []
    if readiness_status == "Ready":
        if approval_status != "approved":
            errors.append("Ready readiness requires an approved selected source")
        if blockers:
            errors.append("Ready readiness requires an empty blockers list")
    elif readiness_status in {"Partial", "Not Ready"} and not blockers:
        errors.append(f"{readiness_status} readiness requires at least one blocker")
    if stage in {"mapped", "pass-1", "final"} and readiness_status != "Ready":
        errors.append(f"stage {stage} requires Ready implementation readiness")
    evidence = payload.get("evidence", [])
    evidence_ids = [item.get("id") for item in evidence if isinstance(item, dict)]
    known_evidence = {item for item in evidence_ids if isinstance(item, str)}
    evidence_by_id = {
        item["id"]: item
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if len(evidence_ids) != len(known_evidence):
        errors.append("evidence IDs must be unique")

    deltas = payload.get("delta_table", [])
    delta_ids = [item.get("acceptance_id") for item in deltas if isinstance(item, dict)]
    mappings = payload.get("implementation_mapping", [])
    mapping_ids = [item.get("acceptance_id") for item in mappings if isinstance(item, dict)]
    if len(delta_ids) != len(set(delta_ids)):
        errors.append("delta acceptance IDs must be unique")
    if len(mapping_ids) != len(set(mapping_ids)):
        errors.append("implementation mapping acceptance IDs must be unique")
    if stage in {"mapped", "pass-1", "final"} and set(delta_ids) != set(mapping_ids):
        errors.append("implementation mapping must cover exactly the delta acceptance IDs")

    referenced: set[str] = set()
    for delta in deltas:
        if not isinstance(delta, dict):
            continue
        for column in ("selected_source", "current_runtime", "target_contract"):
            value = delta.get(column)
            if isinstance(value, dict):
                ids = value.get("evidence_ids", [])
                referenced.update(ids)
                declared_level = value.get("evidence_level")
                actual_levels = {
                    evidence_by_id[evidence_id].get("level")
                    for evidence_id in ids
                    if isinstance(evidence_id, str) and evidence_id in evidence_by_id
                }
                if declared_level not in actual_levels:
                    errors.append(
                        f"delta {delta.get('acceptance_id')} {column} declares "
                        f"{declared_level} without matching evidence"
                    )
                forbidden_levels = {
                    "selected_source": {"browser-computed", "proposed"},
                    "current_runtime": {"source-extracted", "proposed"},
                    "target_contract": {"browser-computed"},
                }[column]
                conflicting = sorted(actual_levels & forbidden_levels)
                if conflicting:
                    errors.append(
                        f"delta {delta.get('acceptance_id')} {column} references "
                        f"forbidden evidence levels: {conflicting}"
                    )

    reviews = payload.get("visual_reviews", [])
    for index, review in enumerate(reviews, start=1):
        if not isinstance(review, dict):
            continue
        if review.get("pass") != index:
            errors.append("visual review pass numbers must be contiguous from 1")
        design = review.get("design_capture")
        runtime = review.get("runtime_capture")
        if isinstance(design, dict) and isinstance(runtime, dict):
            if design.get("viewport") != runtime.get("viewport"):
                errors.append(f"visual review pass {index} capture viewports must match")
            if design.get("state") != runtime.get("state"):
                errors.append(f"visual review pass {index} capture states must match")
        check_ids: set[str] = set()
        for check in review.get("computed_checks", []):
            if isinstance(check, dict):
                ids = check.get("evidence_ids", [])
                referenced.update(ids)
                check_ids.update(ids)
                if not _has_matching_runtime_evidence(ids, evidence_by_id, index, runtime):
                    errors.append(
                        f"visual review pass {index} computed check lacks matching browser-computed evidence"
                    )
                elif not _has_matching_runtime_evidence(
                    ids, evidence_by_id, index, runtime, check.get("category")
                ):
                    errors.append(
                        f"visual review pass {index} computed check {check.get('category')} "
                        "lacks matching category evidence"
                    )
        for finding in review.get("findings", []):
            if isinstance(finding, dict):
                ids = finding.get("evidence_ids", [])
                referenced.update(ids)
                if not _has_matching_runtime_evidence(ids, evidence_by_id, index, runtime):
                    errors.append(
                        f"visual review pass {index} finding {finding.get('acceptance_id')} lacks matching browser-computed evidence"
                    )

    coverage = payload.get("runtime_coverage", {})
    if isinstance(coverage, dict):
        for record in coverage.values():
            if isinstance(record, dict):
                referenced.update(record.get("evidence_ids", []))

    dangling = sorted(referenced - known_evidence)
    if dangling:
        errors.append(f"unknown evidence IDs referenced: {dangling}")

    verdict = payload.get("final_verdict", {})
    if stage == "final" and reviews and isinstance(coverage, dict):
        last_review = reviews[-1] if isinstance(reviews[-1], dict) else {}
        runtime = last_review.get("runtime_capture", {})
        last_pass = last_review.get("pass")
        for name, record in coverage.items():
            if not isinstance(record, dict) or record.get("status") != "verified":
                continue
            ids = record.get("evidence_ids", [])
            if not ids or not _has_matching_runtime_evidence(
                ids, evidence_by_id, last_pass, runtime, name
            ):
                errors.append(
                    f"verified runtime coverage {name} lacks matching final-pass browser-computed evidence"
                )

    if isinstance(verdict, dict) and verdict.get("status") == "Complete":
        if not isinstance(approval, dict) or approval.get("status") != "approved":
            errors.append("Complete verdict requires an approved selected source")
        if not isinstance(readiness, dict) or readiness.get("status") != "Ready":
            errors.append("Complete verdict requires Ready implementation readiness")
        incomplete = [
            name
            for name, record in coverage.items()
            if isinstance(record, dict)
            and record.get("status") in {"failed", "Not verified"}
        ]
        if incomplete:
            errors.append(f"Complete verdict has incomplete runtime coverage: {incomplete}")
        if verdict.get("not_verified"):
            errors.append("Complete verdict cannot retain Not verified items")
        if verdict.get("remaining_gaps"):
            errors.append("Complete verdict cannot retain remaining gaps")
        if reviews and isinstance(reviews[-1], dict):
            if reviews[-1].get("verdict") != "pass":
                errors.append("Complete verdict requires the final visual review to pass")
            latest_status: dict[tuple[object, object], object] = {}
            for review in reviews:
                if not isinstance(review, dict):
                    continue
                for finding in review.get("findings", []):
                    if isinstance(finding, dict):
                        latest_status[(finding.get("severity"), finding.get("acceptance_id"))] = finding.get("status")
            open_blockers = [
                acceptance_id
                for (severity, acceptance_id), status in latest_status.items()
                if severity in {"P0", "P1"} and status == "open"
            ]
            if open_blockers:
                errors.append(f"Complete verdict has open P0/P1 findings: {open_blockers}")
    return errors


def _has_matching_runtime_evidence(
    evidence_ids: list[object],
    evidence_by_id: dict[str, dict[str, object]],
    review_pass: object,
    runtime_capture: object,
    required_category: object = None,
) -> bool:
    if not isinstance(runtime_capture, dict):
        return False
    for evidence_id in evidence_ids:
        item = evidence_by_id.get(evidence_id) if isinstance(evidence_id, str) else None
        if not item or item.get("level") != "browser-computed":
            continue
        if item.get("review_pass") != review_pass:
            continue
        if item.get("viewport") != runtime_capture.get("viewport"):
            continue
        if item.get("state") != runtime_capture.get("state"):
            continue
        if required_category is not None and required_category not in item.get(
            "categories", []
        ):
            continue
        return True
    return False


def validate_artifact(artifact: Path, schema: Path) -> None:
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    contract = json.loads(schema.read_text(encoding="utf-8"))
    errors = schema_errors(payload, contract)
    if errors:
        raise ValueError("; ".join(errors))
    errors = semantic_errors(payload)
    if errors:
        raise ValueError("; ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate frontend-visual-evidence/v1 JSON without network access."
    )
    parser.add_argument("artifact", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=default_schema(),
    )
    args = parser.parse_args()
    try:
        validate_artifact(args.artifact.resolve(), args.schema.resolve())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"validated frontend visual evidence: {args.artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
