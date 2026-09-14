---
name: to-task
description: "Use when accepted product, UI, architecture, or review inputs must be converted into or reconciled with a durable project task ledger containing dependencies, acceptance checks, evidence requirements, status, blockers, and next action; not for deciding specifications, mapping a repository, executing tasks, reviewing changes, or Git delivery."
---

# To Task

Turn current accepted contracts into the repository's durable task authority. Own task
decomposition, reconciliation, and resumable task-ledger state; preserve Product, UI, DESIGN,
architecture, source, verification, review, and delivery as independent owners.

## Workflow

1. Resolve the repository root, effective guidance, requested outcome, current basis,
   and the existing task authority. Read accepted contracts and the latest relevant
   progress or review evidence. Update an existing plan instead of creating a competing
   ledger.
2. Check input readiness by slice. Create tasks only for confirmed outcomes. Keep a
   missing product decision with its owning contract; represent an external dependency
   or missing evidence as a bounded blocker without inventing the answer.
3. Split work into independently demonstrable vertical slices. Each task records a
   stable ID, outcome, owning capability, mutation scope, accepted input/basis,
   dependencies, acceptance criteria, required evidence layers, status, blocker, and
   next action. Use a dependency edge only when one result truly blocks another.
4. Derive status from evidence: `Todo` is defined but waiting; `Ready` has current
   inputs and satisfied dependencies; `In progress` has one owner; `Partial` lacks some
   acceptance evidence; `Blocked` names the preventing condition; `Closed` has current
   evidence for every criterion. Preserve equivalent repository-specific status names.
5. Bind verification to the claim it proves. Separate source, static checks, build,
   protocol/API, runtime/browser/client, artifact, deployment, and Production evidence
   when applicable. A model report, green build, or successful command cannot close a
   higher evidence layer by itself.
6. Reconcile changes incrementally. New Product/UI input, basis drift, or review
   findings reopen only affected tasks and downstream dependents. Prefer the project's
   existing correction convention such as `FIX-nn`, `UI-Rn`, or a child task. Preserve
   valid completed work and recalculate counts and `next_action`.
7. Write the accepted plan or ledger to the repository's existing authority. If no
   durable location is authorized, emit a task-local handoff under the verified ignored
   workspace. Re-read it and return the first Ready task or exact blocker frontier.

## Boundaries

- Do not decide unresolved product behavior, visual direction, or technical contracts.
  Route those facts to their native owner before marking the dependent task Ready.
- Use `repo-map` only for a separately needed repository asset or impact query.
- Do not implement source, operate browser/client state, review a mutable result, change
  Git, schedule work, or claim continuous background execution. Return the Ready
  frontier; the project workflow or host controls execution and calls this Skill again
  after requirements, findings, evidence, or task state changes.
- The ledger records project state. Forgeway may coordinate task planning and retain
  Run/Gate references, but does not replace or duplicate the ledger.

## Output

Return capability `task.ledger.maintain` with the ledger authority, basis, included scope,
task/status counts, dependency frontier, changed tasks, first Ready task, blockers,
evidence gaps, and validation performed. See [task ledger](references/task-ledger.md)
and [eval cases](references/eval-cases.md).
