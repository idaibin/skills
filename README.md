# AICraft

AICraft is the source repository for reusable AI workflow assets: skills, prompts, workflow templates, and shared automation standards.

It defines reusable AI capabilities and execution rules. Downstream repositories such as `blog` and `feeds-hub` consume those standards, then keep their own repository-specific task specs locally.

## Goal

AICraft turns repeated AI working habits into durable assets with clear boundaries. It prioritizes portable skill packages first, then supports them with reusable prompts, workflow templates, and shared standards.

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
docs/standards/skill-routing.md
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
  --skill repo-context code-planner diagnose code-review repo-review code-delivery audit-security chatgpt-review-bridge implement-frontend implement-rust audit-frontend audit-rust ops-browser ops-client human-writing
```

List available skills without installing:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

For the full command list and available skill names, see [`INSTALL.md`](INSTALL.md).

## Skills

| Skill | Use when |
| --- | --- |
| `repo-context` | Grounding repository work in real commands, paths, entry points, docs, project classes, and existing reuse/reference candidates before guessing. |
| `code-planner` | Planning future codebase work, splitting tasks, defining validation gates, and coordinating auditable subagents before implementation. |
| `diagnose` | Reproducing technical failures, isolating variables, confirming root causes, and handing verified remediation to the matching implementation skill. |
| `code-review` | Reviewing existing local Git changes, dirty-tree ownership, contract chains, commit grouping, and exact staging plans before commit. |
| `repo-review` | Independently reviewing an immutable repository snapshot, branch comparison, commit range, pull request, release candidate, or verified review package with consolidated P0-P3 findings. |
| `code-delivery` | Delivering reviewed local changes with path-limited staging, commits, pushes, branch sync, squash-to-main, cleanup, and remote proof. |
| `audit-security` | Auditing known code, API, auth, permission, token/session, upload, logging, dependency, config, or release surfaces for scoped security risks. |
| `chatgpt-review-bridge` | Routing prepared repository review material through standard ChatGPT chats or Projects using capability-aware browser paths, then capturing and locally verifying findings. |
| `implement-frontend` | Implementing frontend UI reuse-first, using existing pages/components as references while preserving lean DOM/CSS, design-system, layout, state, and API contracts. |
| `implement-rust` | Implementing or porting Rust reuse-first with explicit ownership, FFI/unsafe boundaries, behavior parity, idiomatic APIs, and risk-matched validation. |
| `audit-frontend` | Auditing selected frontend profiles across React, Vue, UI/design systems, state/data, accessibility, performance, and Tauri boundaries without splitting by framework. |
| `audit-rust` | Auditing selected Rust profiles for architecture, ownership, concurrency, performance, memory, SQLite, unsafe/FFI, quality gates, and documentation alignment. |
| `ops-browser` | Operating browser pages and collecting screenshots, visual/responsive checks, form/upload/download evidence, console/network data, and session-safe verification. |
| `ops-client` | Verifying or operating specified Tauri/Electron/native desktop clients with launch-command, runtime-source, CGWindowID, real-window, and Accessibility evidence. |
| `human-writing` | Drafting, rewriting, diagnosing, and adapting source-grounded human-quality writing while preserving facts, technical meaning, disclosures, and voice. |

### Core Routing Boundaries

```text
repo-context = what exists, where it lives, and what can be reused
code-review  = whether current local uncommitted changes are safe and ready to commit
repo-review  = what defects exist in an immutable repository/range/PR/release basis
```

These skills all read repository evidence but must remain separate because their primary object, authorization boundary, stop condition, and output contract differ.

### Implementation, Audit, Review, And Delivery Boundaries

- `implement-frontend` and `implement-rust` own requested code changes, refactors, ports, and implementation self-checks.
- `audit-frontend`, `audit-rust`, and `audit-security` are read-only domain specialists. They select only applicable profiles and return bounded findings.
- `code-review` owns local dirty-tree inventory, mixed-hunk classification, contract completeness, staging plans, and commit readiness.
- `repo-review` owns independent review of immutable repository snapshots, ranges, PRs, release candidates, or verified review packages and coordinates bounded specialists.
- `diagnose` owns reproduction and root-cause confirmation; permanent fixes transition to the matching implementation skill.
- `code-delivery` is the sole owner of staging, commits, pushes, squash, cleanup, and other Git mutation after review acceptance.

See [`docs/standards/skill-routing.md`](docs/standards/skill-routing.md) for the design and split/merge criteria.

## Validate Local Skills

For repository development, validate source skill packages before publishing changes:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
```

Useful targeted package checks:

```bash
python3 scripts/validate-skills.py --skill repo-context
python3 scripts/validate-skills.py --skill repo-review
python3 scripts/validate-skills.py --skill diagnose
python3 scripts/validate-skills.py --skill audit-frontend
python3 scripts/validate-skills.py --skill audit-security
```

End-user installation and updates should use the standard `npx skills add` and `npx skills update` flow.

## Principles

- keep active root content reusable
- keep prompt and skill assets directly accessible
- keep publishable skills self-contained; repo-local prompts can supplement them but should not be required
- let prompts capture task language, and let skills capture stable execution workflows
- split a public skill only when user intent, authority, workflow, output contract, and non-trigger set are materially distinct
- prefer internal profiles when framework or checklist variants share the same ownership and output contract
- keep skill trigger/eval cases in `references/eval-cases.md` and validate packages before publishing
- keep shared automation standards in `docs/standards/`
- keep downstream repository task details out of AICraft except for the registry index
- retire time-sensitive or old workflow material from the active root
- avoid mixing transient notes and historical references into the active root
