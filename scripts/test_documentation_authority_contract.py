#!/usr/bin/env python3
"""Static cross-package contract checks for documentation authority ownership."""

from __future__ import annotations

import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE_TERMS = (
    "named owner",
    "producer",
    "non-LLM consumer",
    "semantic version",
    "executable validator",
    "drift policy",
    "retirement rule",
)

LIFECYCLE_GATE_PATTERNS = {
    "docs/skills/skill-standard.md": (
        r"Structured sidecars require (?P<gate>.*?); “AI may read it”",
    ),
    "skills/product-spec/references/documentation-boundaries.md": (
        r"durable structured artifact requires all of: (?P<gate>.*?)\. When",
    ),
    "skills/product-spec/references/eval-cases.md": (
        r"Structured artifact admission \| Requires (?P<gate>.*?) before adding a sidecar\.",
    ),
    "skills/ui-spec/SKILL.md": (
        r"projection is conditional: use it only when (?P<gate>.*?) already exist\.",
    ),
    "skills/repo-map/SKILL.md": (
        r"navigation only and require its (?P<gate>.*?)\. Otherwise",
        r"map sidecars for machine convenience without a (?P<gate>.*?)\.",
    ),
    "skills/repo-map/references/checklist.md": (
        r"structured map sidecars without a (?P<gate>.*?)\.",
    ),
    "skills/repo-map/references/prompt-templates.md": (
        r"sidecar without a proven lifecycle (?P<gate>.*?)\.",
    ),
    "skills/repo-map/references/eval-cases.md": (
        r"Structured map admission \| Adds a sidecar only with a (?P<gate>.*?)\. \|",
    ),
    "skills/dev-frontend/SKILL.md": (
        r"Require a (?P<gate>.*?)\. Run the repository-defined non-mutating validator",
    ),
    "skills/audit-frontend/SKILL.md": (
        r"verify its (?P<gate>.*?)\. Inspect current validator evidence",
    ),
    "skills/repo-review/SKILL.md": (
        r"projection is relevant only when a (?P<gate>.*?) are evidenced;",
    ),
    "skills/repo-review/references/documentation-authority-review.md": (
        r"verify a (?P<gate>.*?)\. “AI may read it”",
        r"projection is reviewed only when its (?P<gate>.*?) are evidenced;",
    ),
}


class DocumentationAuthorityContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def lifecycle_gates(self, relative: str) -> list[str]:
        text = re.sub(r"\s+", " ", self.read(relative))
        gates = []
        for pattern in LIFECYCLE_GATE_PATTERNS[relative]:
            match = re.search(pattern, text)
            self.assertIsNotNone(match, f"missing lifecycle gate in {relative}: {pattern}")
            assert match is not None
            gates.append(match.group("gate"))
        return gates

    def assert_complete_lifecycle(self, gate: str, *, context: str) -> None:
        for term in LIFECYCLE_TERMS:
            with self.subTest(context=context, term=term):
                self.assertIn(term, gate)

    def assert_each_lifecycle_term_is_required(self, gate: str, *, context: str) -> None:
        for term in LIFECYCLE_TERMS:
            mutated = gate.replace(term, "", 1)
            with self.subTest(context=context, removed=term):
                self.assertFalse(
                    all(required in mutated for required in LIFECYCLE_TERMS),
                    f"gate stayed complete after removing {term}: {context}",
                )

    def test_product_spec_terminal_and_sidecar_gates(self) -> None:
        text = re.sub(r"\s+", " ", self.read("skills/product-spec/SKILL.md"))
        self.assertIn("current terminal contract", text)
        workflow_gate = re.search(
            r"create a structured companion only when (?P<gate>.*?) already exist\.",
            text,
        )
        self.assertIsNotNone(workflow_gate)
        assert workflow_gate is not None
        gate = workflow_gate.group("gate")
        self.assert_complete_lifecycle(gate, context="product-spec workflow gate")
        self.assert_each_lifecycle_term_is_required(
            gate, context="product-spec workflow gate"
        )

    def test_structured_projection_consumers_keep_complete_lifecycle(self) -> None:
        for path in LIFECYCLE_GATE_PATTERNS:
            for index, gate in enumerate(self.lifecycle_gates(path)):
                context = f"{path} gate {index + 1}"
                self.assert_complete_lifecycle(gate, context=context)
                self.assert_each_lifecycle_term_is_required(gate, context=context)

    def test_navigation_references_are_distinct_from_copied_authority(self) -> None:
        paths = (
            "skills/dev-frontend/references/eval-cases.md",
            "skills/repo-review/references/eval-cases.md",
        )
        for path in paths:
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("`navigation-reference`", text)
                self.assertIn("`copied-authority`", text)

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
