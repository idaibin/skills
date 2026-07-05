# AICraft

AICraft is the source repository for reusable AI workflow assets: prompts, skills, workflow templates, and shared automation standards.

It defines reusable AI capabilities and execution rules. Downstream repositories such as `blog` and `feeds-hub` consume those standards, then keep their own repository-specific task specs locally.

## Goal

AICraft turns repeated AI working habits into durable assets with clear boundaries:

- `prompts/` stores reusable task templates and workflow instructions.
- `skills/` packages stable workflows into portable agent capabilities.
- `docs/standards/` defines shared execution rules for automation, GitHub branching, and content quality.
- `docs/templates/` stores reusable task-document templates.
- `docs/task-registry.md` indexes concrete scheduled-task implementations in downstream repositories.

The active content should help an agent start with real project context, preserve local changes, follow exact tool and command constraints, verify work, and report results clearly.

## Repository Boundary

```text
aicraft = source capabilities and standards
blog = long-form content publishing implementation
feeds-hub = short-cycle information feed implementation
```

AICraft should not own generated blog posts, feed entries, repository-specific frontmatter, or production content files for downstream repositories.

See:

```text
docs/repo-scope.md
```

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
  - shared automation standards under `docs/standards/`
  - reusable templates under `docs/templates/`
  - concrete task index in `docs/task-registry.md`

## Shared Standards

```text
docs/standards/cron-automation.md
docs/standards/github-branching.md
docs/standards/ai-content-quality.md
```

## Install Skills From GitHub

Install all skills with the standard skills.sh CLI flow:

```bash
npx skills add https://github.com/idaibin/aicraft
npx skills update
```

Install selected skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill code-context code-planner code-review code-delivery frontend-implementation code-security ops-browser ops-client writing-editor
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
| `code-delivery` | Delivering reviewed local changes with validation, path-limited staging, commits, pushes, branch sync, and remote proof. |
| `frontend-implementation` | Implementing or reviewing frontend UI, routes, forms, tables, dashboards, responsive behavior, and architecture while preserving existing design-system and API contracts. |
| `code-security` | Reviewing code, API, auth, permission, token/session, upload, logging, dependency, config, or release changes for security risks. |
| `ops-browser` | Operating browser pages and collecting screenshots, visual/responsive checks, form/upload/download evidence, console/network data, and session-safe verification. |
| `ops-client` | Verifying or operating specified Tauri/Electron/native desktop clients with launch-command, runtime-source, CGWindowID, real-window, and Accessibility evidence. |
| `writing-editor` | Editing Chinese personal technical writing to reduce AI-template prose while preserving viewpoint, tradeoffs, and technical accuracy. |

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
- keep shared automation standards in `docs/standards/`
- keep downstream repository task details out of AICraft except for the registry index
- retire time-sensitive or old workflow material from the active root
- avoid mixing transient notes and historical references into the active root
