# Eval Cases

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `The PRD, UI contract, and architecture are approved. Convert them into tasks, dependencies, acceptance checks, and a resumable status ledger.` | Trigger `to-task`; update the existing task authority and return the first Ready task. | Accepted contracts need decomposition and state. |
| `This review found two UI regressions. Add them to the current task ledger and reopen only affected work.` | Reconcile affected tasks and recalculate the frontier. | Findings change task state. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Map repository roots, runtime identities, and shared dependencies.` | Route to `repo-map`. | Repository discovery has a separate owner. |
| `Decide what happens when the user rejects this approval.` | Route to `product-spec`. | Product behavior is unresolved. |
| `Implement the first Ready React task.` | Route to `dev-frontend`. | Source implementation is outside planning. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Authority reuse | Finds and updates the existing task authority. | Creates a parallel plan or stores project state in the Skill. |
| Vertical slicing | Tasks have observable outcomes and one mutation owner. | Splits work into vague phases or mixes owners. |
| Readiness | `Ready` requires current inputs and satisfied dependencies. | Marks ambiguous behavior Ready. |
| Evidence layering | Acceptance names the evidence layer required by each claim. | Treats build or model output as runtime acceptance. |
| Incremental invalidation | Reopens affected tasks and downstream dependents only. | Resets the complete plan after a local change. |
| Execution boundary | Performs one ledger transaction and returns the Ready frontier without implementing, scheduling, or promising a persistent loop. | Edits source, changes Git, controls a process/session, or claims autonomous continuation. |
| Separated task ledger | Reads task facts from the definition authority and evidence log and writes only the active ledger; statuses, Ready frontier, and next action reflect the recorded evidence. | Rewrites the static plan, mutates the archive or evidence log, or creates a second ledger. |
| Archive reopen | Reopens an archived task only under an explicit project rule, atomically updating the active ledger and the archive while preserving historical evidence and keeping the task active exactly once. | Copies the task into both places as active, drops history, or reopens without authorization. |
