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
    "code-context",
    "code-review",
    "code-delivery",
    "code-security",
    "commit-reviewer",
    "planner",
    "frontend-implementation",
    "frontend-governance",
    "rust-engineering-governance",
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
LEGACY_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(name) for name in LEGACY_SKILL_NAMES) + r")(?![A-Za-z0-9_-])"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_INVOCATION_RE = re.compile(r"(?<![A-Za-z0-9_.])\$([a-z][a-z0-9-]*)")
EVAL_CASES_FILE = "eval-cases.md"
ROUTING_GRAPH_FILE = "docs/skills/routing-graph.json"
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


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key {key!r}")
        result[key] = value
    return result


def expected_routes_to_skill(expected: str, skill_name: str) -> bool:
    """Recognize an affirmative routing decision, not a coincidental skill mention."""

    token_re = re.compile(
        rf"(?<![a-z0-9-]){re.escape(skill_name)}(?![a-z0-9-])",
        re.IGNORECASE,
    )
    positive_re = re.compile(
        r"(?:prefer|use|trigger|before|keep|delegate|route)[^.;]{0,100}$",
        re.IGNORECASE,
    )
    negative_re = re.compile(
        r"(?:(?:do|does|should|must)\s+not|don't|never)\s+"
        r"(?:prefer|use|trigger|route|delegate)[^.;]{0,50}$"
        r"|(?:\bnot\b|rather than|instead of)[^.;]{0,40}$",
        re.IGNORECASE,
    )
    for match in token_re.finditer(expected):
        prefix = expected[max(0, match.start() - 120) : match.start()]
        if negative_re.search(prefix):
            continue
        if positive_re.search(prefix):
            return True
    return False


def validate_routing_graph(root: Path, packages: list[SkillPackage]) -> list[str]:
    """Require symmetric nearest-neighbor routing and documented pairwise eval coverage."""

    errors: list[str] = []
    path = root / ROUTING_GRAPH_FILE
    known = {package.name for package in packages}
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [f"repository: cannot read {ROUTING_GRAPH_FILE}: {error}"]
    if not isinstance(payload, dict):
        return [f"repository: {ROUTING_GRAPH_FILE} must contain an object"]

    listed = set(payload)
    for name in sorted(known - listed):
        errors.append(f"repository: routing graph missing skill {name}")
    for name in sorted(listed - known):
        errors.append(f"repository: routing graph lists unknown skill {name}")

    package_by_name = {package.name: package for package in packages}
    for name in sorted(known & listed):
        neighbors = payload.get(name)
        if not isinstance(neighbors, list) or any(
            not isinstance(neighbor, str) for neighbor in neighbors
        ):
            errors.append(f"repository: routing graph entry {name} must be a string list")
            continue
        if len(neighbors) != len(set(neighbors)):
            errors.append(f"repository: routing graph entry {name} contains duplicates")
        if name in neighbors:
            errors.append(f"repository: routing graph entry {name} cannot reference itself")

        eval_path = package_by_name[name].path / "references" / EVAL_CASES_FILE
        eval_text = (
            eval_path.read_text(encoding="utf-8", errors="ignore")
            if eval_path.is_file()
            else ""
        )
        routing_expectations = [
            cell
            for section in ("## Trigger Eval", "## Non-Trigger Eval")
            for row in markdown_table_rows(eval_text, section)
            for cell in row[1:2]
        ]
        for neighbor in neighbors:
            if neighbor not in known:
                errors.append(
                    f"repository: routing graph entry {name} references unknown skill {neighbor}"
                )
                continue
            reverse = payload.get(neighbor, [])
            if not isinstance(reverse, list) or name not in reverse:
                errors.append(
                    f"repository: routing graph edge {name} -> {neighbor} must be symmetric"
                )
            if not any(
                expected_routes_to_skill(expected, neighbor)
                for expected in routing_expectations
            ):
                errors.append(
                    f"source {name}: routing eval expectations do not cover nearest neighbor {neighbor}"
                )
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

    elif skill_name == "chatgpt-review":
        required = (
            "Package artifact",
            "Split package artifact",
            "Multipart send sequence",
            "External authorization",
            "Response completion",
            "Review artifact visibility",
            "Local verification",
            "Capability Snapshot contract",
            "Browser handoff contract",
            "Operation idempotency",
            "Interruption reconciliation",
            "Identity-bound snapshot",
            "Conversation creation idempotency",
            "Round and operation scope",
            "Legal transitions",
            "Retry attempt lifecycle",
            "Identity privacy",
        )
        for case in missing_table_cases(eval_text, "## Quality Eval", required):
            errors.append(
                f"{label}: chatgpt-review Quality Eval missing required case {case!r}"
            )

    elif skill_name == "audit-frontend":
        scenario_rows = markdown_table_rows(eval_text, "## Scenario Eval")
        scenario_text = "\n".join(" | ".join(row) for row in scenario_rows)
        if len(scenario_rows) < 16:
            errors.append(
                f"{label}: audit-frontend Scenario Eval must contain at least 16 cases"
            )
        for term in ("Vue Composition API", "Pure Options API", "`repo-review` delegates"):
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

    elif skill_name == "repo-review":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Immutable basis", "Specialist composition", "Duplicate control", "Read-only boundary"),
        ):
            errors.append(
                f"{label}: repo-review Quality Eval missing required case {case!r}"
            )

    elif skill_name == "repo-map":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Scope and stop condition", "Context-versus-review boundary", "Reuse inventory", "New-file gate"),
        ):
            errors.append(
                f"{label}: repo-map Quality Eval missing required case {case!r}"
            )

    elif skill_name == "audit-security":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Scope mapping", "Scoped specialist boundary", "Release check"),
        ):
            errors.append(
                f"{label}: audit-security Quality Eval missing required case {case!r}"
            )

    elif skill_name == "ops-browser":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            (
                "Browser debug handoff",
                "State safety",
                "Cleanup",
                "Capability Snapshot contract",
                "Bridge handoff contract",
                "Duplicate-submit prevention",
                "Failed-before-submit retry",
                "Identity freshness",
                "Conversation creation operation",
                "Legal transition result",
                "Retry attempt evidence",
                "Snapshot privacy",
            ),
        ):
            errors.append(
                f"{label}: ops-browser Quality Eval missing required case {case!r}"
            )

    elif skill_name == "ops-client":
        for case in missing_table_cases(
            eval_text,
            "## Quality Eval",
            ("Client debug handoff", "Runtime source", "Unsupported versus unverified"),
        ):
            errors.append(
                f"{label}: ops-client Quality Eval missing required case {case!r}"
            )

    return errors


def markdown_section(markdown_text: str, section: str) -> str:
    start = markdown_text.find(section)
    if start < 0:
        return ""
    body_start = start + len(section)
    next_section = markdown_text.find("\n## ", body_start)
    return markdown_text[body_start:] if next_section < 0 else markdown_text[body_start:next_section]


CROSS_ARTIFACT_TERM_REQUIREMENTS: tuple[
    tuple[str, str, str | None, tuple[str, ...]], ...
] = (
    ("repo-review", "SKILL.md", "## Hard Rules", ("review basis", "resolved SHAs", "read-only")),
    ("repo-review", "references/usage.md", "## Examples", ("Resolve both endpoints", "SHAs")),
    ("repo-map", "SKILL.md", "## Overview", ("does not judge", "defects")),
    ("repo-map", "references/usage.md", "## Triggers", ("immutable repository/range/PR review", "repo-review")),
    ("audit-security", "SKILL.md", "## Modes", ("Scoped specialist subreview", "coordinator retains", "severity")),
    ("audit-security", "references/usage.md", "## Output", ("delegated path/diff boundary", "without editing", "coordinator")),
    ("ops-browser", "SKILL.md", "## Modes", ("diagnose", "already-isolated", "browser-layer")),
    ("ops-browser", "agents/openai.default_prompt", None, ("only after $diagnose delegation", "before browser operation", "final cause/fix")),
    ("ops-browser", "references/usage.md", "## Browser Debug Evidence", ("diagnose", "before browser operation", "retain referenced")),
    ("ops-browser", "SKILL.md", "## Hard Rules", ("operation_id", "ambiguous", "prior evidence")),
    ("chatgpt-review", "SKILL.md", "## Browser Handoff", ("operation_id", "operation ledger", "ambiguous")),
    ("chatgpt-review", "agents/openai.default_prompt", None, ("browser-operation/v1", "operation-ledger", "operation_id", "ambiguous")),
    ("ops-client", "SKILL.md", "## Modes", ("diagnose", "already-isolated", "client-layer")),
    ("ops-client", "SKILL.md", "## Hard Rules", ("Retain screenshots", "handoff owner", "removed disposable state")),
    ("ops-client", "agents/openai.default_prompt", None, ("only after $diagnose delegation", "before client operation", "retain referenced evidence")),
    ("ops-client", "references/usage.md", "## Operation Notes", ("diagnose", "already-isolated", "retain referenced")),
)


def eval_row(eval_text: str, section: str, key: str) -> list[str]:
    wanted = normalized_eval_key(key)
    for row in markdown_table_rows(eval_text, section):
        if row and normalized_eval_key(row[0]) == wanted:
            return row
    return []


def validate_eval_row_semantics(
    eval_text: str,
    section: str,
    key: str,
    column_terms: tuple[tuple[int, tuple[str, ...]], ...],
    *,
    label: str,
) -> list[str]:
    row = eval_row(eval_text, section, key)
    if not row:
        return [f"{label}: missing semantic eval row {key!r} in {section}"]
    errors: list[str] = []
    for column, terms in column_terms:
        cell = row[column].casefold() if len(row) > column else ""
        missing = [term for term in terms if term.casefold() not in cell]
        if missing:
            errors.append(
                f"{label}: eval row {key!r} column {column + 1} missing semantic terms {missing}"
            )
    return errors


def validate_cross_artifact_contracts(
    skill_name: str, surfaces: dict[str, str], *, label: str
) -> list[str]:
    """Validate scoped authority text plus structured Eval row behavior."""

    errors: list[str] = []
    for required_skill, surface, section, terms in CROSS_ARTIFACT_TERM_REQUIREMENTS:
        if required_skill != skill_name:
            continue
        source = surfaces.get(surface, "")
        scoped = markdown_section(source, section) if section else source
        missing = [term for term in terms if term.casefold() not in scoped.casefold()]
        if missing:
            errors.append(
                f"{label}: {skill_name} {surface} {section or 'field'} missing contract terms {missing}"
            )

    eval_text = surfaces.get("references/eval-cases.md", "")
    semantic_rows: dict[str, tuple[tuple[str, str, tuple[tuple[int, tuple[str, ...]], ...]], ...]] = {
        "repo-review": (("## Quality Eval", "Immutable basis", ((1, ("sha", "before conclusions")), (2, ("moving", "ambiguous")))),),
        "repo-map": (("## Quality Eval", "Context-versus-review boundary", ((1, ("without p0-p3", "repo-review")), (2, ("universal review",)))),),
        "audit-security": (("## Quality Eval", "Scoped specialist boundary", ((1, ("delegated paths/diff", "repo-review")), (2, ("expands scope", "whole-review readiness")))),),
        "ops-browser": (
            ("## Trigger Eval", "Reproduce this known browser-only CORS failure and collect console/network evidence.", ((1, ("browser debug evidence", "directly")), (2, ("browser fact",)))),
            ("## Trigger Eval", "Diagnose delegated this exact browser reproduction; collect DOM, console, and network evidence.", ((1, ("browser debug evidence",)), (2, ("delegation",)))),
            ("## Non-Trigger Eval", "Why does this form intermittently fail after submit? Find the root cause.", ((1, ("diagnose", "browser debug evidence")), (2, ("cross-system",)))),
            ("## Quality Eval", "Browser debug handoff", ((1, ("diagnose", "already-isolated", "retains referenced evidence")), (2, ("final cause/fix", "deletes evidence before transfer")))),
        ),
        "ops-client": (
            ("## Trigger Eval", "Diagnose delegated this exact release-window reproduction; collect process and window evidence.", ((1, ("client debug evidence",)), (2, ("delegation",)))),
            ("## Trigger Eval", "On the verified release app, reproduce this already-isolated Accessibility action failure and return client evidence only.", ((1, ("client debug evidence",)), (2, ("bounded", "without cross-system")))),
            ("## Non-Trigger Eval", "Why does the release app button not respond? Find the root cause.", ((1, ("diagnose", "client debug evidence")), (2, ("cross", "boundaries")))),
            ("## Quality Eval", "Client debug handoff", ((1, ("diagnose", "already-isolated", "retains referenced evidence")), (2, ("final cause/fix", "deletes evidence before transfer")))),
        ),
    }
    for section, key, columns in semantic_rows.get(skill_name, ()):
        errors.extend(
            validate_eval_row_semantics(eval_text, section, key, columns, label=label)
        )
    forbidden_by_skill = {
        "ops-browser": (
            "not prefer `diagnose`",
            "trigger `ops-browser` directly and may later",
            "permits final cause/fix",
            "deletes evidence before transfer after reporting",
            "direct operation takes precedence over `diagnose`",
        ),
        "ops-client": (
            "not prefer `diagnose`",
            "trigger `ops-client` directly and may later",
            "permits final cause/fix",
            "deletes evidence before transfer after reporting",
            "direct operation takes precedence over `diagnose`",
        ),
    }
    combined_contract_text = "\n".join(surfaces.values()).casefold()
    for forbidden in forbidden_by_skill.get(skill_name, ()):
        if forbidden.casefold() in combined_contract_text:
            errors.append(
                f"{label}: {skill_name} contains contradictory contract phrase {forbidden!r}"
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
    has_minimum = "Minimum pass:" in scoring
    has_numeric_gate = re.search(r"scores? at least (?:[89]|10)", scoring)
    has_defect_gate = "no P0 or P1 defect remains" in scoring
    if not has_minimum or not (has_numeric_gate or has_defect_gate):
        errors.append(
            f"{label}: scoring must define either a minimum quality score of at least 8 "
            "or a no-P0/P1 defect gate"
        )

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

    contract_surfaces = {
        "SKILL.md": skill_md_text,
        "agents/openai.yaml": (
            openai_yaml.read_text(encoding="utf-8") if openai_yaml.is_file() else ""
        ),
        "agents/openai.default_prompt": (
            yaml_scalar(openai_yaml.read_text(encoding="utf-8"), "default_prompt")
            if openai_yaml.is_file()
            else ""
        ),
        "references/usage.md": (
            (package_path / "references" / "usage.md").read_text(encoding="utf-8")
            if (package_path / "references" / "usage.md").is_file()
            else ""
        ),
        "references/eval-cases.md": (
            (package_path / "references" / EVAL_CASES_FILE).read_text(encoding="utf-8")
            if (package_path / "references" / EVAL_CASES_FILE).is_file()
            else ""
        ),
    }
    errors.extend(
        validate_cross_artifact_contracts(package.name, contract_surfaces, label=label)
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


def validate_shared_browser_operation_protocol(root: Path) -> list[str]:
    relative_paths = (
        Path("skills/chatgpt-review/references/browser-operation-protocol.md"),
        Path("skills/ops-browser/references/browser-operation-protocol.md"),
    )
    contents: list[str] = []
    errors: list[str] = []
    for relative in relative_paths:
        path = root / relative
        try:
            contents.append(path.read_text(encoding="utf-8"))
        except OSError as error:
            errors.append(f"repository: cannot read {relative}: {error}")
    if errors:
        return errors
    if contents[0] != contents[1]:
        errors.append("repository: shared browser-operation protocol copies must be identical")
    required_by_section = {
        "## Capability Snapshot": (
            "schema_version: browser-operation/v1",
            "snapshot_id:",
            "identity:",
            "account_category:",
            "workspace_id:",
            "state_fingerprint:",
            "login_state:",
            "target_origin:",
            "capabilities:",
            "evidence:",
            "gaps:",
            "opaque one-way fingerprint",
            "Never store an email address",
        ),
        "## Handoff Request": (
            "schema_version: browser-operation/v1",
            "operation_id:",
            "round_id:",
            "attempt: <positive integer; starts at 1>",
            "intent:",
            "create-conversation",
            "authorization:",
            "capability_snapshot_id:",
            "preconditions:",
            "expected_postcondition:",
            "retry_policy: <never|only-if-no-side-effect-proven>",
            "prior_evidence:",
        ),
        "## Handoff Result": (
            "schema_version: browser-operation/v1",
            "operation_id:",
            "round_id:",
            "attempt: <same request attempt>",
            "capability_snapshot_id:",
            "state: <preflighted|ready|created|attached|submitted|acknowledged|captured|cleaned|completed|failed-before-submit|blocked|ambiguous>",
            "before:",
            "action:",
            "side_effect:",
            "after:",
            "retained_evidence:",
            "cleanup:",
            "error:",
        ),
        "## Operation State Machine": (
            "| `prepared` | `preflighted`, `blocked` |",
            "| `ready` | `created`, `attached`, `submitted`",
            "| `submitted` | `acknowledged`, `completed`, `ambiguous` |",
            "| `failed-before-submit` | `ready` only for a new attempt",
            "| `completed` | terminal |",
            "failed-before-submit",
            "round_id",
            "retry with the same ID",
        ),
        "## Degraded Mode": ("blocked", "ambiguous", "do not retry"),
    }
    for section, terms in required_by_section.items():
        scoped = markdown_section(contents[0], section)
        if not scoped:
            errors.append(f"repository: shared browser-operation protocol missing section {section!r}")
            continue
        normalized_scoped = re.sub(r"\s+", " ", scoped).casefold()
        for term in terms:
            normalized_term = re.sub(r"\s+", " ", term).casefold()
            if normalized_term not in normalized_scoped:
                errors.append(
                    f"repository: shared browser-operation protocol {section} missing {term!r}"
                )
    return errors


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
    print("Documented eval coverage (not executed behavior):")
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
        source_errors.extend(validate_routing_graph(root, packages))
        source_errors.extend(validate_shared_browser_operation_protocol(root))
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
