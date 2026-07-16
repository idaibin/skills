# Skill Standard

This file defines the project standard for publishable or reusable skill packages under `skills/<skill-name>/`.

Read `../standards/skill-routing.md` together with this document when adding, splitting, merging, or changing a skill boundary.

## Package Shape

Each AICraft skill package must use this structure:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/*.md
  references/eval-cases.md
```

Optional `scripts/` or `assets/` are allowed only when they directly support the skill. Do not add package-local `README.md`, changelogs, install notes, or narrative process docs.

The portable Agent Skills minimum is `SKILL.md`; `agents/openai.yaml` is an
AICraft-required OpenAI integration surface, not a portable requirement. See
[`../quality/official-skill-alignment.md`](../quality/official-skill-alignment.md)
for provider lanes and pinned sources.

The portable specification permits optional `license`, `compatibility`,
`metadata`, and experimental `allowed-tools` frontmatter. AICraft deliberately
uses only `name` and `description`; the collection license is the root
`LICENSE`, while host capabilities and tool authority remain in runtime
instructions and provider metadata.

## Naming And Metadata

- Directory name and `SKILL.md` frontmatter `name` must match.
- Skill names must use lowercase letters, numbers, and hyphens only.
- Prefer short verb-led names.
- Implementation skills use `implement-<domain>`, such as `implement-frontend` or `implement-rust`, and own requested source changes only.
- Domain audit skills use `audit-<domain>`, such as `audit-frontend`, `audit-rust`, or `audit-security`. They are read-only, select only applicable profiles, lead with evidence-backed findings, and route fixes to the corresponding implementation skill.
- `repo-map` owns semantic repository-map maintenance, real boundaries/commands/task routes, verified reuse inventories, and docs/code alignment. It does not mirror source trees, rank defects, or declare review readiness.
- `diagnose` owns failure reproduction, minimization, hypothesis testing, and root-cause confirmation. Permanent remediation transitions to the matching implementation skill.
- `repo-review` owns read-only review across basis-specific modes: local worktree/index changes, immutable snapshots, branch comparisons, commit ranges, pull requests, release candidates, and verified review packages. It owns dirty-tree readiness in Worktree mode and consolidated P0-P3 findings in immutable modes.
- `audit-security` owns bounded security assessment and may act as a specialist under `repo-review`; it does not replace the coordinator.
- `chatgpt-review` owns local review-package artifacts and explicitly authorized external ChatGPT review rounds. It defaults authorized transport to the desktop built-in browser; Current Chrome or standalone browser use requires an explicit request for that route.
- `repo-delivery` is the sole owner of staging, commits, pushes, squash, cleanup, and other Git mutation after review acceptance.
- Do not use unclear abbreviations such as `imp-*` or mix `<domain>-implementation` with `implement-<domain>`.
- `description` must start with `Use when`.
- `description` must describe trigger conditions, not the full workflow.
- Quote frontmatter string values when they contain YAML-significant punctuation such as `: `.
- Keep the frontmatter concise and within the repository policy in
  [`../../contracts/skill-validation.json`](../../contracts/skill-validation.json).
- Do not use long `Triggers include ...` lists in frontmatter. Put rich trigger examples in `references/usage.md` and `references/eval-cases.md`.
- Use English trigger phrases and realistic user wording by default for public, reusable skills. Add localized triggers only when the skill is explicitly audience-specific.
- Do not keep obsolete skill names inside a skill package. Put migration or rejection notes in root documentation, where package-level stale-name checks do not treat them as active routing instructions.

## Public Skill Or Internal Profile

A public skill must represent a distinct user intent and execution owner. Create one only when all of the following are materially distinct from existing skills:

- primary object;
- authorization or mutation boundary;
- workflow and stop conditions;
- output contract;
- nearest non-trigger set;
- repeated real use across several tasks or repositories.

Use an internal mode or profile when technology or checklist variants share the same evidence inventory, owner, mutation boundary, and output contract.

Examples:

- React, Vue Composition, Vue Options, UI/design-system, accessibility, performance, and Tauri checks remain profiles inside `audit-frontend`.
- Architecture, ownership/errors, concurrency, performance/memory, SQLite, and unsafe/FFI remain profiles inside `audit-rust`.
- Do not create `audit-react`, `audit-vue`, or `audit-ui` solely to divide checklists.

## SKILL.md Body

`SKILL.md` should stay lean and procedural. It should include:

- Overview: one short paragraph explaining the capability and primary object.
- Workflow or Modes/Profiles: the core execution path and selection rules.
- Do Not Use For: explicit routing boundaries for the closest neighboring skills.
- Hard Rules: scope, safety, write, staging, tool, authorization, and verification constraints.
- Output Contract: what the agent must report or produce.
- References: direct links to reference files that may be loaded only when needed.

Keep detailed examples, checklists, templates, and evals in `references/`.
Keep package-maintenance instructions in `skills/AGENTS.md` and repository
standards rather than loading them during every Skill invocation.

## References

Reference files must be one level deep under `references/` and linked from `SKILL.md`.
Long operational references must include a compact contents section when they
cross the repository threshold. The threshold and explicit exemptions, such as
eval-case corpora, live in
[`../../contracts/skill-validation.json`](../../contracts/skill-validation.json).

Use references for:

- detailed checklists;
- modes/profiles and selection criteria;
- examples and anti-patterns;
- trigger, non-trigger, scenario, and quality eval cases;
- bundled prompt or document templates.

References must be self-contained when the published skill needs them. Local `prompts/` files may supplement a skill, but a published skill must not require them to run.

When a skill needs prompt-derived templates, maintain those templates inside that skill package before publishing. Do not make published skills depend on repository-level `prompts/`.

When multiple published skills require an identical protocol, keep one
repository source under `protocols/` and generate the self-contained package
copies with `scripts/sync-shared-protocols.py`. The generated copies remain part
of each published package; they are not independent authoring surfaces.

## Agent Metadata

Each AICraft skill must include `agents/openai.yaml` with:

- `display_name`
- `short_description`
- `default_prompt`

These values must match the current `SKILL.md`. Update them whenever the skill name, modes/profiles, primary object, mutation boundary, major triggers, or output contract changes.

This file belongs to the OpenAI lane. Do not treat its fields as portable
Agent Skills metadata or copy them into Claude-only frontmatter.

The repository validator checks metadata structure, lengths, required self-routing, and referenced Skill names. Semantic synchronization remains a required review step.

Inside `default_prompt`, bare `$name` syntax is reserved for routing to a shipped skill and is validated against `skills/*`. Write shell variables in braced form such as `${target}` or positional form such as `$1`; member syntax such as `this.$watch` is not a skill route.

## Safety And Authority Rules

Every repository-facing skill must:

- read effective repository and host guidance first, including `AGENTS.md`,
  `CLAUDE.md` imports, or host-provided instructions when present;
- check `git status --short` before planning writes or commits;
- preserve unrelated local changes;
- use real paths, commands, configs, revisions, and code evidence;
- say `Not found` for missing files, layers, commands, or artifacts;
- say `Not verified` for unchecked claims;
- avoid substituting required tools, browsers, branches, or commands;
- preview generated docs before writing unless the user explicitly asks for implementation.

Authority boundaries:

- context, planning, diagnosis, review, audit, and security skills are read-only unless their own documented artifact boundary explicitly permits a local output file;
- `diagnose` does not apply permanent fixes;
- `implement-*` may edit task-owned source but must not stage, commit, push, or create PRs;
- `repo-review` does not edit or mutate Git/GitHub state;
- `audit-security` does not expand beyond its bounded surface or take over review coordination;
- `repo-delivery` alone owns Git mutation;
- browser, client, and external ChatGPT actions require explicit action authorization and capability verification.

Commit-related skills must avoid broad staging such as `git add .` unless the user explicitly approves that exact scope.

## Engineering Alignment

Repository-facing skills must treat engineering standards as project evidence, not as one universal directory template:

- identify the project class and nearest repository standard before proposing directories, toolchains, package managers, scripts, or migrations;
- preserve the current stack and protected runtime contracts unless the user or repository standard explicitly requests alignment work;
- keep equivalent projects consistent within the same class while allowing framework-native layouts and documented legacy, prototype, multi-process, or production exceptions;
- prefer existing local code and components before adding another implementation;
- require at least two real consumers and a named owner before extracting a cross-repository shared capability, unless repository guidance is stricter;
- when adding, reusing, moving, renaming, or deleting structural code, update manifests/workspace membership, exports, commands, tests, CI/deploy paths, architecture/repo-map docs, generated artifacts, migrations, consumers, and indexes that describe the boundary;
- keep validation commands read-only during review; use explicit fix/write commands only during authorized implementation.

Generic skills must not hardcode one organization's version numbers or directory names as universal rules. Put product-specific baselines in the target repository; teach the skill how to discover and enforce them.

## Eval Requirements

Every skill must include realistic:

- Trigger Eval cases;
- Non-Trigger Eval cases;
- Quality Eval cases;
- Scoring rules.

When a skill boundary changes, add pairwise trigger/non-trigger cases against every closest neighbor. For example:

- `repo-map` versus `repo-review` and `audit-security`;
- `repo-review` versus `audit-security` and `repo-delivery`;
- `diagnose` versus matching `implement-*` skills;
- `audit-frontend` versus `repo-review` and `implement-frontend`.

Every published package must satisfy its documented quality acceptance rules
and the repository validator. Authorization, mutation, external-action, and
evidence-integrity violations are hard failures and cannot be offset by other
scores.

Routing evaluation must score the complete owner-and-handoff contract. A case
passes only when an accepted primary owner is selected, all necessary direct
handoffs and exactly one member of every necessary one-of group are present,
and no unauthorized or optional handoff is emitted.
Datasets must include both positive required-handoff cases and cases where an
empty handoff list is the only correct result; report violations by affected
case count as well as individual handoff count.

## Status And Evidence

Do not assign subjective maturity labels to public skills. Keep three concerns
separate:

- functional category: what capability and authority the skill owns;
- release state: `available`, `hidden`, or `removed`;
- validation state: `verified` or `not_verified` independently for structure,
  behavior, and workflow.

Structure verification covers repository/package consistency only. Behavior
verification requires real natural-language routing, authority, stop, and
handoff results bound to a model, host, committed Skill revision, dataset, and
raw result. Workflow verification additionally requires end-to-end repository
task evidence. Producer-authored hashes make retained evidence tamper-evident;
they do not authenticate the host or independently prove self-reported action
labels. Until the repository adds an independent semantic verifier, authority
and workflow remain `not_verified`. Do not infer either from Markdown eval
tables. A baseline is not required for contract evaluation, but a controlled
candidate/previous/no-Skill group is required for a narrowly scoped improvement
claim. Formal held-out claims additionally require a committed preregistered
campaign, an anchor-frozen evaluation protocol, canonical prompt de-duplication,
and the complete retained attempt ledger described in
[`../quality/validation-plan.md`](../quality/validation-plan.md).

Record the current inventory and evidence boundary in
`docs/quality/status.md`. A public install bundle describes scope only and must
not imply behavior or workflow verification.

## Distribution Rules

End-user installs and updates should use the standard skills.sh CLI flow:

- `npx skills add https://github.com/idaibin/aicraft`
- `npx skills update --project` for current-project installations;
- `npx skills update --global` for global installations, including shared Codex and Claude Code installs.

Do not add package-local self-update modes, remote-source files, or custom update workflows unless a future source-maintenance workflow explicitly needs them. Document install and update behavior in `README.md` and `INSTALL.md`, not inside each skill package.

Root installation documentation must distinguish CLI-tracked installs from
manual copies, state that update is scope-based rather than agent-filtered, and
include explicit remove-and-add instructions for every published skill rename
or merge. Keep Codex and Claude Code on the same standard CLI flow; do not
maintain provider-specific update instructions inside individual packages.

## Validation Checklist

Before considering a skill package ready:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/eval-skill-contracts.py --validate-only
python3 scripts/measure-skill-footprint.py --baseline-ref HEAD
rg -n "^name:|^description: Use when" skills/<skill-name>/SKILL.md
find skills/<skill-name> -maxdepth 3 -type f | sort
rg -n "Triggers include" skills/<skill-name>/SKILL.md
git diff --check -- skills/<skill-name>
```

The `Triggers include` command must return no results. Also verify:

- source package set, README table, INSTALL list, and `skills.sh.json` contain the same skill names;
- every `references/*.md` file is linked from `SKILL.md`;
- eval cases include trigger, non-trigger, quality, and scoring sections;
- metadata and `SKILL.md` agree on primary object, profile/mode, mutation boundary, routing, and output;
- pairwise evals cover the closest neighboring skills;
- `docs/skills/routing-graph.json` lists every package and keeps every nearest-neighbor edge symmetric;
- no stale names, placeholders, required repository-local prompt dependencies, or broken links remain;
- the official-source review recorded in
  `contracts/skill-validation.json` is current and agrees with
  `docs/quality/official-skill-alignment.md`;
- `git diff --check` passes.

After publishing, users install with `npx skills add https://github.com/idaibin/aicraft` and update installed copies with `npx skills update --project` or `npx skills update --global`. Use `--list` only to inspect source discoverability and `npx skills list` to inspect installed skills.

For skills.sh repository pages, use root-level `skills.sh.json` only for display grouping. It does not change CLI install behavior or any `SKILL.md` content.

## Review Rubric

- Pass: required structure, metadata, authority, routing, references, evals, and validation are satisfied.
- Needs attention: usable, but has wording drift, stale examples, weak pairwise routing, missing profile selection, or incomplete validation guidance.
- Fail: missing package files, unsafe write behavior, ambiguous mutation owner, required external dependency, broad staging by default, direct remote overwrite, or misleading trigger metadata.
