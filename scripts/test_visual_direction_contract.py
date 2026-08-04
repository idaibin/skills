#!/usr/bin/env python3
"""Focused regressions for shared visual-direction and nested-inset contracts."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VISUAL_SOURCE = ROOT / "protocols" / "visual-direction-and-anti-slop-v1.md"
LAYOUT_SOURCE = ROOT / "protocols" / "frontend-layout-governance-v1.md"


class VisualDirectionContractTests(unittest.TestCase):
    def test_visual_contract_keeps_contextual_theme_and_color_boundaries(self) -> None:
        text = VISUAL_SOURCE.read_text(encoding="utf-8")
        self.assertIn("one primary accent semantic role", text)
        self.assertIn("semantic success, warning, danger", text)
        self.assertIn("Dark mode is conditional, not mandatory", text)
        self.assertIn("cannot override an accepted source", text)
        self.assertNotIn("8/6/4` as the catalog default", text)

    def test_visual_contract_keeps_owner_and_mode_boundaries(self) -> None:
        text = VISUAL_SOURCE.read_text(encoding="utf-8")
        self.assertIn("**Preserve:**", text)
        self.assertIn("**Overhaul:**", text)
        self.assertIn("deliberate repetition\n   for consistency is valid", text)
        self.assertIn("`ui-spec` records accepted decisions", text)
        self.assertIn("`dev-frontend` implements", text)
        self.assertIn("`audit-frontend` reports", text)

    def test_layout_contract_detects_double_inset_by_axis_and_owner(self) -> None:
        text = LAYOUT_SOURCE.read_text(encoding="utf-8")
        self.assertIn("## Nested Inset Contract", text)
        self.assertIn("shell -> content container -> page root", text)
        self.assertIn("Do not stack equal outer and inner padding", text)
        self.assertIn("Record left,\n  top, right, and bottom separately", text)
        self.assertIn("scrollbar must remain flush", text)

    def test_all_three_frontend_owners_link_the_shared_contracts(self) -> None:
        for skill in ("ui-spec", "dev-frontend", "audit-frontend"):
            with self.subTest(skill=skill):
                entrypoint = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("references/visual-direction-and-anti-slop.md", entrypoint)
                self.assertIn("references/frontend-layout-governance.md", entrypoint)


if __name__ == "__main__":
    unittest.main()
