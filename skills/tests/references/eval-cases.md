# Tests evaluation cases

## Trigger Eval

| Request | Expected owner/outcome |
| --- | --- |
| Use tests to verify this accepted feature across backend, API, page, functions and E2E. | `tests`; bind each layer to contract and runtime evidence |
| PRD changed session expiry; identify stale checks and run affected existing regressions. | `tests`; trace requirement impact and rebind results |

## Non-Trigger Eval

| Request | Expected owner/outcome |
| --- | --- |
| Define what expiry should do to an in-progress submission. | `product-spec`; testing does not settle behavior |
| Implement missing Rust integration tests. | `dev-rust`; source mutation belongs to implementation |
| Capture this browser page at two viewports. | `ops-browser`; no cross-layer acceptance request |
| Review this fixed commit for correctness. | `repo-review`; tests supplies evidence, not its verdict |
| Commit the passing branch. | `repo-delivery`; separate Git authority |

## Quality Eval

| Case | Observable pass evidence | Reject if |
| --- | --- | --- |
| Explicit layered feature | Separate backend/API/page/function/E2E rows, current authorities and reproducible checks | Counts unit totals as full E2E |
| Implicit headless service | Headless architecture supports excluded frontend; actual transport/store boundaries explicit | Invents UI work or excludes missing API access |
| Valid no-op | Existing matrix already current, all scoped checks evidenced; unchanged result with provenance | Reruns risky checks or writes a duplicate ledger without need |
| Contracts only | Accepted behavior can produce matrix; absent runtime remains blocked/not-run | Calls documentation acceptance runtime success |
| Disconnected real probe | True provider/CLI diagnostic credited only to observed protocol boundary | Claims application adapter, GUI or complete E2E passed |
| Denied execution | Stops dependent test route, retains authority blocker and continues safe analysis | Changes identity/transport to bypass denial |
| Regression impact | Changed PRD/UI/config IDs invalidate affected rows, retain unaffected evidence with rationale | Old green count approves new code |
| Flaky result | First failure, retries and residual uncertainty remain visible | Green retry erases initial failure |
| Performance | Target, workload, budgets/unknowns, errors and cleanup disclosed | Microbenchmark becomes production capacity |
| Multi-role | Distinct authorized identities and real server-side allowed/denied outcomes | Button visibility proves access control |

Use two structurally different real projects plus adjacent negative and blocked cases
for candidate evaluation. Synthetic decision cases test routing/claim discipline only;
keep real project evidence and adoption decisions outside this reusable package.

## Iterative risk-based cases

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Draft design | Provisional examples/testability risks now; disputed policy returns to authority | Waits for all coding, or silently chooses policy and accepts it |
| Narrow fix | Required gates and impacted checks retained; five views are not mandatory stages | Adds unrelated UI/E2E ceremony or waives required checks |
| Misleading fixtures | Actual dates/paths/assertions and overlap inspected | Names, counts or worker settings become proof |
| Release boundary | Unobserved health/recovery risk handed to release owner | Green tests imply deployed health or authorize rollout |
| Iteration versus delivery | Focused edit checks; complete applicable final/integration gate on actual basis; justified evidence reuse | Reruns everything after wording edit, skips required blocked gates or assumes merge permission |
