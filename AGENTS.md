# Agent Instructions

This file defines how AI agents should work on this repository. It is not the primary skill installation guide.

## Task Routing

- For repository development, documentation edits, prompt edits, skill package edits, reviews, or commits, follow the repository work rules below.
- Only when the user explicitly asks to install skills from `https://github.com/idaibin/aicraft`, read `INSTALL.md` and follow that installation flow.
- Do not switch into installation mode just because this repository contains `skills/`.
- Use `repo-map` for separate repository mapping, reuse inventory, or docs/code alignment.
- Use `diagnose` for concrete failures; permanent remediation transitions to the matching implementation skill.
- Use `implement-frontend` or `implement-rust` for requested code changes.
- Use `audit-frontend`, `audit-rust`, or `audit-security` for bounded read-only domain audits.
- Use `repo-review` for read-only review of local Git changes or immutable repository snapshots, ranges, pull requests, release candidates, and review packages; select the matching basis mode first.
- Use `chatgpt-review` for local ChatGPT review packages or explicitly authorized external ChatGPT review rounds; use `ops-browser` only for delegated low-level browser operations.
- Use `repo-delivery` for staging, commits, pushes, squash, cleanup, and other Git mutations.

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
- `scripts/test_*.py` contains validator, runner, and comparison regressions.
- `scripts/run-skill-routing-eval.py` plans reproducible routing trials and
  requires explicit `--execute` before it calls a model host.
- `scripts/create-skill-routing-campaign.py` creates and self-validates the
  committed preregistration file for formal held-out trials without calling a
  model host.
- `scripts/compare-skill-evals.py` replays matched candidate, previous, and
  no-Skill evidence from one preregistered campaign.
- `contracts/skill-validation.json` is the machine-readable authority for
  package limits, behavior-eval coverage and score gates, result schemas, and
  official-source review freshness.

When editing or adding skill packages under `skills/`, also read `skills/AGENTS.md`, `docs/skills/skill-standard.md`, and `docs/standards/skill-routing.md`.
When a provider format or official baseline changes, update the contract,
validator fixtures, tests, and `docs/quality/official-skill-alignment.md`
together; do not preserve stale checks only because old fixtures pass.

## Skill Validation

Before reviewing, committing, or publishing skill changes, run:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/eval-skill-contracts.py --validate-only
python3 scripts/measure-skill-footprint.py --baseline-ref HEAD
```

Also run `git diff --check` and report any runtime or external behavior that was not verified.
