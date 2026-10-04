# Unified tests candidate evaluation

## Fixed basis and decision

Base: `129f89b3c8d1ed0a76c172f2209b427ac72a7a35` on the non-main review branch.
The added `tests` package and its catalog integration are a **candidate**, not stable.
Portable capability version is `testing.coverage.verify@0.1.0`.

The existing owners already validate their own implementation, contract or operation.
The distinct reusable output here is a contract-to-layer acceptance matrix that can
consume those results without replacing their authority. Source/test implementation,
Product/UI/API decisions, browser/client mechanics, task-ledger maintenance, fixed-basis
review and Git delivery retain their current owners. No automatic Skill invocation is
claimed. The package adds no runtime scripts, schemas or tool installation.

## Evidence levels

- V1 Package: Verified by package/link/metadata validator for 19 packages.
- V2 Routing: Verified by 72 deterministic cases, zero regressions against the frozen
  base's published baseline. This is catalog consistency, not model selection proof.
- V3 Behavior: Seven blind native-agent decision cases met their oracles. Inputs were
  supplied separately from expected results; the evaluator froze its responses before
  reading gold. No application runtime or source mutation was involved.
- V4 Project: Two real-project owners applied the candidate to already completed
  runtime receipts. One classified an isolated external-CLI protocol diagnostic; the
  other classified a real service/SQLite/HTTP slice. Both retained unrun application/UI
  and whole-product E2E layers. A documentation-only project supplied a blocked case.
  These are evidence-consumption pilots, not Skill-directed full-stack execution.
- V5 Claim floor: The matrix kept fixture, unit, external protocol, real API, UI and
  full E2E evidence distinct. Denied execution stayed blocked; headless frontend
  exclusion required an accepted architecture scope. Runtime installation, production,
  whole-project completion and stable promotion remain Not verified.
- V6 Generalization: The different slices exposed a useful clarification: one layer may
  have several boundary-specific rows with different states. That clarification was
  added without moving project state or facts into the portable package. Comparative
  quality, cost, time or token improvements were not measured.

## Synthetic decision cases

The public inputs and authoring oracles are in `evals/tests-cases.json`.

| Case | Observed bounded decision |
| --- | --- |
| Explicit full flow | Unit/handler proof stays scoped; screenshot needs provenance; API/function/E2E remain unrun |
| Implicit headless service | Frontend excluded by accepted architecture; real HTTP/store/readback proves only that service journey |
| Nearest implementation | Missing Rust test source belongs to dev-rust |
| Valid no-op | Reconcile current receipts without duplicate ledger or unnecessary reruns |
| Denied runtime | Block dependent execution, no alternate identity/route and no false exclusion |
| Real external probe | CLI protocol proof cannot become application-adapter or frontend E2E proof |
| Contract drift/performance | Revalidate affected PRD/UI rows; no budget acceptance or server authorization from weak substitutes |

The evaluator is a native independent agent; model identity was not independently
attested. This is not a CLI JSONL trace, independently isolated invocation per case,
real-browser test, external-model comparison, or measured efficiency result.

## Validation and review

Canonical `bash scripts/check-skills.sh` passed with immutable `SKILLS_BASE_SHA`
set to the base above: 19 packages, 72/72 routing, 452 unit regressions, shared
protocol parity, DESIGN.md contract regressions and whitespace; zero context warnings.
The first run exposed missing new-package catalog fixtures, baseline entries and a
stale digest, plus an unwritable default npm cache. A later execution lacked terminal
completion evidence after an approval-wait cancellation. After confirming no owned
run remained and receiving authorization evidence, one same-gate retry completed
with exit 0 using writable task caches. No product-runtime result follows from this.

Independent decision/review output SHA-256:
`5d86142def0784ab288835cb76e52f768054a5bc51f5cb7b26e2c5d6087e4e59`.
The initial package review found no actionable P0–P3 issue; final catalog-delta review
is required on the delivered basis. Raw responses/read records stay task-local.

## Remaining adoption gate

Retain candidate status until representative projects actually use this workflow to
select and execute their authorized existing checks, including a first real accepted
end-to-end journey at the declared application boundary. Capture fixed source/contract
versions, fixtures, cleanup and failures, include multi-role/performance cases where
applicable, and obtain independent fixed-basis review or an explicit adoption decision.
Missing authority or platform permission cannot be waived to complete the evaluation.
The full product pipelines remain project-owned open work; this package does not certify
them merely because its own catalog and decision checks pass.
