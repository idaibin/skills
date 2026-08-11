#!/usr/bin/env python3
"""Focused regressions for validate-skills.py."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-skills.py")
ROOT = SCRIPT.parent.parent
INDEX_SCHEMA = SCRIPT.parent.parent / "docs" / "skills" / "skills-index.schema.json"
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        package = root / "skills" / "sample-skill"
        (package / "references").mkdir(parents=True)
        (package / "agents").mkdir()
        (package / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Use when a sample needs processing.\n---\n"
            "# Sample\n\nSee [usage](references/usage.md) and "
            "[evals](references/eval-cases.md).\n",
            encoding="utf-8",
        )
        (package / "references" / "usage.md").write_text("# Usage\n", encoding="utf-8")
        (package / "references" / "eval-cases.md").write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "## Quality Eval\n\n- three\n",
            encoding="utf-8",
        )
        (package / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "Sample"\n'
            '  short_description: "Process representative samples"\n'
            '  default_prompt: "Use $sample-skill for this task."\n',
            encoding="utf-8",
        )
        (root / "skills.sh.json").write_text(
            json.dumps({"groupings": [{"title": "Samples", "skills": ["sample-skill"]}]}),
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "| Skill | Use when |\n| --- | --- |\n| `sample-skill` | sample |\n", encoding="utf-8"
        )
        (root / "INSTALL.md").write_text("- `skills/sample-skill`\n", encoding="utf-8")
        index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
        (root / "docs" / "skills").mkdir(parents=True)
        (root / "docs" / "skills" / "skills-index.schema.json").write_text(
            json.dumps(index_schema), encoding="utf-8"
        )
        (root / "skills-index.json").write_text(
            json.dumps(
                {
                    "version": 2,
                    "description": "Fixture discovery index.",
                    "categories": {
                        "samples": {
                            "title": "Samples",
                            "description": "Sample processing.",
                        }
                    },
                    "skills": [
                        {
                            "name": "sample-skill",
                            "category": "samples",
                            "owner": "sample-skill",
                            "mutation_class": "artifact-write",
                            "required_capabilities": ["filesystem-read", "artifact-write"],
                            "allowed_effects": ["read-repository", "write-artifact"],
                            "forbidden_effects": ["write-source", "write-git-state"],
                            "stop_states": ["scope-ambiguous", "evidence-incomplete"],
                            "intents": ["process a sample"],
                            "keywords": ["sample"],
                            "excludes": ["unrelated work"],
                            "related": [],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return root

    def test_valid_repository(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.make_repo()))

    def test_artifact_capability_requires_artifact_effect_for_control_owner(self) -> None:
        entry = {
            "name": "sample-browser",
            "owner": "sample-browser",
            "mutation_class": "browser-control",
            "required_capabilities": ["filesystem-read", "artifact-write", "browser-control"],
            "allowed_effects": ["read-repository", "control-browser-state"],
            "forbidden_effects": ["write-source", "write-git-state"],
            "stop_states": ["scope-ambiguous"],
        }
        errors = VALIDATOR.skill_contract_errors([entry])
        self.assertTrue(any("artifact-write must allow effect write-artifact" in error for error in errors))

    def test_ask_ai_defaults_require_strict_task_context_contract(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        package = Path(temporary.name) / "ask-ai"
        (package / "references").mkdir(parents=True)
        profile = package / "references" / "browser-profile.md"
        profile.write_text(
            "browser_preference:\n"
            "  primary: codex-in-app-browser | user-local-browser | manual\n"
            "  local_browser: <user-selected browser name>\n"
            "  fallback: user-local-browser | codex-in-app-browser | package-only\n"
            "fallback applies only to the current task.\n"
            "context_routes:\n"
            "  review:\n    name: <user-editable review Project/notebook name>\n"
            "    policy: prefer-verified-persistent | require-verified-persistent\n"
            "    fallback: new-standard-chat | package-only\n"
            "    provider_targets:\n"
            "      chatgpt: {surface: project, name: <optional ChatGPT Project name>}\n"
            "      gemini: {surface: notebook, name: <optional Gemini Notebook name>}\n"
            "  design:\n    name: <user-editable design Project/notebook name>\n"
            "    policy: prefer-verified-persistent | require-verified-persistent\n"
            "    fallback: new-standard-chat | package-only\n"
            "  image:\n    name: <user-editable image Project/notebook name>\n"
            "    policy: prefer-verified-persistent | require-verified-persistent\n"
            "    fallback: new-standard-chat | package-only\n"
            "standard_chat:\n  policy: allow-default | explicit-current-request-only\n"
            "cli_monitoring:\n"
            "  strategy: adaptive\n"
            "  short_task_poll_hint_seconds: <positive seconds>\n"
            "  long_task_poll_hint_seconds: <positive seconds>\n"
            "  preferred_wait_observer: <user-selected read-only role | none>\n"
            "  require_observer_runtime_identity: true\n"
            "provider_aliases:\n  <user alias>: <canonical provider>\n"
            "model_aliases:\n  <user model alias>: <installed model identifier>\n"
            "cli_profile:\n"
            "  executable_candidates: [<absolute path or command name>]\n"
            "  prompt_transport: argument | stdin | file\n"
            "  argument_order: <ordered option categories>\n"
            "  workspace:\n"
            "    option: <verified option>\n"
            "    value_source: current-task-repository\n"
            "    semantics: change-directory | add-directory\n"
            "  attribution_paths:\n"
            "  require_repository_binding: true\n"
            "  provider_deadline_seconds: <positive integer | null>\n"
            "  hard_process_deadline_seconds: <positive integer | null>\n"
            "  redact_log_fields: [<field or pattern>]\n"
            "persistent-context\n"
            "preserve unrelated\nvalid fields, write it atomically, then read back\n",
            encoding="utf-8",
        )
        self.assertEqual([], VALIDATOR.ask_ai_defaults_errors(package))
        profile.write_text("context_routes:\n", encoding="utf-8")
        errors = VALIDATOR.ask_ai_defaults_errors(package)
        self.assertTrue(any("codex-in-app-browser" in error for error in errors))
        self.assertTrue(any("user-selected browser" in error for error in errors))
        self.assertTrue(any("current task" in error for error in errors))
        self.assertTrue(any("review Project/notebook" in error for error in errors))
        self.assertTrue(any("design Project/notebook" in error for error in errors))
        self.assertTrue(any("prefer-verified-persistent" in error for error in errors))
        self.assertTrue(any("provider_targets" in error for error in errors))
        self.assertTrue(any("image Project/notebook" in error for error in errors))
        self.assertTrue(any("allow-default" in error for error in errors))
        self.assertTrue(any("cli_monitoring" in error for error in errors))
        self.assertTrue(any("cli_profile" in error for error in errors))
        self.assertTrue(any("persistent-context" in error for error in errors))
        self.assertTrue(any("write it atomically" in error for error in errors))

    def test_ask_ai_browser_preference_is_task_scoped_and_legacy_recoverable(self) -> None:
        profile = (
            ROOT / "skills" / "ask-ai" / "references" / "browser-profile.md"
        ).read_text(encoding="utf-8")
        chatgpt = (
            ROOT / "skills" / "ask-ai" / "references" / "provider-chatgpt.md"
        ).read_text(encoding="utf-8")
        protocol = (ROOT / "protocols" / "browser-operation-v1.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("fresh capability preflight on every new task", profile)
        self.assertIn("fallback applies only to the current task", profile)
        self.assertIn("ask-chatgpt-defaults/v2", profile)
        self.assertIn("requires\nexplicit authorization", profile)
        self.assertIn("does not probe Codex in-app first", chatgpt)
        for mode in (
            "codex-in-app-browser",
            "user-local-browser",
            "desktop-built-in-browser",
            "current-chrome-explicit",
        ):
            self.assertIn(mode, protocol)

    def test_ask_ai_cli_monitoring_is_adaptive_and_single_owner(self) -> None:
        source = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_cli_monitor_errors(source))
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ask-ai"
            (package / "references").mkdir(parents=True)
            provider_cli = package / "references" / "provider-cli.md"
            provider_cli.write_text("## Adaptive Monitoring\n", encoding="utf-8")
            errors = VALIDATOR.ask_ai_cli_monitor_errors(package)
            self.assertTrue(any("one minute" in error for error in errors))
            self.assertTrue(any("five" in error for error in errors))
            self.assertTrue(any("not fixed limits" in error for error in errors))
            self.assertTrue(any("read-only observer" in error for error in errors))
            self.assertTrue(any("effective role/model" in error for error in errors))

    def test_contract_tokens_tolerate_markdown_reflow(self) -> None:
        source = ROOT / "skills" / "ask-ai"
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ask-ai"
            shutil.copytree(source, package)
            provider_cli = package / "references" / "provider-cli.md"
            text = provider_cli.read_text(encoding="utf-8")
            provider_cli.write_text(
                text.replace("about five\nminutes", "about five minutes").replace(
                    "A quiet poll\nkeeps", "A quiet poll keeps"
                ),
                encoding="utf-8",
            )
            self.assertEqual([], VALIDATOR.ask_ai_cli_monitor_errors(package))

    def test_ops_browser_local_workspace_is_configurable_and_strict(self) -> None:
        source = ROOT / "skills" / "ops-browser"
        self.assertEqual([], VALIDATOR.ops_browser_workspace_errors(source))
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ops-browser"
            (package / "references").mkdir(parents=True)
            profile = package / "references" / "local-browser-workspaces.md"
            profile.write_text("schema_version: ops-browser-defaults/v1\n", encoding="utf-8")
            errors = VALIDATOR.ops_browser_workspace_errors(package)
            self.assertTrue(any("unified | by-operation" in error for error in errors))
            self.assertTrue(any("user-selected group name" in error for error in errors))
            self.assertTrue(any("create_if_missing" in error for error in errors))
            self.assertTrue(any("reuse_existing" in error for error in errors))
            self.assertTrue(any("allow_unconfigured_groups" in error for error in errors))
            self.assertTrue(any("allow_ungrouped" in error for error in errors))
            self.assertTrue(any("close_task_tabs_after_use" in error for error in errors))
            self.assertTrue(any("max_open_tabs_per_domain" in error for error in errors))
            self.assertTrue(any("session naming" in error for error in errors))
            self.assertTrue(any("capability-unavailable" in error for error in errors))

    def test_ask_ai_provider_aliases_are_optional_and_canonical(self) -> None:
        source = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_provider_variant_errors(source))
        for aliases in (
            "provider_aliases: {}\n",
            "provider_aliases:\n  qoder: qoder-cli-global\n",
            "provider_aliases:\n  qoder: qoder-cli-cn\n",
            "provider_aliases:\n  agy: google-antigravity\n  z: zcode\n",
        ):
            with self.subTest(aliases=aliases.strip()):
                with tempfile.TemporaryDirectory() as temporary:
                    package = Path(temporary) / "ask-ai"
                    shutil.copytree(source, package)
                    routing = package / "references" / "provider-routing.md"
                    routing.write_text(
                        routing.read_text(encoding="utf-8").replace(
                            "default_provider: manual\n",
                            f"default_provider: manual\n{aliases}",
                            1,
                        ),
                        encoding="utf-8",
                    )
                    self.assertEqual([], VALIDATOR.ask_ai_provider_variant_errors(package))

        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ask-ai"
            shutil.copytree(source, package)
            routing = package / "references" / "provider-routing.md"
            routing.write_text(
                routing.read_text(encoding="utf-8").replace(
                    "default_provider: manual\n",
                    "default_provider: manual\nprovider_aliases:\n  qoder: qoder-cli-unknown\n",
                    1,
                ),
                encoding="utf-8",
            )
            errors = VALIDATOR.ask_ai_provider_variant_errors(package)
            self.assertTrue(any("canonical providers" in error for error in errors))

    def test_ask_ai_authority_contract_matches_index_write_source_forbidden(self) -> None:
        source = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_authority_errors(source))

        def fixture(temporary: str) -> tuple[Path, Path]:
            root = Path(temporary)
            package = root / "skills" / "ask-ai"
            package.parent.mkdir(parents=True)
            shutil.copytree(source, package)
            shutil.copy(ROOT / "skills-index.json", root / "skills-index.json")
            return root, package

        with tempfile.TemporaryDirectory() as temporary:
            root, package = fixture(temporary)
            index_path = root / "skills-index.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            ask_ai = next(item for item in index["skills"] if item["name"] == "ask-ai")
            ask_ai["allowed_effects"].append("write-source")
            index_path.write_text(json.dumps(index), encoding="utf-8")
            errors = VALIDATOR.ask_ai_authority_errors(package)
        self.assertTrue(any("must not include write-source" in error for error in errors))

        with tempfile.TemporaryDirectory() as temporary:
            root, package = fixture(temporary)
            index_path = root / "skills-index.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            ask_ai = next(item for item in index["skills"] if item["name"] == "ask-ai")
            ask_ai["forbidden_effects"].remove("write-source")
            index_path.write_text(json.dumps(index), encoding="utf-8")
            errors = VALIDATOR.ask_ai_authority_errors(package)
        self.assertTrue(any("must include write-source" in error for error in errors))

        for relative, token in (
            ("SKILL.md", "Review and research default to no-write."),
            ("references/provider-cli.md", "implementation-owner-authorized"),
            ("references/eval-cases.md", "Review CLI write-source attempt"),
        ):
            with self.subTest(relative=relative):
                with tempfile.TemporaryDirectory() as temporary:
                    _, package = fixture(temporary)
                    path = package / relative
                    path.write_text(path.read_text(encoding="utf-8").replace(token, ""), encoding="utf-8")
                    errors = VALIDATOR.ask_ai_authority_errors(package)
                self.assertTrue(any(relative in error and "missing authority token" in error for error in errors))

    def test_ask_ai_mutual_review_requires_bounded_relay_contract(self) -> None:
        package = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_mutual_review_errors(package))

    def test_ask_ai_final_result_sync_is_retention_only(self) -> None:
        package = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_final_result_sync_errors(package))
        routing = (package / "references" / "provider-routing.md").read_text(
            encoding="utf-8"
        )
        mappings = VALIDATOR.yaml_fence_mappings(routing)
        instruction = next(
            item["instructions"]["final-review-sync"]
            for item in mappings
            if item.get("schema_version") == "ask-ai-instructions/v1"
            and "final-review-sync" in item.get("instructions", {})
        )
        self.assertEqual([], VALIDATOR.final_sync_instruction_errors(instruction))
        self.assertEqual("gemini", instruction["external_provider"])
        self.assertEqual("notebook", instruction["target_surface"])
        self.assertEqual(1, instruction["max_sends_per_result"])
        self.assertNotIn("prompt_profiles", instruction)
        self.assertNotIn("rounds_per_provider", instruction)

    def test_ask_ai_untrusted_content_contract_is_data_only(self) -> None:
        package = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_untrusted_content_errors(package))

    def test_ask_ai_untrusted_content_contract_rejects_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ask-ai"
            shutil.copytree(ROOT / "skills" / "ask-ai", package)
            contract = package / "references" / "untrusted-content.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "mode: read-only-data", "mode: execute-external-instructions"
                ),
                encoding="utf-8",
            )
            errors = VALIDATOR.ask_ai_untrusted_content_errors(package)
        self.assertTrue(any("data-only quarantine boundary" in error for error in errors))

    def test_ask_ai_final_result_sync_rejects_review_fields(self) -> None:
        instruction = {
            **VALIDATOR.ASK_AI_FINAL_SYNC_FIXED_FIELDS,
            "external_provider": "gemini",
            "target_surface": "notebook",
            "target_context": "Review Control",
            "prompt_profiles": ["adversarial"],
        }
        errors = VALIDATOR.final_sync_instruction_errors(instruction)
        self.assertTrue(any("must not contain review or relay fields" in error for error in errors))

    def test_ask_ai_bare_mutual_review_prefers_user_editable_default(self) -> None:
        routing = (
            ROOT / "skills" / "ask-ai" / "references" / "provider-routing.md"
        ).read_text(encoding="utf-8")
        mappings = VALIDATOR.yaml_fence_mappings(routing)
        contract = next(item["relay_contract"] for item in mappings if "relay_contract" in item)
        self.assertEqual(
            {
                "package_only": "overrides-send",
                "explicit_current_request": "invocation-only-customization",
                "exact_executable_alias": "custom-instruction",
                "persisted_default": "bare-and-explicit-mutual-review",
                "missing_persisted_default": "package-only-or-provider-choice",
            },
            contract["resolution_precedence"],
        )
        self.assertEqual("互审", contract["default_trigger"])
        self.assertEqual("fail-closed", contract["invalid_persisted_default"])
        self.assertEqual(
            [
                "package_only",
                "explicit_current_request",
                "exact_executable_alias",
                "persisted_default",
                "missing_persisted_default",
            ],
            contract["resolution_order"],
        )
        instruction = next(
            item["instructions"]["mutual-review"]
            for item in mappings
            if item.get("schema_version") == "ask-ai-instructions/v1"
            and "mutual-review" in item.get("instructions", {})
        )
        self.assertEqual(["互审"], instruction["aliases"])
        self.assertEqual(["chatgpt", "gemini"], instruction["external_providers"])
        self.assertEqual(3, instruction["max_turns_per_provider"])

    def test_ask_ai_accepts_persisted_bare_mutual_review_alias(self) -> None:
        source = (
            ROOT / "skills" / "ask-ai" / "references" / "provider-routing.md"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "ask-ai"
            references = package / "references"
            references.mkdir(parents=True)
            (references / "provider-routing.md").write_text(
                source,
                encoding="utf-8",
            )
            errors = VALIDATOR.ask_ai_mutual_review_errors(package)
        self.assertEqual([], errors)

    def test_ask_ai_v3_lifecycle_docs_and_discovery_index_are_synced(self) -> None:
        standard = (ROOT / "docs" / "skills" / "skill-standard.md").read_text(
            encoding="utf-8"
        )
        alignment = (
            ROOT / "docs" / "quality" / "official-skill-alignment.md"
        ).read_text(encoding="utf-8")
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        ask_ai = next(item for item in index["skills"] if item["name"] == "ask-ai")
        self.assertIn("distinct correlated create and submit logical IDs", standard)
        self.assertIn("distinct correlated\n  create and submit IDs", alignment)
        self.assertTrue(
            any(
                "bare 互审 uses only a valid user-persisted instruction" in item
                for item in ask_ai["intents"]
            )
        )

    def test_ask_ai_bare_mutual_review_text_uses_saved_default(self) -> None:
        sources = [
            ROOT / "skills" / "ask-ai" / "SKILL.md",
            ROOT / "skills" / "ask-ai" / "references" / "provider-routing.md",
            ROOT / "skills" / "ask-ai" / "references" / "usage.md",
            ROOT / "skills" / "ask-ai" / "references" / "eval-cases.md",
            ROOT / "skills-index.json",
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in sources)
        self.assertIn("user-editable persisted default", text)
        self.assertIn("persisted record is the user-editable default", text)
        self.assertIn("Package-only", text)
        self.assertNotIn("built-in ChatGPT", text)
        self.assertNotIn("ChatGPT then Gemini", text)
        self.assertNotIn("fixed bare-command contract", text)

    def test_owner_handoffs_do_not_freeze_an_incomplete_language_subset(self) -> None:
        product_spec = (ROOT / "skills" / "product-spec" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        frontend_audit = (
            ROOT / "skills" / "audit-frontend" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("matching\n  implementation owner", product_spec)
        self.assertNotIn("use `dev-frontend`\n  or `dev-rust`", product_spec)
        self.assertIn("matching backend implementation or\n  audit owner", frontend_audit)
        self.assertNotIn("backend-only Rust", frontend_audit)

    def test_ask_ai_app_native_relay_keeps_atomic_call_and_logical_operations_distinct(self) -> None:
        package = ROOT / "skills" / "ask-ai"
        self.assertEqual([], VALIDATOR.ask_ai_app_native_relay_errors(package))
        protocol = (
            package / "references" / "app-native-thread-protocol.md"
        ).read_text(encoding="utf-8")
        mappings = VALIDATOR.yaml_fence_mappings(protocol)
        contract = next(
            item["app_native_relay_contract"]
            for item in mappings
            if "app_native_relay_contract" in item
        )
        self.assertEqual(
            ["create-conversation", "submit-initial", "capture-response"],
            contract["initial_turn"]["logical_operations"],
        )
        self.assertEqual(
            {
                "before_host_call": "invoking",
                "normal_host_return": "submitted",
                "uncertain_host_return": "submission-uncertain",
            },
            contract["initial_turn"]["logical_write_projection"],
        )
        self.assertEqual(
            ["submit-follow-up", "capture-response"],
            contract["later_turn"]["logical_operations"],
        )
        self.assertTrue(contract["capture_response"]["idempotent"])

    def test_ask_ai_app_native_relay_contract_rejects_missing_or_merged_operations(self) -> None:
        source = (
            ROOT / "skills" / "ask-ai" / "references" / "app-native-thread-protocol.md"
        ).read_text(encoding="utf-8")
        mutations = {
            "missing-relay-turn": source.replace("    relay_turn: relay_turn_id\n", "", 1),
            "merged-create-submit": source.replace(
                "logical_operations: [create-conversation, submit-initial, capture-response]",
                "logical_operations: [create-and-initial-submit, capture-response]",
                1,
            ),
            "mutable-capture": source.replace("    idempotent: true\n", "    idempotent: false\n", 1),
        }
        for name, value in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                package = Path(temporary) / "ask-ai"
                references = package / "references"
                references.mkdir(parents=True)
                (references / "app-native-thread-protocol.md").write_text(
                    value, encoding="utf-8"
                )
                self.assertTrue(VALIDATOR.ask_ai_app_native_relay_errors(package))

    def test_ask_ai_eval_cases_do_not_describe_v2_as_current_or_combined_logical_operation(self) -> None:
        text = (
            ROOT / "skills" / "ask-ai" / "references" / "eval-cases.md"
        ).read_text(encoding="utf-8")
        for stale in (
            "app-native-thread-operation/v2` to host thread actions",
            "optional v2 evidence",
            "creates a v2 replacement",
            "one combined create-and-initial-submit operation",
            "App-native `create_thread` remains combined under its own protocol",
        ):
            self.assertNotIn(stale, text)
        self.assertIn("app-native-thread-operation/v3", text)
        self.assertIn("correlated but distinct `create-conversation` and `submit-initial`", text)

    def test_ask_ai_relay_instruction_rejects_noncanonical_stop(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 2,
            "stop_after": "first-provider-approves",
        }
        normalized, errors = VALIDATOR.normalize_relay_instruction(instruction)
        self.assertIsNone(normalized)
        self.assertTrue(any("all-providers-approve-same-candidate" in error for error in errors))

    def test_ask_ai_relay_instruction_requires_sequential_workflow_and_positive_turn_cap(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "stop_after": "all-providers-approve-same-candidate",
        }
        self.assertEqual([], VALIDATOR.relay_instruction_errors(instruction))
        three_provider = {
            **instruction,
            "external_providers": ["chatgpt", "gemini", "kimi"],
            "relay_order": ["chatgpt", "gemini", "kimi"],
        }
        self.assertEqual([], VALIDATOR.relay_instruction_errors(three_provider))
        instruction["workflow"] = "independent"
        self.assertTrue(any("workflow" in error for error in VALIDATOR.relay_instruction_errors(instruction)))
        instruction["workflow"] = "sequential-relay"
        for invalid_cap in (None, 0, -1, True, "1"):
            with self.subTest(invalid_cap=invalid_cap):
                if invalid_cap is None:
                    instruction.pop("max_turns_per_provider", None)
                else:
                    instruction["max_turns_per_provider"] = invalid_cap
                errors = VALIDATOR.relay_instruction_errors(instruction)
                self.assertTrue(any("max_turns_per_provider" in error for error in errors))

    def test_ask_ai_relay_instruction_rejects_invalid_promotion_and_roster(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "candidate_promotion": "automatic",
            "stop_after": "all-providers-approve-same-candidate",
        }
        self.assertTrue(any("candidate_promotion" in error for error in VALIDATOR.relay_instruction_errors(instruction)))
        instruction["external_providers"] = ["chatgpt"]
        instruction["relay_order"] = ["chatgpt"]
        self.assertTrue(any("two or more" in error for error in VALIDATOR.relay_instruction_errors(instruction)))

    def test_ask_ai_relay_instruction_rejects_non_string_or_invalid_relay_order_entries(self) -> None:
        instruction = {
            "workflow": "sequential-relay",
            "external_providers": ["chatgpt", "gemini"],
            "initial_provider": "chatgpt",
            "relay_order": ["chatgpt", "gemini"],
            "max_turns_per_provider": 1,
            "stop_after": "all-providers-approve-same-candidate",
        }
        invalid_orders = (
            [["chatgpt"], "gemini"],
            [{"provider": "chatgpt"}, "gemini"],
            ["", "gemini"],
            ["chatgpt", "chatgpt"],
            ["chatgpt", "kimi"],
            ["chatgpt", 7],
        )
        for relay_order in invalid_orders:
            with self.subTest(relay_order=relay_order):
                _, errors = VALIDATOR.normalize_relay_instruction(
                    {**instruction, "relay_order": relay_order}
                )
                self.assertTrue(any("relay_order" in error for error in errors))

    def test_browser_operation_protocol_keeps_relay_turn_action_hierarchy(self) -> None:
        source = ROOT / "protocols" / "browser-operation-v1.md"
        text = source.read_text(encoding="utf-8")
        for token in (
            "relay_turn_id",
            "conversation creation, attachment, submit,",
            "response capture, final marker",
            "one operation ID for multiple actions",
            "a new session is required",
            "Later turns for that same provider reuse that verified conversation",
            "original create operation ID",
        ):
            self.assertIn(token, text)
        for relative in (
            "skills/ask-ai/references/browser-operation-protocol.md",
            "skills/ops-browser/references/browser-operation-protocol.md",
        ):
            self.assertEqual(text, (ROOT / relative).read_text(encoding="utf-8"))

    def test_app_native_protocol_is_synced_from_the_shared_source(self) -> None:
        source = ROOT / "protocols" / "app-native-thread-operation-v3.md"
        target = ROOT / "skills" / "ask-ai" / "references" / "app-native-thread-protocol.md"
        self.assertEqual(source.read_text(encoding="utf-8"), target.read_text(encoding="utf-8"))

    def test_project_grounding_protocol_is_synced_and_semantically_bounded(self) -> None:
        source = ROOT / "protocols" / "project-grounding-v1.md"
        text = source.read_text(encoding="utf-8")
        for relative in (
            "skills/repo-map/references/project-grounding.md",
            "skills/repo-review/references/project-grounding.md",
            "skills/dev-frontend/references/project-grounding.md",
            "skills/dev-java/references/project-grounding.md",
            "skills/dev-rust/references/project-grounding.md",
            "skills/audit-frontend/references/project-grounding.md",
            "skills/audit-java/references/project-grounding.md",
            "skills/audit-rust/references/project-grounding.md",
        ):
            self.assertEqual(text, (ROOT / relative).read_text(encoding="utf-8"))
        evidence_and_status = text.split("## Evidence And Status\n", 1)[1].split(
            "\n## Owner Responsibilities", 1
        )[0]
        evidence_categories = (
            "**Declared:**",
            "**Source-resolved:**",
            "**Automated:**",
            "**Artifact-resolved:**",
            "**Runtime-resolved:**",
        )
        verification_states = (
            "**Verified within scope:**",
            "**Not verified:**",
            "**Not found within searched scope:**",
            "**Not applicable:**",
        )
        dispositions = ("**Block:**", "**Warn:**", "**Continue:**")
        evidence_section, remainder = evidence_and_status.split(
            "Record verification independently", 1
        )
        verification_section, disposition_and_floors = remainder.split(
            "Then record one action disposition:", 1
        )
        disposition_section, _ = disposition_and_floors.split(
            "Apply claim-specific evidence floors:", 1
        )

        def definition_markers(section: str) -> tuple[str, ...]:
            return tuple(re.findall(r"^- (\*\*[^\n]+?:\*\*)", section, re.MULTILINE))

        self.assertEqual(evidence_categories, definition_markers(evidence_section))
        self.assertEqual(verification_states, definition_markers(verification_section))
        self.assertEqual(dispositions, definition_markers(disposition_section))
        runtime_qualifiers = re.search(
            r"\*\*Runtime-resolved:\*\*.*?Qualify it as\n  (?P<values>.*?) and record",
            evidence_section,
            re.DOTALL,
        )
        self.assertIsNotNone(runtime_qualifiers)
        qualifiers = tuple(re.findall(r"`([^`]+)`", runtime_qualifiers.group("values")))
        self.assertEqual(("local", "target-like", "deployed:<environment>"), qualifiers)
        self.assertEqual(3, len(set(qualifiers)))
        self.assertIn("none of these qualifiers implies another.", evidence_and_status)
        floors_section = disposition_and_floors.split("Apply claim-specific evidence floors:\n", 1)[1].split(
            "\n\nA completion claim", 1
        )[0]
        floors = tuple(
            match.group("floor")
            for match in re.finditer(r"^- (?P<floor>.*(?:\n  .*)*)", floors_section, re.MULTILINE)
        )
        self.assertEqual(
            (
                "packaged/generated completion requires `Artifact-resolved` evidence for the named\n  output;",
                "deployed or production behavior requires `Runtime-resolved(deployed:<environment>)`\n  evidence from that named environment;",
                "migration compatibility requires the applicable dialect/data basis, migration path,\n  and compatibility evidence; a clean-schema test alone is insufficient for existing\n  data;",
                "cross-repository integration requires evidence from the affected provider-consumer\n  seam at compatible revisions;",
                "rollout and rollback readiness require their own exercised evidence or remain\n  separately `Not verified`.",
            ),
            floors,
        )
        self.assertIn(
            "A completion claim must be narrowed to the strongest supported evidence level.",
            evidence_and_status,
        )
        self.assertIn(
            "Never upgrade static or local evidence into production readiness.", evidence_and_status
        )
        self.assertIn("signal -> affected invariant -> owner/authority ->", text)
        self.assertIn("within or across repositories", text)
        self.assertIn(
            "Do not activate it merely because a repository contains Java/frontend/config files.",
            text,
        )

    def test_project_grounding_owner_skills_disclose_activation_and_reference(self) -> None:
        for skill in (
            "repo-map",
            "repo-review",
            "dev-frontend",
            "dev-java",
            "dev-rust",
            "audit-frontend",
            "audit-java",
            "audit-rust",
        ):
            with self.subTest(skill=skill):
                text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("references/project-grounding.md", text)
                self.assertIn("Not verified", text)

    def test_project_grounding_owner_evals_and_index_keep_owner_action_distinct(self) -> None:
        expected = {
            "repo-map": (
                "Map the stable owners and verification entry points for profiles, packaged resources, schema compatibility, gateway contracts, and cross-repo delivery; do not claim the target runtime was tested.",
                "Trigger Repo Map with project grounding for stable routing facts.",
                "List the top-level directories and owning manifests; do not map runtime, data, integration, compatibility, or delivery authorities.",
                "Keep project grounding inactive and return the bounded navigation answer.",
            ),
            "repo-review": (
                "Review this fixed range that adds requirements, schema, implementation, tests, and a replacement route together.",
                "Trigger project grounding; treat same-basis artifacts as intent and require independent compatibility/migration evidence before readiness.",
                "Review this Markdown typo-only range; no executable contract changed.",
                "Keep runtime, schema, integration, and migration grounding `Not applicable`; do not inflate the review.",
            ),
            "dev-frontend": (
                "Wire this page to the real backend route; the dev proxy, production gateway context path, auth source, and loading/error/permission states differ.",
                "Trigger `dev-frontend` with project grounding before edits.",
                "Change only a local CSS color token; reachable API, build, runtime, and cross-repository contracts stay unchanged.",
                "Keep project-grounding risk classes `Not applicable`; do not scan unrelated repositories or deployment state.",
            ),
            "dev-java": (
                "Make this Spring service's local startup work by changing service discovery and packaged profile behavior; production must remain registered.",
                "Trigger Runtime/config grounding, resolve precedence and artifact/target boundaries, and block a global workaround until its scope is proven.",
                "Change only a Java comment; no behavior, build, config, or contract changes.",
                "Keep project-grounding risk classes `Not applicable`; do not run environment or migration checks.",
            ),
            "dev-rust": (
                "Change this Rust service's startup configuration, packaged resource precedence, and compatible consumer rollout.",
                "Trigger `dev-rust` with project grounding before edits.",
                "Rename only a private Rust helper; no reachable runtime, packaging, API, persistence, or cross-repository behavior changes.",
                "Keep project-grounding risk classes `Not applicable`; do not scan deployment or consumer repositories.",
            ),
            "audit-frontend": (
                "Audit this Vue app's client route against the backend controller, gateway context, auth scope, production config, and failure states.",
                "Trigger State/Data plus Build/Tooling and project grounding for the bounded provider/consumer chain.",
                "Audit only a local CSS color token rename with no reachable API, build, runtime, or cross-repo effect.",
                "Keep project grounding inactive and unrelated profiles out of scope.",
            ),
            "audit-java": (
                "Audit whether this Java service's source profiles, packaged resources, startup exclusions, and target service registration resolve consistently.",
                "Trigger Build/Migration plus project grounding; keep source, artifact, and runtime evidence distinct.",
                "Audit this Java DTO naming only; no runtime, persistence, public contract, or cross-repo behavior is in scope.",
                "Keep project grounding inactive; do not scan profiles, schemas, or sibling repositories.",
            ),
            "audit-rust": (
                "Audit this Rust service's packaged configuration, startup registration, durable migration compatibility, and consumer handoff.",
                "Trigger `audit-rust` with project grounding; keep source, artifact, and runtime evidence distinct.",
                "Audit only a private Rust naming cleanup with no reachable runtime, packaging, API, persistence, or cross-repository effect.",
                "Keep project grounding inactive and unrelated profiles out of scope.",
            ),
        }
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        indexed = {item["name"]: item for item in index["skills"]}

        def table_rows(section: str) -> dict[str, str]:
            rows: dict[str, str] = {}
            for line in section.splitlines():
                if not line.startswith("|") or line.startswith("| ---"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) >= 2:
                    rows[cells[0].strip("`")] = cells[1]
            return rows

        for skill, (
            trigger_prompt,
            trigger_expected,
            non_trigger_prompt,
            non_trigger_expected,
        ) in expected.items():
            with self.subTest(skill=skill):
                evals = (ROOT / "skills" / skill / "references" / "eval-cases.md").read_text(
                    encoding="utf-8"
                )
                trigger = table_rows(
                    evals.split("## Trigger Eval", 1)[1].split("## Non-Trigger Eval", 1)[0]
                )
                non_trigger = table_rows(
                    evals.split("## Non-Trigger Eval", 1)[1].split("## ", 1)[0]
                )
                self.assertEqual(trigger_expected, trigger[trigger_prompt])
                self.assertEqual(non_trigger_expected, non_trigger[non_trigger_prompt])
                self.assertTrue(indexed[skill]["intents"])

    def test_project_grounding_index_is_owner_qualified_and_not_literal_routing(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        indexed = {item["name"]: item for item in index["skills"]}
        owners = (
            "repo-map",
            "repo-review",
            "dev-frontend",
            "dev-java",
            "dev-rust",
            "audit-frontend",
            "audit-java",
            "audit-rust",
        )
        for owner in owners:
            with self.subTest(owner=owner):
                self.assertNotIn("project grounding", indexed[owner]["keywords"])
        self.assertIn("grounded repository ownership map", indexed["repo-map"]["keywords"])
        self.assertIn("multi-identity repository map", indexed["repo-map"]["keywords"])
        self.assertIn("canonical ownership identity map", indexed["repo-map"]["keywords"])
        self.assertIn("documentation-authority rebuild map", indexed["repo-map"]["keywords"])
        self.assertIn("grounded fixed-basis review", indexed["repo-review"]["keywords"])

    def test_repo_delivery_grounding_record_never_inverts_git_authority(self) -> None:
        skill = (ROOT / "skills" / "repo-delivery" / "SKILL.md").read_text(encoding="utf-8")
        evals = (ROOT / "skills" / "repo-delivery" / "references" / "eval-cases.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "A grounding record may identify evidence gaps, but it never authorizes stage, commit, push,\n  integration, cleanup, or pull-request actions.",
            skill,
        )
        trigger = evals.split("## Trigger Eval\n", 1)[1].split("\n## Non-Trigger Eval", 1)[0]
        non_trigger = evals.split("## Non-Trigger Eval\n", 1)[1].split("\n## Quality Eval", 1)[0]
        quality = evals.split("## Quality Eval\n", 1)[1]
        self.assertIn("grounding record", trigger.lower())
        self.assertIn("stage and commit", trigger.lower())
        self.assertIn("grounding record", non_trigger.lower())
        self.assertIn("do not stage, commit, push, or open a pull request", non_trigger.lower())
        self.assertIn("Grounding-record authority", quality)
        self.assertIn("requires independent Git-delivery authority", quality)

    def test_name_must_match_directory(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text().replace("name: sample-skill", "name: other-skill"))
        self.assertTrue(any("name must match" in error for error in VALIDATOR.validate(root)))

    def test_broken_local_link_fails(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text() + "\n[missing](references/missing.md)\n")
        self.assertTrue(any("broken link" in error for error in VALIDATOR.validate(root)))

    def test_eval_requires_three_scenarios(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(evals.read_text().replace("## Quality Eval", "## Examples"))
        self.assertTrue(any("Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_sections_must_have_content(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(evals.read_text().replace("## Quality Eval\n\n- three", "## Quality Eval"))
        self.assertTrue(any("empty ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_must_be_exact(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "## Quality Eval Notes\n\n- not the required section\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_outside_code_fence(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "```text\n## Quality Eval\n```\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_outside_tilde_fence(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "~~~text\n## Quality Eval\n~~~\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_eval_heading_inside_indented_code(self) -> None:
        root = self.make_repo()
        evals = root / "skills" / "sample-skill" / "references" / "eval-cases.md"
        evals.write_text(
            "# Evals\n\n## Trigger Eval\n\n- one\n\n## Non-Trigger Eval\n\n- two\n\n"
            "    ## Quality Eval\n"
        )
        self.assertTrue(any("missing ## Quality Eval" in error for error in VALIDATOR.validate(root)))

    def test_package_install_command_fails(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text("Run npx skills add example/repo\n")
        self.assertTrue(any("installation commands" in error for error in VALIDATOR.validate(root)))

    def test_catalog_sets_must_match(self) -> None:
        root = self.make_repo()
        (root / "skills.sh.json").write_text(json.dumps({"groupings": []}))
        self.assertTrue(any("skills.sh.json package set differs" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_set_must_match(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"] = []
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("skills-index.json" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_related_skill_must_exist(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["related"] = ["missing-skill"]
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("unknown related Skills" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_category_must_exist(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["category"] = "missing-category"
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("unknown category" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_rejects_self_relation(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["skills"][0]["related"] = ["sample-skill"]
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(any("cannot relate to itself" in error for error in VALIDATOR.validate(root)))

    def test_skill_index_category_must_match_distribution_group(self) -> None:
        root = self.make_repo()
        distribution = json.loads((root / "skills.sh.json").read_text())
        distribution["groupings"][0]["title"] = "Different Group"
        (root / "skills.sh.json").write_text(json.dumps(distribution))
        self.assertTrue(
            any("category titles differ" in error for error in VALIDATOR.validate(root))
        )

    def test_skill_index_rejects_duplicate_category_titles(self) -> None:
        root = self.make_repo()
        index = json.loads((root / "skills-index.json").read_text())
        index["categories"]["other"] = {
            "title": "Samples",
            "description": "Another category.",
        }
        index["skills"][0]["category"] = "other"
        (root / "skills-index.json").write_text(json.dumps(index))
        self.assertTrue(
            any("duplicate category titles" in error for error in VALIDATOR.validate(root))
        )

    def test_openai_metadata_requires_interface_root(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text().replace("interface:", "wrong_root:"))
        self.assertTrue(any("interface mapping" in error for error in VALIDATOR.validate(root)))

    def test_openai_short_description_length_is_checked(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text().replace("Process representative samples", "Too short"))
        self.assertTrue(any("25-64 characters" in error for error in VALIDATOR.validate(root)))

    def test_openai_explicit_only_policy_is_valid(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + "policy:\n  allow_implicit_invocation: false\n",
            encoding="utf-8",
        )
        self.assertEqual([], VALIDATOR.validate(root))

    def test_openai_invocation_policy_requires_boolean(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + 'policy:\n  allow_implicit_invocation: "false"\n',
            encoding="utf-8",
        )
        self.assertTrue(
            any("allow_implicit_invocation must be a boolean" in error for error in VALIDATOR.validate(root))
        )

    def test_openai_invocation_policy_rejects_null_value(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text() + "policy:\n  allow_implicit_invocation:\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any("allow_implicit_invocation must be a boolean" in error for error in VALIDATOR.validate(root))
        )

    def test_openai_invocation_policy_rejects_null_mapping(self) -> None:
        root = self.make_repo()
        metadata = root / "skills" / "sample-skill" / "agents" / "openai.yaml"
        metadata.write_text(metadata.read_text() + "policy:\n", encoding="utf-8")
        self.assertTrue(
            any("top-level policy must be a mapping" in error for error in VALIDATOR.validate(root))
        )

    def test_unknown_frontmatter_field_fails(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text().replace("name: sample-skill", "name: sample-skill\nowner: team"))
        self.assertTrue(any("unsupported frontmatter" in error for error in VALIDATOR.validate(root)))

    def test_portable_optional_fields_are_typed(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text().replace(
                "name: sample-skill",
                "name: sample-skill\ncompatibility: 42\nmetadata:\n  version: 1",
            )
        )
        errors = VALIDATOR.validate(root)
        self.assertTrue(any("compatibility" in error for error in errors))
        self.assertTrue(any("metadata must map strings to strings" in error for error in errors))

    def test_long_reference_requires_contents(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text("# Usage\n" + "detail\n" * 101)
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_exact_contents_heading(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "## Contents List\n\n- item one\n- item two\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_contents_outside_fence(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "```text\n## Contents\n\n- item one\n```\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_requires_contents_tilde_fence(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "~~~text\n## Contents\n\n- item one\n~~~\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_long_reference_contents_in_indented_code(self) -> None:
        root = self.make_repo()
        usage = root / "skills" / "sample-skill" / "references" / "usage.md"
        usage.write_text(
            "# Usage\n"
            + "detail\n" * 101
            + "    ## Contents\n\n- item one\n"
        )
        self.assertTrue(any("needs a ## Contents" in error for error in VALIDATOR.validate(root)))

    def test_block_scalar_description_is_valid(self) -> None:
        root = self.make_repo()
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text().replace(
                "description: Use when a sample needs processing.",
                "description: |\n  Use when a sample needs processing.\n  Handles a representative input.",
            )
        )
        self.assertEqual([], VALIDATOR.validate(root))


if __name__ == "__main__":
    unittest.main()
