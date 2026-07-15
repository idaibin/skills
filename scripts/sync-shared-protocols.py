#!/usr/bin/env python3
"""Synchronize self-contained skill copies from shared protocol sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROTOCOLS = {
    Path("protocols/browser-operation-v1.md"): (
        Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
        Path("skills/ops-browser/references/browser-operation-protocol.md"),
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize shared protocols into published skill packages."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale generated copies without writing files",
    )
    return parser.parse_args()


def synchronize(root: Path, *, check: bool) -> list[str]:
    stale: list[str] = []
    for source_relative, targets in PROTOCOLS.items():
        source = root / source_relative
        content = source.read_text(encoding="utf-8")
        for target_relative in targets:
            target = root / target_relative
            current = target.read_text(encoding="utf-8") if target.is_file() else None
            if current == content:
                continue
            stale.append(str(target_relative))
            if not check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
    return stale


def main() -> int:
    args = parse_args()
    stale = synchronize(repo_root(), check=args.check)
    if args.check and stale:
        for path in stale:
            print(f"stale generated protocol: {path}", file=sys.stderr)
        print(
            "run python3 scripts/sync-shared-protocols.py to refresh generated copies",
            file=sys.stderr,
        )
        return 1
    if stale:
        for path in stale:
            print(f"updated generated protocol: {path}")
    else:
        print("shared protocol copies are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
