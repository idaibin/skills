# Eval Cases

Use these cases when changing `code-review` triggers, ownership labels, staging plans, review depth, specialist subreviews, contract-review scope, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review all changes and split commits.` | Should trigger Standard `code-review`. | Full dirty-tree review. |
| `Review this two-line private helper change; keep the review focused but still check the dirty tree.` | Should trigger Focused review. | Small bounded diff with full ownership inventory. |
| `Review this auth migration and public API deletion before commit.` | Should trigger High-risk review. | Security, migration, API, and destructive structure. |
| `Review only the current session changes and prepare exact staging instructions.` | Should trigger commit-readiness review. | Scoped read-only review and delivery plan. |
| `Review the API contract chain; check fields from backend to page.` | Should trigger `code-review`. | Contract-chain review. |
| `Review this module deletion and confirm manifests, exports, CI, docs, and indexes are clean.` | Should trigger `code-review`. | Structural completeness review. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Split this requirement into executable tasks.` | Should prefer `code-planner`. | Forward planning. |
| `This feature is not written yet; split it into an implementation plan first.` | Should prefer `code-planner`. | Future implementation planning. |
| `Review this endpoint for token leakage and authorization risk.` | Should prefer `code-security` after the target surface is clear. | Security-only review. |
| `Verify the real desktop client window with platform-specific evidence.` | Should prefer `ops-client`. | Desktop-client evidence task. |
| `Review, commit, push, then squash this branch into main.` | Should prefer `code-delivery` after review scope is clear. | End-to-end delivery and remote sync. |
| `These changes are already reviewed; stage and commit them locally without pushing.` | Should prefer `code-delivery`. | Git mutation belongs to delivery. |
| `Implement this feature directly; no review needed.` | Should not require `code-review`. | Implementation task. |
| `Audit this Rust service for concurrency, memory, and SQLite risks without changing code.` | Should prefer `audit-rust`. | Domain-wide read-only audit. |
| `Audit this frontend architecture for reuse, state, accessibility, and performance.` | Should prefer `audit-frontend`. | Domain-wide read-only audit. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Review-depth selection | Selects Focused, Standard, or High-risk from concrete diff boundaries and risk surfaces; explains why. | Uses file count alone or performs a full architecture audit for every tiny diff. |
| Full dirty-tree review | Runs status, diff stat, name-status, and cached equivalents when staged files exist regardless of selected depth. | Focused mode skips dirty-tree inventory or ignores unrelated staged files. |
| Focused review | Reads the complete small diff, immediate callers/tests and staging scope while avoiding irrelevant domain checklists. | Treats focused as permission to skip ownership, tests, or complete diff inspection. |
| High-risk review | Adds relevant auth, migration, public API, concurrency, unsafe, release, deletion, generated-file, and compatibility evidence. | Reviews a destructive or security-sensitive change as ordinary style work. |
| Specialist composition | Keeps `code-review` as the read-only Git-change review coordinator while requesting a bounded frontend, Rust, or security subreview only for the changed surface. | Sends the whole review workflow to an audit skill or skips required domain evidence. |
| Read-only review boundary | Leaves worktree files and Git state unchanged, runs only non-mutating checks, and proposes exact fix and delivery instructions. | Edits/creates/deletes/renames/formats files, runs write-mode checks, stages, unstages, commits, pushes, or rewrites refs. |
| Ownership and mixed hunks | Labels ownership, marks `mixed-hunk`, avoids whole-file staging, and verifies staged diff. | Stages mixed files with whole-file `git add`. |
| Minimal scope | Walks candidate diff lines for task necessity and excludes opportunistic cleanup or future-flexibility changes. | Includes unrelated cleanup because it was nearby. |
| Contract-chain review | Traces route/method/fields to helpers, types, callers, shaping, and runtime evidence or `Not verified`. | Stops at endpoint names. |
| Structural completeness | Verifies manifests, exports, commands, tests, CI/deploy paths, docs, indexes, generated files, migrations, consumer ownership, and stale references when applicable. | Reviews source diff only or accepts speculative shared extraction. |
| Severity evidence | Ranks findings by concrete impact and reachability. | Uses file size, style preference, or hypothetical future use as severity. |
| Commit plan | Groups by semantic unit with exact staging scope, validation status, risks, and commit messages. | Uses broad staging or auto-commits. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
