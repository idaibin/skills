# GitHub Branching Standard

## Default rule

Do not modify `main` directly unless the user or the target repository task spec explicitly allows it.

Do not create pull requests unless the user explicitly asks for a PR.

## Branch prefixes

Use task-type prefixes:

```text
feat/<name>      feature work
fix/<name>       bug fix
content/<name>   content or documentation work
ci/<name>        CI/CD work
chore/<name>     configuration or maintenance work
refact/<name>    refactor work
release/<name>   release, build, or version work
```

Do not use `codex/` as a default branch prefix for this workspace.

## Scheduled cron branch format

Scheduled content tasks must use this temporary branch format:

```text
cron/<task-name>-YYYYMMDD-HHMM
```

Rules:

- `task-name` must be stable and lowercase.
- `YYYYMMDD-HHMM` must be generated in `UTC+08:00 / Asia/Shanghai`.
- The branch must start from the latest production branch, normally `main`.

Examples:

```text
cron/ai-signals-commit-20260702-0800
cron/feeds-hub-update-20260702-0900
```

## Scheduled production write flow

When a task spec explicitly allows scheduled writes to `main`, use this flow:

1. Read the latest `main`.
2. Create a temporary cron branch from latest `main`.
3. Write all generated files to the temporary branch.
4. Validate the generated result.
5. Reread latest `main` before the final production write.
6. If `main` changed, rebuild the final result on top of latest `main`.
7. Write one final commit to `main` for the run.
8. Do not create a PR.
9. If the safe final write cannot be completed, stop and report the blocker.

## Manual documentation updates

For manual standard, README, or automation-document changes, use a normal task branch such as:

```text
content/automation-standards-YYYYMMDD
```

Keep the branch unmerged unless the user explicitly authorizes updating `main`.

## Commit messages

Use the target repository task spec when it defines a fixed commit message.

For general documentation updates, use concise conventional messages such as:

```text
docs: update automation standards
docs: clarify repository scope
content: update feeds
chore(signals): add AI signals for YYYY-MM-DD
```

## Failure behavior

Do not leave partial production updates on `main`.

If the branch exists, the latest branch cannot be read, or the final write cannot be safely created, stop and report the exact blocker.
