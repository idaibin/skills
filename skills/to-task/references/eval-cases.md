# Eval Cases

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `The PRD, UI contract, and architecture are approved. Convert them into tasks, dependencies, acceptance checks, and a resumable status ledger.` | Trigger `to-task`; update the existing task authority and return the first Ready task. | Accepted contracts need decomposition and state. |
| `Plan this shared schema rename. Adding the new field is compatible, but deleting the old field before every frontend and backend consumer migrates would break the build.` | Trigger `to-task`; create an expand task, bounded owner-complete migration batches, and a contract task blocked by every migration, with the declared green gate preserved between batches. | A wide mechanical refactor may need expand–contract rather than fake vertical slices or one unsafe all-at-once task. |
| `This review found two UI regressions. Add them to the current task ledger and reopen only affected work.` | Reconcile affected tasks and recalculate the frontier. | Findings change task state. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Map repository roots, runtime identities, and shared dependencies.` | Route to `repo-map`. | Repository discovery has a separate owner. |
| `Decide what happens when the user rejects this approval.` | Route to `product-spec`. | Product behavior is unresolved. |
| `The UI contract still has two unresolved visual directions; choose one while splitting the work into tasks.` | Route the visual decision to `ui-spec` and keep dependent tasks blocked. | Task decomposition cannot absorb UI authority. |
| `Implement the first Ready React task.` | Route to `dev-frontend`. | Source implementation is outside planning. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Authority reuse | Finds and updates the existing task authority. | Creates a parallel plan or stores project state in the Skill. |
| Vertical slicing | Tasks have observable outcomes, matching verification, and one mutation owner; wide mechanical refactors use expand–contract only when narrow batches cannot remain valid independently. | Splits work into vague horizontal phases, mixes owners, calls an outage window a vertical slice, or uses expand–contract without a demonstrated compatibility need. |
| Readiness | `Ready` requires current inputs and satisfied dependencies. | Marks ambiguous behavior Ready. |
| Decision frontier | Resolves facts first; routes Product/UI/technical decisions to their owners; for a ledger-owned bounded choice asks only the prerequisite-complete frontier through an available native structured control, or names the actual current-mode limitation and uses concise numbered options; records the selection and recomputes statuses. | Decides another owner's contract, asks dependent choices together, ignores an available native control, claims the whole client is unsupported, claims the Skill added the control, or treats the selection as implementation/Git/external authorization. |
| Evidence layering | Acceptance names the evidence layer required by each claim. | Treats build or model output as runtime acceptance. |
| Incremental invalidation | Reopens affected tasks and downstream dependents only. | Resets the complete plan after a local change. |
| Execution boundary | Performs one ledger transaction and returns the Ready frontier without implementing, scheduling, or promising a persistent loop. | Edits source, changes Git, controls a process/session, or claims autonomous continuation. |
| Separated task ledger | Reads task facts from the definition authority and evidence log and writes only the active ledger; statuses, Ready frontier, and next action reflect the recorded evidence. | Rewrites the static plan, mutates the archive or evidence log, or creates a second ledger. |
| Archive reopen | Reopens an archived task only under an explicit project rule, atomically updating the active ledger and the archive while preserving historical evidence and keeping the task active exactly once. | Copies the task into both places as active, drops history, or reopens without authorization. |
