# Repository Delivery Usage

## Summary

Use `repo-delivery` when the user explicitly authorizes Git mutation to preserve a
large task on a task branch or move reviewed changes to a final local or remote Git
state without opening a pull request. Execution durability and final delivery are
separate lifecycles; neither implementation wording nor a review request authorizes a
commit.

## Best For

- Categorized local commits after review scope is approved.
- A completed semantic milestone during a large task when local commit is explicit.
- Repeated semantic milestones covered by one bounded task-level commit plan, without
  re-prompting for every matching slice.
- One targeted fixup owned by a reachable milestone and scheduled for normalization.
- An exceptional checkpoint before a concrete loss/recovery risk.
- Final task-branch history normalization with rewrite authority and tree proof.
- One commit only when explicitly requested or when the approved scope is one indivisible intent.
- Push only the current branch after validation, without creating a PR.
- Publish an explicitly authorized fixed commit on a GitHub-backed feature branch so an external reviewer can inspect the repository URL, branch, and SHA.
- Sync the current branch with its upstream.
- Integrate a completed branch by preserving useful semantic commits or squashing noisy/single-outcome history when repository guidance and evidence support it.
- Delete temporary branches after final state is verified.
- Prove local and remote refs match after delivery.
- Deliver an accepted Skills catalog scope after the canonical repository gate and fixed-basis review, then hand off any separately authorized runtime installation.

## Trigger Examples

- `Review the staged scope, commit, and push this branch.`
- `This completed task slice is focused-tested; commit it locally so I can continue, but do not push.`
- `For this task branch, commit each completed focused-tested feature slice locally as a semantic milestone; fixups may target those milestones, checkpoints only before named high-risk rewrites, and never push.`
- `Commit this correction as a fixup of the named milestone; normalize it only at final delivery.`
- `Before this generator rewrites the module, checkpoint these exact incomplete paths locally; do not push.`
- `The branch is complete; normalize its fixups/checkpoint without changing the tree, then freeze the final review basis.`
- `Push only the current branch after checking the diff; do not open a PR.`
- `Commit and push this reviewed non-main branch so ChatGPT can review its GitHub URL and fixed SHA; do not open a PR.`
- `Squash this completed branch into main and push main.`
- `Sync this branch to remote; do not switch branches.`
- `Commit these reviewed changes and show the final remote ref.`
- `These changes are reviewed; stage and commit them locally, but do not push.`
- `Group these reviewed changes by intent and commit each group locally.`
- `Commit all reviewed paths as exactly one commit.`
- `Merge this branch into main; preserve its meaningful commits if their boundaries are clean, otherwise squash it.`
- `After verification, delete the temporary branch.`
- `Ship this to main following the repo workflow.`
- `The exact Skill package and catalog paths passed the canonical gate and fixed-basis review; commit and push that scope, then hand the immutable basis to the authorized runtime installer.`

## Non-Triggers

- Repository onboarding, command discovery, or docs/code alignment; use `repo-map`.
- Future implementation planning; use the host's built-in planning.
- Large-task implementation or risky operations without explicit Git-mutation authority; continue with the implementation owner and do not checkpoint automatically.
- Dirty-tree ownership, mixed-hunk review, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests with no staging, commit, push, sync, or cleanup authorization; use `repo-review`.
- Review of a fixed change basis, including authentication, authorization, token,
  or input risks; use `repo-review`.
- Browser or desktop-client evidence collection; use `ops-browser` or `ops-client`.
- A full GitHub publish flow that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.
- Skill design, package implementation, or canonical validation repair; return to the owning Skill source workflow before Git delivery.
- Preparing files or a review package when GitHub publication is unavailable or unauthorized; the calling review workflow owns that artifact.

## Output

Report lifecycle/mode, delivery target, branch/upstream, semantic categories, staged
scope and SHA, validation and review state, remaining Worktree content, local-only or
pushed durability, normalization disposition and tree proof when applicable,
integration rationale, final refs, and every `Not verified` item.
