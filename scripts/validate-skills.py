#!/usr/bin/env python3
"""Validate the catalog against the portable Agent Skills and OpenAI surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CATALOG_ROW_RE = re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)
INSTALL_PATH_RE = re.compile(r"^- `skills/([a-z0-9-]+)`$", re.MULTILINE)
ROUTE_RE = re.compile(r"\$([a-z][a-z0-9-]*)")
EVAL_HEADINGS = ("## Trigger Eval", "## Non-Trigger Eval", "## Quality Eval")
FORBIDDEN_PACKAGE_FILES = {"README.md", "INSTALL.md", "INSTALLATION_GUIDE.md", "CHANGELOG.md"}


def frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if match is None:
        raise ValueError("missing or invalid YAML frontmatter delimiters")
    try:
        values = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(values, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return values, text[match.end() :]


def openai_interface(path: Path) -> dict[str, str]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("interface"), dict):
        raise ValueError("top-level interface mapping is required")
    interface = payload["interface"]
    return {
        field: value
        for field in ("display_name", "short_description", "default_prompt")
        if isinstance((value := interface.get(field)), str)
    }


def local_link_errors(markdown: Path, package: Path) -> list[str]:
    errors: list[str] = []
    text = markdown.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        target = target.strip().strip("<>").split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target):
            continue
        resolved = (markdown.parent / target).resolve()
        try:
            resolved.relative_to(package.resolve())
        except ValueError:
            errors.append(f"{markdown.relative_to(package)}: link escapes package: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{markdown.relative_to(package)}: broken link: {target}")
    return errors


def package_errors(package: Path, all_names: set[str]) -> list[str]:
    errors: list[str] = []
    skill_file = package / "SKILL.md"
    if not skill_file.is_file():
        return [f"{package.name}: missing SKILL.md"]

    try:
        metadata, body = frontmatter(skill_file)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        return [f"{package.name}: {error}"]

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != package.name:
        errors.append(f"{package.name}: frontmatter name must match directory")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"{package.name}: name must be 1-64 lowercase letters, digits, or hyphens")
    if (
        not isinstance(description, str)
        or not description
        or len(description) > 1024
        or re.search(r"<[^>]+>", description)
    ):
        errors.append(f"{package.name}: description must be plain text with 1-1024 characters")
    elif "Use when" not in description:
        errors.append(f"{package.name}: description must state when to use the Skill")
    if len(body.splitlines()) > 500:
        errors.append(f"{package.name}: SKILL.md body exceeds the recommended 500 lines")

    for forbidden in FORBIDDEN_PACKAGE_FILES:
        if (package / forbidden).exists():
            errors.append(f"{package.name}: remove package-local {forbidden}")

    references = package / "references"
    if references.is_dir():
        nested = [path for path in references.rglob("*") if path.is_file() and path.parent != references]
        for path in nested:
            errors.append(f"{package.name}: references must stay one level deep: {path.relative_to(package)}")
        linked = {
            target.strip().strip("<>").split("#", 1)[0]
            for target in LINK_RE.findall(skill_file.read_text(encoding="utf-8"))
            if target.startswith("references/")
        }
        for reference in sorted(references.glob("*.md")):
            relative = reference.relative_to(package).as_posix()
            if relative not in linked:
                errors.append(f"{package.name}: reference is not linked from SKILL.md: {relative}")
    else:
        errors.append(f"{package.name}: missing references directory")

    eval_file = references / "eval-cases.md"
    if not eval_file.is_file():
        errors.append(f"{package.name}: missing references/eval-cases.md")
    else:
        eval_text = eval_file.read_text(encoding="utf-8")
        for heading in EVAL_HEADINGS:
            if heading not in eval_text:
                errors.append(f"{package.name}: eval-cases.md missing {heading}")

    openai_file = package / "agents" / "openai.yaml"
    if not openai_file.is_file():
        errors.append(f"{package.name}: missing agents/openai.yaml for OpenAI discovery")
    else:
        try:
            interface = openai_interface(openai_file)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            errors.append(f"{package.name}: openai.yaml {error}")
            interface = {}
        for field in ("display_name", "short_description", "default_prompt"):
            if not interface.get(field):
                errors.append(f"{package.name}: openai.yaml missing interface.{field}")
        prompt = interface.get("default_prompt", "")
        if f"${package.name}" not in prompt:
            errors.append(f"{package.name}: default_prompt must route through ${package.name}")
        for route in ROUTE_RE.findall(prompt):
            if route not in all_names:
                errors.append(f"{package.name}: default_prompt references unknown Skill ${route}")

    for markdown in package.rglob("*.md"):
        errors.extend(f"{package.name}: {error}" for error in local_link_errors(markdown, package))
        if "npx skills" in markdown.read_text(encoding="utf-8"):
            errors.append(f"{package.name}: installation commands belong in root documentation")
    return errors


def catalog_errors(root: Path, names: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads((root / "skills.sh.json").read_text(encoding="utf-8"))
        listed = {
            skill
            for grouping in payload.get("groupings", [])
            for skill in grouping.get("skills", [])
        }
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError) as error:
        errors.append(f"skills.sh.json: invalid catalog: {error}")
        listed = set()
    if listed != names:
        errors.append(f"skills.sh.json package set differs: expected {sorted(names)}, found {sorted(listed)}")

    for filename, pattern in (("README.md", CATALOG_ROW_RE), ("INSTALL.md", INSTALL_PATH_RE)):
        try:
            found = set(pattern.findall((root / filename).read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"{filename}: cannot read catalog: {error}")
            continue
        if found != names:
            errors.append(f"{filename} package set differs: expected {sorted(names)}, found {sorted(found)}")
    return errors


def validate(root: Path) -> list[str]:
    skills = root / "skills"
    packages = sorted(path for path in skills.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    names = {path.name for path in packages}
    errors = catalog_errors(root, names)
    for package in packages:
        errors.extend(package_errors(package, names))
    if not packages:
        errors.append("no Skill packages found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    count = len(list((args.root / "skills").glob("*/SKILL.md")))
    print(f"validated {count} Skill packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
