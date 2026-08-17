---
name: repo-delivery
description: "Use when authorized Git mutation must preserve a large task through semantic milestone, targeted fixup, or exceptional checkpoint commits, normalize task-branch history, or deliver reviewed changes—including a validated Skills catalog release—through commit, push, integration, cleanup, or ref proof; stops before pull-request creation."
---

# Repository Delivery

## Overview

Own two separately authorized Git lifecycles: **Execution Durability** preserves large-task progress on a task branch through semantic milestones, targeted fixups, and exceptional safety checkpoints; **Final Delivery** normalizes the completed branch when requested, fixes the final review basis, and performs reviewed commits, pushes, integration, or cleanup. Execution commits preserve work but never imply final review, merge readiness, or remote durability. Verify branch policy, sharing/rewrite safety, permissions, commit grouping, and staged content before mutation; never open a pull request.

Consume `urn:skills:delivery-request:v1`; this is the sole default Skill that produces
`urn:skills:delivery-receipt:v1`. Consume
an exact reviewed PackageManifest/basis, review Observations, authorization, and target;
emit a typed DeliveryReceipt only after target readback. Local commits without remote
readback remain local durability and do not imply delivered, deployed, or production-
verified state.

Persist the minimum typed PackageManifest and DeliveryReceipt metadata needed to
detect scope, basis, target, and ref drift across steps or sessions. Store it in a
Git-ignored task workspace such as `.codex/reviews/` or in the active Forgeway Run
store; do not commit or upload it by default. Validation without persistence is
acceptable only for a same-process read-only dry run that cannot cross a mutation
boundary. Commit a sanitized receipt only when repository policy or the user
explicitly requires durable audit or release evidence. Never retain raw prompts,
provider responses, credentials, or long logs as delivery-contract fields.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Run `git status --short --branch` and identify branch, upstream, staged files, dirty files, and unrelated local work.
3. Select **Execution Durability** or **Final Delivery** from the requested outcome. For an accepted Skills catalog release, load its conditional profile; runtime installation remains a separate handoff. Implementation-only wording never authorizes either lifecycle.
4. Inspect existing local refs. Fetch or otherwise refresh remote state only for an explicitly authorized push, sync, branch-integration, history-rewrite assessment, or remote-refresh target; a local-commit-only request leaves remote state `Not verified`.
5. Confirm each target through either exact per-action authorization or a bounded task-level execution-durability plan. A standing plan records the task branch, owned scope, allowed milestone/fixup/checkpoint types, event triggers, validation floor, message policy, and push policy; matching commits may proceed without asking again. Scope expansion, a new commit type, failed safety gates, rewrite, push, integration, or cleanup requires fresh authority.
6. Confirm branch policy and permissions: task/default/protected status, upstream and known sharing/review state, force-push restrictions, required checks, branch naming, and every unknown that changes safety.
7. For **Execution Durability**, require exact per-action authority or a still-valid bounded task plan plus an exact separable scope. Classify it as a completed semantic milestone, a correction owned by one reachable milestone, or an exceptional checkpoint permitted by the plan before a concrete loss/recovery risk. Reuse implementation evidence, run focused validation when possible, stage only exact paths/hunks, inspect the complete cached diff, commit, then report remaining and unrelated Worktree content. Continue under the same plan only while its branch, scope, triggers, and safety gates still match; push remains separately authorized.
8. For ordinary reviewed local commits, require the accepted review basis and ownership
   to match the immutable PackageManifest when one is supplied; regenerate through its
   declared producer and stop for review when any file/hash/status differs. Classify
   every approved path or hunk by semantic intent and dependency order. When the
   approved delivery outcome depends on a selected-source visual-completion claim,
   require the applicable final review Observation and referenced final visual-
   evidence artifact before calling it ready; consume those artifacts without
   capturing screenshots, operating a browser/client, or issuing a new visual verdict.
   Default to one commit per independent category. Use one commit only when explicitly
   requested or the complete scope is one indivisible intent. Inspect cached stat,
   name-status, and full diff before each commit.
9. For **Final History Normalization**, require completed implementation, exact rewrite authorization, and either a clean task worktree or an isolated worktree with every remaining staged/unstaged/untracked item fingerprinted outside the rewrite basis. Record the source range, before HEAD/tree, and recoverable pre-rewrite SHA; do not rewrite a default, protected, shared, or active-review branch when safe ownership is not proven. After normalization, require the expected tree and scope to match, freeze the new immutable basis, and obtain final fixed-basis review evidence. Any later history or tree change invalidates that evidence.
10. For branch integration, fix the source range and target tip before choosing the history shape. Preserve coherent, reviewed, meaningful commits when their order and boundaries remain useful; squash noisy, fixup-heavy, checkpoint-bearing, or single-outcome history when policy or explicit intent calls for one commit. Selecting only some source commits requires explicit partial-integration scope and proof that omitted content is intentional.
11. For push, sync, cleanup, or conflict resolution, execute only that target's authorized mutations. Conflict authorization separately covers file resolution, staging, merge/rebase continuation or commit, and push; an omitted action remains forbidden.
12. Verify the requested final local and remote state with branch, status, log, tree,
    remaining Worktree content, and remote ref evidence. A local-only durability commit
    reports remote protection as absent, not implied.
13. When Forgeway delivery integration is active, bind capability, reviewed result
    PackageManifest, accepted review Observations, authorization, target, and exact
    mutation scope to an immutable Run/Attempt. Emit DeliveryReceipt only from actual
    commit/ref/remote readback evidence. Deployment and production verification require
    their own environment-specific receipts and are never inferred from Git success.

## Modes

- **Categorized local commits:** classify reviewed changes and create one commit per independent intent without pushing.
- **Explicit single commit:** create exactly one commit only when requested or when the reviewed scope has one indivisible intent.
- **Semantic milestone:** preserve one completed, separable, focused-validated task slice on a non-default task branch; mark it `slice-validated`, not final-reviewed.
- **Targeted fixup:** commit a correction that belongs to exactly one reachable milestone and mark its normalization target; use a normal semantic correction when that ownership is not singular or rewrite is not planned.
- **Safety checkpoint (exceptional):** preserve incomplete task-owned work only before a concrete loss/recovery risk; record why it exists and require split, absorption, or removal before final integration.
- **Final history normalization:** with exact rewrite authorization, normalize completed task-branch history while preserving the expected tree, then freeze a new final review basis.
- **Current-branch push:** push the already reviewed current branch after upstream/divergence checks; do not stage or commit unless separately authorized.
- **Review publication:** after local review and validation, create and/or push the explicitly authorized fixed commit on a GitHub-backed non-default, non-protected branch so an external reviewer can use repository URL, branch, and SHA. Stop before PR creation or target-branch integration.
- **Branch sync and recovery:** pull, fetch, rebase, merge, fast-forward, cherry-pick, or abort an in-progress Git operation only according to repo guidance, current divergence, and the user's requested target. Cherry-pick still requires explicit partial-integration scope; abort does not authorize follow-up staging, commit, or push.
- **Branch integration:** integrate a fixed reviewed source range into the target by preserving coherent semantic commits or squashing noisy/single-outcome history according to explicit intent, repository policy, and evidence.
- **Squash-to-main:** a conditional branch-integration strategy that moves reviewed branch work into `main` as exactly one final commit only when repo guidance and explicit user intent permit direct `main` updates.
- **Cleanup:** delete local or remote temporary branches only after final target state is verified and cleanup is requested or required by repo guidance.
- **Conflict resolution (conditional):** resolve an authorized in-progress merge/rebase hunk by hunk from both sides' primary intent. Treat resolution writes, staging, continuation/commit, and push as separate permissions.
- **Skills release:** deliver an accepted package/catalog scope after the canonical gate and fixed-basis review; hand off runtime installation. See [references/skills-release.md](references/skills-release.md).

## Do Not Use For

- First-pass repository discovery, real commands, or docs alignment; use `repo-map`.
- Future implementation planning or subagent task splitting; use the host's built-in planning.
- Implementation or validation requests that do not explicitly authorize a local commit or other Git mutation; use the implementation owner and leave Git unchanged.
- Existing local diff review, ownership classification, mixed-hunk analysis, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests that do not authorize Git mutation; use `repo-review`.
- Review of a fixed change basis, including authorization or token risks; use `repo-review`.
- Browser or desktop-client runtime evidence; use `ops-browser` or `ops-client`.
- Branch publishing that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Hard Rules

- Git mutation requires exact per-action authority or a still-valid bounded durability
  plan. Review, grounding, implementation, risk, or local commit authority does not
  imply stage, push, sync, integration, rewrite, cleanup, deletion, conflict handling,
  pull-request, or `main` authority.
- A grounding record may identify evidence gaps, but it never authorizes stage, commit, push,
  integration, cleanup, or pull-request actions.
- Preserve unrelated work. Stage exact paths/hunks, inspect the cached diff, and stop
  on unrelated staged files. Do not use `git add .`, `git add -A`, broad directories,
  or wildcards without explicit approval.
- Keep one commit per logical intent; neither split indivisible contracts nor combine
  independent categories unless one commit is explicitly required. Preserve exact
  user-provided commit text.
- Milestones/fixups/checkpoints are durability only. No automatic/time-based WIP
  commits; checkpoints require a named loss risk and final split/absorb/drop disposition,
  and fixups bind exactly one reachable milestone when normalization is intended.
- Persist the minimum typed delivery state across mutation/session boundaries and
  reverify scope, basis, branch, validation floor, and authority before continuing.
- Never replace the Skills canonical gate with a package-local test or install runtime
  Skills inside Git delivery.
- Rewrite only a proven-owned non-default, non-protected, unshared branch with exact
  authority, clean/isolate-fingerprinted state, recoverable before SHA, and before/after
  tree proof. Any later tree/history change invalidates final review evidence.
- Choose preserve/squash/cherry-pick from policy and explicit scope, account for every
  omitted commit, and do not carry WIP/fixup/conflict/validation-repair history merely
  for convenience.
- Do not rebase/merge over unexplained dirty state or force-push after rejection.
  Re-read divergence and reassess when remote state changed.
- Review publication also requires explicit commit/push authority, verified GitHub
  remote, fixed reviewed basis, non-default/non-protected branch, and remote-ref proof.
  It never updates `main`, creates a PR, force-pushes, or implies reviewer approval.
- Verify remote success from the updated ref/SHA, not command exit. Mark unchecked
  validation, policy, permissions, remote refs, CI, deployment, and cleanup `Not verified`.
- Do not create or update pull requests; stop after the authorized Git ref and cleanup
  state are verified.

## Output Contract

Return capability `repository.git.deliver`, Run/Attempt and reviewed PackageManifest
refs when integration is active, the typed DeliveryReceipt ref or an explicit reason
none was produced, and a compact Delivery Report with `Completed`, `Changed Files`,
`Verification`, `Known Issues`, `Next Steps`, and `Git Status`. Include lifecycle and
mode, per-action or bounded-plan authorization basis, delivery target,
branch/upstream, branch policy, ahead/behind/diverged state, dirty-tree risks,
semantic categories and dependency order, each staged scope and commit hash,
validation and review Observation refs, local-only versus pushed durability,
remaining uncommitted content, required checkpoint/fixup disposition, before/after
tree proof for normalization, branch-integration strategy and rationale, authorized
Git actions, final local and remote ref readback, rejected unsafe operations, and every
`Not verified` item. Reference existing artifacts instead of duplicating them; redact
secrets and unrelated personal data.

## References

- [Usage](references/usage.md), [durability](references/execution-durability.md),
  [normalization](references/history-normalization.md), [checklist](references/checklist.md),
  [report](references/delivery-report.md), [conflicts](references/resolving-merge-conflicts.md),
  [Skills release](references/skills-release.md), [evals](references/eval-cases.md).
