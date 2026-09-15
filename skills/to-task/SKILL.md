---
name: to-task
description: "Use when accepted product, UI, architecture, or review inputs must become or reconcile with a durable project task ledger; not for specification, implementation, review, delivery, or scheduling."
---

# To Task

## Entry Gate

Own durable task-ledger decomposition and reconciliation. Require an accepted outcome,
named ledger authority, and current evidence/basis. Keep Product, UI, DESIGN,
architecture, source, verification, review, and delivery as separate owners.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Create or reconcile a ledger from accepted contracts/findings | [task ledger](references/task-ledger.md) | Current tasks, dependencies, evidence gates, and Ready frontier |
| Need schema, status, or reconciliation rules | [task ledger](references/task-ledger.md) | Correct ledger transition |

## Invariants

- Create tasks only for confirmed outcomes; unresolved decisions remain with their native owner.
- Derive status from criterion-specific evidence. Build, report, or command success never upgrades a higher runtime/deployment layer.
- Preserve valid completed work; reopen only the affected task and downstream dependents on basis drift or findings.
- Do not implement, operate clients, review mutable output, mutate Git, or claim continuous execution.

## Output Map

Return `task.ledger.maintain` with authority, basis, scope, task/status counts,
dependency frontier, changed tasks, first Ready task, blockers, gaps, and validation.

## Reference Map

- Read [task ledger](references/task-ledger.md) for ledger schema, status, reconciliation, and stop rules.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
