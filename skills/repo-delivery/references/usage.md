# Repository Delivery Usage

## Summary

Use `repo-delivery` when the user wants reviewed repository changes moved to a final local or remote Git state without opening a pull request. It is for delivery actions that stop before PR creation, not for first-pass discovery or broad implementation.

## Best For

- Local commit after review scope is approved.
- Push only the current branch after validation, without creating a PR.
- Sync the current branch with its upstream.
- Squash a completed branch into `main` when repo guidance requires it.
- Delete temporary branches after final state is verified.
- Prove local and remote refs match after delivery.

## Trigger Examples

- `Review the staged scope, commit, and push this branch.`
- `Push only the current branch after checking the diff; do not open a PR.`
- `Squash this completed branch into main and push main.`
- `Sync this branch to remote; do not switch branches.`
- `Commit these reviewed changes and show the final remote ref.`
- `These changes are reviewed; stage and commit them locally, but do not push.`
- `After verification, delete the temporary branch.`
- `Ship this to main following the repo workflow.`

## Non-Triggers

- Repository onboarding, command discovery, or docs/code alignment; use `repo-map`.
- Future implementation planning; use `code-planner`.
- Dirty-tree ownership, mixed-hunk review, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests with no staging, commit, push, sync, or cleanup authorization; use `repo-review`.
- Security-only audit; use `audit-security`.
- Browser or desktop-client evidence collection; use `ops-browser` or `ops-client`.
- A full GitHub publish flow that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Output

Report the delivery target, branch/upstream, staged scope, validation, commit hash, pushed refs, merge or squash action, cleanup action, final status, final remote evidence, and any `Not verified` items.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
