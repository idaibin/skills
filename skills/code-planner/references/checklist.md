# Code Planner Checklist

Use this checklist when applying `code-planner` to split codebase requirements into executable and verifiable tasks. Chinese trigger phrases include `代码计划`, `任务拆分`, `可执行`, `可验证`, `子代理`, `审查`, and `打回`.

## Grounding Checklist

1. Read repo guidance:
   - root `AGENTS.md`
   - nearest subproject `AGENTS.md`
   - `AGENT.md` fallback
   - repo rules supplied in the chat
2. Run `git status --short`.
3. Read directly related docs, specs, command files, configs, manifests, route definitions, schemas, API wrappers, tests, and source entry points.
4. Verify runtime, logs, API behavior, browser state, database state, or build output when the task depends on real current behavior.
5. Mark missing files, commands, tools, or runtime evidence as `Not found` or `Not verified`.

## Dirty Tree Ownership Checklist

When local changes already exist:

1. Classify files as `task-owned`, `related-existing`, `unrelated-existing`, or `unknown`.
2. Mark current-session or explicitly requested edits as `task-owned`.
3. Mark pre-existing edits required by the requested work as `related-existing`; these may be modified directly after reporting why they belong to the task.
4. Mark pre-existing unrelated edits as `unrelated-existing`; protect them from edits, staging, commits, and subagent ownership.
5. If a pre-existing change is related but not obviously necessary, inspect the diff before deciding whether it is `related-existing`, `task-owned`, or `unrelated-existing`.
6. Report any `unknown` files that may affect the plan before assigning agents, staging, or committing.
7. Keep staging and commit scopes exact even when task-owned or related-existing files had pre-existing edits.

## Task Package Template

Use this template for each main-thread or subagent task. Keep it concrete enough that a worker can execute it without guessing, and narrow enough that a reviewer can reject it cleanly.

```text
Task: <short task name>
Type: <feature | bugfix | refactor | migration | review | contract-impact>
Owner model: <main-thread | sequential-main-thread | subagent-role>
Objective:
  <behavior or outcome this task completes>
Required reads:
  - <repo guidance, docs, diffs, code entry points, configs, commands, contracts, logs, runtime state>
Owned scope:
  - <exact files, modules, APIs, pages, docs, commands, task-owned changes, or related-existing changes allowed to change>
Do not touch:
  - <unrelated-existing local changes, adjacent modules, generated files, broad refactors, other owner scopes>
Dependencies:
  - <prior task, decision, data, runtime, schema, or contract needed first>
Implementation steps:
  1. <step>
  2. <step>
Validation:
  - <exact command, probe, screenshot, API call, manual check, or review gate>
Done criteria:
  - <observable evidence that proves completion>
Reject conditions:
  - <failed validation, missing evidence, scope drift, contract drift, unrelated edits, unclear ownership>
```

For `contract-impact` tasks, the plan should only mark the risk and required downstream review. Do not paste the full interface review checklist into the task package; require `code-review` before commit for the complete chain check.

## Task Split Checklist

Each task should answer:

- What behavior or outcome does this complete?
- What exact required reads must happen before implementation?
- What exact files, modules, APIs, pages, docs, commands, or pre-existing related changes does it own?
- What exact files, local changes, modules, generated outputs, or refactors are explicitly out of scope?
- What prior task or decision must happen first?
- What implementation steps are required?
- What exact validation proves it works?
- What evidence means the task is done?
- What failure condition sends it back for rework?

## Subagent Decision Checklist

Use subagents only when:

- the user explicitly asks for or allows subagents, delegation, or parallel agents
- subagent tools are available
- tasks are independent and have disjoint write scopes or read-only review surfaces
- the main thread can define bounded prompts and audit the result

Stay sequential when:

- the user forbids subagents
- delegation tools are unavailable
- the work is tightly coupled
- the next critical-path step must be done locally
- ownership cannot be made clear

## Task Type Checklist

- Feature work: split by vertical behavior, API/page pair, module, or user workflow.
- Contract-impact work: mark the task as `contract-impact`, identify affected interface surfaces, and require downstream `code-review` for the complete pre-commit chain review. `code-planner` should not duplicate that full checklist.
- Refactor work: split by ownership boundary and preserve visible behavior explicitly.
- Migration work: split by compatibility boundary, build gate, and rollback boundary.
- Review work: split by changed-file group, API contract surface, UI surface, runtime behavior, or commit group.
- Bugfix work: reproduce first, isolate cause, patch narrowly, then add or run regression checks.

## Review And Reject Checklist

The main thread should verify:

- returned changes are within owned scope
- unrelated local changes were not reverted or staged
- required docs, types, wrappers, routes, tests, and config were updated together
- validation commands or probes match the changed surface
- failures are fixed or explicitly reported
- runtime or contract claims are backed by evidence
- commit or staging scopes are exact and path-limited

Reject work when:

- validation failed or was skipped without explanation
- scope expanded without approval
- a subagent changed another owner scope
- API or UI behavior drifted from the requirement
- output lacks concrete file paths, commands, or evidence
- the result cannot be independently reviewed
