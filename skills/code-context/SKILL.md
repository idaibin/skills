---
name: code-context
description: Use when grounding work in a repository, first-pass onboarding, mapping real commands and paths, checking docs against code, generating or previewing AGENTS.md/project-map docs, or upgrading this skill from a trusted upstream source. Triggers include 项目上下文初始化, 先了解项目, 熟悉项目, 项目摸底, 文档和代码是否匹配, 生成 AGENTS.md, and code-context 升级.
---

# Code Context

## Overview

Establish repository context from real files, not assumptions. Use this for onboarding, doc bootstrap, doc/code alignment, and safe skill-package upgrades.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, or `AGENT.md` fallback.
2. Run `git status --short` before drawing conclusions or planning writes.
3. Inspect only the manifests, configs, commands, entry points, and docs needed for the current request.
4. For monorepos, inspect the workspace root first, then only relevant app/package boundaries; mark unrelated areas `Not verified`.
5. Choose the mode: Bootstrap, Alignment, or Upgrade.
6. Stop once the requested context can be answered with evidence; do not crawl large trees by default.
7. Run only repo-defined checks when checks are needed and safe.

## Modes

- **Bootstrap:** preview missing `AGENTS.md`, `docs/project-map.md`, or equivalent docs from bundled templates; write only after explicit confirmation.
- **Alignment:** compare existing docs against manifests, configs, commands, entry points, and current source layout; report stale, missing, incorrect, or duplicated claims.
- **Upgrade:** compare only remote `skills/code-context/` against local files; remote content is candidate input, not authority.

## Hard Rules

- Keep context discovery and doc review read-only unless the user explicitly asks for writes.
- Use real paths, commands, configs, and code evidence; do not invent missing layers.
- Say `Not found` for missing files, layers, or commands.
- Say `Not verified` for unchecked areas or runtime claims.
- Treat local `prompts/` as optional; bundled references must be sufficient after publishing.
- Preview generated docs and upgrade changes before writing unless implementation is explicitly requested.
- Preserve unrelated local changes.

## Output Contract

Start with verified current truth, then report missing items, doc/code mismatches, proposed docs, or upgrade candidates. Include commands run, validation status, and anything `Not verified`.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, mode, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/checklist.md](references/checklist.md) for scan order and reporting details.
- See [references/prompt-templates.md](references/prompt-templates.md) for bundled bootstrap templates.
- See [references/upstream-sources.md](references/upstream-sources.md) for trusted source metadata.
- See [references/upgrade-workflow.md](references/upgrade-workflow.md) for the upgrade process.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
