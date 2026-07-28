# Skill Standard

This catalog follows the portable [Agent Skills specification](https://agentskills.io/specification),
Anthropic's [authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
and OpenAI's [Build skills](https://learn.chatgpt.com/docs/build-skills) surface.

## Package Shape

Each package in this catalog contains:

```text
skills/<name>/
  SKILL.md
  agents/openai.yaml
  references/
```

`SKILL.md` is the portable requirement. `agents/openai.yaml` is an OpenAI-specific
catalog decision, not part of the portable contract. `scripts/` and `assets/` are
optional when they directly support the Skill. Do not add package-local README,
install guide, changelog, or process-history files.

## Provider Surfaces

- **Portable Agent Skills clients:** consume `SKILL.md` plus package-local resources.
- **OpenAI:** may additionally consume `agents/openai.yaml` for UI metadata, invocation
  policy, and declared tool dependencies. This catalog requires its three interface
  fields because OpenAI is an explicit target.
- **Anthropic:** consumes the portable Skill directory directly. Claude custom Skills
  do not require an `agents/anthropic.yaml`; Claude Code plugin or marketplace metadata,
  when intentionally shipped, belongs to a repository-level distribution wrapper.
- **Other providers:** use the portable package unless the provider publishes a real
  additional contract that the catalog has decided to support.

Do not mirror the same description or workflow into speculative provider files. A
provider adapter must add machine-consumed behavior or distribution metadata, have a
documented owner and validator, and leave `SKILL.md` as the portable authority.

## Metadata

- `name` and `description` are required.
- `name` matches the directory, uses lowercase letters, digits, and hyphens, and is at
  most 64 characters.
- `description` is non-empty, at most 1,024 characters, and says what the Skill does
  and when to use it. Prefer concise `Use when ...` wording. When a real neighboring
  Skill or host capability is easy to confuse with this owner, include one short
  negative or rerouting condition in the description; do not enumerate the full
  `Do Not Use For` section in always-loaded metadata.
- Optional portable `license`, `compatibility`, `metadata`, and `allowed-tools` fields
  are allowed only when they carry real package requirements and match the specification.
- Portable package shape does not imply identical runtime capability on every host. A
  Skill whose external workflow depends on documented host operations declares that
  requirement in `compatibility` and must degrade to a safe local result or stop when
  the current host does not expose an equivalent capability; it never simulates success.
- `agents/openai.yaml` contains `display_name`, `short_description`, and a
  `default_prompt` that routes through `$<skill-name>`; `short_description` stays
  within OpenAI's 25-64 character UI range.

## Instructions And References

- Keep the `SKILL.md` body under 500 lines and include only the core workflow,
  selection rules, safety boundaries, output, and direct reference links.
- Put detailed checklists, examples, framework profiles, and templates in focused
  references loaded on demand.
- Keep references one level deep and link every reference directly from `SKILL.md`.
- Add a `## Contents` section to references longer than 100 lines.
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

Keep raw runs under ignored `eval-results/` or `.codex/reviews/`. Commit only a
sanitized summary whose fixed Skill revision, host/model, scenarios, result, failures,
and coverage limits remain useful. Old raw runs never prove current behavior.

## Distribution

Installation and update commands live only in `README.md` and `INSTALL.md`. Published
packages contain no `npx skills` maintenance instructions. `skills.sh.json` is display
metadata and must list the same package set as the root catalog.

## Validation

Use the command matrix in [`../../skills/AGENTS.md`](../../skills/AGENTS.md). The
validator checks portable metadata, OpenAI metadata, package-local links, progressive
disclosure, representative eval sections, distribution hygiene, and catalog parity.
Focused regression tests are run by local `bash scripts/check-skills.sh`.
The validator does not claim that a model will
behave identically on every host or task.
