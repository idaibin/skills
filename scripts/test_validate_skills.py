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
            'interface:\n  display_name: "Sample"\n  short_description: "Process samples"\n'
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
