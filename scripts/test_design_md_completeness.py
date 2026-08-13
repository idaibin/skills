#!/usr/bin/env python3
"""Deterministic policy tests for adopted DESIGN.md completeness."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ui-spec" / "scripts" / "validate-design-md-completeness.py"
FIXTURES = ROOT / "scripts" / "fixtures" / "design-md-completeness"
SPEC = importlib.util.spec_from_file_location("design_md_completeness", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

SOURCE_ARTIFACT = FIXTURES / "source-evidence.txt"
SOURCE_HASH = CHECKER.sha256(SOURCE_ARTIFACT)
def lint_pass(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    raw = text.split("---", 2)[1]
    parsed = yaml.safe_load(raw)
    return {"findings": [], "summary": {"errors": 0, "warnings": 0, "infos": 0}, "parsed": parsed}


def evaluate(path: Path, *, stage: str = "candidate", shared: str = "present", approval=None):
    approval_path = None
    approval_hash = None
    if stage == "adopted":
        temporary = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        approval_path = Path(temporary.name)
        temporary.close()
        approval_path.write_text(json.dumps({
            "status": "approved", "design_sha256": approval,
            "approved_by_id": "design-owner", "proposer_id": "spec-author",
            "implementer_id": "frontend-owner",
        }), encoding="utf-8")
        approval_hash = CHECKER.sha256(approval_path)
    try:
        return CHECKER.evaluate_document(
            path,
            stage=stage,
            shared_components=shared,
            source_ref="selected-source:fixture",
            source_artifact=SOURCE_ARTIFACT,
            source_sha256=SOURCE_HASH,
            source_status="approved",
            approval_design_sha256=None,
            approved_by=None,
            proposer=None,
            implementer=None,
            official_lint=lint_pass(path),
            official_status=0,
            lint_command="official-lint-fixture",
            approval_record=approval_path,
            approval_record_sha256=approval_hash,
        )
    finally:
        if approval_path:
            approval_path.unlink(missing_ok=True)


class DesignMdCompletenessTests(unittest.TestCase):
    def status(self, result):
        return result["shared_authority_completeness"]["status"]

    def errors(self, result):
        return result["shared_authority_completeness"]["errors"]

    def test_complete_first_adoption_is_ready_for_human_approval(self) -> None:
        result = evaluate(FIXTURES / "complete.md")
        self.assertEqual("ready-for-human-approval", self.status(result))
        self.assertEqual([], self.errors(result))

    def test_adopted_result_requires_exact_design_hash_approval(self) -> None:
        path = FIXTURES / "complete.md"
        result = evaluate(path, stage="adopted", approval=CHECKER.sha256(path))
        self.assertEqual("awaiting-trusted-approval-verification", self.status(result))

    def test_reasoned_omissions_pass_when_no_shared_components_exist(self) -> None:
        result = evaluate(FIXTURES / "omitted.md", shared="absent")
        self.assertEqual("ready-for-human-approval", self.status(result))

    def test_prose_only_officially_valid_document_is_not_ready(self) -> None:
        result = evaluate(FIXTURES / "prose-only.md", shared="present")
        self.assertEqual("not-ready", self.status(result))
        self.assertIn("H2 sections must be the eight canonical headings in canonical order", self.errors(result))
        self.assertIn("colors requires machine tokens or omitted+reason", self.errors(result))

    def mutate(self, source: str, transform) -> Path:
        content = (FIXTURES / source).read_text(encoding="utf-8")
        temporary = tempfile.NamedTemporaryFile(suffix=".md", delete=False)
        path = Path(temporary.name)
        temporary.close()
        path.write_text(transform(content), encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_empty_omitted_reason_fails(self) -> None:
        path = self.mutate("omitted.md", lambda text: text.replace(
            'reason: "This identity has no shared spacing scale; each accepted feature owns layout spacing."',
            'reason: ""',
        ))
        self.assertIn("omitted.spacing requires a concrete non-empty reason", self.errors(evaluate(path, shared="absent")))

    def test_unknown_h2_cannot_replace_canonical_h2(self) -> None:
        path = self.mutate("complete.md", lambda text: text.replace("## Shapes", "## Shape Language"))
        self.assertEqual("not-ready", self.status(evaluate(path)))

    def test_canonical_h2_order_is_required(self) -> None:
        def swap(text: str) -> str:
            colors = text.index("## Colors")
            typography = text.index("## Typography")
            layout = text.index("## Layout")
            return text[:colors] + text[typography:layout] + text[colors:typography] + text[layout:]
        self.assertEqual("not-ready", self.status(evaluate(self.mutate("complete.md", swap))))

    def test_component_omission_fails_when_shared_consumers_exist(self) -> None:
        result = evaluate(FIXTURES / "omitted.md", shared="present")
        self.assertIn("shared component consumers exist, so component token entries are required", self.errors(result))

    def test_token_group_without_prose_binding_fails(self) -> None:
        path = self.mutate(
            "complete.md",
            lambda text: text.replace("`primary`", "the main color", 1).replace(
                "`surface`", "the page background", 1
            ),
        )
        self.assertIn("Colors must bind prose to every `colors` token name: primary, surface", self.errors(evaluate(path)))

    def test_stale_approval_hash_fails(self) -> None:
        result = evaluate(FIXTURES / "complete.md", stage="adopted", approval="b" * 64)
        self.assertIn("human approval record must bind the exact current DESIGN.md SHA-256", self.errors(result))

    def test_source_hash_must_bind_source_artifact_bytes(self) -> None:
        result = CHECKER.evaluate_document(
            FIXTURES / "complete.md",
            stage="candidate",
            shared_components="present",
            source_ref="selected-source:fixture",
            source_artifact=SOURCE_ARTIFACT,
            source_sha256="a" * 64,
            source_status="approved",
            approval_design_sha256=None,
            approved_by=None,
            proposer=None,
            implementer=None,
            official_lint=lint_pass(FIXTURES / "complete.md"),
            official_status=0,
            lint_command="official-lint-fixture",
        )
        self.assertIn(
            "approved visual/source evidence SHA-256 must match source artifact bytes",
            self.errors(result),
        )

    def test_starter_placeholders_fail_even_with_tokens(self) -> None:
        path = self.mutate(
            "complete.md",
            lambda text: text.replace("name: Complete Example", "name: Replace with accepted name"),
        )
        self.assertIn(
            "frontmatter name must replace the starter placeholder", self.errors(evaluate(path))
        )

    def test_token_dump_and_empty_canonical_sections_fail(self) -> None:
        path = self.mutate(
            "complete.md",
            lambda text: re.sub(
                r"## (Overview|Elevation & Depth|Do's and Don'ts)\n.*?(?=\n## |\Z)",
                lambda match: f"## {match.group(1)}\n\n",
                text,
                flags=re.DOTALL,
            ),
        )
        result = evaluate(path)
        self.assertIn("Overview requires non-placeholder application semantics", self.errors(result))
        self.assertEqual("not-ready", self.status(result))

    def test_fenced_token_names_do_not_bind_unrelated_prose(self) -> None:
        path = self.mutate(
            "complete.md",
            lambda text: re.sub(
                r"## Colors\n.*?(?=\n## Typography)",
                "## Colors\n\nThis paragraph discusses a generic interface without assigning any named semantic role to an actual token in the product.\n\n```text\n`primary` `surface`\n```\n",
                text,
                flags=re.DOTALL,
            ),
        )
        self.assertIn(
            "Colors must bind prose to every `colors` token name: primary, surface",
            self.errors(evaluate(path)),
        )

    def test_approval_record_identity_normalization_blocks_collision(self) -> None:
        path = FIXTURES / "complete.md"
        temporary = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        record = Path(temporary.name)
        temporary.close()
        record.write_text(json.dumps({
            "status": "approved", "design_sha256": CHECKER.sha256(path),
            "approved_by_id": "Frontend-Owner ", "proposer_id": "spec-author",
            "implementer_id": "frontend-owner",
        }), encoding="utf-8")
        self.addCleanup(record.unlink, missing_ok=True)
        result = CHECKER.evaluate_document(
            path, stage="adopted", shared_components="present",
            source_ref="selected-source:fixture", source_artifact=SOURCE_ARTIFACT,
            source_sha256=SOURCE_HASH, source_status="approved",
            approval_design_sha256=None, approved_by=None, proposer=None, implementer=None,
            official_lint=lint_pass(path), official_status=0,
            lint_command="official-lint-fixture", approval_record=record,
            approval_record_sha256=CHECKER.sha256(record),
        )
        self.assertIn("human approver, proposer, and implementer identities must be distinct", self.errors(result))

    def test_official_flow_mapping_is_not_rejected_by_policy_parser(self) -> None:
        path = self.mutate(
            "complete.md",
            lambda text: text.replace(
                'colors:\n  primary: "#1A1C1E"\n  surface: "#F7F5F2"',
                'colors: {primary: "#1A1C1E", surface: "#F7F5F2"}',
            ),
        )
        lint, status, command = CHECKER.run_official_lint(path.read_bytes())
        result = CHECKER.evaluate_document(
            path, stage="candidate", shared_components="present",
            source_ref="selected-source:fixture", source_artifact=SOURCE_ARTIFACT,
            source_sha256=SOURCE_HASH, source_status="approved",
            approval_design_sha256=None, approved_by=None, proposer=None, implementer=None,
            official_lint=lint, official_status=status, lint_command=command,
        )
        self.assertEqual("ready-for-human-approval", self.status(result))

    def test_main_rejects_source_artifact_drift(self) -> None:
        design = self.mutate("complete.md", lambda text: text)
        source = self.mutate("source-evidence.txt", lambda text: text)
        original_lint = CHECKER.run_official_lint

        def mutate_after_snapshot(raw):
            result = original_lint(raw)
            source.write_text("changed source bytes", encoding="utf-8")
            return result

        argv = [
            "checker", str(design), "--stage", "candidate", "--shared-components", "present",
            "--source-ref", "selected-source:test", "--source-artifact", str(source),
            "--source-sha256", CHECKER.sha256(source), "--source-status", "approved",
        ]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(CHECKER, "run_official_lint", mutate_after_snapshot):
            self.assertEqual(2, CHECKER.main())


if __name__ == "__main__":
    unittest.main()
