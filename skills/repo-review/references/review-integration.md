# Review Integration

Load this reference only when the fixed review basis includes completed external-review
evidence or an explicitly persisted post-terminal retention instruction. Ordinary local
review does not need this context.

## External Review Evidence

Keep authorized external-review status separate from the local verdict. Integrate only a
completed, attributable result whose provider evidence matches the selected basis. A
pending, timed-out, empty, or unattributed response neither creates nor clears a finding.
Verify accepted findings against local evidence before including them.

Grade the provider's execution containment and record it beside the integrated result:
`sandbox-isolated` only when the reviewer demonstrably ran inside a verified
task-isolation profile, and `prompt-constrained` when the read-only boundary was the
prompt alone, including runs launched with permission-skipping flags. A
prompt-constrained result is still usable after local verification but carries the lower
grade and never counts as isolation proof; unchanged end-state Git equality does not
upgrade the grade. Record unknown containment as `prompt-constrained`.

## Final Result Sync

Freeze the local verdict before any post-terminal action. An explicitly persisted
`ask-ai` `final-result-sync` receives only the sanitized frozen result. Its receipt or
failure is retention evidence, not a review axis, and cannot add, clear, reprioritize, or
otherwise change findings or verdicts. Without a valid persisted instruction, do not send
or prepare an external retention payload.
