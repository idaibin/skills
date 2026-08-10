#!/usr/bin/env python3
"""Validate the catalog against the portable Agent Skills and OpenAI surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CATALOG_ROW_RE = re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)
INSTALL_PATH_RE = re.compile(r"^- `skills/([a-z0-9-]+)`$", re.MULTILINE)
ROUTE_RE = re.compile(r"\$([a-z][a-z0-9-]*)")
EVAL_HEADINGS = ("## Trigger Eval", "## Non-Trigger Eval", "## Quality Eval")
FENCE_RE = re.compile(r"^(?P<indent>[ ]{0,3})(?P<fence>`{3,}|~{3,})(?P<rest>.*)$")
HEADING_RE = re.compile(r"^(?P<indent>[ ]{0,3})##\s+(?P<title>.*?)\s*$")
FORBIDDEN_PACKAGE_FILES = {"README.md", "INSTALL.md", "INSTALLATION_GUIDE.md", "CHANGELOG.md"}
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LONG_REFERENCE_LINES = 100
ASK_AI_DEFAULT_TOKENS = (
    "browser_preference:",
    "primary: codex-in-app-browser | user-local-browser | manual",
    "local_browser: <user-selected browser name>",
    "fallback: user-local-browser | codex-in-app-browser | package-only",
    "fallback applies only to the current task",
    "review_context:",
    "name: <user-editable default persistent context name>",
    "policy: prefer-verified-persistent",
    "fallback: new-standard-chat",
)
ASK_AI_CANONICAL_STOP_AFTER = "all-providers-approve-same-candidate"
ASK_AI_PROMOTION_VALUES = {"user-only", "provider-authored-textual-revision"}
ASK_AI_FINAL_SYNC_FIXED_FIELDS = {
    "workflow": "final-result-sync",
    "trigger": "after-final-local-review",
    "package_policy": "sanitized-final-review-result-only",
    "authorization": "send-after-final-local-review",
    "max_sends_per_result": 1,
    "response_policy": "receipt-only-non-authoritative",
    "stop_after": "sync-recorded-or-incomplete",
}

MUTATION_CLASSES = {
    "read-only",
    "artifact-write",
    "source-write",
    "git-write",
    "browser-control",
    "client-control",
    "external-action",
}
MUTATION_CAPABILITIES = {
    "read-only": set(),
    "artifact-write": {"artifact-write"},
    "source-write": {"source-write"},
    "git-write": {"git-write"},
    "browser-control": {"browser-control"},
    "client-control": {"client-control"},
    "external-action": {"external-provider"},
}
CONTRACT_EFFECT_BY_MUTATION = {
    "read-only": set(),
    "artifact-write": {"write-artifact"},
    "source-write": {"write-source"},
    "git-write": {"write-git-state"},
    "browser-control": {"control-browser-state"},
    "client-control": {"control-client-state"},
    "external-action": {"invoke-external-provider"},
}
CAPABILITY_EFFECTS = {
    "artifact-write": "write-artifact",
    "source-write": "write-source",
    "git-write": "write-git-state",
    "browser-control": "control-browser-state",
    "client-control": "control-client-state",
    "external-provider": "invoke-external-provider",
}


def frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if match is None:
        raise ValueError("missing or invalid YAML frontmatter delimiters")
    try:
        values = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(values, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return values, text[match.end() :]


def openai_interface(path: Path) -> dict[str, str]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("interface"), dict):
        raise ValueError("top-level interface mapping is required")
    interface = payload["interface"]
    return {
        field: value
        for field in ("display_name", "short_description", "default_prompt")
        if isinstance((value := interface.get(field)), str)
    }


def openai_invocation_policy(path: Path) -> bool | None:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("top-level mapping is required")
    if "policy" not in payload:
        return None
    policy = payload["policy"]
    if not isinstance(policy, dict):
        raise ValueError("top-level policy must be a mapping")
    if "allow_implicit_invocation" not in policy:
        return None
    value = policy["allow_implicit_invocation"]
    if not isinstance(value, bool):
        raise ValueError("policy.allow_implicit_invocation must be a boolean")
    return value


def section_has_content(text: str, heading: str) -> bool:
    lines = text.splitlines()
    in_code_fence = False
    fence_char: str = ""
    fence_len: int = 0
    start = None
    for i, line in enumerate(lines):
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _heading_matches(line, heading):
            start = i
            break
    if start is None:
        return False

    for line in lines[start + 1 :]:
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _is_h2_heading(line):
            return False
        if line.strip():
            return True
    return False


def has_exact_h2_heading(text: str, heading: str) -> bool:
    in_code_fence = False
    fence_char: str = ""
    fence_len: int = 0
    for line in text.splitlines():
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _heading_matches(line, heading):
            return True
    return False


def _is_h2_heading(line: str) -> bool:
    return _heading_match(line) is not None


def _heading_match(line: str) -> str | None:
    match = HEADING_RE.match(line)
    if match is None:
        return None
    return f"## {match.group('title').strip()}"


def _heading_matches(line: str, heading: str) -> bool:
    match = _heading_match(line)
    return match is not None and match == heading


def _update_fence_state(
    line: str, in_code_fence: bool, fence_char: str, fence_len: int
) -> tuple[bool, str, int]:
    match = FENCE_RE.match(line)
    if match is None:
        return in_code_fence, fence_char, fence_len
    marker = match.group("fence")
    rest = match.group("rest").strip()
    if not in_code_fence:
        return True, marker[0], len(marker)
    if marker[0] != fence_char or len(marker) < fence_len:
        return in_code_fence, fence_char, fence_len
    if rest == "":
        return False, "", 0
    return in_code_fence, fence_char, fence_len


def local_link_errors(markdown: Path, package: Path) -> list[str]:
    errors: list[str] = []
    text = markdown.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        target = target.strip().strip("<>").split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target):
            continue
        resolved = (markdown.parent / target).resolve()
        try:
            resolved.relative_to(package.resolve())
        except ValueError:
            errors.append(f"{markdown.relative_to(package)}: link escapes package: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{markdown.relative_to(package)}: broken link: {target}")
    return errors


def ask_ai_defaults_errors(package: Path) -> list[str]:
    """Keep provider-neutral browser and persistent-context defaults intact."""
    if package.name != "ask-ai":
        return []
    profile = package / "references" / "browser-profile.md"
    if not profile.is_file():
        return ["ask-ai: missing references/browser-profile.md"]
    text = profile.read_text(encoding="utf-8")
    return [
        f"ask-ai: browser-profile.md missing defaults token: {token}"
        for token in ASK_AI_DEFAULT_TOKENS
        if token not in text
    ]


def ask_ai_provider_variant_errors(package: Path) -> list[str]:
    """Validate Qoder variant aliases as recipient-only defaults."""
    if package.name != "ask-ai":
        return []
    routing = package / "references" / "provider-routing.md"
    if not routing.is_file():
        return ["ask-ai: missing references/provider-routing.md"]
    text = routing.read_text(encoding="utf-8")
    mappings = yaml_fence_mappings(text)
    defaults = next(
        (item for item in mappings if item.get("schema_version") == "ask-ai-defaults/v1"),
        None,
    )
    if not isinstance(defaults, dict):
        return ["ask-ai: provider-routing.md missing ask-ai-defaults/v1 example"]
    aliases = defaults.get("provider_aliases", {})
    if aliases is None:
        aliases = {}
    if not isinstance(aliases, dict):
        return ["ask-ai: ask-ai-defaults/v1 provider_aliases must be a mapping when present"]
    errors: list[str] = []
    canonical = {"qoder-cli-global", "qoder-cli-cn"}
    for alias, recipient in aliases.items():
        if not isinstance(alias, str) or not isinstance(recipient, str):
            errors.append("ask-ai: provider_aliases entries must be string recipient mappings")
        elif recipient not in canonical:
            errors.append("ask-ai: provider_aliases recipients must be canonical Qoder variants")
    if any(token not in text for token in ("capability", "identity", "authentication", "send-authorization")):
        errors.append("ask-ai: provider_aliases example must state recipient-only semantics")
    if "Never cross-fallback between the global" not in text:
        errors.append("ask-ai: Qoder variants must forbid cross-variant fallback")
    return errors


def ask_ai_authority_errors(package: Path) -> list[str]:
    """Keep Ask AI source-write authority aligned with its catalog contract."""
    if package.name != "ask-ai":
        return []
    skill = package / "SKILL.md"
    provider_cli = package / "references" / "provider-cli.md"
    evals = package / "references" / "eval-cases.md"
    missing = [path.relative_to(package).as_posix() for path in (skill, provider_cli, evals) if not path.is_file()]
    if missing:
        return ["ask-ai: missing authority contract files: " + ", ".join(missing)]

    errors: list[str] = []
    documents = {
        "SKILL.md": (
            skill.read_text(encoding="utf-8"),
            (
                "Review and research default to no-write.",
                "matching implementation owner",
                "source write authority belongs to the implementation",
                "repo-delivery",
            ),
        ),
        "references/provider-cli.md": (
            provider_cli.read_text(encoding="utf-8"),
            (
                "Review defaults to no-write.",
                "implementation-owner-authorized",
                "CLI provider presence",
                "not authorize source writes",
                "matching implementation owner",
                "repo-delivery",
            ),
        ),
        "references/eval-cases.md": (
            evals.read_text(encoding="utf-8"),
            (
                "Review CLI write-source attempt",
                "External implementation authorization composition",
                "Git delivery authorization separation",
            ),
        ),
    }
    for relative, (text, required) in documents.items():
        for token in required:
            if token not in text:
                errors.append(f"ask-ai: {relative} missing authority token: {token}")

    index_path = package.parents[1] / "skills-index.json"
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        entry = next(item for item in payload["skills"] if item.get("name") == "ask-ai")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, StopIteration, TypeError) as error:
        return errors + [f"ask-ai: cannot load skills-index authority entry: {error}"]
    allowed = entry.get("allowed_effects")
    forbidden = entry.get("forbidden_effects")
    if not isinstance(allowed, list) or not isinstance(forbidden, list):
        return errors + ["ask-ai: skills-index authority effect lists must be arrays"]
    if "write-source" in allowed:
        errors.append("ask-ai: skills-index allowed_effects must not include write-source")
    if "write-source" not in forbidden:
        errors.append("ask-ai: skills-index forbidden_effects must include write-source")
    return errors


def yaml_fence_mappings(text: str) -> list[dict[str, object]]:
    """Read only well-formed YAML examples from Markdown fences."""
    mappings: list[dict[str, object]] = []
    for match in re.finditer(r"```yaml\s*\n(.*?)\n```", text, re.DOTALL):
        try:
            value = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(value, dict):
            mappings.append(value)
    return mappings


def normalize_relay_instruction(instruction: object) -> tuple[dict[str, object] | None, list[str]]:
    """Validate and normalize one sequential-relay instruction."""
    if not isinstance(instruction, dict):
        return None, ["relay instruction must be a mapping"]
    normalized = dict(instruction)
    if instruction.get("workflow") != "sequential-relay":
        return None, ["relay instruction workflow must be sequential-relay"]
    providers = instruction.get("external_providers")
    if (
        not isinstance(providers, list)
        or len(providers) < 2
        or not all(isinstance(provider, str) and provider for provider in providers)
        or len(set(providers)) != len(providers)
    ):
        return None, ["sequential relay requires two or more distinct external_providers"]
    relay_order = instruction.get("relay_order")
    if (
        not isinstance(relay_order, list)
        or not relay_order
        or not all(isinstance(provider, str) and provider for provider in relay_order)
        or len(relay_order) != len(providers)
        or len(set(relay_order)) != len(relay_order)
        or set(relay_order) != set(providers)
    ):
        return None, ["sequential relay relay_order must contain every provider exactly once"]
    initial_provider = instruction.get("initial_provider")
    if initial_provider not in providers:
        return None, ["sequential relay initial_provider must be in external_providers"]
    max_turns = instruction.get("max_turns_per_provider")
    if isinstance(max_turns, bool) or not isinstance(max_turns, int) or max_turns <= 0:
        return None, ["sequential relay max_turns_per_provider must be a positive integer"]
    promotion = instruction.get("candidate_promotion", "user-only")
    if promotion not in ASK_AI_PROMOTION_VALUES:
        return None, ["sequential relay candidate_promotion must be user-only or provider-authored-textual-revision"]
    if instruction.get("stop_after") != ASK_AI_CANONICAL_STOP_AFTER:
        return None, ["sequential relay stop_after must be all-providers-approve-same-candidate"]
    return normalized, []


def relay_instruction_errors(instruction: object) -> list[str]:
    """Validate one v1 sequential-relay instruction."""
    _, errors = normalize_relay_instruction(instruction)
    return errors


def final_sync_instruction_errors(instruction: object) -> list[str]:
    """Validate one bounded post-terminal retention instruction."""
    if not isinstance(instruction, dict):
        return ["final-result-sync instruction must be a mapping"]
    errors: list[str] = []
    for field, expected in ASK_AI_FINAL_SYNC_FIXED_FIELDS.items():
        if instruction.get(field) != expected:
            errors.append(f"final-result-sync {field} must be {expected}")
    provider = instruction.get("external_provider")
    if not isinstance(provider, str) or not provider:
        errors.append("final-result-sync requires exactly one external_provider")
    surface = instruction.get("target_surface")
    if surface not in {"project", "notebook", "conversation"}:
        errors.append("final-result-sync target_surface must be project, notebook, or conversation")
    context = instruction.get("target_context")
    if not isinstance(context, str) or not context:
        errors.append("final-result-sync requires a non-empty target_context")
    forbidden = {
        "external_providers",
        "prompt_profiles",
        "rounds_per_provider",
        "initial_provider",
        "relay_order",
        "candidate_promotion",
        "max_turns_per_provider",
    }
    present = sorted(forbidden.intersection(instruction))
    if present:
        errors.append(
            "final-result-sync must not contain review or relay fields: " + ", ".join(present)
        )
    return errors


def ask_ai_final_result_sync_errors(package: Path) -> list[str]:
    """Validate the final-review-result retention contract and its routing example."""
    if package.name != "ask-ai":
        return []
    routing = package / "references" / "provider-routing.md"
    sync = package / "references" / "final-result-sync.md"
    gemini = package / "references" / "provider-gemini.md"
    profile = package / "references" / "browser-profile.md"
    evals = package / "references" / "eval-cases.md"
    missing = [path.name for path in (routing, sync, gemini, profile, evals) if not path.is_file()]
    if missing:
        return ["ask-ai: missing final-result-sync contract files: " + ", ".join(missing)]

    errors: list[str] = []
    mappings = yaml_fence_mappings(routing.read_text(encoding="utf-8"))
    instruction = next(
        (
            item["instructions"]["final-review-sync"]
            for item in mappings
            if item.get("schema_version") == "ask-ai-instructions/v1"
            and isinstance(item.get("instructions"), dict)
            and "final-review-sync" in item["instructions"]
        ),
        None,
    )
    errors.extend(f"ask-ai: {error}" for error in final_sync_instruction_errors(instruction))
    sync_text = sync.read_text(encoding="utf-8")
    for token in (
        "This is not a review request.",
        "SYNC RECEIVED: <same Final-result SHA-256>",
        "unsafe-to-sanitize",
        "receipt-only-non-authoritative",
    ):
        if token not in sync_text:
            errors.append(f"ask-ai: final-result-sync.md missing contract token: {token}")
    if "Do not fall back to Standard Chat" not in gemini.read_text(encoding="utf-8"):
        errors.append("ask-ai: Gemini final-result retention must forbid Standard Chat fallback")
    if "context is retention-only and is excluded" not in profile.read_text(encoding="utf-8"):
        errors.append("ask-ai: review-context routing must exclude reserved retention targets")
    eval_text = evals.read_text(encoding="utf-8")
    for token in (
        "configured final-result sync follows a completed local review",
        "Gemini replies to a retention sync with new findings",
        "Final review result retention",
    ):
        if token.lower() not in eval_text.lower():
            errors.append(f"ask-ai: eval-cases.md missing final-result-sync case: {token}")
    return errors


def ask_ai_untrusted_content_errors(package: Path) -> list[str]:
    """Pin the data-only quarantine and browser-boundary contract."""
    if package.name != "ask-ai":
        return []
    contract_file = package / "references" / "untrusted-content.md"
    skill_file = package / "SKILL.md"
    browser_file = package / "references" / "live-browser-review.md"
    routing_file = package / "references" / "provider-routing.md"
    eval_file = package / "references" / "eval-cases.md"
    required = (contract_file, skill_file, browser_file, routing_file, eval_file)
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        return ["ask-ai: missing untrusted-content contract files: " + ", ".join(missing)]

    mappings = yaml_fence_mappings(contract_file.read_text(encoding="utf-8"))
    contract = next(
        (item.get("untrusted_content_contract") for item in mappings if "untrusted_content_contract" in item),
        None,
    )
    expected = {
        "schema_version": "untrusted-review-data/v1",
        "sources": [
            "external-provider-response",
            "inspected-webpage",
            "downloaded-text",
            "citation-target",
        ],
        "quarantine": {
            "enter": "before-first-third-party-byte",
            "mode": "read-only-data",
            "allowed_effects": [
                "capture-visible-content",
                "hash-content",
                "write-ignored-local-ledger",
                "redact",
                "analyze-read-only",
            ],
            "forbidden_effects": [
                "follow-content-instructions",
                "navigate-unapproved-url",
                "invoke-content-requested-tool",
                "read-extra-local-data",
                "expose-secret",
                "change-scope-recipient-route",
                "write-source",
                "write-git-state",
                "mutate-external-system",
                "relay-before-release",
            ],
        },
        "extraction": {
            "visibility": "visible-attributed-content-only",
            "hidden_content": "reject",
            "suspicious_controls": "stop-incomplete",
        },
        "browser": {
            "scope": "exact-origin-url-and-actions",
            "default_denials": [
                "cross-origin-navigation",
                "download",
                "form-submit",
                "permission-change",
                "authentication-action",
                "private-surface",
                "unrelated-tab",
            ],
        },
        "release": {
            "local_verification": "independent-evidence-required",
            "peer_relay": "explicit-source-to-recipient-authorization-and-sanitized-envelope",
        },
        "envelope": {
            "authority": "data-only",
            "capture_hash": "sha256-before-redaction",
            "forwarded_hash": "sha256-after-redaction",
            "attribution": "required",
        },
        "stop_states": [
            "identity-unverified",
            "visible-extraction-unverified",
            "suspicious-hidden-content",
            "semantic-redaction-loss",
            "boundary-expansion-required",
        ],
    }
    errors: list[str] = []
    if contract != expected:
        errors.append("ask-ai: untrusted_content_contract must preserve the complete data-only quarantine boundary")

    required_tokens = {
        skill_file: ("untrusted-content.md", "read-only", "quarantine"),
        browser_file: ("exact origin, URL, and action allowlist", "suspicious-hidden-content"),
        routing_file: ("untrusted-review-data/v1", "SHA-256 of the exact forwarded text"),
        eval_file: ("Untrusted content quarantine", "open `.env`", "cross-origin"),
    }
    for path, tokens in required_tokens.items():
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"ask-ai: {path.name} missing untrusted-content token: {token}")
    return errors


def ask_ai_mutual_review_errors(package: Path) -> list[str]:
    """Validate structured mutual-review examples rather than safety words alone."""
    if package.name != "ask-ai":
        return []
    routing = package / "references" / "provider-routing.md"
    if not routing.is_file():
        return ["ask-ai: missing references/provider-routing.md"]
    mappings = yaml_fence_mappings(routing.read_text(encoding="utf-8"))
    contract = next((item.get("relay_contract") for item in mappings if "relay_contract" in item), None)
    if not isinstance(contract, dict):
        return ["ask-ai: provider-routing.md missing structured relay_contract fixture"]

    errors: list[str] = []
    hierarchy = contract.get("hierarchy")
    expected_hierarchy = {
        "review_round": "round_id",
        "relay_turn": "relay_turn_id",
        "operation": "operation_id-per-side-effect",
    }
    if hierarchy != expected_hierarchy:
        errors.append("ask-ai: relay_contract hierarchy must be review round -> relay turn -> operation")
    precedence = contract.get("resolution_precedence")
    if precedence != {
        "package_only": "overrides-send",
        "explicit_current_request": "invocation-only-customization",
        "exact_executable_alias": "custom-instruction",
        "persisted_default": "bare-and-explicit-mutual-review",
        "built_in_fallback": "chatgpt-gemini-three-turns",
    }:
        errors.append("ask-ai: relay_contract must prefer the user-editable mutual-review default before the built-in fallback")
    if contract.get("resolution_order") != [
        "package_only",
        "explicit_current_request",
        "exact_executable_alias",
        "persisted_default",
        "built_in_fallback",
    ]:
        errors.append("ask-ai: relay_contract mutual-review resolution order is invalid")
    if contract.get("default_trigger") != "互审":
        errors.append("ask-ai: relay_contract default_trigger must be 互审")
    if contract.get("invalid_persisted_default") != "fail-closed":
        errors.append("ask-ai: relay_contract must fail closed on an invalid persisted default")
    if set(contract.get("candidate_promotion_values", [])) != ASK_AI_PROMOTION_VALUES:
        errors.append("ask-ai: relay_contract must enumerate the candidate_promotion values")
    exhaustion = contract.get("exhaustion")
    if not isinstance(exhaustion, dict) or exhaustion != {
        "only_when": "next-required-provider-has-no-legal-turn",
        "lower_priority_than": "changes-required",
    }:
        errors.append("ask-ai: relay_contract must define exhaustion precedence after changes-required")
    conversation_reuse = contract.get("conversation_reuse")
    if not isinstance(conversation_reuse, dict) or conversation_reuse != {
        "first_provider_turn": {
            "reuse_verified_conversation": "preferred",
            "create_when": "no-verified-conversation-and-new-session-is-required",
            "create_operation": "create-conversation",
        },
        "later_provider_turn": {
            "require_same_verified_conversation": True,
            "create_operation": "forbidden",
            "side_effect_operations": ["attach-if-needed", "submit", "capture-response"],
        },
        "interruption": {
            "reconcile_original_create_operation_id": True,
            "replacement_conversation": "forbidden",
        },
    }:
        errors.append("ask-ai: relay_contract must define per-provider conversation reuse and create reconciliation")

    instructions: list[object] = []
    for mapping in mappings:
        if mapping.get("schema_version") != "ask-ai-instructions/v1":
            continue
        records = mapping.get("instructions")
        if isinstance(records, dict):
            instructions.extend(
                record for record in records.values()
                if isinstance(record, dict) and record.get("workflow") == "sequential-relay"
            )
    provider_counts: set[int] = set()
    for instruction in instructions:
        errors.extend(f"ask-ai: {error}" for error in relay_instruction_errors(instruction))
        providers = instruction.get("external_providers") if isinstance(instruction, dict) else None
        if isinstance(providers, list):
            provider_counts.add(len(providers))
    if not {2, 3}.issubset(provider_counts):
        errors.append("ask-ai: provider-routing.md needs valid two- and three-provider relay examples")
    return errors


def ask_ai_app_native_relay_errors(package: Path) -> list[str]:
    """Validate that atomic host calls preserve logical relay operations."""
    if package.name != "ask-ai":
        return []
    protocol = package / "references" / "app-native-thread-protocol.md"
    if not protocol.is_file():
        return ["ask-ai: missing references/app-native-thread-protocol.md"]
    mappings = yaml_fence_mappings(protocol.read_text(encoding="utf-8"))
    contract = next(
        (item.get("app_native_relay_contract") for item in mappings if "app_native_relay_contract" in item),
        None,
    )
    expected = {
        "schema_version": "app-native-thread-operation/v3",
        "hierarchy": {
            "review_round": "round_id",
            "relay_turn": "relay_turn_id",
            "operation": "logical-operation-id",
        },
        "initial_turn": {
            "host_call": "create_thread",
            "create_submit_atomic": True,
            "host_call_correlation": "required",
            "logical_operations": ["create-conversation", "submit-initial", "capture-response"],
            "logical_write_projection": {
                "before_host_call": "invoking",
                "normal_host_return": "submitted",
                "uncertain_host_return": "submission-uncertain",
            },
        },
        "later_turn": {
            "require_same_verified_conversation": True,
            "create_operation": "forbidden",
            "logical_operations": ["submit-follow-up", "capture-response"],
        },
        "capture_response": {
            "state_change": False,
            "idempotent": True,
            "operation_id": "required",
        },
    }
    if contract != expected:
        return ["ask-ai: App-native relay contract must separate correlated create, submit, and idempotent capture operations"]
    return []


def package_errors(package: Path, all_names: set[str]) -> list[str]:
    errors: list[str] = []
    skill_file = package / "SKILL.md"
    if not skill_file.is_file():
        return [f"{package.name}: missing SKILL.md"]

    try:
        metadata, body = frontmatter(skill_file)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        return [f"{package.name}: {error}"]

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    unknown_fields = set(metadata) - PORTABLE_FIELDS
    if unknown_fields:
        errors.append(f"{package.name}: unsupported frontmatter fields: {sorted(unknown_fields)}")
    if name != package.name:
        errors.append(f"{package.name}: frontmatter name must match directory")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"{package.name}: name must be 1-64 lowercase letters, digits, or hyphens")
    if (
        not isinstance(description, str)
        or not description
        or len(description) > 1024
        or re.search(r"<[^>]+>", description)
    ):
        errors.append(f"{package.name}: description must be plain text with 1-1024 characters")
    elif "Use when" not in description:
        errors.append(f"{package.name}: description must state when to use the Skill")
    license_value = metadata.get("license")
    if license_value is not None and (not isinstance(license_value, str) or not license_value.strip()):
        errors.append(f"{package.name}: license must be a non-empty string when provided")
    compatibility = metadata.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not compatibility.strip() or len(compatibility) > 500
    ):
        errors.append(f"{package.name}: compatibility must be a string with 1-500 characters")
    portable_metadata = metadata.get("metadata")
    if portable_metadata is not None and (
        not isinstance(portable_metadata, dict)
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in portable_metadata.items())
    ):
        errors.append(f"{package.name}: metadata must map strings to strings")
    allowed_tools = metadata.get("allowed-tools")
    if allowed_tools is not None and (
        not isinstance(allowed_tools, str) or not allowed_tools.strip()
    ):
        errors.append(f"{package.name}: allowed-tools must be a non-empty string when provided")
    if len(body.splitlines()) > 500:
        errors.append(f"{package.name}: SKILL.md body exceeds the recommended 500 lines")

    for forbidden in FORBIDDEN_PACKAGE_FILES:
        if (package / forbidden).exists():
            errors.append(f"{package.name}: remove package-local {forbidden}")

    references = package / "references"
    if references.is_dir():
        nested = [path for path in references.rglob("*") if path.is_file() and path.parent != references]
        for path in nested:
            errors.append(f"{package.name}: references must stay one level deep: {path.relative_to(package)}")
        linked = {
            target.strip().strip("<>").split("#", 1)[0]
            for target in LINK_RE.findall(skill_file.read_text(encoding="utf-8"))
            if target.startswith("references/")
        }
        for reference in sorted(references.glob("*.md")):
            relative = reference.relative_to(package).as_posix()
            if relative not in linked:
                errors.append(f"{package.name}: reference is not linked from SKILL.md: {relative}")
            reference_text = reference.read_text(encoding="utf-8")
            if len(reference_text.splitlines()) > LONG_REFERENCE_LINES and not has_exact_h2_heading(
                reference_text, "## Contents"
            ):
                errors.append(
                    f"{package.name}: long reference needs a ## Contents section: {relative}"
                )
    else:
        errors.append(f"{package.name}: missing references directory")

    errors.extend(ask_ai_defaults_errors(package))
    errors.extend(ask_ai_provider_variant_errors(package))
    errors.extend(ask_ai_authority_errors(package))
    errors.extend(ask_ai_mutual_review_errors(package))
    errors.extend(ask_ai_final_result_sync_errors(package))
    errors.extend(ask_ai_untrusted_content_errors(package))
    errors.extend(ask_ai_app_native_relay_errors(package))

    eval_file = references / "eval-cases.md"
    if not eval_file.is_file():
        errors.append(f"{package.name}: missing references/eval-cases.md")
    else:
        eval_text = eval_file.read_text(encoding="utf-8")
        for heading in EVAL_HEADINGS:
            if not has_exact_h2_heading(eval_text, heading):
                errors.append(f"{package.name}: eval-cases.md missing {heading}")
            elif not section_has_content(eval_text, heading):
                errors.append(f"{package.name}: eval-cases.md has empty {heading}")

    openai_file = package / "agents" / "openai.yaml"
    if not openai_file.is_file():
        errors.append(f"{package.name}: missing agents/openai.yaml for OpenAI discovery")
    else:
        try:
            interface = openai_interface(openai_file)
            openai_invocation_policy(openai_file)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            errors.append(f"{package.name}: openai.yaml {error}")
            interface = {}
        for field in ("display_name", "short_description", "default_prompt"):
            if not interface.get(field):
                errors.append(f"{package.name}: openai.yaml missing interface.{field}")
        short_description = interface.get("short_description", "")
        if short_description and not 25 <= len(short_description) <= 64:
            errors.append(
                f"{package.name}: openai.yaml interface.short_description must be 25-64 characters"
            )
        prompt = interface.get("default_prompt", "")
        if f"${package.name}" not in prompt:
            errors.append(f"{package.name}: default_prompt must route through ${package.name}")
        for route in ROUTE_RE.findall(prompt):
            if route not in all_names:
                errors.append(f"{package.name}: default_prompt references unknown Skill ${route}")

    for markdown in package.rglob("*.md"):
        errors.extend(f"{package.name}: {error}" for error in local_link_errors(markdown, package))
        if "npx skills" in markdown.read_text(encoding="utf-8"):
            errors.append(f"{package.name}: installation commands belong in root documentation")
    return errors


def catalog_errors(root: Path, names: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads((root / "skills.sh.json").read_text(encoding="utf-8"))
        listed = {
            skill
            for grouping in payload.get("groupings", [])
            for skill in grouping.get("skills", [])
        }
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError) as error:
        errors.append(f"skills.sh.json: invalid catalog: {error}")
        listed = set()
    if listed != names:
        errors.append(f"skills.sh.json package set differs: expected {sorted(names)}, found {sorted(listed)}")

    for filename, pattern in (("README.md", CATALOG_ROW_RE), ("INSTALL.md", INSTALL_PATH_RE)):
        try:
            found = set(pattern.findall((root / filename).read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"{filename}: cannot read catalog: {error}")
            continue
        if found != names:
            errors.append(f"{filename} package set differs: expected {sorted(names)}, found {sorted(found)}")
    return errors


def skill_contract_errors(entries: list[dict[str, object]]) -> list[str]:
    """Validate provider-neutral execution boundaries declared by the index.

    These fields deliberately live outside portable ``SKILL.md`` frontmatter. The
    validator checks the small closed vocabulary and the minimum relation between a
    mutation class, its required capability, and its permitted effect.
    """
    errors: list[str] = []
    for entry in entries:
        name = entry.get("name", "<unknown>")
        owner = entry.get("owner")
        if owner != name:
            errors.append(f"skills-index.json: {name} owner must match name")

        mutation = entry.get("mutation_class")
        if mutation not in MUTATION_CLASSES:
            errors.append(f"skills-index.json: {name} has unknown mutation_class {mutation!r}")
            continue

        capabilities = entry.get("required_capabilities")
        allowed = entry.get("allowed_effects")
        forbidden = entry.get("forbidden_effects")
        stops = entry.get("stop_states")
        if not isinstance(capabilities, list) or not capabilities:
            errors.append(f"skills-index.json: {name} required_capabilities must be non-empty")
            capabilities = []
        if not isinstance(allowed, list) or not allowed:
            errors.append(f"skills-index.json: {name} allowed_effects must be non-empty")
            allowed = []
        if not isinstance(forbidden, list) or not forbidden:
            errors.append(f"skills-index.json: {name} forbidden_effects must be non-empty")
            forbidden = []
        if not isinstance(stops, list) or not stops:
            errors.append(f"skills-index.json: {name} stop_states must be non-empty")
            stops = []

        overlap = set(allowed) & set(forbidden)
        if overlap:
            errors.append(
                f"skills-index.json: {name} allowed_effects and forbidden_effects overlap: {sorted(overlap)}"
            )
        missing_capabilities = MUTATION_CAPABILITIES[mutation] - set(capabilities)
        if missing_capabilities:
            errors.append(
                f"skills-index.json: {name} mutation_class {mutation} requires capabilities "
                f"{sorted(missing_capabilities)}"
            )
        missing_effects = CONTRACT_EFFECT_BY_MUTATION[mutation] - set(allowed)
        if missing_effects:
            errors.append(
                f"skills-index.json: {name} mutation_class {mutation} must allow effects "
                f"{sorted(missing_effects)}"
            )
        for capability, effect in CAPABILITY_EFFECTS.items():
            if capability in capabilities and effect not in allowed:
                errors.append(
                    f"skills-index.json: {name} capability {capability} must allow effect {effect}"
                )
        if mutation == "read-only" and any(
            effect in set(allowed)
            for effect in ("write-source", "write-artifact", "write-git-state", "control-browser-state", "control-client-state", "invoke-external-provider")
        ):
            errors.append(f"skills-index.json: {name} read-only contract allows a mutating effect")
    return errors


def skill_index_errors(root: Path, names: set[str]) -> list[str]:
    errors: list[str] = []
    index_path = root / "skills-index.json"
    schema_path = root / "docs" / "skills" / "skills-index.schema.json"
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"skills-index.json: cannot load index and schema: {error}"]

    schema_errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    for error in schema_errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"skills-index.json: {location}: {error.message}")
    if schema_errors:
        return errors

    entries = payload["skills"]
    errors.extend(skill_contract_errors(entries))
    indexed_names = [entry["name"] for entry in entries]
    if len(indexed_names) != len(set(indexed_names)):
        errors.append("skills-index.json: duplicate Skill names")
    if set(indexed_names) != names:
        errors.append(
            "skills-index.json package set differs: "
            f"expected {sorted(names)}, found {sorted(set(indexed_names))}"
        )

    categories = set(payload["categories"])
    used_categories: set[str] = set()
    for entry in entries:
        name = entry["name"]
        category = entry["category"]
        used_categories.add(category)
        if category not in categories:
            errors.append(f"skills-index.json: {name} references unknown category {category}")
        related = set(entry["related"])
        if name in related:
            errors.append(f"skills-index.json: {name} cannot relate to itself")
        unknown_related = related - names
        if unknown_related:
            errors.append(
                f"skills-index.json: {name} references unknown related Skills "
                f"{sorted(unknown_related)}"
            )
    unused_categories = categories - used_categories
    if unused_categories:
        errors.append(f"skills-index.json: unused categories {sorted(unused_categories)}")

    try:
        distribution = json.loads((root / "skills.sh.json").read_text(encoding="utf-8"))
        groupings = distribution["groupings"]
        grouped_by_title = {grouping["title"]: set(grouping["skills"]) for grouping in groupings}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        errors.append(f"skills-index.json: cannot compare distribution groups: {error}")
        return errors

    category_titles = {
        category: details["title"] for category, details in payload["categories"].items()
    }
    if len(grouped_by_title) != len(groupings):
        errors.append("skills.sh.json: duplicate grouping titles")
    if len(set(category_titles.values())) != len(category_titles):
        errors.append("skills-index.json: duplicate category titles")
    if set(category_titles.values()) != set(grouped_by_title):
        errors.append(
            "skills-index.json category titles differ from skills.sh.json groups: "
            f"expected {sorted(grouped_by_title)}, found {sorted(category_titles.values())}"
        )
    for category, title in category_titles.items():
        expected = {entry["name"] for entry in entries if entry["category"] == category}
        found = grouped_by_title.get(title)
        if found is not None and found != expected:
            errors.append(
                f"skills-index.json category {category} differs from distribution group "
                f"{title}: expected {sorted(expected)}, found {sorted(found)}"
            )
    return errors


def validate(root: Path) -> list[str]:
    skills = root / "skills"
    packages = sorted(path for path in skills.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    names = {path.name for path in packages}
    errors = catalog_errors(root, names)
    errors.extend(skill_index_errors(root, names))
    for package in packages:
        errors.extend(package_errors(package, names))
    if not packages:
        errors.append("no Skill packages found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    count = len(list((args.root / "skills").glob("*/SKILL.md")))
    print(f"validated {count} Skill packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
