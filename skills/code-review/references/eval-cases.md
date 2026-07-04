# Eval Cases

Use these cases when changing `code-review` triggers, ownership labels, staging rules, commit behavior, contract-review scope, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review all changes and split commits.` | Should trigger `code-review`. | Full dirty-tree review. |
| `Commit only the current session changes locally, but do not push.` | Should trigger `code-review`. | Scoped local commit after full review. |
| `Review the API contract chain; check fields from backend to page.` | Should trigger `code-review`. | Contract-chain review. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Split this requirement into executable tasks.` | Should prefer `code-planner`. | Forward planning. |
| `This feature is not written yet; split it into an implementation plan first.` | Should prefer `code-planner`. | Future implementation planning. |
| `Review this endpoint for token leakage and authorization risk.` | Should prefer `code-security` after the target surface is clear. | Security-only review. |
| `Verify the real desktop client window with CGWindowID.` | Should prefer `ops-client`. | Desktop-client evidence task. |
| `Review, commit, push, then squash this branch into main.` | Should prefer `code-delivery` after review scope is clear. | End-to-end delivery and remote sync. |
| `Implement this feature directly; no review needed.` | Should not require `code-review`. | Implementation task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Full dirty-tree review | Runs status, diff stat, name-status, and cached equivalents when staged files exist. | Reviews only a subset without reporting full scope. |
| Ownership and mixed hunks | Labels ownership, marks `mixed-hunk`, avoids whole-file staging, and verifies staged diff. | Stages mixed files with whole-file `git add`. |
| Minimal scope | Walks candidate diff lines for task necessity and excludes opportunistic cleanup or future-flexibility changes. | Includes unrelated cleanup because it was nearby. |
| Contract-chain review | Traces route/method/fields to helpers, types, callers, shaping, and runtime evidence or `Not verified`. | Stops at endpoint names. |
| Commit plan | Groups by semantic unit with exact staging scope, validation status, risks, and commit messages. | Uses broad staging or auto-commits. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
