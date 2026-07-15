# Skill Routing And Design Standard

This standard defines when AICraft should keep capabilities together, split them into public skills, or model them as internal profiles.

## Core Principle

A public skill represents a stable user intent and execution owner, not merely a technology name or checklist category.

Two capabilities should remain separate when they differ materially in:

1. **Primary object** — what is being acted on or judged.
2. **Authorization boundary** — read-only, source mutation, Git mutation, browser/external action, or document writing.
3. **Workflow** — the sequence of evidence, decisions, and stop conditions.
4. **Output contract** — the artifact or decision the user receives.
5. **Nearest non-triggers** — similar requests that must route elsewhere.

Framework-specific or domain-specific checks should stay as profiles when these five properties remain the same.

## Current Repository Routing

| Skill | Primary object | Mutation | Primary output |
| --- | --- | --- | --- |
| `repo-map` | workspace/repository semantics and reuse map | read-only by default; repo-map write only after explicit request | real boundaries, task routes, verified reuse entries, alignment gaps |
| `code-planner` | future implementation requirement | read-only | executable tasks, dependencies, owners, validation and reject gates |
| `diagnose` | concrete failure symptom | read-only for tracked repository and Git state | reproduction loop, confirmed cause, regression seam, implementation handoff |
| `repo-review` | local worktree/index or immutable snapshot/range/PR/release/package | read-only | basis-specific readiness, staging guidance, or consolidated P0-P3 findings |
| `implement-frontend` | requested frontend source change | source mutation | implemented and validated frontend change |
| `implement-rust` | requested Rust source change | source mutation | implemented and validated Rust change |
| `audit-frontend` | selected frontend domain profiles | read-only | bounded frontend findings and validation gaps |
| `audit-rust` | selected Rust domain profiles | read-only | bounded Rust findings and validation gaps |
| `audit-security` | known security-sensitive surface | read-only | scoped security findings and threat sketch |
| `repo-delivery` | reviewed local Git changes | Git mutation | staged/committed/pushed/synchronized refs and proof |
| `ops-browser` | browser session/page state | authorized browser actions | browser evidence and state-change report |
| `ops-client` | real desktop client process/window | authorized client actions | process/window/runtime evidence |
| `chatgpt-review` | external ChatGPT review package or round | local artifact write or authorized external action | prepared/routed package, attributed response, local verification |
| `human-writing` | supplied technical draft | text transformation | edited publication-ready text |

## `repo-map` And `repo-review`

These remain separate because context mapping may write navigation docs, while review is always read-only and evaluates change safety.

### `repo-map`

Answers:

- What exists?
- Where is the real entry point or owner?
- Which canonical component, function, type, or API can be reused, extended, or wrapped before declaring another one?
- Do project docs and current structure agree?

It stops when the requested facts are supported. It does not rank defects or determine commit/release safety.

### `repo-review`

Answers:

- What changed in the current local worktree/index, which changes belong to this task, and are there mixed hunks?
- How should reviewed local changes be grouped and staged safely?
- What actionable defects exist in a fixed repository snapshot, branch comparison, commit range, PR, release candidate, or verified review package?
- Which findings should block merge or release?
- How do frontend, Rust, security, CI, tests, docs, and structural evidence integrate?

It selects one review basis first. Worktree mode owns ownership, mixed hunks, commit readiness, and exact staging guidance; immutable modes resolve SHAs and own P0-P3 findings. All modes stay read-only and coordinate bounded specialists.

## Security Audit

`audit-security` remains separate from review coordinators because its primary object is a known security-sensitive surface and its output is a bounded security assessment.

- Under Worktree `repo-review`, it inspects only delegated local changed paths.
- Under immutable `repo-review`, it inspects only delegated fixed paths/ranges.
- Direct use is appropriate when the user requests only a scoped security audit after the target surface is known.
- It never takes over staging, commit readiness, whole-review severity integration, or Git mutation.

## Diagnosis And Implementation

`diagnose` owns uncertainty reduction, not permanent remediation.

For a combined request such as `diagnose and fix`:

```text
diagnose
  -> confirm exact cause and regression seam
  -> explicit implementation handoff
  -> matching implement-* skill applies the change
  -> repo-review checks the resulting local diff
  -> repo-delivery performs authorized Git mutation
```

This preserves continuous execution without merging investigation and implementation permissions.

## Cross-Skill Handoff Contracts

Cross-skill workflows must transfer bounded state without transferring
authority. The caller owns intent, authorization, scope, and the next-state
decision; the executor owns only its direct action and evidence.

For `chatgpt-review -> ops-browser -> chatgpt-review`, both
published packages carry the identical `browser-operation/v1` protocol. The
bridge owns the Capability requirements, Handoff Request, operation ledger,
`operation_id`, retry decision, rounds, and attribution. `ops-browser` owns the
measured Capability Snapshot and same-ID Handoff Result. An interruption with
uncertain side effects is `ambiguous` and must stop for reconciliation rather
than trigger a replacement operation.

`protocols/browser-operation-v1.md` is the repository authority;
`scripts/sync-shared-protocols.py` generates both published copies. Repository
validation rejects any copy that differs from that source.
Behavior evals must cover at least normal completion, failure before submit,
duplicate-submit prevention, ambiguous interruption, stale capability evidence,
and unauthorized handoff.

For `repo-map -> repo-review`, `repo-map` owns the durable semantic repo
map: current ownership and runtime boundaries, commands, shortest task routes,
and verified reuse entries with canonical owners, access/registration entries, consumers,
and constraints. `repo-review` may
use that map to select an initial read set, but independently verifies every
fact that affects a finding at its selected Worktree or immutable review basis. Missing mapped paths
are resolved from the nearest existing ancestor with a bounded subtree search;
the read-only reviewer records the mismatch and routes document repair back to
`repo-map`. This collaboration does not transfer P0-P3 authority.

## Public Skill Versus Internal Profile

Create a new public skill only when all of the following are true:

- a user can express a distinct intent without naming internal implementation details;
- it has a distinct authority or mutation boundary;
- at least a substantial part of its workflow and stop conditions differs from existing skills;
- its output contract is independently useful;
- it has at least three clear trigger and three clear non-trigger cases;
- the workflow has repeated across several real tasks or repositories.

Use an internal profile when the capability shares the same owner, evidence inventory, mutation boundary, and output format.

### Frontend Example

Keep these inside `audit-frontend`:

- React
- Vue Composition
- Vue Options
- architecture/reuse
- state/data/contracts
- component/layout/design system
- accessibility
- performance
- Tauri desktop boundary

Do not create `audit-react`, `audit-vue`, or `audit-ui` solely to divide checklists. The profiles frequently interact and use the same ownership map and report contract.

A future `audit-ux` could become separate only if it is primarily screenshot/Figma/runtime-experience based, can operate independently of source architecture, and has a distinct visual/product-experience output contract.

## Required Package Surfaces

Every public skill must keep these synchronized:

- `SKILL.md`
- `agents/openai.yaml`
- `references/eval-cases.md`
- all linked reference guidance
- `README.md`
- `INSTALL.md`
- `skills.sh.json`

Changes to triggers, authority, modes/profiles, output, or routing require pairwise evals against the closest neighboring skills.

The machine-readable nearest-neighbor inventory lives in
`docs/skills/routing-graph.json`. Every public package must appear in the graph,
every edge must be symmetric, and both endpoint packages must name the other in
their Trigger or Non-Trigger eval sections. An empty list is valid only when a
skill has no plausible routing competitor in the published suite.

## Routing Review Checklist

Before publishing a skill change:

- confirm the description starts with `Use when` and names the real user intent;
- confirm `Do Not Use For` names the closest competing skills;
- confirm metadata routes to the same owner and mutation boundary as `SKILL.md`;
- add pairwise trigger/non-trigger cases for every nearest neighbor;
- ensure only `repo-delivery` owns Git mutation;
- ensure audits and reviews remain read-only;
- ensure implementation skills do not claim staging, commit, push, or PR ownership;
- ensure external/browser actions require their own explicit authorization;
- run targeted and full validation.
