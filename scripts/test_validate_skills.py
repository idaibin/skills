#!/usr/bin/env python3
"""Focused regressions for validate-skills.py."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        package = root / "skills" / "sample-skill"
        (package / "references").mkdir(parents=True)
        (package / "agents").mkdir()
        (package / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Use when a sample needs processing.\n---\n"
            "# Sample\n\nSee [usage](references/usage.md) and "
            "[evals](references/eval-cases.md).\n",
            encoding="utf-8",
        )
        (package / "references" / "usage.md").write_text("# Usage\n", encoding="utf-8")
        (package / "references" / "eval-cases.md").write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "## Quality Eval\n\n- three\n",
            encoding="utf-8",
        )
        (package / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "Sample"\n'
            '  short_description: "Process representative samples"\n'
            '  default_prompt: "Use $sample-skill for this task."\n',
            encoding="utf-8",
        )
        (root / "skills.sh.json").write_text(
            json.dumps({"groupings": [{"skills": ["sample-skill"]}]}), encoding="utf-8"
        )
        (root / "README.md").write_text(
            "| Skill | Use when |\n| --- | --- |\n| `sample-skill` | sample |\n", encoding="utf-8"
        )
        (root / "INSTALL.md").write_text("- `skills/sample-skill`\n", encoding="utf-8")
        return root

    def test_valid_repository(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.make_repo()))

    def test_name_must_match_directory(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text().replace("name: sample-skill", "name: other-skill"))
        self.assertTrue(any("name must match" in error for error in VALIDATOR.validate(root)))

    def test_broken_local_link_fails(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text() + "\n[missing](references/missing.md)\n")
        self.assertTrue(any("broken link" in error for error in VALIDATOR.validate(root)))

    def test_eval_requires_three_scenarios(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(evals.read_text().replace("## Quality Eval", "## Examples"))
        self.assertTrue(any("Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_sections_must_have_content(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(evals.read_text().replace("## Quality Eval\n\n- three", "## Quality Eval"))
        self.assertTrue(any("empty ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_must_be_exact(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "## Quality Eval Notes\n\n- not the required section\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_outside_code_fence(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "```text\n## Quality Eval\n```\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_outside_tilde_fence(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "~~~text\n## Quality Eval\n~~~\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_inside_indented_code(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "    ## Quality Eval\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_package_install_command_fails(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text("Run npx skills add example/repo\n")
        self.assertTrue(any("installation commands" in error for error in VALIDATOR.validate(root)))

    def test_catalog_sets_must_match(self) -> None:
        root = self.make_repo()
        (root / "skills.sh.json").write_text(json.dumps({"groupings": []}))
        self.assertTrue(any("skills.sh.json package set differs" in error for error in VALIDATOR.validate(root)))

    def test_openai_metadata_requires_interface_root(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text().replace("interface:", "wrong_root:"))
        self.assertTrue(any("interface mapping" in error for error in VALIDATOR.validate(root)))

    def test_openai_short_description_length_is_checked(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text().replace("Process representative samples", "Too short"))
        self.assertTrue(any("25-64 characters" in error for error in VALIDATOR.validate(root)))

    def test_openai_explicit_only_policy_is_valid(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + "policy:\n  allow_implicit_invocation: false\n",
            encoding="utf-8",
        )
        self.assertEqual([], VALIDATOR.validate(root))

    def test_openai_invocation_policy_requires_boolean(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + 'policy:\n  allow_implicit_invocation: "false"\n',
            encoding="utf-8",
        )
        self.assertTrue(
            any("allow_implicit_invocation must be a boolean" in error for error in VALIDATOR.validate(root))
        )

    def test_openai_invocation_policy_rejects_null_value(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + "policy:\n  allow_implicit_invocation:\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any("allow_implicit_invocation must be a boolean" in error for error in VALIDATOR.validate(root))
        )

    def test_openai_invocation_policy_rejects_null_mapping(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text() + "policy:\n", encoding="utf-8")
        self.assertTrue(
            any("top-level policy must be a mapping" in error for error in VALIDATOR.validate(root))
        )

    def test_unknown_frontmatter_field_fails(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text().replace("name: sample-skill", "name: sample-skill\nowner: team"))
        self.assertTrue(any("unsupported frontmatter" in error for error in VALIDATOR.validate(root)))

    def test_portable_optional_fields_are_typed(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text().replace(
                "name: sample-skill",
                "name: sample-skill\ncompatibility: 42\nmetadata:\n  version: 1",
            )
        )
        errors = VALIDATOR.validate(root)
        self.assertTrue(any("compatibility" in error for error in errors))
        self.assertTrue(any("metadata must map strings to strings" in error for error in errors))

    def test_long_reference_requires_contents(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text("# Usage\n" + "detail\n" * 101)
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_exact_contents_heading(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "## Contents List\n\n- item one\n- item two\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_contents_outside_fence(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "```text\n## Contents\n\n- item one\n```\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_contents_tilde_fence(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "~~~text\n## Contents\n\n- item one\n~~~\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_contents_in_indented_code(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "    ## Contents\n\n- item one\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_block_scalar_description_is_valid(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text().replace(
                "description: Use when a sample needs processing.",
                "description: |\n  Use when a sample needs processing.\n  Handles a representative input.",
            )
        )
        self.assertEqual([], VALIDATOR.validate(root))


if __name__ == "__main__":
    unittest.main()
