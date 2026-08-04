# Worktree Review Checklist

Use this checklist before delivery from a dirty worktree or when reviewing interface contracts. Trigger phrases include `pre-commit review`, `review all changes`, `API contract-chain review`, `classify changes`, `split commits`, and `generate commit message`.

This checklist is read-only. Do not edit, create, delete, rename, or format worktree files, and do not run write-mode checks. Route fixes to implementation and Git mutation to `repo-delivery`.

## Contents

- [Required Evidence](#required-evidence)
- [Inventory](#inventory)
- [Completeness](#completeness)
- [Split Rules](#split-rules)
- [Common Cases](#common-cases)
- [Do Not Commit](#do-not-commit)
- [Staging-Plan Rules](#staging-plan-rules)
- [Delivery Boundary](#delivery-boundary)
- [Commit Message Style](#commit-message-style)

## Required Evidence

- Read effective repository guidance first, including nearest `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
- Run `git status --short`.
- Run `git diff --stat` and `git diff --name-status`.
- If anything is staged, run `git diff --cached --stat` and `git diff --cached --name-status`.
- Inspect actual diffs for every file that may enter a commit group.
- Identify the complete local change scope before choosing the commit-planning or staging scope.
- Identify ownership for every changed file before proposing staging or delivery.

## Inventory

- List files by state: modified, new, deleted, renamed, generated.
- Group files by intent, not by path alone.
- Separate code, docs, config, CI, deploy, and refactor work unless they are tightly coupled.
- Mark current-session or explicitly requested edits as `task-owned`.
- Mark pre-existing edits required by the requested work as `related-existing`, then review and modify them only as needed for the requested scope.
- Mark unrelated pre-existing edits as `unrelated-existing` and leave them untouched.
- Mark files with both in-scope and out-of-scope hunks as `mixed-hunk`; do not propose whole-file staging unless every hunk belongs to the current commit group.
- Mark unclear ownership as `unknown`, report it before staging or editing, and ask only when the requested scope cannot be determined from evidence.

## Completeness

- Verify the functional change is closed.
- Walk every changed line that may enter a commit and ask whether the task requires that exact line; remove or exclude lines that are only cleanup, modernization, future flexibility, or "while here" changes.
- Verify changed files sit in the expected project directories and follow existing module/component boundaries.
- Verify changed code follows local naming, style, and implementation conventions.
- Verify docs were updated when contracts, commands, or paths changed.
- Verify docs and code do not contradict each other.
- For added, reused, moved, renamed, or deleted structural code, verify:
  - manifests, workspace membership, module exports, and dependency declarations
  - commands, tests, examples, fixtures, and generated-source ownership
  - CI, packaging, release, deploy, service, updater, and runtime paths
  - architecture docs, project maps, indexes, adoption records, and migration notes
  - targeted stale-reference search after the change
- For shared extraction, verify real consumers, product neutrality, stable API, named ownership, shared tests, and consumer validation; reject speculative sharing.
- For interface or contract changes, verify the real contract chain end to end:
  - backend route, endpoint path, request method, and field definitions
  - request helper, URL shaping, response unwrapping, and error handling
  - frontend or client type definitions
  - page, component, service, or caller usage
  - data transformation, normalization, default values, and compatibility layers
  - runtime payload or response evidence; write `Not verified` when runtime evidence was not checked
- Verify tests or validation commands were updated when behavior changed.
- Check type, lint, build, formatter, unused import, unused definition, and broken reference risk. Treat tool output as evidence, then account for public exports, conditional builds, dynamic registration, generation, and external consumers before declaring code dead.
- When relevant, check whether the change creates competing authorities,
  speculative or responsibility-free layers, or a hidden producer/consumer
  contract. Require concrete coordinated-change or reachable failure evidence;
  similarity, file size, wrapper count, and optional lint advice alone are not
  findings.
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
- Keep repository-owned generated artifacts with the semantic change when policy
  requires them; exclude disposable generated output.

## Common Cases

- Feature work with tests and contract docs: one commit if the files describe the same change.
- Artifact or path renames across `justfile`, Dockerfiles, and workflows: one deploy commit.
- Crate/package/module moves: keep manifests, exports, commands, tests, CI/deploy paths, and ownership docs in the semantic change that makes the move valid.
- Repository docs and readmes that only describe the new contract: one docs commit.
- Repository-owned generated clients, schemas, or indexes: when policy requires them,
  verify their authority, diff, and idempotence and keep them with the contract change.
- Build caches or release artifacts: do not commit unless the artifact itself is the deliverable.
- User-owned local edits mixed with task files: plan only the requested staging slice and mention the excluded files.
- Adjacent cleanup noticed during review: report it as a follow-up or exclude it from the current commit unless the user explicitly expanded scope.

## Do Not Commit

- Build outputs such as `target/`.
- Runtime logs, caches, screenshots, and temp files.
- Local env files and other machine-specific artifacts.
- Disposable or ignored generated output; repository-owned generated artifacts follow
  the owning policy and semantic change.
- Unrelated local changes, even when they are already in the same directory.

## Staging-Plan Rules

- Produce exact path-limited staging instructions for `repo-delivery`.
- Inspect any existing staged files and staged diff read-only.
- For `mixed-hunk` files, require hunk-level staging or a split before delivery, followed by staged-diff verification rather than file-list-only proof.
- Do not use `git add .`, `git add -A`, directory-wide adds, or broad wildcard staging unless the user explicitly approves that exact full scope.
- If there are pre-existing staged files outside the current group, report the delivery blocker.
- For direct user requests, default to the full reviewed local change scope unless the user explicitly limits the commit scope.
- If the user asks to commit only current context, current session, or this task's changes, default the staging plan to that subset after full-scope review.
- If another AI agent invokes this skill as a sub-workflow, follow that caller's stated scope after full-scope review.
- Ask for scope clarification only when the requested subset is ambiguous, required files outside it appear necessary, or pre-existing staged files conflict.

## Delivery Boundary

- Use this skill to produce review findings, safe commit groups, exact staging instructions, validation requirements, and commit messages without Git mutation.
- Use `repo-delivery` for staging, local commits, pushes, sync, squash-to-main, branch cleanup, and remote-state proof.

## Commit Message Style

- Use Conventional Commits.
- Keep the message concise.
- Match the user's requested language or repository convention; otherwise use concise English.
