#!/usr/bin/env python3
"""Append one validated Ask AI feedback terminal event."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import sys


ALLOWED_EVENT_TYPES = {"review-attempt", "response-captured", "verification-update"}
REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "event_type",
    "timestamp",
    "feedback_id",
    "review_id",
    "round_id",
    "fixed_basis_hash",
    "provider",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | {
    "event_version",
    "surface",
    "route",
    "conversation_fingerprint",
    "completion_evidence",
    "model",
    "model_evidence",
    "reasoning",
    "task_theme",
    "primary_domain",
    "review_modes",
    "response_contract",
    "prompt_artifact_id",
    "prompt_artifact_hash",
    "prompt_artifact_size",
    "response_artifact_id",
    "response_artifact_hash",
    "completion_state",
    "instruction_adherence",
    "citation_state",
    "material_findings",
    "confirmed_findings",
    "rejected_findings",
    "duplicate_findings",
    "not_verified_gaps",
    "local_verdict",
    "decision_usefulness",
    "outcome",
    "summary",
    "prompt_hypothesis",
    "next_experiment",
}
FORBIDDEN_KEY_PARTS = {"raw", "content", "secret", "token", "email", "url", "path"}
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def load_config(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    values: dict[str, object] = {}
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, raw_value = (part.strip() for part in line.split(":", 1))
        if raw_value.lower() in {"true", "false"}:
            values[key] = raw_value.lower() == "true"
        else:
            values[key] = raw_value.strip('"\'')
    if values.get("schema_version") != "ask-ai-feedback/v1":
        raise ValueError("unsupported feedback config schema")
    if values.get("enabled") is not True:
        raise ValueError("feedback is not enabled")
    round_log = values.get("round_log")
    if not isinstance(round_log, str) or not round_log:
        raise ValueError("round_log is required")
    return values


def validate_event(event: object) -> dict:
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    missing = REQUIRED_FIELDS - event.keys()
    unknown = event.keys() - ALLOWED_FIELDS
    if missing:
        raise ValueError(f"missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
    if event["schema_version"] != "ask-ai-feedback/v1":
        raise ValueError("unsupported event schema")
    if event["event_type"] not in ALLOWED_EVENT_TYPES:
        raise ValueError("unsupported event type")
    if not HEX_64.fullmatch(str(event["fixed_basis_hash"])):
        raise ValueError("fixed_basis_hash must be lowercase SHA-256")
    for key, value in event.items():
        lowered = key.lower().replace("-", "_").split("_")
        if FORBIDDEN_KEY_PARTS.intersection(lowered):
            raise ValueError(f"forbidden metadata field: {key}")
        values = value if isinstance(value, list) else [value]
        for item in values:
            if isinstance(item, str):
                if len(item) > 240 or "\n" in item or "\r" in item:
                    raise ValueError(f"unsafe text value: {key}")
                if item.startswith(("/", "~", "file:", "http:", "https:")):
                    raise ValueError(f"path or URL value forbidden: {key}")
    return event


def append_event(log_path: Path, event: dict) -> None:
    log_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = log_path.with_suffix(log_path.suffix + ".lock")
    encoded = (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if log_path.exists():
            with log_path.open(encoding="utf-8") as existing:
                for line in existing:
                    if json.loads(line).get("event_id") == event["event_id"]:
                        raise ValueError("duplicate event_id")
        descriptor = os.open(log_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            remaining = memoryview(encoded)
            while remaining:
                written = os.write(descriptor, remaining)
                if written == 0:
                    raise OSError("feedback append made no progress")
                remaining = remaining[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        with log_path.open("rb") as recorded:
            recorded.seek(-len(encoded), os.SEEK_END)
            if recorded.read() != encoded:
                raise OSError("feedback append readback mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--event-file", required=True, type=Path)
    args = parser.parse_args()
    try:
        config = load_config(args.config.expanduser())
        event = validate_event(json.loads(args.event_file.read_text(encoding="utf-8")))
        append_event(Path(str(config["round_log"])).expanduser(), event)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"feedback-deferred: {error}", file=sys.stderr)
        return 1
    print(f"feedback-recorded: {event['event_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
