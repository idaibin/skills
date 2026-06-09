# AICraft

A focused repository for reusable AI workflow assets: prompts, skills, and packaged context patterns that can be reused, published, or adapted across real projects.

## Goal

AICraft turns repeated AI working habits into durable assets with clear boundaries:

- `prompts/` stores reusable task templates and workflow instructions.
- `skills/` packages stable workflows into portable agent capabilities.
- retired material stays out of the active working set and can be recovered from git history when needed.

The active content should help an agent start with real project context, preserve local changes, follow exact tool and command constraints, verify work, and report results clearly.

## Active Structure

- `skills/`
  - publishable or reusable skill packages
  - each skill keeps its own `SKILL.md`, `agents/`, and `references/` layout

- `prompts/`
  - reusable prompt assets
  - grouped by use case, such as development workflows, automation, agent systems, and project-specific prompts
  - each file should have a clear task boundary, scenario, prompt text, and usage constraints

## Install Skills From GitHub

For AI-assisted or manual installation from GitHub, use [`INSTALL.md`](INSTALL.md). It lists the exact skill package paths and the direct Codex install command.

## Sync Local Skills

Install or upgrade all repository skills into the local Codex skills directory:

```bash
python3 scripts/sync-skills.py --validate-only
python3 scripts/sync-skills.py
python3 scripts/sync-skills.py --apply
```

The validation command checks the source packages without requiring local installation. The dry run previews the sync. The apply command writes to `${CODEX_HOME:-~/.codex}/skills`, updates every discovered `skills/*/SKILL.md` package, validates the installed target, and removes obsolete legacy skill directories.

Useful targeted checks:

```bash
python3 scripts/sync-skills.py --skill code-planner --apply
python3 scripts/sync-skills.py --validate-only --check-target
python3 scripts/sync-skills.py --target /private/tmp/aicraft-skills-test --apply
```

After installing or upgrading local skills, restart Codex so updated skill metadata and descriptions are loaded.

## Principles

- keep active root content reusable
- keep prompt and skill assets directly accessible
- keep publishable skills self-contained; repo-local prompts can supplement them but should not be required
- let prompts capture task language, and let skills capture stable execution workflows
- keep skill trigger/eval cases in `references/eval-cases.md` and validate packages before publishing or syncing
- retire time-sensitive or old workflow material from the active root
- avoid mixing transient notes and historical references into the active root
