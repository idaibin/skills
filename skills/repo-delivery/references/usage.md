# Repository Delivery Usage

## Summary

Use `repo-delivery` when the user wants reviewed repository changes moved to a final local or remote Git state without opening a pull request. It is for delivery actions that stop before PR creation, not for first-pass discovery or broad implementation.

## Best For

- Categorized local commits after review scope is approved.
- One commit only when explicitly requested or when the approved scope is one indivisible intent.
- Push only the current branch after validation, without creating a PR.
- Sync the current branch with its upstream.
- Integrate a completed branch by preserving useful semantic commits or squashing noisy/single-outcome history when repository guidance and evidence support it.
- Delete temporary branches after final state is verified.
- Prove local and remote refs match after delivery.

## Trigger Examples

- `Review the staged scope, commit, and push this branch.`
- `Push only the current branch after checking the diff; do not open a PR.`
- `Squash this completed branch into main and push main.`
- `Sync this branch to remote; do not switch branches.`
- `Commit these reviewed changes and show the final remote ref.`
- `These changes are reviewed; stage and commit them locally, but do not push.`
- `Group these reviewed changes by intent and commit each group locally.`
- `Commit all reviewed paths as exactly one commit.`
- `Merge this branch into main; preserve its meaningful commits if their boundaries are clean, otherwise squash it.`
- `After verification, delete the temporary branch.`
- `Ship this to main following the repo workflow.`

## Non-Triggers

- Repository onboarding, command discovery, or docs/code alignment; use `repo-map`.
- Future implementation planning; use the host's built-in planning.
- Dirty-tree ownership, mixed-hunk review, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests with no staging, commit, push, sync, or cleanup authorization; use `repo-review`.
- Security-only audit; use `audit-security`.
- Browser or desktop-client evidence collection; use `ops-browser` or `ops-client`.
- A full GitHub publish flow that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Output

Report the delivery target, branch/upstream, semantic categories, staged scope and hash for each commit, explicit single-commit reason when applicable, branch-integration strategy and rationale, validation, pushed refs, cleanup action, final status, final remote evidence, and any `Not verified` items.
