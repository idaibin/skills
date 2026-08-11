#!/usr/bin/env python3
"""Static contract checks for ask-ai CLI and Web research provider profiles."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / "scripts/probe-ask-ai-clis.py"
PROBE_SPEC = importlib.util.spec_from_file_location("probe_ask_ai_clis", PROBE_PATH)
assert PROBE_SPEC and PROBE_SPEC.loader
PROBE = importlib.util.module_from_spec(PROBE_SPEC)
PROBE_SPEC.loader.exec_module(PROBE)


class AskAIProviderProfileTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_skill_links_new_provider_profiles(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        self.assertIn("references/provider-cli.md", skill)
        self.assertIn("references/provider-web-research.md", skill)

    def test_first_tier_cli_roster_is_explicit(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        for provider in (
            "Google Antigravity",
            "Claude Code",
            "Qoder CLI Global",
            "Qoder CLI CN",
            "ZCode",
            "CodeBuddy Code",
            "Cursor CLI",
            "GitHub Copilot CLI",
            "Kiro CLI",
            "Factory Droid",
            "OpenCode",
        ):
            with self.subTest(provider=provider):
                self.assertIn(f"| {provider} |", profile)

    def test_cli_contract_fails_closed_on_dangerous_shortcuts(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        for term in (
            "exact `cwd`",
            "structured result/event/log metadata",
            "session ID",
            "submission-uncertain",
            "different repository or account",
            "flags such as `dangerously-skip-permissions`",
            "Argument binding",
            "Input reachability",
            "Timeout layers",
            "effective model",
            "must not enter an",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)

    def test_cli_profile_is_local_version_bound_and_repository_safe(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        for term in (
            "Configured Runtime Profiles",
            "user-owned `cli_profiles` record",
            "must not embed provider versions, model IDs, executable paths",
            "profile_digest:",
            "repository-bound resume",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)
        self.assertNotIn("Do not route `ZCode CLI`", profile)
        for forbidden in ("`zcode 0.16.1`", "claude-opus-4-6-thinking", "gemini-3.1-pro-high"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, profile)

    def test_cli_regressions_cover_model_attribution_and_known_invocation_drift(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        adapter = self.read("skills/ask-ai/references/provider-adapter.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        for term in (
            "installed help as a candidate contract",
            "configured, reverified values",
            "apply configured redaction",
            "Response prose",
            "host poll/yield expiry",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)
        for field in (
            "requested_model:",
            "effective_model:",
            "effective_reasoning:",
            "model_evidence:",
            "reasoning_evidence:",
            "model_match:",
            "reasoning_match:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, adapter)
        for scenario in (
            "output explains an option token",
            "Qoder cannot read a review package outside",
            "CLI model attribution and vote eligibility",
            "CLI timeout semantics",
        ):
            with self.subTest(scenario=scenario):
                self.assertIn(scenario, evals)

    def test_gemini_image_work_requires_exact_generation_and_editing_tool(self) -> None:
        image_routing = self.read("skills/ask-ai/references/image-routing.md")
        gemini = self.read("skills/ask-ai/references/provider-gemini.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        exact_tool = "「图片 — 图片生成与编辑」"
        for text in (image_routing, gemini, evals):
            with self.subTest(source=text[:40]):
                self.assertIn(exact_tool, text)
        for term in (
            "mode-select",
            "active mode after attachment",
            "does not apply to `image-review`",
        ):
            with self.subTest(term=term):
                self.assertIn(term, image_routing)
        for term in (
            "This is a hard target constraint",
            "immediately before submit",
            "stop `Not verified` before prompt submission",
        ):
            with self.subTest(term=term):
                self.assertIn(term, gemini)

    def test_qoder_variants_are_canonical_and_do_not_cross_fallback(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        routing = self.read("skills/ask-ai/references/provider-routing.md")
        for term in (
            "qoder-cli-global",
            "qoder-cli-cn",
            "supplies its own executable candidates",
            "CN profile rejects global-only evidence",
            "ambiguous family alias",
            "no cross-variant fallback",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)
        for term in (
            "provider_aliases",
            "default_provider: manual",
            "Never cross-fallback between the global",
            "never plain `Qoder`/`qoder`",
        ):
            with self.subTest(term=term):
                self.assertIn(term, routing)
        self.assertNotIn("qoder: qoder-cli-cn", routing)

    def test_web_profiles_cover_distinct_research_routes(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-web-research.md")
        for route in (
            "broad-deep-research",
            "source-bound-synthesis",
            "scholarly-discovery",
            "citation-context-check",
        ):
            with self.subTest(route=route):
                self.assertIn(f"`{route}`", profile)
        for provider in ("ChatGPT", "Gemini", "Perplexity", "NotebookLM", "Elicit", "Consensus", "Scite"):
            with self.subTest(provider=provider):
                self.assertIn(provider, profile)

    def test_source_gate_preserves_original_identity_and_uncertainty(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-web-research.md")
        for term in (
            "Claim-Evidence Ledger",
            "persistent_id: <DOI|PMID|PMCID|arXiv|ISBN|repository SHA|not-available>",
            "provider_support: <direct|partial|contextual|mismatched|missing>",
            "local_verification: <verified|inference|not-verified>",
            "unsupported extrapolation",
            "A valid DOI proves bibliographic identity, not correctness",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)

    def test_cli_discovery_probe_is_non_submitting_and_covers_roster(self) -> None:
        providers = {provider for provider, _, _ in PROBE.PROVIDERS}
        for provider in (
            "google-antigravity",
            "claude-code",
            "qoder-cli-global",
            "qoder-cli-cn",
            "zcode",
            "codebuddy-code",
            "cursor-cli",
            "github-copilot-cli",
            "kiro-cli",
            "factory-droid",
            "opencode",
        ):
            with self.subTest(provider=provider):
                self.assertIn(provider, providers)
        probe = self.read("scripts/probe-ask-ai-clis.py")
        self.assertIn('"scope": "discovery-only"', probe)
        self.assertIn('"runtime_conformance": "not-run"', probe)
        self.assertIn('"pass-with-stderr"', probe)
        self.assertIn('git", "diff", "--binary", "HEAD"', probe)
        self.assertIn('git", "check-ignore", "--quiet"', probe)
        self.assertNotIn('input("', probe)

    def test_qoder_probe_requires_variant_specific_identity_evidence(self) -> None:
        providers = dict((provider, candidates) for provider, candidates, _ in PROBE.PROVIDERS)
        self.assertEqual(("qodercli",), providers["qoder-cli-global"])
        self.assertEqual(
            ("qoderclicn", "qodercn", "qoder-cn", "qoder"),
            providers["qoder-cli-cn"],
        )
        self.assertIn("QODER_CN_MARKERS", self.read("scripts/probe-ask-ai-clis.py"))
        self.assertIn("identity_evidence", self.read("scripts/probe-ask-ai-clis.py"))

    def test_qoder_probe_rejects_cross_variant_identity(self) -> None:
        success = {"status": "pass", "output": "Qoder CLI 1.0"}
        cn_help = {"status": "pass", "output": "Qoder CLI CN 1.1.17\nUsage: qoderclicn"}
        cn_version = {"status": "pass", "output": "1.1.17"}
        global_identity, global_evidence = PROBE.qoder_identity(
            "qoder-cli-global", "/tmp/qodercli", success, cn_help
        )
        self.assertEqual("not-verified", global_identity)
        self.assertFalse(global_evidence["variant"])

        cn_generic_identity, cn_generic_evidence = PROBE.qoder_identity(
            "qoder-cli-cn", "/tmp/qoderclicn-1.1.17", success, success
        )
        self.assertEqual("not-verified", cn_generic_identity)
        self.assertFalse(cn_generic_evidence["variant"])

        cn_identity, cn_evidence = PROBE.qoder_identity(
            "qoder-cli-cn", "/tmp/qoderclicn-1.1.17", cn_version, cn_help
        )
        self.assertEqual("matched", cn_identity)
        self.assertTrue(all(cn_evidence.values()))

        bare_identity, bare_evidence = PROBE.qoder_identity(
            "qoder-cli-cn", "/tmp/qoder", cn_version, cn_help
        )
        self.assertEqual("not-verified", bare_identity)
        self.assertFalse(bare_evidence["path"])

        global_versioned_identity, global_versioned_evidence = PROBE.qoder_identity(
            "qoder-cli-global", "/tmp/qodercli-1.2.3", success, success
        )
        self.assertEqual("matched", global_versioned_identity)
        self.assertTrue(all(global_versioned_evidence.values()))

    def test_probe_fingerprint_detects_rewrites_of_an_already_modified_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            tracked = root / "tracked.txt"
            tracked.write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test-invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "base",
                ],
                cwd=root,
                check=True,
            )
            tracked.write_text("first change\n", encoding="utf-8")
            before = PROBE.git_fingerprint(root)
            tracked.write_text("second change\n", encoding="utf-8")
            self.assertNotEqual(before, PROBE.git_fingerprint(root))

    def test_probe_output_inside_repository_must_be_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            (root / ".gitignore").write_text(".codex/\n", encoding="utf-8")
            PROBE.validate_output_path(root, root / ".codex/artifact.json")
            with self.assertRaises(SystemExit):
                PROBE.validate_output_path(root, root / "artifact.json")


if __name__ == "__main__":
    unittest.main()
