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
  - grouped by use case, such as development workflows, automation, agent systems, design, and project-specific prompts
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

Install globally for both OpenAI Codex and Anthropic Claude Code:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --global --agent codex claude-code
npx skills update --global
```

The CLI records the source needed for later updates. Manually copied skill
folders are not reliably updateable through `npx skills update`.

Install selected skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map code-planner diagnose repo-review repo-delivery audit-security chatgpt-review implement-frontend implement-rust audit-frontend audit-rust ops-browser ops-client human-writing
```

List available skills without installing:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

For project/global scope, agent-specific installation, update limitations, and
rename migration, see [`INSTALL.md`](INSTALL.md).

## Skills

| Skill | Use when |
| --- | --- |
| `repo-map` | Maintaining the smallest useful semantic repository map of real boundaries, commands, task routes, and verified reusable components, functions, types, or APIs. |
| `code-planner` | Planning future codebase work, splitting tasks, defining validation gates, and coordinating auditable subagents before implementation. |
| `diagnose` | Reproducing technical failures, isolating variables, confirming root causes, and handing verified remediation to the matching implementation skill. |
| `repo-review` | Read-only review of local worktrees, fixed commits/ranges, PRs, releases, or review packages, with basis-specific ownership/readiness or P0-P3 findings. |
| `repo-delivery` | Delivering reviewed local changes with path-limited staging, commits, pushes, branch sync, squash-to-main, cleanup, and remote proof. |
| `audit-security` | Auditing known code, API, auth, permission, token/session, upload, logging, dependency, config, or release surfaces for scoped security risks. |
| `chatgpt-review` | Preparing or routing repository review material through standard ChatGPT chats or Projects, then capturing and locally verifying findings. |
| `implement-frontend` | Implementing frontend UI reuse-first with detected React, Vue, Tailwind, CSS, design-system, state, layout, and API-contract profiles. |
| `implement-rust` | Implementing or porting Rust reuse-first with explicit ownership, FFI/unsafe boundaries, behavior parity, idiomatic APIs, and risk-matched validation. |
| `audit-frontend` | Auditing selected React, Vue, Tailwind/CSS, UI/design-system, state/data, accessibility, performance, and Tauri profiles without splitting by technology. |
| `audit-rust` | Auditing selected Rust profiles for architecture, ownership, concurrency, performance, memory, SQLite, unsafe/FFI, quality gates, and documentation alignment. |
| `ops-browser` | Operating browser pages and collecting screenshots, visual/responsive checks, form/upload/download evidence, console/network data, and session-safe verification. |
| `ops-client` | Verifying or operating specified Tauri/Electron/native desktop clients with launch-command, runtime-source, CGWindowID, real-window, and Accessibility evidence. |
| `human-writing` | Drafting, rewriting, diagnosing, and adapting source-grounded human-quality writing while preserving facts, technical meaning, disclosures, and voice. |

### Repository Engineering Boundaries

```text
repo-map      = what exists, where it lives, and what can be reused
repo-review   = whether local or immutable repository changes are safe, using the matching review-basis mode
repo-delivery = authorized staging, commits, pushes, synchronization, and cleanup
```

`repo-review` keeps Worktree and immutable review evidence separate internally while presenting one public review entrypoint.

`repo-map` normally maintains `<map-root>/docs/repo-map/README.md` as a compact semantic index, not a mirrored source tree. It first resolves a containing Git root; from a non-Git path it discovers child Git roots, or treats the path as an ordinary directory project when none exist. It records real ownership and runtime boundaries, shortest task routes, and verified reuse entries with canonical definitions, access/registration entries, representative consumers, and usage constraints. `repo-review` may use that map to navigate, but independently verifies every finding at its selected Worktree or immutable basis. Semantic drift is repaired as the smallest dependent consistency closure; missing paths are recovered from the nearest existing ancestor without rebuilding verified sections.

### Implementation, Audit, Review, And Delivery Boundaries

- `implement-frontend` and `implement-rust` own requested code changes, refactors, ports, and implementation self-checks.
- `audit-frontend`, `audit-rust`, and `audit-security` are read-only domain specialists. They select only applicable profiles and return bounded findings.
- `repo-review` owns local dirty-tree readiness and immutable snapshot/range/PR/release review through separate basis modes, and coordinates bounded specialists.
- `diagnose` owns reproduction and root-cause confirmation; permanent fixes transition to the matching implementation skill.
- `repo-delivery` is the sole owner of staging, commits, pushes, squash, cleanup, and other Git mutation after review acceptance.

See [`docs/standards/skill-routing.md`](docs/standards/skill-routing.md) for the design and split/merge criteria.

## Validate Local Skills

For repository development, validate source skill packages before publishing changes:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
```

The validator also checks the symmetric nearest-neighbor routing inventory in
[`docs/skills/routing-graph.json`](docs/skills/routing-graph.json) and requires
both endpoint skills to cover each other in routing evals.

Useful targeted package checks:

```bash
python3 scripts/validate-skills.py --skill repo-map
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
