# Eval Cases

Use these cases when changing `code-delivery` triggers, modes, staging rules, push behavior, squash workflow, cleanup rules, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review the staged scope, commit, and push this branch.` | Should trigger `code-delivery`. | Commit plus push delivery. |
| `Push only the current branch after checking the diff.` | Should trigger `code-delivery`. | Current-branch remote delivery. |
| `Squash this completed branch into main and push main.` | Should trigger `code-delivery`. | Squash-to-main delivery. |
| `Sync this branch to remote; do not switch branches.` | Should trigger `code-delivery`. | Branch-specific remote sync. |
| `After verification, delete the temporary branch.` | Should trigger `code-delivery`. | Delivery cleanup. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and entry points first.` | Should prefer `code-context`. | Repository grounding. |
| `Split this future feature into tasks and owners.` | Should prefer `code-planner`. | Forward planning. |
| `Review all dirty changes and propose commit groups.` | Should prefer `code-review`. | Pre-delivery review scope is not clear. |
| `Check this endpoint for authorization risk.` | Should prefer `code-security` after scope is clear. | Security-only review. |
| `Verify this web page in the browser before release.` | Should prefer `ops-browser`. | Runtime browser evidence. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Dirty-tree safety | Runs status with branch, identifies staged/unstaged/untracked files, and preserves unrelated work. | Stages or commits unrelated files. |
| Review dependency | Uses existing review evidence or routes to `code-review` when ownership, mixed hunks, or commit groups are unclear. | Delivers an unclear dirty tree. |
| Staged diff proof | Uses exact path or hunk staging and checks staged stat, name-status, and diff before commit. | Uses broad staging or commits unchecked staged files. |
| Commit integrity | Preserves user-provided commit text verbatim or uses repo convention when none is supplied. | Rewrites supplied commit text. |
| Push and remote proof | Pushes only requested refs and verifies final remote refs. | Claims push success without remote evidence. |
| Squash-to-main | Refreshes target branch, produces exactly one final commit when required, pushes `main`, and verifies `origin/main`. | Leaves iterative branch commits on `main` or skips final proof. |
| Cleanup | Deletes temporary branches only after final target state is verified and cleanup is requested or repo-required. | Deletes branches before proving delivery. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
