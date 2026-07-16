#!/usr/bin/env python3
"""Validate repository skill packages."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


LEGACY_SKILL_NAMES = (
    "repo-context",
    "code-context",
    "code-review",
    "code-delivery",
    "code-security",
    "commit-reviewer",
    "planner",
    "frontend-implementation",
    "frontend-governance",
    "rust-engineering-governance",
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
LEGACY_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(name) for name in LEGACY_SKILL_NAMES) + r")(?![A-Za-z0-9_-])"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_INVOCATION_RE = re.compile(r"(?<![A-Za-z0-9_.])\$([a-z][a-z0-9-]*)")
EVAL_CASES_FILE = "eval-cases.md"
ROUTING_GRAPH_FILE = "docs/skills/routing-graph.json"
QUALITY_STATUS_FILE = "docs/quality/status.md"
QUALITY_EVIDENCE_FILE = "docs/quality/evidence-manifest.json"
VALIDATION_CONTRACT_FILE = "contracts/skill-validation.json"
EVAL_REQUIRED_SECTIONS = (
    "## Trigger Eval",
    "## Non-Trigger Eval",
    "## Quality Eval",
    "## Scoring",
)
FORBIDDEN_DESCRIPTION_PHRASES = ("Triggers include",)
MIN_TRIGGER_CASES = 3
MIN_NON_TRIGGER_CASES = 3
MIN_QUALITY_CASES = 4
QUALITY_CATEGORIES = {
    "Core Engineering",
    "Implementation",
    "Specialist Audit",
    "Runtime Operations",
    "External Review",
    "Writing Extension",
}
RELEASE_STATES = {"available", "hidden", "removed"}
VALIDATION_STATES = {"verified", "not_verified"}
REQUIRED_SKILL_SECTIONS = (
    "## Overview",
    "## Do Not Use For",
    "## Hard Rules",
    "## Output Contract",
    "## References",
)
PLACEHOLDER_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:TODO|TBD|FIXME|PLACEHOLDER)(?:\s*:|\s*$)",
    re.MULTILINE,
)
TEXT_FILE_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".sh", ".json", ".toml", ".txt"}
ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "scripts" / "evaluation_protocol.py"
_PROTOCOL_SPEC = importlib.util.spec_from_file_location(
    "aicraft_evaluation_protocol_for_validator", PROTOCOL_PATH
)
if _PROTOCOL_SPEC is None or _PROTOCOL_SPEC.loader is None:
    raise RuntimeError(f"cannot load evaluation protocol from {PROTOCOL_PATH}")
PROTOCOL = importlib.util.module_from_spec(_PROTOCOL_SPEC)
sys.modules[_PROTOCOL_SPEC.name] = PROTOCOL
_PROTOCOL_SPEC.loader.exec_module(PROTOCOL)


def load_validation_contracts() -> dict[str, object]:
    path = Path(__file__).resolve().parents[1] / VALIDATION_CONTRACT_FILE
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle, object_pairs_hook=_reject_contract_duplicate_keys)
    if not isinstance(payload, dict):
        raise ValueError(f"{VALIDATION_CONTRACT_FILE} must contain an object")
    return payload


def _reject_contract_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


VALIDATION_CONTRACTS = load_validation_contracts()
AUDIT_RUST_CONTRACT = VALIDATION_CONTRACTS["specialized_evals"]["audit-rust"]
PACKAGE_POLICY = VALIDATION_CONTRACTS["package_policy"]
QUALITY_EVIDENCE_SCHEMA_VERSION = int(
    VALIDATION_CONTRACTS["behavior_eval"][
        "quality_evidence_manifest_schema_version"
    ]
)
CLAIMABLE_COMPARISON_KINDS = set(
    VALIDATION_CONTRACTS["behavior_eval"]["claimable_comparison_kinds"]
)
MAX_DESCRIPTION_CHARS = int(PACKAGE_POLICY["maximum_description_characters"])
MAX_SKILL_LINES = int(PACKAGE_POLICY["maximum_skill_lines"])
MIN_SHORT_DESCRIPTION_CHARS = int(
    PACKAGE_POLICY["short_description_characters"]["minimum"]
)
MAX_SHORT_DESCRIPTION_CHARS = int(
    PACKAGE_POLICY["short_description_characters"]["maximum"]
)
MAX_DEFAULT_PROMPT_CHARS = int(PACKAGE_POLICY["maximum_default_prompt_characters"])
REFERENCE_TOC_AFTER_LINES = int(PACKAGE_POLICY["reference_toc_after_lines"])
REFERENCE_TOC_EXEMPTIONS = set(PACKAGE_POLICY["reference_toc_exemptions"])


def validate_official_baseline(
    contracts: dict[str, object], *, today: date | None = None
) -> list[str]:
    """Require a dated, provider-complete official standards baseline."""

    errors: list[str] = []
    baseline = contracts.get("official_baseline")
    if not isinstance(baseline, dict):
        return ["repository: official_baseline must be an object"]

    parsed_dates: dict[str, date] = {}
    for key in ("reviewed_at", "review_due"):
        raw = baseline.get(key)
        if not isinstance(raw, str):
            errors.append(f"repository: official_baseline.{key} must be an ISO date")
            continue
        try:
            parsed_dates[key] = date.fromisoformat(raw)
        except ValueError:
            errors.append(f"repository: official_baseline.{key} must be an ISO date")

    reviewed_at = parsed_dates.get("reviewed_at")
    review_due = parsed_dates.get("review_due")
    if reviewed_at and review_due:
        current = today or date.today()
        if reviewed_at > current:
            errors.append(
                "repository: official_baseline.reviewed_at cannot be in the future"
            )
        if review_due < reviewed_at:
            errors.append("repository: official_baseline.review_due precedes reviewed_at")
        maximum_age = baseline.get("maximum_review_age_days")
        if isinstance(maximum_age, bool) or not isinstance(maximum_age, int) or maximum_age < 1:
            errors.append(
                "repository: official_baseline.maximum_review_age_days must be a positive integer"
            )
        elif (review_due - reviewed_at).days > maximum_age:
            errors.append(
                "repository: official_baseline review window exceeds maximum_review_age_days"
            )
        if current > review_due:
            errors.append(
                f"repository: official skill baseline review expired on {review_due.isoformat()}"
            )

    sources = baseline.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("repository: official_baseline.sources must be a non-empty object list")
        return errors
    observed_lanes: set[str] = set()
    for index, source in enumerate(sources, 1):
        if not isinstance(source, dict):
            errors.append(f"repository: official_baseline source {index} must be an object")
            continue
        lane = source.get("lane")
        if not isinstance(lane, str) or not lane:
            errors.append(f"repository: official_baseline source {index} missing lane")
        else:
            observed_lanes.add(lane)
        for key in ("provider", "url", "revision"):
            value = source.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"repository: official_baseline source {index} missing {key}"
                )
        url = source.get("url")
        if isinstance(url, str) and not url.startswith("https://"):
            errors.append(
                f"repository: official_baseline source {index} url must use https"
            )
    required_lanes = {"portable-core", "openai", "claude", "evaluation"}
    missing_lanes = required_lanes - observed_lanes
    if missing_lanes:
        errors.append(
            f"repository: official_baseline missing provider lanes {sorted(missing_lanes)}"
        )
    return errors


@dataclass(frozen=True)
class SkillPackage:
    name: str
    path: Path


@dataclass(frozen=True)
class QualityMetrics:
    description_chars: int
    skill_lines: int
    trigger_cases: int
    non_trigger_cases: int
    quality_cases: int


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate repository skill packages.")
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="validate only this skill name; may be provided multiple times",
    )
    parser.add_argument(
        "--quality-report",
        action="store_true",
        help="print description, entrypoint, and eval coverage metrics",
    )
    return parser.parse_args()


def discover_skills(skills_dir: Path) -> list[SkillPackage]:
    packages = []
    if not skills_dir.exists():
        return packages

    for child in sorted(skills_dir.iterdir(), key=lambda item: item.name):
        if child.is_dir() and (child / "SKILL.md").is_file():
            packages.append(SkillPackage(name=child.name, path=child))
    return packages


def validate_repository_indexes(root: Path, packages: list[SkillPackage]) -> list[str]:
    errors: list[str] = []
    expected = {package.name for package in packages}

    skills_index = root / "skills.sh.json"
    try:
        payload = json.loads(skills_index.read_text(encoding="utf-8"))
        indexed_names = [
            name
            for grouping in payload.get("groupings", [])
            for name in grouping.get("skills", [])
        ]
    except (OSError, json.JSONDecodeError, AttributeError) as error:
        errors.append(f"repository: cannot read skills.sh.json: {error}")
    else:
        if len(indexed_names) != len(set(indexed_names)):
            errors.append("repository: skills.sh.json contains duplicate skill names")
        indexed = set(indexed_names)
        for name in sorted(expected - indexed):
            errors.append(f"repository: skills.sh.json missing skill {name}")
        for name in sorted(indexed - expected):
            errors.append(f"repository: skills.sh.json lists unknown skill {name}")

    index_specs = (
        (root / "README.md", re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)),
        (root / "INSTALL.md", re.compile(r"^- `skills/([a-z0-9-]+)`$", re.MULTILINE)),
    )
    for path, pattern in index_specs:
        try:
            listed = set(pattern.findall(path.read_text(encoding="utf-8")))
        except OSError as error:
            errors.append(f"repository: cannot read {path.name}: {error}")
            continue
        for name in sorted(expected - listed):
            errors.append(f"repository: {path.name} missing skill {name}")
        for name in sorted(listed - expected):
            errors.append(f"repository: {path.name} lists unknown skill {name}")

    return errors


def validate_quality_evidence(
    root: Path,
) -> tuple[list[str], dict[tuple[str, str], set[int]]]:
    """Validate immutable, executable behavior/workflow evidence records."""

    errors: list[str] = []
    trials: dict[tuple[str, str], set[int]] = {}
    manifest_path = root / QUALITY_EVIDENCE_FILE
    if not manifest_path.is_file():
        return errors, trials
    try:
        payload = json.loads(
            manifest_path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [f"repository: cannot read {QUALITY_EVIDENCE_FILE}: {error}"], trials
    if not isinstance(payload, dict):
        return [f"repository: {QUALITY_EVIDENCE_FILE} must contain an object"], trials
    manifest_fields = {"schema_version", "claims", "evidence", "comparisons"}
    if set(payload) != manifest_fields:
        errors.append(
            f"repository: {QUALITY_EVIDENCE_FILE} top-level fields must be "
            f"{sorted(manifest_fields)}"
        )
    if payload.get("schema_version") != QUALITY_EVIDENCE_SCHEMA_VERSION:
        errors.append(
            f"repository: {QUALITY_EVIDENCE_FILE} schema_version must be "
            f"{QUALITY_EVIDENCE_SCHEMA_VERSION}"
        )
    claims = payload.get("claims")
    if not isinstance(claims, list) or any(
        not isinstance(item, dict) for item in claims
    ):
        errors.append(
            f"repository: {QUALITY_EVIDENCE_FILE} claims must be an object list"
        )
        claims = []
    records = payload.get("evidence")
    if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
        errors.append(f"repository: {QUALITY_EVIDENCE_FILE} evidence must be an object list")
        return errors, trials
    comparisons = payload.get("comparisons")
    if not isinstance(comparisons, list) or any(
        not isinstance(item, dict) for item in comparisons
    ):
        errors.append(
            f"repository: {QUALITY_EVIDENCE_FILE} comparisons must be an object list"
        )
        comparisons = []

    evaluator = root / "scripts" / "eval-skill-contracts.py"
    known_kinds = {"routing", "authority", "workflow"}
    observed_ids: set[str] = set()
    observed_trials: set[tuple[str, str, int]] = set()
    observed_run_ids: set[str] = set()
    observed_bundle_paths: set[Path] = set()
    observed_bundle_hashes: set[str] = set()
    observed_raw_paths: set[Path] = set()
    observed_raw_hashes: set[str] = set()
    valid_evidence: dict[str, dict[str, object]] = {}
    root_resolved = root.resolve()
    evidence_fields = {
        "id",
        "kind",
        "dataset",
        "dataset_sha256",
        "campaign",
        "campaign_sha256",
        "bundle",
        "bundle_sha256",
    }
    for index, record in enumerate(records, 1):
        evidence_id = record.get("id")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {index} missing id"
            )
            continue
        if evidence_id in observed_ids:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} duplicates evidence id {evidence_id}"
            )
            continue
        observed_ids.add(evidence_id)
        if set(record) != evidence_fields:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} "
                f"fields must be {sorted(evidence_fields)}"
            )
            continue

        kind = record.get("kind")
        if kind not in known_kinds:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} has unknown kind {kind!r}"
            )
            continue
        dataset = record.get("dataset")
        if (
            not isinstance(dataset, str)
            or not dataset.strip()
            or Path(dataset).is_absolute()
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} dataset must be a relative path"
            )
            continue
        dataset_path = (root / dataset).resolve()
        try:
            dataset_path.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} dataset escapes repository"
            )
            continue
        if not dataset_path.is_file():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} dataset does not exist"
            )
            continue
        expected_dataset_hash = record.get("dataset_sha256")
        actual_dataset_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        if (
            not isinstance(expected_dataset_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_dataset_hash) is None
            or expected_dataset_hash != actual_dataset_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} dataset hash mismatch"
            )
            continue
        campaign = record.get("campaign")
        if (
            not isinstance(campaign, str)
            or not campaign.strip()
            or Path(campaign).is_absolute()
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} campaign must be a relative path"
            )
            continue
        campaign_path = (root / campaign).resolve()
        try:
            campaign_path.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} campaign escapes repository"
            )
            continue
        expected_campaign_hash = record.get("campaign_sha256")
        if (
            not campaign_path.is_file()
            or not isinstance(expected_campaign_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_campaign_hash) is None
            or hashlib.sha256(campaign_path.read_bytes()).hexdigest()
            != expected_campaign_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} campaign hash mismatch"
            )
            continue
        bundle = record.get("bundle")
        if not isinstance(bundle, str) or not bundle.strip() or Path(bundle).is_absolute():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} bundle must be a relative path"
            )
            continue
        bundle_path = (root / bundle).resolve()
        try:
            bundle_path.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} bundle escapes repository"
            )
            continue
        if not bundle_path.is_file():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} bundle does not exist"
            )
            continue
        if bundle_path in observed_bundle_paths:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} reuses bundle path {bundle}"
            )
            continue
        expected_hash = record.get("bundle_sha256")
        actual_hash = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
        if (
            not isinstance(expected_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None
            or expected_hash != actual_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} bundle hash mismatch"
            )
            continue
        if actual_hash in observed_bundle_hashes:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} replays an existing bundle hash"
            )
            continue
        observed_bundle_paths.add(bundle_path)
        observed_bundle_hashes.add(actual_hash)
        try:
            bundle_payload = json.loads(
                bundle_path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
            run_config = bundle_payload["run_config"]
            variant = run_config["variant"]
            trial = run_config["trial"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} cannot read run_config: {error}"
            )
            continue
        if (
            run_config.get("campaign_path") != campaign
            or run_config.get("campaign_sha256") != expected_campaign_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} bundle campaign binding mismatch"
            )
            continue
        if variant not in {"candidate", "baseline", "previous"} or (
            isinstance(trial, bool) or not isinstance(trial, int) or trial < 1
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} has invalid variant/trial"
            )
            continue
        run_id = bundle_payload.get("run_id")
        if not isinstance(run_id, str) or not run_id.strip():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} missing run_id"
            )
            continue
        if run_id in observed_run_ids:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} duplicates run_id {run_id}"
            )
            continue
        observed_run_ids.add(run_id)

        skill_revision = bundle_payload.get("skill_revision")
        if not isinstance(skill_revision, str) or re.fullmatch(
            r"[0-9a-f]{40}", skill_revision
        ) is None:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} has invalid skill_revision"
            )
            continue
        if variant == "candidate":
            skill_diff = subprocess.run(
                ["git", "diff", "--quiet", skill_revision, "--", "skills"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
            if skill_diff.returncode != 0:
                detail = (skill_diff.stderr or skill_diff.stdout).strip()
                suffix = f": {detail}" if detail else ""
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} skill_revision "
                    f"does not match the current skills tree{suffix}"
                )
                continue
            untracked_skills = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard", "--", "skills"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
            if untracked_skills.returncode != 0 or untracked_skills.stdout.strip():
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} cannot bind to a skills tree with untracked files"
                )
                continue
        skill_tree_sha = bundle_payload.get("skill_tree_sha")
        if not isinstance(skill_tree_sha, str) or re.fullmatch(
            r"[0-9a-f]{40}", skill_tree_sha
        ) is None:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} has invalid skill_tree_sha"
            )
            continue
        revision_tree = subprocess.run(
            ["git", "rev-parse", f"{skill_revision}:skills"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if (
            revision_tree.returncode != 0
            or revision_tree.stdout.strip() != skill_tree_sha
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} skill_tree_sha "
                "does not match skill_revision"
            )
            continue

        results = bundle_payload.get("results")
        if not isinstance(results, list) or any(
            not isinstance(item, dict) for item in results
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} results must be an object list"
            )
            continue
        raw_replay = False
        bundle_root = bundle_path.parent.resolve()
        for result in results:
            raw_evidence = result.get("raw_evidence")
            raw_hash = result.get("raw_evidence_sha256")
            if (
                not isinstance(raw_evidence, str)
                or not raw_evidence.strip()
                or Path(raw_evidence).is_absolute()
                or not isinstance(raw_hash, str)
                or re.fullmatch(r"[0-9a-f]{64}", raw_hash) is None
            ):
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} has invalid raw evidence metadata"
                )
                raw_replay = True
                break
            raw_path = (bundle_root / raw_evidence).resolve()
            try:
                raw_path.relative_to(bundle_root)
            except ValueError:
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} raw evidence escapes its bundle"
                )
                raw_replay = True
                break
            if not raw_path.is_file() or hashlib.sha256(raw_path.read_bytes()).hexdigest() != raw_hash:
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} raw evidence hash mismatch"
                )
                raw_replay = True
                break
            if raw_path in observed_raw_paths or raw_hash in observed_raw_hashes:
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} replays raw evidence"
                )
                raw_replay = True
                break
            observed_raw_paths.add(raw_path)
            observed_raw_hashes.add(raw_hash)
        if raw_replay:
            continue
        trial_key = (str(kind), str(variant), trial)
        if trial_key in observed_trials:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} duplicates {kind}/{variant} trial {trial}"
            )
            continue

        evaluator_command = [
            sys.executable,
            str(evaluator),
            f"--{kind}-dataset",
            str(dataset_path),
            f"--{kind}-results",
            str(bundle_path),
        ]
        if variant != "candidate":
            evaluator_command.append("--allow-score-failure")
        completed = subprocess.run(
            evaluator_command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} evidence {evidence_id} did not pass evidence validation{suffix}"
            )
            continue
        observed_trials.add(trial_key)
        trials.setdefault((str(kind), str(variant)), set()).add(trial)
        valid_evidence[evidence_id] = {
            "kind": str(kind),
            "variant": str(variant),
            "trial": trial,
            "model": bundle_payload.get("model"),
            "host": bundle_payload.get("host"),
            "host_name": run_config.get("host_name"),
            "skill_revision": skill_revision,
            "dataset_git_revision": run_config.get("dataset_git_revision"),
            "evaluation_anchor_revision": run_config.get(
                "evaluation_anchor_revision"
            ),
            "campaign_id": run_config.get("campaign_id"),
            "campaign_path": run_config.get("campaign_path"),
            "campaign_sha256": run_config.get("campaign_sha256"),
            "evaluation_protocol_revision": run_config.get(
                "evaluation_protocol_revision"
            ),
            "evaluation_protocol_sha256": run_config.get(
                "evaluation_protocol_sha256"
            ),
            "held_out_provenance_path": run_config.get(
                "held_out_provenance_path"
            ),
            "held_out_provenance_sha256": run_config.get(
                "held_out_provenance_sha256"
            ),
            "bundle_path": bundle_path,
            "bundle_sha256": actual_hash,
            "dataset_path": dataset_path,
            "dataset_sha256": actual_dataset_hash,
        }

    comparison_errors, passing_comparisons = validate_quality_comparisons(
        root, comparisons, valid_evidence
    )
    errors.extend(comparison_errors)
    claim_fields = {
        "id",
        "status",
        "comparison_id",
        "dimension",
        "kind",
        "host_name",
        "host_version",
        "model",
        "candidate_skill_revision",
        "previous_skill_revision",
        "baseline_skill_revision",
        "dataset_sha256",
        "dataset_git_revision",
        "evaluation_anchor_revision",
        "campaign_id",
        "campaign_path",
        "campaign_sha256",
        "evaluation_protocol_revision",
        "evaluation_protocol_sha256",
        "held_out_provenance_path",
        "held_out_provenance_sha256",
        "skills",
    }
    observed_claim_ids: set[str] = set()
    for index, claim in enumerate(claims, 1):
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {index} missing id"
            )
            continue
        if claim_id in observed_claim_ids:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} duplicates claim id {claim_id}"
            )
            continue
        observed_claim_ids.add(claim_id)
        if set(claim) != claim_fields:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} fields must be "
                f"{sorted(claim_fields)}"
            )
            continue
        if claim.get("status") != "verified":
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} status must be verified; "
                "omit unverified claims"
            )
            continue
        comparison_id = claim.get("comparison_id")
        if comparison_id not in passing_comparisons:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} requires its "
                "replayed passing comparison"
            )
            continue
        expected = passing_comparisons[str(comparison_id)]
        if expected["kind"] not in CLAIMABLE_COMPARISON_KINDS:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} kind "
                f"{expected['kind']!r} is producer-attested only and cannot be verified"
            )
            continue
        dimension = claim.get("dimension")
        if dimension not in expected["dimensions"]:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} dimension "
                f"{dimension!r} did not pass its comparison gate"
            )
            continue
        scoped_fields = {
            "kind": "kind",
            "host_name": "host_name",
            "host_version": "host",
            "model": "model",
            "candidate_skill_revision": "candidate_skill_revision",
            "previous_skill_revision": "previous_skill_revision",
            "baseline_skill_revision": "baseline_skill_revision",
            "dataset_sha256": "dataset_sha256",
            "dataset_git_revision": "dataset_git_revision",
            "evaluation_anchor_revision": "evaluation_anchor_revision",
            "campaign_id": "campaign_id",
            "campaign_path": "campaign_path",
            "campaign_sha256": "campaign_sha256",
            "evaluation_protocol_revision": "evaluation_protocol_revision",
            "evaluation_protocol_sha256": "evaluation_protocol_sha256",
            "held_out_provenance_path": "held_out_provenance_path",
            "held_out_provenance_sha256": "held_out_provenance_sha256",
            "skills": "skills",
        }
        for claim_key, expected_key in scoped_fields.items():
            if claim.get(claim_key) != expected[expected_key]:
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} claim {claim_id} {claim_key} "
                    "does not match its comparison scope"
                )
    return errors, trials


def validate_quality_comparisons(
    root: Path,
    comparisons: list[dict[str, object]],
    evidence: dict[str, dict[str, object]],
) -> tuple[list[str], dict[str, dict[str, object]]]:
    """Replay comparison reports from validated immutable evidence bundles."""

    errors: list[str] = []
    passing: dict[str, dict[str, object]] = {}
    comparator = root / "scripts" / "compare-skill-evals.py"
    root_resolved = root.resolve()
    observed_ids: set[str] = set()
    observed_reports: set[Path] = set()
    observed_report_hashes: set[str] = set()
    comparison_fields = {
        "id",
        "kind",
        "candidate_evidence",
        "previous_evidence",
        "baseline_evidence",
        "campaign",
        "campaign_sha256",
        "report",
        "report_sha256",
    }

    for index, record in enumerate(comparisons, 1):
        comparison_id = record.get("id")
        if not isinstance(comparison_id, str) or not comparison_id.strip():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {index} missing id"
            )
            continue
        if comparison_id in observed_ids:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} duplicates comparison id {comparison_id}"
            )
            continue
        observed_ids.add(comparison_id)
        if set(record) != comparison_fields:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} "
                f"fields must be {sorted(comparison_fields)}"
            )
            continue
        kind = record.get("kind")
        if kind not in {"routing", "authority", "workflow"}:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} has unknown kind {kind!r}"
            )
            continue

        selected: dict[str, list[str]] = {}
        invalid_selection = False
        for key in (
            "candidate_evidence",
            "previous_evidence",
            "baseline_evidence",
        ):
            values = record.get(key)
            if (
                not isinstance(values, list)
                or not values
                or any(not isinstance(item, str) or not item.strip() for item in values)
                or len(values) != len(set(values))
            ):
                errors.append(
                    f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} "
                    f"{key} must be a non-empty unique string list"
                )
                invalid_selection = True
                break
            selected[key] = values
        if invalid_selection:
            continue
        selected_sets = [
            set(selected["candidate_evidence"]),
            set(selected["previous_evidence"]),
            set(selected["baseline_evidence"]),
        ]
        if any(
            selected_sets[left] & selected_sets[right]
            for left in range(len(selected_sets))
            for right in range(left + 1, len(selected_sets))
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} reuses evidence across variants"
            )
            continue
        evidence_ids = [
            *selected["candidate_evidence"],
            *selected["previous_evidence"],
            *selected["baseline_evidence"],
        ]
        missing = [evidence_id for evidence_id in evidence_ids if evidence_id not in evidence]
        if missing:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} references invalid evidence {sorted(missing)}"
            )
            continue
        candidate_records = [evidence[item] for item in selected["candidate_evidence"]]
        previous_records = [evidence[item] for item in selected["previous_evidence"]]
        baseline_records = [evidence[item] for item in selected["baseline_evidence"]]
        all_records = [*candidate_records, *previous_records, *baseline_records]
        if any(item["kind"] != kind for item in all_records):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} mixes evidence kinds"
            )
            continue
        if any(item["variant"] != "candidate" for item in candidate_records):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} candidate_evidence must use candidate bundles"
            )
            continue
        if any(item["variant"] != "previous" for item in previous_records):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} previous_evidence must use previous bundles"
            )
            continue
        if any(item["variant"] != "baseline" for item in baseline_records):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} baseline_evidence must use baseline bundles"
            )
            continue
        dataset_paths = {Path(item["dataset_path"]) for item in all_records}
        dataset_hashes = {str(item["dataset_sha256"]) for item in all_records}
        if len(dataset_paths) != 1 or len(dataset_hashes) != 1:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} must use one dataset"
            )
            continue
        campaign_paths = {str(item["campaign_path"]) for item in all_records}
        campaign_hashes = {str(item["campaign_sha256"]) for item in all_records}
        if len(campaign_paths) != 1 or len(campaign_hashes) != 1:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} must use one campaign"
            )
            continue
        campaign_relative = next(iter(campaign_paths))
        campaign_hash = next(iter(campaign_hashes))
        if (
            record.get("campaign") != campaign_relative
            or record.get("campaign_sha256") != campaign_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} campaign binding mismatch"
            )
            continue
        campaign_path = (root / campaign_relative).resolve()

        report = record.get("report")
        if not isinstance(report, str) or not report.strip() or Path(report).is_absolute():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report must be a relative path"
            )
            continue
        report_path = (root / report).resolve()
        try:
            report_path.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report escapes repository"
            )
            continue
        if not report_path.is_file():
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report does not exist"
            )
            continue
        report_hash = hashlib.sha256(report_path.read_bytes()).hexdigest()
        expected_report_hash = record.get("report_sha256")
        if (
            not isinstance(expected_report_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_report_hash) is None
            or expected_report_hash != report_hash
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report hash mismatch"
            )
            continue
        if report_path in observed_reports or report_hash in observed_report_hashes:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} replays a comparison report"
            )
            continue
        observed_reports.add(report_path)
        observed_report_hashes.add(report_hash)
        try:
            recorded_report = json.loads(
                report_path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} cannot read report: {error}"
            )
            continue

        candidate_records.sort(key=lambda item: int(item["trial"]))
        previous_records.sort(key=lambda item: int(item["trial"]))
        baseline_records.sort(key=lambda item: int(item["trial"]))
        command = [
            sys.executable,
            str(comparator),
            "--kind",
            str(kind),
            "--dataset",
            str(next(iter(dataset_paths))),
            "--campaign",
            str(campaign_path),
        ]
        for item in candidate_records:
            command.extend(("--candidate", str(item["bundle_path"])))
        for item in previous_records:
            command.extend(("--previous", str(item["bundle_path"])))
        for item in baseline_records:
            command.extend(("--baseline", str(item["bundle_path"])))
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            replayed_report = json.loads(
                completed.stdout,
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except (json.JSONDecodeError, ValueError) as error:
            detail = (completed.stderr or completed.stdout).strip()
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} replay produced invalid JSON: {detail or error}"
            )
            continue
        if completed.returncode != 0 or replayed_report.get("status") != "PASS":
            detail = replayed_report.get("errors", [])
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} did not pass replay: {detail}"
            )
            continue
        if replayed_report != recorded_report:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report does not match replay"
            )
            continue
        dimensions = replayed_report.get("claimable_dimensions")
        if not isinstance(dimensions, list) or any(
            not isinstance(item, str) for item in dimensions
        ):
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} report "
                "missing claimable_dimensions"
            )
            continue
        allowed_dimensions = set(
            VALIDATION_CONTRACTS["behavior_eval"]["comparative"][
                "claimable_dimensions"
            ]
        )
        unknown_dimensions = set(dimensions) - allowed_dimensions
        if unknown_dimensions:
            errors.append(
                f"repository: {QUALITY_EVIDENCE_FILE} comparison {comparison_id} "
                f"reports unknown claimable dimensions {sorted(unknown_dimensions)}"
            )
            continue
        candidate_record = candidate_records[0]
        previous_record = previous_records[0]
        baseline_record = baseline_records[0]
        passing[str(comparison_id)] = {
            "kind": str(kind),
            "host_name": candidate_record["host_name"],
            "host": candidate_record["host"],
            "model": candidate_record["model"],
            "candidate_skill_revision": candidate_record["skill_revision"],
            "previous_skill_revision": previous_record["skill_revision"],
            "baseline_skill_revision": baseline_record["skill_revision"],
            "dataset_sha256": candidate_record["dataset_sha256"],
            "dataset_git_revision": candidate_record["dataset_git_revision"],
            "evaluation_anchor_revision": candidate_record[
                "evaluation_anchor_revision"
            ],
            "campaign_id": candidate_record["campaign_id"],
            "campaign_path": candidate_record["campaign_path"],
            "campaign_sha256": candidate_record["campaign_sha256"],
            "evaluation_protocol_revision": candidate_record[
                "evaluation_protocol_revision"
            ],
            "evaluation_protocol_sha256": candidate_record[
                "evaluation_protocol_sha256"
            ],
            "held_out_provenance_path": candidate_record[
                "held_out_provenance_path"
            ],
            "held_out_provenance_sha256": candidate_record[
                "held_out_provenance_sha256"
            ],
            "skills": sorted(
                path.parent.name for path in (root / "skills").glob("*/SKILL.md")
            ),
            "dimensions": dimensions,
        }
    return errors, passing


def validate_quality_status(root: Path, packages: list[SkillPackage]) -> list[str]:
    errors: list[str] = []
    path = root / QUALITY_STATUS_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return [f"repository: cannot read {QUALITY_STATUS_FILE}: {error}"]

    evidence_errors, evidence_trials = validate_quality_evidence(root)
    errors.extend(evidence_errors)
    minimum_trials = int(
        VALIDATION_CONTRACTS["behavior_eval"]["comparative"][
            "minimum_trials_per_variant"
        ]
    )

    rows = markdown_table_rows(text, "## Skill Status")
    expected = {package.name for package in packages}
    observed: dict[str, list[str]] = {}
    for row in rows:
        if len(row) != 6:
            errors.append(
                f"repository: {QUALITY_STATUS_FILE} skill row must have 6 columns: {row}"
            )
            continue
        name = row[0].strip().strip("`")
        if name in observed:
            errors.append(f"repository: {QUALITY_STATUS_FILE} duplicates skill {name}")
            continue
        observed[name] = row
        category, release, structure, behavior, workflow = row[1:]
        if category not in QUALITY_CATEGORIES:
            errors.append(
                f"repository: {QUALITY_STATUS_FILE} skill {name} has unknown category {category!r}"
            )
        if release not in RELEASE_STATES:
            errors.append(
                f"repository: {QUALITY_STATUS_FILE} skill {name} has unknown release state {release!r}"
            )
        for axis, state in (
            ("structure", structure),
            ("behavior", behavior),
            ("workflow", workflow),
        ):
            if state not in VALIDATION_STATES:
                errors.append(
                    f"repository: {QUALITY_STATUS_FILE} skill {name} has unknown {axis} state {state!r}"
                )
        if behavior == "verified":
            if "authority" not in CLAIMABLE_COMPARISON_KINDS:
                errors.append(
                    f"repository: {QUALITY_STATUS_FILE} skill {name} behavior=verified "
                    "is unavailable while authority evidence is producer-attested only"
                )
            for kind in ("routing", "authority"):
                recorded = len(evidence_trials.get((kind, "candidate"), set()))
                if recorded < minimum_trials:
                    errors.append(
                        f"repository: {QUALITY_STATUS_FILE} skill {name} behavior=verified "
                        f"requires {minimum_trials} passing candidate {kind} trials; found {recorded}"
                    )
        if workflow == "verified":
            if "workflow" not in CLAIMABLE_COMPARISON_KINDS:
                errors.append(
                    f"repository: {QUALITY_STATUS_FILE} skill {name} workflow=verified "
                    "is unavailable while workflow evidence is producer-attested only"
                )
            recorded = len(evidence_trials.get(("workflow", "candidate"), set()))
            if recorded < minimum_trials:
                errors.append(
                    f"repository: {QUALITY_STATUS_FILE} skill {name} workflow=verified "
                    f"requires {minimum_trials} passing candidate workflow trials; found {recorded}"
                )

    for name in sorted(expected - set(observed)):
        errors.append(f"repository: {QUALITY_STATUS_FILE} missing skill {name}")
    for name in sorted(set(observed) - expected):
        errors.append(f"repository: {QUALITY_STATUS_FILE} lists unknown skill {name}")
    return errors


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key {key!r}")
        result[key] = value
    return result


def expected_routes_to_skill(expected: str, skill_name: str) -> bool:
    """Recognize an affirmative routing decision, not a coincidental skill mention."""

    token_re = re.compile(
        rf"(?<![a-z0-9-]){re.escape(skill_name)}(?![a-z0-9-])",
        re.IGNORECASE,
    )
    positive_re = re.compile(
        r"(?:prefer|use|trigger|before|keep|delegate|route)[^.;]{0,100}$",
        re.IGNORECASE,
    )
    negative_re = re.compile(
        r"(?:(?:do|does|should|must)\s+not|don't|never)\s+"
        r"(?:prefer|use|trigger|route|delegate)[^.;]{0,50}$"
        r"|(?:\bnot\b|rather than|instead of)[^.;]{0,40}$",
        re.IGNORECASE,
    )
    for match in token_re.finditer(expected):
        prefix = expected[max(0, match.start() - 120) : match.start()]
        if negative_re.search(prefix):
            continue
        if positive_re.search(prefix):
            return True
    return False


def validate_routing_graph(root: Path, packages: list[SkillPackage]) -> list[str]:
    """Require symmetric nearest-neighbor routing and documented pairwise eval coverage."""

    errors: list[str] = []
    path = root / ROUTING_GRAPH_FILE
    known = {package.name for package in packages}
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [f"repository: cannot read {ROUTING_GRAPH_FILE}: {error}"]
    if not isinstance(payload, dict):
        return [f"repository: {ROUTING_GRAPH_FILE} must contain an object"]

    listed = set(payload)
    for name in sorted(known - listed):
        errors.append(f"repository: routing graph missing skill {name}")
    for name in sorted(listed - known):
        errors.append(f"repository: routing graph lists unknown skill {name}")

    package_by_name = {package.name: package for package in packages}
    for name in sorted(known & listed):
        neighbors = payload.get(name)
        if not isinstance(neighbors, list) or any(
            not isinstance(neighbor, str) for neighbor in neighbors
        ):
            errors.append(f"repository: routing graph entry {name} must be a string list")
            continue
        if len(neighbors) != len(set(neighbors)):
            errors.append(f"repository: routing graph entry {name} contains duplicates")
        if name in neighbors:
            errors.append(f"repository: routing graph entry {name} cannot reference itself")

        eval_path = package_by_name[name].path / "references" / EVAL_CASES_FILE
        eval_text = (
            eval_path.read_text(encoding="utf-8", errors="ignore")
            if eval_path.is_file()
            else ""
        )
        routing_expectations = [
            cell
            for section in ("## Trigger Eval", "## Non-Trigger Eval")
            for row in markdown_table_rows(eval_text, section)
            for cell in row[1:2]
        ]
        for neighbor in neighbors:
            if neighbor not in known:
                errors.append(
                    f"repository: routing graph entry {name} references unknown skill {neighbor}"
                )
                continue
            reverse = payload.get(neighbor, [])
            if not isinstance(reverse, list) or name not in reverse:
                errors.append(
                    f"repository: routing graph edge {name} -> {neighbor} must be symmetric"
                )
            if not any(
                expected_routes_to_skill(expected, neighbor)
                for expected in routing_expectations
            ):
                errors.append(
                    f"source {name}: routing eval expectations do not cover nearest neighbor {neighbor}"
                )
    return errors


class StrictYamlError(ValueError):
    """Raised when a repository metadata file leaves the supported YAML subset."""


def _yaml_without_comment(value: str) -> str:
    """Remove a YAML comment outside quotes from one scalar line."""

    quote: str | None = None
    escaped = False
    index = 0
    while index < len(value):
        character = value[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
        elif quote == "'":
            if character == "'" and index + 1 < len(value) and value[index + 1] == "'":
                index += 1
            elif character == quote:
                quote = None
        elif character in {'"', "'"}:
            quote = character
        elif character == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        index += 1
    return value.rstrip()


def _parse_yaml_scalar(raw_value: str, *, line_number: int) -> object:
    value = _yaml_without_comment(raw_value).strip()
    if not value:
        raise StrictYamlError(f"line {line_number}: scalar value must not be empty")

    if value.startswith('"'):
        escaped = False
        closing = -1
        for index, character in enumerate(value[1:], 1):
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                closing = index
                break
        if closing < 0:
            raise StrictYamlError(f"line {line_number}: unterminated double-quoted scalar")
        trailing = value[closing + 1 :].strip()
        if trailing:
            raise StrictYamlError(
                f"line {line_number}: unexpected content after quoted scalar"
            )
        try:
            parsed = json.loads(value[: closing + 1])
        except json.JSONDecodeError as error:
            raise StrictYamlError(
                f"line {line_number}: invalid double-quoted scalar: {error.msg}"
            ) from error
        if not isinstance(parsed, str):
            raise StrictYamlError(f"line {line_number}: expected a string scalar")
        return parsed

    if value.startswith("'"):
        result: list[str] = []
        index = 1
        while index < len(value):
            character = value[index]
            if character == "'":
                if index + 1 < len(value) and value[index + 1] == "'":
                    result.append("'")
                    index += 2
                    continue
                trailing = value[index + 1 :].strip()
                if trailing:
                    raise StrictYamlError(
                        f"line {line_number}: unexpected content after quoted scalar"
                    )
                return "".join(result)
            result.append(character)
            index += 1
        raise StrictYamlError(f"line {line_number}: unterminated single-quoted scalar")

    if value[0] in "-?:,[]{}#&*!|>@`" or re.search(r":(?:\s|$)", value):
        raise StrictYamlError(
            f"line {line_number}: unsupported or ambiguous plain scalar"
        )
    lowered = value.casefold()
    if lowered in {
        "null",
        "~",
        "true",
        "false",
        "yes",
        "no",
        "on",
        "off",
    } or re.fullmatch(r"[-+]?(?:\d[\d_]*)(?:\.\d[\d_]*)?", value):
        raise StrictYamlError(
            f"line {line_number}: non-string YAML scalars are not supported"
        )
    return value


def parse_strict_yaml_mapping(yaml_text: str) -> dict[str, object]:
    """Parse the repository's intentionally small, two-level YAML mapping subset."""

    result: dict[str, object] = {}
    active_child: dict[str, object] | None = None
    for line_number, raw_line in enumerate(yaml_text.splitlines(), 1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise StrictYamlError(f"line {line_number}: tabs are not allowed")
        indentation = len(raw_line) - len(raw_line.lstrip(" "))
        if indentation not in {0, 2}:
            raise StrictYamlError(
                f"line {line_number}: indentation must be zero or two spaces"
            )
        content = raw_line[indentation:]
        if ":" not in content:
            raise StrictYamlError(f"line {line_number}: expected key: value")
        key, raw_value = content.split(":", 1)
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key) is None:
            raise StrictYamlError(f"line {line_number}: invalid mapping key {key!r}")

        target = result if indentation == 0 else active_child
        if target is None:
            raise StrictYamlError(
                f"line {line_number}: nested key has no parent mapping"
            )
        if key in target:
            raise StrictYamlError(f"line {line_number}: duplicate key {key!r}")

        without_comment = _yaml_without_comment(raw_value).strip()
        if indentation == 0 and not without_comment:
            child: dict[str, object] = {}
            result[key] = child
            active_child = child
            continue
        if indentation == 2 and not without_comment:
            raise StrictYamlError(
                f"line {line_number}: nested mappings deeper than interface are unsupported"
            )
        target[key] = _parse_yaml_scalar(raw_value, line_number=line_number)
        if indentation == 0:
            active_child = None
    return result


def _frontmatter_payload(skill_md: Path) -> tuple[dict[str, object], list[str]]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, ["frontmatter must start with '---'"]
    try:
        closing = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["frontmatter is missing closing '---'"]
    try:
        payload = parse_strict_yaml_mapping("\n".join(lines[1:closing]))
    except StrictYamlError as error:
        return {}, [f"frontmatter is invalid YAML: {error}"]
    return payload, []


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    payload, errors = _frontmatter_payload(skill_md)
    if errors:
        return {}
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str)
    }


def frontmatter_contract_errors(skill_md: Path) -> list[str]:
    payload, errors = _frontmatter_payload(skill_md)
    if errors:
        return errors
    expected_keys = {"name", "description"}
    for key in sorted(set(payload) - expected_keys):
        errors.append(
            f"frontmatter key {key!r} is not part of this repository's portable core"
        )
    for key in sorted(expected_keys - set(payload)):
        errors.append(f"frontmatter missing key {key!r}")
    for key in sorted(expected_keys & set(payload)):
        value = payload[key]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"frontmatter key {key!r} must be a non-empty string")
    return errors


def skill_name_errors(name: str) -> list[str]:
    errors: list[str] = []
    if not name or len(name) > 64 or SKILL_NAME_RE.fullmatch(name) is None:
        errors.append("must contain 1-64 lowercase letters, digits, or hyphens")
    if name.startswith("-") or name.endswith("-"):
        errors.append("must not start or end with a hyphen")
    if "--" in name:
        errors.append("must not contain consecutive hyphens")
    return errors


def frontmatter_yaml_string_errors(skill_md: Path) -> list[str]:
    # Kept as a compatibility shim for callers; strict parsing now owns this check.
    return []


def yaml_value_exists(yaml_text: str, key: str) -> bool:
    return bool(yaml_scalar(yaml_text, key))


def yaml_scalar(yaml_text: str, key: str) -> str:
    try:
        payload = parse_strict_yaml_mapping(yaml_text)
    except StrictYamlError:
        return ""
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        return ""
    value = interface.get(key)
    return value if isinstance(value, str) else ""


def openai_yaml_contract(yaml_text: str) -> tuple[dict[str, str], list[str]]:
    """Validate and return the exact provider interface metadata schema."""

    try:
        payload = parse_strict_yaml_mapping(yaml_text)
    except StrictYamlError as error:
        return {}, [f"invalid YAML: {error}"]
    errors: list[str] = []
    if set(payload) != {"interface"}:
        unknown = sorted(set(payload) - {"interface"})
        missing = "interface" not in payload
        if missing:
            errors.append("top level must contain interface")
        if unknown:
            errors.append(f"top level contains unsupported keys {unknown}")
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        errors.append("interface must be a mapping")
        return {}, errors
    required = {"display_name", "short_description", "default_prompt"}
    missing_keys = sorted(required - set(interface))
    unknown_keys = sorted(set(interface) - required)
    if missing_keys:
        errors.append(f"interface missing keys {missing_keys}")
    if unknown_keys:
        errors.append(f"interface contains unsupported keys {unknown_keys}")
    values: dict[str, str] = {}
    for key in sorted(required & set(interface)):
        value = interface[key]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"interface.{key} must be a non-empty string")
        else:
            values[key] = value
    return values, errors


def has_markdown_reference(package_path: Path) -> bool:
    references_dir = package_path / "references"
    return references_dir.is_dir() and any(references_dir.glob("*.md"))


def markdown_links(markdown_text: str) -> set[str]:
    links: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(markdown_text):
        link = match.group(1).split("#", 1)[0]
        if link and not re.match(r"^[a-z]+://", link):
            links.add(link)
    return links


def markdown_table_rows(markdown_text: str, section: str) -> list[list[str]]:
    start = markdown_text.find(section)
    if start < 0:
        return []
    body_start = start + len(section)
    next_section = markdown_text.find("\n## ", body_start)
    body = markdown_text[body_start:] if next_section < 0 else markdown_text[body_start:next_section]
    table_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table_lines[2:]
    ]


def normalized_eval_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`")).casefold()


def missing_table_cases(
    eval_text: str, section: str, required_cases: tuple[str, ...]
) -> list[str]:
    rows = markdown_table_rows(eval_text, section)
    keys = {normalized_eval_key(row[0]) for row in rows if row}
    return [case for case in required_cases if normalized_eval_key(case) not in keys]


def validate_specialized_eval_contracts(
    skill_name: str, eval_text: str, *, label: str
) -> list[str]:
    """Validate high-risk package contracts that generic table checks cannot prove."""

    errors: list[str] = []
    if skill_name == "implement-rust":
        section = "## Overlay Selection Eval"
        if section not in eval_text:
            errors.append(f"{label}: missing specialized section {section!r}")
        else:
            rows = markdown_table_rows(eval_text, section)
            keys = [normalized_eval_key(row[0]) for row in rows if row]
            required_prefixes = (
                "routine:",
                "contract:",
                "sqlite:",
                "ffi:",
                "ffi + sqlite:",
                "target-only:",
            )
            for prefix in required_prefixes:
                if not any(key.startswith(prefix) for key in keys):
                    errors.append(
                        f"{label}: {section} missing required case prefix {prefix!r}"
                    )

    elif skill_name == "audit-rust":
        profile_section = AUDIT_RUST_CONTRACT["profile_section"]
        if profile_section not in eval_text:
            errors.append(f"{label}: missing specialized section {profile_section!r}")
        else:
            profile_start = eval_text.find(profile_section)
            profile_end = eval_text.find("\n## ", profile_start + len(profile_section))
            profile_text = (
                eval_text[profile_start:]
                if profile_end < 0
                else eval_text[profile_start:profile_end]
            )
            for term in AUDIT_RUST_CONTRACT["required_profiles"]:
                if term not in profile_text:
                    errors.append(
                        f"{label}: {profile_section} missing required profile case {term!r}"
                    )
            out_of_scope_term = AUDIT_RUST_CONTRACT["out_of_scope_term"]
            if out_of_scope_term not in profile_text:
                errors.append(
                    f"{label}: {profile_section} must require unselected profiles to be {out_of_scope_term!r}"
                )

        scenario_section = AUDIT_RUST_CONTRACT["scenario_section"]
        scenario_end_section = AUDIT_RUST_CONTRACT["scenario_end_section"]
        scenario_start = eval_text.find(scenario_section)
        scenario_end = eval_text.find(f"\n{scenario_end_section}", scenario_start)
        if scenario_start < 0 or scenario_end < 0:
            errors.append(f"{label}: missing complete specialized section {scenario_section!r}")
        else:
            scenario_text = eval_text[scenario_start:scenario_end]
            matches = list(re.finditer(r"^###\s+(\d+)\.\s+.+$", scenario_text, re.MULTILINE))
            minimum_scenarios = AUDIT_RUST_CONTRACT["minimum_scenarios"]
            if len(matches) < minimum_scenarios:
                errors.append(
                    f"{label}: audit-rust Scenario Eval must contain at least {minimum_scenarios} scenarios"
                )
            for index, match in enumerate(matches):
                block_end = (
                    matches[index + 1].start()
                    if index + 1 < len(matches)
                    else len(scenario_text)
                )
                block = scenario_text[match.start():block_end]
                number = match.group(1)
                for field in AUDIT_RUST_CONTRACT["scenario_fields"]:
                    if f"**{field}:**" not in block:
                        errors.append(
                            f"{label}: audit-rust scenario {number} missing field {field!r}"
                        )

    elif skill_name == "chatgpt-review":
        required = (
            "Package artifact",
            "Split package artifact",
            "Multipart send sequence",
            "External authorization",
            "Response completion",
            "Review artifact visibility",
            "Local verification",
            "Capability Snapshot contract",
            "Browser handoff contract",
            "Operation idempotency",
            "Interruption reconciliation",
            "Identity-bound snapshot",
            "Conversation creation idempotency",
            "Round and operation scope",
            "Legal transitions",
            "Retry attempt lifecycle",
            "Identity privacy",
        )
        for case in missing_table_cases(eval_text, "## Quality Eval", required):
            errors.append(
                f"{label}: chatgpt-review Quality Eval missing required case {case!r}"
            )

    elif skill_name == "audit-frontend":
        scenario_rows = markdown_table_rows(eval_text, "## Scenario Eval")
        scenario_text = "\n".join(" | ".join(row) for row in scenario_rows)
        if len(scenario_rows) < 16:
            errors.append(
                f"{label}: audit-frontend Scenario Eval must contain at least 16 cases"
            )
        for term in ("Vue Composition API", "Pure Options API", "`repo-review` delegates"):
            if term not in scenario_text:
                errors.append(
                    f"{label}: audit-frontend Scenario Eval missing required case {term!r}"
                )
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Framework profile", "Vue API-style fidelity", "Read-only boundary"),
        ):
            errors.append(
                f"{label}: audit-frontend Quality Eval missing required case {case!r}"
            )

    elif skill_name == "repo-review":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Immutable basis", "Specialist composition", "Duplicate control", "Read-only boundary"),
        ):
            errors.append(
                f"{label}: repo-review Quality Eval missing required case {case!r}"
            )

    elif skill_name == "repo-map":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Scope and stop condition", "Context-versus-review boundary", "Reuse inventory", "New-file gate"),
        ):
            errors.append(
                f"{label}: repo-map Quality Eval missing required case {case!r}"
            )

    elif skill_name == "audit-security":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Scope mapping", "Scoped specialist boundary", "Release check"),
        ):
            errors.append(
                f"{label}: audit-security Quality Eval missing required case {case!r}"
            )

    elif skill_name == "ops-browser":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            (
                "Browser debug handoff",
                "State safety",
                "Cleanup",
                "Capability Snapshot contract",
                "Bridge handoff contract",
                "Duplicate-submit prevention",
                "Failed-before-submit retry",
                "Identity freshness",
                "Conversation creation operation",
                "Legal transition result",
                "Retry attempt evidence",
                "Snapshot privacy",
            ),
        ):
            errors.append(
                f"{label}: ops-browser Quality Eval missing required case {case!r}"
            )

    elif skill_name == "ops-client":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Client debug handoff", "Runtime source", "Unsupported versus unverified"),
        ):
            errors.append(
                f"{label}: ops-client Quality Eval missing required case {case!r}"
            )

    return errors


def markdown_section(markdown_text: str, section: str) -> str:
    start = markdown_text.find(section)
    if start < 0:
        return ""
    body_start = start + len(section)
    next_section = markdown_text.find("\n## ", body_start)
    return markdown_text[body_start:] if next_section < 0 else markdown_text[body_start:next_section]


CROSS_ARTIFACT_TERM_REQUIREMENTS: tuple[
    tuple[str, str, str | None, tuple[str, ...]], ...
] = tuple(
    (
        item["skill"],
        item["surface"],
        item["section"],
        tuple(item["terms"]),
    )
    for item in VALIDATION_CONTRACTS["cross_artifact_terms"]
)


def eval_row(eval_text: str, section: str, key: str) -> list[str]:
    wanted = normalized_eval_key(key)
    for row in markdown_table_rows(eval_text, section):
        if row and normalized_eval_key(row[0]) == wanted:
            return row
    return []


def validate_eval_row_semantics(
    eval_text: str,
    section: str,
    key: str,
    column_terms: tuple[tuple[int, tuple[str, ...]], ...],
    *,
    label: str,
) -> list[str]:
    row = eval_row(eval_text, section, key)
    if not row:
        return [f"{label}: missing semantic eval row {key!r} in {section}"]
    errors: list[str] = []
    for column, terms in column_terms:
        cell = row[column].casefold() if len(row) > column else ""
        missing = [term for term in terms if term.casefold() not in cell]
        if missing:
            errors.append(
                f"{label}: eval row {key!r} column {column + 1} missing semantic terms {missing}"
            )
    return errors


def validate_cross_artifact_contracts(
    skill_name: str, surfaces: dict[str, str], *, label: str
) -> list[str]:
    """Validate scoped authority text plus structured Eval row behavior."""

    errors: list[str] = []
    for required_skill, surface, section, terms in CROSS_ARTIFACT_TERM_REQUIREMENTS:
        if required_skill != skill_name:
            continue
        source = surfaces.get(surface, "")
        scoped = markdown_section(source, section) if section else source
        missing = [term for term in terms if term.casefold() not in scoped.casefold()]
        if missing:
            errors.append(
                f"{label}: {skill_name} {surface} {section or 'field'} missing contract terms {missing}"
            )

    eval_text = surfaces.get("references/eval-cases.md", "")
    semantic_rows: dict[str, tuple[tuple[str, str, tuple[tuple[int, tuple[str, ...]], ...]], ...]] = {
        "repo-review": (("## Quality Eval", "Immutable basis", ((1, ("sha", "before conclusions")), (2, ("moving", "ambiguous")))),),
        "repo-map": (("## Quality Eval", "Context-versus-review boundary", ((1, ("without p0-p3", "repo-review")), (2, ("universal review",)))),),
        "audit-security": (("## Quality Eval", "Scoped specialist boundary", ((1, ("delegated paths/diff", "repo-review")), (2, ("expands scope", "whole-review readiness")))),),
        "ops-browser": (
            ("## Trigger Eval", "Reproduce this known browser-only CORS failure and collect console/network evidence.", ((1, ("browser debug evidence", "directly")), (2, ("browser fact",)))),
            ("## Trigger Eval", "Diagnose delegated this exact browser reproduction; collect DOM, console, and network evidence.", ((1, ("browser debug evidence",)), (2, ("delegation",)))),
            ("## Non-Trigger Eval", "Why does this form intermittently fail after submit? Find the root cause.", ((1, ("diagnose", "browser debug evidence")), (2, ("cross-system",)))),
            ("## Quality Eval", "Browser debug handoff", ((1, ("diagnose", "already-isolated", "retains referenced evidence")), (2, ("final cause/fix", "deletes evidence before transfer")))),
        ),
        "ops-client": (
            ("## Trigger Eval", "Diagnose delegated this exact release-window reproduction; collect process and window evidence.", ((1, ("client debug evidence",)), (2, ("delegation",)))),
            ("## Trigger Eval", "On the verified release app, reproduce this already-isolated Accessibility action failure and return client evidence only.", ((1, ("client debug evidence",)), (2, ("bounded", "without cross-system")))),
            ("## Non-Trigger Eval", "Why does the release app button not respond? Find the root cause.", ((1, ("diagnose", "client debug evidence")), (2, ("cross", "boundaries")))),
            ("## Quality Eval", "Client debug handoff", ((1, ("diagnose", "already-isolated", "retains referenced evidence")), (2, ("final cause/fix", "deletes evidence before transfer")))),
        ),
    }
    for section, key, columns in semantic_rows.get(skill_name, ()):
        errors.extend(
            validate_eval_row_semantics(eval_text, section, key, columns, label=label)
        )
    forbidden_by_skill = {
        "ops-browser": (
            "not prefer `diagnose`",
            "trigger `ops-browser` directly and may later",
            "permits final cause/fix",
            "deletes evidence before transfer after reporting",
            "direct operation takes precedence over `diagnose`",
        ),
        "ops-client": (
            "not prefer `diagnose`",
            "trigger `ops-client` directly and may later",
            "permits final cause/fix",
            "deletes evidence before transfer after reporting",
            "direct operation takes precedence over `diagnose`",
        ),
    }
    combined_contract_text = "\n".join(surfaces.values()).casefold()
    for forbidden in forbidden_by_skill.get(skill_name, ()):
        if forbidden.casefold() in combined_contract_text:
            errors.append(
                f"{label}: {skill_name} contains contradictory contract phrase {forbidden!r}"
            )
    return errors


def package_files(package_path: Path) -> list[Path]:
    return [path for path in package_path.rglob("*") if path.is_file()]


def validate_local_links(package_path: Path, *, label: str) -> list[str]:
    errors: list[str] = []
    for markdown_file in sorted(package_path.rglob("*.md")):
        markdown_text = markdown_file.read_text(encoding="utf-8")
        for link in sorted(markdown_links(markdown_text)):
            target = (markdown_file.parent / link).resolve()
            try:
                target.relative_to(package_path.resolve())
            except ValueError:
                errors.append(f"{label}: link escapes skill package: {markdown_file.name} -> {link}")
                continue
            if not target.exists():
                relative = markdown_file.relative_to(package_path)
                errors.append(f"{label}: broken local link in {relative}: {link}")
    return errors


def validate_eval_cases(
    eval_cases: Path, *, label: str, skill_name: str | None = None
) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    eval_text = eval_cases.read_text(encoding="utf-8")
    trigger_rows = markdown_table_rows(eval_text, "## Trigger Eval")
    non_trigger_rows = markdown_table_rows(eval_text, "## Non-Trigger Eval")
    quality_rows = markdown_table_rows(eval_text, "## Quality Eval")

    minimums = (
        ("trigger", trigger_rows, MIN_TRIGGER_CASES, 2),
        ("non-trigger", non_trigger_rows, MIN_NON_TRIGGER_CASES, 2),
        ("quality", quality_rows, MIN_QUALITY_CASES, 3),
    )
    for name, rows, minimum, columns in minimums:
        if len(rows) < minimum:
            errors.append(f"{label}: eval {name} cases must contain at least {minimum} rows")
        for index, row in enumerate(rows, start=1):
            if len(row) < columns or any(not cell for cell in row[:columns]):
                errors.append(f"{label}: eval {name} row {index} must contain {columns} non-empty columns")

    for name, rows in (("trigger", trigger_rows), ("non-trigger", non_trigger_rows), ("quality", quality_rows)):
        keys = [normalized_eval_key(row[0]) for row in rows if row]
        if len(keys) != len(set(keys)):
            errors.append(f"{label}: eval {name} cases contain duplicate first-column values")

    scoring_start = eval_text.find("## Scoring")
    scoring = eval_text[scoring_start:] if scoring_start >= 0 else ""
    has_minimum = "Minimum pass:" in scoring
    has_numeric_gate = re.search(r"scores? at least (?:[89]|10)", scoring)
    has_defect_gate = "no P0 or P1 defect remains" in scoring
    if not has_minimum or not (has_numeric_gate or has_defect_gate):
        errors.append(
            f"{label}: scoring must define either a minimum quality score of at least 8 "
            "or a no-P0/P1 defect gate"
        )

    if skill_name is not None:
        errors.extend(
            validate_specialized_eval_contracts(skill_name, eval_text, label=label)
        )

    metrics = QualityMetrics(
        description_chars=0,
        skill_lines=0,
        trigger_cases=len(trigger_rows),
        non_trigger_cases=len(non_trigger_rows),
        quality_cases=len(quality_rows),
    )
    return errors, metrics


def validate_references(package_path: Path, skill_md_text: str, *, label: str) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    metrics: QualityMetrics | None = None
    references_dir = package_path / "references"
    if not references_dir.is_dir():
        errors.append(f"{label}: missing references/")
        return errors, metrics

    reference_files = sorted(references_dir.glob("*.md"))
    if not reference_files:
        errors.append(f"{label}: missing references/*.md")
        return errors, metrics

    for nested_reference in sorted(references_dir.rglob("*.md")):
        if nested_reference.parent != references_dir:
            relative = nested_reference.relative_to(package_path)
            errors.append(f"{label}: reference files must be one level deep: {relative}")

    for reference_file in reference_files:
        reference_text = reference_file.read_text(encoding="utf-8")
        line_count = len(reference_text.splitlines())
        if (
            line_count > REFERENCE_TOC_AFTER_LINES
            and reference_file.name not in REFERENCE_TOC_EXEMPTIONS
            and "## Contents" not in reference_text
        ):
            errors.append(
                f"{label}: references/{reference_file.name} has {line_count} lines and "
                f"must include ## Contents after {REFERENCE_TOC_AFTER_LINES} lines"
            )

    eval_cases = references_dir / EVAL_CASES_FILE
    if not eval_cases.is_file():
        errors.append(f"{label}: missing references/{EVAL_CASES_FILE}")
    else:
        eval_text = eval_cases.read_text(encoding="utf-8")
        for section in EVAL_REQUIRED_SECTIONS:
            if section not in eval_text:
                errors.append(f"{label}: references/{EVAL_CASES_FILE} missing section {section!r}")
        eval_errors, metrics = validate_eval_cases(
            eval_cases, label=label, skill_name=package_path.name
        )
        errors.extend(eval_errors)

    linked = markdown_links(skill_md_text)
    for reference_file in reference_files:
        expected_link = f"references/{reference_file.name}"
        if expected_link not in linked:
            errors.append(f"{label}: SKILL.md does not link {expected_link}")

    errors.extend(validate_local_links(package_path, label=label))
    return errors, metrics


def validate_package(package: SkillPackage, *, label: str) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    metrics: QualityMetrics | None = None
    package_path = package.path
    skill_md = package_path / "SKILL.md"
    openai_yaml = package_path / "agents" / "openai.yaml"
    skill_md_text = ""

    for name_error in skill_name_errors(package.name):
        errors.append(f"{label}: invalid skill directory name {package.name!r}: {name_error}")

    if not skill_md.is_file():
        errors.append(f"{label}: missing SKILL.md")
    else:
        skill_md_text = skill_md.read_text(encoding="utf-8")
        for frontmatter_error in frontmatter_contract_errors(skill_md):
            errors.append(f"{label}: SKILL.md {frontmatter_error}")
        for frontmatter_error in frontmatter_yaml_string_errors(skill_md):
            errors.append(f"{label}: SKILL.md {frontmatter_error}")
        frontmatter = read_frontmatter(skill_md)
        actual_name = frontmatter.get("name")
        description = frontmatter.get("description", "")
        if actual_name != package.name:
            errors.append(f"{label}: SKILL.md name must be {package.name!r}, found {actual_name!r}")
        if actual_name is not None:
            for name_error in skill_name_errors(actual_name):
                errors.append(f"{label}: SKILL.md name {name_error}")
        if not description.startswith("Use when"):
            errors.append(f"{label}: SKILL.md description must start with 'Use when'")
        if len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{label}: SKILL.md description must be {MAX_DESCRIPTION_CHARS} characters or fewer"
            )
        for phrase in FORBIDDEN_DESCRIPTION_PHRASES:
            if phrase in description:
                errors.append(f"{label}: SKILL.md description must not contain {phrase!r}")
        skill_lines = len(skill_md_text.splitlines())
        if skill_lines > MAX_SKILL_LINES:
            errors.append(f"{label}: SKILL.md must be {MAX_SKILL_LINES} lines or fewer")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in skill_md_text:
                errors.append(f"{label}: SKILL.md missing section {section!r}")
        if "## Workflow" not in skill_md_text and "## Modes" not in skill_md_text:
            errors.append(f"{label}: SKILL.md must include Workflow or Modes")

    if not openai_yaml.is_file():
        errors.append(f"{label}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        interface, yaml_errors = openai_yaml_contract(yaml_text)
        for yaml_error in yaml_errors:
            errors.append(f"{label}: agents/openai.yaml {yaml_error}")
        short_description = interface.get("short_description", "")
        default_prompt = interface.get("default_prompt", "")
        if default_prompt and f"${package.name}" not in default_prompt:
            errors.append(f"{label}: agents/openai.yaml default prompt should mention ${package.name}")
        if short_description and len(short_description) < MIN_SHORT_DESCRIPTION_CHARS:
            errors.append(
                f"{label}: short_description must be at least {MIN_SHORT_DESCRIPTION_CHARS} characters"
            )
        if len(short_description) > MAX_SHORT_DESCRIPTION_CHARS:
            errors.append(
                f"{label}: short_description must be {MAX_SHORT_DESCRIPTION_CHARS} characters or fewer"
            )
        if len(default_prompt) > MAX_DEFAULT_PROMPT_CHARS:
            errors.append(
                f"{label}: default_prompt must be {MAX_DEFAULT_PROMPT_CHARS} characters or fewer"
            )
        expected_prefix = f"Use ${package.name}"
        if default_prompt and not default_prompt.startswith(expected_prefix):
            errors.append(
                f"{label}: default_prompt must start with {expected_prefix!r}"
            )
        sentence_endings = re.findall(r"[.!?](?=\s|$)", default_prompt)
        if len(sentence_endings) > 1:
            errors.append(f"{label}: default_prompt must be one concise sentence")

    if not has_markdown_reference(package_path):
        errors.append(f"{label}: missing references/*.md")
    else:
        reference_errors, eval_metrics = validate_references(package_path, skill_md_text, label=label)
        errors.extend(reference_errors)
        if eval_metrics is not None:
            metrics = QualityMetrics(
                description_chars=len(description),
                skill_lines=len(skill_md_text.splitlines()),
                trigger_cases=eval_metrics.trigger_cases,
                non_trigger_cases=eval_metrics.non_trigger_cases,
                quality_cases=eval_metrics.quality_cases,
            )

    contract_surfaces = {
        "SKILL.md": skill_md_text,
        "agents/openai.yaml": (
            openai_yaml.read_text(encoding="utf-8") if openai_yaml.is_file() else ""
        ),
        "agents/openai.default_prompt": (
            yaml_scalar(openai_yaml.read_text(encoding="utf-8"), "default_prompt")
            if openai_yaml.is_file()
            else ""
        ),
        "references/usage.md": (
            (package_path / "references" / "usage.md").read_text(encoding="utf-8")
            if (package_path / "references" / "usage.md").is_file()
            else ""
        ),
        "references/eval-cases.md": (
            (package_path / "references" / EVAL_CASES_FILE).read_text(encoding="utf-8")
            if (package_path / "references" / EVAL_CASES_FILE).is_file()
            else ""
        ),
    }
    errors.extend(
        validate_cross_artifact_contracts(package.name, contract_surfaces, label=label)
    )

    for forbidden in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        if (package_path / forbidden).exists():
            errors.append(f"{label}: package-local {forbidden} is not allowed")

    for file_path in package_files(package_path):
        if file_path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        file_text = file_path.read_text(encoding="utf-8", errors="ignore")
        if LEGACY_RE.search(file_text):
            relative = file_path.relative_to(package_path)
            errors.append(f"{label}: stale legacy skill name found in {relative}")
        if PLACEHOLDER_RE.search(file_text):
            relative = file_path.relative_to(package_path)
            errors.append(f"{label}: unresolved placeholder marker found in {relative}")

    return errors, metrics


def validate_source_packages(packages: list[SkillPackage]) -> tuple[list[str], dict[str, QualityMetrics]]:
    errors: list[str] = []
    metrics: dict[str, QualityMetrics] = {}
    if not packages:
        errors.append("source: no skill packages found under skills/*/SKILL.md")
        return errors, metrics

    for package in packages:
        package_errors, package_metrics = validate_package(package, label=f"source {package.name}")
        errors.extend(package_errors)
        if package_metrics is not None:
            metrics[package.name] = package_metrics

    descriptions: dict[str, str] = {}
    for package in packages:
        frontmatter = read_frontmatter(package.path / "SKILL.md")
        normalized = re.sub(r"\s+", " ", frontmatter.get("description", "").strip()).casefold()
        if normalized in descriptions:
            errors.append(
                f"source {package.name}: duplicate description also used by {descriptions[normalized]}"
            )
        descriptions[normalized] = package.name
    return errors, metrics


def validate_shared_browser_operation_protocol(root: Path) -> list[str]:
    source_relative = Path("protocols/browser-operation-v1.md")
    generated_paths = (
        Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
        Path("skills/ops-browser/references/browser-operation-protocol.md"),
    )
    errors: list[str] = []
    try:
        source_content = (root / source_relative).read_text(encoding="utf-8")
    except OSError as error:
        return [f"repository: cannot read {source_relative}: {error}"]
    for relative in generated_paths:
        path = root / relative
        try:
            generated_content = path.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"repository: cannot read {relative}: {error}")
            continue
        if generated_content != source_content:
            errors.append(
                f"repository: generated browser-operation protocol is stale: {relative}; "
                "run python3 scripts/sync-shared-protocols.py"
            )
    required_by_section = {
        "## Capability Snapshot": (
            "schema_version: browser-operation/v1",
            "snapshot_id:",
            "identity:",
            "account_category:",
            "workspace_id:",
            "state_fingerprint:",
            "login_state:",
            "target_origin:",
            "capabilities:",
            "evidence:",
            "gaps:",
            "opaque one-way fingerprint",
            "Never store an email address",
        ),
        "## Handoff Request": (
            "schema_version: browser-operation/v1",
            "operation_id:",
            "round_id:",
            "attempt: <positive integer; starts at 1>",
            "intent:",
            "create-conversation",
            "authorization:",
            "capability_snapshot_id:",
            "preconditions:",
            "expected_postcondition:",
            "retry_policy: <never|only-if-no-side-effect-proven>",
            "prior_evidence:",
        ),
        "## Handoff Result": (
            "schema_version: browser-operation/v1",
            "operation_id:",
            "round_id:",
            "attempt: <same request attempt>",
            "capability_snapshot_id:",
            "state: <preflighted|ready|created|attached|submitted|acknowledged|captured|cleaned|completed|failed-before-submit|blocked|ambiguous>",
            "before:",
            "action:",
            "side_effect:",
            "after:",
            "retained_evidence:",
            "cleanup:",
            "error:",
        ),
        "## Operation State Machine": (
            "| `prepared` | `preflighted`, `blocked` |",
            "| `ready` | `created`, `attached`, `submitted`",
            "| `submitted` | `acknowledged`, `completed`, `ambiguous` |",
            "| `failed-before-submit` | `ready` only for a new attempt",
            "| `completed` | terminal |",
            "failed-before-submit",
            "round_id",
            "retry with the same ID",
        ),
        "## Degraded Mode": ("blocked", "ambiguous", "do not retry"),
    }
    for section, terms in required_by_section.items():
        scoped = markdown_section(source_content, section)
        if not scoped:
            errors.append(f"repository: shared browser-operation protocol missing section {section!r}")
            continue
        normalized_scoped = re.sub(r"\s+", " ", scoped).casefold()
        for term in terms:
            normalized_term = re.sub(r"\s+", " ", term).casefold()
            if normalized_term not in normalized_scoped:
                errors.append(
                    f"repository: shared browser-operation protocol {section} missing {term!r}"
                )
    return errors


def validate_skill_invocations(
    packages: list[SkillPackage], *, known_skill_names: set[str] | None = None
) -> list[str]:
    """Reject bare `$name` routes in default prompts that are not shipped skills.

    Agent metadata reserves bare `$name` for skill routing. Shell variables must
    use `${name}` or positional syntax such as `$1`; member access such as
    `this.$watch` is excluded by the route pattern.
    """

    errors: list[str] = []
    known = (
        {package.name for package in packages}
        if known_skill_names is None
        else known_skill_names
    )
    for package in packages:
        metadata_path = package.path / "agents" / "openai.yaml"
        if not metadata_path.is_file():
            continue
        yaml_text = metadata_path.read_text(encoding="utf-8", errors="ignore")
        default_prompt = yaml_scalar(yaml_text, "default_prompt")
        for referenced in sorted(set(SKILL_INVOCATION_RE.findall(default_prompt))):
            if referenced in known:
                continue
            relative = metadata_path.relative_to(package.path)
            errors.append(
                f"source {package.name}: unknown skill invocation ${referenced} in {relative}; "
                "bare $name is reserved for shipped skills, so use ${name} for shell variables"
            )
    return errors


def selected_packages(packages: list[SkillPackage], names: list[str]) -> tuple[list[SkillPackage], list[str]]:
    if not names:
        return packages, []

    package_by_name = {package.name: package for package in packages}
    selected: list[SkillPackage] = []
    missing: list[str] = []
    for name in names:
        package = package_by_name.get(name)
        if package is None:
            missing.append(name)
        else:
            selected.append(package)
    return selected, missing


def print_package_list(title: str, packages: list[SkillPackage]) -> None:
    print(title)
    for package in packages:
        print(f"  - {package.name}: {package.path}")


def print_quality_report(packages: list[SkillPackage], metrics: dict[str, QualityMetrics]) -> None:
    print("Documented eval coverage (not executed behavior):")
    print("  skill                     desc  lines  trigger  non-trigger  quality")
    for package in packages:
        item = metrics.get(package.name)
        if item is None:
            continue
        print(
            f"  {package.name:<25} {item.description_chars:>4}  {item.skill_lines:>5}"
            f"  {item.trigger_cases:>7}  {item.non_trigger_cases:>11}  {item.quality_cases:>7}"
        )


def main() -> int:
    args = parse_args()
    root = repo_root()
    source_dir = root / "skills"

    packages = discover_skills(source_dir)
    selected, missing = selected_packages(packages, args.skill)
    if missing:
        print(f"error: unknown skill(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    print_package_list("Discovered skill packages:", packages)

    source_errors, quality_metrics = validate_source_packages(selected)
    source_errors.extend(
        validate_skill_invocations(
            selected, known_skill_names={package.name for package in packages}
        )
    )
    if not args.skill:
        source_errors.extend(validate_official_baseline(VALIDATION_CONTRACTS))
        source_errors.extend(validate_repository_indexes(root, packages))
        source_errors.extend(validate_quality_status(root, packages))
        source_errors.extend(validate_routing_graph(root, packages))
        source_errors.extend(validate_shared_browser_operation_protocol(root))
    if source_errors:
        for error in source_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.quality_report:
        print_quality_report(selected, quality_metrics)

    print(f"validated source packages: {source_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
