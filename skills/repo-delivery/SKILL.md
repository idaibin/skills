---
name: repo-delivery
description: "Use when reviewed repository changes are explicitly authorized for staging, commit, push, branch integration, synchronization, cleanup, or ref proof; owns Git mutation and stops before pull-request creation."
---

# Repository Delivery

## Overview

Deliver an already understood and reviewed change through the shortest safe Git path.
Ordinary delivery is the default: freeze scope and branch once, execute the authorized
Git chain as one bounded transaction, and read back the final refs once.

Consume `urn:skills:delivery-request:v1` and produce
`urn:skills:delivery-receipt:v1` only after the requested target is read back. A local
commit is local durability, not remote delivery, deployment, or production proof.

## Workflow

1. **Compact preflight:** read effective guidance and run one branch-aware status. Freeze
   authorization, branch/upstream, exact paths or hunks, accepted validation basis, and
   history strategy. Fetch only when a remote action needs fresh divergence. Stop on
   unrelated staged content, mixed ownership, or unresolved strategy.
2. **One transaction:** reuse unchanged implementation/review validation. Stage exact
   paths or hunks, run cached `diff --check`, and inspect only cached stat and
   name-status. Do not print or reread the full cached diff unless mixed/unreviewed hunks
   make content inspection necessary. Then perform the authorized commit/rebase/push
   chain without returning to the model between successful steps. Prefer
   `scripts/compact-delivery.sh` for an ordinary exact-path commit with optional rebase
   and push; otherwise use one equivalent bounded command or one execution agent.
3. **One readback:** after the chain, read local branch/SHA/status and, after push, the
   actual remote ref in the same execution. Compare the final SHA once. Do not perform
   per-file remote comparisons unless a named manifest, generated artifact contract,
   or explicit user request requires them. Report unchecked CI, deployment, runtime,
   or production state as `Not verified`.

## Parallel Current-Branch Delivery

When the authorized outcome is to commit current changes, synchronize the same remote
branch, rebase, and push, use two preparatory owners in parallel:

1. **Commit owner:** the only Worktree/index/`HEAD` writer. It stages the exact accepted
   scope, performs cached checks, and creates the local commit.
2. **Remote owner:** owns only remote-ref preparation. It fetches the named remote branch
   and returns its exact SHA/divergence without touching the Worktree, index, or `HEAD`.
3. After both complete, one writer verifies their bases and runs `git rebase` against
   the fetched exact remote ref; `git pull --rebase` is acceptable when no reliable
   prefetched ref is available. This final phase is single-writer, never parallel.
4. On conflict, the same writer resolves only conflicts whose local and remote intent
   is established, runs the smallest affected check, continues the rebase, pushes, and
   performs one remote-SHA readback. Stop on unrelated or ambiguous conflict ownership.

If the host cannot isolate the commit and remote-ref owners safely, keep one execution
agent and one composite transaction rather than risk concurrent Git state mutation.

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
- Keep successful delivery output to branch, commit SHA, pushed ref/SHA, staged-file
  count, remaining-entry count, and any `Not verified` boundary. Expand command output
  only on failure.
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
- Ordinary exact-path transaction helper: [compact-delivery.sh](scripts/compact-delivery.sh).
