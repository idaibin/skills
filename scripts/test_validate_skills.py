#!/usr/bin/env python3
"""Focused regressions for validate-skills.py."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-skills.py")
ROOT = SCRIPT.parent.parent
INDEX_SCHEMA = SCRIPT.parent.parent / "docs" / "skills" / "skills-index.schema.json"
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
            json.dumps({"groupings": [{"title": "Samples", "skills": ["sample-skill"]}]}),
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "| Skill | Use when |\n| --- | --- |\n| `sample-skill` | sample |\n", encoding="utf-8"
        )
        (root / "INSTALL.md").write_text("- `skills/sample-skill`\n", encoding="utf-8")
        index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
        (root / "docs" / "skills").mkdir(parents=True)
        (root / "docs" / "skills" / "skills-index.schema.json").write_text(
            json.dumps(index_schema), encoding="utf-8"
        )
        (root / "skills-index.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "description": "Fixture discovery index.",
                    "categories": {
                        "samples": {
                            "title": "Samples",
                            "description": "Sample processing.",
                        }
                    },
                    "skills": [
                        {
                            "name": "sample-skill",
                            "category": "samples",
                            "intents": ["process a sample"],
                            "keywords": ["sample"],
                            "excludes": ["unrelated work"],
                            "related": [],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return root

    def test_valid_repository(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.make_repo()))

    def test_ask_ai_defaults_require_persistent_context_fallback_contract(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        package = Path(temporary.name) / "ask-ai"
        (package / "references").mkdir(parents=True)
        profile = package / "references" / "browser-profile.md"
        profile.write_text(
            "review_context:\n  name: <user-editable default persistent context name>\n"
            "  policy: prefer-verified-persistent\n"
            "  fallback: new-standard-chat\n",
            encoding="utf-8",
        )
        self.assertEqual([], VALIDATOR.ask_ai_defaults_errors(package))
        profile.write_text("review_context:\n", encoding="utf-8")
        errors = VALIDATOR.ask_ai_defaults_errors(package)
        self.assertTrue(any("user-editable default" in error for error in errors))
        self.assertTrue(any("prefer-verified-persistent" in error for error in errors))
        self.assertTrue(any("new-standard-chat" in error for error in errors))

    def test_ask_ai_mutual_review_requires_bounded_relay_contract(self) -> None:
        package = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_mutual_review_errors(package))

    def test_ask_ai_relay_instruction_normalizes_only_two_provider_legacy_stop(self) -> None:
        two_provider = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 2,
            "stop_after": "dual-approval-same-candidate",
        }
        normalized, errors = VALIDATOR.normalize_relay_instruction(two_provider)
        self.assertEqual([], errors)
        self.assertIsNotNone(normalized)
        self.assertEqual("all-providers-approve-same-candidate", normalized["stop_after"])
        three_provider = {**two_provider, "external_providers": ["chatgpt", "gemini", "kimi"], "relay_order": ["chatgpt", "gemini", "kimi"]}
        errors = VALIDATOR.relay_instruction_errors(three_provider)
        self.assertTrue(any("exactly two providers" in error for error in errors))

    def test_ask_ai_relay_instruction_requires_sequential_workflow_and_positive_turn_cap(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "stop_after": "all-providers-approve-same-candidate",
        }
        self.assertEqual([], VALIDATOR.relay_instruction_errors(instruction))
        three_provider = {
            **instruction,
            "external_providers": ["chatgpt", "gemini", "kimi"],
            "relay_order": ["chatgpt", "gemini", "kimi"],
        }
        self.assertEqual([], VALIDATOR.relay_instruction_errors(three_provider))
        instruction["workflow"] = "independent"
        self.assertTrue(any("workflow" in error for error in VALIDATOR.relay_instruction_errors(instruction)))
        instruction["workflow"] = "sequential-relay"
        for invalid_cap in (None, 0, -1, True, "1"):
            with self.subTest(invalid_cap=invalid_cap):
                if invalid_cap is None:
                    instruction.pop("max_turns_per_provider", None)
                else:
                    instruction["max_turns_per_provider"] = invalid_cap
                errors = VALIDATOR.relay_instruction_errors(instruction)
                self.assertTrue(any("max_turns_per_provider" in error for error in errors))

    def test_ask_ai_relay_instruction_rejects_invalid_promotion_and_roster(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "candidate_promotion": "automatic",
            "stop_after": "all-providers-approve-same-candidate",
        }
        self.assertTrue(any("candidate_promotion" in error for error in VALIDATOR.relay_instruction_errors(instruction)))
        instruction["external_providers"] = ["chatgpt"]
        instruction["relay_order"] = ["chatgpt"]
        self.assertTrue(any("two or more" in error for error in VALIDATOR.relay_instruction_errors(instruction)))

    def test_ask_ai_relay_instruction_rejects_non_string_or_invalid_relay_order_entries(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "stop_after": "all-providers-approve-same-candidate",
        }
        invalid_orders = (
            [["chatgpt"], "gemini"],
            [{"provider": "chatgpt"}, "gemini"],
            ["", "gemini"],
            ["chatgpt", "chatgpt"],
            ["chatgpt", "kimi"],
            ["chatgpt", 7],
        )
        for relay_order in invalid_orders:
            with self.subTest(relay_order=relay_order):
                _, errors = VALIDATOR.normalize_relay_instruction(
                    {**instruction, "relay_order": relay_order}
                )
                self.assertTrue(any("relay_order" in error for error in errors))

    def test_browser_operation_protocol_keeps_relay_turn_action_hierarchy(self) -> None:
        source = ROOT / "protocols" / "browser-operation-v1.md"
        text = source.read_text(encoding="utf-8")
        for token in (
            "relay_turn_id",
            "conversation creation, attachment, submit,",
            "response capture, final marker",
            "one operation ID for multiple actions",
            "a new session is required",
            "Later turns for that same provider reuse that verified conversation",
            "original create operation ID",
        ):
            self.assertIn(token, text)
        for relative in (
            "skills/ask-ai/references/browser-operation-protocol.md",
            "skills/ops-browser/references/browser-operation-protocol.md",
        ):
            self.assertEqual(text, (ROOT / relative).read_text(encoding="utf-8"))

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

    def test_skill_index_set_must_match(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"] = []
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("skills-index.json" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_related_skill_must_exist(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["related"] = ["missing-skill"]
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("unknown related Skills" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_category_must_exist(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["category"] = "missing-category"
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("unknown category" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_rejects_self_relation(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["related"] = ["sample-skill"]
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("cannot relate to itself" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_category_must_match_distribution_group(self) -> None:
        root = self.make_repo()
        distribution = json.loads((root / "skills.sh.json").read_text())
        distribution["groupings"][0]["title"] = "Different Group"
        (root / "skills.sh.json").write_text(json.dumps(distribution))
        self.assertTrue(
            any("category titles differ" in error for error in VALIDATOR.validate(root))
        )

    def test_skill_index_rejects_duplicate_category_titles(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["categories"]["other"] = {
            "title": "Samples",
            "description": "Another category.",
        }
        index["skills"][0]["category"] = "other"
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(
            any("duplicate category titles" in error for error in VALIDATOR.validate(root))
        )

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
