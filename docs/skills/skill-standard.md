# Skill Standard

This catalog follows the portable [Agent Skills specification](https://agentskills.io/specification),
Anthropic's [authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
and OpenAI's [Build skills](https://learn.chatgpt.com/docs/build-skills) surface.

## Package Shape

Each package contains:

```text
skills/<name>/
  SKILL.md
  agents/openai.yaml
  references/
```

`SKILL.md` is the portable requirement. `agents/openai.yaml` is retained because this
catalog supports OpenAI discovery and UI metadata. `scripts/` and `assets/` are optional
when they directly support the Skill. Do not add package-local README, install guide,
changelog, or process-history files.

## Metadata

- `name` and `description` are required.
- `name` matches the directory, uses lowercase letters, digits, and hyphens, and is at
  most 64 characters.
- `description` is non-empty, at most 1,024 characters, and says what the Skill does
  and when to use it. Prefer concise `Use when ...` wording.
- Optional portable fields are allowed only when they carry real package requirements.
- `agents/openai.yaml` contains `display_name`, `short_description`, and a
  `default_prompt` that routes through `$<skill-name>`.

## Instructions And References

- Keep the `SKILL.md` body under 500 lines and include only the core workflow,
  selection rules, safety boundaries, output, and direct reference links.
- Put detailed checklists, examples, framework profiles, and templates in focused
  references loaded on demand.
- Keep references one level deep and link every reference directly from `SKILL.md`.
- Avoid duplicated guidance. One behavior has one authoritative source.
- A package may not require another Skill or repository-root file to perform its job.

## Skill Boundaries

Create a new public Skill only when the user intent, authority boundary, workflow, and
output are independently useful. Use a profile when React/Vue, Rust subsystems, or
other variants share the same owner and output. See
[`../standards/skill-routing.md`](../standards/skill-routing.md) for the current owners.

Repository-facing boundaries remain simple:

- mapping, review, and audit are read-only unless a named artifact write is explicitly
  part of that Skill;
- `dev-*` may edit task-owned source but does not stage, commit, push, or open a PR;
- `repo-delivery` owns Git mutation;
- browser, client, and external actions require explicit authorization;
- all Skills preserve unrelated local changes and report unchecked runtime claims as
  `Not verified`.

## Evaluation

Maintain at least three representative scenarios for each Skill: a normal trigger, a
nearby non-trigger or boundary, and a quality/edge case. This catalog keeps them in
`references/eval-cases.md` so they remain close to the package.

Run those scenarios when behavior changes. Compare with the previous version or no
Skill when the result is genuinely uncertain or when making an improvement claim.
Repeated campaigns, preregistration, global evidence manifests, token thresholds, and
directory-wide certification are not required for publishing.

## Distribution

Installation and update commands live only in `README.md` and `INSTALL.md`. Published
packages contain no `npx skills` maintenance instructions. `skills.sh.json` is display
metadata and must list the same package set as the root catalog.

## Validation

Use the command matrix in [`../../skills/AGENTS.md`](../../skills/AGENTS.md). The
validator checks portable metadata, OpenAI metadata, package-local links, progressive
disclosure, representative eval sections, distribution hygiene, and catalog parity.
It does not claim that a model will behave identically on every host or task.
