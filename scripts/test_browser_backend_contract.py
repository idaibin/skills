#!/usr/bin/env python3
"""Static checks for ask-ai provider adapters and browser backend handoffs."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BrowserBackendContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_shared_protocol_copies_match(self) -> None:
        canonical = self.read("protocols/browser-operation-v1.md")
        for path in (
            "skills/ask-ai/references/browser-operation-protocol.md",
            "skills/ops-browser/references/browser-operation-protocol.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(canonical, self.read(path))

    def test_capability_snapshot_exposes_backend_classes(self) -> None:
        protocol = self.read("protocols/browser-operation-v1.md")
        for field in (
            "deterministic_automation",
            "agentic_navigation",
            "direct_cdp",
        ):
            with self.subTest(field=field):
                self.assertIn(f"{field}:", protocol)

    def test_handoff_carries_constraints_and_backend_evidence(self) -> None:
        protocol = self.read("protocols/browser-operation-v1.md")
        for term in (
            "execution_constraints:",
            "action_shape:",
            "allowed_origins:",
            "max_steps:",
            "max_actions:",
            "execution:",
            "backend:",
            "selection_reason:",
            "budget_used:",
        ):
            with self.subTest(term=term):
                self.assertIn(term, protocol)

    def test_fixed_external_writes_remain_deterministic_first(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        usage = self.read("skills/ops-browser/references/usage.md")
        evals = self.read("skills/ops-browser/references/eval-cases.md")
        self.assertIn(
            "For a fixed route, known controls, repeatable capture, regression check, or external write, prefer deterministic APIs or Playwright",
            skill,
        )
        self.assertIn(
            "Browser-native/tool API or Playwright | Route, controls, assertions, or capture targets can be specified; the flow must be repeatable; an external write is authorized",
            usage,
        )
        self.assertIn("Uses an LLM browser agent only for open-ended read-oriented navigation", evals)
        self.assertIn("Uses agentic navigation for a fixed write flow", evals)

    def test_agentic_handoff_cannot_carry_write_authority(self) -> None:
        protocol = self.read("protocols/browser-operation-v1.md")
        self.assertIn("An LLM browser agent handoff must use", protocol)
        self.assertIn("`external_write: not-authorized`", protocol)
        self.assertIn("only read, navigate, and capture classes", protocol)
        self.assertIn("end the agentic handoff and require a new", protocol)
        self.assertIn("deterministic handoff with fresh identity, target, authorization, and operation ID", protocol)

    def test_provider_adapter_contract_is_linked_and_evaluated(self) -> None:
        adapter = self.read("skills/ask-ai/references/provider-adapter.md")
        skill = self.read("skills/ask-ai/SKILL.md")
        routing = self.read("skills/ask-ai/references/provider-routing.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        for operation in (
            "discover_target",
            "verify_identity",
            "resolve_context",
            "create_conversation",
            "submit",
            "capture_response",
            "reconcile_submission",
        ):
            with self.subTest(operation=operation):
                self.assertIn(f"{operation}:", adapter)
        self.assertIn("provider-adapter.md", skill)
        self.assertIn("ask-ai-provider-adapter/v1", routing)
        self.assertIn("Provider adapter conformance", evals)
        self.assertIn("Provider conversation reuse", evals)


if __name__ == "__main__":
    unittest.main()
