#!/usr/bin/env python3
"""Executable contract regressions for repo-review portable request/results."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).parent.parent
SCHEMAS = ROOT / "docs" / "skills" / "schemas"
REQUEST_SCHEMA = json.loads((SCHEMAS / "review-request.v1.schema.json").read_text(encoding="utf-8"))
FINDINGS_SCHEMA = json.loads((SCHEMAS / "review-findings.v1.schema.json").read_text(encoding="utf-8"))
ASSET_MAP_SCHEMA = json.loads((SCHEMAS / "asset-map-result.v1.schema.json").read_text(encoding="utf-8"))


def valid_request() -> dict:
    return {
        "schema_version": "1.0",
        "capability_id": "repository.change.review",
        "capability_version": "1.0.0",
        "review_id": "review:fixture",
        "basis": {
            "mode": "fixed-range",
            "repository_id": "fixture",
            "base_sha": "1" * 40,
            "head_sha": "2" * 40,
        },
        "scope": {
            "changed_paths": ["src/example.ts"],
            "included_paths": ["src/**"],
            "excluded_paths": ["dist/**"],
        },
        "authorities": {
            "standards_refs": ["AGENTS.md"],
            "spec_refs": ["REQ-FIXTURE-001"],
            "acceptance_refs": ["AC-FIXTURE-001"],
        },
        "graph_context": {
            "snapshot_ref": "scan:fixture",
            "impact_query_refs": ["query:impact:fixture"],
            "allowed_paths": ["src/**", "tests/**"],
            "unresolved": [],
        },
    }


def valid_noop_findings() -> dict:
    return {
        "schema_version": "1.0",
        "capability_id": "repository.change.review",
        "capability_version": "1.0.0",
        "review_id": "review:fixture",
        "basis": {"mode": "fixed-range", "base_sha": "1" * 40, "head_sha": "2" * 40},
        "verdict": "pass",
        "finding_count": 0,
        "blocking_count": 0,
        "findings": [],
        "scope_assessment": {
            "status": "within-scope",
            "changed_paths": ["src/example.ts"],
            "allowed_paths": ["src/**", "tests/**"],
            "violations": [],
            "graph_snapshot_ref": "scan:fixture",
            "limitations": [],
        },
        "spec_assessment": {
            "status": "not-verified",
            "acceptance_refs": [],
            "uncovered_refs": [],
            "limitations": ["No trustworthy specification was supplied."],
        },
        "checks": [{"name": "unit", "status": "pass", "evidence": "command exited 0"}],
        "limitations": [],
    }


class ReviewContractTests(unittest.TestCase):
    def test_request_and_noop_result_validate(self) -> None:
        jsonschema.Draft202012Validator(REQUEST_SCHEMA).validate(valid_request())
        jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(valid_noop_findings())

    def test_fixed_range_requires_both_shas(self) -> None:
        request = valid_request()
        del request["basis"]["base_sha"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(REQUEST_SCHEMA).validate(request)

    def test_absolute_and_parent_escaping_paths_fail(self) -> None:
        for unsafe in ("/tmp/example.ts", "../example.ts", "src/../example.ts", "C:\\example.ts"):
            with self.subTest(path=unsafe):
                request = valid_request()
                request["scope"]["changed_paths"] = [unsafe]
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.Draft202012Validator(REQUEST_SCHEMA).validate(request)

    def test_finding_requires_line_anchor_quote_and_remediation(self) -> None:
        result = valid_noop_findings()
        result.update({
            "verdict": "gap",
            "finding_count": 1,
            "blocking_count": 1,
            "findings": [{
                "finding_id": "finding:fixture",
                "severity": "P1",
                "title": "Scope escape",
                "path": "src/example.ts",
                "line_start": 10,
                "line_end": 12,
                "quote": "unsafe();",
                "axes": ["scope", "standards"],
                "impact": "The change reaches an undeclared owner.",
                "remediation": "Expand the authorized task or revert the path.",
                "evidence_status": "verified",
            }],
        })
        jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(result)
        for required in ("line_start", "line_end", "quote", "remediation"):
            invalid = copy.deepcopy(result)
            del invalid["findings"][0][required]
            with self.subTest(required=required), self.assertRaises(jsonschema.ValidationError):
                jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(invalid)

    def test_impact_query_envelope_validates(self) -> None:
        result = {
            "schema_version": "1.0",
            "capability_id": "repository.asset.query",
            "capability_version": "1.0.0",
            "repository_id": "fixture",
            "snapshot_ref": "scan:fixture",
            "basis": {"head_sha": "1" * 40, "worktree_state": "clean"},
            "scope": {"includes": ["src/**"], "exclusions": []},
            "coverage": {"files_scanned": 1},
            "query": {
                "kind": "impact",
                "root_asset_id": "asset:fixture",
                "direction": "both",
                "depth": 3,
                "relation_filters": [],
            },
            "assets": [{"asset_id": "asset:fixture"}],
            "relations": [],
            "validation": {"valid": True, "issues": []},
        }
        jsonschema.Draft202012Validator(ASSET_MAP_SCHEMA).validate(result)

    def test_pass_cannot_hide_blocking_or_scope_failure(self) -> None:
        for mutation in ("blocking", "scope", "spec"):
            with self.subTest(mutation=mutation):
                result = valid_noop_findings()
                if mutation == "blocking":
                    result["blocking_count"] = 1
                elif mutation == "scope":
                    result["scope_assessment"].update({"status": "out-of-scope", "violations": ["outside.ts"]})
                else:
                    result["spec_assessment"].update({"status": "unsatisfied", "uncovered_refs": ["AC-1"]})
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(result)

    def test_scope_and_spec_status_require_consistent_gaps(self) -> None:
        result = valid_noop_findings()
        result["verdict"] = "gap"
        result["scope_assessment"]["status"] = "out-of-scope"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(result)
        result = valid_noop_findings()
        result["verdict"] = "gap"
        result["spec_assessment"]["status"] = "unsatisfied"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(FINDINGS_SCHEMA).validate(result)


if __name__ == "__main__":
    unittest.main()
