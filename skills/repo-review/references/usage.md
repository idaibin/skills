# Repository Review

## Use `repo-review` When

- reviewing current staged, unstaged, or untracked changes before commit;
- classifying dirty-tree ownership or mixed hunks;
- preparing semantic commit groups and exact staging guidance;
- reviewing a fixed commit or `base..head`, including a branch or PR normalized to immutable SHAs;
- reviewing a verified review package;
- adding release-readiness evidence only when that conditional profile is explicitly requested;
- coordinating bounded frontend/Rust specialist findings and professional Codex Security evidence for a fixed change basis.
- reviewing a fixed-basis HTTP REST contract change across authority, normalized
  OpenAPI, backend conformance, generated client, consumer, and CI.

## Nearest Skill Boundaries

| Request | Owner |
| --- | --- |
| Map directories, architecture, commands, conventions, and reuse entries | `repo-map` |
| Review any local or immutable repository change basis | `repo-review` |
| Define unresolved product behavior or API business intent | `product-spec` |
| Review security-sensitive changes on a fixed change basis | `repo-review`, routing to `codex-security:security-diff-scan` when available |
| Scan the complete repository tree at a fixed SHA | `repo-review`, safely materializing the snapshot and routing it to `codex-security:security-scan` |
| Scan a repository or current-source path with no diff basis | `codex-security:security-scan` |
| Diagnose a concrete failure | Host diagnosis under effective instructions |
| Apply accepted fixes | matching `dev-*` |
| Stage, commit, push, squash, or clean branches | `repo-delivery` |

## Examples

### Worktree

`Review all local changes, preserve unrelated edits, split semantic commits, and give exact staging guidance.`

Inventory status/index evidence, classify ownership and mixed hunks, inspect complete candidate diffs, and do not mutate Git.

### Commit range

`Review 23d30ccd..d1c5f0d8 independently and return P0-P3 findings.`

Resolve both endpoints to immutable SHAs before conclusions.

### Pull request normalized to fixed range

`Review PR 42 without posting comments.`

Verify complete PR evidence, resolve base/head SHAs, and review that fixed range; comment posting remains unauthorized.

### Conditional Release profile

`Review this release candidate for migrations, packaging, CI, rollback, and security configuration.`

Add this profile to a fixed candidate revision only when release readiness was requested; report merge/release implications and `Not verified` runtime/CI gaps.

### Repo-map navigation

A `repo-map` artifact may identify owners and shortest reading paths. Independently verify finding facts at the selected basis. If a mapped path is stale, search from the nearest existing ancestor and route document repair to `repo-map`.

### Protocol contract

`Review this fixed range for OpenAPI compatibility and generated-client drift.`

Fix the Git basis, authority type, generator version/command, baseline normalized
OpenAPI, and candidate clean generation before findings. Static checks do not prove
backend runtime conformance, consumer states, or clean CI.

## Output

All modes report basis, scope, findings, evidence, validation, exclusions, and gaps.
Worktree findings-only records full status but reports bounded findings without
commit groups or staging guidance. Worktree commit-readiness additionally reports
complete ownership, mixed hunks, semantic groups, exact staging, and commit messages.
Fixed-basis review adds resolved SHAs. Release implications appear only when the conditional Release profile was selected.

When a direct or coordinated Codex Security workflow is unavailable, report the
workflow name and exact requested scope as `Not verified`; do not substitute an
internal checklist scan.
