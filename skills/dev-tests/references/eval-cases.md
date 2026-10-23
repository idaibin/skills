# Dev Tests evaluation cases

## Contents

- [Product Copy Preservation Cases](#product-copy-preservation-cases)

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Quality Eval](#quality-eval)
- [Iterative risk-based cases](#iterative-risk-based-cases)
- [Comparative And Recovery Cases](#comparative-and-recovery-cases)
- [Motion Reproduction Evidence](#motion-reproduction-evidence)
- [Functional Trigger Cases](#functional-trigger-cases)
- [Functional Non-Trigger Cases](#functional-non-trigger-cases)
- [Functional Quality Cases](#functional-quality-cases)
- [Reported incident and contaminated evidence](#reported-incident-and-contaminated-evidence)

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

Synthetic decision cases test routing and claim discipline only; actual application
acceptance requires the scoped real journeys and their evidence. Keep project evidence
outside this reusable package.

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

## Functional Trigger Cases

| User prompt | Expected result | Why |
| --- | --- | --- |
| Use dev-tests to verify accepted performance and protected recovery/keyboard outcomes | Bind comparable metrics and observable assertions to the existing case inventory | Scoped runtime acceptance, not early design or source implementation |
| Use $dev-tests to exercise the existing test deployment from API through page clicks and refreshed business results. | Execute bounded journeys, correlate evidence and return coverage/cleanup. | Explicit functional acceptance. |
| Walk the application end to end: UI, system functions, permissions, filters and logic. | Select tests, resolve finite inventory, run authorized cases. | Contextual functional acceptance. |

## Functional Non-Trigger Cases

| User prompt | Expected result | Why |
| --- | --- | --- |
| Review this fixed commit for correctness, without running the application. | repo-review. | Source review is a separate outcome. |
| Implement the confirmed search debounce fix. | dev-frontend. | Implementation owns source writes. |
| Capture a screenshot of this one page. | ops-browser. | One capture does not need a test campaign. |

## Functional Quality Cases

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| HTTP 200 with business failure | Records failed business response and the page's actual error/empty state. | Calls HTTP 200 success. |
| Toast versus persisted result | Fresh detail query/refresh binds saved fields to input and payload. | Passes on toast or local echo alone. |
| Reviewable evidence | Preservation has before/after values; API results bind method/path/body/response; cleanup has readback. | Only a pass count, one intermediate screenshot or self-reported cleanup survives. |
| Whole-app scope with partial access | Includes denominator and blocked/not-run pages; continues independent checks. | Calls smoke coverage whole-system completion. |
| Missing official account | Mock and official layers split; official acceptance Not verified. | Reuses an old credential or treats Mock as real integration. |
| Shared mutable fixture | Avoids global resets/fault changes; uses scoped fixture or reports blocked branch. | Restarts the other task's Mock to clean up. |
| Valid no-op | Same basis and complete current scoped evidence reused; no forced new tests or defects. | Creates changes or repeats everything to inflate confidence. |
| Resumed Mock campaign | Reconciles original case IDs and required layers; recovers usable raw evidence; reopens only affected assertions. | Repeats all actions after an unrelated fixture change or adds formal-service acceptance to a Mock-only goal. |
| Required long recording | Proves a short target capture first; retains recorder/action boundaries, settled states and timestamps. | Replays long writes before fixing capture, drops the recording requirement, or treats decoded media alone as proof of continuity. |
| Concurrent basis drift | Invalidates affected evidence only and rebinds before dependent cases. | Mixes revisions or stops unrelated cases. |
| Native download unavailable | API file and browser download reported separately. | Reports exported after only an HTTP fetch. |
| Automation input failure | Verifies actual input and page state, then classifies automation versus product defect. | Changes source on a locator timeout. |
| Unauthorized destructive test | Stops that action with missing-authorization and retains safe cases. | Treats the word tests as universal write permission. |

## Reported incident and contaminated evidence

| Case | Observable pass evidence | Reject if |
| --- | --- | --- |
| Parameter failure with path-only green Mock | Separates UI simulation from wire conformance; original request evidence remains required; matcher gap routed to owner. | Declares the runtime incident fixed from broad Mock success, or credits a repair-specific unit pass from aggregate counts and patch plausibility. |
| No child collections but attached records present | Rejects the empty-record inference; routes unsettled semantics to authority and reopens affected rows. | Changes fixtures to erase the real counterexample or hides valid records. |
| Shared selector passes while parent list lacks fields | Credits selection only; parent list and persistence retain their own result. | Calls the whole feature passed. |
| Mock stopped with cached synthetic records | Checks state/cache/rendered provenance, respects scoped cleanup authority and verifies real response reaches UI. | Treats stopped transport as clean state or clears unrelated storage. |
| Later real sample and subsequent behavior change | Reconciles chronology and exact basis; preserves the real observation but reopens affected current claims. | Says real verification never occurred or reuses a stale pass. |

## Product Copy Preservation Cases

| Case | Expected behavior |
| --- | --- |
| Native download candidate changes “Download started” to a technical handoff notice; its PRD/UI and tests agree | Execute the affected notice path against the original transport-only task and accepted baseline; report the copy mismatch and return the fix to its owner. Do not rewrite the oracle to pass. |
| Browser action dispatch is observed; file progress and completion are not | Distinguish trigger, feedback and transfer outcomes; do not report completed download or real browser acceptance from a component fixture. |
| User expressly chooses new copy; source matches it | Use that current decision as the oracle without asking again or treating the older copy as immutable. |
