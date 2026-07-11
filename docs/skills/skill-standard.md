# Skill Standard

This file defines the project standard for publishable or reusable skill packages under `skills/<skill-name>/`.

## Package Shape

Each skill package must use this structure:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/*.md
  references/eval-cases.md
```

Optional `scripts/` or `assets/` are allowed only when they directly support the skill. Do not add package-local `README.md`, changelogs, install notes, or narrative process docs.

## Naming And Metadata

- Directory name and `SKILL.md` frontmatter `name` must match.
- Skill names must use lowercase letters, numbers, and hyphens only.
- Prefer short verb-led names. Implementation skills use
  `implement-<domain>`, such as `implement-frontend` or `implement-rust`.
- Domain audit skills use `audit-<domain>`, such as `audit-frontend` or
  `audit-rust`. They are read-only by default, lead with evidence-backed
  findings, and route requested fixes to the corresponding `implement-*` skill.
- Keep `code-review` distinct from `audit-*` and `code-delivery`: `code-review`
  owns existing Git changes, dirty-tree classification, contract and structural
  completeness, staging plans, and commit readiness; `audit-*` owns domain-wide
  or reviewer-invoked scoped specialist analysis; `code-delivery` owns staging,
  commits, pushes, and other Git mutations after review.
- Do not use unclear abbreviations such as `imp-*` or mix
  `<domain>-implementation` with `implement-<domain>`.
- `description` must start with `Use when`.
- `description` must describe trigger conditions, not the full workflow.
- Quote frontmatter string values when they contain YAML-significant punctuation such as `: `.
- Keep the frontmatter concise; target description length is under 500 characters.
- Do not use long `Triggers include ...` lists in frontmatter. Put rich trigger examples in `references/usage.md` and `references/eval-cases.md`.
- Use English trigger phrases and realistic user wording by default for public, reusable skills. Add localized trigger phrases only when the skill is explicitly audience-specific.
- Do not keep obsolete skill names inside a skill package. Put migration or
  rejection notes in root documentation, where package-level stale-name checks
  do not treat them as active routing instructions.

## SKILL.md Body

`SKILL.md` should stay lean and procedural. It should include:

- Overview: one short paragraph explaining the capability.
- Workflow or Modes: the core execution path and mode selection.
- Do Not Use For: explicit routing boundaries for adjacent skills when overlap is likely.
- Hard Rules: scope, safety, write, staging, tool, or verification constraints.
- Output Contract: what the agent must report.
- References: direct links to reference files that may be loaded only when needed.
- Maintenance: a short note to update eval cases and metadata when triggers, modes, or output contracts change.

Keep detailed examples, checklists, templates, and trigger/quality evals in `references/`.

## References

Reference files must be one level deep under `references/` and linked from `SKILL.md`.

Use references for:

- detailed checklists
- examples
- trigger, non-trigger, and quality eval cases
- bundled prompt or document templates

References must be self-contained when the published skill needs them. Local `prompts/` files may supplement a skill, but a published skill must not require them to run.

When a skill needs prompt-derived templates, maintain those templates inside that skill package before publishing. Do not make published skills depend on repository-level `prompts/`.

## Agent Metadata

Each skill should include `agents/openai.yaml` with:

- `display_name`
- `short_description`
- `default_prompt`

These values must match the current `SKILL.md`. Update them whenever the skill name, modes, or major triggers change. The repository validator checks metadata structure, lengths, required self-routing, and referenced Skill names; semantic synchronization with workflow, mutation boundaries, and current behavior remains a required human review step unless a package defines an additional machine-readable contract.

Inside `default_prompt`, bare `$name` syntax is reserved for routing to a shipped
skill and is validated against `skills/*`. Write shell variables in braced form
such as `${target}` (or positional form such as `$1`); member syntax such as
`this.$watch` is not a skill route.

## Safety Rules

Every skill that touches repositories must:

- read relevant `AGENTS.md` or nearest repo guidance first when present
- check `git status --short` before planning writes or commits
- preserve unrelated local changes
- use real paths, commands, configs, and code evidence
- say `Not found` for missing files, layers, or commands
- say `Not verified` for unchecked claims
- avoid substituting required tools, browsers, branches, or commands
- preview generated docs before writing unless the user explicitly asks for implementation

Commit-related skills must additionally avoid broad staging such as `git add .` unless the user explicitly approves that exact scope.

## Engineering Alignment

Repository-facing skills must treat engineering standards as project evidence,
not as one universal directory template:

- identify the project class and nearest repository standard before proposing
  directories, toolchains, package managers, scripts, or migrations
- preserve the current stack and protected runtime contracts unless the user or
  repository standard explicitly requests alignment work
- keep equivalent projects consistent within the same class while allowing
  framework-native layouts and documented legacy, prototype, multi-process, or
  production exceptions
- prefer existing local code and components before adding another implementation
- require at least two real consumers and a named owner before extracting a
  cross-repository shared capability, unless repository guidance is stricter
- when adding, reusing, moving, renaming, or deleting structural code, update
  manifests/workspace membership, module exports, commands, tests, CI/deploy
  paths, architecture/project-map docs, and indexes that describe the boundary
- keep validation commands read-only; use explicit `:fix`, write, or formatting
  commands for source rewrites

Generic skills must not hardcode one organization's version numbers or directory
names as universal rules. Put product-specific baselines in the target
repository; teach the skill how to discover and enforce them.

## Distribution Rules

End-user installs and updates should use the standard skills.sh CLI flow:

- `npx skills add https://github.com/idaibin/aicraft`
- `npx skills update`

Do not add package-local self-update modes, remote-source files, or custom update workflows unless a future source-maintenance workflow explicitly needs them. For normal users, document install and update behavior in `README.md` and `INSTALL.md`, not inside each skill package.

## Validation Checklist

Before considering a skill package ready:

- `python3 scripts/validate-skills.py`
- `python3 scripts/test_validate_skills.py`
- `rg -n "^name:|^description: Use when" skills/<skill-name>/SKILL.md`
- `find skills/<skill-name> -maxdepth 3 -type f | sort`
- `rg -n "Triggers include" skills/<skill-name>/SKILL.md` must return no results
- `rg -n "[ \t]+$" skills/<skill-name>`
- `git diff --check -- skills/<skill-name>`

The repository validator also requires the source package set, README skill
table, INSTALL package list, and `skills.sh.json` grouping index to match. Add,
rename, or delete a skill only when all four surfaces are updated together.
- confirm every `references/*.md` file is linked from `SKILL.md`
- confirm `references/eval-cases.md` includes trigger, non-trigger, quality, and scoring cases
- stale-name check for previous names or obsolete aliases
- self-contained check for required external prompt or doc dependencies
- `agents/openai.yaml` structural validator checks plus human review for stale display name, short description, default prompt, modes, mutation boundary, and routing semantics

After publishing to GitHub, users install with `npx skills add https://github.com/idaibin/aicraft` and update installed copies with `npx skills update`. Use `npx skills add https://github.com/idaibin/aicraft --list` only when you need to inspect discoverability without installing.

For skills.sh repository pages, use a root-level `skills.sh.json` only for display grouping. It does not change CLI install behavior or any `SKILL.md` content.

## Review Rubric

- Pass: all required structure, metadata, safety, references, and validation checks are satisfied.
- Needs attention: usable, but has wording drift, stale examples, weak triggers, missing references, or incomplete validation guidance.
- Fail: missing `SKILL.md`, unsafe write behavior, required external dependency, broad staging by default, direct remote overwrite, or misleading trigger metadata.
