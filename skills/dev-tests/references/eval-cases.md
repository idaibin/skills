# Dev Tests evaluation cases

## Trigger Eval

| Request | Expected owner/outcome |
| --- | --- |
| Use dev-tests to verify this accepted feature across backend, API, page, functions and E2E. | `dev-tests`; bind each layer to contract and runtime evidence |
| PRD changed session expiry; identify stale checks and run affected existing regressions. | `dev-tests`; trace requirement impact and rebind results |

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
| Resumed campaign | Original case IDs and layers reconciled against usable raw evidence; only affected assertions rerun | Creates continuation cases or repeats every action after an unrelated fixture change |
| Delegated result | Result closes only the assigned execution until its case and layer are reconciled | Agent completion marks the whole campaign passed |
| Flaky result | First failure, retries and residual uncertainty remain visible | Green retry erases initial failure |
| Borrowed dependency pass, independent install failure | Keeps the pass on its borrowed basis; classifies missing harness packages and reruns impacted checks after authorized dependency repair | Treats old passing counts as independent readiness or removes business assertions |
| Performance | Target, workload, budgets/unknowns, errors and cleanup disclosed | Microbenchmark becomes production capacity |
| Multi-role | Distinct authorized identities and real server-side allowed/denied outcomes | Button visibility proves access control |
| Valid screenshot shows a broken in-page image; fixture exists but cannot decode | Keeps asset acceptance open; requests a decode and target-content assertion at the project test or runtime owner | Screenshot validity, fixture presence/hash or green unrelated tests pass the image claim |
| Current-basis valid screenshot and fixture show the intended image | Credits only the image claim and boundary actually asserted | Rejects proven content solely because an unrelated layer remains open |
| HTTP 200 serves an error or login page | Checks semantic page/API outcome and leaves the target journey open | Status code alone becomes product acceptance |
| HTTP 200 serves the required page and state | Credits the asserted route, content and runtime basis within scope | Treats every 200 as failure |
| Screenshot from an older build | Retains it as historical and requires current-basis evidence for the affected claim | Old image is silently reused as current |
| Screenshot bound to unchanged current build/state | Reuses it with explicit basis and impact rationale where project rules allow | Needlessly recaptures unchanged evidence |

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

## Comparative And Recovery Cases

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Two noisy lab samples improve while cache and dataset change | Preserves samples and confounders; improvement inconclusive, field p75 unproven | Picks fastest run or claims RUM attainment |
| Report refresh returns simulated 503; download fails after successful generation | Checks separate retries, old results, duplicate admission and scoped fixture boundary | Calls failures empty data or simulated recovery real-service proof |
| Modal controls load, fail, retry and become busy | Verifies Tab/Shift+Tab, control replacement and close-focus return against UI contract | Screenshot or disabled styling proves keyboard behavior |
| Requested performance capture is unavailable | Blocks dependent measurement; continues independent checks without alternate denied route | Infers timing from screenshots or starts production load |

## Motion Reproduction Evidence

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Old drawer source and candidate face the same close-order and cached-departure assertions | Retains the old failures and candidate results with source identity; states component-harness coverage | Overwrites the live source or calls the fixture a browser/paint pass |
| Motion-off sampling finds zero transition durations but a leaving overlay still intercepts input | Tests the actual affected first frame, geometry and hit target; keeps policy and lifecycle evidence separate | Closes the criterion solely from computed duration counts or unrelated route samples |
