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
- `description` must start with `Use when`.
- `description` must describe trigger conditions, not the full workflow.
- Quote frontmatter string values when they contain YAML-significant punctuation such as `: `.
- Keep the frontmatter concise; target description length is under 500 characters.
- Do not use long `Triggers include ...` lists in frontmatter. Put rich trigger examples in `references/usage.md` and `references/eval-cases.md`.
- Use English trigger phrases and realistic user wording by default for public, reusable skills. Add localized trigger phrases only when the skill is explicitly audience-specific.
- Do not keep obsolete skill names in trigger text unless they are explicitly marked as migration or rejection checks.

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

These values must match the current `SKILL.md`. Update them whenever the skill name, modes, or major triggers change.

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

## Distribution Rules

End-user installs and updates should use the standard skills.sh CLI flow:

- `npx skills add https://github.com/idaibin/aicraft`
- `npx skills update`

Do not add package-local self-update modes, remote-source files, or custom update workflows unless a future source-maintenance workflow explicitly needs them. For normal users, document install and update behavior in `README.md` and `INSTALL.md`, not inside each skill package.

## Validation Checklist

Before considering a skill package ready:

- `python3 scripts/validate-skills.py`
- `rg -n "^name:|^description: Use when" skills/<skill-name>/SKILL.md`
- `find skills/<skill-name> -maxdepth 3 -type f | sort`
- `rg -n "Triggers include" skills/<skill-name>/SKILL.md` must return no results
- `rg -n "[ \t]+$" skills/<skill-name>`
- `git diff --check -- skills/<skill-name>`
- confirm every `references/*.md` file is linked from `SKILL.md`
- confirm `references/eval-cases.md` includes trigger, non-trigger, quality, and scoring cases
- stale-name check for previous names or obsolete aliases
- self-contained check for required external prompt or doc dependencies
- `agents/openai.yaml` check for stale display name, short description, or default prompt

After publishing to GitHub, users install with `npx skills add https://github.com/idaibin/aicraft` and update installed copies with `npx skills update`. Use `npx skills add https://github.com/idaibin/aicraft --list` only when you need to inspect discoverability without installing.

For skills.sh repository pages, use a root-level `skills.sh.json` only for display grouping. It does not change CLI install behavior or any `SKILL.md` content.

## Review Rubric

- Pass: all required structure, metadata, safety, references, and validation checks are satisfied.
- Needs attention: usable, but has wording drift, stale examples, weak triggers, missing references, or incomplete validation guidance.
- Fail: missing `SKILL.md`, unsafe write behavior, required external dependency, broad staging by default, direct remote overwrite, or misleading trigger metadata.
