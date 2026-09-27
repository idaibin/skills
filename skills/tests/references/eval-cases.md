# Eval Cases

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| Use $tests to exercise the existing test deployment from API through page clicks and refreshed business results. | Execute bounded journeys, correlate evidence and return coverage/cleanup. | Explicit functional acceptance. |
| Walk the application end to end: UI, system functions, permissions, filters and logic. | Select tests, resolve finite inventory, run authorized cases. | Contextual functional acceptance. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| Review this fixed commit for correctness, without running the application. | repo-review. | Source review is a separate outcome. |
| Implement the confirmed search debounce fix. | dev-frontend. | Implementation owns source writes. |
| Capture a screenshot of this one page. | ops-browser. | One capture does not need a test campaign. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| HTTP 200 with business failure | Records failed business response and the page's actual error/empty state. | Calls HTTP 200 success. |
| Toast versus persisted result | Fresh detail query/refresh binds saved fields to input and payload. | Passes on toast or local echo alone. |
| Reviewable evidence | Preservation has before/after values; API results bind method/path/body/response; cleanup has readback. | Only a pass count, one intermediate screenshot or self-reported cleanup survives. |
| Whole-app scope with partial access | Includes denominator and blocked/not-run pages; continues independent checks. | Calls smoke coverage whole-system completion. |
| Missing official account | Mock and official layers split; official acceptance Not verified. | Reuses an old credential or treats Mock as real integration. |
| Shared mutable fixture | Avoids global resets/fault changes; uses scoped fixture or reports blocked branch. | Restarts the other task's Mock to clean up. |
| Valid no-op | Same basis and complete current scoped evidence reused; no forced new tests or defects. | Creates changes or repeats everything to inflate confidence. |
| Concurrent basis drift | Invalidates affected evidence only and rebinds before dependent cases. | Mixes revisions or stops unrelated cases. |
| Native download unavailable | API file and browser download reported separately. | Reports exported after only an HTTP fetch. |
| Automation input failure | Verifies actual input and page state, then classifies automation versus product defect. | Changes source on a locator timeout. |
| Unauthorized destructive test | Stops that action with missing-authorization and retains safe cases. | Treats the word tests as universal write permission. |
