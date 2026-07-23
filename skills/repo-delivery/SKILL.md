---
name: repo-delivery
description: "Use when reviewed changes need authorized Git mutation: categorized commits, push or sync, branch integration, temporary-branch cleanup, or ref proof; owns Git delivery and stops before pull-request creation."
---

# Repository Delivery

## Overview

Deliver reviewed repository changes from a local worktree to the requested Git state. This is the sole owner of staging, categorized commits, pushes, branch integration, and other Git mutations after review acceptance. Verify branch policy, divergence, permissions, commit grouping, and staged content before mutation; never open a pull request.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Run `git status --short --branch` and identify branch, upstream, staged files, dirty files, and unrelated local work.
3. Inspect existing local refs. Fetch or otherwise refresh remote state only for an explicitly authorized push, sync, branch-integration, or remote-refresh target; a local-commit-only request leaves remote state `Not verified`.
4. Confirm each separately authorized target: categorized local commits, an explicitly requested single commit, push current branch, sync, branch integration, cleanup, or conflict resolution. Commit authorization never implies push or another target.
5. Confirm branch policy and permissions: protected/default branch, force-push restrictions, required checks, branch naming, and whether direct updates are allowed or `Not verified`.
6. Ensure review is complete. Use `repo-review` first when ownership, mixed hunks, contract chains, or commit grouping are not already clear.
7. Run or reuse task-appropriate validation before staging unless the user explicitly requests delivery without further checks.
8. Dispatch only to the authorized target workflow. Do not pass a push-only, sync-only, cleanup-only, or resolve-only request through staging or commit steps.
9. For authorized local commits, classify every approved path or hunk by semantic intent and dependency order. Default to one commit per independent category. Use one commit only when the user explicitly requests it or the classification proves the complete scope is one indivisible intent. For each commit, stage only its exact paths/hunks, inspect `git diff --cached --stat`, `git diff --cached --name-status`, and the full cached diff, commit with the supplied text or a concise repository-conforming message, then recheck the remaining dirty tree.
10. For branch integration, fix the source range and target tip before choosing the history shape. Preserve coherent, reviewed, meaningful commits when their order and boundaries remain useful; squash noisy, fixup-heavy, or single-outcome history when policy or explicit intent calls for one commit. Selecting only some source commits requires an explicit partial-integration scope and proof that omitted content is intentional.
11. For push, sync, cleanup, or conflict resolution, execute only that target's authorized mutations. Conflict authorization separately covers file resolution, staging, merge/rebase continuation or commit, and push; an omitted action remains forbidden.
12. After a local commit, stop by default. Verify the requested final local and remote state with branch, status, log, and remote ref evidence.

## Modes

- **Categorized local commits:** classify reviewed changes and create one commit per independent intent without pushing.
- **Explicit single commit:** create exactly one commit only when requested or when the reviewed scope has one indivisible intent.
- **Current-branch push:** push the already reviewed current branch after upstream/divergence checks; do not stage or commit unless separately authorized.
- **Branch sync:** pull, fetch, rebase, merge, or fast-forward only according to repo guidance, current divergence, and the user's requested target.
- **Branch integration:** integrate a fixed reviewed source range into the target by preserving coherent semantic commits or squashing noisy/single-outcome history according to explicit intent, repository policy, and evidence.
- **Squash-to-main:** a conditional branch-integration strategy that moves reviewed branch work into `main` as exactly one final commit only when repo guidance and explicit user intent permit direct `main` updates.
- **Cleanup:** delete local or remote temporary branches only after final target state is verified and cleanup is requested or required by repo guidance.
- **Conflict resolution (conditional):** resolve an authorized in-progress merge/rebase hunk by hunk from both sides' primary intent. Treat resolution writes, staging, continuation/commit, and push as separate permissions.

## Do Not Use For

- First-pass repository discovery, real commands, or docs alignment; use `repo-map`.
- Future implementation planning or subagent task splitting; use the host's built-in planning.
- Existing local diff review, ownership classification, mixed-hunk analysis, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests that do not authorize Git mutation; use `repo-review`.
- Security-only change review; use `repo-review`, which routes professional security work to Codex Security when available.
- Browser or desktop-client runtime evidence; use `ops-browser` or `ops-client`.
- Branch publishing that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Hard Rules

- Do not make ordinary task changes directly on protected or default branches when repo guidance forbids it.
- Do not infer staging or commit authorization from a review-only request.
- Do not infer push, sync, branch-integration, cleanup, conflict-resolution, or branch-deletion authorization from a local commit request.
- Do not infer that `main` is writable merely because local checkout permits a commit.
- Do not stage unrelated local changes.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Do not commit when unrelated staged files are present.
- Do not collapse multiple independent categories into one commit unless the user explicitly requests one commit.
- Do not split one indivisible contract change merely to increase commit count.
- Do not rewrite, force-push, squash, delete branches, change remotes, or alter upstream tracking unless the user requested it or repo guidance requires it for the delivery target.
- Never use force push as an automatic response to non-fast-forward rejection. Re-read remote state and report the divergence first.
- Do not rebase or merge over a dirty worktree without an explicit safe plan for local changes.
- Preserve user-provided commit text verbatim.
- Prefer exact path or hunk staging; verify the staged diff before every commit.
- Keep one commit to one logical intent; do not mix a second category merely because it is already modified.
- Do not choose squash merely because it is convenient. Record why preserved commits or a squash best represents the reviewed source range.
- Do not preserve WIP, fixup, conflict-only, or validation-repair commits as important history when they can be safely folded into their owning intent.
- Do not cherry-pick a subset of another branch unless partial integration is explicit and every omitted commit is accounted for.
- Verify remote success from the updated ref or commit SHA, not only from a successful command exit.
- If remote state changed after review or validation, stop and reassess before pushing or updating a target branch.
- Say `Not verified` when validation, branch protection, permissions, remote refs, CI, deployed state, or branch cleanup were not checked.
- Do not create or update pull requests; this workflow stops after the requested Git ref and cleanup state are verified.

## Output Contract

Return a compact Delivery Report with `Completed`, `Changed Files`, `Verification`, `Known Issues`, `Next Steps`, and `Git Status`. Include delivery target, branch/upstream, branch policy, ahead/behind/diverged state, dirty-tree risks, semantic categories and dependency order, each staged scope and commit hash, explicit single-commit reason when used, branch-integration strategy and rationale, push/merge/rebase/squash/cherry-pick/cleanup actions, final local and remote ref evidence, rejected unsafe operations, and every `Not verified` item. Reference existing specs, plans, reviews, commits, and artifacts instead of duplicating them; redact secrets and unrelated personal data.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and mode examples.
- See [references/checklist.md](references/checklist.md) for delivery and verification details.
- See [references/delivery-report.md](references/delivery-report.md) for the compact handoff/report template.
- See [references/resolving-merge-conflicts.md](references/resolving-merge-conflicts.md) only for an authorized in-progress merge/rebase conflict.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
