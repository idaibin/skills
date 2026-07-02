---
name: code-planner
description: Use when future codebase work needs a plan before implementation: split requirements into scoped executable tasks with owners, dependencies, validation gates, reject criteria, and auditable subagent coordination.
---

# Code Planner

## Overview

Turn a codebase requirement into scoped work units with required reads, owned scope, validation, done criteria, and reject gates. Use subagents by default only when delegation is safe and auditable.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Run `git status --short` before planning writes, assigning work, staging, or committing.
3. Inspect only the docs, code, diffs, contracts, commands, logs, or runtime state needed to make the plan executable.
4. Split work into independent task packages with required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria.
5. Choose the owner model.
6. Keep the main thread responsible for integration, review, and final acceptance.

## Owner Model

- **Subagent mode:** default when tools are available, task scopes are independent, ownership is clear, and main-thread audit is possible.
- **Sequential mode:** use when delegation is forbidden, unavailable, unnecessary, tightly coupled, immediately blocking, or ownership cannot be made clear.
- **Review-only mode:** use when the user asks to inspect, judge feasibility, or review before implementation.
- **Upgrade mode:** use when updating this skill from a trusted upstream source.

## Task Contract

Each task must include objective, required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, and reject criteria. Mark interface-heavy work as `contract-impact` and route final chain review to `code-review` before commit.

## Do Not Use For

- First-pass repository discovery, real commands, entry points, or docs alignment; use `code-context`.
- Existing local diff review, commit grouping, staging, or commit messages; use `code-review`.
- Direct implementation when the user asks for a small change and no plan.
- Browser/client operation or runtime evidence collection; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not modify or revert unrelated local changes.
- Label dirty files as `task-owned`, `related-existing`, `unrelated-existing`, or `unknown` before assigning or editing.
- Do not broaden scope because an adjacent refactor looks useful.
- Do not accept subagent output without inspecting returned findings, diffs, or artifacts.
- If a required command, tool, browser, or runtime is missing, say `Not found` or `Not verified`; do not substitute silently.
- Keep staging, commits, and pushes path-limited unless the user explicitly requests broader scope.

## Output Contract

Start with verified current state and dirty-tree risks. Then provide task packages with owner model, dependencies, validation, done criteria, reject criteria, integration gates, non-goals, assumptions, and `Not verified` items.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, owner-model, task-contract, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/checklist.md](references/checklist.md) for planning and subagent decision details.
- See [references/upstream-sources.md](references/upstream-sources.md) for trusted source metadata.
- See [references/upgrade-workflow.md](references/upgrade-workflow.md) for the upgrade process.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
