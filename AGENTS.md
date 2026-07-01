# Agent Instructions

This file defines how AI agents should work on this repository. It is not the primary skill installation guide.

## Task Routing

- For repository development, documentation edits, prompt edits, skill package edits, reviews, or commits, follow the repository work rules below.
- Only when the user explicitly asks to install skills from `https://github.com/idaibin/aicraft`, read `INSTALL.md` and follow that installation flow.
- Do not switch into installation mode just because this repository contains `skills/`.

## Repository Work Rules

- Before modifying files, read this file plus directly related docs and code.
- Run `git status --short` before edits.
- Keep changes scoped to the requested task and preserve unrelated local changes.
- Use existing structure, tools, naming, and style.
- Run validation that matches the change, or state why it could not be run.

## Project Structure

- `skills/` contains publishable or reusable skill packages.
- `prompts/` contains reusable prompt assets.
- `scripts/validate-skills.py` validates source skill packages for repository development.

When editing or adding skill packages under `skills/`, also read `skills/AGENTS.md` and `docs/skills/skill-standard.md`.
