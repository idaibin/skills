# Final History Normalization

Normalize only completed task-branch history and only with exact rewrite authorization.
This profile prepares a final review basis; it does not itself approve or integrate the
result.

## Safety Gate

1. Fix the base, source range, current HEAD, upstream, default/protected status, and
   known remote, collaboration, and active-review use.
2. Require a clean task worktree. Otherwise use an isolated worktree and fingerprint
   every remaining staged, unstaged, and untracked item outside the rewrite basis.
3. Record the recoverable pre-rewrite SHA and before tree SHA.
4. Do not rewrite a default/protected branch. When a branch is shared, remotely
   consumed, under active review, or sharing is `Not verified`, prefer merge-time
   squash or a clean integration branch.
5. Choose preserve, autosquash, squash, split, reorder, or drop only from the completed
   semantic ownership of each commit. A checkpoint must be absorbed, split, or removed;
   a fixup must be folded into its single owner unless policy explicitly preserves it.

## Proof And Review

- Record after HEAD/tree and verify the expected before/after task tree is equal.
- Recheck submodules, generated outputs, and all fingerprinted remaining Worktree
  content; tree equality alone does not cover untracked files.
- Stop on any unexplained tree, scope, or remaining-content mismatch. Keep the
  pre-rewrite SHA available for recovery and do not push the rewritten history.
- Freeze the normalized immutable base/head and obtain final fixed-basis review
  evidence. Any later commit, amend, rebase, squash, or tree change invalidates it.
- Force-with-lease, push, integration, and cleanup each remain separately authorized.

Report the chosen actions and rationale, before/after HEAD and tree SHAs, equality and
remaining-content proof, final review basis/verdict, remote action or `Not performed`,
and every sharing, protection, CI, or runtime gap that remains `Not verified`.
