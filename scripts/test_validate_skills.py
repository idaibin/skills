#!/usr/bin/env python3
"""Regression tests for the skill package validator."""

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load validator: {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

markdown_table_rows = VALIDATOR.markdown_table_rows
validate_eval_cases = VALIDATOR.validate_eval_cases
validate_local_links = VALIDATOR.validate_local_links
validate_repository_indexes = VALIDATOR.validate_repository_indexes
validate_routing_graph = VALIDATOR.validate_routing_graph
validate_skill_invocations = VALIDATOR.validate_skill_invocations
validate_specialized_eval_contracts = VALIDATOR.validate_specialized_eval_contracts
validate_cross_artifact_contracts = VALIDATOR.validate_cross_artifact_contracts
expected_routes_to_skill = VALIDATOR.expected_routes_to_skill
validate_shared_browser_operation_protocol = VALIDATOR.validate_shared_browser_operation_protocol

BEHAVIOR_EVAL_PATH = Path(__file__).with_name("eval-human-writing.py")
BEHAVIOR_SPEC = importlib.util.spec_from_file_location("eval_human_writing", BEHAVIOR_EVAL_PATH)
if BEHAVIOR_SPEC is None or BEHAVIOR_SPEC.loader is None:
    raise RuntimeError(f"Cannot load behavior eval: {BEHAVIOR_EVAL_PATH}")
BEHAVIOR_EVAL = importlib.util.module_from_spec(BEHAVIOR_SPEC)
sys.modules[BEHAVIOR_SPEC.name] = BEHAVIOR_EVAL
BEHAVIOR_SPEC.loader.exec_module(BEHAVIOR_EVAL)


VALID_EVAL = """# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `one` | Trigger. |
| `two` | Trigger. |
| `three` | Trigger. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `four` | Prefer another skill. |
| `five` | Prefer another skill. |
| `six` | Prefer another skill. |

## Quality Eval

| Case | Pass | Reject If |
| --- | --- | --- |
| A | Evidence A | Failure A |
| B | Evidence B | Failure B |
| C | Evidence C | Failure C |
| D | Evidence D | Failure D |

## Scoring

Minimum pass: every quality case scores at least 8.
"""


class ValidateSkillsTests(unittest.TestCase):
    def specialized_contract_errors(
        self, skill_name: str, mutation: tuple[str, str]
    ) -> list[str]:
        path = (
            VALIDATOR_PATH.parents[1]
            / "skills"
            / skill_name
            / "references"
            / "eval-cases.md"
        )
        original = path.read_text(encoding="utf-8")
        changed = original.replace(mutation[0], mutation[1], 1)
        self.assertNotEqual(original, changed)
        return validate_specialized_eval_contracts(skill_name, changed, label="test")

    def cross_artifact_contract_errors(
        self, skill_name: str, surface: str, marker: str, section: str | None = None
    ) -> list[str]:
        package = VALIDATOR_PATH.parents[1] / "skills" / skill_name
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
                "default_prompt",
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        original = surfaces[surface]
        if section is None:
            changed = re.sub(
                re.escape(marker), "removed-contract-marker", original, flags=re.IGNORECASE
            )
        else:
            start = original.find(section)
            self.assertGreaterEqual(start, 0)
            body_start = start + len(section)
            next_section = original.find("\n## ", body_start)
            end = len(original) if next_section < 0 else next_section
            scoped = re.sub(
                re.escape(marker),
                "removed-contract-marker",
                original[body_start:end],
                flags=re.IGNORECASE,
            )
            changed = original[:body_start] + scoped + original[end:]
        self.assertNotEqual(surfaces[surface], changed)
        surfaces[surface] = changed
        return validate_cross_artifact_contracts(skill_name, surfaces, label="test")

    def test_repository_indexes_must_match_source_packages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha"),
                VALIDATOR.SkillPackage(name="beta", path=root / "skills" / "beta"),
            ]
            (root / "README.md").write_text(
                "| `alpha` | First |\n| `beta` | Second |\n", encoding="utf-8"
            )
            (root / "INSTALL.md").write_text(
                "- `skills/alpha`\n- `skills/beta`\n", encoding="utf-8"
            )
            (root / "skills.sh.json").write_text(
                '{"groupings":[{"skills":["alpha","beta"]}]}', encoding="utf-8"
            )

            self.assertEqual([], validate_repository_indexes(root, packages))

            (root / "skills.sh.json").write_text(
                '{"groupings":[{"skills":["alpha","gamma"]}]}', encoding="utf-8"
            )
            errors = validate_repository_indexes(root, packages)

        self.assertTrue(any("missing skill beta" in error for error in errors))
        self.assertTrue(any("unknown skill gamma" in error for error in errors))

    def test_shared_browser_operation_protocol_must_not_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            relative_paths = (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            )
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            for relative in relative_paths:
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(source, encoding="utf-8")

            self.assertEqual([], validate_shared_browser_operation_protocol(root))

            (root / relative_paths[1]).write_text(source + "drift\n", encoding="utf-8")
            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(any("must be identical" in error for error in errors))

    def test_shared_browser_operation_protocol_requires_structured_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            changed = source.replace("round_id: <same request round id>\n", "", 1)
            for relative in (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(changed, encoding="utf-8")

            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(
            any("Handoff Result" in error and "round_id:" in error for error in errors)
        )

    def test_shared_browser_operation_protocol_rejects_invalid_retry_enum(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = (
                VALIDATOR_PATH.parents[1]
                / "skills"
                / "chatgpt-review"
                / "references"
                / "browser-operation-protocol.md"
            ).read_text(encoding="utf-8")
            changed = source.replace(
                "retry_policy: <never|only-if-no-side-effect-proven>",
                "retry_policy: <always>",
                1,
            )
            for relative in (
                Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
                Path("skills/ops-browser/references/browser-operation-protocol.md"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(changed, encoding="utf-8")

            errors = validate_shared_browser_operation_protocol(root)

        self.assertTrue(
            any("Handoff Request" in error and "retry_policy" in error for error in errors)
        )

    def test_legacy_regex_catches_retired_skill_names(self) -> None:
        for name in (
            "repo-context",
            "frontend-implementation",
            "frontend-governance",
            "rust-engineering-governance",
        ):
            self.assertIsNotNone(VALIDATOR.LEGACY_RE.search(f"use {name} now"))

    def test_markdown_table_rows_returns_data_only(self) -> None:
        rows = markdown_table_rows(VALID_EVAL, "## Trigger Eval")
        self.assertEqual(3, len(rows))
        self.assertEqual(["`one`", "Trigger."], rows[0])

    def test_eval_validation_accepts_minimum_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(VALID_EVAL, encoding="utf-8")
            errors, metrics = validate_eval_cases(eval_file, label="test")

        self.assertEqual([], errors)
        self.assertIsNotNone(metrics)
        self.assertEqual(3, metrics.trigger_cases)
        self.assertEqual(4, metrics.quality_cases)

    def test_eval_validation_rejects_duplicates_and_weak_scoring(self) -> None:
        invalid_eval = VALID_EVAL.replace("`two`", "`one`").replace("at least 8", "at least 5")
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(invalid_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("score" in error for error in errors))

    def test_eval_validation_rejects_historical_score_of_seven(self) -> None:
        historical_eval = VALID_EVAL.replace("at least 8", "at least 7")
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(historical_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertTrue(any("at least 8" in error for error in errors))

    def test_eval_validation_accepts_defect_gate(self) -> None:
        defect_gate_eval = VALID_EVAL.replace(
            "every quality case scores at least 8",
            "no P0 or P1 defect remains",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            eval_file = Path(temp_dir) / "eval-cases.md"
            eval_file.write_text(defect_gate_eval, encoding="utf-8")
            errors, _ = validate_eval_cases(eval_file, label="test")

        self.assertEqual([], errors)

    def test_routing_graph_requires_symmetric_documented_neighbors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            alpha = root / "skills" / "alpha"
            beta = root / "skills" / "beta"
            for package, neighbor in ((alpha, "beta"), (beta, "alpha")):
                references = package / "references"
                references.mkdir(parents=True)
                (package / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text(
                    f"## Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n| route | Prefer `{neighbor}`. |\n"
                    "\n## Non-Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n",
                    encoding="utf-8",
                )
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":["alpha"]}', encoding="utf-8"
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            self.assertEqual([], validate_routing_graph(root, packages))

            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":[]}', encoding="utf-8"
            )
            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("must be symmetric" in error for error in errors))

    def test_routing_graph_ignores_neighbor_mentions_outside_expected_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            alpha = root / "skills" / "alpha"
            beta = root / "skills" / "beta"
            for package, prompt, expected in (
                (alpha, "Mention beta only in this prompt", "Stay with alpha."),
                (beta, "Route this case", "Prefer alpha."),
            ):
                references = package / "references"
                references.mkdir(parents=True)
                (package / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text(
                    "## Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n"
                    f"| {prompt} | {expected} |\n"
                    "\n## Non-Trigger Eval\n\n| Prompt | Expected |\n| --- | --- |\n",
                    encoding="utf-8",
                )
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"beta":["alpha"]}', encoding="utf-8"
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("source alpha" in error and "beta" in error for error in errors))

    def test_routing_expectation_requires_affirmative_semantics(self) -> None:
        self.assertTrue(expected_routes_to_skill("Should prefer `repo-map`.", "repo-map"))
        self.assertTrue(
            expected_routes_to_skill(
                "Trigger coordinator; delegate bounded work to `audit-rust`.",
                "audit-rust",
            )
        )
        self.assertFalse(expected_routes_to_skill("Do not use `repo-map`.", "repo-map"))
        self.assertFalse(expected_routes_to_skill("Should not use `repo-map`.", "repo-map"))
        self.assertFalse(
            expected_routes_to_skill(
                "Prefer `diagnose`, not `repo-map`.",
                "repo-map",
            )
        )
        self.assertFalse(expected_routes_to_skill("Mentions `repo-map` only.", "repo-map"))

    def test_routing_graph_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for name in ("alpha", "beta"):
                references = root / "skills" / name / "references"
                references.mkdir(parents=True)
                (references.parent / "SKILL.md").write_text("", encoding="utf-8")
                (references / "eval-cases.md").write_text("", encoding="utf-8")
            graph = root / "docs" / "skills"
            graph.mkdir(parents=True)
            (graph / "routing-graph.json").write_text(
                '{"alpha":["beta"],"alpha":[],"beta":["alpha"]}',
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=root / "skills" / "alpha"),
                VALIDATOR.SkillPackage(name="beta", path=root / "skills" / "beta"),
            ]

            errors = validate_routing_graph(root, packages)

        self.assertTrue(any("duplicate key 'alpha'" in error for error in errors))

    def test_human_writing_behavior_fixtures_pass(self) -> None:
        results = BEHAVIOR_EVAL.run_fixtures(BEHAVIOR_EVAL.DEFAULT_FIXTURES)

        self.assertGreaterEqual(len(results), 10)
        self.assertTrue(all(result.passed for result in results))

    def test_human_writing_behavior_fixture_detects_bad_output(self) -> None:
        result = BEHAVIOR_EVAL.evaluate_case(
            {
                "id": "regression",
                "expected_pass": True,
                "output": "整体性能提升 10 倍。",
                "must_contain": ["类型检查", "官方"],
                "must_not_contain": ["整体性能"],
            }
        )

        self.assertFalse(result.passed)
        self.assertTrue(result.failures)

    def test_local_link_validation_rejects_missing_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "sample-skill"
            package.mkdir()
            (package / "SKILL.md").write_text("[missing](references/missing.md)\n", encoding="utf-8")

            errors = validate_local_links(package, label="test")

        self.assertEqual(1, len(errors))
        self.assertIn("broken local link", errors[0])

    def test_skill_invocations_must_resolve_to_shipped_packages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "skills"
            alpha = root / "alpha"
            beta = root / "beta"
            alpha.mkdir(parents=True)
            beta.mkdir(parents=True)
            (alpha / "SKILL.md").write_text(
                "Shell examples may contain echo $target and tool $1.\n",
                encoding="utf-8",
            )
            (beta / "SKILL.md").write_text("No routed skill.\n", encoding="utf-8")
            (alpha / "agents").mkdir()
            (alpha / "agents" / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Use $beta, $missing-skill, and $diagnosse; run echo ${target} $1 and preserve this.$watch."\n',
                encoding="utf-8",
            )
            packages = [
                VALIDATOR.SkillPackage(name="alpha", path=alpha),
                VALIDATOR.SkillPackage(name="beta", path=beta),
            ]

            errors = validate_skill_invocations(
                [packages[0]], known_skill_names={package.name for package in packages}
            )

        self.assertEqual(2, len(errors))
        self.assertTrue(any("unknown skill invocation $missing-skill" in error for error in errors))
        self.assertTrue(any("unknown skill invocation $diagnosse" in error for error in errors))
        self.assertFalse(any("unknown skill invocation $target" in error for error in errors))
        self.assertFalse(any("unknown skill invocation $watch" in error for error in errors))

    def test_implement_rust_requires_overlay_selection_eval(self) -> None:
        errors = self.specialized_contract_errors(
            "implement-rust", ("## Overlay Selection Eval", "## Removed Overlay Eval")
        )
        self.assertTrue(any("Overlay Selection Eval" in error for error in errors))

    def test_audit_rust_requires_every_scenario_field(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-rust", ("- **Validation:**", "- **Removed validation:**")
        )
        self.assertTrue(any("scenario 1 missing field 'Validation'" in error for error in errors))

    def test_audit_rust_requires_out_of_scope_profile_rule(self) -> None:
        path = (
            VALIDATOR_PATH.parents[1]
            / "skills"
            / "audit-rust"
            / "references"
            / "eval-cases.md"
        )
        changed = path.read_text(encoding="utf-8").replace("Out of scope", "Excluded")
        errors = validate_specialized_eval_contracts("audit-rust", changed, label="test")
        self.assertTrue(any("Out of scope" in error for error in errors))

    def test_review_bridge_requires_split_package_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "chatgpt-review",
            ("| Split package artifact |", "| Removed split package artifact |"),
        )
        self.assertTrue(any("Split package artifact" in error for error in errors))

    def test_review_bridge_requires_artifact_visibility_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "chatgpt-review",
            ("| Review artifact visibility |", "| Removed artifact visibility |"),
        )
        self.assertTrue(any("Review artifact visibility" in error for error in errors))

    def test_audit_frontend_requires_framework_specific_scenarios(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-frontend", ("Pure Options API", "Removed API style")
        )
        self.assertTrue(any("Pure Options API" in error for error in errors))

    def test_repo_review_requires_immutable_basis_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "repo-review", ("| Immutable basis |", "| Removed basis |")
        )
        self.assertTrue(any("Immutable basis" in error for error in errors))

    def test_repo_map_requires_review_boundary_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "repo-map", ("| Context-versus-review boundary |", "| Removed review boundary |")
        )
        self.assertTrue(any("Context-versus-review boundary" in error for error in errors))

    def test_audit_security_requires_coordinator_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "audit-security", ("| Scoped specialist boundary |", "| Removed handoff |")
        )
        self.assertTrue(any("Scoped specialist boundary" in error for error in errors))

    def test_ops_browser_requires_debug_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "ops-browser", ("| Browser debug handoff |", "| Removed debug handoff |")
        )
        self.assertTrue(any("Browser debug handoff" in error for error in errors))

    def test_ops_client_requires_debug_handoff_contract(self) -> None:
        errors = self.specialized_contract_errors(
            "ops-client", ("| Client debug handoff |", "| Removed debug handoff |")
        )
        self.assertTrue(any("Client debug handoff" in error for error in errors))

    def test_every_declared_cross_artifact_term_is_mutation_protected(self) -> None:
        tested = 0
        declared = sum(
            len(terms)
            for _, _, _, terms in VALIDATOR.CROSS_ARTIFACT_TERM_REQUIREMENTS
        )
        for skill_name, surface, section, terms in VALIDATOR.CROSS_ARTIFACT_TERM_REQUIREMENTS:
            for term in terms:
                with self.subTest(skill=skill_name, surface=surface, term=term):
                    errors = self.cross_artifact_contract_errors(
                        skill_name, surface, term, section
                    )
                    self.assertTrue(any("missing contract terms" in error for error in errors))
                    tested += 1
        self.assertEqual(declared, tested)

    def test_browser_eval_route_reversal_is_rejected(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-browser"
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"), "default_prompt"
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] = surfaces["references/eval-cases.md"].replace(
            "Should prefer `diagnose`, which may delegate Browser Debug Evidence to `ops-browser`.",
            "Should trigger `ops-browser` directly.",
            1,
        )
        errors = validate_cross_artifact_contracts("ops-browser", surfaces, label="test")
        self.assertTrue(any("missing semantic terms" in error for error in errors))

    def test_client_eval_evidence_weakening_is_rejected(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-client"
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": (package / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(
                (package / "agents" / "openai.yaml").read_text(encoding="utf-8"), "default_prompt"
            ),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] = surfaces["references/eval-cases.md"].replace(
            "deletes evidence before transfer",
            "deletes disposable state",
            1,
        )
        errors = validate_cross_artifact_contracts("ops-client", surfaces, label="test")
        self.assertTrue(any("missing semantic terms" in error for error in errors))

    def test_semantic_contradiction_is_rejected_with_required_terms_present(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-browser"
        yaml_text = (package / "agents" / "openai.yaml").read_text(encoding="utf-8")
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": yaml_text,
            "agents/openai.default_prompt": VALIDATOR.yaml_scalar(yaml_text, "default_prompt"),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        surfaces["references/eval-cases.md"] += (
            "\nContradiction: direct operation takes precedence over `diagnose`.\n"
        )
        errors = validate_cross_artifact_contracts("ops-browser", surfaces, label="test")
        self.assertTrue(any("contradictory contract phrase" in error for error in errors))

    def test_metadata_terms_must_remain_in_default_prompt(self) -> None:
        package = VALIDATOR_PATH.parents[1] / "skills" / "ops-browser"
        yaml_text = (package / "agents" / "openai.yaml").read_text(encoding="utf-8")
        default_prompt = VALIDATOR.yaml_scalar(yaml_text, "default_prompt")
        moved_term = "before browser operation"
        surfaces = {
            "SKILL.md": (package / "SKILL.md").read_text(encoding="utf-8"),
            "agents/openai.yaml": yaml_text + f"\n# {moved_term}\n",
            "agents/openai.default_prompt": default_prompt.replace(moved_term, "after routing"),
            "references/usage.md": (package / "references" / "usage.md").read_text(encoding="utf-8"),
            "references/eval-cases.md": (package / "references" / "eval-cases.md").read_text(encoding="utf-8"),
        }
        errors = validate_cross_artifact_contracts("ops-browser", surfaces, label="test")
        self.assertTrue(any("missing contract terms" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
