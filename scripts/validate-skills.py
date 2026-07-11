#!/usr/bin/env python3
"""Validate repository skill packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LEGACY_SKILL_NAMES = (
    "repo-context",
    "commit-reviewer",
    "planner",
    "frontend-implementation",
    "frontend-governance",
    "rust-engineering-governance",
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
LEGACY_RE = re.compile(
    r"(?<![A-Za-z0-9_-])("
    + "|".join(re.escape(name) for name in LEGACY_SKILL_NAMES)
    + r")(?![A-Za-z0-9_-])"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_INVOCATION_RE = re.compile(r"(?<![A-Za-z0-9_.])\$([a-z][a-z0-9-]*)")
EVAL_CASES_FILE = "eval-cases.md"
EVAL_REQUIRED_SECTIONS = (
    "## Trigger Eval",
    "## Non-Trigger Eval",
    "## Quality Eval",
    "## Scoring",
)
FORBIDDEN_DESCRIPTION_PHRASES = ("Triggers include",)
MAX_DESCRIPTION_CHARS = 500
MAX_SKILL_LINES = 500
MAX_SHORT_DESCRIPTION_CHARS = 120
MAX_DEFAULT_PROMPT_CHARS = 800
MIN_TRIGGER_CASES = 3
MIN_NON_TRIGGER_CASES = 3
MIN_QUALITY_CASES = 4
AUDIT_RUST_SCENARIO_FIELDS = (
    "Input",
    "Investigate",
    "Correct",
    "Reject",
    "Acceptable scope",
    "Validation",
    "Final report",
)
REQUIRED_SKILL_SECTIONS = (
    "## Overview",
    "## Do Not Use For",
    "## Hard Rules",
    "## Output Contract",
    "## References",
)
PLACEHOLDER_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:TODO|TBD|FIXME|PLACEHOLDER)(?:\s*:|\s*$)",
    re.MULTILINE,
)
TEXT_FILE_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".sh", ".json", ".toml", ".txt"}


@dataclass(frozen=True)
class SkillPackage:
    name: str
    path: Path


@dataclass(frozen=True)
class QualityMetrics:
    description_chars: int
    skill_lines: int
    trigger_cases: int
    non_trigger_cases: int
    quality_cases: int


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
    parser.add_argument(
        "--quality-report",
        action="store_true",
        help="print description, entrypoint, and eval coverage metrics",
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


def validate_repository_indexes(root: Path, packages: list[SkillPackage]) -> list[str]:
    errors: list[str] = []
    expected = {package.name for package in packages}

    skills_index = root / "skills.sh.json"
    try:
        payload = json.loads(skills_index.read_text(encoding="utf-8"))
        indexed_names = [
            name
            for grouping in payload.get("groupings", [])
            for name in grouping.get("skills", [])
        ]
    except (OSError, json.JSONDecodeError, AttributeError) as error:
        errors.append(f"repository: cannot read skills.sh.json: {error}")
    else:
        if len(indexed_names) != len(set(indexed_names)):
            errors.append("repository: skills.sh.json contains duplicate skill names")
        indexed = set(indexed_names)
        for name in sorted(expected - indexed):
            errors.append(f"repository: skills.sh.json missing skill {name}")
        for name in sorted(indexed - expected):
            errors.append(f"repository: skills.sh.json lists unknown skill {name}")

    index_specs = (
        (root / "README.md", re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)),
        (root / "INSTALL.md", re.compile(r"^- `skills/([a-z0-9-]+)`$", re.MULTILINE)),
    )
    for path, pattern in index_specs:
        try:
            listed = set(pattern.findall(path.read_text(encoding="utf-8")))
        except OSError as error:
            errors.append(f"repository: cannot read {path.name}: {error}")
            continue
        for name in sorted(expected - listed):
            errors.append(f"repository: {path.name} missing skill {name}")
        for name in sorted(listed - expected):
            errors.append(f"repository: {path.name} lists unknown skill {name}")

    return errors


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


def yaml_scalar(yaml_text: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.+)$", yaml_text, re.MULTILINE)
    if match is None:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


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


def markdown_table_rows(markdown_text: str, section: str) -> list[list[str]]:
    start = markdown_text.find(section)
    if start < 0:
        return []
    body_start = start + len(section)
    next_section = markdown_text.find("\n## ", body_start)
    body = markdown_text[body_start:] if next_section < 0 else markdown_text[body_start:next_section]
    table_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table_lines[2:]
    ]


def normalized_eval_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`")).casefold()


def missing_table_cases(
    eval_text: str, section: str, required_cases: tuple[str, ...]
) -> list[str]:
    rows = markdown_table_rows(eval_text, section)
    keys = {normalized_eval_key(row[0]) for row in rows if row}
    return [case for case in required_cases if normalized_eval_key(case) not in keys]


def validate_specialized_eval_contracts(
    skill_name: str, eval_text: str, *, label: str
) -> list[str]:
    """Validate high-risk package contracts that generic table checks cannot prove."""

    errors: list[str] = []
    if skill_name == "implement-rust":
        section = "## Overlay Selection Eval"
        if section not in eval_text:
            errors.append(f"{label}: missing specialized section {section!r}")
        else:
            rows = markdown_table_rows(eval_text, section)
            keys = [normalized_eval_key(row[0]) for row in rows if row]
            required_prefixes = (
                "routine:",
                "contract:",
                "sqlite:",
                "ffi:",
                "ffi + sqlite:",
                "target-only:",
            )
            for prefix in required_prefixes:
                if not any(key.startswith(prefix) for key in keys):
                    errors.append(
                        f"{label}: {section} missing required case prefix {prefix!r}"
                    )

    elif skill_name == "audit-rust":
        profile_section = "## Profile Selection Eval"
        if profile_section not in eval_text:
            errors.append(f"{label}: missing specialized section {profile_section!r}")
        else:
            profile_start = eval_text.find(profile_section)
            profile_end = eval_text.find("\n## ", profile_start + len(profile_section))
            profile_text = (
                eval_text[profile_start:]
                if profile_end < 0
                else eval_text[profile_start:profile_end]
            )
            for term in (
                "Architecture/baseline",
                "SQLite",
                "Concurrency/runtime",
                "Unsafe/FFI",
            ):
                if term not in profile_text:
                    errors.append(
                        f"{label}: {profile_section} missing required profile case {term!r}"
                    )
            if "Out of scope" not in profile_text:
                errors.append(
                    f"{label}: {profile_section} must require unselected profiles to be 'Out of scope'"
                )

        scenario_start = eval_text.find("## Scenario Eval")
        scenario_end = eval_text.find("\n## Quality Eval", scenario_start)
        if scenario_start < 0 or scenario_end < 0:
            errors.append(f"{label}: missing complete specialized section '## Scenario Eval'")
        else:
            scenario_text = eval_text[scenario_start:scenario_end]
            matches = list(re.finditer(r"^###\s+(\d+)\.\s+.+$", scenario_text, re.MULTILINE))
            if len(matches) != 22:
                errors.append(
                    f"{label}: audit-rust Scenario Eval must contain exactly 22 scenarios"
                )
            for index, match in enumerate(matches):
                block_end = (
                    matches[index + 1].start()
                    if index + 1 < len(matches)
                    else len(scenario_text)
                )
                block = scenario_text[match.start():block_end]
                number = match.group(1)
                for field in AUDIT_RUST_SCENARIO_FIELDS:
                    if f"**{field}:**" not in block:
                        errors.append(
                            f"{label}: audit-rust scenario {number} missing field {field!r}"
                        )

    elif skill_name == "chatgpt-review-bridge":
        required = (
            "Package artifact",
            "Split package artifact",
            "Multipart send sequence",
            "External authorization",
            "Response completion",
            "Review artifact visibility",
            "Local verification",
        )
        for case in missing_table_cases(eval_text, "## Quality Eval", required):
            errors.append(
                f"{label}: chatgpt-review-bridge Quality Eval missing required case {case!r}"
            )

    elif skill_name == "audit-frontend":
        scenario_rows = markdown_table_rows(eval_text, "## Scenario Eval")
        scenario_text = "\n".join(" | ".join(row) for row in scenario_rows)
        if len(scenario_rows) < 16:
            errors.append(
                f"{label}: audit-frontend Scenario Eval must contain at least 16 cases"
            )
        for term in ("Vue Composition API", "Pure Options API", "`code-review` delegates"):
            if term not in scenario_text:
                errors.append(
                    f"{label}: audit-frontend Scenario Eval missing required case {term!r}"
                )
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Framework profile", "Vue API-style fidelity", "Read-only boundary"),
        ):
            errors.append(
                f"{label}: audit-frontend Quality Eval missing required case {case!r}"
            )

    return errors


def package_files(package_path: Path) -> list[Path]:
    return [path for path in package_path.rglob("*") if path.is_file()]


def validate_local_links(package_path: Path, *, label: str) -> list[str]:
    errors: list[str] = []
    for markdown_file in sorted(package_path.rglob("*.md")):
        markdown_text = markdown_file.read_text(encoding="utf-8")
        for link in sorted(markdown_links(markdown_text)):
            target = (markdown_file.parent / link).resolve()
            try:
                target.relative_to(package_path.resolve())
            except ValueError:
                errors.append(f"{label}: link escapes skill package: {markdown_file.name} -> {link}")
                continue
            if not target.exists():
                relative = markdown_file.relative_to(package_path)
                errors.append(f"{label}: broken local link in {relative}: {link}")
    return errors


def validate_eval_cases(
    eval_cases: Path, *, label: str, skill_name: str | None = None
) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    eval_text = eval_cases.read_text(encoding="utf-8")
    trigger_rows = markdown_table_rows(eval_text, "## Trigger Eval")
    non_trigger_rows = markdown_table_rows(eval_text, "## Non-Trigger Eval")
    quality_rows = markdown_table_rows(eval_text, "## Quality Eval")

    minimums = (
        ("trigger", trigger_rows, MIN_TRIGGER_CASES, 2),
        ("non-trigger", non_trigger_rows, MIN_NON_TRIGGER_CASES, 2),
        ("quality", quality_rows, MIN_QUALITY_CASES, 3),
    )
    for name, rows, minimum, columns in minimums:
        if len(rows) < minimum:
            errors.append(f"{label}: eval {name} cases must contain at least {minimum} rows")
        for index, row in enumerate(rows, start=1):
            if len(row) < columns or any(not cell for cell in row[:columns]):
                errors.append(f"{label}: eval {name} row {index} must contain {columns} non-empty columns")

    for name, rows in (("trigger", trigger_rows), ("non-trigger", non_trigger_rows), ("quality", quality_rows)):
        keys = [normalized_eval_key(row[0]) for row in rows if row]
        if len(keys) != len(set(keys)):
            errors.append(f"{label}: eval {name} cases contain duplicate first-column values")

    scoring_start = eval_text.find("## Scoring")
    scoring = eval_text[scoring_start:] if scoring_start >= 0 else ""
    if "Minimum pass:" not in scoring or not re.search(r"scores? at least (?:[7-9]|10)", scoring):
        errors.append(f"{label}: scoring must define a minimum quality score of at least 7")

    if skill_name is not None:
        errors.extend(
            validate_specialized_eval_contracts(skill_name, eval_text, label=label)
        )

    metrics = QualityMetrics(
        description_chars=0,
        skill_lines=0,
        trigger_cases=len(trigger_rows),
        non_trigger_cases=len(non_trigger_rows),
        quality_cases=len(quality_rows),
    )
    return errors, metrics


def validate_references(package_path: Path, skill_md_text: str, *, label: str) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    metrics: QualityMetrics | None = None
    references_dir = package_path / "references"
    if not references_dir.is_dir():
        errors.append(f"{label}: missing references/")
        return errors, metrics

    reference_files = sorted(references_dir.glob("*.md"))
    if not reference_files:
        errors.append(f"{label}: missing references/*.md")
        return errors, metrics

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
        eval_errors, metrics = validate_eval_cases(
            eval_cases, label=label, skill_name=package_path.name
        )
        errors.extend(eval_errors)

    linked = markdown_links(skill_md_text)
    for reference_file in reference_files:
        expected_link = f"references/{reference_file.name}"
        if expected_link not in linked:
            errors.append(f"{label}: SKILL.md does not link {expected_link}")

    errors.extend(validate_local_links(package_path, label=label))
    return errors, metrics


def validate_package(package: SkillPackage, *, label: str) -> tuple[list[str], QualityMetrics | None]:
    errors: list[str] = []
    metrics: QualityMetrics | None = None
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
        skill_lines = len(skill_md_text.splitlines())
        if skill_lines > MAX_SKILL_LINES:
            errors.append(f"{label}: SKILL.md must be {MAX_SKILL_LINES} lines or fewer")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in skill_md_text:
                errors.append(f"{label}: SKILL.md missing section {section!r}")
        if "## Workflow" not in skill_md_text and "## Modes" not in skill_md_text:
            errors.append(f"{label}: SKILL.md must include Workflow or Modes")
        if "## Maintenance" not in skill_md_text and "## Skill Maintenance" not in skill_md_text:
            errors.append(f"{label}: SKILL.md must include Maintenance")

    if not openai_yaml.is_file():
        errors.append(f"{label}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        for key in ("display_name", "short_description", "default_prompt"):
            if not yaml_value_exists(yaml_text, key):
                errors.append(f"{label}: agents/openai.yaml missing {key}")
        if f"${package.name}" not in yaml_text:
            errors.append(f"{label}: agents/openai.yaml default prompt should mention ${package.name}")
        short_description = yaml_scalar(yaml_text, "short_description")
        default_prompt = yaml_scalar(yaml_text, "default_prompt")
        if len(short_description) > MAX_SHORT_DESCRIPTION_CHARS:
            errors.append(
                f"{label}: short_description must be {MAX_SHORT_DESCRIPTION_CHARS} characters or fewer"
            )
        if len(default_prompt) > MAX_DEFAULT_PROMPT_CHARS:
            errors.append(
                f"{label}: default_prompt must be {MAX_DEFAULT_PROMPT_CHARS} characters or fewer"
            )

    if not has_markdown_reference(package_path):
        errors.append(f"{label}: missing references/*.md")
    else:
        reference_errors, eval_metrics = validate_references(package_path, skill_md_text, label=label)
        errors.extend(reference_errors)
        if eval_metrics is not None:
            metrics = QualityMetrics(
                description_chars=len(description),
                skill_lines=len(skill_md_text.splitlines()),
                trigger_cases=eval_metrics.trigger_cases,
                non_trigger_cases=eval_metrics.non_trigger_cases,
                quality_cases=eval_metrics.quality_cases,
            )

    for forbidden in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        if (package_path / forbidden).exists():
            errors.append(f"{label}: package-local {forbidden} is not allowed")

    for file_path in package_files(package_path):
        if file_path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        file_text = file_path.read_text(encoding="utf-8", errors="ignore")
        if LEGACY_RE.search(file_text):
            relative = file_path.relative_to(package_path)
            errors.append(f"{label}: stale legacy skill name found in {relative}")
        if PLACEHOLDER_RE.search(file_text):
            relative = file_path.relative_to(package_path)
            errors.append(f"{label}: unresolved placeholder marker found in {relative}")

    return errors, metrics


def validate_source_packages(packages: list[SkillPackage]) -> tuple[list[str], dict[str, QualityMetrics]]:
    errors: list[str] = []
    metrics: dict[str, QualityMetrics] = {}
    if not packages:
        errors.append("source: no skill packages found under skills/*/SKILL.md")
        return errors, metrics

    for package in packages:
        package_errors, package_metrics = validate_package(package, label=f"source {package.name}")
        errors.extend(package_errors)
        if package_metrics is not None:
            metrics[package.name] = package_metrics

    descriptions: dict[str, str] = {}
    for package in packages:
        frontmatter = read_frontmatter(package.path / "SKILL.md")
        normalized = re.sub(r"\s+", " ", frontmatter.get("description", "").strip()).casefold()
        if normalized in descriptions:
            errors.append(
                f"source {package.name}: duplicate description also used by {descriptions[normalized]}"
            )
        descriptions[normalized] = package.name
    return errors, metrics


def validate_skill_invocations(
    packages: list[SkillPackage], *, known_skill_names: set[str] | None = None
) -> list[str]:
    """Reject bare `$name` routes in default prompts that are not shipped skills.

    Agent metadata reserves bare `$name` for skill routing. Shell variables must
    use `${name}` or positional syntax such as `$1`; member access such as
    `this.$watch` is excluded by the route pattern.
    """

    errors: list[str] = []
    known = (
        {package.name for package in packages}
        if known_skill_names is None
        else known_skill_names
    )
    for package in packages:
        metadata_path = package.path / "agents" / "openai.yaml"
        if not metadata_path.is_file():
            continue
        yaml_text = metadata_path.read_text(encoding="utf-8", errors="ignore")
        default_prompt = yaml_scalar(yaml_text, "default_prompt")
        for referenced in sorted(set(SKILL_INVOCATION_RE.findall(default_prompt))):
            if referenced in known:
                continue
            relative = metadata_path.relative_to(package.path)
            errors.append(
                f"source {package.name}: unknown skill invocation ${referenced} in {relative}; "
                "bare $name is reserved for shipped skills, so use ${name} for shell variables"
            )
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


def print_quality_report(packages: list[SkillPackage], metrics: dict[str, QualityMetrics]) -> None:
    print("Quality coverage:")
    print("  skill                     desc  lines  trigger  non-trigger  quality")
    for package in packages:
        item = metrics.get(package.name)
        if item is None:
            continue
        print(
            f"  {package.name:<25} {item.description_chars:>4}  {item.skill_lines:>5}"
            f"  {item.trigger_cases:>7}  {item.non_trigger_cases:>11}  {item.quality_cases:>7}"
        )


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

    source_errors, quality_metrics = validate_source_packages(selected)
    source_errors.extend(
        validate_skill_invocations(
            selected, known_skill_names={package.name for package in packages}
        )
    )
    if not args.skill:
        source_errors.extend(validate_repository_indexes(root, packages))
    if source_errors:
        for error in source_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.quality_report:
        print_quality_report(selected, quality_metrics)

    print(f"validated source packages: {source_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
