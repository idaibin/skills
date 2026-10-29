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
            "worker_runtime_model:",
            "ownership_key:",
            "tab_owner:",
            "owner_id:",
            "exclusive:",
            "restoration:",
            "post_readback:",
            "response_capture:",
            "response_container_id:",
            "file_sha256:",
            "readback_verified:",
        ):
            with self.subTest(term=term):
                self.assertIn(term, protocol)

    def test_fixed_external_writes_remain_deterministic_first(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        usage = self.read("skills/ops-browser/references/usage.md")
        evals = self.read("skills/ops-browser/references/eval-cases.md")
        self.assertIn("references/usage.md", skill)
        self.assertIn(
            "Browser-native/tool API or Playwright | Route, controls, assertions, or capture targets can be specified; the flow must be repeatable; an external write is authorized",
            usage,
        )
        self.assertIn("Uses an LLM browser agent only for open-ended read-oriented navigation", evals)
        self.assertIn("Uses agentic navigation for a fixed write flow", evals)

    def test_viewport_requirement_separates_resolution_from_shared_state_control(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        policy = self.read("skills/ops-browser/references/viewport-policy.md")
        evals = self.read("skills/ops-browser/references/eval-cases.md")
        usage = self.read("skills/ops-browser/references/usage.md")
        lifecycle = self.read("skills/ops-browser/references/tab-lifecycle.md")
        self.assertIn(
            "Any browser operation | [platform operations](references/platform-operations.md), [tab lifecycle](references/tab-lifecycle.md), and [viewport policy](references/viewport-policy.md)",
            skill,
        )
        for term in (
            "an effective host or personal default",
            "for an independently isolated browser only, the package fallback:",
            "`1920 x 1080` CSS pixels for desktop Web",
            "`iPhone 15` portrait device profile for mobile Web",
            "explicit user authorization; a requested viewport or task-owned tab is insufficient.",
            "`window.innerWidth` and `window.innerHeight`",
            "matching width and height alone does not prove",
            "device profile is active",
        ):
            with self.subTest(term=term):
                self.assertIn(term, policy)
        self.assertIn("Resolve viewport control authority from host policy and user authorization", skill)
        self.assertIn("Applies effective host policy; unknown or prohibited shared-state changes", evals)
        self.assertIn("changes shared user browser state", evals)
        self.assertIn("only within verified host policy and user authority", lifecycle)
        self.assertIn("Cleanup does not enlarge viewport control authority", usage)

    def test_explicit_deterministic_fixture_routes_before_navigation(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        mock = " ".join(self.read("skills/ops-browser/references/network-mock.md").split())
        route = next(line for line in skill.splitlines() if "[Network Mock]" in line)
        self.assertIn("explicitly authorized deterministic frontend fixtures", route)
        self.assertIn("install request-stage protection before navigation", mock)
        self.assertIn("no real API failure is required", mock)
        self.assertIn("Record the authorization source, target and allowed effects with the run evidence", mock)
        self.assertIn("stop if that authority is unverified", mock)
        self.assertNotIn("Observe real APIs first. When an API fails", mock)

    def test_ordinary_real_service_diagnosis_does_not_automatically_mock(self) -> None:
        mock = " ".join(self.read("skills/ops-browser/references/network-mock.md").split())
        self.assertIn("For ordinary real-service diagnosis, observe real APIs first", mock)
        self.assertIn("synthetic inputs are within the task's accepted scope", mock)
        self.assertIn("valid empty business results separately; they are not defects", mock)
        self.assertIn("does not implement missing UI or prove real-service integration", mock)

    def test_mock_keeps_contract_unknown_request_and_provenance_boundaries(self) -> None:
        mock = " ".join(self.read("skills/ops-browser/references/network-mock.md").split())
        self.assertIn("If a required contract is missing, retain that gap rather than inventing", mock)
        self.assertIn("Unknown rules, invalid fixtures and handler errors never fall back to the real network", mock)
        self.assertIn("a consumer-derived shape remains distinct from a formal contract", mock)
        self.assertIn("contract source/version", mock)
        self.assertIn("known gaps", mock)
        self.assertIn("Mock never broadens production write authority", mock)

    def test_adapter_qualification_reuses_matching_proof_without_dropping_controls(self) -> None:
        mock = " ".join(self.read("skills/ops-browser/references/network-mock.md").split())
        self.assertIn("Qualify the adapter on first use or after version/capability drift", mock)
        self.assertIn("reuse matching proof across business cases", mock)
        self.assertIn("Verify each invocation's target/connection epoch, coverage and isolation remain within that proof", mock)
        self.assertIn("worker/service-worker, extension and proxy changes", mock)
        for control in ("cross-context negative controls", "warm HTTP cache hit", "cold read in the other context",
            "one event consumer/cursor", "atomic pause claim tied to connection epoch", "record stale IDs without retrying them"):
            self.assertIn(control, mock)

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

    def test_explicit_fixed_local_route_has_no_implicit_fallback(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        workspace = self.read(
            "skills/ops-browser/references/local-browser-workspaces.md"
        )
        evals = self.read("skills/ops-browser/references/eval-cases.md")
        source = skill + workspace + evals
        for term in (
            "explicit current-request surface",
            "configured Chrome extension",
            "existing Profile",
            "stop `Not verified`",
        ):
            with self.subTest(term=term):
                self.assertIn(term, source)
        self.assertIn("Normal user-local route", evals)
        self.assertIn("Critical stop preserves route", evals)

    def test_project_work_and_cloud_environment_targets_do_not_alias(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        provider = self.read("skills/ask-ai/references/provider-chatgpt.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        source = skill + provider
        for term in (
            "`project-work`",
            "`cloud-environment-settings`",
            "/codex/cloud/settings/environment",
            "forbidden for `project-work`",
        ):
            with self.subTest(term=term):
                self.assertIn(term, source)
        self.assertIn("Never visit environment settings", evals)
        self.assertIn("different target kind and cannot recover", evals)

    def test_target_binding_and_canonical_restoration_are_cross_package(self) -> None:
        paths = (
            "skills/ops-browser/references/local-browser-workspaces.md",
            "skills/ask-ai/references/provider-chatgpt.md",
        )
        for path in paths:
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("target kind", text.lower())
                self.assertIn("tab identity", text)
                self.assertIn("restoration", text.lower())
                self.assertIn("fingerprint", text.lower())

        self.assertIn("references/local-browser-workspaces.md", self.read("skills/ops-browser/SKILL.md"))
        self.assertIn("references/provider-chatgpt.md", self.read("skills/ask-ai/SKILL.md"))

        for path in (
            "skills/ops-browser/references/eval-cases.md",
            "skills/ask-ai/references/eval-cases.md",
        ):
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("Canonical restoration record", text)
                self.assertIn("old, duplicate, or conflicting", text)

    def test_protocol_requires_closed_local_preflight_and_completion_receipt(self) -> None:
        protocol = self.read("protocols/browser-operation-v1.md")
        for term in (
            "connected extension connector",
            "verified account/session",
            "exact tab identity",
            "native group identity",
            "cannot return `ready` or authorize `claim_verified_tab`",
            "debug enablement or initialization",
            "canonical restoration receipt",
            "remain `captured`",
        ):
            with self.subTest(term=term):
                self.assertIn(term, protocol)


if __name__ == "__main__":
    unittest.main()
