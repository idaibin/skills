---
name: tests
description: "Plan and verify layered test coverage from accepted PRD/UI contracts through backend, API, frontend and end-to-end evidence. Run existing scoped tests; route missing test implementation to its code owner."
---

# Tests

## Entry Gate

Own a bounded test-coverage and evidence decision for a declared feature, change, or
journey. Resolve the accepted product/UI/API authorities, target revision, environment,
requested layers, and execution permission before selecting checks. An existing
project test plan remains authoritative; reuse its IDs and evidence locations.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Plan coverage or reconcile existing results against contracts | [coverage](references/coverage.md) | Requirement-to-layer matrix and qualified gaps |
| Run existing checks, rerun failures, or choose regression scope | [execution](references/execution.md) | Reproducible scoped runs and evidence-bound outcomes |
| Role isolation, concurrent users, load or performance applies | [roles and performance](references/roles-and-performance.md) | Authorized scenarios, budgets and bounded measurements |
| Compose a result for review or another owner | [result contract](references/result-contract.md) | Versioned basis, coverage, evidence and handoff |

## Invariants

- Product behavior belongs to `product-spec`, visual behavior to `ui-spec`, and wire
  semantics to `api-spec`. Test ambiguity cannot silently decide those contracts.
- Select and run existing project tests within scope. Missing tests, harness changes,
  fixtures requiring source edits, and fixes belong to the matching implementation
  owner. Browser/client mechanics belong to `ops-browser`/`ops-client`; these names are
  handoff targets, not automatic invocation or granted capabilities.
- Read current project commands and their effects before execution. Use isolated test
  state and authorized resources; preserve safety stops, denied routes and scope limits.
  A failure does not authorize another identity, mechanism, or environment to bypass them.
- Preserve `passed`, `failed`, `blocked`, `not-run`, and `excluded` separately. A mock,
  fixture, static check or lower layer proves only its observed boundary, never a real
  integration or complete E2E. Missing access is a blocker, not an exclusion.
- Rebind evidence after requirement, UI, code, configuration or environment changes.
  Reuse unaffected evidence only with an explicit impact rationale; old green results
  cannot approve a new basis by default.
- Produce test evidence, not a competing task ledger or a release verdict. `to-task`
  owns durable work reconciliation, `repo-review` the fixed-basis review, and
  `repo-delivery` separately authorized Git actions. No deployment, installation,
  publication, production load, or implicit promotion follows from testing.

## Output Map

Return the [result contract](references/result-contract.md): frozen basis and authority
versions, layer matrix, executed checks and evidence, failures and blockers, justified
exclusions, remaining acceptance gaps and smallest owner-specific next action. State
whether a first real E2E was observed and its exact boundary. Never flatten the matrix
into “all tests passed” when required cells remain unresolved.

## Reference Map

- Read [coverage](references/coverage.md) when deriving or reconciling the acceptance matrix.
- Read [execution](references/execution.md) before running checks or making regression claims.
- Read [roles and performance](references/roles-and-performance.md) only for relevant multi-user, authorization or performance requirements.
- Read [result contract](references/result-contract.md) when consuming results or returning evidence.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary execution.
