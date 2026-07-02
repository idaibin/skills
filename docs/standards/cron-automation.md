# Cron Automation Standard

## Purpose

This standard defines the boundary between a ChatGPT scheduled task and GitHub-hosted automation documents.

## What stays in the ChatGPT scheduled task

The scheduled task should only keep bootstrap information:

- Task title.
- Schedule and timing mode.
- Default timezone.
- Target repository name.
- The exact GitHub documents that must be read before execution.
- A hard stop rule when required documents cannot be read.

The scheduled task prompt must not duplicate full business rules, frontmatter schemas, content templates, branch strategies, or quality rules.

## What stays in GitHub documents

GitHub-hosted automation documents should contain the durable execution rules:

- Shared standards from `idaibin/aicraft/docs/standards/**`.
- Target repository task spec under `docs/automation/**`.
- Allowed paths.
- Output file paths.
- Frontmatter schema.
- Content format.
- Validation checklist.
- Task-specific commit message.
- Task-specific skip rules.

## Required read order

Every scheduled run must read documents in this order:

1. `idaibin/aicraft/docs/standards/cron-automation.md`
2. `idaibin/aicraft/docs/standards/github-branching.md`
3. `idaibin/aicraft/docs/standards/ai-content-quality.md`
4. Target repository `docs/repo-scope.md`
5. Target repository task spec under `docs/automation/**`

If any required document cannot be read, stop and report the blocker. Do not continue from memory.

## Timezone

Default automation timezone for these content tasks is:

```text
UTC+08:00 / Asia/Shanghai
```

Rules:

- Generate task dates in `Asia/Shanghai` unless a task spec explicitly overrides it.
- Generate branch timestamps in `Asia/Shanghai`.
- Convert source UTC timestamps before writing local display fields.
- Use explicit offsets such as `2026-07-02T08:54:00+08:00` when full timestamps are stored.
- Do not use `CST` because it is ambiguous.
- Do not display or store raw UTC as local task time.

## Failure behavior

Stop instead of guessing when:

- Required GitHub documents cannot be read.
- The latest target branch cannot be read.
- Source evidence is insufficient.
- The target repository has changed and the final tree cannot be safely rebuilt.
- Validation cannot be completed.
- The tool cannot perform the required Git operation safely.

## Reporting

Every run should report:

- Documents read.
- Target repository and branch.
- Branch used.
- Files changed.
- Topics generated.
- Topics skipped and reasons.
- Validation performed.
- Whether a PR was created. This should be `No` unless explicitly requested.
- Any blocker or unsupported operation.
