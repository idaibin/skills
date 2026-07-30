#!/usr/bin/env python3
"""Synchronize self-contained skill copies from shared protocol sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROTOCOLS = {
    Path("protocols/frontend-visual-evidence-v1.md"): (
        Path("skills/ui-spec/references/frontend-visual-evidence.md"),
        Path("skills/dev-frontend/references/frontend-visual-evidence.md"),
        Path("skills/audit-frontend/references/frontend-visual-evidence.md"),
        Path("skills/repo-review/references/frontend-visual-evidence.md"),
        Path("skills/ops-browser/references/frontend-visual-evidence.md"),
    ),
    Path("protocols/frontend-visual-evidence-v1.schema.json"): (
        Path("skills/ui-spec/assets/frontend-visual-evidence.schema.json"),
        Path("skills/dev-frontend/assets/frontend-visual-evidence.schema.json"),
        Path("skills/audit-frontend/assets/frontend-visual-evidence.schema.json"),
        Path("skills/repo-review/assets/frontend-visual-evidence.schema.json"),
        Path("skills/ops-browser/assets/frontend-visual-evidence.schema.json"),
    ),
    Path("scripts/validate-frontend-visual-evidence.py"): (
        Path("skills/ui-spec/scripts/validate-frontend-visual-evidence.py"),
        Path("skills/dev-frontend/scripts/validate-frontend-visual-evidence.py"),
        Path("skills/audit-frontend/scripts/validate-frontend-visual-evidence.py"),
        Path("skills/repo-review/scripts/validate-frontend-visual-evidence.py"),
        Path("skills/ops-browser/scripts/validate-frontend-visual-evidence.py"),
    ),
    Path("protocols/frontend-layout-governance-v1.md"): (
        Path("skills/dev-frontend/references/frontend-layout-governance.md"),
        Path("skills/audit-frontend/references/frontend-layout-governance.md"),
    ),
    Path("protocols/specification-authorities-v1.md"): (
        Path("skills/dev-frontend/references/specification-authorities.md"),
        Path("skills/audit-frontend/references/specification-authorities.md"),
    ),
    Path("protocols/browser-operation-v1.md"): (
        Path("skills/ask-ai/references/browser-operation-protocol.md"),
        Path("skills/ops-browser/references/browser-operation-protocol.md"),
    ),
    Path("protocols/behavior-first-v1.md"): (
        Path("skills/dev-frontend/references/behavior-first.md"),
        Path("skills/dev-java/references/behavior-first.md"),
        Path("skills/dev-rust/references/behavior-first.md"),
    ),
    Path("protocols/codebase-design-v1.md"): (
        Path("skills/dev-frontend/references/codebase-design.md"),
        Path("skills/dev-java/references/codebase-design.md"),
        Path("skills/dev-rust/references/codebase-design.md"),
        Path("skills/audit-frontend/references/codebase-design.md"),
        Path("skills/audit-java/references/codebase-design.md"),
        Path("skills/audit-rust/references/codebase-design.md"),
        Path("skills/repo-review/references/codebase-design.md"),
    ),
    Path("protocols/code-quality-v1.md"): (
        Path("skills/dev-frontend/references/code-quality.md"),
        Path("skills/dev-java/references/code-quality.md"),
        Path("skills/dev-rust/references/code-quality.md"),
        Path("skills/audit-frontend/references/code-quality.md"),
        Path("skills/audit-java/references/code-quality.md"),
        Path("skills/audit-rust/references/code-quality.md"),
        Path("skills/repo-review/references/code-quality.md"),
    ),
    Path("protocols/java-engineering-v1.md"): (
        Path("skills/dev-java/references/java-engineering.md"),
        Path("skills/audit-java/references/java-engineering.md"),
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
