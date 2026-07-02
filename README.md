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

- `docs/`
  - repository maintenance standards and contributor-facing references
  - not part of the installable skill package set

## Install Skills From GitHub

Install all skills with the standard skills.sh CLI flow:

```bash
npx skills add https://github.com/idaibin/aicraft
npx skills update
```

Install selected skills:

```bash
npx skills add https://github.com/idaibin/aicraft --skill ops-browser ops-client
```

List available skills without installing:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

For the full command list and available skill names, see [`INSTALL.md`](INSTALL.md).

## Skills

| Skill | Use when |
| --- | --- |
| `code-context` | Grounding repository work in real commands, paths, entry points, docs, and project context before guessing. |
| `code-planner` | Planning future codebase work, splitting tasks, defining validation gates, and coordinating auditable subagents before implementation. |
| `code-review` | Reviewing existing local changes, dirty-tree ownership, contract chains, commit grouping, and exact staging before commit. |
| `code-security` | Reviewing code, API, auth, permission, token/session, upload, logging, dependency, config, or release changes for security risks. |
| `ops-browser` | Operating browser pages, forms, uploads, console/network checks, background-safe browser verification, and tab/session cleanup. |
| `ops-client` | Operating or verifying specified desktop clients, repository-contained Tauri/Electron/native apps, startup commands, real windows, and Accessibility actions. |

## Validate Local Skills

For repository development, validate source skill packages before publishing changes:

```bash
python3 scripts/validate-skills.py
```

Useful targeted checks:

```bash
python3 scripts/validate-skills.py --skill code-planner
```

End-user installation and updates should use the standard `npx skills add` and `npx skills update` flow.

## Principles

- keep active root content reusable
- keep prompt and skill assets directly accessible
- keep publishable skills self-contained; repo-local prompts can supplement them but should not be required
- let prompts capture task language, and let skills capture stable execution workflows
- keep skill trigger/eval cases in `references/eval-cases.md` and validate packages before publishing
- retire time-sensitive or old workflow material from the active root
- avoid mixing transient notes and historical references into the active root
