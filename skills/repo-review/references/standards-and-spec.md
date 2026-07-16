# Standards and Spec Review

## Standards Axis

Build the standard set from effective repository/host guidance, contribution and architecture docs, language/framework conventions selected by the changed surface, and enforced tool output. Check correctness, architecture, security, performance, maintainability, compatibility, and structural lifecycle only where evidence makes them applicable.

For each finding, cite the governing source when one exists. Treat general smells as judgment signals, not hard violations; repository rules and demonstrated local conventions win.

## Spec Axis

Locate the originating requirement in this order when available:

1. a user-supplied spec, issue, PRD, or acceptance criteria;
2. issue/requirement references bound to the branch, commits, or review package;
3. a repository spec artifact clearly matching the reviewed change;
4. explicit decisions and acceptance criteria retained in the current task context.

Check:

- required behavior missing or partial;
- implemented behavior that contradicts the requirement;
- acceptance criteria without evidence;
- unrequested behavior or scope creep;
- error, edge, migration, permission, compatibility, or rollback behavior the spec requires;
- docs/tests that claim different behavior from the spec.

If no trustworthy source exists, report `Spec Compliance: Not verified (no spec source)` and continue the Standards axis. Do not reconstruct intent from code and then claim compliance.

## Independence and Integration

Keep evidence collection independent so standards quality cannot hide a requirement miss and requirement coverage cannot excuse unsafe code. Parallel read-only passes are optional, not mandatory. The `repo-review` coordinator verifies both reports, removes duplicates, assigns one P0-P3 severity from concrete impact, and labels each finding with its contributing axis.

## Verdict

Report:

```markdown
## Findings
### P0
### P1
### P2
### P3
## Standards Verdict
## Spec Compliance
## Final Verdict
## Residual Risk and Not Verified
```
