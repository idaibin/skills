#!/usr/bin/env python3
"""Validate the required shape and cross-file identity of a UI design package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as error:  # pragma: no cover - host dependency boundary
    raise SystemExit("PyYAML is required: install it in the active project environment") from error


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "assets" / "ui-package.schema.json"


def load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    documents: dict[str, Any] = {}
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    file_schemas = schema["properties"]
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

    task = documents.get("task.yaml", {})
    if task and not task.get("scope", {}).get("exclude"):
        errors.append("task.yaml: scope.exclude must declare a boundary")
    if task and not task.get("facts", {}).get("unavailable"):
        errors.append("task.yaml: facts.unavailable must declare non-capabilities")

    evaluation = documents.get("evaluation.yaml", {})
    scores = evaluation.get("scores", {}) if evaluation else {}
    if scores and not isinstance(scores, dict):
        errors.append("evaluation.yaml: scores must be an object")
    elif scores:
        numeric_scores = [value for value in scores.values() if isinstance(value, (int, float)) and not isinstance(value, bool)]
        if len(numeric_scores) != len(scores):
            errors.append("evaluation.yaml: every score must be numeric")
        elif sum(numeric_scores) != evaluation.get("total"):
            errors.append("evaluation.yaml: total must equal the weighted score sum")
    if evaluation.get("hard_blockers") and evaluation.get("decision") == "accepted":
        errors.append("evaluation.yaml: accepted decision cannot contain hard blockers")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path, help="Directory containing the seven UI package files")
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
