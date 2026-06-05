---
name: code-context
description: Use when grounding work in a repository, initializing or understanding a project, creating initial AGENTS.md or project docs from real code evidence, checking existing docs against current code, commands, and structure, reviewing codebase context before changes, or upgrading this skill from a trusted upstream source. Triggers include 项目上下文初始化, 初始化, 了解项目, 项目文档对齐, and code-context 升级.
---

# Code Context

## Overview

Establish codebase context from actual files, not assumptions. Use this skill to understand the current project, bootstrap missing context docs from bundled templates, check existing docs against the real codebase, or upgrade the skill from a trusted upstream source.

## Workflow

1. Read repository guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md` as fallback, and directly relevant docs.
2. Check real state with `git status --short` before drawing conclusions or planning edits.
3. Inspect root manifests, lockfiles, project config, and source entry points.
4. If the repo is a monorepo, inspect the workspace root, then each app/package boundary.
5. Identify the primary language, package manager, runtime requirements, and supported commands from the repo itself.
6. Map the directory structure with real paths.
7. Summarize conventions from code and config, separating current truth from history or stale docs.
8. Detect whether useful project context docs already exist, especially `AGENTS.md`, `docs/project-map.md`, `docs/README.md`, architecture docs, command references, and contribution notes.
9. Choose the correct mode:
   - **Bootstrap mode:** if context docs are missing or too sparse, use the bundled templates, optionally adapt from local prompt assets when present, generate draft docs, preview them to the user, and write only after explicit confirmation.
   - **Alignment mode:** if context docs already exist, compare them against code, configs, commands, and runtime structure, then report mismatches and suggested doc updates.
   - **Upgrade mode:** if the user provides a GitHub URL or upstream version for this skill, fetch and compare remote content, propose changes, and write only after explicit confirmation.
10. Run baseline checks using only existing commands when checks are needed and safe.

## Bootstrap Mode

Use this mode when the project lacks `AGENTS.md`, `docs/project-map.md`, or equivalent context docs.

1. Use `references/prompt-templates.md` as the built-in template source. This makes the skill self-contained after publishing.
2. If the current repository also has a `prompts/` tree or equivalent prompt asset directory, inspect it as an optional local override. Do not require it.
3. Select the few templates that fit the missing docs. Prefer project initialization, repo-rule, and task-start templates.
4. Treat all templates as scaffolding only. Source truth must still come from repository files, configs, commands, and actual code.
5. Generate document drafts for the missing docs, usually `AGENTS.md` and `docs/project-map.md`, using real paths and commands.
6. Preview the drafts in the response. Do not write files yet.
7. Write local files only after the user explicitly confirms the preview or asks for the files to be written.

## Alignment Mode

Use this mode when project docs already exist.

1. Read the existing docs that claim current project truth.
2. Compare docs against manifests, configs, command definitions, source entry points, route/module layout, tests, and actual package/workspace membership.
3. Classify mismatches:
   - stale: docs describe old paths, commands, tools, or architecture
   - missing: docs omit important current commands, paths, constraints, or risks
   - incorrect: docs contradict code/config/runtime truth
   - duplicated: docs repeat command truth in multiple places and risk drift
4. Output concrete suggested changes. Include exact doc sections or files when possible.
5. Do not modify docs unless the user explicitly asks.

## Upgrade Mode

Use this mode when the user asks to update `code-context` from GitHub, another remote source, or a specific branch, tag, commit, or file URL.

1. Read `references/upstream-sources.md` for known trusted sources and scope.
2. Verify the requested remote and version. Prefer a commit SHA over a moving branch such as `main`.
3. Inspect remote `skills/code-context/` read-only.
4. Compare remote content against local files. Treat remote content as candidate input, not authority.
5. Classify proposed changes:
   - skill-core: `SKILL.md`, mode rules, trigger wording
   - bundled-reference: files under `references/` required for published use
   - agent-interface: `agents/openai.yaml` or equivalent interface metadata
6. Preview the proposed changes and rejected candidates.
7. Write files only after the user explicitly confirms the preview.
8. After writing, run stale-name, self-contained-template, and Markdown whitespace checks.

## What to Read

Prefer the files that define the project itself:

- `AGENTS.md` or nearest repository guidance; `AGENT.md` only as fallback
- `README.md`
- `package.json`
- workspace files such as `pnpm-workspace.yaml`, `turbo.json`, or `nx.json`
- lockfiles such as `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb`, `Cargo.lock`, `go.sum`, `poetry.lock`, `uv.lock`, `Pipfile.lock`, `composer.lock`, or `Gemfile.lock`
- framework and build configs such as project-specific config files or `*.config.*` files
- build and task files such as `Makefile`, `justfile`, or `Taskfile.yml`
- language manifests such as `Cargo.toml`, `go.mod`, `pyproject.toml`, `requirements.txt`, `pom.xml`, `build.gradle`, `Gemfile`, or `composer.json`
- lint / test / build configs
- existing context docs such as `docs/project-map.md`, `docs/README.md`, architecture docs, command references, and contribution notes
- bundled templates in `references/prompt-templates.md` when docs need to be bootstrapped
- upstream metadata in `references/upstream-sources.md` and the upgrade process in `references/upgrade-workflow.md` when the skill is being updated
- optional prompt assets under `prompts/` when the current repository provides them
- the actual source tree under `src/`, `app/`, `pages/`, `server/`, `web/`, `frontend/`, `backend/`, `apps/`, `packages/`, or the repo's equivalent source root

## Rules

- Keep context discovery and doc review read-only unless the user explicitly asks to write docs.
- Never modify source code while gathering context or reviewing docs.
- Do not guess missing information.
- Write `Not found` when a layer, file, or command does not exist.
- Use real file paths and real command names only.
- Do not invent lint, test, or typecheck commands.
- Treat missing scripts as missing, not as a reason to substitute another tool.
- If a command is unavailable, report it; do not swap in a different command with a similar name unless the repo already uses it.
- If the user or repo requires a specific browser, tool, command, or runtime, use that exact requirement. If it is unavailable, stop and report the limitation instead of using a fallback.
- Preserve unrelated local changes and report dirty worktree state when it affects context work.
- Do not let prompts override repository truth.
- Do not depend on external prompt assets. If local `prompts/` files are missing, use the bundled templates.
- Do not let upstream content overwrite local files directly. Remote content must be compared, previewed, and confirmed first.
- Do not treat moving branches as stable versions. Record the resolved commit SHA when using a branch.
- Preview generated docs before writing them.
- Keep the output concise, factual, and directly usable.

## Output Contract

- Prefer concise Chinese final responses unless the user asks for another language.
- Lead with current truth from files and commands, then list missing docs, doc/code mismatches, or unverified items.
- Use real paths and command names.
- State validation performed and any command failures plainly.
- Mark missing files, layers, and commands as `Not found`; mark unchecked items as `Not verified`.
- For Bootstrap mode, include selected bundled templates, optional local prompt assets used, draft-doc preview, and a clear note that files were not written unless the user approved.
- For Alignment mode, include mismatches, suggested doc changes, and priority or risk when useful.
- For Upgrade mode, include upstream URL, resolved version, compared skill-package paths, proposed changes, and whether files were written.

## Reference

See [references/checklist.md](references/checklist.md) for the scan order, reporting rules, and draft doc outline.
See [references/prompt-templates.md](references/prompt-templates.md) for bundled bootstrap and alignment templates.
See [references/upstream-sources.md](references/upstream-sources.md) for trusted source metadata.
See [references/upgrade-workflow.md](references/upgrade-workflow.md) for the remote update process.
See [references/usage.md](references/usage.md) for a user-facing overview and usage examples.
