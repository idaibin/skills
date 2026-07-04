#!/usr/bin/env python3
"""Validate repository skill packages."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LEGACY_SKILL_NAMES = ("repo-context", "commit-reviewer", "planner")
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
LEGACY_RE = re.compile(
    r"(?<![A-Za-z0-9_-])("
    + "|".join(re.escape(name) for name in LEGACY_SKILL_NAMES)
    + r")(?![A-Za-z0-9_-])"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EVAL_CASES_FILE = "eval-cases.md"
EVAL_REQUIRED_SECTIONS = (
    "## Trigger Eval",
    "## Non-Trigger Eval",
    "## Quality Eval",
    "## Scoring",
)
FORBIDDEN_DESCRIPTION_PHRASES = ("Triggers include",)
MAX_DESCRIPTION_CHARS = 500


@dataclass(frozen=True)
class SkillPackage:
    name: str
    path: Path


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
    return parser.parse_args()


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


def frontmatter_yaml_string_errors(skill_md: Path) -> list[str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0] != "---":
        return []

    errors: list[str] = []
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if not value:
            continue
        is_quoted = (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        )
        if not is_quoted and ": " in value:
            errors.append(
                f"{key.strip()}: quote frontmatter string values that contain ': '"
            )
    return errors


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
        for frontmatter_error in frontmatter_yaml_string_errors(skill_md):
            errors.append(f"{label}: SKILL.md {frontmatter_error}")
        frontmatter = read_frontmatter(skill_md)
        actual_name = frontmatter.get("name")
        description = frontmatter.get("description", "")
        if actual_name != package.name:
            errors.append(f"{label}: SKILL.md name must be {package.name!r}, found {actual_name!r}")
        if not description.startswith("Use when"):
            errors.append(f"{label}: SKILL.md description must start with 'Use when'")
        if len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{label}: SKILL.md description must be {MAX_DESCRIPTION_CHARS} characters or fewer"
            )
        for phrase in FORBIDDEN_DESCRIPTION_PHRASES:
            if phrase in description:
                errors.append(f"{label}: SKILL.md description must not contain {phrase!r}")

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

    source_errors = validate_source_packages(selected)
    if source_errors:
        for error in source_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"validated source packages: {source_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
