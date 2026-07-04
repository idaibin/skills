# Review Checklist

Use this checklist before planning or making commits in a dirty worktree or reviewing interface contracts. Trigger phrases include `pre-commit review`, `review all changes`, `API contract-chain review`, `classify changes`, `split commits`, and `generate commit message`.

## Required Evidence

- Read `AGENTS.md` first when present; use nearest `AGENTS.md` for subprojects and `AGENT.md` only as a fallback.
- Run `git status --short`.
- Run `git diff --stat` and `git diff --name-status`.
- If anything is staged, run `git diff --cached --stat` and `git diff --cached --name-status`.
- Inspect actual diffs for every file that may enter a commit group.
- Identify the complete local change scope before choosing the commit-planning or staging scope.
- Identify ownership for every changed file before editing, staging, or committing.

## Inventory

- List files by state: modified, new, deleted, renamed, generated.
- Group files by intent, not by path alone.
- Separate code, docs, config, CI, deploy, and refactor work unless they are tightly coupled.
- Mark current-session or explicitly requested edits as `task-owned`.
- Mark pre-existing edits required by the requested work as `related-existing`, then review and modify them only as needed for the requested scope.
- Mark unrelated pre-existing edits as `unrelated-existing` and leave them untouched.
- Mark files with both in-scope and out-of-scope hunks as `mixed-hunk`; do not stage the whole file unless every hunk belongs to the current commit group.
- Mark unclear ownership as `unknown`, report it before staging or editing, and ask only when the requested scope cannot be determined from evidence.

## Completeness

- Verify the functional change is closed.
- Walk every changed line that may enter a commit and ask whether the task requires that exact line; remove or exclude lines that are only cleanup, modernization, future flexibility, or "while here" changes.
- Verify changed files sit in the expected project directories and follow existing module/component boundaries.
- Verify changed code follows local naming, style, and implementation conventions.
- Verify docs were updated when contracts, commands, or paths changed.
- Verify docs and code do not contradict each other.
- For interface or contract changes, verify the real contract chain end to end:
  - backend route, endpoint path, request method, and field definitions
  - request helper, URL shaping, response unwrapping, and error handling
  - frontend or client type definitions
  - page, component, service, or caller usage
  - data transformation, normalization, default values, and compatibility layers
  - runtime payload or response evidence; write `Not verified` when runtime evidence was not checked
- Verify tests or validation commands were updated when behavior changed.
- Check type, lint, build, formatter, unused import, unused definition, and broken reference risk.
- Check for missing config, workflow, or path updates.
- Check for files that should not be committed.
- Record what was verified and what is still `Not verified`.

## Split Rules

- Prefer one semantic change per commit.
- Keep dependent files together when one file cannot stand alone.
- Keep code + migration together.
- Keep code + contract docs together when the docs describe the same change.
- Separate build/deploy/CI changes from feature behavior when possible.
- Separate docs-only changes from code changes when possible.
- Keep generated artifacts out unless they are the requested deliverable.

## Common Cases

- Feature work with tests and contract docs: one commit if the files describe the same change.
- Artifact or path renames across `justfile`, Dockerfiles, and workflows: one deploy commit.
- Repository docs and readmes that only describe the new contract: one docs commit.
- Generated outputs such as build caches or release artifacts: do not commit unless the artifact itself is the deliverable.
- User-owned local edits mixed with task files: stage only the requested slice and mention the excluded files.
- Adjacent cleanup noticed during review: report it as a follow-up or exclude it from the current commit unless the user explicitly expanded scope.

## Do Not Commit

- Build outputs such as `target/`.
- Runtime logs, caches, screenshots, and temp files.
- Local env files and other machine-specific artifacts.
- Generated artifacts unless they are the intended deliverable.
- Unrelated local changes, even when they are already in the same directory.

## Staging Rules

- Use exact path-limited staging commands.
- Verify staged files before each commit.
- For `mixed-hunk` files, use hunk-level staging or split the file before staging; then verify the staged diff, not only the staged file list.
- Do not use `git add .`, `git add -A`, directory-wide adds, or broad wildcard staging unless the user explicitly approves that exact full scope.
- If there are pre-existing staged files outside the current group, stop and report the conflict before committing.
- For direct user requests, default to the full reviewed local change scope unless the user explicitly limits the commit scope.
- If the user asks to commit only current context, current session, or this task's changes, default to staging only that subset after full-scope review.
- If another AI agent invokes this skill as a sub-workflow, follow that caller's stated scope after full-scope review.
- Ask before staging only when the requested subset is ambiguous, required files outside the subset appear necessary, or pre-existing staged files conflict with the requested scope.

## Delivery Boundary

- Use this skill to produce local review findings, safe commit groups, and local commit actions only when the user explicitly asks.
- Use `code-delivery` when the requested outcome includes pushing, syncing with a remote branch, squash-merging to `main`, deleting temporary branches, or proving remote state after delivery.

## Commit Message Style

- Use Conventional Commits.
- Keep the message concise.
- Match the user's requested language or repository convention; otherwise use concise English.
