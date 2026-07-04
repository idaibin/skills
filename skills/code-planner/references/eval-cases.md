# Eval Cases

Use these cases when changing `code-planner` triggers, task contracts, owner models, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Split this migration into executable, verifiable tasks.` | Should trigger `code-planner`. | Planning and validation gates. |
| `Plan first; do not edit yet.` | Should trigger `code-planner`. | Explicit planning before implementation. |
| `Use multiple subagents for implementation, review, and commit readiness.` | Should trigger `code-planner`. | Delegated planning. |
| `No subagents; keep it sequential in the main thread, but plan first.` | Should trigger sequential mode. | Explicit no-delegation override. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review all local changes and split commits.` | Should prefer `code-review`. | Dirty-tree review. |
| `Check whether the current changes are ready to commit.` | Should prefer `code-review`. | Existing local changes are review scope. |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Open the app in a browser and check console/network errors.` | Should prefer `ops-browser`. | Browser operation task. |
| `Fix this button style directly.` | Should not require `code-planner` unless planning is requested. | Simple implementation. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Task package | Includes required reads, owned scope, do-not-touch, dependencies, steps, validation, done criteria, and reject criteria. | Leaves hidden decisions or no validation. |
| Subagent plan | Uses subagents only when tools are available, scopes independent, ownership clear, and audit possible. | Delegates forbidden, unnecessary, unclear, or tightly coupled work. |
| Contract-impact | Marks risk and routes final chain review to `code-review`. | Pretends planning replaces commit review. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
