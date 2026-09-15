# Task Ledger Contract

Use the repository's established plan format. When none exists, use the smallest
Markdown structure that preserves these fields:

| Field | Required meaning |
| --- | --- |
| ID | Stable identity; corrections keep their parent relationship. |
| Outcome | Observable result produced for the user or next owner. |
| Owner | One capability responsible for the current mutation. |
| Scope | Exact repository, module, artifact, or external surface. |
| Inputs | Accepted contract and basis references consumed. |
| Dependencies | Only results that must finish before this task starts. |
| Acceptance | Falsifiable criteria, including failure and recovery when applicable. |
| Evidence | Required source/static/build/runtime/artifact/deployment layers. |
| Status | Current state derived from dependencies and evidence. |
| Blocker | Named missing condition and the tasks it actually blocks. |
| Next action | One concrete action or owner that advances the task. |

Keep a compact status summary and one ordered Ready frontier. Detailed execution logs
belong in the repository's progress/evidence authority and are referenced rather than
copied into every task.

## Decision Frontier

Resolve ledger facts from accepted contracts, current evidence, and the existing task
authority before questioning the user. Connect only unresolved choices that can change
task boundaries, owner, dependency order, acceptance evidence, blocker scope, or the
Ready frontier. A product, UI, architecture, implementation, review, or delivery
decision stays with that owner: record it as a scoped blocker and next action instead
of deciding it inside `to-task`.

For a ledger-owned choice, ask only a current-frontier question whose prerequisites
are settled. When two or three meaningful mutually exclusive outcomes exist, prefer
the current host mode's native structured-choice affordance; put the recommendation
first and state the task/evidence consequence. If that affordance is unavailable,
identify the limitation at its actual scope and use concise numbered options; do not
claim that the client as a whole lacks the capability or that this Skill created a
native control. Record the selected outcome and basis, recompute affected dependencies
and statuses, and never mark a dependent task Ready while its material owner decision
remains unresolved. A selection does not authorize implementation, Git mutation,
external action, or continuous execution.

## Task Slicing

- Prefer a narrow, independently demonstrable outcome that includes its matching
  owner-level implementation and verification instead of horizontal batches such as
  "all UI", "all services", or "all tests". When different mutation owners are
  required, use explicit dependencies and make the smallest owner-complete task the
  Ready unit.
- Keep each task within one fresh execution context and one mutation owner. A task may
  cross technical layers owned by that capability, but it must not hide a Product,
  UI, architecture, review, delivery, or external-operation decision.
- Treat a wide mechanical refactor as an exception when no narrow migration batch can
  remain valid independently. Model it as **expand–contract**: add the compatible new
  form, migrate consumers in bounded batches that preserve the declared green gate,
  then remove the old form only after every migration dependency is complete.
- When a migration batch cannot stay green alone, record the shared integration basis
  and block final integration/verification on every batch. Do not call a horizontal
  outage window a vertical slice.

## Separated Ledger Authorities

Identify ledger roles by meaning, never by file name. A project may keep them in one
file or split them across several:

| Role | Owns | Write rule |
| --- | --- | --- |
| Definition authority | stable task definitions, dependencies, acceptance, and exit conditions | read-only during reconciliation; changes follow the owning contract |
| Active ledger | status, Owner, blockers, Ready frontier, and next action | the primary write authority of every ordinary reconciliation |
| Archive | confirmed-complete tasks that can be reopened | written only by an authorized archive or reopen transaction |
| Evidence log | execution evidence and checkpoints | appended or referenced per the project's convention; never rewritten |

- Never create a second ledger that competes with the project's existing one.
- An ordinary reconciliation modifies only the active ledger.
- Archiving or reopening a task atomically updates the active ledger and the archive
  together, and only when the project contract explicitly authorizes that transition.
- Status reconciliation never rewrites static definitions or historical evidence.

## Continuous Workflow Boundary

`to-task` performs one bounded ledger transaction: read current authorities and basis,
reconcile changed inputs and evidence, derive statuses and the Ready frontier, write the
existing ledger atomically, and read it back. It does not run the selected task or own a
timer, daemon, idle scheduler, model session, retry loop, or process lifetime.

The target repository's `AGENTS.md`, start-task contract, or harness owns continuation:
select one Ready item, invoke its implementation or verification owner, collect the
actual result, then invoke `to-task` again to update evidence and state. A host that
cannot continue automatically still leaves a complete `next_action` for another model
or session.
