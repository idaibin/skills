#!/usr/bin/env python3
"""Validate and sync repository skill packages into the local Codex skills directory."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


LEGACY_SKILL_NAMES = ("repo-context", "commit-reviewer", "planner")
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
LEGACY_RE = re.compile(
    r"(?<![A-Za-z0-9-])(" + "|".join(re.escape(name) for name in LEGACY_SKILL_NAMES) + r")(?![A-Za-z0-9-])"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EVAL_CASES_FILE = "eval-cases.md"
EVAL_REQUIRED_SECTIONS = (
    "## Trigger Eval",
    "## Non-Trigger Eval",
    "## Quality Eval",
    "## Scoring",
)


@dataclass(frozen=True)
class SkillPackage:
    name: str
    path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync all repository skill packages into the local Codex skills directory."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the sync; without this flag the command only prints the planned changes",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate selected source packages without copying or deleting",
    )
    parser.add_argument(
        "--check-target",
        action="store_true",
        help="with --validate-only, also validate matching installed packages in the target directory",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="sync only this skill name; may be provided multiple times",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target(),
        help="target skills directory; defaults to ${CODEX_HOME:-~/.codex}/skills",
    )
    args = parser.parse_args()
    if args.apply and args.validate_only:
        parser.error("--apply and --validate-only cannot be used together")
    if args.check_target and not args.validate_only:
        parser.error("--check-target requires --validate-only")
    return args


def discover_skills(skills_dir: Path) -> list[SkillPackage]:
    packages = []
    if not skills_dir.exists():
        return packages

    for child in sorted(skills_dir.iterdir(), key=lambda item: item.name):
        if child.is_dir() and (child / "SKILL.md").is_file():
            packages.append(SkillPackage(name=child.name, path=child))
    return packages


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0] != "---":
        return {}

    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return frontmatter
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return {}


def yaml_value_exists(yaml_text: str, key: str) -> bool:
    return re.search(rf"^\s*{re.escape(key)}\s*:\s*.+$", yaml_text, re.MULTILINE) is not None


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


def package_files(package_path: Path) -> list[Path]:
    return [path for path in package_path.rglob("*") if path.is_file()]


def validate_references(package_path: Path, skill_md_text: str, *, label: str) -> list[str]:
    errors: list[str] = []
    references_dir = package_path / "references"
    if not references_dir.is_dir():
        errors.append(f"{label}: missing references/")
        return errors

    reference_files = sorted(references_dir.glob("*.md"))
    if not reference_files:
        errors.append(f"{label}: missing references/*.md")
        return errors

    for nested_reference in sorted(references_dir.rglob("*.md")):
        if nested_reference.parent != references_dir:
            relative = nested_reference.relative_to(package_path)
            errors.append(f"{label}: reference files must be one level deep: {relative}")

    eval_cases = references_dir / EVAL_CASES_FILE
    if not eval_cases.is_file():
        errors.append(f"{label}: missing references/{EVAL_CASES_FILE}")
    else:
        eval_text = eval_cases.read_text(encoding="utf-8")
        for section in EVAL_REQUIRED_SECTIONS:
            if section not in eval_text:
                errors.append(f"{label}: references/{EVAL_CASES_FILE} missing section {section!r}")

    linked = markdown_links(skill_md_text)
    for reference_file in reference_files:
        expected_link = f"references/{reference_file.name}"
        if expected_link not in linked:
            errors.append(f"{label}: SKILL.md does not link {expected_link}")

    return errors


def validate_package(package: SkillPackage, *, label: str) -> list[str]:
    errors: list[str] = []
    package_path = package.path
    skill_md = package_path / "SKILL.md"
    openai_yaml = package_path / "agents" / "openai.yaml"
    skill_md_text = ""

    if not SKILL_NAME_RE.match(package.name):
        errors.append(f"{label}: invalid skill directory name: {package.name}")

    if not skill_md.is_file():
        errors.append(f"{label}: missing SKILL.md")
    else:
        skill_md_text = skill_md.read_text(encoding="utf-8")
        frontmatter = read_frontmatter(skill_md)
        actual_name = frontmatter.get("name")
        description = frontmatter.get("description", "")
        if actual_name != package.name:
            errors.append(f"{label}: SKILL.md name must be {package.name!r}, found {actual_name!r}")
        if not description.startswith("Use when"):
            errors.append(f"{label}: SKILL.md description must start with 'Use when'")

    if not openai_yaml.is_file():
        errors.append(f"{label}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        for key in ("display_name", "short_description", "default_prompt"):
            if not yaml_value_exists(yaml_text, key):
                errors.append(f"{label}: agents/openai.yaml missing {key}")
        if f"${package.name}" not in yaml_text:
            errors.append(f"{label}: agents/openai.yaml default prompt should mention ${package.name}")

    if not has_markdown_reference(package_path):
        errors.append(f"{label}: missing references/*.md")
    else:
        errors.extend(validate_references(package_path, skill_md_text, label=label))

    for forbidden in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        if (package_path / forbidden).exists():
            errors.append(f"{label}: package-local {forbidden} is not allowed")

    for file_path in package_files(package_path):
        if LEGACY_RE.search(file_path.read_text(encoding="utf-8", errors="ignore")):
            relative = file_path.relative_to(package_path)
            errors.append(f"{label}: stale legacy skill name found in {relative}")

    return errors


def validate_source_packages(packages: list[SkillPackage]) -> list[str]:
    errors: list[str] = []
    if not packages:
        errors.append("source: no skill packages found under skills/*/SKILL.md")
        return errors

    for package in packages:
        errors.extend(validate_package(package, label=f"source {package.name}"))
    return errors


def validate_target_packages(target_dir: Path, packages: list[SkillPackage]) -> list[str]:
    errors: list[str] = []
    if not target_dir.exists():
        errors.append(f"target: directory does not exist: {target_dir}")
        return errors

    for package in packages:
        target_package = SkillPackage(name=package.name, path=target_dir / package.name)
        if not target_package.path.exists():
            errors.append(f"target {package.name}: package is not installed")
            continue
        errors.extend(validate_package(target_package, label=f"target {package.name}"))

    for legacy_name in LEGACY_SKILL_NAMES:
        legacy_path = target_dir / legacy_name
        if legacy_path.exists():
            errors.append(f"target: legacy skill must be removed: {legacy_path}")

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


def ensure_safe_target(source_dir: Path, target_dir: Path) -> None:
    resolved_source = source_dir.resolve()
    resolved_target = target_dir.expanduser().resolve()
    if resolved_target == resolved_source:
        raise RuntimeError("target directory cannot be the repository skills/ source directory")
    if resolved_source in resolved_target.parents:
        raise RuntimeError("target directory cannot be inside the repository skills/ source directory")


def remove_path(path: Path, *, dry_run: bool) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if dry_run:
        print(f"would remove: {path}")
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    print(f"removed: {path}")


def copy_package(package: SkillPackage, target_dir: Path, *, dry_run: bool) -> None:
    target_package = target_dir / package.name
    if dry_run:
        print(f"would sync: {package.path} -> {target_package}")
        return

    remove_path(target_package, dry_run=False)
    shutil.copytree(package.path, target_package)
    print(f"synced: {package.path} -> {target_package}")


def sync_packages(packages: list[SkillPackage], target_dir: Path, *, dry_run: bool) -> None:
    if dry_run:
        if not target_dir.exists():
            print(f"would create target directory: {target_dir}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    for package in packages:
        copy_package(package, target_dir, dry_run=dry_run)

    for legacy_name in LEGACY_SKILL_NAMES:
        remove_path(target_dir / legacy_name, dry_run=dry_run)


def print_package_list(title: str, packages: list[SkillPackage]) -> None:
    print(title)
    for package in packages:
        print(f"  - {package.name}: {package.path}")


def main() -> int:
    args = parse_args()
    root = repo_root()
    source_dir = root / "skills"
    target_dir = args.target.expanduser()

    packages = discover_skills(source_dir)
    selected, missing = selected_packages(packages, args.skill)
    if missing:
        print(f"error: unknown skill(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    print_package_list("Discovered skill packages:", packages)

    source_errors = validate_source_packages(selected)
    if source_errors:
        for error in source_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.validate_only:
        if args.check_target:
            target_errors = validate_target_packages(target_dir, selected)
            if target_errors:
                for error in target_errors:
                    print(f"error: {error}", file=sys.stderr)
                return 1
            print(f"validated source and target packages: {target_dir}")
        else:
            print(f"validated source packages: {source_dir}")
        return 0

    ensure_safe_target(source_dir, target_dir)
    print_package_list("Selected for sync:", selected)
    sync_packages(selected, target_dir, dry_run=not args.apply)

    if args.apply:
        target_errors = validate_target_packages(target_dir, selected)
        if target_errors:
            for error in target_errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"validated synced packages: {target_dir}")
    else:
        print("dry-run only; pass --apply to write changes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
