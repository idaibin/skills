#!/usr/bin/env python3
"""Print a deterministic digest for a sanitized Skill canary scope."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def included_file(path: Path) -> bool:
    return not (set(path.parts) & IGNORED_PARTS or path.suffix in IGNORED_SUFFIXES)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def indexed_skill_scope(root: Path) -> tuple[str, ...]:
    payload = json.loads((root / "skills-index.json").read_text(encoding="utf-8"))
    names = tuple(package["name"] for package in payload["packages"])
    if len(names) != len(set(names)):
        raise ValueError("skills-index.json contains duplicate package names")
    return tuple(f"skills/{name}" for name in names)


DEFAULT_SCOPE = indexed_skill_scope(repo_root())


def included_files(root: Path, relative_paths: tuple[str, ...]) -> list[Path]:
    root = root.resolve()
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
    return sorted(set(files), key=lambda item: item.relative_to(root).as_posix())


def file_hashes(root: Path, relative_paths: tuple[str, ...]) -> dict[str, str]:
    root = root.resolve()
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in included_files(root, relative_paths)
    }


def digest_paths(root: Path, relative_paths: tuple[str, ...]) -> str:
    root = root.resolve()
    digest = hashlib.sha256()
    for path in included_files(root, relative_paths):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compare-root",
        type=Path,
        help="compare the selected package trees with another root, such as ~/.agents",
    )
    parser.add_argument("paths", nargs="*", default=list(DEFAULT_SCOPE))
    args = parser.parse_args()
    root = repo_root()
    selected = tuple(args.paths)
    print(digest_paths(root, selected))
    if args.compare_root is not None:
        source = file_hashes(root, selected)
        installed = file_hashes(args.compare_root, selected)
        missing = sorted(source.keys() - installed.keys())
        extra = sorted(installed.keys() - source.keys())
        changed = sorted(path for path in source.keys() & installed.keys() if source[path] != installed[path])
        if missing or extra or changed:
            print(json.dumps({"missing": missing, "extra": extra, "changed": changed}, ensure_ascii=False))
            return 1
        print(json.dumps({"status": "match", "packages": len(selected), "files": len(source)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
