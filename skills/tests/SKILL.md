---
name: tests
description: "Plan and execute end-to-end acceptance across APIs, pages, UI walkthroughs, clicks, system functions, and business logic; use for functional testing and regression, not source-only review or implementation."
---

# Tests

## Entry Gate

Own an evidence-bound test run against accepted behavior: scope, cases, execution,
defects, affected-state retest, and cleanup. Resolve the exact checkout/runtime,
Product/UI/API authorities, account/role, data source, and allowed effects before
executing. A session link is reference evidence, not permission to operate that
session or inherit its mutations. Preserve unrelated work and other tasks' services.
Live acceptance requires a reachable identified runtime and an authorized browser or
API runner; unavailable layers remain `Not verified`.

Use the existing test plan and case IDs when present. When asked to apply this skill,
execute the reachable authorized cases; a checklist alone is not the result.

## Route Map

| Condition | Read | Outcome |
| --- | --- | --- |
| Any functional test run | [execution workflow](references/workflow.md) | Frozen scope, cases, actual results and exit decision |
| API or data behavior participates | [API and logic](references/api-and-logic.md) | Wire, business-status, state and persistence assertions |
| Pages, UI or clicks participate | [page walkthrough](references/page-walkthrough.md) | Reachability, real interaction, visual and browser evidence |
| Writing a plan, result or defect | [test record](references/test-record.md) | Reviewable cases, coverage denominator and recovery queue |
| Source-only fixed-change review | Route to the available review owner | Review rather than runtime acceptance |
| A defect needs implementation | Hand its reproduction and expected contract to the implementation owner | Fix only within existing authorization, then retest here |

Browser/client adapters perform low-level operations. This skill owns case selection,
assertions, cross-layer correlation and the final acceptance verdict. Missing optional
adapters do not require installation when the host already exposes an equivalent tool.

## Invariants

- Every pass binds an expected result to current observed evidence at the same basis.
  Source, unit tests, Mock, real API, browser, files and deployment are separate layers.
- Use documented existing runtime addresses and commands. Follow project limits on
  builds and service control; never start, restart or substitute a service merely to
  make a test pass when that action is outside the request.
- Plan writes before executing them: environment, disposable records, side effects,
  authorization and cleanup. Scope uncertain actions to read-only cases; requests to
  test do not grant permission to notify users, change credentials or destroy data.
- Keep product rules authoritative. Do not weaken assertions, alter contracts or
  change shared fixtures to match a failing implementation. Record conflicts precisely.
- Complete a business journey before moving on: entry, action, request, rendered
  outcome, independent readback where required, and cleanup. Neither a click call,
  HTTP 200 nor a success toast alone establishes that outcome.
- Count failures and missing evidence. Use PASS, FAIL, BLOCKED, NOT RUN and N/A per
  case; missing required proof is `Not verified`, never a pass or an exclusion.
- Do not repeatedly retry an unchanged failing hypothesis. After two failures for
  the same cause retain both outcomes and use diagnostic evidence for a new route.
  Stop only dependent operations and continue independently executable cases.

## Output Map

Return scope/basis and environment; case results with claim-matched evidence;
defects with owner, impact and reproduction; scoped coverage and remaining gaps;
cleanup results; and the exact next action or recovery condition. Report sampled
coverage as a sample, never as whole-system acceptance. Keep project evidence in its
authorized local evidence location, not inside this reusable package.

## Reference Map

- [Workflow](references/workflow.md): all test executions and resumed runs.
- [API and logic](references/api-and-logic.md): network/data/state transitions.
- [Page walkthrough](references/page-walkthrough.md): UI, clicks, visual or browser checks.
- [Test record](references/test-record.md): plan, cases, defects and final reporting.
- Maintainers only: read [eval cases](references/eval-cases.md) when validating this
  skill; do not load it during ordinary runtime.
