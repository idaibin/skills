---
name: code-planner
description: "Use when future codebase work needs a plan before implementation: split requirements into scoped executable tasks with owners, dependencies, validation gates, reject criteria, and auditable subagent coordination."
---

# Code Planner

## Overview

Turn a codebase requirement into scoped work units with required reads, owned scope, validation, done criteria, and reject gates. Prefer the least complex owner model that preserves correctness; use subagents only when their outputs can be isolated and independently audited.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Run `git status --short` before planning writes, assigning work, staging, or committing.
3. Inspect only the docs, code, diffs, contracts, commands, logs, or runtime state needed to make the plan executable.
4. Identify project class, repository standards, protected paths, and whether the work adds, reuses, moves, renames, or deletes a structural boundary.
5. Classify complexity before splitting work:
   - **Small:** one owner, one bounded surface, no contract migration; use a compact sequential plan or proceed directly when the user did not request planning.
   - **Coupled:** several steps share mutable files, interfaces, or validation; keep execution sequential under one owner.
   - **Parallelizable:** at least two independent scopes with explicit interfaces, disjoint write ownership, and independently reviewable outputs.
6. Split only where the boundary reduces integration risk. Do not create task packages merely to satisfy a preferred count.
7. For every task package, name required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria.
8. Choose the owner model using the gates below.
9. Keep the main thread responsible for interface decisions, integration, returned-output inspection, final validation, and acceptance.
10. Record assumptions that could change task order or scope; do not present estimates or dependencies as verified when the repository does not prove them.

## Owner Model

- **Sequential mode:** default for small work, tightly coupled changes, shared files, uncertain interfaces, unavailable delegation tools, or tasks whose outputs cannot be independently verified.
- **Subagent mode:** use only when tools are available, there are at least two materially independent scopes, write ownership is disjoint or read-only, contracts are explicit, and the main thread can inspect each returned diff or artifact before integration.
- **Review-only mode:** use when the user asks to inspect, judge feasibility, or review before implementation.

Subagent mode must state:

- why parallel execution is safer or faster than sequential work;
- each agent's exact read and write scope;
- shared interfaces that no agent may change independently;
- expected artifact or diff;
- validation each agent must return;
- main-thread integration and rejection checks.

## Task Contract

Each task must include objective, required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria. Mark interface-heavy work as `contract-impact`; mark add/reuse/move/delete work as `structure-impact`. Route final chain and completeness review to `code-review` before commit.

For a small task, these fields may be compressed into a single concise block. Completeness does not require verbose repetition.

## Do Not Use For

- First-pass repository discovery, real commands, entry points, or docs alignment; use `code-context`.
- Existing local diff review, commit grouping, staging plans, or commit messages; use `code-review`. Actual staging, commits, or pushes belong to `code-delivery` after review.
- Direct implementation when the user asks for a small change and no plan.
- Browser/client operation or runtime evidence collection; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not modify or revert unrelated local changes.
- Label dirty files as `task-owned`, `related-existing`, `unrelated-existing`, or `unknown` before assigning or editing.
- Do not broaden scope because an adjacent refactor looks useful.
- Do not delegate merely because subagents are available.
- Do not classify work as Coupled merely because tasks read the same repository or share final integration. Parallelizable work may share read-only context when write ownership, interfaces, outputs, and acceptance checks remain independent.
- Do not keep genuinely independent, disjoint, auditable scopes sequential without naming a concrete integration/ownership risk, an explicit user no-delegation instruction, or unavailable delegation tools.
- Do not assign two writers to the same file, schema, migration, public interface, generated artifact, or branch unless one is explicitly review-only.
- Do not accept subagent output without inspecting returned findings, diffs, commands, and artifacts.
- If a required command, tool, browser, or runtime is missing, say `Not found` or `Not verified`; do not substitute silently.
- Require planned staging, commits, and pushes to stay path-limited unless the user explicitly requests broader scope, and assign their execution to `code-delivery` after review.
- For `structure-impact`, include manifests/workspace membership, module exports, commands, tests, CI/deploy paths, architecture/project-map docs, indexes, stale-reference search, and rollback or migration boundaries when applicable.
- Do not use task count, estimated duration, or agent count as a proxy for plan quality. A task is valid only when its ownership and acceptance can be tested.

## Output Contract

Start with verified current state, project class, standards, dirty-tree risks, complexity class, and selected owner model. Then provide task packages with dependencies, validation, done criteria, reject criteria, structure/contract integration gates, non-goals, assumptions, and `Not verified` items. When subagents are selected, include the delegation justification, write-conflict analysis, expected returned evidence, and main-thread integration checks.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, owner-model, task-contract, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/checklist.md](references/checklist.md) for planning and subagent decision details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
