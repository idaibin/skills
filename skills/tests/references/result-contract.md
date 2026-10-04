# Test result contract

`urn:skills:test-request:v1` and `urn:skills:test-result:v1` are portable contract names,
not claims of an installed validator or runtime. Use the project's existing report
format with these semantic fields rather than requiring a second database or ledger.

## Input

- Repository and immutable revision or Worktree patch digest; selected feature/change/journey.
- Accepted product, UI and API sources with versions and acceptance IDs.
- Requested test layers, relevant environments/roles and execution scope/permissions.
- Existing project commands, fixtures, evidence sources, budgets and exclusions.

Missing input blocks only dependent rows; preserve feasible independent checks.

## Result

- Basis: repository/revision/patch, contract versions, runtime/build/configuration identity.
- Coverage rows: requirement ID, layer, scenario, role, real/stubbed boundary, oracle,
  fixture/source, command or recipe, run identity, state and supporting evidence. Keep
  separate rows for differently verified boundaries within the same layer.
- Evidence: time, source version/provenance, observed assertions, exit/result, artifact
  path or authorized URL and digest where useful, limitations, cleanup outcome.
- Failures: expected/actual, reproducible steps, first failure and retry history,
  owning boundary and smallest next check or fix.
- Gaps: missing tests/contracts/capabilities, blockers, justified exclusions and impacted
  regression rows; distinguish historical evidence from current-basis acceptance.
- Conclusion: which scoped requirements are proven, whether the first real E2E exists
  and exactly where it begins/ends, and which required layers remain open.
- Handoff: bounded input for implementation, operations, `to-task`, fixed-basis review or
  authorized delivery. A target owner name is not proof it ran or permission to run it.

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
