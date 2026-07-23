#!/usr/bin/env python3
"""Validate the required shape and cross-file identity of a UI specification package."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError as error:  # pragma: no cover - host dependency boundary
    raise SystemExit("PyYAML is required: install it in the active project environment") from error


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "assets" / "ui-spec-package.schema.json"
SCORE_MAXIMA = {
    "product_truth": 15,
    "source_fidelity": 15,
    "information_architecture": 10,
    "interaction_states": 15,
    "responsive_accessibility": 15,
    "component_token_mapping": 15,
    "engineering_fit": 10,
    "evidence": 5,
}
CORE_SCORE_KEYS = tuple(key for key, maximum in SCORE_MAXIMA.items() if maximum == 15)
SAFE_TASK_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)


def missing_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def valid_approval_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_visual_source(
    name: str,
    document: dict[str, Any],
    required_keys: tuple[str, ...],
    errors: list[str],
) -> dict[str, Any]:
    visual_source = document.get("visual_source")
    if not isinstance(visual_source, dict):
        errors.append(f"{name}: visual_source must be an object")
        return {}
    for key in required_keys:
        if key not in visual_source or missing_value(visual_source[key]):
            errors.append(f"{name}: visual_source.{key} is required")
    if visual_source.get("status") not in ("selected", "accepted"):
        errors.append(f"{name}: visual_source.status must be selected or accepted")
    for key in ("use", "ignore"):
        if key in visual_source and not isinstance(visual_source[key], list):
            errors.append(f"{name}: visual_source.{key} must be a list")
        elif isinstance(visual_source.get(key), list):
            for index, item in enumerate(visual_source[key]):
                if not isinstance(item, str) or not item.strip():
                    errors.append(
                        f"{name}: visual_source.{key}[{index}] must be a non-empty string"
                    )
    return visual_source


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    documents: dict[str, Any] = {}
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    file_schemas = schema["properties"]
    visual_source_keys = tuple(schema["$defs"]["visualSource"]["required"])
    for name in schema["required"]:
        keys = file_schemas[name].get("required", [])
        path = root / name
        if not path.is_file():
            errors.append(f"{name}: missing")
            continue
        try:
            document = load(path)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{name}: invalid document: {error}")
            continue
        if not isinstance(document, dict):
            errors.append(f"{name}: root must be an object")
            continue
        documents[name] = document
        for key in keys:
            if key not in document:
                errors.append(f"{name}: missing {key}")

    references = documents.get("references.yaml", {}).get("references", [])
    if not isinstance(references, list):
        errors.append("references.yaml: references must be a list")
        references = []
    for index, reference in enumerate(references):
        if not isinstance(reference, dict):
            errors.append(f"references.yaml: references[{index}] must be an object")
            continue
        for key in ("id", "source", "rights_status", "use", "ignore"):
            if key not in reference or reference[key] in (None, "", []):
                errors.append(f"references.yaml: references[{index}].{key} is required")

    profile_source = validate_visual_source(
        "profile.yaml", documents.get("profile.yaml", {}), visual_source_keys, errors
    )
    task_source = validate_visual_source(
        "task.yaml", documents.get("task.yaml", {}), visual_source_keys, errors
    )
    for key in visual_source_keys:
        if key in profile_source and key in task_source and profile_source[key] != task_source[key]:
            errors.append(f"visual source mismatch: profile.yaml and task.yaml differ on {key}")

    task = documents.get("task.yaml", {})
    if task and not task.get("scope", {}).get("exclude"):
        errors.append("task.yaml: scope.exclude must declare a boundary")
    if task and not task.get("facts", {}).get("unavailable"):
        errors.append("task.yaml: facts.unavailable must declare non-capabilities")

    evaluation = documents.get("evaluation.yaml", {})
    scores = evaluation.get("scores", {}) if evaluation else {}
    score_structure_valid = True
    if not isinstance(scores, dict):
        errors.append("evaluation.yaml: scores must be an object")
        score_structure_valid = False
        scores = {}
    else:
        actual_keys = set(scores)
        expected_keys = set(SCORE_MAXIMA)
        if actual_keys != expected_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            errors.append(
                f"evaluation.yaml: score keys must match rubric; missing={missing}, extra={extra}"
            )
            score_structure_valid = False
        for key, maximum in SCORE_MAXIMA.items():
            value = scores.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"evaluation.yaml: scores.{key} must be numeric")
                score_structure_valid = False
            elif not 0 <= value <= maximum:
                errors.append(f"evaluation.yaml: scores.{key} must be between 0 and {maximum}")
                score_structure_valid = False
    total = evaluation.get("total") if evaluation else None
    if not isinstance(total, (int, float)) or isinstance(total, bool):
        errors.append("evaluation.yaml: total must be numeric")
        score_structure_valid = False
    elif score_structure_valid and total != sum(scores.values()):
        errors.append("evaluation.yaml: total must equal the weighted score sum")
        score_structure_valid = False
    if evaluation.get("hard_blockers") and evaluation.get("decision") == "accepted":
        errors.append("evaluation.yaml: accepted decision cannot contain hard blockers")

    manifest = documents.get("artifact-manifest.yaml", {})
    manifest_source = manifest.get("source", {}) if manifest else {}
    if manifest_source and not isinstance(manifest_source, dict):
        errors.append("artifact-manifest.yaml: source must be an object")
        manifest_source = {}
    for key in ("repository", "ref", "visual_source_id", "visual_source_revision"):
        if key not in manifest_source or missing_value(manifest_source.get(key)):
            errors.append(f"artifact-manifest.yaml: source.{key} is required")
    if profile_source:
        if manifest_source.get("visual_source_id") != profile_source.get("id"):
            errors.append("visual source mismatch: manifest ID differs from profile/task")
        if manifest_source.get("visual_source_revision") != profile_source.get("revision"):
            errors.append("visual source mismatch: manifest revision differs from profile/task")

    outputs = manifest.get("outputs", {}) if manifest else {}
    task_id = task.get("task", {}).get("id") if task else None
    if not isinstance(outputs, dict) or not outputs:
        errors.append("artifact-manifest.yaml: outputs must be a non-empty object")
    elif not isinstance(task_id, str) or not SAFE_TASK_ID.fullmatch(task_id):
        errors.append("task.yaml: task.id must be a lowercase kebab-case slug")
    else:
        expected_parent = PurePosixPath(".codex") / "artifacts" / task_id
        for name, output in outputs.items():
            output_path = PurePosixPath(output) if isinstance(output, str) else None
            if (
                output_path is None
                or output_path.is_absolute()
                or ".." in output_path.parts
                or output_path.parent != expected_parent
            ):
                errors.append(
                    f"artifact-manifest.yaml: outputs.{name} must be under {expected_parent}"
                )

    if evaluation.get("decision") == "accepted":
        if score_structure_valid:
            if total < 85:
                errors.append("evaluation.yaml: accepted decision requires total >= 85")
            for key in CORE_SCORE_KEYS:
                if scores[key] < 11:
                    errors.append(f"evaluation.yaml: accepted decision requires scores.{key} >= 11")
        approval = manifest.get("approval", {}) if manifest else {}
        if not isinstance(approval, dict):
            errors.append("artifact-manifest.yaml: approval must be an object")
        else:
            approved_by = approval.get("approved_by")
            if not isinstance(approved_by, str) or not approved_by.strip():
                errors.append(
                    "artifact-manifest.yaml: accepted decision requires approval.approved_by "
                    "as a non-empty string"
                )
            if not valid_approval_timestamp(approval.get("approved_at")):
                errors.append(
                    "artifact-manifest.yaml: accepted decision requires approval.approved_at "
                    "as an ISO-8601 timestamp with timezone"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path, help="Directory containing the seven UI specification files")
    args = parser.parse_args()
    errors = validate(args.package)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"OK {args.package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
