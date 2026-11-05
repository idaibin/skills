# Test result contract

`urn:skills:test-request:v1` and `urn:skills:test-result:v1` are portable contract names,
not claims of an installed validator or runtime. Use the project's existing report
format with these semantic fields rather than requiring a second database or ledger.

## Input

- Repository and immutable revision or Worktree patch digest; selected feature/change/journey.
- Applicable product, UI and API sources with versions, acceptance status and IDs;
  or current source/runtime evidence and labeled assumptions for existing-project
  regression/exploration. A complete PRD is not a required input.
- Requested test layers, relevant environments/roles and execution scope/permissions.
- Existing project commands, fixtures, evidence sources, budgets and exclusions.

Missing input blocks only dependent rows; preserve feasible independent checks.

## Result

- Basis: repository/revision/patch, contract versions, runtime/build/configuration identity.
- Coverage rows: requirement/risk ID, layer, scenario, role, real/stubbed boundary, oracle,
  fixture/source, command or recipe, run identity, state and supporting evidence. Keep
  separate rows for differently verified boundaries within the same layer. Maintain one
  current state per case and boundary; link historical attempts without presenting
  them as competing current results.
- Evidence: time, source version/provenance, observed assertions, exit/result, artifact
  path or authorized URL and digest where useful, limitations, cleanup outcome.
- Failures: expected/actual, reproducible steps, first failure and retry history,
  owning boundary and smallest next check or fix.
- Gaps: missing tests/contracts/capabilities, blockers, justified exclusions and impacted
  regression rows, residual risks and provisional decisions; distinguish historical
  evidence from current-basis acceptance.
- Conclusion: which scoped requirements are proven, whether the first real E2E exists
  and exactly where it begins/ends, and which required layers remain open.
- Handoff: bounded input for implementation, operations, `to-task`, fixed-basis review or
  authorized delivery. A target owner name is not proof it ran or permission to run it.

For comparative performance rows include metric/start-end definition, baseline and
candidate identity, raw sample references/count, aggregation/spread, exclusions and
comparability limitations. Return separate conclusions for improvement, accepted
budget, protected journeys and existing/missing regression protection. Keep script
inspection distinct from execution. Link dependency-sensitive assertions to their
revalidation trigger rather than claiming they survive upgrades.

## Oracle basis and pending human decisions

Use existing oracle, evidence and gap notes, not new row states or another ledger.
Label each expectation as a confirmed rule, current-behavior baseline or provisional
inference, with source paths/ref and observations. Report native assertion outcomes
separately from business correctness: `passed` on a baseline means consistency with
that baseline; `passed` on an inference only supports the hypothesis. A mismatch
is evidence to investigate, not automatically a confirmed product defect.

For a conflict or unverifiable business meaning, retain the exact question, competing
interpretations, evidence, affected case IDs and human decision owner. Defer that
business verdict and continue independent cases. Safe exploratory steps need not wait;
unknown permissions or unsafe effects stop the affected operation. Missing full PRD
alone is neither a whole-run blocker nor grounds to exclude cases. A later human
decision updates the affected oracle/tests and triggers scoped reruns while preserving
old evidence. Do not report all business requirements accepted while decisions remain.

## Row states

| State | Meaning |
| --- | --- |
| `passed` | Required assertions observed on the declared basis and boundary; evidence accessible |
| `failed` | An executed assertion contradicted its oracle; retain diagnostic/harness attribution |
| `blocked` | Required prerequisite, environment, authority or permission prevents checking |
| `not-run` | Applicable check has not run on this basis, including stale-only evidence |
| `excluded` | Accepted scope makes the row inapplicable; include authority and rationale |

A bare successful exit, generated report, unit/mock suite, missing tool or docs-only
review cannot promote another row to passed. Keep performance measurements without a
budget distinct from budget acceptance. Overall completion requires all required
applicable rows passed and no unresolved flakes/cleanup gaps affecting the claim;
authorized exclusions remain visible. Testing completion never implies independent
review, merge, deployment or promotion of this Skill itself.
