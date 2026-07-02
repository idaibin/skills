---
name: code-review
description: Use when existing local git changes need pre-commit review: classify dirty-tree ownership, inspect diffs and API contract chains, propose safe commit groups, exact staging, or commit messages.
---

# Code Review

## Overview

Review local git changes before commit, protect unrelated edits, verify contracts, and produce safe commit groups with exact staging scope. This is a review and commit-planning skill, not an implementation skill.

## Workflow

1. Read repo guidance related to the changed files.
2. Inventory the full local change scope with `git status --short`, `git diff --stat`, and `git diff --name-status`; check cached equivalents when anything is staged.
3. Classify each changed file as `task-owned`, `related-existing`, `unrelated-existing`, `mixed-hunk`, or `unknown`.
4. Inspect actual diffs for every file that may enter a commit group.
5. For API or interface changes, trace route/method/fields through request helpers, types, callers, data shaping, and runtime evidence or mark gaps `Not verified`.
6. Run or request checks that match the change; report failures and skipped checks.
7. Split by semantic unit and output exact commit groups.
8. Commit only when the user explicitly asks.

## Modes

- **Review mode:** inspect pending changes and output findings plus commit groups.
- **Commit mode:** stage only approved files or hunks, verify staged file list and staged diff, then commit.
- **Upgrade mode:** compare only remote `skills/code-review/` against local files; preview before writing.

## Do Not Use For

- First-pass repository onboarding or docs/code alignment; use `code-context`.
- Future implementation planning before changes exist; use `code-planner`.
- Security-only audit after ownership and contract surfaces are already known; use `code-security`.
- Browser or desktop-client operation evidence; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not modify or revert unrelated local changes.
- Mark files with in-scope and out-of-scope hunks as `mixed-hunk`.
- Do not use whole-file staging for `mixed-hunk` files unless every hunk belongs to the current group.
- Use hunk-level staging, split the file, or exclude it until staging is safe.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Stop before committing if staged files outside the current group already exist.
- Do not stage generated artifacts unless they are the requested deliverable.
- Do not commit automatically.

## Output Contract

Start with local change scope, ownership classification, and main risks. Include review findings before the commit plan. For each commit group, include purpose, exact files or hunk-level staging approach, validation status, risks, and a concise Conventional Commit message. Say `Not found` for missing files, layers, or commands; say `Not verified` for unchecked claims.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, ownership, staging, commit, contract-review, or upgrade changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/review-checklist.md](references/review-checklist.md) for detailed review and staging rules.
- See [references/examples.md](references/examples.md) for split examples.
- See [references/upstream-sources.md](references/upstream-sources.md) for trusted source metadata.
- See [references/upgrade-workflow.md](references/upgrade-workflow.md) for the upgrade process.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
