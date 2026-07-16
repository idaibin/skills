#!/usr/bin/env python3
"""Create a canonical, preregistered Skill routing evaluation campaign.

The command is local-only: it reads Git metadata and hashes committed files and
never invokes a model host. Each invocation creates a fresh campaign UUID
unless the caller supplies one explicitly for deterministic fixture use.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path, PurePosixPath
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "scripts" / "evaluation_protocol.py"
_PROTOCOL_SPEC = importlib.util.spec_from_file_location(
    "aicraft_evaluation_protocol_for_campaign_creator", PROTOCOL_PATH
)
if _PROTOCOL_SPEC is None or _PROTOCOL_SPEC.loader is None:
    raise RuntimeError(f"cannot load evaluation protocol from {PROTOCOL_PATH}")
PROTOCOL = importlib.util.module_from_spec(_PROTOCOL_SPEC)
sys.modules[_PROTOCOL_SPEC.name] = PROTOCOL
_PROTOCOL_SPEC.loader.exec_module(PROTOCOL)

class CampaignCreationError(ValueError):
    """Raised when inputs cannot form a valid frozen campaign."""


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _git(root: Path, arguments: Sequence[str], *, binary: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=not binary,
    )
    if completed.returncode != 0:
        stderr = (
            completed.stderr.decode("utf-8", errors="replace")
            if binary
            else completed.stderr
        )
        stdout = (
            completed.stdout.decode("utf-8", errors="replace")
            if binary
            else completed.stdout
        )
        raise CampaignCreationError(
            (stderr or stdout or "git command failed").strip()
        )
    return completed.stdout


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repository_file(root: Path, value: str, *, label: str) -> tuple[Path, str]:
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != value:
        raise CampaignCreationError(
            f"{label} must be a normalized repository-relative POSIX path"
        )
    resolved = (root / value).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise CampaignCreationError(f"{label} escapes repository") from error
    if not resolved.is_file():
        raise CampaignCreationError(f"{label} does not exist: {value}")
    return resolved, value


def _committed_artifact(
    root: Path, relative_path: str, *, anchor: str, label: str
) -> dict[str, str]:
    path, relative_path = _repository_file(
        root, relative_path, label=f"--{label}"
    )
    revision = str(
        _git(root, ["log", "-1", "--format=%H", "--", relative_path])
    ).strip()
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise CampaignCreationError(f"{label} must be committed")
    committed = _git(root, ["show", f"{revision}:{relative_path}"], binary=True)
    if hashlib.sha256(committed).hexdigest() != _sha256_file(path):
        raise CampaignCreationError(
            f"{label} worktree content must exactly match its committed blob"
        )
    try:
        post_anchor = PROTOCOL.revision_is_ancestor(
            root, anchor, revision, strict=True
        )
    except PROTOCOL.ProtocolError as error:
        raise CampaignCreationError(str(error)) from error
    if not post_anchor:
        raise CampaignCreationError(f"{label} must be committed after the anchor")
    return {
        "path": relative_path,
        "sha256": _sha256_file(path),
        "git_revision": revision,
    }


def build_campaign(
    root: Path,
    *,
    candidate_anchor: str,
    previous_revision: str,
    dataset_path: str,
    provenance_path: str,
    host: str,
    model: str,
    timeout_seconds: int,
    concurrency: int,
    trial_count: int,
    campaign_id: str | None = None,
) -> dict[str, object]:
    """Build one fresh campaign payload without writing it."""

    root = root.resolve()
    try:
        contract = PROTOCOL.load_contract(root)
        anchor = PROTOCOL.resolve_commit(root, candidate_anchor)
        previous = PROTOCOL.resolve_commit(root, previous_revision)
    except PROTOCOL.ProtocolError as error:
        raise CampaignCreationError(str(error)) from error
    if not PROTOCOL.revision_is_ancestor(root, previous, anchor, strict=True):
        raise CampaignCreationError(
            "--previous-skill-revision must be a strict ancestor of the candidate anchor"
        )
    minimum_trials = int(
        contract["behavior_eval"]["comparative"]["minimum_trials_per_variant"]
    )
    if trial_count < minimum_trials:
        raise CampaignCreationError(
            f"--trials must be at least the contract minimum {minimum_trials}"
        )
    if timeout_seconds < 1 or concurrency < 1:
        raise CampaignCreationError("timeout and concurrency must be positive")

    dataset = _committed_artifact(
        root, dataset_path, anchor=anchor, label="dataset"
    )
    provenance = _committed_artifact(
        root, provenance_path, anchor=anchor, label="provenance"
    )
    if dataset["git_revision"] != provenance["git_revision"]:
        raise CampaignCreationError(
            "dataset and provenance must be introduced in the same post-anchor commit"
        )
    try:
        protocol_files = PROTOCOL.protocol_manifest_from_revision(
            root, anchor, contract
        )
        protocol_hash = PROTOCOL.evaluation_protocol_hash(protocol_files)
        PROTOCOL.assert_protocol_matches_anchor(
            root, anchor, protocol_hash, protocol_files, contract
        )
        prompt = PROTOCOL.canonical_prompt_template(contract)
        adjudication = PROTOCOL.canonical_adjudication(contract)
        environment_hash = PROTOCOL.canonical_hash(
            PROTOCOL.canonical_environment_policy(host, contract)
        )
        retry_policy_hash = PROTOCOL.canonical_hash(
            PROTOCOL.canonical_transient_retry_policy(host, contract)
        )
        host_hash = PROTOCOL.canonical_hash(
            PROTOCOL.canonical_host_policy(host, model, contract)
        )
    except PROTOCOL.ProtocolError as error:
        raise CampaignCreationError(str(error)) from error

    condition = {
        "host_name": host,
        "model": model,
        "timeout_seconds": timeout_seconds,
        "concurrency": concurrency,
        "prompt_template_version": int(
            contract["behavior_eval"]["prompt_template_version"]
        ),
        "prompt_template_sha256": PROTOCOL.sha256_text(prompt),
        "adjudication": adjudication,
        "host_config_sha256": host_hash,
        "environment_policy_sha256": environment_hash,
        "retry_policy_sha256": retry_policy_hash,
    }
    identity = {
        "schema_version": int(
            contract["behavior_eval"]["campaign_schema_version"]
        ),
        "candidate_skill_revision": anchor,
        "evaluation_anchor_revision": anchor,
        "previous_skill_revision": previous,
        "baseline_skill_revision": anchor,
        "dataset": dataset,
        "provenance": provenance,
        "condition": condition,
        "trial_count": trial_count,
        "evaluation_protocol": {
            "revision": anchor,
            "sha256": protocol_hash,
            "files": protocol_files,
        },
    }
    try:
        campaign_uuid = uuid.UUID(campaign_id) if campaign_id else uuid.uuid4()
    except ValueError as error:
        raise CampaignCreationError("--campaign-id must be a UUID") from error
    campaign_id = str(campaign_uuid)
    return {
        "schema_version": identity["schema_version"],
        "campaign_id": campaign_id,
        "artifact_root": f"eval-results/routing/campaigns/{campaign_id}",
        "candidate_skill_revision": anchor,
        "evaluation_anchor_revision": anchor,
        "previous_skill_revision": previous,
        "baseline_skill_revision": anchor,
        "dataset": dataset,
        "provenance": provenance,
        "condition": condition,
        "trials": [
            {
                "trial": trial,
                "comparison_group_id": str(
                    uuid.uuid5(campaign_uuid, f"comparison-group:{trial}")
                ),
            }
            for trial in range(1, trial_count + 1)
        ],
        "evaluation_protocol": identity["evaluation_protocol"],
    }


def create_campaign(
    root: Path,
    output_path: Path,
    payload: dict[str, object],
    *,
    overwrite: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    """Self-validate, then optionally atomically write the campaign."""

    root = root.resolve()
    output = output_path if output_path.is_absolute() else root / output_path
    output = output.resolve()
    try:
        output.relative_to(root)
    except ValueError as error:
        raise CampaignCreationError("--output must be inside the repository") from error
    if output.exists() and not overwrite:
        raise CampaignCreationError(f"refusing to overwrite existing campaign: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(
        payload, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    temporary = output.with_name(f".{output.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(encoded, encoding="utf-8")
    try:
        try:
            validated = PROTOCOL.load_campaign(
                root,
                temporary,
                PROTOCOL.load_contract(root),
                require_committed=False,
            )
        except PROTOCOL.ProtocolError as error:
            raise CampaignCreationError(
                f"generated campaign failed self-validation: {error}"
            ) from error
        if validated.payload != payload:
            raise CampaignCreationError(
                "generated campaign changed during self-validation"
            )
        if not dry_run:
            os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-anchor", required=True)
    parser.add_argument("--previous-skill-revision", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=_positive_integer, default=120)
    parser.add_argument("--concurrency", type=_positive_integer, default=1)
    parser.add_argument("--trials", type=_positive_integer, default=3)
    parser.add_argument(
        "--campaign-id",
        help=(
            "Optional explicit UUID for deterministic fixtures; omit it for a "
            "fresh preregistered campaign, including infrastructure retries."
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="self-validate and print the campaign without writing --output",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="explicitly replace an existing uncommitted output file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    try:
        payload = build_campaign(
            ROOT,
            candidate_anchor=arguments.candidate_anchor,
            previous_revision=arguments.previous_skill_revision,
            dataset_path=arguments.dataset,
            provenance_path=arguments.provenance,
            host=arguments.host,
            model=arguments.model,
            timeout_seconds=arguments.timeout,
            concurrency=arguments.concurrency,
            trial_count=arguments.trials,
            campaign_id=arguments.campaign_id,
        )
        create_campaign(
            ROOT,
            arguments.output,
            payload,
            overwrite=arguments.force,
            dry_run=arguments.dry_run,
        )
    except (CampaignCreationError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    if arguments.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        output = (
            arguments.output
            if arguments.output.is_absolute()
            else ROOT / arguments.output
        ).resolve()
        print(
            json.dumps(
                {
                    "campaign_id": payload["campaign_id"],
                    "output": str(output),
                    "sha256": _sha256_file(output),
                    "model_invoked": False,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
