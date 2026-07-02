# Code Context Checklist

Use this checklist when applying `code-context` to understand a repository, bootstrap missing context docs, review existing docs against code, or upgrade this skill from a trusted upstream source. Trigger phrases include `repository context`, `understand this project`, `do not guess`, `real commands`, `real entry points`, `doc/code alignment`, and `code-context upgrade`.

## Scan Order

1. Read `AGENTS.md` first when present; use nearest subproject `AGENTS.md` and `AGENT.md` only as fallback.
2. Run `git status --short` to capture real dirty-tree state.
3. Read `README.md`, root manifests, lockfiles, and framework/build configs.
4. If the repo is a monorepo, identify the workspace root and then inspect only the app/package boundaries relevant to the request.
5. Map the real source tree only to the depth needed for the current answer.
6. Read the files that implement project-specific conventions when those conventions affect the requested context.
7. Run baseline checks only with commands already defined by the repo.
8. Detect context doc state:
   - missing or sparse docs: use Bootstrap mode
   - existing docs with current-truth claims: use Alignment mode
   - remote source or version supplied for this skill: use Upgrade mode

## What To Report

- Tech stack
- Package manager
- Runtime requirements
- Startup, dev, serve, preview, build, lint, typecheck, and test commands
- Real paths for entry points, routes, shared components, application layers or services, state, styles, and tests
- Files that are absent, reported as `Not found`
- Dirty worktree state and unrelated changes that must be preserved
- Checks performed, failures, and `Not verified` items
- Selected bundled templates, optional local prompt assets, and previewed drafts in Bootstrap mode
- Doc/code mismatches and suggested changes in Alignment mode
- Upstream URL, resolved version, compared skill-package paths, proposed changes, and rejected candidates in Upgrade mode

## Baseline Check Rules

- Prefer existing scripts or documented commands.
- Do not invent replacement commands.
- If a command is missing, report `Not found`.
- If a command fails, classify it as:
  - environment issue
  - configuration issue
  - existing project issue
- If a repo or user requires a specific tool, browser, command, or runtime, do not substitute another one. Report unavailable requirements as blockers.

## Bootstrap Mode

- Use when `AGENTS.md`, `docs/project-map.md`, or equivalent context docs are missing.
- Use `references/prompt-templates.md` first. It is bundled with the skill and must work after publishing.
- If local `prompts/` exists, inspect it only as an optional override or project-specific supplement.
- Prefer initialization, repo-rule, task-start, and doc-alignment templates.
- Explain which bundled templates or local prompt assets were selected and why.
- Generate draft docs from repository truth, not from template or prompt assumptions.
- Preview drafts first. Do not write files until the user confirms.

## Alignment Mode

- Use when project docs already exist.
- Compare docs against manifests, configs, commands, source entry points, routes/modules, tests, and workspace membership.
- Report stale, missing, incorrect, duplicated, or unverifiable doc claims.
- Suggest exact doc changes or sections to update.
- Do not modify docs unless the user explicitly asks.

## Upgrade Mode

- Use when the user supplies a GitHub URL, branch, tag, commit, directory, or file URL for updating this skill.
- Read `references/upstream-sources.md` for known default sources.
- Prefer commit SHA over moving branches; resolve and report the SHA when using a branch.
- Inspect upstream content read-only.
- Compare upstream `skills/code-context/` against local files.
- Classify candidates as skill-core, bundled-reference, agent-interface, or reject.
- Preview proposed changes first. Do not write files until the user confirms.
- Keep the skill self-contained; do not introduce required external prompt dependencies or pull from remote repository-level `prompts/`.

## Read-Only Rules

- Do not modify source files during context discovery or doc review.
- Do not generate file writes unless the user explicitly confirms a preview or asks for writing.
- If docs are drafted, keep current truth separate from history or plans.
- Preserve unrelated local changes.

## Draft Output Outline

### AGENTS.md
- Repository purpose
- Directory structure
- Working rules
- Code change constraints
- Required checks after changes
- Final report format
- Disallowed actions

### docs/project-map.md
- Tech stack
- Install / start / test / build commands
- Directory structure
- File chain for typical page work
- Locations for components, interfaces, state, styles, and tests
- Frequent edit areas
- Risky areas
- Recommended reading order
