---
name: repo-delivery
description: "Use when reviewed local repository changes need Git delivery that stops before pull-request creation: path-limited staging, verification, local commit, current-branch push or sync, squash-to-main, temporary branch cleanup, or proof that local and remote refs match."
---

# Repository Delivery

## Overview

Deliver reviewed repository changes from a local worktree to the requested Git state. This is the sole owner of staging, commits, pushes, and other Git mutations after review acceptance. Verify branch policy, divergence, permissions, and staged content before mutation; never open a pull request.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Run `git status --short --branch` and identify branch, upstream, staged files, dirty files, and unrelated local work.
3. Fetch or inspect the relevant remote refs when network access is available; determine ahead/behind/diverged state before choosing push, rebase, merge, or squash behavior.
4. Confirm the requested delivery target: local commit only, push current branch, sync current branch, squash to `main`, delete temporary branch, or a narrower path scope.
5. Confirm branch policy and permissions: protected/default branch, force-push restrictions, required checks, branch naming, and whether direct updates are allowed or `Not verified`.
6. Ensure review is complete. Use `repo-review` first when ownership, mixed hunks, contract chains, or commit grouping are not already clear.
7. Run or reuse task-appropriate validation before staging unless the user explicitly requests delivery without further checks.
8. Stage only approved files or hunks, then inspect `git diff --cached --stat`, `git diff --cached --name-status`, and the staged diff.
9. Commit only the approved staged scope with the user's exact commit text when supplied; otherwise use the repository convention or a concise Conventional Commit.
10. Push, rebase, merge, squash, delete branches, or refresh from remote only when that action is the requested delivery target and the current divergence state supports the chosen operation.
11. Verify final local and remote state with branch, status, log, and remote ref evidence.

## Modes

- **Local commit:** create one or more commits without pushing.
- **Current-branch push:** push the current branch after validation, staged-diff review, and upstream/divergence checks.
- **Branch sync:** pull, fetch, rebase, merge, or fast-forward only according to repo guidance, current divergence, and the user's requested target.
- **Squash-to-main:** move reviewed branch work into `main` as exactly one final commit only when repo guidance and explicit user intent permit direct `main` updates.
- **Cleanup:** delete local or remote temporary branches only after final target state is verified and cleanup is requested or required by repo guidance.

## Do Not Use For

- First-pass repository discovery, real commands, or docs alignment; use `repo-map`.
- Future implementation planning or subagent task splitting; use `code-planner`.
- Existing local diff review, ownership classification, mixed-hunk analysis, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests that do not authorize Git mutation; use `repo-review`.
- Security-only audit; use `audit-security`.
- Browser or desktop-client runtime evidence; use `ops-browser` or `ops-client`.
- Branch publishing that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Hard Rules

- Do not make ordinary task changes directly on protected or default branches when repo guidance forbids it.
- Do not infer staging or commit authorization from a review-only request.
- Do not infer that `main` is writable merely because local checkout permits a commit.
- Do not stage unrelated local changes.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Do not commit when unrelated staged files are present.
- Do not rewrite, force-push, squash, delete branches, change remotes, or alter upstream tracking unless the user requested it or repo guidance requires it for the delivery target.
- Never use force push as an automatic response to non-fast-forward rejection. Re-read remote state and report the divergence first.
- Do not rebase or merge over a dirty worktree without an explicit safe plan for local changes.
- Preserve user-provided commit text verbatim.
- Prefer exact path or hunk staging; verify the staged diff before every commit.
- Verify remote success from the updated ref or commit SHA, not only from a successful command exit.
- If remote state changed after review or validation, stop and reassess before pushing or updating a target branch.
- Say `Not verified` when validation, branch protection, permissions, remote refs, CI, deployed state, or branch cleanup were not checked.
- Do not create or update pull requests; this workflow stops after the requested Git ref and cleanup state are verified.

## Output Contract

Start with delivery target, branch/upstream, branch policy, ahead/behind/diverged state, dirty-tree risks, and validation status. Then report staged scope, commit hash or skipped commit reason, push/merge/rebase/squash/cleanup actions, final local and remote ref evidence, rejected unsafe operations, and any `Not verified` items.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, mode, delivery, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and mode examples.
- See [references/checklist.md](references/checklist.md) for delivery and verification details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
