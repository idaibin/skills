# Tests candidate evaluation

## Current basis and scope

Candidate capability: `testing.coverage.verify@0.1.1`, based on
`23cc6b0a30abf15dd86cbb6cd148d13c731cca97`. No stable promotion or installation.
The distinct output is risk-based contract-to-boundary acceptance evidence. Product,
UI/API decisions, source/test implementation, browser/client mechanics, task-ledger
maintenance, fixed-basis review and Git delivery retain their existing owners.

Early provisional examples and testability analysis can inform design before code;
unsettled business policy cannot become an acceptance oracle. Five coverage views are
navigation, not exhaustive quality categories or chronological stages. Applicable
security, accessibility, recovery and compatibility risks may cross any view.
Iteration uses focused checks and necessary regression; final submission/authorized
integration require complete applicable gates on the actual assembled basis. Unchanged
evidence can be reused with an explicit impact rationale where project rules permit;
required blocked gates remain open. Test success never proves deployed health.

## Source cross-check (2026-10-04)

- [ISTQB CTFL 4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf),
  §§1.4.1, 2.1.2–2.1.5, 5.2.3: early analysis/testability and likelihood/impact inform
  iterative test scope. This supports the boundary correction, not wholesale adoption
  of a methodology or every syllabus category.
- [W3C WAI](https://www.w3.org/WAI/test-evaluate/): evaluate accessibility throughout
  design/development; tools alone cannot establish conformance. Applicable checks need
  suitable oracles and human evaluation where required.
- [Google SRE](https://sre.google/workbook/canarying-releases/): release assessment
  requires attributable monitoring evidence. Missing health/recovery evidence is a
  release-owner handoff, not permission to configure monitoring or deploy a canary.

Actual-use feedback supports preserving a pre-run plan identity and checking exercised
fixtures, paths and overlap rather than inferring coverage from names/counts/configuration.
Public cases remain synthetic; project facts and runtime receipts stay project-owned.

## Evidence and limits

- V1/V2: 19-package structural checks and 73 deterministic routing cases pass, with
  zero regressions against the immutable base. Canonical gate passed: 452 unit
  regressions, shared protocol parity, DESIGN.md checks and whitespace; zero context
  warnings. An initial approval-wait cancellation left no terminal result; one
  authorized same-gate retry completed with exit 0.
- V3: Seven initial and four refinement native-agent decision cases met their oracles.
  The refinement reviewer froze responses before reading gold and found no actionable
  P0–P3. Refinement output SHA-256:
  `f38a2d4f31951a3b6feef3ee08aa4ba8aa22c205b4ac44796fca41867e0aa68d`.
  This is supplied-case decision evidence, not CLI JSONL, isolated model benchmarking,
  actual runtime execution by that reviewer, or measured efficiency.
- V4: Two structurally different real projects used the initial candidate before bounded
  execution (production client/external protocol and API/storage/authorization). Another
  project remained a docs-only blocked case. These do not certify complete products.
- V5/V6: Real, fixture, unit, API, UI and E2E results stay separate. Different statuses may
  coexist within one layer. Prior same-layer pass, configured workers, test names,
  missing capability and denied routes cannot raise the evidence level. No quantitative
  quality/time/cost improvement or generalized full-stack completion is claimed.

## Remaining adoption gate

Keep candidate status until representative accepted application journeys, including
real entry-to-outcome E2E, have current-basis evidence and independent adoption review.
Include role/concurrency/performance checks where relevant, with agreed budgets and
permissions. Required blocked UI/runtime checks cannot be waived. Canonical adoption
artifact publication remains a separately scoped governance step; no automatic
publication, deployment, installation or promotion follows from catalog checks.
