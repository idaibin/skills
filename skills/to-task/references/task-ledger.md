# Task Ledger Contract

## Contents

- [Current Authority And Evidence](#current-authority-and-evidence)
- [Decision Frontier](#decision-frontier)
- [Task Slicing](#task-slicing)
- [Outcome and Retry Continuity](#outcome-and-retry-continuity)
- [Separated Ledger Authorities](#separated-ledger-authorities)
- [Continuous Workflow Boundary](#continuous-workflow-boundary)

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

## Current Authority And Evidence

Separate the current task state from retained history. For a directive that changes
readiness or a blocker, record its source reference, authority, original order/time,
task/repository/action scope, and any directive it supersedes. Put this provenance in
the existing Inputs, Blocker, or evidence notes; do not create a competing ledger or
rewrite the original evidence. A copied plan, summary, timer request, or provider
response is evidence of its source, not a new user instruction.

Apply the host's instruction priority before recency. A valid newer instruction from
an authority competent to change the restriction supersedes the older instruction
only within their overlapping scope and effects. Thus a direct authorization for the
same task may replace its earlier handoff-only limit without another approval; an
unrelated authorization leaves a page-write cancellation effective. Record partial
replacement explicitly and retain every unaffected restriction. If source, order,
or scope is unresolved, block only the disputed action and name the missing fact.

Before writing, identify each requested change and confirm its accepted outcome,
authoritative contract, and ledger write authority. For a change missing any of these,
leave its existing task state untouched and report the gap to the requester; do not add
or edit its blocker, next action, or status merely to document the stop. A read-only
inspection may establish the gap, but grants no write authority.

Reconcile a separate authorized change only when its status, dependencies, and Ready
effect can be derived without the missing input. Preserve the stopped task's original
row and derive the shared Ready frontier only from accepted facts. If no authorized
change remains, or the changes cannot be separated without deciding the missing
contract or altering the stopped task, leave the entire ledger byte-for-byte unchanged.

A latest effective pause or cancellation keeps its scope non-executable until a
valid later instruction expressly resumes that scope. Resuming one remediation item
does not resume other items, projects, or old automation. Neither an older execution
plan nor its later summary or scheduled replay can reactivate paused work. A current
host-policy refusal is a separate constraint: retain its exact action and reason;
rewriting a request, switching tools/owners, or opening a fresh session cannot clear
it. Resume that action only when the governing authority actually changes the
applicable policy or establishes that the refusal no longer applies.

Date observations and bind them to their target, basis, and evidence layer. A historic
capture failure proves that attempt failed; it does not prove the current client is
offline, locked, or incapable. Recheck current facts only through permitted read-only
observations, and leave unavailable current evidence unknown or `Not verified`.
Preserve an unresolved applicable refusal rather than treating it as an obsolete
technical failure. Report active blockers separately from superseded instructions
and historical failures, with a concrete resume condition for each active blocker.

Keep completed criteria closed unless new relevant evidence or an accepted basis
change invalidates those criteria. Link a reopen to that criterion and change;
recompute only dependencies whose prerequisites or acceptance are affected. An
unrelated change, new session, or permission to do different work is not grounds to
reopen a completed item.

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

## Outcome and Retry Continuity

Keep each fix tied to its original feature and acceptance ID across renamed slices,
owners, and alternative routes. Preserve the first failure and what changed the
hypothesis; passing a child check does not make the parent feature runtime-accepted.
When no authorized task is executable, return the pending decision or runtime queue
with exact resume conditions instead of inventing cleanup work to keep activity going.

## Separated Ledger Authorities

Identify ledger roles by meaning, never by file name. A project may keep them in one
file or split them across several:

| Role | Owns | Write rule |
| --- | --- | --- |
| Definition authority | stable task definitions, dependencies, acceptance, and exit conditions | read-only during reconciliation; changes follow the owning contract |
| Active ledger | status, Owner, blockers, Ready frontier, and next action | the primary write authority of an authorized ordinary reconciliation |
| Archive | confirmed-complete tasks that can be reopened | written only by an authorized archive or reopen transaction |
| Evidence log | execution evidence and checkpoints | appended or referenced per the project's convention; never rewritten |

- Never create a second ledger that competes with the project's existing one.
- An ordinary reconciliation modifies only the active ledger.
- Archiving or reopening a task atomically updates the active ledger and the archive
  together, and only when the project contract explicitly authorizes that transition.
- Status reconciliation never rewrites static definitions or historical evidence.

## Continuous Workflow Boundary

`to-task` performs one bounded ledger transaction for separable authorized changes:
read current authorities and basis, reconcile changed inputs and evidence, derive
statuses and the Ready frontier, write the existing ledger atomically, and read it back.
It reports stopped changes outside the ledger and performs no transaction when none
remain safely authorized. It does not run
the selected task or own a timer, daemon, idle scheduler, model session, retry loop,
or process lifetime.

The target repository's `AGENTS.md`, start-task contract, or harness owns continuation:
select one Ready item, invoke its implementation or verification owner, collect the
actual result, then invoke `to-task` again to update evidence and state. A host that
cannot continue automatically still leaves a complete `next_action` for another model
or session.
