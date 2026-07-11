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
| `repo-context` | repository facts and ownership map | read-only by default; doc write only after explicit request | commands, paths, project class, reuse candidates, alignment gaps |
| `code-planner` | future implementation requirement | read-only | executable tasks, dependencies, owners, validation and reject gates |
| `diagnose` | concrete failure symptom | read-only for tracked repository and Git state | reproduction loop, confirmed cause, regression seam, implementation handoff |
| `code-review` | current local worktree and index changes | read-only | findings, ownership, mixed hunks, commit groups, exact staging plan |
| `repo-review` | immutable repository snapshot/range/PR/release/package | read-only | consolidated P0-P3 findings and verification scope |
| `implement-frontend` | requested frontend source change | source mutation | implemented and validated frontend change |
| `implement-rust` | requested Rust source change | source mutation | implemented and validated Rust change |
| `audit-frontend` | selected frontend domain profiles | read-only | bounded frontend findings and validation gaps |
| `audit-rust` | selected Rust domain profiles | read-only | bounded Rust findings and validation gaps |
| `audit-security` | known security-sensitive surface | read-only | scoped security findings and threat sketch |
| `code-delivery` | reviewed local Git changes | Git mutation | staged/committed/pushed/synchronized refs and proof |
| `ops-browser` | browser session/page state | authorized browser actions | browser evidence and state-change report |
| `ops-client` | real desktop client process/window | authorized client actions | process/window/runtime evidence |
| `chatgpt-review-bridge` | external ChatGPT review round | authorized external action | routed package, attributed response, local verification |
| `human-writing` | supplied technical draft | text transformation | edited publication-ready text |

## `repo-context`, `code-review`, And `repo-review`

These remain separate even though all inspect repository files.

### `repo-context`

Answers:

- What exists?
- Where is the real entry point or owner?
- Which implementation can be reused or used as a reference?
- Do project docs and current structure agree?

It stops when the requested facts are supported. It does not rank defects or determine commit/release safety.

### `code-review`

Answers:

- What changed in the current local worktree/index?
- Which changes belong to this task?
- Are there mixed hunks or unrelated staged files?
- Are contracts and structural lifecycle complete?
- How should the changes be staged and committed safely?

Its primary object is local uncommitted state. It never claims whole-repository or branch-range coverage.

### `repo-review`

Answers:

- What actionable defects exist in a fixed repository snapshot, branch comparison, commit range, PR, release candidate, or verified review package?
- Which findings should block merge or release?
- How do frontend, Rust, security, CI, tests, docs, and structural evidence integrate?

It fixes an immutable review basis, coordinates bounded specialists, consolidates duplicate root causes, and outputs P0-P3 findings. It does not own local staging or commit readiness.

## Security Audit

`audit-security` remains separate from review coordinators because its primary object is a known security-sensitive surface and its output is a bounded security assessment.

- Under `code-review`, it inspects only delegated local changed paths and returns findings to the dirty-tree coordinator.
- Under `repo-review`, it inspects only delegated immutable paths/ranges and returns findings to the repository-review coordinator.
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
  -> code-review checks the resulting local diff
  -> code-delivery performs authorized Git mutation
```

This preserves continuous execution without merging investigation and implementation permissions.

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

## Routing Review Checklist

Before publishing a skill change:

- confirm the description starts with `Use when` and names the real user intent;
- confirm `Do Not Use For` names the closest competing skills;
- confirm metadata routes to the same owner and mutation boundary as `SKILL.md`;
- add pairwise trigger/non-trigger cases for every nearest neighbor;
- ensure only `code-delivery` owns Git mutation;
- ensure audits and reviews remain read-only;
- ensure implementation skills do not claim staging, commit, push, or PR ownership;
- ensure external/browser actions require their own explicit authorization;
- run targeted and full validation.
