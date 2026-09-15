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
        cls.checklist = (
            ROOT / "skills/dev-frontend/references/checklist.md"
        ).read_text(encoding="utf-8")
        cls.evals = (
            ROOT / "skills/dev-frontend/references/eval-cases.md"
        ).read_text(encoding="utf-8")
        cls.ui_governance = (
            ROOT / "skills/dev-frontend/references/ui-components-and-tokens.md"
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


if __name__ == "__main__":
    unittest.main()
