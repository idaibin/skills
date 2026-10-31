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
    "skills/ui-spec/references/documentation-boundaries.md": (
        r"projection is conditional: use it only when (?P<gate>.*?) already exist\.",
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
    "skills/dev-frontend/references/ui-components-and-tokens.md": (
        r"structured projection requires a (?P<gate>.*?)\. Otherwise",
    ),
    "skills/repo-audit/references/frontend-profile.md": (
        r"verify its (?P<gate>.*?)\. Inspect current validator evidence",
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

    def test_product_spec_terminal_and_sidecar_gates(self) -> None:
        skill = self.read("skills/product-spec/SKILL.md")
        text = re.sub(r"\s+", " ", self.read("skills/product-spec/references/documentation-boundaries.md"))
        self.assertIn("references/documentation-boundaries.md", skill)
        self.assertIn("latest accepted product contract", text)
        workflow_gate = re.search(
            r"durable structured artifact requires all of: (?P<gate>.*?)\. When",
            text,
        )
        self.assertIsNotNone(workflow_gate)
        assert workflow_gate is not None
        gate = workflow_gate.group("gate")
        self.assert_complete_lifecycle(gate, context="product-spec workflow gate")

    def test_product_mode_oracle_preserves_observed_reconstruction_boundary(self) -> None:
        # Static oracle/profile consistency, not a scored reconstruction task.
        evals = self.read("skills/product-spec/references/eval-cases.md")
        quality = evals.split("## Quality Eval\n", 1)[1].split("\n## ", 1)[0]
        rows = [
            [cell.strip() for cell in line.split("|")[1:-1]]
            for line in quality.splitlines()
            if line.startswith("| Mode selection |")
        ]
        self.assertEqual(1, len(rows))
        self.assertEqual(3, len(rows[0]))
        _, expected, rejected = rows[0]
        for mode in ("Feature Spec", "Foundation Spec", "Artifact Update"):
            self.assertIn(mode, expected)
        self.assertIn("for product definition", expected)
        self.assertIn("explicitly requested Evidence Reconstruction", expected)
        self.assertIn("only the observed-candidate profile", expected)
        self.assertNotIn("Exposes only Feature Spec, Foundation Spec, and Artifact Update", expected)
        for forbidden in ("Discovery", "grill", "Brief", "Standard"):
            self.assertIn(forbidden, rejected)
        self.assertIn("promotes an observed reconstruction candidate into an accepted or Ready product contract", rejected)
        profile = re.sub(r"\s+", " ", self.read("skills/product-spec/references/source-reconstruction.md"))
        self.assertIn("Use only when the user explicitly asks", profile)
        self.assertIn("observed/inferred/accepted distinctions", profile)
        self.assertIn("Do not call it Ready or implementation-authorizing", profile)
        self.assertIn("without the owner's explicit decision", profile)
        self.assertIn("The product owner accepts exact scope/version/content", profile)

    def test_java_conformance_work_is_distinct_from_completion(self) -> None:
        # Static authority/gate consistency, not execution of Java implementation.
        text = self.read("skills/dev-java/references/protocol-contracts.md")
        normalized = re.sub(r"\s+", " ", text)
        self.assertIn(
            "Explicitly authorized implementation may establish conformance to the exact accepted "
            "contract within the approved source scope; existing unresolved-authority and "
            "decisive-input stop conditions still apply.",
            normalized,
        )
        self.assertIn(
            "Automated reliance on implementation conformance or delivery completion MUST stop "
            "when any applicable condition is true:",
            normalized,
        )
        self.assertNotIn("Implementation automation or delivery completion MUST stop", normalized)
        for boundary in (
            "the owner is wrong or ambiguous",
            "acceptance is not bound to the exact scope/version/content hash",
            "an accepted business-exposure rule still conflicts with a reachable source route",
            "Owner acceptance otherwise makes the contract authoritative before Java implementation",
            "incomplete implementation or lifecycle evidence does not demote that authority",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, normalized)
        completion_gate = text.split("condition is true:\n", 1)[1].split(
            "\nFor code-first automation", 1
        )[0]
        self.assertEqual(
            [
                "- code-first generation has no executable producer bound to the fixed Git basis;",
                "- contract-first Java routes/DTOs/security/errors do not conform to the accepted contract;",
                "- only parser/schema validation has passed;",
                "- no fixed legacy baseline or compatibility comparison exists for existing consumers;",
                "- non-LLM consumer, validator, drift policy, or retirement rule is missing;",
                "- an actual generated derivative has no declared producer;",
                "- operation errors are mechanically copied rather than resolved from reachable code;",
                "- unresolved handbook, UI, or decision content remains embedded in OpenAPI.",
            ],
            [line for line in completion_gate.splitlines() if line.startswith("- ")],
        )

    def test_rust_native_rest_oracle_keeps_independent_contract_overlay(self) -> None:
        evals = self.read("skills/dev-rust/references/eval-cases.md")
        trigger = evals.split("## Trigger Eval\n", 1)[1].split("\n## Non-Trigger Eval", 1)[0]
        prompt = (
            "`Add this REST handler using the repository's native route, DTO, client, and tests; "
            "do not introduce schema generation.`"
        )
        rows = [
            [cell.strip() for cell in line.split("|")[1:-1]]
            for line in trigger.splitlines()
            if line.startswith("| " + prompt + " |")
        ]
        self.assertEqual(1, len(rows))
        self.assertEqual(3, len(rows[0]))
        _, expected, why = rows[0]
        self.assertIn("Baseline + Contract", expected)
        self.assertIn("any other independently applicable overlays", expected)
        self.assertIn("mark protocol automation `Not applicable`", expected)
        self.assertNotIn("Baseline only", expected)
        self.assertEqual("HTTP implementation does not itself require OpenAPI.", why)

    def test_rust_behavior_oracle_reuses_meaningful_checks_without_fabricating_red(self) -> None:
        # Static consistency with the shared protocol, not a scored Rust task.
        evals = self.read("skills/dev-rust/references/eval-cases.md")
        quality = evals.split("## Quality Eval\n", 1)[1].split("\n## ", 1)[0]
        rows = [
            [cell.strip() for cell in line.split("|")[1:-1]]
            for line in quality.splitlines()
            if line.startswith("| Behavior-first slices |")
        ]
        self.assertEqual(1, len(rows))
        self.assertEqual(3, len(rows[0]))
        _, expected, rejected = rows[0]
        for requirement in (
            "reuses an existing check with an independent expected result",
            "adds/extends one for meaningful uncovered risk",
            "implements a coherent slice",
            "reports whether red was observed",
            "preserves an explicitly adopted TDD workflow",
            "If no honest seam exists, records another focused validation path and its reason",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, expected)
        for forbidden in (
            "Duplicates implementation logic in expectations",
            "adds implementation-mirroring checks for a reversible low-impact edit",
            "ignores required project TDD",
            "claims red-green evidence without observing red before green",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, rejected)
        self.assertNotIn("works one failing behavior test", expected)

    def test_structured_projection_consumers_keep_complete_lifecycle(self) -> None:
        for path in LIFECYCLE_GATE_PATTERNS:
            for index, gate in enumerate(self.lifecycle_gates(path)):
                context = f"{path} gate {index + 1}"
                self.assert_complete_lifecycle(gate, context=context)

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

    def test_ui_candidate_lifecycle_stays_local_and_owner_bounded(self) -> None:
        skill = self.read("skills/ui-spec/SKILL.md")
        candidate = self.read(
            "skills/ui-spec/references/candidate-visual-direction.md"
        )
        for required in (
            ".codex/reviews/",
            "candidate UI specification",
            "complete generation prompt",
            "content hashes",
            "`ask-ai`",
            "`DESIGN.md` unchanged",
            "Not Ready for dev-frontend",
        ):
            with self.subTest(required=required):
                self.assertIn(required, skill + candidate)
        self.assertIn("edit the candidate specification first", candidate)
        self.assertIn("default state", candidate)
        self.assertIn("separate interaction states", candidate)
        self.assertIn("never send from\nthis Skill", candidate)

    def test_ui_multi_surface_readiness_uses_existing_checklist(self) -> None:
        # Static consumer/owner alignment, not an Agent readiness evaluation.
        target = "evaluation-rubric.md#end-of-work-readiness-checklist"
        sections = {}
        for name, heading in (
            ("multi-surface.md", "Readiness and Partial Results"),
            ("workflow.md", "Evaluation And Handoff"),
        ):
            text = self.read(f"skills/ui-spec/references/{name}")
            section = text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
            sections[name] = re.sub(r"\s+", " ", section)
            self.assertIn(target, re.findall(r"\[[^\]]+\]\(([^)]+)\)", section))
        multi = sections["multi-surface.md"]
        self.assertIn("`Partial` only when it contains both ready and blocked slices", multi)
        self.assertNotIn("when any requested slice is unready or missing required gates", multi)
        self.assertNotIn("mark an incomplete multi-surface result `Partial`", sections["workflow.md"])
        self.assertIn("One incomplete slice does not block unrelated ready slices", multi)
        self.assertIn("`Complete` only when all requested slices are ready", multi)
        self.assertIn("only when that slice passes all gates", multi)
        self.assertIn("Unconfirmed slices remain listed in the shared index with blockers", multi)
        rubric = self.read("skills/ui-spec/references/evaluation-rubric.md")
        checklist = re.sub(r"\s+", " ", rubric.split("## End-of-Work Readiness Checklist\n", 1)[1])
        self.assertIn("Use `Partial` only when a multi-slice result contains both ready and blocked slices", checklist)
        self.assertIn("If an item fails, stop at that item", checklist)
        self.assertIn("report non-blocking `Not verified` gaps without downgrading the slice", checklist)

    def test_consumers_use_the_same_resolved_design_root(self) -> None:
        paths = (
            "protocols/specification-authorities-v1.md",
            "protocols/visual-direction-and-anti-slop-v1.md",
            "skills/ui-spec/references/visual-direction-and-anti-slop.md",
            "skills/dev-frontend/references/visual-direction-and-anti-slop.md",
            "skills/repo-audit/references/visual-direction-and-anti-slop.md",
            "skills/dev-frontend/references/specification-authorities.md",
            "skills/repo-audit/references/frontend-profile.md",
            "skills/repo-review/references/standards-and-spec.md",
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
        for owner in ("product-spec", "ui-spec", "dev-frontend", "repo-audit", "repo-review"):
            path = f"skills/{owner}/references/eval-cases.md"
            text = self.read(path)
            with self.subTest(path=path):
                self.assertNotIn("repository-root `DESIGN.md`", text)
                self.assertNotIn("root `DESIGN.md`", text)

    def test_repo_map_separates_source_and_runtime_identity(self) -> None:
        skill = self.read("skills/repo-map/SKILL.md")
        text = self.read("skills/repo-map/references/checklist.md") + self.read(
            "skills/repo-map/references/api-contract-map.md"
        )
        self.assertIn("references/checklist.md", skill)
        self.assertIn("references/api-contract-map.md", skill)
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

    def test_ui_governance_keeps_page_registry_and_source_authorities_separate(self) -> None:
        ui_evals = self.read("skills/ui-spec/references/eval-cases.md")
        audit_components = self.read(
            "skills/repo-audit/references/frontend-component-system.md"
        )
        self.assertIn("Registry/token lifecycle in their declared owners", ui_evals)
        self.assertIn("without treating the Registry as the props", audit_components)
        self.assertIn("Whole-image similarity metrics are diagnostic", audit_components)
        self.assertIn("optional assets are absent", audit_components)

    def test_design_completeness_handoff_is_host_neutral(self) -> None:
        contract = self.read("skills/ui-spec/references/design-md-contract.md")
        self.assertIn("does not mutate the producer result", contract)
        package_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "skills" / "ui-spec").rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".json", ".yaml", ".yml"}
        )
        self.assertNotIn("forge" + "way", package_text.lower())
        for path in (
            "skills/dev-frontend/references/eval-cases.md",
            "skills/repo-audit/references/eval-cases.md",
            "skills/repo-review/references/eval-cases.md",
        ):
            with self.subTest(path=path):
                consumer = self.read(path)
                self.assertNotIn("ui-spec-design-completeness/1: complete", consumer)
                self.assertNotIn("producer result `complete`", consumer)


if __name__ == "__main__":
    unittest.main()
