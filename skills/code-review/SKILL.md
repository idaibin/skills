---
name: code-review
description: "Use when existing local git changes need pre-commit review: classify dirty-tree ownership, inspect diffs and contract chains, select review depth, coordinate scoped specialist subreviews, and propose safe commit groups, exact staging plans, or commit messages without mutating Git state."
---

# Code Review

## Overview

Review local Git changes read-only before commit, protect all existing worktree content, verify contracts, and produce safe commit groups with exact staging scope. Scale review depth to the diff risk; this is not an implementation or repository-wide audit skill.

## Workflow

1. Read repo guidance related to the changed files.
2. Inventory the full local change scope with `git status --short`, `git diff --stat`, and `git diff --name-status`; check cached equivalents when anything is staged.
3. Classify each changed file as `task-owned`, `related-existing`, `unrelated-existing`, `mixed-hunk`, or `unknown`.
4. Select review depth:
   - **Focused:** small, single-owner, non-structural diff with no public/API/security boundary.
   - **Standard:** multi-file feature or fix with tests, callers, or local contracts.
   - **High-risk:** auth/security, migrations, public APIs, concurrency, unsafe/FFI, release, deletion/move, generated artifacts, or cross-package structure.
5. Inspect actual diffs for every file that may enter a commit group. Focused review may omit unrelated file bodies but must still inventory and classify them.
6. For API or interface changes, trace route/method/fields through request helpers, types, callers, data shaping, and runtime evidence or mark gaps `Not verified`.
7. For structural changes, trace manifests, exports, commands, tests, CI/deploy paths, docs, indexes, migrations, generated files, and stale references.
8. For High-risk changed surfaces, invoke `audit-frontend`, `audit-rust`, or `code-security` as a scoped read-only specialist subreview when their domain evidence is required. Keep dirty-tree ownership, staging plans, and final acceptance here.
9. Run or request checks that match the change and selected depth; report failures and skipped checks.
10. Split by semantic unit and output exact commit groups and staging instructions. Route requested staging, commits, pushes, or other Git mutations to `code-delivery` after review acceptance.

## Modes

- **Focused review:** inspect the complete small diff, verify ownership, immediate callers/tests, and exact staging; avoid producing a full architecture checklist when no boundary changed.
- **Standard review:** inspect all candidate changes, contract chains, tests, structural lifecycle, and semantic commit grouping.
- **High-risk review:** add domain-specific validation and, when needed, coordinate a scoped specialist subreview while retaining one read-only Git-change review coordinator.
- **Commit-readiness review:** produce semantic groups, exact path- or hunk-level staging instructions, validation status, and commit messages for `code-delivery`; do not stage or commit.

## Do Not Use For

- First-pass repository onboarding or docs/code alignment; use `code-context`.
- Future implementation planning before changes exist; use `code-planner`.
- Security-only audit after ownership and contract surfaces are already known; use `code-security`.
- Domain-wide frontend or Rust architecture, performance, memory, concurrency, SQLite, accessibility, or reuse audit without a Git change set; use `audit-frontend` or `audit-rust`.
- Browser or desktop-client operation evidence; use `ops-browser` or `ops-client`.
- Staging, local commits, pushes, branch sync, squash-to-main, remote cleanup, or post-push verification; use `code-delivery` after review scope is accepted.

## Hard Rules

- Do not modify or revert unrelated local changes.
- Do not modify, create, delete, rename, or format worktree files, including task-owned files. Route requested fixes to the matching `implement-*` skill, then review the resulting diff.
- Run only non-mutating checks. Do not invoke formatter/fixer/write modes during review.
- Do not let Focused review skip full dirty-tree inventory or ownership classification.
- Mark files with in-scope and out-of-scope hunks as `mixed-hunk`.
- Do not use whole-file staging for `mixed-hunk` files unless every hunk belongs to the current group.
- Require hunk-level staging, a file split, or exclusion in the delivery plan until staging is safe.
- Do not recommend `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Do not stage, unstage, commit, amend, push, rewrite refs, or delete branches. Inspect existing staged state read-only and route mutations to `code-delivery`.
- Treat staged files outside the current group as a delivery blocker and report them.
- Do not include generated artifacts in a staging plan unless they are required by the repository contract or are the requested deliverable.
- Do not approve add/reuse/move/rename/delete work while source, manifests, exports, commands, tests, CI/deploy paths, architecture/project-map docs, indexes, generated outputs, migrations, or stale references still disagree.
- Do not invent runtime, CI, deployment, migration, or consumer evidence. Use `Not verified` when the available diff cannot prove it.
- Review severity must be based on concrete impact and reachability, not file size, style preference, or hypothetical future use.

## Output Contract

Start with selected review depth, local change scope, ownership classification, staged-state risks, and severity-ranked findings. Include contract and structural completeness before the commit plan. For each commit group, include purpose, exact files or hunk-level staging approach, validation status, risks, and a concise Conventional Commit message. State excluded changes, failed or skipped checks, and `Not found` or `Not verified` evidence gaps.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, ownership, staging-plan, specialist-subreview, or contract-review changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/review-checklist.md](references/review-checklist.md) for detailed review and staging-plan rules.
- See [references/examples.md](references/examples.md) for split examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
