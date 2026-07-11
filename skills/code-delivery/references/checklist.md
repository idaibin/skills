# Delivery Checklist

Use this checklist when committing, pushing, syncing, squashing, or cleaning up branches.

`code-delivery` owns Git mutation after review acceptance. A review-only request does not authorize staging or committing.

## Required Evidence

- Read relevant repo guidance before delivery.
- Run `git status --short --branch`.
- Identify branch, upstream, staged files, unstaged files, untracked files, and unrelated local work.
- Confirm the requested delivery target and path scope.
- Confirm the user authorized the exact staging, commit, push, sync, squash, or cleanup action being performed.
- Confirm review status or run `code-review` first when ownership, mixed hunks, or commit groups are unclear.
- Run task-matching validation or report why it was skipped.
- Inspect staged diff before every commit.
- Verify final local and remote state after delivery.

## Staging And Commit

- Stage only approved files or hunks.
- Prefer exact paths or hunk staging.
- Never use broad staging unless the user explicitly approves that exact scope.
- Stop if unrelated staged files already exist.
- Preserve user-provided commit text verbatim.
- Use repository convention or concise Conventional Commits when no text is provided.
- Record the resulting commit hash.

## Push And Sync

- Push only the requested branch or ref.
- Fetch before comparing or integrating remote state.
- Do not rebase, merge, force-push, or change upstream unless the delivery target requires it.
- Use `--force-with-lease` only when rewrite delivery is explicitly requested and repo guidance permits it.
- Verify remote refs after push with `git ls-remote`, `git status --short --branch`, or an equivalent repo-defined command.

## Squash-To-Main

- Use only when requested or required by repo guidance.
- Confirm the current branch contains the completed reviewed work.
- Ensure `main` is refreshed from `origin/main` before final integration unless repo guidance says otherwise.
- Produce exactly one final commit on `main` when that is the requested workflow.
- Push `main` only after staged diff and validation are complete.
- Delete temporary branches only after `main` remote state is verified.

## Do Not Deliver

- Unrelated local changes.
- Mixed hunks that have not been split or staged safely.
- Generated artifacts unless they are the requested deliverable.
- Commits on protected branches when repo guidance forbids direct changes.
- Remote branch deletions or history rewrites without explicit authorization or repo-required workflow.

## Final Report

Include branch/upstream, validation commands and results, commit hash, pushed refs, final status, remote proof, cleanup performed, skipped actions, and `Not verified` gaps.
