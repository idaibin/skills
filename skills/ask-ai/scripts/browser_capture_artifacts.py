#!/usr/bin/env python3
"""Prepare and finalize durable browser-review capture artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REVIEW_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SCHEMA = "ask-ai-browser-capture/v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_receipt(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha256_bytes(data)}


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def git_output(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def verified_parent(repo_arg: str) -> tuple[Path, Path]:
    repo = Path(repo_arg).resolve(strict=True)
    git_root = Path(git_output(repo, "rev-parse", "--show-toplevel")).resolve()
    if git_root != repo:
        raise ValueError(f"repo must be the Git root: {git_root}")
    parent = repo / ".codex" / "reviews"
    parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink() or parent.resolve().parent != (repo / ".codex").resolve():
        raise ValueError("capture parent must be a non-symlink .codex/reviews directory")
    probe = parent / ".ask-ai-ignore-probe"
    ignored = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "-q", str(probe)],
        check=False,
    )
    if ignored.returncode != 0:
        raise ValueError(".codex/reviews is not ignored by Git")
    return repo, parent


def paths_for(parent: Path, review_id: str) -> dict[str, Path]:
    if not REVIEW_ID.fullmatch(review_id):
        raise ValueError("invalid review_id")
    return {
        "package": parent / f"{review_id}-package.md",
        "invocation": parent / f"{review_id}-invocation.json",
        "events": parent / f"{review_id}-events.jsonl",
        "response_partial": parent / f"{review_id}-response.partial.md",
        "response_final": parent / f"{review_id}-response.final.md",
    }


def append_event(path: Path, event: dict[str, object]) -> dict[str, object]:
    existing = path.read_bytes() if path.exists() else b""
    line = json.dumps(event, ensure_ascii=False, sort_keys=True).encode() + b"\n"
    atomic_write(path, existing + line)
    lines = [item for item in path.read_text(encoding="utf-8").splitlines() if item]
    if not lines or json.loads(lines[-1]) != event:
        raise ValueError("event readback mismatch")
    return read_receipt(path)


def prepare(args: argparse.Namespace) -> dict[str, object]:
    _, parent = verified_parent(args.repo)
    paths = paths_for(parent, args.review_id)
    package = paths["package"]
    if not package.is_file() or package.is_symlink():
        raise ValueError(f"frozen package missing: {package}")
    for role, path in paths.items():
        if role != "package" and path.exists():
            raise ValueError(f"capture artifact already exists: {path}")

    now = datetime.now(timezone.utc).isoformat()
    atomic_write(paths["response_partial"], b"")
    atomic_write(paths["response_final"], b"")
    event = {
        "actor": "primary-coordinator",
        "event_id": f"{args.operation_id}:prepared",
        "event_seq": 1,
        "operation_id": args.operation_id,
        "provider": args.provider,
        "state": "prepared",
        "timestamp": now,
    }
    append_event(paths["events"], event)
    artifact_receipts = {
        role: read_receipt(path)
        for role, path in paths.items()
        if role != "invocation"
    }
    invocation = {
        "schema_version": SCHEMA,
        "review_id": args.review_id,
        "operation_id": args.operation_id,
        "provider": args.provider,
        "state": "prepared",
        "prepared_at": now,
        "artifacts": artifact_receipts,
        "capture_requirement": {
            "atomic_write": "required",
            "complete": True,
            "readback_verified": True,
            "truncated": False,
        },
    }
    atomic_write(paths["invocation"], json_bytes(invocation))
    verified = json.loads(paths["invocation"].read_text(encoding="utf-8"))
    if verified["state"] != "prepared" or verified["operation_id"] != args.operation_id:
        raise ValueError("invocation readback mismatch")
    result_artifacts = dict(artifact_receipts)
    result_artifacts["invocation"] = read_receipt(paths["invocation"])
    return {"status": "prepared", "invocation": str(paths["invocation"]), "artifacts": result_artifacts}


def finalize(args: argparse.Namespace) -> dict[str, object]:
    _, parent = verified_parent(args.repo)
    paths = paths_for(parent, args.review_id)
    invocation = json.loads(paths["invocation"].read_text(encoding="utf-8"))
    if invocation.get("schema_version") != SCHEMA or invocation.get("state") != "prepared":
        raise ValueError("capture invocation is not prepared")
    if invocation.get("operation_id") != args.operation_id:
        raise ValueError("operation_id mismatch")
    if not args.conversation_id or not args.response_container_id:
        raise ValueError("stable conversation and response container IDs are required")
    content = paths["response_partial"].read_bytes()
    if not content:
        raise ValueError("response.partial is empty")
    text = content.decode("utf-8")
    atomic_write(paths["response_final"], content)
    final_readback = paths["response_final"].read_bytes()
    if final_readback != content:
        raise ValueError("response.final readback mismatch")
    content_sha = sha256_bytes(content)
    final_artifact = read_receipt(paths["response_final"])
    receipt = {
        "conversation_id": args.conversation_id,
        "response_container_id": args.response_container_id,
        "content": {
            "complete": True,
            "truncated": False,
            "character_count": len(text),
            "sha256": content_sha,
        },
        "artifact": {
            "path": final_artifact["path"],
            "bytes": final_artifact["bytes"],
            "file_sha256": final_artifact["sha256"],
            "atomic_write": "verified",
            "readback_verified": True,
        },
    }
    event = {
        "actor": "primary-coordinator",
        "event_id": f"{args.operation_id}:captured",
        "event_seq": 2,
        "operation_id": args.operation_id,
        "provider": invocation["provider"],
        "response_sha256": content_sha,
        "state": "captured",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    append_event(paths["events"], event)
    invocation["state"] = "captured"
    invocation["response_capture"] = receipt
    invocation["artifacts"]["events"] = read_receipt(paths["events"])
    invocation["artifacts"]["response_partial"] = read_receipt(paths["response_partial"])
    invocation["artifacts"]["response_final"] = read_receipt(paths["response_final"])
    atomic_write(paths["invocation"], json_bytes(invocation))
    verified = json.loads(paths["invocation"].read_text(encoding="utf-8"))
    if verified.get("response_capture") != receipt:
        raise ValueError("capture receipt readback mismatch")
    return {"status": "captured", "response_capture": receipt}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)
    prepare_parser = subcommands.add_parser("prepare")
    prepare_parser.add_argument("--repo", required=True)
    prepare_parser.add_argument("--review-id", required=True)
    prepare_parser.add_argument("--provider", required=True)
    prepare_parser.add_argument("--operation-id", required=True)
    finalize_parser = subcommands.add_parser("finalize")
    finalize_parser.add_argument("--repo", required=True)
    finalize_parser.add_argument("--review-id", required=True)
    finalize_parser.add_argument("--operation-id", required=True)
    finalize_parser.add_argument("--conversation-id", required=True)
    finalize_parser.add_argument("--response-container-id", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare(args) if args.command == "prepare" else finalize(args)
    except (OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "package-only", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
