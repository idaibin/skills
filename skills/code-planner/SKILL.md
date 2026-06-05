---
name: code-planner
description: Use when planning codebase work, splitting implementation/refactor/migration/review tasks into independent executable and verifiable units, coordinating subagents when explicitly allowed, defining review/reject gates, or handling 代码计划, 可执行, 可验证, 任务拆分, 子代理, 审查, 打回 requests.
---

# Code Planner

## Overview

Turn a codebase requirement into scoped work units that can be implemented, reviewed, verified, and accepted without hidden decisions. Ground every plan in the current repository and keep the main thread accountable for final review.

## Workflow

1. Read repository guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md` as fallback, or repo rules supplied in the chat.
2. Check `git status --short` before planning writes, assigning work, staging, or committing.
3. Inspect directly related docs, code, configs, schemas, API contracts, routes, tests, runtime state, logs, or command definitions. Do not infer contracts from file names alone.
4. Separate discoverable repo facts from product intent. Ask only when a choice cannot be discovered locally and materially changes the plan.
5. Split work into independent task packages with required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria.
6. Choose the execution model:
   - **Sequential mode:** default when subagents are forbidden, unavailable, unnecessary, or the work is tightly coupled.
   - **Subagent mode:** use only when the user explicitly asks for or allows subagents and tasks can be owned independently.
   - **Review-only mode:** use when the user asks to inspect, judge feasibility, or review current changes before implementation.
   - **Upgrade mode:** use when the user asks to update this skill from a trusted upstream source.
7. For large feature work, prefer a gate pattern per feature: implementation or analysis, review, submit-readiness judgment, then main-thread integration.
8. The main thread must inspect outputs, diffs, and evidence; run or confirm matching validation; and reject incomplete work before declaring completion.

## Task Contract

Each task must include:

- Objective: the behavior or outcome this task completes.
- Required reads: repo guidance, docs, code, diffs, configs, commands, routes, schemas, or runtime evidence that must be inspected before work starts.
- Owned scope: files, modules, APIs, pages, docs, commands, and pre-existing related changes the task may modify.
- Do not touch: unrelated files, local changes, generated outputs, or adjacent refactors that must stay protected.
- Dependencies: prior tasks, decisions, data, docs, contracts, or runtime state needed first.
- Implementation steps: concise ordered actions with no unresolved design choices.
- Validation: exact commands, probes, screenshots, API calls, review checks, or manual checks.
- Done criteria: observable evidence that satisfies the requirement.
- Reject criteria: conditions that require rework, such as failed validation, contract drift, unrelated edits, unclear ownership, missing tests, or unverified runtime claims.

Prefer small vertical slices that can be verified alone. For interface-heavy work, mark the task as `contract-impact` during planning only. Do not duplicate the complete interface review checklist here; require downstream `code-review` before commit to perform the full chain review across backend route/schema, request helper, type definitions, page calls, data shaping, and real payload behavior.

## Hard Rules

- Do not use subagents unless the user explicitly asks for or allows delegation and a subagent tool is available.
- Do not use subagents for tightly coupled or immediately blocking work that the main thread must resolve first.
- Do not modify or revert unrelated local changes.
- Dirty-tree ownership must be explicit: mark current-session/requested files as `task-owned`; mark pre-existing edits required by the requested scope as `related-existing`; mark unrelated edits as `unrelated-existing`; mark unclear files as `unknown`.
- If `related-existing` local changes are required for the requested work, modify them directly after reporting why they belong to the task; protect unrelated changes, not necessary changes.
- If pre-existing local changes are related but ownership is unclear, inspect enough diff to decide whether they are `related-existing`, `task-owned`, or protected outside changes before assigning or editing.
- Do not broaden scope because a related refactor looks useful.
- Do not claim a task is complete until its validation and main-thread review pass.
- Do not accept subagent output without inspecting the returned findings, diffs, or artifacts.
- If the user forbids subagents, execute the same task list sequentially in the main thread.
- If a required file, command, tool, browser, or runtime is missing, say `Not found` or `Not verified`; do not silently substitute another one.
- Keep staging, commits, and pushes path-limited unless the user explicitly requests a broader scope.

## Upgrade Mode

Use this mode when the user asks to update `code-planner` from GitHub, another remote source, or a specific branch, tag, commit, directory, or file URL. Read [`references/upstream-sources.md`](references/upstream-sources.md), inspect remote content read-only, compare only the matching remote `skills/code-planner/` package, preview proposed changes and rejected candidates, and write only after the user explicitly confirms or asks for implementation.

## Output Contract

- Prefer concise Chinese final responses unless the user asks for another language.
- Start with verified current state and any missing or dirty-tree risks.
- Provide a task list with owner model: main thread, subagent role, or sequential main-thread step.
- For each task, include required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria.
- Include integration and final review gates.
- State assumptions, unresolved decisions, explicit non-goals, and anything `Not verified`.
- During execution, keep a live checklist and update statuses as tasks complete.

## References

See [`references/checklist.md`](references/checklist.md) for the detailed planning and review checklist.
See [`references/usage.md`](references/usage.md) for trigger examples and expected outputs.
See [`references/upstream-sources.md`](references/upstream-sources.md) for trusted source metadata.
See [`references/upgrade-workflow.md`](references/upgrade-workflow.md) for the remote update process.
