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
- Keep the frontmatter concise; target description length is under 500 characters.
- Include stable Chinese trigger phrases and realistic user wording when they materially improve routing.
- Do not keep obsolete skill names in trigger text unless they are explicitly marked as migration or rejection checks.

## SKILL.md Body

`SKILL.md` should stay lean and procedural. It should include:

- Overview: one short paragraph explaining the capability.
- Workflow or Modes: the core execution path and mode selection.
- Hard Rules: scope, safety, write, staging, tool, or verification constraints.
- Output Contract: what the agent must report.
- References: direct links to reference files that may be loaded only when needed.
- Maintenance: a short note to update eval cases and metadata when triggers, modes, or output contracts change.

Keep detailed examples, checklists, templates, upstream metadata, and upgrade workflows in `references/`.

## References

Reference files must be one level deep under `references/` and linked from `SKILL.md`.

Use references for:

- detailed checklists
- examples
- trigger, non-trigger, and quality eval cases
- bundled prompt or document templates
- upstream source metadata
- upgrade workflows

References must be self-contained when the published skill needs them. Local `prompts/` files may supplement a skill, but a published skill must not require them to run.

When a skill needs prompt-derived templates, maintain those templates inside that skill package before publishing. Do not make skill upgrade workflows pull from repository-level `prompts/`.

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
- preview generated docs or upgrade changes before writing unless the user explicitly asks for implementation

Commit-related skills must additionally avoid broad staging such as `git add .` unless the user explicitly approves that exact scope.

## Upgrade Rules

Skills with remote update support should include:

- `references/upstream-sources.md`
- `references/upgrade-workflow.md`
- an `Upgrade Mode` in `SKILL.md`

Remote content is candidate input, not authority. Resolve moving branches to commit SHA, compare read-only, preview proposed changes, and write only after confirmation or an explicit implementation request.

Default upgrade scope is the matching remote skill package: `skills/<skill-name>/`. If prompt changes are required by the skill, they must already be reflected in that remote skill package, usually under `references/`.

## Validation Checklist

Before considering a skill package ready:

- `python3 scripts/validate-skills.py`
- `find skills/<skill-name> -maxdepth 3 -type f | sort`
- `rg -n "^name:|^description: Use when" skills/<skill-name>/SKILL.md`
- `rg -n "[ \t]+$" skills/<skill-name>`
- `git diff --check -- skills/<skill-name>`
- confirm every `references/*.md` file is linked from `SKILL.md`
- confirm `references/eval-cases.md` includes trigger, non-trigger, quality, and scoring cases
- stale-name check for previous names or obsolete aliases
- self-contained check for required external prompt or doc dependencies
- `agents/openai.yaml` check for stale display name, short description, or default prompt

After publishing to GitHub, confirm the repository is discoverable by the standard installer:

- `npx skills add https://github.com/idaibin/aicraft --list`

## Review Rubric

- Pass: all required structure, metadata, safety, references, and validation checks are satisfied.
- Needs attention: usable, but has wording drift, stale examples, weak triggers, missing references, or incomplete validation guidance.
- Fail: missing `SKILL.md`, unsafe write behavior, required external dependency, broad staging by default, direct remote overwrite, or misleading trigger metadata.
