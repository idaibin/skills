#!/usr/bin/env python3
"""Run deterministic catalog routing and critical-stop contract cases."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "skills-index.json"
DEFAULT_CASES = ROOT / "evals" / "skill-routing-cases.json"
DEFAULT_SCHEMA = ROOT / "docs" / "skills" / "skill-routing-cases.schema.json"


def load_search_module():
    path = ROOT / "scripts" / "search-skills.py"
    spec = importlib.util.spec_from_file_location("skill_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load_search_module()

STOP_CLASSIFIERS = (
    ("basis-drift", re.compile(r"(?:fixed\s+)?basis\s+(?:sha\s+)?(?:is\s+)?(?:unavailable|changed|drifted)|basis\s+sha\s+is\s+unavailable", re.IGNORECASE)),
    ("strategy-unresolved", re.compile(r"(?:history\s+)?strategy\s+(?:was\s+|is\s+)?(?:not\s+selected|unresolved)|no\s+(?:history\s+)?strategy\s+(?:was\s+|is\s+)?selected", re.IGNORECASE)),
    ("missing-authorization", re.compile(r"authorization\s+(?:to\s+[^,;.]+\s+)?(?:is\s+)?(?:missing|not\s+granted)|not\s+authorized|authorization\s+is\s+not\s+granted", re.IGNORECASE)),
    ("scope-ambiguous", re.compile(r"(?:target\s+)?scope\s+is\s+ambiguous|ambiguous\s+scope", re.IGNORECASE)),
    ("capability-unavailable", re.compile(r"(?:required\s+)?capability\s+is\s+unavailable", re.IGNORECASE)),
    ("out-of-scope-workspace", re.compile(r"outside\s+this\s+workspace|out\s+of\s+scope|cwd\s+differs", re.IGNORECASE)),
    ("provider-unavailable", re.compile(r"provider\s+is\s+unavailable", re.IGNORECASE)),
    ("runtime-unverified", re.compile(r"runtime\s+(?:is\s+)?(?:unverified|not\s+verified)", re.IGNORECASE)),
    ("unsafe-or-destructive", re.compile(r"unsafe\s+or\s+destructive|destructive\s+target", re.IGNORECASE)),
    ("evidence-incomplete", re.compile(r"no\s+authoritative\s+fact\s+source|(?:visual\s+)?source\s+(?:basis\s+)?is\s+(?:unavailable|missing)|required\s+(?:product\s+)?facts\s+are\s+missing|evidence\s+is\s+incomplete", re.IGNORECASE)),
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint(index_path: Path, cases_path: Path) -> str:
    digest = hashlib.sha256()
    for path in (index_path, cases_path):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def classify_stop(prompt: str) -> str | None:
    """Classify an explicit critical-stop condition from the request text."""
    matches = [state for state, pattern in STOP_CLASSIFIERS if pattern.search(prompt)]
    return matches[0] if len(matches) == 1 else None


def validate_case_contract(
    index: dict[str, object], cases: dict[str, object], schema: dict[str, object]
) -> list[str]:
    errors = [
        f"cases schema: {'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            jsonschema.Draft202012Validator(schema).iter_errors(cases),
            key=lambda error: [str(part) for part in error.absolute_path],
        )
    ]
    if errors:
        return errors

    entries = {
        str(entry["name"]): entry for entry in SEARCH.package_entries(index)
    }
    capabilities = {
        str(capability["capability_id"]): capability
        for capability in index.get("capabilities", [])
        if isinstance(capability, dict) and capability.get("capability_id")
    }
    seen_ids: set[str] = set()
    coverage: dict[str, set[str]] = {name: set() for name in entries}
    for case in cases["cases"]:
        case_id = str(case["id"])
        skill = str(case["skill"])
        kind = str(case["class"])
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)
        if skill not in entries:
            errors.append(f"{case_id}: unknown skill {skill}")
            continue
        capability_id = case.get("capability_id")
        if capability_id is not None:
            capability = capabilities.get(str(capability_id))
            if capability is None:
                errors.append(f"{case_id}: unknown capability {capability_id}")
            elif capability.get("package") != skill:
                errors.append(
                    f"{case_id}: capability {capability_id} is owned by {capability.get('package')}, not {skill}"
                )
        coverage[skill].add(kind)
        if kind == "normal" and case["expected_owner"] != skill:
            errors.append(f"{case_id}: normal case must route to its owning skill")
        if kind == "boundary" and case["expected_owner"] == skill:
            errors.append(f"{case_id}: boundary case must reroute to another owner")
        if kind == "critical-stop":
            expected_stop = str(case["expected_stop"])
            if case["expected_owner"] != skill:
                errors.append(f"{case_id}: critical stop must retain its owning skill")
            if expected_stop not in entries[skill]["stop_states"]:
                errors.append(
                    f"{case_id}: stop {expected_stop} is absent from {skill}.stop_states"
                )
    required = {"normal", "boundary", "critical-stop"}
    for skill, kinds in coverage.items():
        if kinds != required:
            errors.append(
                f"{skill}: routing coverage must be {sorted(required)}, found {sorted(kinds)}"
            )
    return errors


def evaluate(
    index: dict[str, object], cases: dict[str, object]
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for case in cases["cases"]:
        kind = str(case["class"])
        failures: list[str] = []
        observed_owner: str | None = None
        observed_stop: str | None = None
        if kind in {"normal", "boundary"}:
            matches = SEARCH.search(index, str(case["prompt"]))
            observed_owner = str(matches[0]["owner"]) if matches else None
            if observed_owner != case["expected_owner"]:
                failures.append(
                    f"expected owner {case['expected_owner']}, observed {observed_owner or 'none'}"
                )
            capability_id = case.get("capability_id")
            if capability_id and matches:
                observed_capabilities = {
                    str(capability.get("capability_id"))
                    for capability in matches[0].get("capabilities", [])
                }
                if capability_id not in observed_capabilities:
                    failures.append(
                        f"expected capability {capability_id}, observed {sorted(observed_capabilities)}"
                    )
        else:
            entry = next(
                item for item in SEARCH.package_entries(index) if item["name"] == case["skill"]
            )
            observed_owner = str(entry["owner"])
            prompt_score, _ = SEARCH.score_entry(entry, str(case["prompt"]))
            if prompt_score <= 0:
                failures.append("critical stop prompt has no owning-skill signal")
            observed_stop = classify_stop(str(case["prompt"]))
            if observed_stop != case["expected_stop"]:
                failures.append(
                    f"expected stop {case['expected_stop']}, observed {observed_stop or 'none'}"
                )
            if case["expected_stop"] not in entry["stop_states"]:
                failures.append(f"missing declared stop {case['expected_stop']}")
        results.append(
            {
                "id": case["id"],
                "case_fingerprint": "sha256:"
                + hashlib.sha256(
                    json.dumps(case, sort_keys=True, ensure_ascii=False).encode("utf-8")
                ).hexdigest(),
                "class": kind,
                "skill": case["skill"],
                "expected_owner": case["expected_owner"],
                "observed_owner": observed_owner,
                "expected_stop": case.get("expected_stop"),
                "observed_stop": observed_stop,
                "status": "passed" if not failures else "failed",
                "failures": failures,
            }
        )
    return results


def regression_errors(
    current: list[dict[str, object]],
    baseline: dict[str, object],
    retired_skills: set[str] | None = None,
) -> list[str]:
    retired_skills = retired_skills or set()
    current_by_id = {str(case["id"]): case for case in current}
    errors: list[str] = []
    old_cases = baseline.get("cases")
    if not isinstance(old_cases, list) or not old_cases:
        return ["baseline is invalid: cases must be a non-empty list"]
    required = {"id", "case_fingerprint", "status", "observed_owner"}
    for position, old in enumerate(old_cases):
        if not isinstance(old, dict) or not required <= set(old):
            errors.append(f"baseline case {position} is missing required result fields")
            continue
        if old.get("status") != "passed":
            continue
        case_id = str(old.get("id"))
        new = current_by_id.get(case_id)
        if new is None:
            if str(old.get("skill")) not in retired_skills:
                errors.append(f"baseline case removed: {case_id}")
        elif new.get("status") != "passed":
            errors.append(f"baseline case regressed: {case_id}")
        elif new.get("case_fingerprint") != old.get("case_fingerprint"):
            errors.append(f"baseline case definition changed: {case_id}")
        elif new.get("observed_owner") != old.get("observed_owner"):
            errors.append(
                f"baseline owner changed: {case_id}: "
                f"{old.get('observed_owner')} -> {new.get('observed_owner')}"
            )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--basis", default="working-tree")
    parser.add_argument("--baseline-report", type=Path)
    parser.add_argument(
        "--baseline-ref",
        help="Read the immutable baseline from <git-ref>:evals/skill-routing-baseline.json",
    )
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def load_baseline(args: argparse.Namespace) -> dict[str, object] | None:
    if args.baseline_ref and args.baseline_report:
        raise ValueError("choose either --baseline-ref or --baseline-report")
    if args.baseline_ref:
        completed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{args.baseline_ref}:evals/skill-routing-baseline.json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)
    return load_json(args.baseline_report) if args.baseline_report else None


def main() -> int:
    args = parse_args()
    index = load_json(args.index)
    cases = load_json(args.cases)
    schema = load_json(args.schema)
    contract_errors = validate_case_contract(index, cases, schema)
    evaluated = [] if contract_errors else evaluate(index, cases)
    baseline = load_baseline(args)
    current_skills = {
        str(entry["name"]) for entry in SEARCH.package_entries(index)
    }
    baseline_skills = {
        str(case["skill"])
        for case in baseline.get("cases", [])
        if isinstance(case, dict) and case.get("skill")
    } if baseline is not None else set()
    candidate_baseline = load_json(ROOT / "evals" / "skill-routing-baseline.json")
    candidate_baseline_skills = {
        str(case["skill"])
        for case in candidate_baseline.get("cases", [])
        if isinstance(case, dict) and case.get("skill")
    }
    retired_skills = (
        (baseline_skills - current_skills)
        & (baseline_skills - candidate_baseline_skills)
    )
    regressions = (
        regression_errors(
            evaluated,
            baseline,
            retired_skills=retired_skills,
        )
        if baseline is not None and not contract_errors
        else []
    )
    failed = [case for case in evaluated if case["status"] == "failed"]
    report = {
        "schema_version": "skill-routing-eval-report/v1",
        "basis": args.basis,
        "fingerprint": fingerprint(args.index, args.cases),
        "summary": {
            "total": len(evaluated),
            "passed": len(evaluated) - len(failed),
            "failed": len(failed),
            "contract_errors": len(contract_errors),
            "regressions": len(regressions),
        },
        "contract_errors": contract_errors,
        "regressions": regressions,
        "cases": evaluated,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.write_report:
        args.write_report.write_text(rendered + "\n", encoding="utf-8")
    if args.json:
        print(rendered)
    else:
        print(
            "skill routing evals: "
            f"{report['summary']['passed']}/{report['summary']['total']} passed; "
            f"contract_errors={len(contract_errors)} regressions={len(regressions)}"
        )
        for error in (*contract_errors, *regressions):
            print(f"ERROR: {error}")
        for case in failed:
            print(f"ERROR: {case['id']}: {'; '.join(case['failures'])}")
    return 1 if contract_errors or regressions or failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
