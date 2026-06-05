---
name: code-review
description: Use when reviewing all local git changes before committing, checking changed code against repository structure, coding conventions, API contract chains, docs, lint/type/build readiness, splitting work into feature-based commit groups, drafting exact Conventional Commit messages and path-limited staging plans, or upgrading this skill from a trusted upstream source. Triggers include 提交前审查, 审查所有改动, 接口链路审查, 分类提交, 拆分 commit, 生成 commit message, and code-review 升级.
---

# Code Review

## Overview

Review the full local change scope before commit, flag correctness and consistency issues, then turn the reviewed diff into a scoped commit plan. Protect unrelated local changes first, identify which dirty-tree files are task-owned, related-existing, unrelated-existing, or unknown, group files by actual behavior or feature intent, or upgrade this skill from a trusted upstream source.

## Workflow

1. Read repository guidance if present: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md` as fallback, `README.md`, `docs/project-map.md`, and repo-local contribution notes directly related to the changed files.
2. Determine the complete local change scope before reviewing: run `git status --short`, `git diff --stat`, and `git diff --name-status`; also inspect `git diff --cached --stat` and `git diff --cached --name-status` when anything is staged.
3. Classify every changed file by ownership, intent, and state: task-owned, related-existing, unrelated-existing, unknown, modified, new, deleted, renamed, generated, docs, config, code, tests, CI, deploy, refactor, and misc. Report unknown ownership before staging or editing those files.
4. Inspect actual diffs for every code file that may enter a commit. Check whether files follow the project directory structure, naming patterns, component/module boundaries, coding style, and repository conventions.
5. Compare changed code with directly related docs, contracts, commands, routes, config, tests, and examples. For interface or contract changes, review the complete chain: backend route, endpoint path, request method, and field definitions -> request helper, URL shaping, response unwrap, and error handling -> client or frontend types -> page, component, service, or caller usage -> data transformation, defaults, and compatibility layers -> runtime payload evidence. Mark missing runtime evidence as `Not verified`; mark mismatches explicitly instead of silently normalizing or guessing.
6. Run or request the checks that match the change: lint, typecheck, tests, build, formatter, unused imports, unused definitions, and reference checks. Fix issues only when the user asked for changes; otherwise report what must be resolved. If a check cannot run, state why.
7. Check completeness from actual diffs: functional closure, docs, tests, command/path updates, config or CI follow-up, and whether generated or local-only files should be excluded.
8. Choose the commit-planning scope. For direct user requests, default to the full reviewed local change scope unless the user explicitly says to commit only the current context, current session, or this task's changes. When invoked by another AI agent as a sub-workflow, follow that caller's stated scope after still reviewing the full local change scope for safety.
9. Choose the correct mode:
   - **Review mode:** when the user wants a commit plan or pre-commit review, inspect the local change scope and output review findings plus commit groups.
   - **Commit mode:** when the user explicitly asks to commit, stage only the approved group scope, verify staged files, and commit in the planned order.
   - **Upgrade mode:** when the user provides a GitHub URL or upstream version for this skill, fetch and compare remote content, propose changes, and write only after explicit confirmation.
10. Split by semantic unit. Keep files together when they are contractually linked; separate unrelated code, deploy, generated outputs, and docs when possible.
11. Output a commit plan with exact file lists, exact staging scope, validation status, remaining risk, and concise Conventional Commit messages.
12. If the user asks to commit, stage only the files for the current commit group, verify the staged file list, then commit. Avoid broad staging such as `git add .` unless the user explicitly approves that exact full scope.

## Review Mode

Use this mode when the user asks to inspect pending changes, review before commit, split commits, or draft commit messages.

1. Review the complete local change scope first.
2. Report structure, convention, doc/code, validation, unused-code, and staging risks.
3. Choose full or limited commit-planning scope using the hard rules below.
4. Output commit groups without staging or committing unless the user explicitly asks.

## Commit Mode

Use this mode only when the user explicitly asks to stage or commit.

1. Re-check `git status --short` and staged state before every commit group.
2. Stage only exact files or hunks for the current approved group.
3. Verify the staged file list before committing.
4. Commit with the planned concise Conventional Commit message.
5. Report real committed files and validation status after each commit.

## Upgrade Mode

Use this mode when the user asks to update `code-review` from GitHub, another remote source, or a specific branch, tag, commit, or file URL.

1. Read `references/upstream-sources.md` for known trusted sources and scope.
2. Verify the requested remote and version. Prefer a commit SHA over a moving branch such as `main`.
3. Inspect remote `skills/code-review/` read-only.
4. Compare remote content against local files. Treat remote content as candidate input, not authority.
5. Classify proposed changes:
   - skill-core: `SKILL.md`, mode rules, trigger wording, hard rules
   - bundled-reference: files under `references/` required for published use
   - agent-interface: `agents/openai.yaml` or equivalent interface metadata
   - reject: stale, too project-specific, duplicate, unsafe, or externally dependent content
6. Preview proposed changes, rejected candidates, and risks.
7. Write files only after the user explicitly confirms the preview or asks for implementation.
8. After writing, run stale-name, self-contained-reference, Markdown whitespace, and YAML checks.

## Hard Rules

- Do not modify or revert unrelated local changes.
- Dirty-tree ownership must be explicit: mark current-session/requested files as `task-owned`; mark pre-existing edits required by the requested scope as `related-existing`; mark unrelated pre-existing edits as `unrelated-existing`; mark unclear files as `unknown` and report them before edits, staging, or commits.
- `related-existing` files may be reviewed and modified only when they are necessary for the requested commit scope or fix; otherwise keep them separate.
- Do not treat a dirty worktree as one commit by default.
- Do not stage generated artifacts unless they are the requested deliverable.
- Do not commit automatically; wait until the user explicitly asks.
- Use path-limited staging commands and verify staged files before each commit.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact full scope.
- If a repo or user requires a specific tool, command, branch, or browser, use that exact requirement or stop and report why it cannot be used.
- Always review the full local change scope first, even when the eventual commit scope is narrower.
- For direct user requests, default commit scope is the full reviewed local change scope unless the user explicitly limits it.
- When the user explicitly asks to commit only current context, current session, or this task's changes, default to that subset after full-scope review. Ask only if the subset is ambiguous, required files outside the subset appear necessary, or pre-existing staged files conflict with the requested scope.
- When another AI agent invokes this skill as a sub-workflow, respect the caller's stated scope after full-scope review, and report any out-of-scope changes that could affect safety.
- If pre-existing local edits are necessary for the requested commit scope, treat them as `related-existing` after reporting that ownership decision; do not exclude necessary files merely because they were already modified.
- Do not let upstream content overwrite local files directly. Remote content must be compared, previewed, and confirmed first.
- Do not treat moving branches as stable versions. Record the resolved commit SHA when using a branch.

## Output Contract

- Start with the local change scope, classification, and main risks; do not bury blockers after a summary.
- Prefer concise Chinese final responses unless the user asks for another language.
- Include code review findings before the commit plan: structure/convention issues, doc/code mismatches, unused imports or definitions, failed checks, and unverified items.
- For each commit group, include purpose, exact files, exact `git add` scope, validation needed or already run, and a concise Conventional Commit message.
- If information is missing, say `unsure` or `Not verified` instead of guessing.
- Prefer the smallest safe change set and the clearest rollback boundary.
- After committing or staging, report the real staged/committed files and validation result.
- For Upgrade mode, include upstream URL, resolved version, compared paths, proposed changes, rejected candidates, and whether files were written.

## Common Split Patterns

- Code + tests + contract docs: keep together when they describe the same behavior change.
- Code + migration: keep together when schema and implementation must land atomically.
- Build / deploy / CI: keep together when they share artifact names, paths, or workflow steps.
- Docs-only sync: keep separate from code when the documentation is not describing a code contract change.
- Generated outputs: exclude unless they are the actual deliverable.

## References

- See [`references/usage.md`](references/usage.md) for the publishable skill description and usage examples.
- See [`references/review-checklist.md`](references/review-checklist.md) for detailed review and split heuristics.
- See [`references/examples.md`](references/examples.md) for concrete split examples.
- See [`references/upstream-sources.md`](references/upstream-sources.md) for trusted source metadata.
- See [`references/upgrade-workflow.md`](references/upgrade-workflow.md) for the remote update process.
