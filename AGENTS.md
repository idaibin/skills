# Agent Instructions

This file defines how AI agents should work on this repository. It is not the primary skill installation guide.

## Task Routing

- For repository development, documentation edits, prompt edits, skill package edits, reviews, or commits, follow the repository work rules below.
- Only when the user explicitly asks to install skills from `https://github.com/idaibin/skills`, read `INSTALL.md` and follow that installation flow.
- Do not switch into installation mode just because this repository contains `skills/`.
- Use `repo-map` for separate repository mapping, reuse inventory, or docs/code alignment.
- Use `domain-modeling` when shared cross-functional business language or rules conflict; load lifecycle or bounded-context depth only when that shared ambiguity requires it. Route feature-local behavior and acceptance to `product-spec`.
- Use the host's built-in planning for requirement readiness, technical design, task decomposition, acceptance criteria, and validation gates.
- For concrete failures, follow the effective personal or repository diagnosis rules before permanent remediation; use the matching implementation skill only when a source change is requested.
- Use `dev-frontend` or `dev-rust` for requested code changes.
- Use `audit-frontend`, `audit-rust`, or `audit-security` for bounded read-only domain audits.
- Use `repo-review` for read-only review of the current Worktree/index, a fixed immutable SHA/range, or a verified review package. Resolve pull requests to fixed base/head SHAs; apply Release only as a conditional profile over a fixed basis.
- Use `ask-chatgpt` for local ChatGPT packages or explicitly authorized ChatGPT review, research, visual exploration, and decision challenge after the Codex-first gate; use `ops-browser` only for delegated low-level browser operations.
- Use `repo-delivery` for categorized commits by default, explicit single commits, pushes, evidence-based branch integration, cleanup, and other Git mutations.

Use `.codex/` as the local task workspace. Store unfinished cross-session continuation
under `.codex/handoffs/<task-id>.md` and raw review packages, external responses,
ledgers, and attachments under `.codex/reviews/<review-id>/`; both subdirectories are
ignored. Put only explicitly approved, sanitized, durable handoffs or review evidence
under the repository's established `docs/` structure.

## Repository Work Rules

- Before modifying files, read this file plus directly related docs and code.
- Run `git status --short` before edits.
- Keep changes scoped to the requested task and preserve unrelated local changes.
- Use existing structure, tools, naming, and style.
- Run validation that matches the change, or state why it could not be run.
- For add, reuse, move, rename, or delete work, keep source, package metadata,
  references, eval cases, root indexes, installation docs, and stale-name checks
  synchronized.

## Project Structure

- `skills/` contains publishable or reusable skill packages.
- `scripts/validate-skills.py` checks portable package structure, OpenAI metadata,
  local links, representative eval sections, distribution hygiene, and catalog parity.
- `scripts/sync-shared-protocols.py` keeps identical self-contained package protocols
  synchronized from `protocols/`.
- `scripts/test_*.py` contains focused validator regressions.

When editing or adding skill packages under `skills/`, also read `skills/AGENTS.md`, `docs/skills/skill-standard.md`, and `docs/standards/skill-routing.md`.
When a provider format changes, update the standard, validator, focused tests, and
`docs/quality/official-skill-alignment.md` together.

## Skill Validation

Use the validation matrix in `skills/AGENTS.md`. Always run `git diff --check` and
report any runtime or external behavior that was not exercised.
