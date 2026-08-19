---
name: repo-delivery
description: "Use when reviewed repository changes are explicitly authorized for staging, commit, push, branch integration, synchronization, cleanup, or ref proof; owns Git mutation and stops before pull-request creation."
---

# Repository Delivery

## Overview

Deliver an already understood and reviewed change through the shortest safe Git path.
Ordinary delivery is the default: verify scope and branch, stage exact paths, inspect
the staged diff, perform only authorized actions, and read back the final refs.

Consume `urn:skills:delivery-request:v1` and produce
`urn:skills:delivery-receipt:v1` only after the requested target is read back. A local
commit is local durability, not remote delivery, deployment, or production proof.

## Workflow

1. Read repository guidance and run `git status --short --branch`. Identify branch,
   upstream, staged/unstaged/untracked content, unrelated work, and the exact authorized
   Git actions.
2. For push, synchronization, integration, or cleanup, fetch the relevant remote refs
   and compare divergence. For a local commit only, do not add remote work.
3. Use the accepted review basis and exact path/hunk scope. Re-review only when the
   basis changed, ownership is unclear, mixed hunks exist, or the requested final gate
   requires it. Do not repeat implementation checks merely because delivery started.
4. Choose the history shape before mutation. Follow repository policy or explicit user
   intent; if merge, rebase, squash, or cherry-pick remain materially different valid
   choices, stop as `strategy-unresolved`.
5. Stage only the accepted paths or hunks and inspect cached stat, name-status, and full
   diff. Keep one semantic outcome together; split only independently useful changes.
6. Commit, push, integrate, synchronize, or clean up only as authorized. Resolve
   conflicts only when conflict edits, staging, continuation, and follow-up actions are
   all in scope.
7. Verify final branch, status, log/tree, remaining Worktree content, and requested
   local/remote refs. Report every unexecuted runtime, CI, deployment, or production
   check as `Not verified`.

For same-process ordinary delivery, current Git evidence is sufficient. Persist a
minimal PackageManifest/receipt record only when Forgeway integration, a cross-session
workflow, or repository policy actually requires resumable typed state.

## Conditional Paths

- **Large-task durability:** use [execution durability](references/execution-durability.md)
  only for an authorized semantic milestone, targeted fixup, or exceptional checkpoint
  on a non-default task branch. These commits do not imply review or merge readiness.
- **History normalization:** use [history normalization](references/history-normalization.md)
  only with explicit rewrite authority, exclusive branch ownership, a recoverable
  before SHA, and before/after tree proof.
- **Review publication:** publish a fixed non-default GitHub branch only when an
  external reviewer explicitly needs its URL and SHA. Never create a pull request or
  update `main` through this path.
- **Skills catalog release:** load [Skills release](references/skills-release.md), run
  the canonical catalog gate once on the final basis, deliver the reviewed scope, then
  handle separately authorized runtime installation from the immutable delivered ref.
- **Forgeway delivery:** bind the reviewed Result Package, authorization, mutation
  scope, target, and readback to its Run/Attempt. Deployment and Production still need
  separate receipts.

## Hard Rules

- Missing action-specific authorization stops as `missing-authorization`. Commit does
  not imply push; push does not imply integration, cleanup, deployment, or production.
- Preserve unrelated work. Never use broad staging when exact paths or hunks are
  available, and stop on unrelated pre-staged content.
- A grounding record may identify evidence gaps, but it never authorizes stage, commit, push,
  integration, cleanup, or pull-request actions.
- Do not merge or rebase over unexplained dirty state, force-push after rejection, or
  rewrite a default/protected/shared branch.
- Do not rerun unchanged full validation after an accepted final-basis pass. Rerun only
  when the basis changed or the repository's final delivery policy requires it.
- Verify remote success from the actual remote ref, not a command exit or local
  tracking ref.
- Never create or update a pull request, tag, release, deployment, or registry
  publication unless a separate owning workflow and explicit authorization cover it.

## Output

Return capability `repository.git.deliver` with mode, authorization, target, branch and
divergence, accepted basis/scope, staged paths, validation reused or run, commit/ref
proof, remaining Worktree content, cleanup, and `Not verified` gaps. Emit a typed
DeliveryReceipt only when its target readback exists; otherwise state why none exists.

## References

- Ordinary delivery: [usage](references/usage.md), [checklist](references/checklist.md),
  [report](references/delivery-report.md), [evals](references/eval-cases.md).
- Conditional: [durability](references/execution-durability.md),
  [normalization](references/history-normalization.md),
  [conflicts](references/resolving-merge-conflicts.md),
  [Skills release](references/skills-release.md).
