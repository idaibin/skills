# Delivery Checklist

Use this checklist when committing, pushing, syncing, squashing, or cleaning up branches.

`repo-delivery` owns Git mutation after review acceptance. A review-only request does not authorize staging or committing.

## Required Evidence

- Read relevant repo guidance before delivery.
- Run `git status --short --branch`.
- Identify branch, upstream, staged files, unstaged files, untracked files, and unrelated local work.
- Confirm the requested delivery target, path scope, and whether one commit was explicitly required.
- Confirm the user authorized the exact staging, commit, push, sync, branch-integration, or cleanup action being performed.
- Confirm review status or run `repo-review` first when ownership, mixed hunks, or commit groups are unclear.
- For review publication, confirm explicit commit and push authorization, a GitHub remote, a non-default/non-protected branch, and the exact fixed SHA the reviewer will receive.
- Run task-matching validation or report why it was skipped.
- Inspect staged diff before every commit.
- Verify final local and remote state after delivery.

## Staging And Commit

- Classify every approved path/hunk into semantic categories and record dependency order before staging.
- Default to one commit per independent category. One commit is valid when the user explicitly requests it or the reviewed scope has one indivisible intent.
- Keep one contract change with its required tests, migrations, generated artifacts, and documentation even when they span directories.
- Stage only approved files or hunks.
- Prefer exact paths or hunk staging.
- Never use broad staging unless the user explicitly approves that exact scope.
- Stop if unrelated staged files already exist.
- Preserve user-provided commit text verbatim.
- Use repository convention or concise Conventional Commits when no text is provided.
- Record the resulting commit hash.
- Recheck the remaining dirty tree after every category so later commits cannot absorb already delivered or unrelated content.
- Stop after a local commit unless push or another Git target was separately authorized.

## Merge Or Rebase Conflicts

- Load `resolving-merge-conflicts.md` only for an authorized in-progress operation.
- Trace both sides' primary intent for every conflicted hunk; never clear markers by blindly choosing ours/theirs.
- Run focused checks. If staging is authorized, stage only resolved paths/hunks and inspect the cached diff; continue only when separately authorized.
- Abort when intent, basis, permissions, or local-work preservation cannot be established; no rule forbids a safe abort.
- Conflict resolution does not imply staging, continuation, commit, push, force-push, cleanup, or branch deletion.

## Push And Sync

- Push only the requested branch or ref.
- Fetch before comparing or integrating remote state.
- Do not rebase, merge, force-push, or change upstream unless the delivery target requires it.
- Use `--force-with-lease` only when rewrite delivery is explicitly requested and repo guidance permits it.
- Verify remote refs after push with `git ls-remote`, `git status --short --branch`, or an equivalent repo-defined command.

## Review Publication

- Use only when the external review explicitly needs a repository URL, branch, and fixed SHA.
- Require local review and validation before committing or pushing the review basis.
- Publish only the authorized current feature branch; never `main`, another default/protected branch, a pull request, or a force-pushed rewrite.
- Return the canonical GitHub repository URL, branch, base/head SHA, and remote-ref proof to the calling review owner.
- When the remote is not GitHub, the branch is default/protected, authorization is incomplete, or publication cannot be proved safe, do not mutate Git; let the caller provide the minimum necessary files or review package instead.

## Branch Integration Strategy

- Fix the target tip and source range before deciding how history should land.
- Preserve source commits when each is meaningful, reviewed, independently coherent, dependency-ordered, and useful for future traceability or rollback.
- Squash when the source history is WIP/fixup-heavy, conflict-repair-heavy, mechanically fragmented, or intentionally represents one outcome; also follow an explicit one-commit or repository-policy requirement.
- Fold fixup, conflict-only, and validation-repair commits into their owning intent instead of preserving them as important history.
- Use a partial cherry-pick only when partial integration is explicit; account for every omitted source commit and verify the resulting target tree matches the approved scope.
- Record the chosen strategy and why the rejected alternative was less faithful to the reviewed intent.

## Squash-To-Main

- Use only when requested or required by repo guidance.
- Confirm the current branch contains the completed reviewed work.
- Ensure `main` is refreshed from `origin/main` before final integration unless repo guidance says otherwise.
- Produce exactly one final commit on `main` only when squash is the selected strategy.
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
