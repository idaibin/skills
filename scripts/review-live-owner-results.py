#!/usr/bin/env python3
"""Replay an independent review of written deliverables against frozen case criteria."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

from live_owner_fixture import FIXTURES

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/live-agent-cases.json"
spec = importlib.util.spec_from_file_location("live_validator", ROOT / "scripts/validate-live-agent-evals.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case, raw, deliverable, criteria, checks):
    if not isinstance(deliverable, str):
        raise ValueError("deliverable must be text")
    if len(checks) != len(criteria):
        raise ValueError("incomplete criterion review")
    for requirement, check in zip(criteria, checks, strict=True):
        if check["criterion"] != requirement or not check["reason"].strip():
            raise ValueError("missing or mismatched criterion")
        if check["verdict"] not in ("met", "unmet", "unverified"):
            raise ValueError("unknown criterion verdict")
        if check["verdict"] == "met" and not check["quote"].strip():
            raise ValueError("a positive review requires attributable evidence")
        if check["quote"] not in deliverable:
            raise ValueError("attributed evidence does not occur in the deliverable")
    result = copy.deepcopy(raw)
    pending_artifact = raw["status"] == "not-verified" and "owner-artifact-oracle" in raw["not_verified"]
    if raw["status"] != "passed" and not pending_artifact:
        return result
    if pending_artifact:
        result["not_verified"].remove("owner-artifact-oracle")
    verdicts = {check["verdict"] for check in checks}
    if "unmet" in verdicts:
        result["status"] = "failed"
    elif "unverified" in verdicts:
        result["status"] = "not-verified"
        if "owner-artifact-review" not in result.setdefault("not_verified", []):
            result["not_verified"].append("owner-artifact-review")
    else:
        if pending_artifact:
            result["artifacts"].append("owner-result")
            result["process"].append("deliver-owner-output")
            if set(case["required_process"]).issubset(result["process"]):
                result["observations"] = sorted(set(result["observations"]) | {"process", "artifact"})
        result["status"] = "passed"
        # The raw runner defers its final gates while an artifact oracle is missing.
        # Apply those gates again; a positive editorial judgment only supplies the artifact.
        errors = validator.result_errors({"cases": [case]}, {
            "schema_version": validator.RESULT_SCHEMA_VERSION, "case_results": [result]})
        trace = raw["trace"]
        if (errors or trace["exit_code"] != 0 or not trace["write_order_verified"]
                or trace["changed_files"] or trace["forbidden_command_class_hits"]
                or not trace["git"]["ok"] or any(trace["git"]["changed_git_state"].values())):
            result["status"] = "failed"
    return result


def replay(run, review):
    definitions = run / "case-definitions.json"
    fixture_path = run / "owner-fixtures.json"
    cases = {c["id"]: c for c in read(definitions)["cases"]}
    fixtures = read(fixture_path)
    manifest = read(run / "manifest.json")
    if review["manifest_sha256"] != digest(run / "manifest.json"):
        raise ValueError("review belongs to another manifest")
    for key, path in (("cases", definitions), ("owner_fixtures", fixture_path)):
        if manifest["source_hashes"][key] != digest(path):
            raise ValueError("case definitions or reviewer criteria drifted")
    raw = read(run / "results.json")
    ids = manifest["selected_case_ids"]
    if (ids != raw["selected_case_ids"] or len(set(ids)) != len(ids)
            or ids != [r["case_id"] for r in raw["case_results"]] or set(ids) != set(review["cases"])):
        raise ValueError("review and raw result inventory differ")
    graded = []
    for original in raw["case_results"]:
        key = original["case_id"]
        folder = run / "cases" / key
        entry = review["cases"][key]
        files = ("result.json", "last-message.json", "input.txt", "trace.jsonl")
        if entry["sha256"] != {name: digest(folder / name) for name in files}:
            raise ValueError(f"{key}: evidence changed after review")
        if read(folder / "result.json") != original:
            raise ValueError(f"{key}: raw summary does not match case")
        final = read(folder / "last-message.json")
        with (folder / "trace.jsonl").open() as trace:
            messages = [event["item"]["text"] for line in trace if line.strip()
                        for event in [json.loads(line)] if event.get("type") == "item.completed"
                        and event.get("item", {}).get("type") == "agent_message"]
        if not messages or json.loads(messages[-1]) != final:
            raise ValueError(f"{key}: deliverable does not match the terminal trace")
        result = evaluate(cases[key], original, final["deliverable"], fixtures[key]["review"], entry["checks"])
        if fixtures[key].get("graph") and result["status"] == "passed":
            _, separator, body = (folder / "input.txt").read_text().partition("\nFixed graph receipt:\n")
            receipt = json.loads(body) if separator else {}
            if (not receipt.get("snapshot", {}).get("snapshot_ref")
                    or receipt.get("validation", {}).get("valid") is not True
                    or not receipt.get("assets")):
                raise ValueError(f"{key}: a positive map review requires a validated snapshot and query")
        graded.append(result)
    return {**raw, "case_results": graded}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("review", type=Path, help="independently prepared local review receipt")
    args = parser.parse_args()
    payload = replay(args.run, read(args.review))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r["status"] == "passed" for r in payload["case_results"]) else 1)
