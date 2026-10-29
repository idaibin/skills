#!/usr/bin/env python3
"""Static contract checks for ask-ai CLI and Web research provider profiles."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import plistlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_package_only_route_does_not_load_response_or_feedback_modules(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        route_map = skill.split("## Route Map\n", 1)[1].split("\n## Invariants", 1)[0]
        package_row = next(
            line for line in route_map.splitlines() if line.startswith("| Package-only review composition")
        )
        self.assertIn("references/review-prompts.md", package_row)
        self.assertNotIn("untrusted-content.md", package_row)
        self.assertNotIn("feedback-recording.md", package_row)
        self.assertIn("Returned external content is being inspected", route_map)
        self.assertIn("feedback recording is enabled", route_map)

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

    def test_cli_contract_preserves_native_capabilities_inside_verified_modes(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        for term in (
            "exact `cwd`",
            "structured result/event/log metadata",
            "session ID",
            "submission-uncertain",
            "different repository or account",
            "Native Execution Modes",
            "into a text-only model",
            "automatically approve operations",
            "disposable worktree",
            "Version Drift And Conformance Receipts",
            "exact fingerprint and profile digest",
            "`compatible-drift`",
            "SemVer alone",
            "at most once per new",
            "Write the receipt atomically",
            "Argument binding",
            "Input reachability",
            "Timeout layers",
            "effective model",
            "must not enter an",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)

    def test_web_payload_and_local_cli_directory_boundaries_are_distinct(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        cli = self.read("skills/ask-ai/references/provider-cli.md")
        handoff = self.read("skills/ask-ai/references/cli-artifact-handoff.md")
        adapter = self.read("skills/ask-ai/references/provider-adapter.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")

        self.assertIn("references/provider-cli.md", skill)
        self.assertIn("references/eval-cases.md", skill)
        self.assertIn("smallest self-contained redacted package", evals)
        self.assertIn("bind the exact verified repository/Worktree root", evals)
        self.assertIn("complete-directory read, search", cli)
        for text in (cli, handoff, adapter, evals):
            with self.subTest(source=text[:40]):
                normalized = " ".join(text.split())
                self.assertTrue(
                    "complete-directory" in normalized
                    or "complete selected directory" in normalized
                )
                self.assertTrue(
                    "file allowlist" in normalized
                    or "read allowlist" in normalized
                    or "file list" in normalized
                )
        self.assertIn("parent/home", cli)
        self.assertIn("persistent writes still require", cli)

    def test_cli_profile_is_local_version_bound_and_repository_safe(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        for term in (
            "Configured Runtime Profiles",
            "user-owned `cli_profiles` record",
            "construct the smallest",
            "negative option inventories",
            "profile_digest:",
            "repository-bound resume",
        ):
            with self.subTest(term=term):
                self.assertIn(term, profile)
        self.assertNotIn("Do not route `ZCode CLI`", profile)
        for forbidden in ("`zcode 0.16.1`", "claude-opus-4-6-thinking", "gemini-3.1-pro-high"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, profile)

    def test_agy_defaults_to_flash_with_complete_directory_permissions(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        self.assertIn("references/provider-cli.md", skill)
        for text in (profile, evals):
            normalized = " ".join(text.split())
            self.assertIn("Flash", normalized)
            self.assertTrue(
                "complete selected directory" in normalized
                or "complete-directory" in normalized
                or "whole selected directory" in normalized
            )
        self.assertIn("Select AGY Opus only when", profile)
        self.assertIn("--add-dir", profile)
        self.assertIn("--dangerously-skip-permissions", profile)
        self.assertIn("Do not select Pro, Sonnet, or Opus from task complexity", evals)

    def test_cli_execution_is_delegated_but_result_verification_stays_primary(self) -> None:
        skill = self.read("skills/ask-ai/SKILL.md")
        cli = self.read("skills/ask-ai/references/provider-cli.md")
        handoff = self.read("skills/ask-ai/references/cli-artifact-handoff.md")
        adapter = self.read("skills/ask-ai/references/provider-adapter.md")
        profile = self.read("skills/ask-ai/references/browser-profile.md")

        self.assertIn("references/cli-artifact-handoff.md", skill)
        self.assertIn("runtime-verified delegated CLI executor", handoff)
        self.assertIn("exactly one process start", cli)
        self.assertIn("provider result content remains unread by the executor", cli)
        self.assertIn("do not silently run locally or substitute another executor", cli)
        self.assertIn(
            "primary coordinator independently retrieves and reads",
            " ".join(handoff.split()),
        )
        self.assertIn("result_reader: <primary-coordinator", adapter)
        self.assertIn("execution_delegation: required | optional | disabled", profile)
        self.assertIn("executor_result_access: metadata-only", profile)

    def test_cli_regressions_cover_model_attribution_and_known_invocation_drift(self) -> None:
        profile = self.read("skills/ask-ai/references/provider-cli.md")
        adapter = self.read("skills/ask-ai/references/provider-adapter.md")
        evals = self.read("skills/ask-ai/references/eval-cases.md")
        for term in (
            "installed help as live candidate discovery",
            "minimum options",
            "task-local conformance evidence",
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
            "native_mode:",
            "native_capabilities:",
            "permission_strategy:",
            "persistence_boundary:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, adapter)
        for scenario in (
            "output explains an option token",
            "Qoder cannot read a review package outside",
            "provider response says no active workspace is set",
            "same CLI executable fingerprint and profile digest",
            "AGY moves from 1.1.13 to 1.1.14",
            "CLI model attribution and vote eligibility",
            "CLI timeout semantics",
            "CLI positive capability discovery",
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

    def make_discovery_fixture(self, directory: str) -> tuple[Path, Path, Path]:
        root = Path(directory)
        repository = root / "repository"
        repository.mkdir()
        subprocess.run(["git", "init", "--quiet"], cwd=repository, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test-invalid",
             "commit", "--quiet", "--allow-empty", "-m", "base"],
            cwd=repository, check=True,
        )
        bin_dir = root / "bin"
        bin_dir.mkdir()
        return repository, bin_dir, root / "invocations.jsonl"

    def write_probe_executable(self, path: Path, marker: Path, *, mutate: bool = False) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"#!{sys.executable}\n"
            "import json, sys\nfrom pathlib import Path\n"
            f"with Path({str(marker)!r}).open('a') as log:\n"
            "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "print('ZCode CLI fixture')\n"
            + ("if '--version' in sys.argv:\n"
               "    with Path(__file__).open('a') as target: target.write('\\n# changed\\n')\n"
               if mutate else ""),
            encoding="utf-8",
        )
        path.chmod(0o755)

    def discover_fixture(self, repository: Path, bin_dir: Path, *extra: str) -> dict:
        output = io.StringIO()
        with mock.patch.object(PROBE, "PROVIDERS", (("zcode", ("zcode",), ("zcode",)),)), \
             mock.patch.object(sys, "argv", [str(PROBE_PATH), "--repo", str(repository),
                                             "--bin-dir", str(bin_dir), *extra]), \
             contextlib.redirect_stdout(output):
            self.assertEqual(0, PROBE.main())
        return json.loads(output.getvalue())["providers"][0]

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_discovery_does_not_launch_an_unqualified_path_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            self.write_probe_executable(bin_dir / "zcode", marker)
            result = self.discover_fixture(repository, bin_dir)
            self.assertFalse(marker.exists(), "discovery executed an unqualified program")
            self.assertEqual("present", result["discovery"])
            self.assertEqual("not-verified", result["identity"])
            self.assertEqual("not-run", result["version"]["status"])
            self.assertEqual("not-run", result["help"]["status"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_qualified_cli_runs_only_version_and_help(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            executable = bin_dir / "zcode"
            self.write_probe_executable(executable, marker)
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(executable), digest)
            self.assertEqual([["--version"], ["--help"]],
                             [json.loads(line) for line in marker.read_text().splitlines()])
            self.assertEqual("matched", result["identity"])
            self.assertEqual("not-run", result["runtime_conformance"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_gui_main_symlink_is_not_started_even_with_a_matching_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            contents = Path(directory) / "ZCode.app" / "Contents"
            executable = contents / "MacOS" / "ZCode"
            self.write_probe_executable(executable, marker)
            (contents / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "ZCode"}))
            link = bin_dir / "zcode"
            link.symlink_to(executable)
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(link), digest)
            self.assertFalse(marker.exists())
            self.assertEqual("desktop-entrypoint", result["version"]["reason"])
            self.assertEqual("not-run", result["help"]["status"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_qualified_bundle_resource_cli_is_not_mistaken_for_the_gui(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            contents = Path(directory) / "ZCode.app" / "Contents"
            executable = contents / "Resources" / "cli" / "zcode"
            self.write_probe_executable(executable, marker)
            (contents / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "ZCode"}))
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(executable), digest)
            self.assertEqual("matched", result["identity"])
            self.assertEqual(2, len(marker.read_text().splitlines()))

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_gui_bundle_context_is_preserved_through_symlink_chains(self) -> None:
        for route in ("direct", "file-alias", "directory-alias"):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as directory:
                repository, bin_dir, marker = self.make_discovery_fixture(directory)
                outside = Path(directory) / "outside" / "desktop"
                self.write_probe_executable(outside, marker)
                contents = Path(directory) / "ZCode.app" / "Contents"
                launcher = contents / "MacOS" / "ZCode"
                launcher.parent.mkdir(parents=True)
                launcher.symlink_to(outside)
                (contents / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "ZCode"}))
                selected = launcher
                if route == "file-alias":
                    selected = bin_dir / "zcode"
                    selected.symlink_to(launcher)
                elif route == "directory-alias":
                    alias = bin_dir / "bundle-bin"
                    alias.symlink_to(launcher.parent, target_is_directory=True)
                    selected = alias / "ZCode"
                digest = hashlib.sha256(outside.read_bytes()).hexdigest()
                result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                               str(selected), digest)
                self.assertFalse(marker.exists())
                self.assertEqual("desktop-entrypoint", result["version"]["reason"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_truncated_bundle_metadata_returns_not_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            contents = Path(directory) / "ZCode.app" / "Contents"
            executable = contents / "MacOS" / "ZCode"
            self.write_probe_executable(executable, marker)
            (contents / "Info.plist").write_text('<?xml version="1.0"?><plist><dict>')
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(executable), digest)
            self.assertFalse(marker.exists())
            self.assertEqual("bundle-entrypoint-unverified", result["version"]["reason"])
            self.assertEqual("not-run", result["help"]["status"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_bundle_main_hardlink_alias_is_not_started(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            contents = Path(directory) / "ZCode.app" / "Contents"
            launcher = contents / "MacOS" / "ZCode"
            self.write_probe_executable(launcher, marker)
            alias = launcher.with_name("zcode-alias")
            os.link(launcher, alias)
            (contents / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "ZCode"}))
            digest = hashlib.sha256(alias.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(alias), digest)
            self.assertFalse(marker.exists())
            self.assertEqual("desktop-entrypoint", result["version"]["reason"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_invalid_qualified_entry_never_falls_back_to_path(self) -> None:
        for missing in (False, True):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as directory:
                repository, bin_dir, marker = self.make_discovery_fixture(directory)
                executable = bin_dir / "zcode"
                self.write_probe_executable(executable, marker)
                selected = Path(directory) / "missing-zcode" if missing else executable
                result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                               str(selected), "0" * 64)
                self.assertFalse(marker.exists())
                self.assertEqual("not-run", result["version"]["status"])
                self.assertEqual("not-run", result["help"]["status"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_executable_drift_after_version_blocks_help(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            executable = bin_dir / "zcode"
            self.write_probe_executable(executable, marker, mutate=True)
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(executable), digest)
            self.assertEqual([["--version"]],
                             [json.loads(line) for line in marker.read_text().splitlines()])
            self.assertEqual("pass", result["version"]["status"])
            self.assertEqual("not-run", result["help"]["status"])
            self.assertEqual("executable-digest-mismatch", result["help"]["reason"])
            self.assertEqual("not-verified", result["identity"])

    @unittest.skipUnless(os.name == "posix", "fixture uses an executable shebang")
    def test_symlink_target_drift_blocks_help_even_with_identical_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, bin_dir, marker = self.make_discovery_fixture(directory)
            first = Path(directory) / "first" / "zcode"
            second = Path(directory) / "second" / "zcode"
            alias = bin_dir / "zcode"
            self.write_probe_executable(first, marker)
            with first.open("a") as handle:
                handle.write(
                    "if '--version' in sys.argv:\n"
                    f"    Path({str(alias)!r}).unlink()\n"
                    f"    Path({str(alias)!r}).symlink_to({str(second)!r})\n"
                )
            second.parent.mkdir()
            second.write_bytes(first.read_bytes())
            second.chmod(0o755)
            alias.symlink_to(first)
            digest = hashlib.sha256(first.read_bytes()).hexdigest()
            result = self.discover_fixture(repository, bin_dir, "--verified-cli", "zcode",
                                           str(alias), digest)
            self.assertEqual([["--version"]],
                             [json.loads(line) for line in marker.read_text().splitlines()])
            self.assertEqual(str(first.resolve()), result["executable"])
            self.assertEqual("entrypoint-drift", result["help"]["reason"])
            self.assertEqual("not-verified", result["identity"])

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
