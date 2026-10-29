#!/usr/bin/env python3
"""Executable regressions for the dev-frontend contract-freeze boundary."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DevFrontendContractFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "skills/dev-frontend/SKILL.md").read_text(encoding="utf-8")
        cls.usage = (
            ROOT / "skills/dev-frontend/references/usage.md"
        ).read_text(encoding="utf-8")
        cls.checklist = (
            ROOT / "skills/dev-frontend/references/checklist.md"
        ).read_text(encoding="utf-8")
        cls.evals = (
            ROOT / "skills/dev-frontend/references/eval-cases.md"
        ).read_text(encoding="utf-8")
        cls.ui_governance = (
            ROOT / "skills/dev-frontend/references/ui-components-and-tokens.md"
        ).read_text(encoding="utf-8")
        cls.decomposition = (
            ROOT / "skills/dev-frontend/references/decomposition.md"
        ).read_text(encoding="utf-8")

    def test_reuse_search_precedes_the_final_freeze(self) -> None:
        search = self.checklist.index("Before the final freeze, run a bounded search")
        freeze = self.checklist.index("record the smallest executable contract")
        self.assertLess(search, freeze)
        self.assertIn("references/checklist.md", self.skill)
        self.assertIn("reuse decision", self.checklist)

    def test_unresolved_decisive_contract_stops_without_global_api_archaeology(self) -> None:
        self.assertIn("Stop when a decisive behavior or visual contract is unresolved", self.skill)
        self.assertIn("changed by, depended on by, or decisive to acceptance", self.checklist)
        self.assertIn("local UI-state fix does not require an unrelated backend survey", self.checklist)
        self.assertIn("Do not change its request or response contract", self.evals)

    def test_correction_rejects_delayed_work_and_reconciles_landed_hunks(self) -> None:
        self.assertIn("Reject in-flight or delayed delegated results", self.checklist)
        self.assertIn("Inventory and reconcile any old-revision hunks", self.checklist)
        self.assertIn("one old hunk already landed", self.evals)

    def test_adopted_ui_governance_is_conditional_and_project_native(self) -> None:
        self.assertIn("only when the authorized change affects", self.ui_governance)
        self.assertIn("Do not require these assets", self.ui_governance)
        self.assertIn("Component -> Semantic -> Primitive", self.ui_governance)
        self.assertIn("authored CSS custom-property\n   self-reference", self.ui_governance)
        self.assertIn("project-native gate", self.ui_governance)
        self.assertIn("Adopted UI governance", self.evals)

    def test_decomposition_uses_ownership_instead_of_line_limits(self) -> None:
        self.assertIn("references/decomposition.md", self.skill)
        self.assertIn("Treat size as a review signal", self.skill)
        self.assertIn("meaningful names and separable contracts", self.decomposition)
        self.assertIn("Do not create generic dumping grounds", self.decomposition)
        self.assertIn("generated, vendored, or machine-owned files", self.decomposition)
        self.assertIn("Divergent change", self.decomposition)
        self.assertIn("Shotgun surgery", self.decomposition)
        self.assertIn("Apply the deletion test", self.decomposition)
        self.assertIn("File and function decomposition", self.evals)

    def test_existing_surface_audit_without_diff_routes_to_repo_audit(self) -> None:
        # Read the actual discovery copy: the index-only matcher cannot catch this.
        description = next(
            line for line in self.skill.splitlines() if line.startswith("description:")
        )
        with self.subTest(request="Audit existing React architecture/state without a diff or edits"):
            self.assertIn("change-based reviews to repo-review", description)
            self.assertIn("audits without a change basis to repo-audit", description)
            self.assertNotIn("Use repo-review for review-only requests", description)
            self.assertIn("review; use `repo-audit`", self.usage)

    def test_known_frontend_fix_discovers_its_own_package_test_commands(self) -> None:
        non_triggers = self.usage.split("## Non-Triggers", 1)[1].split("## Output", 1)[0]
        graph_route = next(line for line in non_triggers.splitlines() if "`repo-map`" in line)
        with self.subTest(request="Fix one known React line; find test/lint in package.json, no graph"):
            self.assertIn("Cross-repository or repository-wide", graph_route)
            self.assertIn("graph queries; use `repo-map`", graph_route)
            self.assertIn("task-local fix with known source", graph_route)
            self.assertIn("`dev-frontend` owner discovers `package.json` test/lint commands directly", graph_route)
            self.assertNotIn("Repository onboarding or command discovery; use `repo-map`", non_triggers)

    def test_visual_rubric_preserves_qualifying_first_pass_and_required_rechecks(self) -> None:
        # Static rubric regression, not proof that an Agent performed the comparison.
        rows = [line for line in self.evals.splitlines() if line.startswith("| Visual comparison gate |")]
        self.assertEqual(1, len(rows))
        cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
        self.assertEqual(3, len(cells))
        _, expected, reject = cells
        for term in (
            "one qualifying comparison", "full required coverage", "same viewport/state",
            "computed geometry/style", "After a confirmed fix", "new runtime evidence",
            "evidence is invalidated", "stricter accepted project pass requirements",
        ):
            with self.subTest(expected=term):
                self.assertIn(term, expected)
        for term in (
            "solely to reach two", "skips a required recheck", "screenshot alone",
            "SCSS inspection", "build/lint success",
        ):
            with self.subTest(reject=term):
                self.assertIn(term, reject)
                self.assertNotIn(term, expected)
        self.assertNotIn("Two-pass visual gate", self.evals)
        protocol = (ROOT / "protocols/frontend-visual-evidence-v1.md").read_text(encoding="utf-8")
        self.assertIn("If all\napplicable acceptance passes, close without repeating an unchanged comparison", protocol)
        self.assertIn("required_comparison_passes", protocol)
        self.assertIn("omission means one", protocol)


if __name__ == "__main__":
    unittest.main()
