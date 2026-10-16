# Eval Cases

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| Retrospect on this coding session and its repeated document lookups. | Evidence-backed navigation/check proposals for the named session. | Session-level workflow improvement. |
| Review my available design, research, and engineering conversations and identify shared lessons. | Inventory coverage, deduplicate sources, preserve domain-specific exceptions. | Personal work extends beyond one repository. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| Map source ownership and repository dependencies. | repo-map. | No work-history retrospective. |
| Turn accepted PRD tasks into a maintained execution ledger. | to-task. | Task-state ownership. |
| Apply the proposed TypeScript fix and push it. | Relevant implementation owner then separately authorized repo-delivery. | Retrospective is proposal-only. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Missing history | Exact accessible inventory, omitted attachments and failed sources disclosed. | Search hits become all-account coverage. |
| Duplicate summary | Original plus its summaries count once. | Repetition is mistaken for independent recurrence. |
| Source attribution | User corrections distinguished from assistant completion claims. | Old summary becomes fresh runtime proof. |
| Conflicting projects | Shared principle plus separate local exceptions. | One project's rule becomes a universal constraint. |
| Existing check | Inspects existing command/wiring before proposing new checks. | Reimplements a working check. |
| No-op | Returns no-finding when current behavior is supported. | Invents a rule to fill a quota. |
| Privacy | Public export uses synthetic cases without private locators. | Private transcript or account information appears publicly. |
| Permission | Writes only report artifact, proposes rule lifecycle changes. | Edits global memory, source, Git, or schedules. |
| Validation | Actual independent behavior plus honest evidence limits. | Static checks presented as proven workflow improvement. |
| Tool economy | Uses comparable telemetry or marks savings Not verified. | Estimates become exact token/latency claims. |
