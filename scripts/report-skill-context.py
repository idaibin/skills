#!/usr/bin/env python3
"""Report deterministic Skill entrypoint and direct-reference context estimates."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\((references/[^)#]+)(?:#[^)]+)?\)")
ENTRYPOINT_WARNING_TOKENS = 4_000
REFERENCE_WARNING_TOKENS = 8_000


def estimated_tokens(text: str) -> int:
    """Return a model-neutral, deterministic character-based estimate.

    This is a budgeting signal, not a tokenizer claim. Four Unicode code points per
    token keeps the report portable while host/model canaries retain final authority.
    """
    return math.ceil(len(text) / 4)


def package_report(package: Path) -> dict[str, object]:
    entrypoint = package / "SKILL.md"
    text = entrypoint.read_text(encoding="utf-8")
    linked = sorted(set(LINK_RE.findall(text)))
    references: list[dict[str, object]] = []
    for relative in linked:
        path = package / relative
        if not path.is_file():
            continue
        reference_text = path.read_text(encoding="utf-8")
        references.append(
            {
                "path": relative,
                "characters": len(reference_text),
                "estimated_tokens": estimated_tokens(reference_text),
                "runtime_candidate": Path(relative).name != "eval-cases.md",
            }
        )
    runtime_references = [item for item in references if item["runtime_candidate"]]
    entry_tokens = estimated_tokens(text)
    largest = max(
        (int(item["estimated_tokens"]) for item in runtime_references), default=0
    )
    warnings: list[str] = []
    if entry_tokens > ENTRYPOINT_WARNING_TOKENS:
        warnings.append(
            f"entrypoint estimate {entry_tokens} exceeds warning {ENTRYPOINT_WARNING_TOKENS}"
        )
    if largest > REFERENCE_WARNING_TOKENS:
        warnings.append(
            f"largest direct runtime reference estimate {largest} exceeds warning "
            f"{REFERENCE_WARNING_TOKENS}"
        )
    return {
        "skill": package.name,
        "entrypoint_characters": len(text),
        "entrypoint_estimated_tokens": entry_tokens,
        "direct_reference_count": len(references),
        "runtime_reference_count": len(runtime_references),
        "declared_runtime_closure_estimated_tokens": entry_tokens
        + sum(int(item["estimated_tokens"]) for item in runtime_references),
        "largest_runtime_reference_estimated_tokens": largest,
        "warnings": warnings,
        "references": references,
    }


def catalog_report(root: Path) -> dict[str, object]:
    packages = sorted(
        path
        for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    reports = [package_report(package) for package in packages]
    return {
        "schema_version": "skill-context-report/v1",
        "estimator": "unicode-characters-divided-by-4",
        "evidence_boundary": (
            "Declared closure is the sum of directly linked runtime-candidate references; "
            "it is not proof that a host loads them together or an exact model token count."
        ),
        "thresholds": {
            "entrypoint_warning_tokens": ENTRYPOINT_WARNING_TOKENS,
            "reference_warning_tokens": REFERENCE_WARNING_TOKENS,
        },
        "summary": {
            "skills": len(reports),
            "warnings": sum(len(item["warnings"]) for item in reports),
        },
        "skills": reports,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = catalog_report(args.root.resolve())
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.write_report:
        args.write_report.write_text(rendered + "\n", encoding="utf-8")
    if args.json:
        print(rendered)
    else:
        print(
            f"skill context report: {report['summary']['skills']} skills; "
            f"warnings={report['summary']['warnings']}"
        )
        for package in report["skills"]:
            for warning in package["warnings"]:
                print(f"WARN: {package['skill']}: {warning}")
    return 1 if args.fail_on_warning and report["summary"]["warnings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
