# Eval Cases

Use these cases when changing `code-planner` triggers, task contracts, owner models, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Split this migration into executable, verifiable tasks.` | Should trigger `code-planner`. | Planning and validation gates. |
| `Plan first; do not edit yet.` | Should trigger `code-planner`. | Explicit planning before implementation. |
| `Use multiple subagents for implementation, review, and commit readiness.` | Should trigger `code-planner`. | Delegated planning. |
| `No subagents; keep it sequential in the main thread, but plan first.` | Should trigger sequential mode. | Explicit no-delegation override. |
| `Plan this module move and include manifests, exports, tests, CI, docs, indexes, and rollback.` | Should trigger `code-planner`. | Structure-impact planning. |
| `Classify this one-file private helper change before planning it.` | Should select Small and keep a compact sequential plan. | One bounded owner with no useful split. |
| `Plan this schema migration where API and client both depend on an unfrozen DTO.` | Should select Coupled and keep interface-changing work sequential. | Shared mutable contract. |
| `Plan independent frontend copy, Rust docs, and CI fixture changes with disjoint files and checks.` | Should select Parallelizable and define audited subagent scopes. | Independent write ownership and validation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review all local changes and split commits.` | Should prefer `repo-review`. | Dirty-tree review. |
| `Check whether the current changes are ready to commit.` | Should prefer `repo-review`. | Existing local changes are review scope. |
| `Understand this repository's real commands and directory structure first.` | Should prefer `repo-map`. | Repository mapping. |
| `Open the app in a browser and check console/network errors.` | Should prefer `ops-browser`. | Browser operation task. |
| `Fix this button style directly.` | Should not require `code-planner` unless planning is requested. | Simple implementation. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Task package | Includes required reads, owned scope, do-not-touch, dependencies, steps, validation, done criteria, and reject criteria. | Leaves hidden decisions or no validation. |
| Subagent plan | Uses subagents only when tools are available, scopes independent, ownership clear, and audit possible. | Delegates forbidden, unnecessary, unclear, or tightly coupled work. |
| Small classification | Compresses one bounded owner and no contract migration into a concise sequential plan. | Creates several ceremonial tasks or subagents for one surface. |
| Coupled classification | Names shared mutable files, unfrozen interfaces, migration order, or a shared validation loop and keeps that work sequential. | Parallelizes writers across the same contract or calls all multi-file work coupled without evidence. |
| Parallelizable classification | Uses at least two disjoint write scopes with explicit interfaces, independent artifacts/checks, and main-thread integration; it may still honor an explicit no-subagents override. | Keeps independent scopes sequential without a concrete risk/user override/tool gap, or delegates overlapping writers. |
| User delegation override | Honors explicit `No subagents` even when scopes are technically Parallelizable, records the override, and preserves the same task boundaries for sequential execution. | Delegates against the user's instruction or falsely reclassifies independent scopes as Coupled. |
| Contract-impact | Marks risk and routes final chain review to `repo-review`. | Pretends planning replaces commit review. |
| Structure-impact | Identifies project class and includes manifest, export, command, test, CI/deploy, docs, index, stale-reference, and migration/rollback work. | Treats a directory move as source-only renaming. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
