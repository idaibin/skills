# Content Automation Task Template

Use this template in a target repository under:

```text
docs/automation/<task-name>.md
```

The target repository document should only contain repository-specific differences. Shared rules should be referenced from `idaibin/aicraft/docs/standards/**`.

```md
# <Task Name>

## Authority

This task follows:

- `idaibin/aicraft/docs/standards/cron-automation.md`
- `idaibin/aicraft/docs/standards/github-branching.md`
- `idaibin/aicraft/docs/standards/ai-content-quality.md`
- `docs/repo-scope.md`

This file only defines repository-specific task rules.

## Target Repository

- Repository: `<owner>/<repo>`
- Production branch: `main`
- Task name: `<stable-task-name>`
- Schedule: `<daily/hourly/custom>`
- Timezone: `UTC+08:00 / Asia/Shanghai`
- PR: `No`

## Objective

Describe the task objective in one short paragraph.

## Allowed Paths

```text
<allowed path 1>
<allowed path 2>
```

## Disallowed Paths

```text
<disallowed path 1>
<disallowed path 2>
```

## Inputs and Source Priority

List task-specific sources or source priorities.

## Output Files

```text
<path pattern>
```

## Frontmatter or Data Schema

```yaml
field: value
```

## Body Format

Describe the required Markdown, MDX, JSON, or asset format.

## Task-specific Deduplication

List keys or comparisons unique to this repository.

## Skip Rules

Define when the task should skip writing content.

## Validation

List repository-specific validation checks.

## Commit Message

```text
<fixed or patterned commit message>
```
```
