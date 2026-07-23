# Eval Cases

Use these cases when changing `repo-delivery` triggers, modes, staging rules, push behavior, divergence handling, squash workflow, cleanup rules, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review the staged scope, commit, and push this branch.` | Should trigger `repo-delivery`. | Commit plus push delivery. |
| `These changes are reviewed; stage and commit them locally, but do not push.` | Should trigger Local commit mode. | Explicit local Git mutation after review. |
| `Classify all reviewed changes by intent and create one local commit per category.` | Should trigger Categorized local commits mode. | Default multi-intent delivery. |
| `Commit all approved changes as exactly one commit.` | Should trigger Explicit single commit mode while still verifying the complete classified scope. | Explicit exception to categorized commits. |
| `Push only the current branch after checking the diff; do not open a PR.` | Should trigger `repo-delivery`. | Current-branch delivery without PR publishing. |
| `This branch was rejected as non-fast-forward; inspect divergence and tell me the safe delivery path.` | Should trigger branch-state handling. | Remote divergence before mutation. |
| `Squash this completed branch into main and push main.` | Should trigger only after branch policy and explicit direct-main permission are verified. | High-risk target-branch delivery. |
| `Sync this branch to remote; do not switch branches.` | Should trigger `repo-delivery`. | Branch-specific remote sync. |
| `After verification, delete the temporary branch.` | Should trigger cleanup mode. | Delivery cleanup. |
| `Integrate this reviewed branch into main; preserve meaningful commits when their boundaries are clean, otherwise squash noisy history.` | Should trigger Branch integration and record the evidence-based history strategy. | Integration shape is conditional, not automatically squash. |
| `This rebase is already conflicted; trace both sides' intent, resolve each hunk, run checks, and continue the rebase, but do not push.` | Trigger conditional conflict resolution with bounded authorization. | Existing Git operation needs intent-preserving mutation. |
| `Push this already reviewed branch only; do not stage or commit dirty files.` | Trigger push-only dispatch and forbid staging/commit. | Push authority is independent. |
| `Resolve these named conflicts, but do not stage, continue, commit, or push.` | Trigger resolve-only dispatch and stop with the requested file state. | Conflict sub-actions require separate authority. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and entry points first.` | Should prefer `repo-map`. | Repository mapping. |
| `Split this future feature into tasks and owners.` | Should not trigger this Skill; use the host's built-in planning. | Forward planning. |
| `Review all dirty changes and propose commit groups.` | Should prefer `repo-review`. | Pre-delivery review scope is not clear. |
| `Review this diff and give me a commit message, but do not change Git state.` | Should prefer `repo-review`. | Review-only request without delivery authorization. |
| `Review this endpoint diff for authorization risk.` | Should prefer `repo-review`, routing professional security work to Codex Security when available. | Security-only change review. |
| `Verify this web page in the browser before release.` | Should prefer `ops-browser`. | Runtime browser evidence. |
| `Commit this branch, push it, and open a draft PR.` | Should prefer the GitHub publishing workflow. | PR creation is outside Git-only delivery. |
| `Send this branch to ChatGPT for five independent review rounds before delivery.` | Should prefer `ask-chatgpt`; delivery begins only after the review loop is accepted. | External review orchestration is not Git mutation. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Dirty-tree safety | Runs branch-aware status, identifies staged/unstaged/untracked files, and preserves unrelated work. | Stages or commits unrelated files. |
| Branch policy | Checks default/protected branch rules, direct-update permission, required checks, branch naming, and reports unknowns. | Assumes local checkout means the remote branch is writable. |
| Divergence | Fetches or inspects relevant refs, reports ahead/behind/diverged state, and selects fast-forward/rebase/merge/stop from policy and user intent. | Pushes blindly or force-pushes after non-fast-forward rejection. |
| Remote freshness | Rechecks remote state when it may have changed after review or validation. | Updates a target branch from stale evidence. |
| Review dependency | Uses existing review evidence or routes to `repo-review` when ownership, mixed hunks, or commit groups are unclear. | Delivers an unclear dirty tree. |
| Mutation authorization | Stages or commits only after the user requested that delivery action and review scope is accepted. | Infers mutation authority from a review-only request. |
| Staged diff proof | Uses exact path or hunk staging and checks staged stat, name-status, and diff before commit. | Uses broad staging or commits unchecked staged files. |
| Commit integrity | Preserves user-provided commit text verbatim or uses repo convention when none is supplied. | Rewrites supplied commit text. |
| Logical commit scope | Classifies changes by intent, stages only one category, inspects the cached diff, and creates one commit per intent. | Mixes unrelated categories or assumes whole-file ownership from proximity. |
| Single-commit exception | Uses one commit only for an explicit one-commit request or one indivisible reviewed intent, while still recording the category analysis. | Collapses independent categories for convenience or splits one contract artificially. |
| Commit/push separation | Stops after authorized local commits unless push was separately requested. | Treats commit permission as push permission. |
| Push and remote proof | Pushes only requested refs and verifies the final remote commit/ref, not just command exit. | Claims push success without remote evidence. |
| Squash-to-main | Requires explicit user intent and verified policy, refreshes target, produces the required final commit shape, and verifies `origin/main`. | Mutates main because local operations allow it or skips final proof. |
| Branch history strategy | Fixes source/target, preserves coherent meaningful commits, squashes noisy or single-outcome history, and records the rationale. Partial integration accounts for every omitted commit. | Always squashes, blindly preserves WIP/fixup commits, or silently drops source commits. |
| Dirty sync safety | Does not rebase/merge over a dirty worktree without an explicit preservation plan. | Risks overwriting local work during sync. |
| Conflict resolution | Traces both sides' primary intent, resolves hunk by hunk, validates, and continues only the authorized operation; permits abort when safety evidence is missing. | blindly chooses ours/theirs, forbids abort, or stages/commits/pushes beyond authorization. |
| Cleanup | Deletes temporary branches only after final target state is verified and cleanup is requested or repo-required. | Deletes branches before proving delivery. |
| Pull-request boundary | Stops after Git delivery and routes an explicit PR request to the publishing workflow. | Creates or updates a pull request. |
| Delivery handoff | Reports Completed, Changed Files, Verification, Known Issues, Next Steps, and Git Status; references existing artifacts and redacts sensitive data. | Duplicates large specs/reviews, omits final Git proof, or leaks sensitive content. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
