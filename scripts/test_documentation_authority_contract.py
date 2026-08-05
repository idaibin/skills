#!/usr/bin/env python3
"""Static cross-package contract checks for documentation authority ownership."""

from __future__ import annotations

import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationAuthorityContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_product_spec_terminal_and_sidecar_gates(self) -> None:
        text = self.read("skills/product-spec/SKILL.md")
        self.assertIn("current terminal contract", text)
        self.assertIn("named owner, producer, consumer, version, validator", text)

    def test_ui_spec_resolves_design_root_and_local_evidence(self) -> None:
        text = self.read("skills/ui-spec/SKILL.md")
        self.assertIn("<design-root>/DESIGN.md", text)
        self.assertIn(".codex/artifacts/", text)
        self.assertNotIn("repository-root `DESIGN.md`", text)

    def test_consumers_use_the_same_resolved_design_root(self) -> None:
        paths = (
            "protocols/specification-authorities-v1.md",
            "protocols/visual-direction-and-anti-slop-v1.md",
            "skills/ui-spec/references/visual-direction-and-anti-slop.md",
            "skills/dev-frontend/references/visual-direction-and-anti-slop.md",
            "skills/audit-frontend/references/visual-direction-and-anti-slop.md",
            "skills/dev-frontend/SKILL.md",
            "skills/audit-frontend/SKILL.md",
            "skills/repo-review/SKILL.md",
            "skills/product-spec/references/template.md",
        )
        for path in paths:
            with self.subTest(path=path):
                text = self.read(path)
                self.assertIn("design-root", text)
                self.assertNotIn("repository-root `DESIGN.md`", text)
                self.assertNotIn("root `DESIGN.md`", text)
                self.assertIsNone(
                    re.search(r"\b(?:repository-)?root\s+`DESIGN\.md`", text)
                )

    def test_evals_do_not_restore_git_root_design_authority(self) -> None:
        for owner in ("product-spec", "ui-spec", "dev-frontend", "audit-frontend", "repo-review"):
            path = f"skills/{owner}/references/eval-cases.md"
            text = self.read(path)
            with self.subTest(path=path):
                self.assertNotIn("repository-root `DESIGN.md`", text)
                self.assertNotIn("root `DESIGN.md`", text)

    def test_repo_map_separates_source_and_runtime_identity(self) -> None:
        text = self.read("skills/repo-map/SKILL.md")
        self.assertIn("canonical/source owner", text)
        self.assertIn("runtime service identity", text)

    def test_repo_review_loads_documentation_authority_profile(self) -> None:
        skill = self.read("skills/repo-review/SKILL.md")
        reference = self.read(
            "skills/repo-review/references/documentation-authority-review.md"
        )
        self.assertIn("documentation-authority-review.md", skill)
        self.assertIn("Structured artifact gate", reference)
        self.assertIn("newly frozen basis", reference)

    def test_design_template_has_no_date_like_version_default(self) -> None:
        template = self.read("skills/ui-spec/assets/DESIGN.md")
        self.assertNotIn("version:", template)


if __name__ == "__main__":
    unittest.main()
