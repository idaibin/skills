#!/usr/bin/env python3
"""Focused regressions for the ui-spec artifact validator."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ui-spec" / "scripts" / "validate_ui_spec.py"
TEMPLATES = ROOT / "skills" / "ui-spec" / "assets" / "templates"
SPEC = importlib.util.spec_from_file_location("validate_ui_spec", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class UiSpecValidatorTests(unittest.TestCase):
    def make_package(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        package = Path(temporary.name) / "package"
        shutil.copytree(TEMPLATES, package)
        return package

    def load_yaml(self, package: Path, name: str) -> dict:
        return yaml.safe_load((package / name).read_text(encoding="utf-8"))

    def write_yaml(self, package: Path, name: str, document: dict) -> None:
        (package / name).write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    def mark_accepted(self, package: Path) -> None:
        evaluation = self.load_yaml(package, "evaluation.yaml")
        evaluation["scores"] = {
            "product_truth": 15,
            "source_fidelity": 15,
            "information_architecture": 10,
            "interaction_states": 15,
            "responsive_accessibility": 15,
            "component_token_mapping": 15,
            "engineering_fit": 10,
            "evidence": 5,
        }
        evaluation["total"] = 100
        evaluation["decision"] = "accepted"
        self.write_yaml(package, "evaluation.yaml", evaluation)

    def test_templates_are_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.make_package()))

    def test_empty_selected_source_fails(self) -> None:
        package = self.make_package()
        profile = self.load_yaml(package, "profile.yaml")
        profile["visual_source"] = {}
        self.write_yaml(package, "profile.yaml", profile)
        self.assertTrue(any("visual_source.id" in error for error in VALIDATOR.validate(package)))

    def test_source_revision_mismatch_fails(self) -> None:
        package = self.make_package()
        task = self.load_yaml(package, "task.yaml")
        task["visual_source"]["revision"] = "different-revision"
        self.write_yaml(package, "task.yaml", task)
        self.assertTrue(any("differ on revision" in error for error in VALIDATOR.validate(package)))

    def test_accepted_without_approval_fails(self) -> None:
        package = self.make_package()
        self.mark_accepted(package)
        errors = VALIDATOR.validate(package)
        self.assertTrue(any("approval.approved_by" in error for error in errors))
        self.assertTrue(any("approval.approved_at" in error for error in errors))

    def test_accepted_approval_requires_identity_and_timestamp(self) -> None:
        invalid_approvals = (
            {"approved_by": " ", "approved_at": "2026-07-22T10:00:00+08:00"},
            {"approved_by": 1, "approved_at": "2026-07-22T10:00:00+08:00"},
            {"approved_by": "design-owner", "approved_at": False},
            {"approved_by": "design-owner", "approved_at": "not-a-timestamp"},
            {"approved_by": "design-owner", "approved_at": "2026-07-22T10:00:00"},
        )
        for approval in invalid_approvals:
            with self.subTest(approval=approval):
                package = self.make_package()
                self.mark_accepted(package)
                manifest = self.load_yaml(package, "artifact-manifest.yaml")
                manifest["approval"] = approval
                self.write_yaml(package, "artifact-manifest.yaml", manifest)
                self.assertTrue(VALIDATOR.validate(package))

        package = self.make_package()
        self.mark_accepted(package)
        manifest = self.load_yaml(package, "artifact-manifest.yaml")
        manifest["approval"] = {
            "approved_by": "design-owner",
            "approved_at": "2026-07-22T10:00:00+08:00",
        }
        self.write_yaml(package, "artifact-manifest.yaml", manifest)
        self.assertEqual([], VALIDATOR.validate(package))

    def test_outputs_must_use_task_specific_directory(self) -> None:
        package = self.make_package()
        manifest = self.load_yaml(package, "artifact-manifest.yaml")
        manifest["outputs"]["task"] = ".codex/artifacts/ui-spec/task.yaml"
        self.write_yaml(package, "artifact-manifest.yaml", manifest)
        self.assertTrue(any("outputs.task" in error for error in VALIDATOR.validate(package)))

    def test_unsafe_task_ids_fail(self) -> None:
        for task_id in ("../../src", "/private/tmp/spec", "nested/spec"):
            with self.subTest(task_id=task_id):
                package = self.make_package()
                task = self.load_yaml(package, "task.yaml")
                task["task"]["id"] = task_id
                self.write_yaml(package, "task.yaml", task)
                self.assertTrue(any("kebab-case slug" in error for error in VALIDATOR.validate(package)))

    def test_visual_source_boundaries_require_non_empty_strings(self) -> None:
        for bad_item in (None, "", {"unexpected": "object"}):
            with self.subTest(bad_item=bad_item):
                package = self.make_package()
                profile = self.load_yaml(package, "profile.yaml")
                profile["visual_source"]["use"] = [bad_item]
                self.write_yaml(package, "profile.yaml", profile)
                self.assertTrue(any("use[0]" in error for error in VALIDATOR.validate(package)))

    def test_score_contract_rejects_extra_overflow_and_wrong_types(self) -> None:
        mutations = (
            ("bonus", 1, "score keys must match rubric"),
            ("product_truth", 16, "must be between 0 and 15"),
            ("product_truth", "15", "scores.product_truth must be numeric"),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key, value=value):
                package = self.make_package()
                evaluation = self.load_yaml(package, "evaluation.yaml")
                evaluation["scores"][key] = value
                self.write_yaml(package, "evaluation.yaml", evaluation)
                self.assertTrue(any(expected in error for error in VALIDATOR.validate(package)))

        package = self.make_package()
        evaluation = self.load_yaml(package, "evaluation.yaml")
        evaluation["total"] = "85"
        evaluation["decision"] = "accepted"
        self.write_yaml(package, "evaluation.yaml", evaluation)
        errors = VALIDATOR.validate(package)
        self.assertTrue(any("total must be numeric" in error for error in errors))

    def test_different_task_ids_use_distinct_directories(self) -> None:
        parents = set()
        for task_id in ("account-settings-spec", "billing-flow-spec"):
            package = self.make_package()
            task = self.load_yaml(package, "task.yaml")
            task["task"]["id"] = task_id
            self.write_yaml(package, "task.yaml", task)
            manifest = self.load_yaml(package, "artifact-manifest.yaml")
            for name, output in manifest["outputs"].items():
                manifest["outputs"][name] = str(Path(".codex/artifacts") / task_id / Path(output).name)
            self.write_yaml(package, "artifact-manifest.yaml", manifest)
            self.assertEqual([], VALIDATOR.validate(package))
            parents.add(Path(manifest["outputs"]["task"]).parent)
        self.assertEqual(2, len(parents))


if __name__ == "__main__":
    unittest.main()
