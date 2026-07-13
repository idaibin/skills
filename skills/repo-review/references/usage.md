# Repository Review

## Use `repo-review` When

- reviewing current staged, unstaged, or untracked changes before commit;
- classifying dirty-tree ownership or mixed hunks;
- preparing semantic commit groups and exact staging guidance;
- reviewing a fixed commit, `base..head`, branch comparison, or PR;
- reviewing a release candidate or verified review package;
- coordinating bounded frontend, Rust, or security specialist findings.

## Nearest Skill Boundaries

| Request | Owner |
| --- | --- |
| Map directories, architecture, commands, conventions, and reuse entries | `repo-map` |
| Review any local or immutable repository change basis | `repo-review` |
| Audit only a known security surface | `audit-security` |
| Diagnose a concrete failure | `diagnose` |
| Apply accepted fixes | matching `implement-*` |
| Stage, commit, push, squash, or clean branches | `repo-delivery` |

## Examples

### Worktree

`Review all local changes, preserve unrelated edits, split semantic commits, and give exact staging guidance.`

Inventory status/index evidence, classify ownership and mixed hunks, inspect complete candidate diffs, and do not mutate Git.

### Commit range

`Review 23d30ccd..d1c5f0d8 independently and return P0-P3 findings.`

Resolve both endpoints to immutable SHAs before conclusions.

### Pull request

`Review PR 42 without posting comments.`

Verify complete PR evidence and resolved SHAs; comment posting remains unauthorized.

### Release candidate

`Review this release candidate for migrations, packaging, CI, rollback, and security configuration.`

Use the immutable candidate revision and report merge/release implications.

### Repo-map navigation

A `repo-map` artifact may identify owners and shortest reading paths. Independently verify finding facts at the selected basis. If a mapped path is stale, search from the nearest existing ancestor and route document repair to `repo-map`.

## Output

All modes report basis, scope, findings, evidence, validation, exclusions, and gaps. Worktree mode adds ownership, mixed-hunk risks, commit groups, staging guidance, and commit messages. Immutable modes add resolved SHAs and merge/release implications.
