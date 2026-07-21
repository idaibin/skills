# Skill Standard

This file defines the project standard for publishable or reusable skill packages under `skills/<skill-name>/`.

Read `../standards/skill-routing.md` together with this document when adding, splitting, merging, or changing a skill boundary.

## Package Shape

Each published Skill package must use this structure:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/*.md
  references/eval-cases.md
```

Optional `scripts/` or `assets/` are allowed only when they directly support the skill. Do not add package-local `README.md`, changelogs, install notes, or narrative process docs.

The portable Agent Skills minimum is `SKILL.md`. This catalog also requires
`agents/openai.yaml` as an OpenAI integration surface; it is not a portable
requirement. See
[`../quality/official-skill-alignment.md`](../quality/official-skill-alignment.md)
for provider lanes and pinned sources.

The portable specification permits optional `license`, `compatibility`,
`metadata`, and experimental `allowed-tools` frontmatter. This catalog
deliberately uses only `name` and `description`; the collection license is the root
`LICENSE`, while host capabilities and tool authority remain in runtime
instructions and provider metadata.

## Naming And Metadata

- Directory name and `SKILL.md` frontmatter `name` must match.
- Skill names must use lowercase letters, numbers, and hyphens only.
- Prefer short verb-led names.
- Implementation skills use `dev-<domain>`, such as `dev-frontend` or `dev-rust`, and own requested source changes only.
- Domain audit skills use `audit-<domain>`, such as `audit-frontend`, `audit-rust`, or `audit-security`. They are read-only, select only applicable profiles, lead with evidence-backed findings, and route fixes to the corresponding implementation skill.
- `repo-map` owns semantic repository-map maintenance, real boundaries/commands/task routes, verified reuse inventories, bounded protocol-authority/consumer maps, and docs/code alignment. It does not mirror source trees, copy executable schemas, rank defects, declare review readiness, or infer runtime/compatibility results from topology alone.
- `domain-modeling` owns shared business language, ambiguity, rules, and relevant boundary scenarios. Lifecycle and bounded contexts are conditional depth, not default output; technical DDD, APIs, databases, frontend/backend structure, and source changes remain outside its boundary. It may update only an existing durable fact source with explicit authorization.
- `ui-design` owns concrete Feature UI by default: visual and interaction design for one page or flow plus a `dev-frontend` handoff. Its conditional Design System profile owns shared tokens, component semantics, variants, and overall visual-language changes. Host image tools render images; `ui-design` constrains and evaluates them without claiming runtime execution.
- General planning and diagnosis belong to the host's built-in capabilities plus effective personal and repository instructions. Do not publish a Skill for a workflow that can be expressed reliably as concise guidance without specialized knowledge, tooling, bundled resources, or a distinct authority boundary.
- `repo-review` owns three read-only bases: current Worktree/index, fixed immutable SHA/range, and verified review package. Pull requests resolve to fixed base/head SHAs; Release is a conditional profile over a fixed basis, not a separate basis. It owns dirty-tree readiness in Worktree mode and consolidated P0-P3 findings in fixed modes.
- `audit-security` owns bounded security assessment and may act as a specialist under `repo-review`; it does not replace the coordinator.
- `ask-chatgpt` owns local ChatGPT request packages and explicitly authorized ChatGPT web collaboration after a Codex-first gate. Content themes remain separate from verified Standard Chat, Search, Deep Research, Images, or reviewer-browser capabilities. It defaults authorized transport to the desktop built-in browser; Current Chrome or standalone browser use requires an explicit request for that route.
- `repo-delivery` is the sole owner of staging, categorized commits by default, explicit single commits, pushes, evidence-based branch integration, cleanup, and other Git mutation after review acceptance.
- Do not use unclear abbreviations such as `imp-*` or mix `<domain>-implementation` with `dev-<domain>`.
- `description` must start with `Use when`.
- `description` must describe trigger conditions, not the full workflow.
- Quote frontmatter string values when they contain YAML-significant punctuation such as `: `.
- Keep the frontmatter concise and within the repository policy in
  [`../../contracts/skill-validation.json`](../../contracts/skill-validation.json).
- Do not use long `Triggers include ...` lists in frontmatter. Put rich trigger examples in `references/usage.md` and `references/eval-cases.md`.
- Use English trigger phrases and realistic user wording by default for public, reusable skills. Add localized triggers only when the skill is explicitly audience-specific.
- Use only the current catalog names in packages, metadata, routing examples, and installation documentation.

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

- React, Vue Composition, Vue Options, UI/Design System implementation checks, accessibility, performance, and Tauri checks remain profiles inside `audit-frontend`.
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
Keep package-maintenance instructions only in `skills/AGENTS.md`; repository
standards should link to that authority rather than repeat its commands.

## Execution Economy

- Start with one primary owner and no handoff. Add one only when another Skill must
  act now to complete the requested outcome.
- Load `SKILL.md` first and only references selected by the active mode, profile,
  risk, or artifact. Do not read every reference as initialization.
- Use the smallest evidence set that can change the decision. Do not scan the full
  repository, generate a full map, run every profile, or repeat unchanged checks.
- Run focused validation for the changed slice first. Expand to repository baseline
  or risk overlays only when the boundary requires it.
- Reuse current task evidence until files, basis, environment, or requirements
  change. Do not rerun discovery, generation, or review for ceremony.
- Do not create tasks, threads, subagents, documents, or review rounds without a
  required independent result or explicit orchestration request.
- Continue non-blocked work and collect approval-dependent actions at the end. Stop
  early only when every safe in-scope path depends on approval.
- Keep output proportional: report decisions, evidence, changes, validation, and
  gaps; omit exhaustive inventories and repeated process narration.

## Predictable Instruction Design

- Treat every public description as context load and every extra public Skill as user cognitive load. Keep one owner/leading phrase per distinct intent; use profiles for branches that share authority and output.
- End each ordered step with a checkable completion condition. Prefer evidence such as a resolved basis, exhausted owned file set, observed red/green result, or explicit stop state over vague completion language.
- Keep each behavior in one authoritative source. Generate identical installed copies from a shared protocol instead of maintaining parallel references.
- Use branch-driven progressive disclosure: inline what every invocation needs and link only the references selected by the active mode, profile, risk, or artifact.
- During edits, remove no-op guidance, duplicated meaning, and stale sediment before adding prose. Use compact leading words such as `basis`, `seam`, `red`, `vertical slice`, and `fixed scope` when they make a gate more observable.

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

References must be self-contained when the published Skill needs them. When a
Skill needs prompt-derived templates, maintain those templates inside that
package before publishing; the catalog has no repository-level runtime prompt
library.

When multiple published skills require an identical protocol, keep one
repository source under `protocols/` and generate the self-contained package
copies with `scripts/sync-shared-protocols.py`. The generated copies remain part
of each published package; they are not independent authoring surfaces.

## Agent Metadata

Each published Skill must include `agents/openai.yaml` with:

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

- context, review, audit, and security skills are read-only unless their own documented artifact boundary explicitly permits a local output file;
- `dev-*` may edit task-owned source but must not stage, commit, push, or create PRs;
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
- `audit-frontend` versus `repo-review` and `dev-frontend`.

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

- `npx skills add https://github.com/idaibin/skills`
- `npx skills update --project` for current-project installations;
- `npx skills update --global` for global installations, including shared Codex and Claude Code installs.

Do not add package-local self-update modes, remote-source files, or custom update workflows unless a future source-maintenance workflow explicitly needs them. Document install and update behavior in `README.md` and `INSTALL.md`, not inside each skill package.

Root installation documentation must distinguish CLI-tracked installs from
manual copies, state that update is scope-based rather than agent-filtered, and
include explicit remove-and-add instructions for every published skill rename
or merge. Keep Codex and Claude Code on the same standard CLI flow; do not
maintain provider-specific update instructions inside individual packages.

## Validation Checklist

Use the targeted/full validation matrix in `skills/AGENTS.md`; it is the single
command authority. Also inspect the changed package's metadata, file inventory,
local links, and stale trigger phrases. `Triggers include` must not appear. Verify:

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

After publishing, users install with `npx skills add https://github.com/idaibin/skills` and update installed copies with `npx skills update --project` or `npx skills update --global`. Use `--list` only to inspect source discoverability and `npx skills list` to inspect installed skills.

For skills.sh repository pages, use root-level `skills.sh.json` only for display grouping. It does not change CLI install behavior or any `SKILL.md` content.

## Review Rubric

- Pass: required structure, metadata, authority, routing, references, evals, and validation are satisfied.
- Needs attention: usable, but has wording drift, stale examples, weak pairwise routing, missing profile selection, or incomplete validation guidance.
- Fail: missing package files, unsafe write behavior, ambiguous mutation owner, required external dependency, broad staging by default, direct remote overwrite, or misleading trigger metadata.
