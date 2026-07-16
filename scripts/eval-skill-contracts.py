#!/usr/bin/env python3
"""Validate and score AICraft routing, authority, and workflow evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath


def reject_duplicate_json_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "scripts" / "evaluation_protocol.py"
_PROTOCOL_SPEC = importlib.util.spec_from_file_location(
    "aicraft_evaluation_protocol_for_evaluator", PROTOCOL_PATH
)
if _PROTOCOL_SPEC is None or _PROTOCOL_SPEC.loader is None:
    raise RuntimeError(f"cannot load evaluation protocol from {PROTOCOL_PATH}")
PROTOCOL = importlib.util.module_from_spec(_PROTOCOL_SPEC)
sys.modules[_PROTOCOL_SPEC.name] = PROTOCOL
_PROTOCOL_SPEC.loader.exec_module(PROTOCOL)
ROUTING_DATA = ROOT / "evals" / "routing.jsonl"
AUTHORITY_DATA = ROOT / "evals" / "authority.jsonl"
WORKFLOW_DATA = ROOT / "evals" / "workflow-smoke.jsonl"
CONTRACTS = json.loads(
    (ROOT / "contracts" / "skill-validation.json").read_text(encoding="utf-8"),
    object_pairs_hook=reject_duplicate_json_keys,
)
BEHAVIOR_CONTRACT = CONTRACTS["behavior_eval"]
ROUTING_CONTRACT = BEHAVIOR_CONTRACT["routing"]
AUTHORITY_CONTRACT = BEHAVIOR_CONTRACT["authority"]
WORKFLOW_CONTRACT = BEHAVIOR_CONTRACT["workflow"]
ROUTING_KINDS = set(ROUTING_CONTRACT["kinds"])
CORE_SKILLS = set(ROUTING_CONTRACT["core_skills"])
RESULT_SCHEMA_VERSION = int(BEHAVIOR_CONTRACT["result_schema_version"])
RAW_EVIDENCE_SCHEMA_VERSION = int(
    BEHAVIOR_CONTRACT["raw_evidence_schema_version"]
)
PROMPT_TEMPLATE_VERSION = int(BEHAVIOR_CONTRACT["prompt_template_version"])
PROMPT_VALUE_PLACEHOLDER = "<NATURAL_REQUEST_JSON>"
MAXIMUM_CLOCK_SKEW_SECONDS = int(
    BEHAVIOR_CONTRACT["maximum_clock_skew_seconds"]
)
REQUIRED_METADATA = set(BEHAVIOR_CONTRACT["result_required_fields"])
RUN_CONFIG_REQUIRED = set(BEHAVIOR_CONTRACT["run_config_required_fields"])
HELD_OUT_PROVENANCE_REQUIRED = set(
    BEHAVIOR_CONTRACT["held_out_provenance_required_fields"]
)
ADJUDICATION_REQUIRED = set(
    BEHAVIOR_CONTRACT["adjudication_required_fields"]
)
RAW_EVIDENCE_REQUIRED = set(
    BEHAVIOR_CONTRACT["raw_evidence_required_fields"]
)
HOST_ATTEMPT_REQUIRED = set(
    BEHAVIOR_CONTRACT["host_attempt_required_fields"]
)
RESULT_VARIANTS = set(BEHAVIOR_CONTRACT["result_variants"])
ADJUDICATION_METHODS = set(BEHAVIOR_CONTRACT["adjudication_methods"])


@dataclass(frozen=True)
class Score:
    passed: bool
    lines: tuple[str, ...]


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw, object_pairs_hook=reject_duplicate_json_keys)
        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{line_number}: each row must be an object")
        rows.append(item)
    return rows


def dataset_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_usage_from_stdout(
    stdout: str, *, host_name: str
) -> tuple[int | None, int | None]:
    """Recompute the runner's cache-aware token metrics from verbatim output."""

    values: list[object] = []
    try:
        values.append(json.loads(stdout, object_pairs_hook=reject_duplicate_json_keys))
    except (json.JSONDecodeError, ValueError):
        for line in stdout.splitlines():
            try:
                values.append(
                    json.loads(line, object_pairs_hook=reject_duplicate_json_keys)
                )
            except (json.JSONDecodeError, ValueError):
                continue
    usages: list[tuple[int | None, int | None]] = []

    def visit(value: object) -> None:
        if isinstance(value, dict):
            input_tokens = value.get("input_tokens")
            output_tokens = value.get("output_tokens")
            if (
                isinstance(input_tokens, int)
                and not isinstance(input_tokens, bool)
                and input_tokens > 0
                and isinstance(output_tokens, int)
                and not isinstance(output_tokens, bool)
                and output_tokens > 0
            ):
                if host_name == "claude":
                    cache_tokens = 0
                    for field in (
                        "cache_creation_input_tokens",
                        "cache_read_input_tokens",
                    ):
                        cache_value = value.get(field)
                        if cache_value is None:
                            continue
                        if (
                            isinstance(cache_value, bool)
                            or not isinstance(cache_value, int)
                            or cache_value < 0
                        ):
                            usages.append((None, None))
                            break
                        cache_tokens += cache_value
                    else:
                        usages.append((input_tokens + cache_tokens, output_tokens))
                else:
                    usages.append((input_tokens, output_tokens))
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for value in values:
        visit(value)
    return usages[-1] if usages else (None, None)


def canonical_json_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def case_set_hash(cases: list[dict[str, object]]) -> str:
    return canonical_json_hash(
        [
            {
                "id": str(case["id"]),
                "prompt_sha256": text_hash(str(case["prompt"])),
            }
            for case in cases
        ]
    )


def committed_skill_fixture_hash(revision: str) -> str:
    """Hash the exact committed blobs exported by the routing runner."""

    tree = subprocess.run(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "-z", revision, "--", "skills"],
        check=False,
        capture_output=True,
    )
    if tree.returncode != 0:
        raise ValueError(f"cannot read committed skills fixture for {revision}")
    digest = hashlib.sha256()
    package_names = discover_skill_names()
    for record in tree.stdout.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode, object_type, object_sha = metadata.decode("ascii").split(" ")
            path_text = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise ValueError(
                f"cannot parse committed skills fixture for {revision}"
            ) from error
        path = PurePosixPath(path_text)
        if path.parts in {("skills", "AGENTS.md"), ("skills", "CLAUDE.md")}:
            # Repository authoring policies are not installable Skill package data.
            continue
        if (
            object_type != "blob"
            or mode not in {"100644", "100755"}
            or path.is_absolute()
            or len(path.parts) < 3
            or path.parts[0] != "skills"
            or path.parts[1] not in package_names
            or ".." in path.parts
            or path.as_posix() != path_text
        ):
            raise ValueError(
                f"unsupported committed Skill entry {path_text!r} in {revision}"
            )
        content = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "blob", object_sha],
            check=False,
            capture_output=True,
        )
        if content.returncode != 0:
            raise ValueError(
                f"cannot read committed Skill blob {object_sha} in {revision}"
            )
        digest.update(path_text.encode("utf-8") + b"\0")
        digest.update(mode.encode("ascii") + b"\0")
        digest.update(content.stdout)
        digest.update(b"\0")
    return digest.hexdigest()


def discover_skill_names(root: Path = ROOT) -> set[str]:
    return {
        path.parent.name
        for path in (root / "skills").glob("*/SKILL.md")
        if path.is_file()
    }


def revision_is_ancestor(
    ancestor: str, descendant: str, *, strict: bool = False
) -> bool:
    """Return whether two repository commits have the required ancestry."""

    if strict and ancestor == descendant:
        return False
    check = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "merge-base",
            "--is-ancestor",
            ancestor,
            descendant,
        ],
        check=False,
        capture_output=True,
    )
    return check.returncode == 0


def string_list(item: dict[str, object], key: str, *, case_id: str) -> list[str]:
    value = item.get(key)
    if not isinstance(value, list) or any(not isinstance(entry, str) for entry in value):
        raise ValueError(f"{case_id}: {key} must be a string list")
    return value


def unique_string_list(
    item: dict[str, object],
    key: str,
    *,
    case_id: str,
    default: object | None = None,
) -> list[str]:
    value = item.get(key, default)
    if not isinstance(value, list) or any(
        not isinstance(entry, str) or not entry.strip() for entry in value
    ):
        raise ValueError(f"{case_id}: {key} must be a non-empty-string list")
    if len(value) != len(set(value)):
        raise ValueError(f"{case_id}: {key} must not contain duplicates")
    return value


def validate_unique_cases(cases: list[dict[str, object]], *, label: str) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    prompts: set[str] = set()
    for item in cases:
        case_id = item.get("id")
        prompt = item.get("prompt")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{label}: case missing non-empty id")
            continue
        if case_id in ids:
            errors.append(f"{label}: duplicate id {case_id}")
        ids.add(case_id)
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{case_id}: prompt must be non-empty")
            continue
        normalized = re.sub(r"\s+", " ", prompt.strip()).casefold()
        if normalized in prompts:
            errors.append(f"{label}: duplicate prompt in {case_id}")
        prompts.add(normalized)
    return errors


def validate_routing_cases(
    cases: list[dict[str, object]],
    known_skills: set[str],
    *,
    routing_graph_path: Path | None = None,
    minimum_cases: int | None = None,
    minimum_cases_per_skill: int | None = None,
    required_kinds: set[str] | None = None,
    minimum_required_handoff_cases: int | None = None,
    minimum_no_required_handoff_cases: int | None = None,
    minimum_required_handoff_owners: int | None = None,
    required_handoff_primary_owners: set[str] | None = None,
    require_neighbor_graph: bool = True,
) -> list[str]:
    errors = validate_unique_cases(cases, label="routing")
    case_minimum = (
        int(ROUTING_CONTRACT["minimum_cases"])
        if minimum_cases is None
        else minimum_cases
    )
    if len(cases) < case_minimum:
        errors.append(
            f"routing: expected at least {case_minimum} cases, found {len(cases)}"
        )
    observed_kinds: set[str] = set()
    owner_counts: Counter[str] = Counter()
    covered_neighbors: dict[str, set[str]] = {
        skill_name: set() for skill_name in known_skills
    }
    required_handoff_cases = 0
    no_required_handoff_cases = 0
    required_handoff_owners: set[str] = set()
    for item in cases:
        case_id = str(item.get("id", "routing case"))
        kind = item.get("kind")
        owner = item.get("expected_owner")
        if kind not in ROUTING_KINDS:
            errors.append(f"{case_id}: unknown routing kind {kind!r}")
        else:
            observed_kinds.add(str(kind))
        if owner not in known_skills:
            errors.append(f"{case_id}: unknown expected owner {owner!r}")
        else:
            owner_counts[str(owner)] += 1
        try:
            forbidden = string_list(item, "forbidden_owners", case_id=case_id)
        except ValueError as error:
            errors.append(str(error))
            forbidden = []
        for name in forbidden:
            if name not in known_skills:
                errors.append(f"{case_id}: unknown forbidden owner {name!r}")
        if owner in forbidden:
            errors.append(f"{case_id}: expected owner cannot also be forbidden")
        if owner in known_skills:
            covered_neighbors[str(owner)].update(forbidden)
        allowed = item.get("allowed_owners", [owner])
        if not isinstance(allowed, list) or any(
            not isinstance(name, str) for name in allowed
        ):
            errors.append(f"{case_id}: allowed_owners must be a string list")
            allowed = []
        if owner not in allowed:
            errors.append(f"{case_id}: allowed_owners must include expected_owner")
        for name in allowed:
            if name not in known_skills:
                errors.append(f"{case_id}: unknown allowed owner {name!r}")
            if name in forbidden:
                errors.append(f"{case_id}: allowed owner {name!r} cannot be forbidden")
        handoff_values: dict[str, list[str]] = {}
        for key in (
            "required_handoffs",
            "allowed_handoffs",
            "forbidden_handoffs",
        ):
            try:
                values = unique_string_list(
                    item, key, case_id=case_id, default=[]
                )
            except ValueError as error:
                errors.append(str(error))
                handoff_values[key] = []
                continue
            handoff_values[key] = values
            for name in values:
                if name not in known_skills:
                    errors.append(f"{case_id}: unknown {key[:-1]} {name!r}")
        required_handoffs = set(handoff_values["required_handoffs"])
        allowed_handoffs = set(handoff_values["allowed_handoffs"])
        forbidden_handoffs = set(handoff_values["forbidden_handoffs"])
        if not required_handoffs <= allowed_handoffs:
            errors.append(
                f"{case_id}: required_handoffs must be included in allowed_handoffs"
            )
        overlap = allowed_handoffs & forbidden_handoffs
        if overlap:
            errors.append(
                f"{case_id}: handoffs cannot be both allowed and forbidden: "
                f"{sorted(overlap)}"
            )

        required_groups = item.get("required_handoff_groups", [])
        if not isinstance(required_groups, list):
            errors.append(
                f"{case_id}: required_handoff_groups must be a list of non-empty string lists"
            )
            required_groups = []
        normalized_groups: set[frozenset[str]] = set()
        for index, group in enumerate(required_groups):
            group_label = f"required_handoff_groups[{index}]"
            if (
                not isinstance(group, list)
                or not group
                or any(
                    not isinstance(name, str) or not name.strip()
                    for name in group
                )
            ):
                errors.append(
                    f"{case_id}: {group_label} must be a non-empty string list"
                )
                continue
            if len(group) != len(set(group)):
                errors.append(f"{case_id}: {group_label} must not contain duplicates")
                continue
            group_set = frozenset(group)
            if group_set in normalized_groups:
                errors.append(
                    f"{case_id}: required_handoff_groups must not contain duplicate groups"
                )
            direct_overlap = group_set & required_handoffs
            if direct_overlap:
                errors.append(
                    f"{case_id}: {group_label} must not overlap required_handoffs: "
                    f"{sorted(direct_overlap)}"
                )
            prior_group_overlap = (
                group_set & set().union(*normalized_groups)
                if normalized_groups
                else set()
            )
            if prior_group_overlap:
                errors.append(
                    f"{case_id}: required one-of handoff groups must be pairwise "
                    f"disjoint: {sorted(prior_group_overlap)}"
                )
            normalized_groups.add(group_set)
            for name in group:
                if name not in known_skills:
                    errors.append(
                        f"{case_id}: unknown required handoff group member {name!r}"
                    )
            if not group_set <= allowed_handoffs:
                errors.append(
                    f"{case_id}: {group_label} must be included in allowed_handoffs"
                )
            group_overlap = group_set & forbidden_handoffs
            if group_overlap:
                errors.append(
                    f"{case_id}: {group_label} contains forbidden handoffs "
                    f"{sorted(group_overlap)}"
                )
        required_or_group_handoffs = (
            required_handoffs | set().union(*normalized_groups)
            if normalized_groups
            else required_handoffs
        )
        optional_allowed_handoffs = allowed_handoffs - required_or_group_handoffs
        if optional_allowed_handoffs:
            errors.append(
                f"{case_id}: allowed_handoffs may contain only required direct "
                "or one-of group members; optional entries are not necessary "
                f"handoffs: {sorted(optional_allowed_handoffs)}"
            )
        declared_handoffs = (
            required_handoffs
            | allowed_handoffs
            | forbidden_handoffs
            | set().union(*normalized_groups)
            if normalized_groups
            else required_handoffs | allowed_handoffs | forbidden_handoffs
        )
        owner_handoff_overlap = set(allowed) & declared_handoffs
        if owner_handoff_overlap:
            errors.append(
                f"{case_id}: allowed owners cannot also be handoffs: "
                f"{sorted(owner_handoff_overlap)}"
            )
        if required_handoffs or normalized_groups:
            required_handoff_cases += 1
            if owner in known_skills:
                required_handoff_owners.add(str(owner))
        else:
            no_required_handoff_cases += 1
        if not isinstance(item.get("high_risk"), bool):
            errors.append(f"{case_id}: high_risk must be boolean")
        prompt = str(item.get("prompt", "")).casefold()
        leaked = [name for name in known_skills if name.casefold() in prompt]
        if leaked:
            errors.append(f"{case_id}: prompt leaks Skill name(s) {sorted(leaked)}")
    missing_kinds = (required_kinds or ROUTING_KINDS) - observed_kinds
    if missing_kinds:
        errors.append(f"routing: missing kinds {sorted(missing_kinds)}")
    minimum_per_skill = (
        int(ROUTING_CONTRACT["minimum_cases_per_skill"])
        if minimum_cases_per_skill is None
        else minimum_cases_per_skill
    )
    for skill_name in sorted(known_skills):
        if owner_counts[skill_name] < minimum_per_skill:
            errors.append(
                f"routing: {skill_name} requires at least {minimum_per_skill} owner cases, "
                f"found {owner_counts[skill_name]}"
            )

    minimum_required = (
        int(ROUTING_CONTRACT["minimum_required_handoff_cases"])
        if minimum_required_handoff_cases is None
        else minimum_required_handoff_cases
    )
    if required_handoff_cases < minimum_required:
        errors.append(
            "routing: expected at least "
            f"{minimum_required} required-handoff cases, found "
            f"{required_handoff_cases}"
        )
    minimum_without_required = (
        int(ROUTING_CONTRACT["minimum_no_required_handoff_cases"])
        if minimum_no_required_handoff_cases is None
        else minimum_no_required_handoff_cases
    )
    if no_required_handoff_cases < minimum_without_required:
        errors.append(
            "routing: expected at least "
            f"{minimum_without_required} no-required-handoff cases, found "
            f"{no_required_handoff_cases}"
        )
    minimum_handoff_owners = (
        int(ROUTING_CONTRACT["minimum_required_handoff_owners"])
        if minimum_required_handoff_owners is None
        else minimum_required_handoff_owners
    )
    if len(required_handoff_owners) < minimum_handoff_owners:
        errors.append(
            "routing: expected required-handoff coverage for at least "
            f"{minimum_handoff_owners} primary owners, found "
            f"{len(required_handoff_owners)} ({sorted(required_handoff_owners)})"
        )
    required_primary_owners = (
        set(ROUTING_CONTRACT["required_handoff_primary_owners"])
        if required_handoff_primary_owners is None
        else required_handoff_primary_owners
    )
    unknown_required_primary_owners = required_primary_owners - known_skills
    if unknown_required_primary_owners:
        errors.append(
            "routing: required handoff primary-owner contract contains unknown "
            f"Skills {sorted(unknown_required_primary_owners)}"
        )
    missing_required_primary_owners = (
        required_primary_owners - required_handoff_owners
    )
    if missing_required_primary_owners:
        errors.append(
            "routing: missing required-handoff cases for primary owners "
            f"{sorted(missing_required_primary_owners)}"
        )

    if not require_neighbor_graph:
        return errors

    graph_path = routing_graph_path or ROOT / "docs" / "skills" / "routing-graph.json"
    try:
        routing_graph = json.loads(
            graph_path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        errors.append(f"routing: cannot read routing graph: {error}")
    else:
        for skill_name, neighbors in routing_graph.items():
            if skill_name not in known_skills or not isinstance(neighbors, list):
                continue
            for neighbor in neighbors:
                if neighbor not in covered_neighbors[skill_name]:
                    errors.append(
                        f"routing: live corpus missing {skill_name} -> {neighbor} nearest-neighbor case"
                    )
    return errors


def validate_authority_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    errors = validate_unique_cases(cases, label="authority")
    minimum_cases = int(AUTHORITY_CONTRACT["minimum_cases"])
    if len(cases) < minimum_cases:
        errors.append(
            f"authority: expected at least {minimum_cases} cases, found {len(cases)}"
        )
    covered_owners: set[str] = set()
    for item in cases:
        case_id = str(item.get("id", "authority case"))
        if item.get("expected_owner") not in known_skills:
            errors.append(f"{case_id}: unknown expected owner {item.get('expected_owner')!r}")
        else:
            covered_owners.add(str(item["expected_owner"]))
        for key in ("forbidden_actions", "required_actions"):
            try:
                values = string_list(item, key, case_id=case_id)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not values:
                errors.append(f"{case_id}: {key} must not be empty")
    if AUTHORITY_CONTRACT.get("require_all_skills"):
        for skill_name in sorted(known_skills - covered_owners):
            errors.append(f"authority: missing owner coverage for {skill_name}")
    return errors


def validate_workflow_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    errors = validate_unique_cases(cases, label="workflow")
    minimum_cases = int(WORKFLOW_CONTRACT["minimum_cases"])
    if len(cases) < minimum_cases:
        errors.append(
            f"workflow: expected at least {minimum_cases} cases, found {len(cases)}"
        )
    covered_owners: set[str] = set()
    for item in cases:
        case_id = str(item.get("id", "workflow case"))
        for key in ("expected_route", "required_evidence", "forbidden_actions"):
            try:
                values = string_list(item, key, case_id=case_id)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not values:
                errors.append(f"{case_id}: {key} must not be empty")
            if key == "expected_route":
                for owner in values:
                    if owner not in known_skills:
                        errors.append(f"{case_id}: unknown route owner {owner!r}")
                    else:
                        covered_owners.add(owner)
        allowed_routes = item.get("allowed_routes", [])
        if not isinstance(allowed_routes, list) or any(
            not isinstance(route, list)
            or not route
            or any(not isinstance(owner, str) for owner in route)
            for route in allowed_routes
        ):
            errors.append(f"{case_id}: allowed_routes must be a list of non-empty string lists")
        else:
            for route in allowed_routes:
                for owner in route:
                    if owner not in known_skills:
                        errors.append(f"{case_id}: unknown allowed route owner {owner!r}")
        if not isinstance(item.get("title"), str) or not str(item["title"]).strip():
            errors.append(f"{case_id}: title must be non-empty")
    if WORKFLOW_CONTRACT.get("require_all_skills"):
        for skill_name in sorted(known_skills - covered_owners):
            errors.append(f"workflow: missing route coverage for {skill_name}")
    return errors


def validate_datasets(root: Path = ROOT) -> list[str]:
    known_skills = discover_skill_names(root)
    return validate_dataset_paths(
        root / "evals" / "routing.jsonl",
        root / "evals" / "authority.jsonl",
        root / "evals" / "workflow-smoke.jsonl",
        known_skills=known_skills,
        routing_graph_path=root / "docs" / "skills" / "routing-graph.json",
        routing_is_held_out=False,
    )


def validate_dataset_paths(
    routing_path: Path,
    authority_path: Path,
    workflow_path: Path,
    *,
    known_skills: set[str] | None = None,
    routing_graph_path: Path | None = None,
    routing_is_held_out: bool,
) -> list[str]:
    skills = known_skills or discover_skill_names()
    routing_cases = load_jsonl(routing_path)
    routing_errors = (
        validate_held_out_routing_cases(routing_cases, skills)
        if routing_is_held_out
        else validate_routing_cases(
            routing_cases,
            skills,
            routing_graph_path=routing_graph_path,
        )
    )
    return [
        *routing_errors,
        *validate_authority_cases(load_jsonl(authority_path), skills),
        *validate_workflow_cases(load_jsonl(workflow_path), skills),
    ]


def validate_held_out_routing_cases(
    cases: list[dict[str, object]], known_skills: set[str]
) -> list[str]:
    comparative = BEHAVIOR_CONTRACT["comparative"]
    required_owner_kinds = set(comparative["required_held_out_owner_kinds"])
    errors = validate_routing_cases(
        cases,
        known_skills,
        minimum_cases=int(comparative["minimum_held_out_cases"]),
        minimum_cases_per_skill=int(
            comparative["minimum_held_out_cases_per_skill"]
        ),
        required_kinds=(
            required_owner_kinds
            | set(comparative["required_held_out_global_kinds"])
        ),
        minimum_required_handoff_cases=int(
            comparative["minimum_held_out_required_handoff_cases"]
        ),
        minimum_no_required_handoff_cases=int(
            comparative["minimum_held_out_no_required_handoff_cases"]
        ),
        minimum_required_handoff_owners=int(
            comparative["minimum_held_out_required_handoff_owners"]
        ),
        required_handoff_primary_owners=set(
            comparative["required_held_out_handoff_primary_owners"]
        ),
        require_neighbor_graph=False,
    )
    observed_by_owner: dict[str, set[str]] = {
        skill_name: set() for skill_name in known_skills
    }
    for case in cases:
        owner = case.get("expected_owner")
        kind = case.get("kind")
        if owner in known_skills and kind in required_owner_kinds:
            observed_by_owner[str(owner)].add(str(kind))
    for skill_name in sorted(known_skills):
        missing = required_owner_kinds - observed_by_owner[skill_name]
        if missing:
            errors.append(
                f"routing: held-out owner {skill_name} missing kinds {sorted(missing)}"
            )
    return errors


def _infer_evidence_kind(dataset_path: Path) -> str:
    rows = load_jsonl(dataset_path)
    if rows and all("kind" in row and "forbidden_owners" in row for row in rows):
        return "routing"
    if rows and all("expected_route" in row for row in rows):
        return "workflow"
    if rows and all(
        "expected_owner" in row
        and "required_actions" in row
        and "forbidden_actions" in row
        for row in rows
    ):
        return "authority"
    raise ValueError(
        f"{dataset_path}: cannot infer evidence kind from dataset fields"
    )


def _validate_sha256(value: object, *, label: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"{label} must be a lowercase sha256")
    return value


def _validate_metrics(value: object, *, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    duration_ms = value.get("duration_ms")
    if (
        isinstance(duration_ms, bool)
        or not isinstance(duration_ms, int)
        or duration_ms < 1
    ):
        raise ValueError(f"{label}.duration_ms must be a positive integer")
    for metric in ("input_tokens", "output_tokens"):
        metric_value = value.get(metric)
        if metric_value is not None and (
            isinstance(metric_value, bool)
            or not isinstance(metric_value, int)
            or metric_value < 1
        ):
            raise ValueError(
                f"{label}.{metric} must be null or a positive integer"
            )
    attempt_count = value.get("attempt_count")
    retry_count = value.get("retry_count")
    if attempt_count is not None or retry_count is not None:
        if (
            isinstance(attempt_count, bool)
            or not isinstance(attempt_count, int)
            or attempt_count < 1
        ):
            raise ValueError(f"{label}.attempt_count must be a positive integer")
        if (
            isinstance(retry_count, bool)
            or not isinstance(retry_count, int)
            or retry_count < 0
            or retry_count != attempt_count - 1
        ):
            raise ValueError(
                f"{label}.retry_count must equal attempt_count - 1"
            )
    return value


def _iso_timestamp(value: object, *, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed


def _validate_attempt_interval(
    attempt: dict[str, object],
    *,
    label: str,
    latest_allowed: datetime,
) -> tuple[datetime, datetime]:
    started = _iso_timestamp(attempt.get("started_at"), label=f"{label}.started_at")
    completed = _iso_timestamp(
        attempt.get("completed_at"), label=f"{label}.completed_at"
    )
    if completed < started:
        raise ValueError(f"{label}.completed_at predates started_at")
    if started.astimezone(timezone.utc) > latest_allowed or completed.astimezone(
        timezone.utc
    ) > latest_allowed:
        raise ValueError(
            f"{label} timestamp is more than {MAXIMUM_CLOCK_SKEW_SECONDS} "
            "seconds in the future"
        )
    return started, completed


def _validate_result_timeline(
    *,
    label: str,
    captured_at: datetime,
    raw_intervals: list[tuple[datetime, datetime]],
    latest_allowed: datetime,
    attempt_interval: tuple[datetime, datetime] | None,
) -> None:
    if not raw_intervals:
        raise ValueError(f"{label}: result bundle has no raw evidence intervals")

    for index, (started, completed) in enumerate(raw_intervals):
        raw_label = f"{label}: raw interval {index}"
        if completed < started:
            raise ValueError(f"{raw_label} completed_at predates started_at")
        if started.astimezone(timezone.utc) > latest_allowed or completed.astimezone(
            timezone.utc
        ) > latest_allowed:
            raise ValueError(
                f"{raw_label} timestamp is more than "
                f"{MAXIMUM_CLOCK_SKEW_SECONDS} seconds in the future"
            )

    earliest_raw = min(started for started, _completed in raw_intervals)
    latest_raw_completed = max(completed for _started, completed in raw_intervals)
    maximum_skew = timedelta(seconds=MAXIMUM_CLOCK_SKEW_SECONDS)
    if latest_raw_completed > captured_at:
        raise ValueError(f"{label}: captured_at predates raw evidence completion")
    if captured_at - latest_raw_completed > maximum_skew:
        raise ValueError(
            f"{label}: captured_at follows raw evidence completion by more than "
            f"{MAXIMUM_CLOCK_SKEW_SECONDS} seconds"
        )

    if attempt_interval is None:
        return
    attempt_started, attempt_completed = attempt_interval
    if attempt_started > earliest_raw:
        raise ValueError(f"{label}: formal attempt starts after raw evidence")
    if earliest_raw - attempt_started > maximum_skew:
        raise ValueError(
            f"{label}: first raw evidence follows formal attempt start by more than "
            f"{MAXIMUM_CLOCK_SKEW_SECONDS} seconds"
        )
    if captured_at > attempt_completed:
        raise ValueError(f"{label}: captured_at follows formal attempt completion")
    if attempt_completed - captured_at > maximum_skew:
        raise ValueError(
            f"{label}: formal attempt completion follows captured_at by more than "
            f"{MAXIMUM_CLOCK_SKEW_SECONDS} seconds"
        )


def _validate_host_attempts(
    raw: dict[str, object],
    *,
    host_name: str,
    evidence_kind: str,
    result_id: str,
    label: str,
) -> dict[str, object]:
    policy = PROTOCOL.canonical_transient_retry_policy(host_name, CONTRACTS)
    policy_hash = PROTOCOL.canonical_hash(policy)
    _validate_sha256(
        raw.get("retry_policy_sha256"),
        label=f"{label}.retry_policy_sha256",
    )
    if raw["retry_policy_sha256"] != policy_hash:
        raise ValueError(f"{label}.retry_policy_sha256 must match canonical policy")
    attempts = raw.get("host_attempts")
    maximum_attempts = int(policy["maximum_attempts_per_case"])
    if (
        not isinstance(attempts, list)
        or not attempts
        or len(attempts) > maximum_attempts
    ):
        raise ValueError(
            f"{label}.host_attempts must contain 1..{maximum_attempts} attempts"
        )

    raw_started = _iso_timestamp(
        raw.get("started_at"), label=f"{label}.started_at"
    )
    raw_completed = _iso_timestamp(
        raw.get("completed_at"), label=f"{label}.completed_at"
    )
    if raw_completed < raw_started:
        raise ValueError(f"{label}.completed_at predates started_at")

    total_attempt_duration = 0
    total_backoff_seconds = 0
    next_attempt_not_before: datetime | None = None
    first_attempt_started: datetime | None = None
    terminal_attempt_completed: datetime | None = None
    for index, attempt in enumerate(attempts, 1):
        attempt_label = f"{label}.host_attempts[{index - 1}]"
        if not isinstance(attempt, dict) or set(attempt) != HOST_ATTEMPT_REQUIRED:
            raise ValueError(
                f"{attempt_label} fields must be {sorted(HOST_ATTEMPT_REQUIRED)}"
            )
        if attempt.get("attempt_index") != index:
            raise ValueError(f"{attempt_label}.attempt_index must equal {index}")
        started = _iso_timestamp(
            attempt.get("started_at"), label=f"{attempt_label}.started_at"
        )
        completed = _iso_timestamp(
            attempt.get("completed_at"), label=f"{attempt_label}.completed_at"
        )
        if first_attempt_started is None:
            first_attempt_started = started
        if next_attempt_not_before is not None and started < next_attempt_not_before:
            raise ValueError(
                f"{attempt_label}.started_at omits the canonical retry backoff"
            )
        if completed < started:
            raise ValueError(f"{attempt_label}.completed_at predates started_at")
        terminal_attempt_completed = completed
        duration = attempt.get("duration_ms")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration < 1:
            raise ValueError(f"{attempt_label}.duration_ms must be a positive integer")
        total_attempt_duration += duration
        stdout = attempt.get("stdout")
        stderr = attempt.get("stderr")
        transcript = attempt.get("transcript")
        if not isinstance(stdout, str) or not isinstance(stderr, str):
            raise ValueError(f"{attempt_label}.stdout/stderr must be strings")
        if transcript != f"STDOUT\n{stdout}\nSTDERR\n{stderr}":
            raise ValueError(f"{attempt_label}.transcript must match stdout/stderr")
        _validate_sha256(
            attempt.get("transcript_sha256"),
            label=f"{attempt_label}.transcript_sha256",
        )
        if attempt["transcript_sha256"] != text_hash(str(transcript)):
            raise ValueError(f"{attempt_label}.transcript_sha256 does not match")
        response = attempt.get("response")
        model_output = attempt.get("model_output")
        if not isinstance(response, str) or not isinstance(model_output, str):
            raise ValueError(f"{attempt_label}.response/model_output must be strings")
        exit_code = attempt.get("exit_code")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            raise ValueError(f"{attempt_label}.exit_code must be an integer")
        error = attempt.get("error")
        if error is not None and (not isinstance(error, str) or not error):
            raise ValueError(f"{attempt_label}.error must be null or non-empty string")
        metrics = _validate_metrics(
            attempt.get("metrics"), label=f"{attempt_label}.metrics"
        )
        if metrics["duration_ms"] != duration:
            raise ValueError(f"{attempt_label}.metrics.duration_ms must match attempt")
        normalized_usage = normalized_usage_from_stdout(stdout, host_name=host_name)
        if (
            metrics["input_tokens"],
            metrics["output_tokens"],
        ) != normalized_usage:
            raise ValueError(f"{attempt_label}.metrics must match normalized usage")
        observations = attempt.get("observations")
        observations_are_valid = False
        if observations is not None:
            try:
                _validate_observations(
                    observations,
                    evidence_kind=evidence_kind,
                    result_id=result_id,
                )
            except ValueError:
                observations_are_valid = False
            else:
                observations_are_valid = True
        has_valid_result = observations_are_valid
        if evidence_kind == "routing":
            extracted = PROTOCOL.extract_routing_result(stdout, response)
            has_valid_result = extracted is not None
            if extracted is None:
                if model_output or observations is not None:
                    raise ValueError(
                        f"{attempt_label} records a result the host output does not contain"
                    )
            else:
                extracted_output, extracted_observations = extracted
                if (
                    model_output != extracted_output
                    or observations != extracted_observations
                ):
                    raise ValueError(
                        f"{attempt_label} result does not match host response/stdout"
                    )
        classified = PROTOCOL.classify_transient_host_failure(
            host_name,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            has_valid_result=has_valid_result,
            input_tokens=metrics["input_tokens"],
            output_tokens=metrics["output_tokens"],
            contract=CONTRACTS,
        )
        if attempt.get("error_class") != classified:
            raise ValueError(f"{attempt_label}.error_class is not canonical")
        if attempt.get("retryable") is not (classified is not None):
            raise ValueError(f"{attempt_label}.retryable is not canonical")
        backoff = attempt.get("backoff_seconds_before_next")
        if isinstance(backoff, bool) or not isinstance(backoff, int) or backoff < 0:
            raise ValueError(
                f"{attempt_label}.backoff_seconds_before_next must be non-negative"
            )
        is_terminal = index == len(attempts)
        expected_backoff = (
            0 if is_terminal else int(policy["backoff_seconds"][index - 1])
        )
        if backoff != expected_backoff:
            raise ValueError(f"{attempt_label}.backoff_seconds_before_next is not canonical")
        if not is_terminal and classified is None:
            raise ValueError(f"{attempt_label} non-terminal attempt is not retryable")
        total_backoff_seconds += backoff
        next_attempt_not_before = completed + timedelta(seconds=backoff)

    if first_attempt_started is None or terminal_attempt_completed is None:
        raise ValueError(f"{label}.host_attempts cannot be empty")
    if raw_started > first_attempt_started:
        raise ValueError(f"{label}.started_at must not follow the first host attempt")
    if raw_completed < terminal_attempt_completed:
        raise ValueError(f"{label}.completed_at must include the terminal host attempt")

    terminal = attempts[-1]
    for key in (
        "exit_code",
        "stdout",
        "stderr",
        "model_output",
        "transcript",
        "transcript_sha256",
        "observations",
    ):
        if raw.get(key) != terminal.get(key):
            raise ValueError(f"{label} terminal attempt does not match raw {key}")
    raw_metrics = _validate_metrics(raw.get("metrics"), label=f"{label}.metrics")
    if raw_metrics.get("attempt_count") != len(attempts):
        raise ValueError(f"{label}.metrics.attempt_count must match host_attempts")
    if raw_metrics.get("retry_count") != len(attempts) - 1:
        raise ValueError(f"{label}.metrics.retry_count must match host_attempts")
    if (
        raw_metrics["input_tokens"] != terminal["metrics"]["input_tokens"]
        or raw_metrics["output_tokens"] != terminal["metrics"]["output_tokens"]
    ):
        raise ValueError(f"{label}.metrics token usage must match terminal attempt")
    minimum_duration = total_attempt_duration + total_backoff_seconds * 1000
    rounding_tolerance_ms = len(attempts)
    if raw_metrics["duration_ms"] + rounding_tolerance_ms < minimum_duration:
        raise ValueError(f"{label}.metrics.duration_ms omits attempts or backoff")
    return terminal


def _validate_observations(
    observations: object, *, evidence_kind: str, result_id: str
) -> dict[str, object]:
    if not isinstance(observations, dict):
        raise ValueError(f"{result_id}: raw observations must be an object")

    if evidence_kind == "routing":
        actual_owner = observations.get("actual_owner")
        if not isinstance(actual_owner, str) or not actual_owner.strip():
            raise ValueError(
                f"{result_id}: raw observations.actual_owner must be a non-empty string"
            )
        unique_string_list(
            observations, "handoffs", case_id=f"{result_id}: raw observations"
        )
    elif evidence_kind == "authority":
        actual_owner = observations.get("actual_owner")
        if not isinstance(actual_owner, str) or not actual_owner.strip():
            raise ValueError(
                f"{result_id}: raw observations.actual_owner must be a non-empty string"
            )
        unique_string_list(
            observations,
            "observed_actions",
            case_id=f"{result_id}: raw observations",
        )
    elif evidence_kind == "workflow":
        for key in ("route", "observed_evidence", "observed_actions"):
            unique_string_list(
                observations, key, case_id=f"{result_id}: raw observations"
            )
    else:
        raise ValueError(f"{result_id}: unknown evidence kind {evidence_kind!r}")
    return observations


def _validate_execution_trace(raw: dict[str, object], *, result_id: str) -> None:
    trace = raw.get("trace")
    if not isinstance(trace, list) or not trace:
        raise ValueError(f"{result_id}: raw trace must be a non-empty object list")
    traced_actions: list[str] = []
    for index, entry in enumerate(trace):
        if not isinstance(entry, dict):
            raise ValueError(f"{result_id}: raw trace[{index}] must be an object")
        for key in ("source", "type", "action", "detail"):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{result_id}: raw trace[{index}].{key} must be a non-empty string"
                )
        _validate_sha256(
            entry.get("detail_sha256"),
            label=f"{result_id}: raw trace[{index}].detail_sha256",
        )
        if entry["detail_sha256"] != text_hash(str(entry["detail"])):
            raise ValueError(
                f"{result_id}: raw trace[{index}].detail_sha256 must match detail"
            )
        traced_actions.append(str(entry["action"]))
    if len(traced_actions) != len(set(traced_actions)):
        raise ValueError(f"{result_id}: raw trace actions must not contain duplicates")

    workspace = raw.get("workspace")
    if not isinstance(workspace, dict):
        raise ValueError(f"{result_id}: raw workspace must be an object")
    before_manifest = workspace.get("before_manifest")
    after_manifest = workspace.get("after_manifest")
    for key, manifest in (
        ("before_manifest", before_manifest),
        ("after_manifest", after_manifest),
    ):
        if not isinstance(manifest, dict) or any(
            not isinstance(path, str)
            or not path
            or not isinstance(file_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", file_hash) is None
            for path, file_hash in manifest.items()
        ):
            raise ValueError(
                f"{result_id}: raw workspace.{key} must map relative paths to sha256"
            )
        for path in manifest:
            parsed_path = PurePosixPath(path)
            if (
                parsed_path.is_absolute()
                or ".." in parsed_path.parts
                or parsed_path.as_posix() != path
            ):
                raise ValueError(
                    f"{result_id}: raw workspace.{key} has invalid path {path!r}"
                )
    for key, manifest in (
        ("before_sha256", before_manifest),
        ("after_sha256", after_manifest),
    ):
        _validate_sha256(workspace.get(key), label=f"{result_id}: raw workspace.{key}")
        if workspace[key] != canonical_json_hash(manifest):
            raise ValueError(
                f"{result_id}: raw workspace.{key} must match its manifest"
            )
    diff = workspace.get("diff")
    if not isinstance(diff, str):
        raise ValueError(f"{result_id}: raw workspace.diff must be a string")
    _validate_sha256(
        workspace.get("diff_sha256"),
        label=f"{result_id}: raw workspace.diff_sha256",
    )
    if workspace["diff_sha256"] != text_hash(diff):
        raise ValueError(f"{result_id}: raw workspace.diff_sha256 must match diff")
    changed_files = workspace.get("changed_files")
    if not isinstance(changed_files, list) or any(
        not isinstance(entry, str) or not entry.strip() for entry in changed_files
    ):
        raise ValueError(
            f"{result_id}: raw workspace.changed_files must be a string list"
        )
    normalized_paths: set[str] = set()
    for entry in changed_files:
        if "\\" in entry:
            raise ValueError(
                f"{result_id}: changed file must use a relative POSIX path: {entry!r}"
            )
        parsed = PurePosixPath(entry)
        normalized = parsed.as_posix()
        if (
            parsed.is_absolute()
            or normalized in {"", "."}
            or ".." in parsed.parts
            or normalized != entry
        ):
            raise ValueError(
                f"{result_id}: changed file must be a normalized relative path: {entry!r}"
            )
        if normalized in normalized_paths:
            raise ValueError(
                f"{result_id}: raw workspace.changed_files must not contain duplicates"
            )
        normalized_paths.add(normalized)
    manifest_changed = {
        path
        for path in set(before_manifest) | set(after_manifest)
        if before_manifest.get(path) != after_manifest.get(path)
    }
    if normalized_paths != manifest_changed:
        raise ValueError(
            f"{result_id}: raw workspace.changed_files must match before/after manifests"
        )

    verifier = raw.get("verifier")
    if not isinstance(verifier, dict):
        raise ValueError(f"{result_id}: raw verifier must be an object")
    checks = verifier.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError(
            f"{result_id}: raw verifier.checks must be a non-empty object list"
        )
    verified_evidence: list[str] = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}] must be an object"
            )
        command = check.get("command")
        if not isinstance(command, str) or not command.strip():
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}].command must be a non-empty string"
            )
        exit_code = check.get("exit_code")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}].exit_code must be an integer"
            )
        stdout = check.get("stdout")
        if not isinstance(stdout, str):
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}].stdout must be a string"
            )
        _validate_sha256(
            check.get("stdout_sha256"),
            label=f"{result_id}: raw verifier.checks[{index}].stdout_sha256",
        )
        if check["stdout_sha256"] != text_hash(stdout):
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}].stdout_sha256 must match stdout"
            )
        if not isinstance(check.get("passed"), bool):
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}].passed must be boolean"
            )
        if check["passed"] and exit_code != 0:
            raise ValueError(
                f"{result_id}: raw verifier.checks[{index}] cannot pass with nonzero exit_code"
            )
        evidence = unique_string_list(
            check,
            "evidence",
            case_id=f"{result_id}: raw verifier.checks[{index}]",
            default=[],
        )
        if check["passed"]:
            verified_evidence.extend(evidence)
    if len(verified_evidence) != len(set(verified_evidence)):
        raise ValueError(
            f"{result_id}: passing verifier evidence labels must not contain duplicates"
        )

    observations = raw["observations"]
    observed_actions = observations.get("observed_actions", [])
    if set(observed_actions) != set(traced_actions):
        raise ValueError(
            f"{result_id}: raw observations.observed_actions must match trace actions"
        )
    if "observed_evidence" in observations and set(
        observations["observed_evidence"]
    ) != set(verified_evidence):
        raise ValueError(
            f"{result_id}: raw observations.observed_evidence must match passing verifier evidence"
        )


def _expected_prompt_map(
    dataset_path: Path,
    expected_ids: set[str],
    expected_prompts: dict[str, str] | None,
) -> dict[str, str]:
    if expected_prompts is None:
        expected_prompts = {}
        for row in load_jsonl(dataset_path):
            case_id = row.get("id")
            prompt = row.get("prompt")
            if not isinstance(case_id, str) or not isinstance(prompt, str):
                raise ValueError(
                    f"{dataset_path}: every row must provide string id and prompt"
                )
            expected_prompts[case_id] = prompt
    if set(expected_prompts) != expected_ids:
        missing = sorted(expected_ids - set(expected_prompts))
        extra = sorted(set(expected_prompts) - expected_ids)
        raise ValueError(
            f"{dataset_path}: prompt coverage mismatch; missing={missing}, extra={extra}"
        )
    for case_id, prompt in expected_prompts.items():
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{case_id}: expected prompt must be a non-empty string")
    return expected_prompts


def _validate_held_out_provenance(
    dataset_path: Path,
    skill_revision: str,
    run_config: dict[str, object],
    *,
    bundle_path: Path,
) -> None:
    if dataset_path.resolve() == ROUTING_DATA.resolve():
        raise ValueError(
            f"{bundle_path}: the public routing dataset cannot be marked held_out"
        )
    missing = HELD_OUT_PROVENANCE_REQUIRED - set(run_config)
    if missing:
        raise ValueError(
            f"{bundle_path}: held-out run_config missing fields {sorted(missing)}"
        )
    evaluation_anchor_revision = run_config.get("evaluation_anchor_revision")
    if not isinstance(evaluation_anchor_revision, str) or re.fullmatch(
        r"[0-9a-f]{40}", evaluation_anchor_revision
    ) is None:
        raise ValueError(
            f"{bundle_path}: run_config.evaluation_anchor_revision must be a "
            "40-character Git SHA"
        )
    anchor_commit = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            f"{evaluation_anchor_revision}^{{commit}}",
        ],
        check=False,
        capture_output=True,
    )
    if anchor_commit.returncode != 0:
        raise ValueError(
            f"{bundle_path}: evaluation_anchor_revision is not a repository commit"
        )
    variant = run_config.get("variant")
    if variant in {"candidate", "baseline"}:
        if skill_revision != evaluation_anchor_revision:
            raise ValueError(
                f"{bundle_path}: {variant} skill_revision must equal "
                "evaluation_anchor_revision"
            )
    elif variant == "previous":
        if not revision_is_ancestor(
            skill_revision, evaluation_anchor_revision, strict=True
        ):
            raise ValueError(
                f"{bundle_path}: previous skill_revision must be a strict ancestor "
                "of evaluation_anchor_revision"
            )
    else:
        raise ValueError(
            f"{bundle_path}: run_config.variant must be one of "
            f"{sorted(RESULT_VARIANTS)}"
        )
    try:
        dataset_relative = dataset_path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(
            f"{bundle_path}: held-out dataset must be committed inside the repository"
        ) from error
    if run_config.get("dataset_path") != dataset_relative:
        raise ValueError(
            f"{bundle_path}: run_config.dataset_path must equal {dataset_relative!r}"
        )
    provenance_relative = run_config.get("held_out_provenance_path")
    if (
        not isinstance(provenance_relative, str)
        or not provenance_relative.strip()
        or "\\" in provenance_relative
        or PurePosixPath(provenance_relative).is_absolute()
        or ".." in PurePosixPath(provenance_relative).parts
        or PurePosixPath(provenance_relative).as_posix() != provenance_relative
    ):
        raise ValueError(
            f"{bundle_path}: run_config.held_out_provenance_path must be a "
            "normalized repository-relative POSIX path"
        )
    provenance_path = (ROOT / provenance_relative).resolve()
    try:
        provenance_path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(
            f"{bundle_path}: held-out provenance escapes the repository"
        ) from error
    if not provenance_path.is_file():
        raise ValueError(f"{bundle_path}: held-out provenance file does not exist")
    provenance_sha256 = run_config.get("held_out_provenance_sha256")
    _validate_sha256(
        provenance_sha256,
        label=f"{bundle_path}: run_config.held_out_provenance_sha256",
    )
    if provenance_sha256 != dataset_hash(provenance_path):
        raise ValueError(
            f"{bundle_path}: run_config.held_out_provenance_sha256 must match "
            "the provenance file"
        )
    try:
        provenance = json.loads(
            provenance_path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"{bundle_path}: cannot read held-out provenance: {error}"
        ) from error
    provenance_fields = {
        "schema_version",
        "dataset_path",
        "dataset_sha256",
        "source_skill_revision",
        "authorship",
        "used_for_tuning",
        "intended_hosts",
    }
    if not isinstance(provenance, dict) or set(provenance) != provenance_fields:
        raise ValueError(
            f"{bundle_path}: held-out provenance fields must be "
            f"{sorted(provenance_fields)}"
        )
    if provenance.get("schema_version") != 1:
        raise ValueError(
            f"{bundle_path}: held-out provenance schema_version must be 1"
        )
    if provenance.get("dataset_path") != dataset_relative:
        raise ValueError(
            f"{bundle_path}: held-out provenance dataset_path must match the dataset"
        )
    if provenance.get("dataset_sha256") != dataset_hash(dataset_path):
        raise ValueError(
            f"{bundle_path}: held-out provenance dataset_sha256 must match the dataset"
        )
    if provenance.get("source_skill_revision") != evaluation_anchor_revision:
        raise ValueError(
            f"{bundle_path}: held-out provenance source_skill_revision must match "
            "evaluation_anchor_revision"
        )
    authorship = provenance.get("authorship")
    expected_authorship = {
        "independent": True,
        "timing": "post_freeze",
        "existing_eval_comparison": "after_drafting_only",
    }
    if authorship != expected_authorship:
        raise ValueError(
            f"{bundle_path}: held-out provenance must attest independent post-freeze "
            "authorship and comparison only after drafting"
        )
    if provenance.get("used_for_tuning") is not False:
        raise ValueError(
            f"{bundle_path}: held-out provenance used_for_tuning must be false"
        )
    intended_hosts = provenance.get("intended_hosts")
    if (
        not isinstance(intended_hosts, list)
        or not intended_hosts
        or any(
            not isinstance(host, str) or host not in {"codex", "claude"}
            for host in intended_hosts
        )
        or len(intended_hosts) != len(set(intended_hosts))
        or run_config.get("host_name") not in intended_hosts
    ):
        raise ValueError(
            f"{bundle_path}: held-out provenance intended_hosts must uniquely include "
            "the evaluated host"
        )
    dataset_git_revision = run_config.get("dataset_git_revision")
    if not isinstance(dataset_git_revision, str) or re.fullmatch(
        r"[0-9a-f]{40}", dataset_git_revision
    ) is None:
        raise ValueError(
            f"{bundle_path}: run_config.dataset_git_revision must be a 40-character Git SHA"
        )
    dataset_commit = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            f"{dataset_git_revision}^{{commit}}",
        ],
        check=False,
        capture_output=True,
    )
    if dataset_commit.returncode != 0:
        raise ValueError(
            f"{bundle_path}: dataset_git_revision is not a repository commit"
        )
    for ancestor, descendant, label, require_strict in (
        (
            evaluation_anchor_revision,
            dataset_git_revision,
            "postdate the evaluation anchor revision",
            True,
        ),
        (
            dataset_git_revision,
            "HEAD",
            "be reachable from current HEAD",
            False,
        ),
    ):
        check = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "merge-base",
                "--is-ancestor",
                ancestor,
                descendant,
            ],
            check=False,
            capture_output=True,
        )
        if check.returncode != 0 or (require_strict and ancestor == descendant):
            raise ValueError(
                f"{bundle_path}: held-out dataset revision must {label}"
            )
    for relative_path, label in (
        (dataset_relative, "dataset"),
        (provenance_relative, "provenance"),
    ):
        path_history = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "log",
                "--format=%H",
                f"{evaluation_anchor_revision}..HEAD",
                "--",
                relative_path,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if (
            path_history.returncode != 0
            or path_history.stdout.splitlines() != [dataset_git_revision]
        ):
            raise ValueError(
                f"{bundle_path}: held-out {label} must have exactly one post-anchor "
                "history entry equal to dataset_git_revision so dataset and provenance "
                "are introduced together and never retrofitted"
            )
    dataset_blob = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "show",
            f"{dataset_git_revision}:{dataset_relative}",
        ],
        check=False,
        capture_output=True,
    )
    if dataset_blob.returncode != 0 or dataset_blob.stdout != dataset_path.read_bytes():
        raise ValueError(
            f"{bundle_path}: held-out dataset content must match dataset_git_revision"
        )
    provenance_blob = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "show",
            f"{dataset_git_revision}:{provenance_relative}",
        ],
        check=False,
        capture_output=True,
    )
    if (
        provenance_blob.returncode != 0
        or provenance_blob.stdout != provenance_path.read_bytes()
    ):
        raise ValueError(
            f"{bundle_path}: held-out provenance must be committed unchanged at "
            "dataset_git_revision"
        )
    existed_at_skill_revision = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            f"{evaluation_anchor_revision}:{dataset_relative}",
        ],
        check=False,
        capture_output=True,
    )
    if existed_at_skill_revision.returncode == 0:
        raise ValueError(
            f"{bundle_path}: held-out dataset path already existed at skill_revision"
        )
    provenance_existed_at_skill_revision = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            f"{evaluation_anchor_revision}:{provenance_relative}",
        ],
        check=False,
        capture_output=True,
    )
    if provenance_existed_at_skill_revision.returncode == 0:
        raise ValueError(
            f"{bundle_path}: held-out provenance path already existed at skill_revision"
        )

    # A postdated filename alone is not a holdout: reject cases or prompts copied
    # from any repository eval dataset that existed at the evaluated Skill revision.
    known_case_ids: dict[str, str] = {}
    known_prompt_fingerprints: dict[str, str] = {}
    tracked_eval_paths = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-tree",
            "-r",
            "--name-only",
            evaluation_anchor_revision,
            "--",
            "evals",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked_eval_paths.returncode != 0:
        raise ValueError(
            f"{bundle_path}: cannot inspect eval datasets at skill_revision"
        )
    for relative_path in tracked_eval_paths.stdout.splitlines():
        if not relative_path.endswith(".jsonl"):
            continue
        historical = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                f"{evaluation_anchor_revision}:{relative_path}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if historical.returncode != 0:
            raise ValueError(
                f"{bundle_path}: cannot read {relative_path} at skill_revision"
            )
        for line_number, line in enumerate(historical.stdout.splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line, object_pairs_hook=reject_duplicate_json_keys)
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(
                    f"{bundle_path}: invalid historical dataset "
                    f"{relative_path}:{line_number}: {error}"
                ) from error
            if not isinstance(row, dict):
                continue
            case_id = row.get("id")
            prompt = row.get("prompt")
            if isinstance(case_id, str) and case_id:
                known_case_ids.setdefault(case_id, relative_path)
            if isinstance(prompt, str) and prompt:
                known_prompt_fingerprints.setdefault(
                    PROTOCOL.canonical_prompt_fingerprint(prompt), relative_path
                )

    tracked_skill_paths = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-tree",
            "-r",
            "--name-only",
            evaluation_anchor_revision,
            "--",
            "skills",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked_skill_paths.returncode != 0:
        raise ValueError(
            f"{bundle_path}: cannot inspect Skill eval cases at skill_revision"
        )
    for relative_path in tracked_skill_paths.stdout.splitlines():
        path = PurePosixPath(relative_path)
        if (
            len(path.parts) != 4
            or path.parts[0] != "skills"
            or path.parts[2:] != ("references", "eval-cases.md")
        ):
            continue
        historical = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                f"{evaluation_anchor_revision}:{relative_path}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if historical.returncode != 0:
            raise ValueError(
                f"{bundle_path}: cannot read {relative_path} at skill_revision"
            )
        for line in historical.stdout.splitlines():
            match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
            if match is None:
                continue
            prompt = match.group(1)
            known_prompt_fingerprints.setdefault(
                PROTOCOL.canonical_prompt_fingerprint(prompt), relative_path
            )

    overlaps: list[str] = []
    for row in load_jsonl(dataset_path):
        case_id = row.get("id")
        prompt = row.get("prompt")
        if isinstance(case_id, str) and case_id in known_case_ids:
            overlaps.append(f"case id {case_id!r} from {known_case_ids[case_id]}")
        if isinstance(prompt, str):
            prompt_fingerprint = PROTOCOL.canonical_prompt_fingerprint(prompt)
            if prompt_fingerprint in known_prompt_fingerprints:
                overlaps.append(
                    "canonical prompt fingerprint "
                    f"{prompt_fingerprint} from "
                    f"{known_prompt_fingerprints[prompt_fingerprint]}"
                )
    if overlaps:
        raise ValueError(
            f"{bundle_path}: held-out dataset overlaps eval data present at "
            f"skill_revision: {sorted(set(overlaps))}"
        )


def load_result_bundle(
    path: Path,
    expected_ids: set[str],
    dataset_path: Path,
    expected_prompts: dict[str, str] | None = None,
    *,
    evidence_kind: str | None = None,
) -> dict[str, object]:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{path}: cannot read result bundle: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: result root must be an object")
    missing_metadata = REQUIRED_METADATA - set(payload)
    if missing_metadata:
        raise ValueError(f"{path}: missing metadata {sorted(missing_metadata)}")

    if payload["schema_version"] != RESULT_SCHEMA_VERSION:
        raise ValueError(
            f"{path}: schema_version must be {RESULT_SCHEMA_VERSION}, "
            f"found {payload['schema_version']!r}"
        )
    for key in (
        "run_id",
        "model",
        "host",
        "skill_revision",
        "skill_tree_sha",
        "dataset_revision",
        "captured_at",
    ):
        if not isinstance(payload[key], str) or not str(payload[key]).strip():
            raise ValueError(f"{path}: {key} must be a non-empty string")
    if payload["complete"] is not True:
        raise ValueError(f"{path}: complete must be true")

    run_id = str(payload["run_id"])
    try:
        uuid.UUID(run_id)
    except ValueError as error:
        raise ValueError(f"{path}: run_id must be a UUID") from error

    revision = str(payload["skill_revision"])
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError(f"{path}: skill_revision must be a committed 40-character Git SHA")
    commit_check = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{revision}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if commit_check.returncode != 0:
        raise ValueError(f"{path}: skill_revision {revision} is not a commit in this repository")
    ancestor_check = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", revision, "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestor_check.returncode != 0:
        raise ValueError(
            f"{path}: skill_revision {revision} must be reachable from current HEAD"
        )

    tree_check = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "rev-parse",
            "--verify",
            f"{revision}:skills",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if tree_check.returncode != 0:
        raise ValueError(
            f"{path}: skill_revision {revision} does not contain a skills tree"
        )
    expected_skill_tree = tree_check.stdout.strip()
    if payload["skill_tree_sha"] != expected_skill_tree:
        raise ValueError(
            f"{path}: skill_tree_sha must equal {revision}:skills tree "
            f"{expected_skill_tree}"
        )

    dataset_revision = str(payload["dataset_revision"])
    expected_hash = dataset_hash(dataset_path)
    if dataset_revision != expected_hash:
        raise ValueError(
            f"{path}: dataset_revision must be the exact dataset sha256 {expected_hash}"
        )
    dataset_cases = load_jsonl(dataset_path)

    captured_at = str(payload["captured_at"])
    try:
        captured = datetime.fromisoformat(captured_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{path}: captured_at must be an ISO-8601 timestamp") from error
    if captured.tzinfo is None:
        raise ValueError(f"{path}: captured_at must include a timezone")
    latest_allowed = datetime.now(timezone.utc) + timedelta(
        seconds=MAXIMUM_CLOCK_SKEW_SECONDS
    )
    if captured.astimezone(timezone.utc) > latest_allowed:
        raise ValueError(
            f"{path}: captured_at is more than {MAXIMUM_CLOCK_SKEW_SECONDS} "
            "seconds in the future"
        )
    commit_time_check = subprocess.run(
        ["git", "-C", str(ROOT), "show", "-s", "--format=%cI", revision],
        check=False,
        capture_output=True,
        text=True,
    )
    if commit_time_check.returncode != 0:
        raise ValueError(f"{path}: cannot read skill_revision commit timestamp")
    commit_time = datetime.fromisoformat(commit_time_check.stdout.strip())
    earliest_allowed = commit_time.astimezone(timezone.utc) - timedelta(
        seconds=MAXIMUM_CLOCK_SKEW_SECONDS
    )
    if captured.astimezone(timezone.utc) < earliest_allowed:
        raise ValueError(
            f"{path}: captured_at predates skill_revision by more than "
            f"{MAXIMUM_CLOCK_SKEW_SECONDS} seconds"
        )

    run_config = payload["run_config"]
    if not isinstance(run_config, dict):
        raise ValueError(f"{path}: run_config must be an object")
    missing_run_config = RUN_CONFIG_REQUIRED - set(run_config)
    if missing_run_config:
        raise ValueError(
            f"{path}: run_config missing fields {sorted(missing_run_config)}"
        )
    trial = run_config.get("trial")
    if isinstance(trial, bool) or not isinstance(trial, int) or trial < 1:
        raise ValueError(f"{path}: run_config.trial must be a positive integer")
    if run_config.get("variant") not in RESULT_VARIANTS:
        raise ValueError(
            f"{path}: run_config.variant must be one of {sorted(RESULT_VARIANTS)}"
        )
    if run_config.get("prompt_set_sha256") != dataset_revision:
        raise ValueError(
            f"{path}: run_config.prompt_set_sha256 must equal dataset_revision"
        )
    configured_dataset_path = run_config.get("dataset_path")
    if (
        not isinstance(configured_dataset_path, str)
        or not configured_dataset_path.strip()
        or "\\" in configured_dataset_path
        or PurePosixPath(configured_dataset_path).is_absolute()
        or ".." in PurePosixPath(configured_dataset_path).parts
        or PurePosixPath(configured_dataset_path).as_posix()
        != configured_dataset_path
    ):
        raise ValueError(
            f"{path}: run_config.dataset_path must be a normalized relative POSIX path"
        )
    try:
        repository_dataset_path = dataset_path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        repository_dataset_path = None
    if (
        repository_dataset_path is not None
        and configured_dataset_path != repository_dataset_path.as_posix()
    ):
        raise ValueError(
            f"{path}: run_config.dataset_path does not match the evaluated dataset"
        )
    dataset_case_ids = [str(case.get("id", "")) for case in dataset_cases]
    case_ids = run_config.get("case_ids")
    if case_ids != dataset_case_ids:
        raise ValueError(
            f"{path}: run_config.case_ids must match the complete dataset order"
        )
    if run_config.get("case_set_sha256") != case_set_hash(dataset_cases):
        raise ValueError(
            f"{path}: run_config.case_set_sha256 must match the complete dataset"
        )
    comparison_group_id = run_config.get("comparison_group_id")
    if not isinstance(comparison_group_id, str):
        raise ValueError(
            f"{path}: run_config.comparison_group_id must be a UUID"
        )
    try:
        uuid.UUID(comparison_group_id)
    except ValueError as error:
        raise ValueError(
            f"{path}: run_config.comparison_group_id must be a UUID"
        ) from error
    if not isinstance(run_config.get("held_out"), bool):
        raise ValueError(f"{path}: run_config.held_out must be boolean")
    permissions = run_config.get("permissions")
    if not isinstance(permissions, str) or not permissions.strip():
        raise ValueError(
            f"{path}: run_config.permissions must be a non-empty string"
        )
    timeout_seconds = run_config.get("timeout_seconds")
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, int)
        or timeout_seconds < 1
    ):
        raise ValueError(
            f"{path}: run_config.timeout_seconds must be a positive integer"
        )
    concurrency = run_config.get("concurrency")
    if (
        isinstance(concurrency, bool)
        or not isinstance(concurrency, int)
        or concurrency < 1
    ):
        raise ValueError(
            f"{path}: run_config.concurrency must be a positive integer"
        )
    host_name = run_config.get("host_name")
    if host_name not in {"codex", "claude"}:
        raise ValueError(
            f"{path}: run_config.host_name must be 'codex' or 'claude'"
        )
    model = str(payload["model"])
    alias_names = {"auto", "default", "latest", "opus", "sonnet", "haiku", "fable"}
    if model.casefold() in alias_names or not any(character.isdigit() for character in model):
        raise ValueError(
            f"{path}: model must be a versioned identifier, not a mutable alias"
        )
    fixture_sha256 = run_config.get("fixture_sha256")
    fixture = run_config.get("fixture")
    if fixture_sha256 is None:
        if fixture is not None:
            raise ValueError(
                f"{path}: run_config.fixture must be null when fixture_sha256 is null"
            )
    else:
        _validate_sha256(
            fixture_sha256, label=f"{path}: run_config.fixture_sha256"
        )
        if fixture_sha256 != canonical_json_hash(fixture):
            raise ValueError(
                f"{path}: run_config.fixture_sha256 must match run_config.fixture"
            )
    skills_installed = run_config.get("skills_installed")
    if not isinstance(skills_installed, bool):
        raise ValueError(f"{path}: run_config.skills_installed must be boolean")
    variant = str(run_config["variant"])
    skill_fixture_sha256 = run_config.get("skill_fixture_sha256")
    if variant in {"candidate", "previous"}:
        if skills_installed is not True:
            raise ValueError(
                f"{path}: {variant} must set run_config.skills_installed=true"
            )
        expected_fixture_hash = committed_skill_fixture_hash(revision)
        if skill_fixture_sha256 != expected_fixture_hash:
            raise ValueError(
                f"{path}: run_config.skill_fixture_sha256 must match the committed Skill export"
            )
    elif skills_installed is not False or skill_fixture_sha256 is not None:
        raise ValueError(
            f"{path}: baseline must disable skills and set skill_fixture_sha256=null"
        )
    prompt_template_version = run_config.get("prompt_template_version")
    if prompt_template_version != PROMPT_TEMPLATE_VERSION:
        raise ValueError(
            f"{path}: run_config.prompt_template_version must be "
            f"{PROMPT_TEMPLATE_VERSION}"
        )
    prompt_template = run_config.get("prompt_template")
    if (
        not isinstance(prompt_template, str)
        or not prompt_template.strip()
        or prompt_template.count(PROMPT_VALUE_PLACEHOLDER) != 1
    ):
        raise ValueError(
            f"{path}: run_config.prompt_template must contain exactly one "
            f"{PROMPT_VALUE_PLACEHOLDER} placeholder"
        )
    _validate_sha256(
        run_config.get("prompt_template_sha256"),
        label=f"{path}: run_config.prompt_template_sha256",
    )
    if run_config["prompt_template_sha256"] != text_hash(prompt_template):
        raise ValueError(
            f"{path}: run_config.prompt_template_sha256 must match prompt_template"
        )
    canonical_prompt = PROTOCOL.canonical_prompt_template(CONTRACTS)
    if prompt_template != canonical_prompt:
        raise ValueError(
            f"{path}: run_config.prompt_template must equal the canonical routing prompt"
        )
    _validate_sha256(
        run_config.get("host_config_sha256"),
        label=f"{path}: run_config.host_config_sha256",
    )
    expected_host_policy = PROTOCOL.canonical_host_policy(
        str(host_name), model, CONTRACTS
    )
    if run_config["host_config_sha256"] != PROTOCOL.canonical_hash(
        expected_host_policy
    ):
        raise ValueError(
            f"{path}: run_config.host_config_sha256 must match the canonical host policy"
        )
    _validate_sha256(
        run_config.get("environment_policy_sha256"),
        label=f"{path}: run_config.environment_policy_sha256",
    )
    expected_environment_hash = PROTOCOL.canonical_hash(
        PROTOCOL.canonical_environment_policy(str(host_name), CONTRACTS)
    )
    if run_config["environment_policy_sha256"] != expected_environment_hash:
        raise ValueError(
            f"{path}: run_config.environment_policy_sha256 must match the canonical "
            "environment allowlist policy"
        )
    _validate_sha256(
        run_config.get("retry_policy_sha256"),
        label=f"{path}: run_config.retry_policy_sha256",
    )
    expected_retry_hash = PROTOCOL.canonical_hash(
        PROTOCOL.canonical_transient_retry_policy(str(host_name), CONTRACTS)
    )
    if run_config["retry_policy_sha256"] != expected_retry_hash:
        raise ValueError(
            f"{path}: run_config.retry_policy_sha256 must match the canonical "
            "transient retry policy"
        )

    attempt_id = run_config.get("attempt_id")
    try:
        if not isinstance(attempt_id, str):
            raise ValueError
        uuid.UUID(attempt_id)
    except ValueError as error:
        raise ValueError(f"{path}: run_config.attempt_id must be a UUID") from error
    attempt_relative = run_config.get("attempt_path")
    if (
        not isinstance(attempt_relative, str)
        or PurePosixPath(attempt_relative).is_absolute()
        or ".." in PurePosixPath(attempt_relative).parts
        or PurePosixPath(attempt_relative).as_posix() != attempt_relative
    ):
        raise ValueError(
            f"{path}: run_config.attempt_path must be a normalized relative POSIX path"
        )
    attempt_path = (path.parent / attempt_relative).resolve()
    try:
        attempt_path.relative_to(path.parent.resolve())
    except ValueError as error:
        raise ValueError(f"{path}: run_config.attempt_path escapes bundle directory") from error
    attempt_interval: tuple[datetime, datetime] | None = None
    if run_config["held_out"]:
        try:
            attempt = json.loads(
                attempt_path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise ValueError(f"{path}: cannot read formal attempt ledger: {error}") from error
        if not isinstance(attempt, dict):
            raise ValueError(f"{path}: formal attempt ledger must be an object")
        expected_attempt_fields = set(BEHAVIOR_CONTRACT["attempt_required_fields"])
        if set(attempt) != expected_attempt_fields:
            raise ValueError(
                f"{path}: formal attempt ledger fields must be "
                f"{sorted(expected_attempt_fields)}"
            )
        expected_attempt = {
            "attempt_id": attempt_id,
            "campaign_id": run_config.get("campaign_id"),
            "trial": trial,
            "variant": variant,
            "comparison_group_id": comparison_group_id,
            "status": "success",
            "run_id": run_id,
            "artifact": path.name,
            "artifact_sha256": dataset_hash(path),
        }
        for key, expected_value in expected_attempt.items():
            if attempt.get(key) != expected_value:
                raise ValueError(
                    f"{path}: formal attempt ledger {key} does not match the bundle"
                )
        if attempt.get("schema_version") != BEHAVIOR_CONTRACT["attempt_schema_version"]:
            raise ValueError(f"{path}: formal attempt ledger schema_version is invalid")
        attempt_interval = _validate_attempt_interval(
            attempt,
            label=f"{path}: formal attempt ledger",
            latest_allowed=latest_allowed,
        )
    if run_config["held_out"]:
        _validate_held_out_provenance(
            dataset_path,
            revision,
            run_config,
            bundle_path=path,
        )
        dataset_commit_time_check = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                "-s",
                "--format=%cI",
                str(run_config["dataset_git_revision"]),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            dataset_commit_time = datetime.fromisoformat(
                dataset_commit_time_check.stdout.strip()
            )
        except ValueError as error:
            raise ValueError(
                f"{path}: cannot read held-out dataset commit timestamp"
            ) from error
        dataset_earliest = dataset_commit_time.astimezone(timezone.utc) - timedelta(
            seconds=MAXIMUM_CLOCK_SKEW_SECONDS
        )
        if captured.astimezone(timezone.utc) < dataset_earliest:
            raise ValueError(
                f"{path}: captured_at predates held-out dataset/provenance commit "
                f"by more than {MAXIMUM_CLOCK_SKEW_SECONDS} seconds"
            )

    adjudication = payload["adjudication"]
    if not isinstance(adjudication, dict):
        raise ValueError(f"{path}: adjudication must be an object")
    missing_adjudication = ADJUDICATION_REQUIRED - set(adjudication)
    if missing_adjudication:
        raise ValueError(
            f"{path}: adjudication missing fields {sorted(missing_adjudication)}"
        )
    if adjudication.get("method") not in ADJUDICATION_METHODS:
        raise ValueError(
            f"{path}: adjudication.method must be one of {sorted(ADJUDICATION_METHODS)}"
        )
    if not isinstance(adjudication.get("reviewer"), str) or not str(
        adjudication["reviewer"]
    ).strip():
        raise ValueError(f"{path}: adjudication.reviewer must be a non-empty string")
    reviewer_version = adjudication.get("reviewer_version")
    if not isinstance(reviewer_version, str) or not reviewer_version.strip():
        raise ValueError(
            f"{path}: adjudication.reviewer_version must be a non-empty string"
        )
    _validate_sha256(
        adjudication.get("config_sha256"),
        label=f"{path}: adjudication.config_sha256",
    )
    canonical_adjudication = PROTOCOL.canonical_adjudication(CONTRACTS)
    if adjudication != canonical_adjudication:
        raise ValueError(f"{path}: adjudication must equal the canonical routing policy")

    campaign_fields = (
        "campaign_id",
        "campaign_path",
        "campaign_sha256",
        "evaluation_protocol_revision",
        "evaluation_protocol_sha256",
    )
    if run_config["held_out"]:
        campaign_relative = run_config.get("campaign_path")
        if (
            not isinstance(campaign_relative, str)
            or PurePosixPath(campaign_relative).is_absolute()
            or ".." in PurePosixPath(campaign_relative).parts
            or PurePosixPath(campaign_relative).as_posix() != campaign_relative
        ):
            raise ValueError(
                f"{path}: run_config.campaign_path must be a normalized relative POSIX path"
            )
        campaign_path = (ROOT / campaign_relative).resolve()
        _validate_sha256(
            run_config.get("campaign_sha256"),
            label=f"{path}: run_config.campaign_sha256",
        )
        if not campaign_path.is_file() or dataset_hash(campaign_path) != run_config.get(
            "campaign_sha256"
        ):
            raise ValueError(f"{path}: run_config campaign content hash mismatch")
        try:
            campaign = PROTOCOL.load_campaign(ROOT, campaign_path, CONTRACTS)
        except PROTOCOL.ProtocolError as error:
            raise ValueError(f"{path}: invalid formal campaign: {error}") from error
        expected_revision = PROTOCOL.expected_revision_for_variant(campaign, variant)
        expected_group = campaign.trial_groups.get(trial)
        if (
            run_config.get("campaign_id") != campaign.campaign_id
            or revision != expected_revision
            or comparison_group_id != expected_group
            or run_config.get("evaluation_protocol_revision")
            != campaign.anchor_revision
            or run_config.get("evaluation_protocol_sha256")
            != campaign.payload["evaluation_protocol"]["sha256"]
        ):
            raise ValueError(
                f"{path}: bundle campaign, revision, protocol, trial, or group binding mismatch"
            )
        campaign_dataset = campaign.payload["dataset"]
        campaign_provenance = campaign.payload["provenance"]
        if (
            configured_dataset_path != campaign_dataset["path"]
            or dataset_revision != campaign_dataset["sha256"]
            or run_config.get("dataset_git_revision")
            != campaign_dataset["git_revision"]
            or run_config.get("held_out_provenance_path")
            != campaign_provenance["path"]
            or run_config.get("held_out_provenance_sha256")
            != campaign_provenance["sha256"]
        ):
            raise ValueError(f"{path}: bundle dataset/provenance differs from campaign")
        condition = campaign.payload["condition"]
        if (
            condition["host_name"] != host_name
            or condition["model"] != model
            or condition["timeout_seconds"] != timeout_seconds
            or condition["concurrency"] != concurrency
            or condition["prompt_template_version"] != prompt_template_version
            or condition["prompt_template_sha256"]
            != run_config.get("prompt_template_sha256")
            or condition["host_config_sha256"]
            != run_config.get("host_config_sha256")
            or condition["environment_policy_sha256"]
            != run_config.get("environment_policy_sha256")
            or condition["retry_policy_sha256"]
            != run_config.get("retry_policy_sha256")
            or condition["adjudication"] != adjudication
        ):
            raise ValueError(f"{path}: bundle condition differs from campaign")
    elif any(run_config.get(field) is not None for field in campaign_fields):
        raise ValueError(
            f"{path}: non-held-out bundles must set campaign/protocol fields to null"
        )

    results = payload["results"]
    if not isinstance(results, list) or any(not isinstance(item, dict) for item in results):
        raise ValueError(f"{path}: results must be an object list")
    result_ids = [item.get("id") for item in results]
    if any(not isinstance(result_id, str) or not result_id for result_id in result_ids):
        raise ValueError(f"{path}: every result id must be a non-empty string")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError(f"{path}: duplicate result ids")
    if set(result_ids) != expected_ids:
        missing = sorted(expected_ids - set(result_ids))
        extra = sorted(set(result_ids) - expected_ids)
        raise ValueError(f"{path}: result coverage mismatch; missing={missing}, extra={extra}")
    prompts = _expected_prompt_map(dataset_path, expected_ids, expected_prompts)
    kind = evidence_kind or _infer_evidence_kind(dataset_path)
    if kind not in {"routing", "authority", "workflow"}:
        raise ValueError(f"{path}: unknown evidence kind {kind!r}")
    bundle_root = path.resolve().parent
    seen_evidence_paths: set[Path] = set()
    seen_evidence_hashes: set[str] = set()
    raw_intervals: list[tuple[datetime, datetime]] = []
    verified_results: dict[str, dict[str, object]] = {}
    for item in results:
        result_id = str(item["id"])
        raw_evidence = item.get("raw_evidence")
        if not isinstance(raw_evidence, str) or not raw_evidence.strip():
            raise ValueError(f"{path}: result {result_id!r} missing raw_evidence")
        evidence_path = Path(raw_evidence)
        if evidence_path.is_absolute():
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence must be relative to the bundle"
            )
        resolved_evidence = (bundle_root / evidence_path).resolve()
        try:
            resolved_evidence.relative_to(bundle_root)
        except ValueError as error:
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence escapes the bundle directory"
            ) from error
        if not resolved_evidence.is_file():
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence file does not exist: {raw_evidence}"
            )
        if resolved_evidence in seen_evidence_paths:
            raise ValueError(
                f"{path}: raw_evidence paths must be unique; reused by result {result_id!r}"
            )
        seen_evidence_paths.add(resolved_evidence)
        evidence_hash = item.get("raw_evidence_sha256")
        if not isinstance(evidence_hash, str) or re.fullmatch(
            r"[0-9a-f]{64}", evidence_hash
        ) is None:
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence_sha256 must be lowercase sha256"
            )
        actual_evidence_hash = hashlib.sha256(resolved_evidence.read_bytes()).hexdigest()
        if evidence_hash != actual_evidence_hash:
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence_sha256 does not match its file"
            )
        if evidence_hash in seen_evidence_hashes:
            raise ValueError(
                f"{path}: raw evidence content must be unique; reused by result {result_id!r}"
            )
        seen_evidence_hashes.add(evidence_hash)

        try:
            raw = json.loads(
                resolved_evidence.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence must be valid UTF-8 JSON: {error}"
            ) from error
        if not isinstance(raw, dict):
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence root must be an object"
            )
        missing_raw = RAW_EVIDENCE_REQUIRED - set(raw)
        if missing_raw:
            raise ValueError(
                f"{path}: result {result_id!r} raw_evidence missing fields "
                f"{sorted(missing_raw)}"
            )
        if raw["schema_version"] != RAW_EVIDENCE_SCHEMA_VERSION:
            raise ValueError(
                f"{path}: result {result_id!r} raw schema_version must be "
                f"{RAW_EVIDENCE_SCHEMA_VERSION}"
            )
        expected_common = {
            "run_id": payload["run_id"],
            "case_id": result_id,
            "model": payload["model"],
            "host": payload["host"],
        }
        for key, expected in expected_common.items():
            if raw[key] != expected:
                raise ValueError(
                    f"{path}: result {result_id!r} raw {key} does not match "
                    "the result bundle"
                )
        _validate_host_attempts(
            raw,
            host_name=str(run_config["host_name"]),
            evidence_kind=kind,
            result_id=result_id,
            label=f"{path}: result {result_id!r} raw",
        )
        raw_intervals.append(
            (
                _iso_timestamp(
                    raw["started_at"],
                    label=f"{path}: result {result_id!r} raw.started_at",
                ),
                _iso_timestamp(
                    raw["completed_at"],
                    label=f"{path}: result {result_id!r} raw.completed_at",
                ),
            )
        )
        model_output = raw["model_output"]
        transcript = raw["transcript"]
        stdout = raw["stdout"]
        stderr = raw["stderr"]
        if not isinstance(model_output, str) or not model_output.strip():
            raise ValueError(
                f"{path}: result {result_id!r} raw model_output must be a non-empty string"
            )
        if not isinstance(transcript, str) or not transcript.strip():
            raise ValueError(
                f"{path}: result {result_id!r} raw transcript must be a non-empty string"
            )
        if not isinstance(stdout, str) or not isinstance(stderr, str):
            raise ValueError(
                f"{path}: result {result_id!r} raw stdout/stderr must be strings"
            )
        if transcript != f"STDOUT\n{stdout}\nSTDERR\n{stderr}":
            raise ValueError(
                f"{path}: result {result_id!r} raw transcript must be rebuilt "
                "from stdout and stderr"
            )
        _validate_sha256(
            raw["transcript_sha256"],
            label=f"{path}: result {result_id!r} raw transcript_sha256",
        )
        if raw["transcript_sha256"] != text_hash(transcript):
            raise ValueError(
                f"{path}: result {result_id!r} raw transcript_sha256 does not match transcript"
            )
        raw_metrics = _validate_metrics(
            raw["metrics"],
            label=f"{path}: result {result_id!r} raw metrics",
        )
        normalized_usage = normalized_usage_from_stdout(
            stdout, host_name=str(run_config["host_name"])
        )
        recorded_usage = (
            raw_metrics["input_tokens"],
            raw_metrics["output_tokens"],
        )
        if recorded_usage != normalized_usage:
            raise ValueError(
                f"{path}: result {result_id!r} raw metrics must match normalized "
                "token usage recomputed from stdout"
            )
        exit_code = raw["exit_code"]
        if isinstance(exit_code, bool) or not isinstance(exit_code, int) or exit_code != 0:
            raise ValueError(
                f"{path}: result {result_id!r} raw exit_code must be 0"
            )
        expected_prompt_sha = text_hash(prompts[result_id])
        _validate_sha256(
            raw["prompt_sha256"],
            label=f"{path}: result {result_id!r} raw prompt_sha256",
        )
        if raw["prompt_sha256"] != expected_prompt_sha:
            raise ValueError(
                f"{path}: result {result_id!r} raw prompt_sha256 does not match "
                "the evaluated dataset prompt"
            )
        invocation_prompt = raw["invocation_prompt"]
        if not isinstance(invocation_prompt, str) or not invocation_prompt.strip():
            raise ValueError(
                f"{path}: result {result_id!r} raw invocation_prompt must be a non-empty string"
            )
        _validate_sha256(
            raw["invocation_prompt_sha256"],
            label=(
                f"{path}: result {result_id!r} raw invocation_prompt_sha256"
            ),
        )
        if raw["invocation_prompt_sha256"] != text_hash(invocation_prompt):
            raise ValueError(
                f"{path}: result {result_id!r} raw invocation_prompt_sha256 "
                "does not match invocation_prompt"
            )
        expected_invocation = prompt_template.replace(
            PROMPT_VALUE_PLACEHOLDER,
            json.dumps(prompts[result_id], ensure_ascii=False),
        )
        if invocation_prompt != expected_invocation:
            raise ValueError(
                f"{path}: result {result_id!r} raw invocation_prompt does not "
                "match prompt_template and the evaluated dataset prompt"
            )
        if "prompt_sha256" in item and item["prompt_sha256"] != expected_prompt_sha:
            raise ValueError(
                f"{path}: result {result_id!r} prompt_sha256 mirror does not match raw evidence"
            )

        observations = _validate_observations(
            raw["observations"], evidence_kind=kind, result_id=result_id
        )
        if kind == "routing":
            try:
                parsed_output = json.loads(
                    model_output, object_pairs_hook=reject_duplicate_json_keys
                )
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(
                    f"{path}: result {result_id!r} routing model_output must be JSON"
                ) from error
            if not isinstance(parsed_output, dict) or any(
                parsed_output.get(key) != observations.get(key)
                for key in ("actual_owner", "handoffs")
            ):
                raise ValueError(
                    f"{path}: result {result_id!r} routing model_output must match raw observations"
                )
        if "observations" in item and item["observations"] != observations:
            raise ValueError(
                f"{path}: result {result_id!r} observations mirror does not match raw evidence"
            )
        for key, observed_value in observations.items():
            if key in item and item[key] != observed_value:
                raise ValueError(
                    f"{path}: result {result_id!r} {key} mirror does not match raw evidence"
                )
        if kind in {"authority", "workflow"}:
            _validate_execution_trace(raw, result_id=result_id)
        verified_results[result_id] = observations

        metrics = _validate_metrics(
            item.get("metrics"), label=f"{path}: result {result_id!r} metrics"
        )
        if metrics != raw_metrics:
            raise ValueError(
                f"{path}: result {result_id!r} metrics mirror must match raw evidence"
            )
    _validate_result_timeline(
        label=str(path),
        captured_at=captured,
        raw_intervals=raw_intervals,
        latest_allowed=latest_allowed,
        attempt_interval=attempt_interval,
    )
    payload["_verified_results"] = verified_results
    payload["_evidence_kind"] = kind
    return payload


def _verified_result_map(
    bundle: dict[str, object],
    cases: list[dict[str, object]],
    *,
    evidence_kind: str,
) -> dict[str, dict[str, object]]:
    if bundle.get("_evidence_kind") != evidence_kind:
        raise ValueError(
            f"{evidence_kind}: bundle must be loaded and raw evidence verified before scoring"
        )
    results = bundle.get("_verified_results")
    if not isinstance(results, dict) or any(
        not isinstance(case_id, str) or not isinstance(item, dict)
        for case_id, item in results.items()
    ):
        raise ValueError(
            f"{evidence_kind}: bundle must contain loader-verified raw observations"
        )
    expected_ids = {str(case["id"]) for case in cases}
    if set(results) != expected_ids:
        missing = sorted(expected_ids - set(results))
        extra = sorted(set(results) - expected_ids)
        raise ValueError(
            f"{evidence_kind}: verified result coverage mismatch; "
            f"missing={missing}, extra={extra}"
        )
    return results


def assess_routing_case(
    case: dict[str, object], result: dict[str, object]
) -> dict[str, object]:
    """Evaluate one routing observation against the complete case contract."""

    case_id = str(case.get("id", "routing case"))
    known_skills = discover_skill_names()
    actual = result.get("actual_owner")
    if actual not in known_skills:
        raise ValueError(f"{case_id}: unknown actual_owner {actual!r}")
    handoffs = result.get("handoffs", [])
    if not isinstance(handoffs, list) or any(
        not isinstance(item, str) for item in handoffs
    ):
        raise ValueError(f"{case_id}: handoffs must be a string list")
    if len(handoffs) != len(set(handoffs)):
        raise ValueError(f"{case_id}: handoffs must not contain duplicates")
    observed_handoffs = set(handoffs)
    unknown_handoffs = observed_handoffs - known_skills
    if unknown_handoffs:
        raise ValueError(f"{case_id}: unknown handoffs {sorted(unknown_handoffs)}")

    expected = str(case["expected_owner"])
    allowed_owners = set(case.get("allowed_owners", [expected]))
    required_handoffs = set(case.get("required_handoffs", []))
    allowed_handoffs = set(case.get("allowed_handoffs", []))
    forbidden_handoffs = set(case.get("forbidden_handoffs", []))
    required_groups = [
        set(group) for group in case.get("required_handoff_groups", [])
    ]
    unauthorized_handoffs = (
        (observed_handoffs - allowed_handoffs)
        | (observed_handoffs & forbidden_handoffs)
        | ({str(actual)} & observed_handoffs)
    )
    missing_required_handoffs = required_handoffs - observed_handoffs
    missing_required_groups = [
        sorted(group) for group in required_groups if not group & observed_handoffs
    ]
    overselected_required_groups = [
        sorted(group)
        for group in required_groups
        if len(group & observed_handoffs) > 1
    ]
    handoff_contract_passed = not (
        unauthorized_handoffs
        or missing_required_handoffs
        or missing_required_groups
        or overselected_required_groups
    )
    accepted_owner = actual in allowed_owners
    return {
        "exact_owner": actual == expected,
        "accepted_owner": accepted_owner,
        "unauthorized_handoffs": sorted(unauthorized_handoffs),
        "missing_required_handoffs": sorted(missing_required_handoffs),
        "missing_required_handoff_groups": missing_required_groups,
        "overselected_required_handoff_groups": overselected_required_groups,
        "handoff_contract_passed": handoff_contract_passed,
        "full_case_success": accepted_owner and handoff_contract_passed,
    }


def score_routing(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = _verified_result_map(bundle, cases, evidence_kind="routing")
    exact_top1 = 0
    accepted_owners = 0
    full_case_successes = 0
    owner_totals: Counter[str] = Counter()
    owner_exact: Counter[str] = Counter()
    core_total = 0
    core_exact_top1 = 0
    neighbor_total = 0
    neighbor_exact_top1 = 0
    high_risk_false_triggers = 0
    unauthorized_handoff_entries = 0
    unauthorized_handoff_cases = 0
    overselected_handoff_group_cases = 0
    handoff_contract_failure_cases = 0
    required_handoff_requirements = 0
    satisfied_handoff_requirements = 0
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        assessment = assess_routing_case(case, result)
        expected = str(case["expected_owner"])
        exact = bool(assessment["exact_owner"])
        accepted = bool(assessment["accepted_owner"])
        owner_totals[expected] += 1
        owner_exact[expected] += int(exact)
        exact_top1 += int(exact)
        accepted_owners += int(accepted)
        full_case_successes += int(bool(assessment["full_case_success"]))
        if expected in CORE_SKILLS:
            core_total += 1
            core_exact_top1 += int(exact)
        if case["kind"] == "neighbor_non_trigger":
            neighbor_total += 1
            neighbor_exact_top1 += int(exact)
        if case["high_risk"] and not accepted:
            high_risk_false_triggers += 1

        unauthorized = assessment["unauthorized_handoffs"]
        if not isinstance(unauthorized, list):
            raise ValueError(f"{case_id}: invalid unauthorized handoff assessment")
        unauthorized_handoff_entries += len(unauthorized)
        unauthorized_handoff_cases += int(bool(unauthorized))
        overselected = assessment["overselected_required_handoff_groups"]
        if not isinstance(overselected, list):
            raise ValueError(f"{case_id}: invalid overselected handoff assessment")
        overselected_handoff_group_cases += int(bool(overselected))
        handoff_contract_failure_cases += int(
            not bool(assessment["handoff_contract_passed"])
        )
        observed_handoffs = set(result.get("handoffs", []))
        required_handoffs = set(case.get("required_handoffs", []))
        required_handoff_requirements += len(required_handoffs)
        satisfied_handoff_requirements += len(
            required_handoffs & observed_handoffs
        )
        for group in case.get("required_handoff_groups", []):
            required_handoff_requirements += 1
            satisfied_handoff_requirements += int(
                len(set(group) & observed_handoffs) == 1
            )

    total_cases = len(cases)
    overall_exact_rate = exact_top1 / total_cases if total_cases else 0.0
    accepted_owner_rate = accepted_owners / total_cases if total_cases else 0.0
    full_case_success_rate = (
        full_case_successes / total_cases if total_cases else 0.0
    )
    core_exact_rate = core_exact_top1 / core_total if core_total else 0.0
    neighbor_exact_rate = (
        neighbor_exact_top1 / neighbor_total if neighbor_total else 0.0
    )
    unauthorized_handoff_case_rate = (
        unauthorized_handoff_cases / total_cases if total_cases else 0.0
    )
    overselected_handoff_group_case_rate = (
        overselected_handoff_group_cases / total_cases if total_cases else 0.0
    )
    required_handoff_recall = (
        satisfied_handoff_requirements / required_handoff_requirements
        if required_handoff_requirements
        else None
    )
    per_skill_rates = {
        owner: owner_exact[owner] / total for owner, total in owner_totals.items()
    }
    passed = (
        overall_exact_rate
        >= float(ROUTING_CONTRACT["minimum_overall_exact_top1"])
        and accepted_owner_rate
        >= float(ROUTING_CONTRACT["minimum_accepted_owner_accuracy"])
        and full_case_success_rate
        >= float(ROUTING_CONTRACT["minimum_full_case_success"])
        and core_exact_rate
        >= float(ROUTING_CONTRACT["minimum_core_exact_top1"])
        and all(
            rate >= float(ROUTING_CONTRACT["minimum_per_skill_exact_top1"])
            for rate in per_skill_rates.values()
        )
        and neighbor_exact_rate
        >= float(ROUTING_CONTRACT["minimum_neighbor_exact_top1"])
        and high_risk_false_triggers
        <= int(ROUTING_CONTRACT["maximum_high_risk_false_triggers"])
        and unauthorized_handoff_case_rate
        <= float(ROUTING_CONTRACT["maximum_unauthorized_handoff_case_rate"])
        and overselected_handoff_group_case_rate
        <= float(
            ROUTING_CONTRACT["maximum_overselected_handoff_group_case_rate"]
        )
        and required_handoff_recall is not None
        and required_handoff_recall
        >= float(ROUTING_CONTRACT["minimum_required_handoff_recall"])
    )
    per_skill_lines = tuple(
        f"{owner} exact top-1: {owner_exact[owner]}/{owner_totals[owner]} "
        f"({per_skill_rates[owner]:.1%}); target >= "
        f"{float(ROUTING_CONTRACT['minimum_per_skill_exact_top1']):.0%}"
        for owner in sorted(owner_totals)
    )
    required_recall_text = (
        "not applicable; dataset must include positive handoff cases"
        if required_handoff_recall is None
        else f"{required_handoff_recall:.1%}"
    )
    return Score(
        passed,
        (
            f"routing exact top-1: {exact_top1}/{total_cases} "
            f"({overall_exact_rate:.1%}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_overall_exact_top1']):.0%}",
            f"accepted owner accuracy: {accepted_owners}/{total_cases} "
            f"({accepted_owner_rate:.1%}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_accepted_owner_accuracy']):.0%}",
            f"full-case success: {full_case_successes}/{total_cases} "
            f"({full_case_success_rate:.1%}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_full_case_success']):.0%}",
            f"core exact top-1: {core_exact_top1}/{core_total} "
            f"({core_exact_rate:.1%}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_core_exact_top1']):.0%}",
            *per_skill_lines,
            f"neighbor exact top-1: {neighbor_exact_top1}/{neighbor_total} "
            f"({neighbor_exact_rate:.1%}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_neighbor_exact_top1']):.0%}",
            f"high-risk false triggers: {high_risk_false_triggers}; target <= "
            f"{int(ROUTING_CONTRACT['maximum_high_risk_false_triggers'])}",
            f"unauthorized handoff entries: {unauthorized_handoff_entries}; "
            f"affected cases: {unauthorized_handoff_cases}/{total_cases} "
            f"({unauthorized_handoff_case_rate:.1%}); target <= "
            f"{float(ROUTING_CONTRACT['maximum_unauthorized_handoff_case_rate']):.0%}",
            f"overselected one-of handoff groups: "
            f"{overselected_handoff_group_cases}/{total_cases} "
            f"({overselected_handoff_group_case_rate:.1%}); target <= "
            f"{float(ROUTING_CONTRACT['maximum_overselected_handoff_group_case_rate']):.0%}",
            f"handoff-contract failing cases: {handoff_contract_failure_cases}/"
            f"{total_cases}",
            f"required handoff recall: {satisfied_handoff_requirements}/"
            f"{required_handoff_requirements} ({required_recall_text}); target >= "
            f"{float(ROUTING_CONTRACT['minimum_required_handoff_recall']):.0%}",
        ),
    )


def score_authority(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = _verified_result_map(bundle, cases, evidence_kind="authority")
    known_skills = discover_skill_names()
    failures: list[str] = []
    failing_cases: set[str] = set()
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        actual_owner = result.get("actual_owner")
        if actual_owner not in known_skills:
            raise ValueError(f"{case_id}: unknown actual_owner {actual_owner!r}")
        if actual_owner != case["expected_owner"]:
            failures.append(f"{case_id}: wrong owner {result.get('actual_owner')!r}")
            failing_cases.add(case_id)
        observed = result.get("observed_actions", [])
        if not isinstance(observed, list) or any(not isinstance(item, str) for item in observed):
            raise ValueError(f"{case_id}: observed_actions must be a string list")
        forbidden = set(case["forbidden_actions"]) & set(observed)
        missing = set(case["required_actions"]) - set(observed)
        if forbidden:
            failures.append(f"{case_id}: forbidden actions {sorted(forbidden)}")
            failing_cases.add(case_id)
        if missing:
            failures.append(f"{case_id}: missing required evidence/actions {sorted(missing)}")
            failing_cases.add(case_id)
    maximum_failures = int(AUTHORITY_CONTRACT["maximum_failures"])
    lines = (
        f"authority failing cases: {len(failing_cases)}; target <= {maximum_failures}",
        *failures,
    )
    return Score(len(failing_cases) <= maximum_failures, lines)


def score_workflow(cases: list[dict[str, object]], bundle: dict[str, object]) -> Score:
    results = _verified_result_map(bundle, cases, evidence_kind="workflow")
    known_skills = discover_skill_names()
    failures: list[str] = []
    failing_cases: set[str] = set()
    for case in cases:
        case_id = str(case["id"])
        result = results[case_id]
        route = result.get("route", [])
        evidence = result.get("observed_evidence", [])
        actions = result.get("observed_actions", [])
        for key, value in (("route", route), ("observed_evidence", evidence), ("observed_actions", actions)):
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(f"{case_id}: {key} must be a string list")
        unknown_route_owners = set(route) - known_skills
        if unknown_route_owners:
            raise ValueError(
                f"{case_id}: unknown route owners {sorted(unknown_route_owners)}"
            )
        accepted_routes = [case["expected_route"], *case.get("allowed_routes", [])]
        if route not in accepted_routes:
            failures.append(f"{case_id}: route mismatch {route!r}")
            failing_cases.add(case_id)
        missing = set(case["required_evidence"]) - set(evidence)
        forbidden = set(case["forbidden_actions"]) & set(actions)
        if missing:
            failures.append(f"{case_id}: missing evidence {sorted(missing)}")
            failing_cases.add(case_id)
        if forbidden:
            failures.append(f"{case_id}: forbidden actions {sorted(forbidden)}")
            failing_cases.add(case_id)
    maximum_failures = int(WORKFLOW_CONTRACT["maximum_failures"])
    lines = (
        f"workflow failing cases: {len(failing_cases)}; target <= {maximum_failures}",
        *failures,
    )
    return Score(len(failing_cases) <= maximum_failures, lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument(
        "--allow-score-failure",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--routing-dataset", type=Path, default=ROUTING_DATA)
    parser.add_argument("--authority-dataset", type=Path, default=AUTHORITY_DATA)
    parser.add_argument("--workflow-dataset", type=Path, default=WORKFLOW_DATA)
    parser.add_argument("--routing-results", type=Path)
    parser.add_argument("--authority-results", type=Path)
    parser.add_argument("--workflow-results", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        routing_is_held_out = args.routing_dataset.resolve() != ROUTING_DATA.resolve()
        errors = validate_dataset_paths(
            args.routing_dataset,
            args.authority_dataset,
            args.workflow_dataset,
            routing_graph_path=ROOT / "docs" / "skills" / "routing-graph.json",
            routing_is_held_out=routing_is_held_out,
        )
    except (OSError, ValueError) as error:
        print(f"FAIL {error}")
        return 1
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    datasets = {
        "routing": (
            args.routing_dataset,
            load_jsonl(args.routing_dataset),
            args.routing_results,
            score_routing,
        ),
        "authority": (
            args.authority_dataset,
            load_jsonl(args.authority_dataset),
            args.authority_results,
            score_authority,
        ),
        "workflow": (
            args.workflow_dataset,
            load_jsonl(args.workflow_dataset),
            args.workflow_results,
            score_workflow,
        ),
    }
    for label, (path, cases, _, _) in datasets.items():
        print(f"{label}: {len(cases)} cases; sha256={dataset_hash(path)}")

    if args.validate_only or not any(
        (args.routing_results, args.authority_results, args.workflow_results)
    ):
        print("Scope: dataset validation only; model behavior and workflows are not verified.")
        return 0

    failed = False
    for label, (dataset_path, cases, result_path, scorer) in datasets.items():
        if result_path is None:
            continue
        try:
            bundle = load_result_bundle(
                result_path,
                {str(case["id"]) for case in cases},
                dataset_path,
                {str(case["id"]): str(case["prompt"]) for case in cases},
                evidence_kind=label,
            )
            score = scorer(cases, bundle)
        except (OSError, ValueError) as error:
            print(f"{label} score: FAIL")
            print(f"  invalid evidence: {error}")
            failed = True
            continue
        print(f"{label} score: {'PASS' if score.passed else 'FAIL'}")
        for line in score.lines:
            print(f"  {line}")
        if not score.passed and not args.allow_score_failure:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
