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
- Portable `description` remains required even when a provider should expose the Skill
  only for explicit use. For OpenAI, express that provider-specific choice with
  `policy.allow_implicit_invocation: false`; never copy invocation-control fields from
  another provider into portable `SKILL.md` frontmatter.

## Repository Discovery Index

`skills-index.json` is the catalog's provider-neutral repository discovery source. It
records logical categories, user intents, search keywords, exclusions, and related
owners for browsing and `scripts/search-skills.py`. It is not portable Skill
frontmatter, does not override `SKILL.md`, and must not be presented as if every Agent
client loads it automatically.

Keep runtime trigger keywords in the portable `description`. Do not add custom top-level
fields such as `routing`, `triggers`, or `related` to `SKILL.md`; the portable spec's
optional `metadata` remains string-to-string provider/client metadata, not this
catalog's nested routing registry. Keep package set, names, relations, categories, and
index shape validator-backed.

## Instructions And References

- Keep the `SKILL.md` body under 500 lines and include only the core workflow,
  selection rules, safety boundaries, output, and direct reference links.
- Put detailed checklists, examples, framework profiles, and templates in focused
  references loaded on demand.
- Keep references one level deep and link every reference directly from `SKILL.md`.
- Add a `## Contents` section to references longer than 100 lines.
- Give each ordered step a checkable transition or completion criterion. Prefer an
  observable state, exhausted bounded set, or named stop condition over vague verbs
  such as understand, improve, or finish.
- Inline what every execution branch needs; disclose branch-specific reference behind
  a direct, condition-worded pointer. Co-locate a concept's rule, exception, and stop
  condition instead of scattering fragments across the entrypoint and references.
- Avoid duplicated guidance. One behavior has one authoritative source; repeat a short,
  stable term only when it intentionally anchors routing or execution.
- A package may not require another Skill or repository-root file to perform its job.

## Task-Local Output

Follow active repository instructions before writing task-local files. With no more
specific rule, store temporary reports, reviews, handoffs, evidence, and helper files
as `.codex/<category>/<type>-<YYYYMMDD-HHmmss>.<ext>` using local time. Use exactly
one category parent under `.codex`—normally `artifacts`, `reviews`, `handoffs`, or
`tmp`—and do not create task, type, or date subdirectories by default. Related files
share a timestamped filename prefix instead of a directory. Durable user-requested
project documentation and final deliverables remain in their authoritative repository
or output location.

## Maintenance And Pruning

For every Skill revision, inspect each touched sentence against four questions:

1. Does it change routing, execution, safety, evidence, output, or a completion gate?
2. Is it still true for the supported hosts and current owner boundary?
3. Is the same meaning already authoritative elsewhere?
4. Does a conditional branch belong behind an existing reference pointer?

Delete no-op, stale, or duplicated prose instead of rephrasing it. Prefer positive
target behavior; retain prohibitions for real safety or authority guardrails and pair
them with the permitted action or stop path. Do not split a workflow merely because it
is long: first sharpen completion criteria and disclose conditional reference, then
split only when an independently useful invocation or a proven sequence failure needs
a separate context boundary.

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

Feed a real failure back into the narrowest owning rule and existing eval file that
would have caught it. Do not create a public Skill, shared regression framework, or
cross-catalog reference solely to document the iteration method.

Keep raw runs directly under ignored `eval-results/` or `.codex/reviews/` with
timestamped filenames. Commit only a
sanitized summary whose fixed Skill revision, host/model, scenarios, result, failures,
and coverage limits remain useful. Old raw runs never prove current behavior.

## Distribution

Installation and update commands live only in `README.md` and `INSTALL.md`. Published
packages contain no `npx skills` maintenance instructions. `skills.sh.json` is
distribution display metadata; `skills-index.json` is semantic discovery metadata.
Both must list the same package set as the root catalog.

## Validation

Use the command matrix in [`../../skills/AGENTS.md`](../../skills/AGENTS.md). The
validator checks portable metadata, OpenAI metadata, package-local links, progressive
disclosure, representative eval sections, semantic-index integrity, distribution
hygiene, and catalog parity.
Focused regression tests are run by local `bash scripts/check-skills.sh`.
The validator does not claim that a model will
behave identically on every host or task.
