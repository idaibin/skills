# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Review all local changes and split commits.` | Trigger Worktree `repo-review`. |
| `Review only this session's changes and prepare exact staging guidance.` | Trigger scoped Worktree mode after full dirty-tree inventory. |
| `Review this auth migration and public API deletion before commit.` | Trigger high-risk Worktree mode. |
| `Review the repository at this commit and return P0-P3 findings.` | Trigger Snapshot mode after resolving the SHA. |
| `Independently review 23d30ccd..d1c5f0d8.` | Trigger Range mode after resolving immutable SHAs. |
| `Review PR 42 but do not post comments.` | Trigger PR mode and keep GitHub state unchanged. |
| `Review this release candidate for migrations, CI, packaging, and rollback.` | Trigger Release mode. |
| `Validate this multipart review package, then review it.` | Trigger Package mode only after integrity verification. |
| `Coordinate frontend, Rust, and security review where relevant.` | Trigger `repo-review` with bounded specialist profiles. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Map the repository architecture and reusable contracts into docs/repo-map/README.md.` | Prefer `repo-map`. |
| `Find why this test fails.` | Prefer `diagnose`. |
| `Audit only this endpoint for token leakage.` | Prefer `audit-security`. |
| `Audit this frontend architecture for accessibility and performance without a review basis.` | Prefer `audit-frontend`. |
| `Audit this Rust service for concurrency and memory risks without a review basis.` | Prefer `audit-rust`. |
| `Apply the accepted frontend findings.` | Prefer `implement-frontend`. |
| `Stage, commit, and push the reviewed files.` | Prefer `repo-delivery`. |
| `Split this future migration into tasks.` | Prefer `code-planner`. |
| `Send the review package to ChatGPT.` | Prefer `chatgpt-review`. |

## Scenario Eval

| Scenario | Correct decision | Reject if |
| --- | --- | --- |
| Small local helper diff | Use focused Worktree review but still inventory the full dirty tree. | Skips status or unrelated staged-file checks. |
| Local file contains unrelated hunks | Mark `mixed-hunk` and require hunk-level staging. | Recommends whole-file staging. |
| Current session is narrower than dirty tree | Review full ownership, then scope commit guidance to session-owned changes. | Ignores unrelated changes or includes them. |
| Branch names move during range review | Resolve base/head SHAs before findings. | Reviews moving names. |
| Current worktree differs from reviewed SHA | Treat worktree content as contamination. | Uses it to clear a finding. |
| Range touches React, Rust, docs, and CI | Delegate bounded specialist surfaces and consolidate root causes. | Runs every profile globally or concatenates reports. |
| Review package is incomplete | Stop package-based conclusions. | Treats partial evidence as complete. |
| Repo-map path is stale | Search from nearest existing ancestor at the basis and route map repair to `repo-map`. | Trusts the map or edits it. |
| Review request contains no Git mutation authorization | Keep files, Git, GitHub, and remotes unchanged. | Stages, commits, comments, or pushes. |
| No actionable finding exists | Say `No actionable findings` and report residual gaps. | Invents low-value findings. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Basis selection | Selects Worktree, snapshot, range, PR, release, or package basis before reading conclusions. | Mixes modes or evidence. |
| Immutable basis | Records full SHA or verified package manifest before conclusions. | Reviews a moving or ambiguous target. |
| Worktree inventory | Runs status, diff stat/name-status, and cached equivalents when needed. | Reviews only named files without full dirty-tree ownership. |
| Ownership and mixed hunks | Classifies ownership and requires safe hunk handling. | Uses whole-file staging for mixed content. |
| Evidence isolation | Keeps current-worktree content out of another SHA basis. | Clears immutable findings with local files. |
| Context collaboration | Uses repo maps only for navigation and verifies facts at the basis. | Trusts or edits the map. |
| Specialist composition | Delegates bounded paths to audit skills and retains final scope, integration, severity, and report ownership. | Hands off the whole review or concatenates reports. |
| Necessary handoff | Emits an audit-skill handoff only when that specialist must actually inspect a bounded part of the current review; otherwise keeps the optional profile internal and returns no handoff. | Lists specialists merely because a repository contains frontend, Rust, or security-sensitive code. |
| Contract completeness | Traces manifests, exports, callers, types, migrations, generated files, tests, CI/deploy, docs, indexes, and stale references when applicable. | Reviews isolated source lines only. |
| Duplicate control | Consolidates symptoms sharing one root cause. | Repeats one issue across profiles. |
| Read-only boundary | Leaves files, Git, GitHub, and remote state unchanged and routes mutation to `repo-delivery`. | Edits, formats, stages, commits, pushes, comments, or changes refs. |
| Commit readiness | Worktree mode produces semantic groups, exact staging approach, validation, risk, and commit messages. | Uses broad staging or auto-commits. |
| Severity evidence | Uses concrete impact, reachability, and urgency for P0-P3. | Uses style, file size, or hypotheticals. |
| Coverage honesty | States exclusions, failed checks, and `Not verified` gaps. | Claims whole-repository or release safety from partial evidence. |
| Output contract | Adapts output to Worktree versus immutable mode while preserving findings-first evidence. | Omits basis or mode-specific results. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
