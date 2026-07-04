---
name: code-delivery
description: "Use when reviewed repository changes need final delivery: path-limited staging, verification, commit, push, branch sync, squash-to-main, temporary branch cleanup, or proof that local and remote state match."
---

# Code Delivery

## Overview

Deliver already-scoped repository changes from local worktree to the requested remote state. Use this after the change scope is understood and review risks are clear.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Run `git status --short --branch` and identify branch, upstream, staged files, dirty files, and unrelated local work.
3. Confirm the requested delivery target: local commit only, push current branch, sync current branch, squash to `main`, delete temporary branch, or a narrower path scope.
4. Ensure review is complete. Use `code-review` first when ownership, mixed hunks, contract chains, or commit grouping are not already clear.
5. Run or reuse task-appropriate validation before staging unless the user explicitly requests delivery without further checks.
6. Stage only approved files or hunks, then inspect `git diff --cached --stat`, `git diff --cached --name-status`, and the staged diff.
7. Commit only the approved staged scope with the user's exact commit text when supplied; otherwise use the repository convention or a concise Conventional Commit.
8. Push, squash, merge, delete branches, or refresh from remote only when that action is the requested delivery target.
9. Verify final local and remote state with branch, status, log, and remote ref evidence.

## Modes

- **Local commit:** create one or more commits without pushing.
- **Current-branch push:** push the current branch after validation and staged-diff review.
- **Branch sync:** pull, fetch, rebase, merge, or fast-forward only according to repo guidance and the user's requested target.
- **Squash-to-main:** move reviewed branch work into `main` as exactly one final commit when repo guidance requires it.
- **Cleanup:** delete local or remote temporary branches only after final target state is verified and cleanup is requested or required by repo guidance.

## Do Not Use For

- First-pass repository discovery, real commands, or docs alignment; use `code-context`.
- Future implementation planning or subagent task splitting; use `code-planner`.
- Existing local diff review, ownership classification, mixed-hunk analysis, or commit grouping before delivery scope is clear; use `code-review`.
- Security-only review; use `code-security`.
- Browser or desktop-client runtime evidence; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not make ordinary task changes directly on protected branches when repo guidance forbids it.
- Do not stage unrelated local changes.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Do not commit when unrelated staged files are present.
- Do not rewrite, force-push, squash, delete branches, or change remotes unless the user requested it or repo guidance requires it for the delivery target.
- Preserve user-provided commit text verbatim.
- Prefer exact path or hunk staging; verify the staged diff before every commit.
- Say `Not verified` when validation, remote refs, CI, deployed state, or branch cleanup were not checked.

## Output Contract

Start with delivery target, branch/upstream, dirty-tree risks, and validation status. Then report staged scope, commit hash or skipped commit reason, push/merge/squash/cleanup actions, final local and remote evidence, and any `Not verified` items.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, mode, delivery, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and mode examples.
- See [references/checklist.md](references/checklist.md) for delivery and verification details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
