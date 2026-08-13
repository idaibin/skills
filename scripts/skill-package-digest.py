#!/usr/bin/env python3
"""Print a deterministic digest for a sanitized Skill canary scope."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


DEFAULT_SCOPE = (
    "skills/ui-spec",
    "skills/ask-ai",
    "skills/dev-frontend",
    "skills/audit-frontend",
    "skills/repo-review",
    "skills/ops-browser",
    "skills/workspace-taskboard",
)
IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def included_file(path: Path) -> bool:
    return not (set(path.parts) & IGNORED_PARTS or path.suffix in IGNORED_SUFFIXES)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def digest_paths(root: Path, relative_paths: tuple[str, ...]) -> str:
    root = root.resolve()
    digest = hashlib.sha256()
    files: list[Path] = []
    for relative in relative_paths:
        path = (root / relative).resolve()
        path.relative_to(root)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(
                item for item in path.rglob("*")
                if item.is_file() and included_file(item)
            )
        else:
            raise FileNotFoundError(relative)
    for path in sorted(set(files), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=list(DEFAULT_SCOPE))
    args = parser.parse_args()
    print(digest_paths(repo_root(), tuple(args.paths)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
