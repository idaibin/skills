# Agent Instructions

This file defines how AI agents should work on this repository. It is not the primary skill installation guide.

## Task Routing

- For repository development, documentation edits, prompt edits, skill package edits, reviews, or commits, follow the repository work rules below.
- Only when the user explicitly asks to install skills from `https://github.com/idaibin/aicraft`, read `INSTALL.md` and follow that installation flow.
- Do not switch into installation mode just because this repository contains `skills/`.
- Use `implement-frontend` or `implement-rust` for requested code changes. Use
  `audit-frontend` or `audit-rust` for read-only domain audits. Use
  `code-review` for existing Git changes, staging plans, and commit readiness;
  use `code-delivery` for staging, commits, pushes, and other Git mutations.

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
- `prompts/` contains reusable prompt assets.
- `scripts/validate-skills.py` validates source skill packages for repository development.
- `scripts/test_validate_skills.py` runs validator regression tests.

When editing or adding skill packages under `skills/`, also read `skills/AGENTS.md` and `docs/skills/skill-standard.md`.

## Skill Validation

Before reviewing, committing, or publishing skill changes, run:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
```

Also run `git diff --check` and report any runtime or external behavior that was
not verified.
