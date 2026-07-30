#!/usr/bin/env python3
"""Validate the catalog against the portable Agent Skills and OpenAI surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CATALOG_ROW_RE = re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)
INSTALL_PATH_RE = re.compile(r"^- `skills/([a-z0-9-]+)`$", re.MULTILINE)
ROUTE_RE = re.compile(r"\$([a-z][a-z0-9-]*)")
EVAL_HEADINGS = ("## Trigger Eval", "## Non-Trigger Eval", "## Quality Eval")
FENCE_RE = re.compile(r"^(?P<indent>[ ]{0,3})(?P<fence>`{3,}|~{3,})(?P<rest>.*)$")
HEADING_RE = re.compile(r"^(?P<indent>[ ]{0,3})##\s+(?P<title>.*?)\s*$")
FORBIDDEN_PACKAGE_FILES = {"README.md", "INSTALL.md", "INSTALLATION_GUIDE.md", "CHANGELOG.md"}
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LONG_REFERENCE_LINES = 100


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


def openai_invocation_policy(path: Path) -> bool | None:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("top-level mapping is required")
    if "policy" not in payload:
        return None
    policy = payload["policy"]
    if not isinstance(policy, dict):
        raise ValueError("top-level policy must be a mapping")
    if "allow_implicit_invocation" not in policy:
        return None
    value = policy["allow_implicit_invocation"]
    if not isinstance(value, bool):
        raise ValueError("policy.allow_implicit_invocation must be a boolean")
    return value


def section_has_content(text: str, heading: str) -> bool:
    lines = text.splitlines()
    in_code_fence = False
    fence_char: str = ""
    fence_len: int = 0
    start = None
    for i, line in enumerate(lines):
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _heading_matches(line, heading):
            start = i
            break
    if start is None:
        return False

    for line in lines[start + 1 :]:
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _is_h2_heading(line):
            return False
        if line.strip():
            return True
    return False


def has_exact_h2_heading(text: str, heading: str) -> bool:
    in_code_fence = False
    fence_char: str = ""
    fence_len: int = 0
    for line in text.splitlines():
        in_code_fence, fence_char, fence_len = _update_fence_state(
            line, in_code_fence, fence_char, fence_len
        )
        if in_code_fence:
            continue
        if _heading_matches(line, heading):
            return True
    return False


def _is_h2_heading(line: str) -> bool:
    return _heading_match(line) is not None


def _heading_match(line: str) -> str | None:
    match = HEADING_RE.match(line)
    if match is None:
        return None
    return f"## {match.group('title').strip()}"


def _heading_matches(line: str, heading: str) -> bool:
    match = _heading_match(line)
    return match is not None and match == heading


def _update_fence_state(
    line: str, in_code_fence: bool, fence_char: str, fence_len: int
) -> tuple[bool, str, int]:
    match = FENCE_RE.match(line)
    if match is None:
        return in_code_fence, fence_char, fence_len
    marker = match.group("fence")
    rest = match.group("rest").strip()
    if not in_code_fence:
        return True, marker[0], len(marker)
    if marker[0] != fence_char or len(marker) < fence_len:
        return in_code_fence, fence_char, fence_len
    if rest == "":
        return False, "", 0
    return in_code_fence, fence_char, fence_len


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
    unknown_fields = set(metadata) - PORTABLE_FIELDS
    if unknown_fields:
        errors.append(f"{package.name}: unsupported frontmatter fields: {sorted(unknown_fields)}")
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
    license_value = metadata.get("license")
    if license_value is not None and (not isinstance(license_value, str) or not license_value.strip()):
        errors.append(f"{package.name}: license must be a non-empty string when provided")
    compatibility = metadata.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not compatibility.strip() or len(compatibility) > 500
    ):
        errors.append(f"{package.name}: compatibility must be a string with 1-500 characters")
    portable_metadata = metadata.get("metadata")
    if portable_metadata is not None and (
        not isinstance(portable_metadata, dict)
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in portable_metadata.items())
    ):
        errors.append(f"{package.name}: metadata must map strings to strings")
    allowed_tools = metadata.get("allowed-tools")
    if allowed_tools is not None and (
        not isinstance(allowed_tools, str) or not allowed_tools.strip()
    ):
        errors.append(f"{package.name}: allowed-tools must be a non-empty string when provided")
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
            reference_text = reference.read_text(encoding="utf-8")
            if len(reference_text.splitlines()) > LONG_REFERENCE_LINES and not has_exact_h2_heading(
                reference_text, "## Contents"
            ):
                errors.append(
                    f"{package.name}: long reference needs a ## Contents section: {relative}"
                )
    else:
        errors.append(f"{package.name}: missing references directory")

    eval_file = references / "eval-cases.md"
    if not eval_file.is_file():
        errors.append(f"{package.name}: missing references/eval-cases.md")
    else:
        eval_text = eval_file.read_text(encoding="utf-8")
        for heading in EVAL_HEADINGS:
            if not has_exact_h2_heading(eval_text, heading):
                errors.append(f"{package.name}: eval-cases.md missing {heading}")
            elif not section_has_content(eval_text, heading):
                errors.append(f"{package.name}: eval-cases.md has empty {heading}")

    openai_file = package / "agents" / "openai.yaml"
    if not openai_file.is_file():
        errors.append(f"{package.name}: missing agents/openai.yaml for OpenAI discovery")
    else:
        try:
            interface = openai_interface(openai_file)
            openai_invocation_policy(openai_file)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            errors.append(f"{package.name}: openai.yaml {error}")
            interface = {}
        for field in ("display_name", "short_description", "default_prompt"):
            if not interface.get(field):
                errors.append(f"{package.name}: openai.yaml missing interface.{field}")
        short_description = interface.get("short_description", "")
        if short_description and not 25 <= len(short_description) <= 64:
            errors.append(
                f"{package.name}: openai.yaml interface.short_description must be 25-64 characters"
            )
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


def skill_index_errors(root: Path, names: set[str]) -> list[str]:
    errors: list[str] = []
    index_path = root / "skills-index.json"
    schema_path = root / "docs" / "skills" / "skills-index.schema.json"
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"skills-index.json: cannot load index and schema: {error}"]

    schema_errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    for error in schema_errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"skills-index.json: {location}: {error.message}")
    if schema_errors:
        return errors

    entries = payload["skills"]
    indexed_names = [entry["name"] for entry in entries]
    if len(indexed_names) != len(set(indexed_names)):
        errors.append("skills-index.json: duplicate Skill names")
    if set(indexed_names) != names:
        errors.append(
            "skills-index.json package set differs: "
            f"expected {sorted(names)}, found {sorted(set(indexed_names))}"
        )

    categories = set(payload["categories"])
    used_categories: set[str] = set()
    for entry in entries:
        name = entry["name"]
        category = entry["category"]
        used_categories.add(category)
        if category not in categories:
            errors.append(f"skills-index.json: {name} references unknown category {category}")
        related = set(entry["related"])
        if name in related:
            errors.append(f"skills-index.json: {name} cannot relate to itself")
        unknown_related = related - names
        if unknown_related:
            errors.append(
                f"skills-index.json: {name} references unknown related Skills "
                f"{sorted(unknown_related)}"
            )
    unused_categories = categories - used_categories
    if unused_categories:
        errors.append(f"skills-index.json: unused categories {sorted(unused_categories)}")

    try:
        distribution = json.loads((root / "skills.sh.json").read_text(encoding="utf-8"))
        groupings = distribution["groupings"]
        grouped_by_title = {grouping["title"]: set(grouping["skills"]) for grouping in groupings}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        errors.append(f"skills-index.json: cannot compare distribution groups: {error}")
        return errors

    category_titles = {
        category: details["title"] for category, details in payload["categories"].items()
    }
    if len(grouped_by_title) != len(groupings):
        errors.append("skills.sh.json: duplicate grouping titles")
    if len(set(category_titles.values())) != len(category_titles):
        errors.append("skills-index.json: duplicate category titles")
    if set(category_titles.values()) != set(grouped_by_title):
        errors.append(
            "skills-index.json category titles differ from skills.sh.json groups: "
            f"expected {sorted(grouped_by_title)}, found {sorted(category_titles.values())}"
        )
    for category, title in category_titles.items():
        expected = {entry["name"] for entry in entries if entry["category"] == category}
        found = grouped_by_title.get(title)
        if found is not None and found != expected:
            errors.append(
                f"skills-index.json category {category} differs from distribution group "
                f"{title}: expected {sorted(expected)}, found {sorted(found)}"
            )
    return errors


def validate(root: Path) -> list[str]:
    skills = root / "skills"
    packages = sorted(path for path in skills.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    names = {path.name for path in packages}
    errors = catalog_errors(root, names)
    errors.extend(skill_index_errors(root, names))
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
