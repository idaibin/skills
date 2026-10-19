# Pages, UI and interaction

## Reach the function

Enter from the real menu, button or link when testing navigation. Preserve the current
origin, base path and required business query context. A directly opened destination
proves only route rendering; it cannot repair a failed navigation assertion. Verify
SPA, iframe, new-tab and downloaded-file targets at their actual terminal surface.
An observed `window.open` event without an observable child page is not launch success.

Freeze app, route, viewport/device, zoom, theme, data and interaction state. Identify
the shell, shared component, UI adapter and page owners before attributing a visual
issue. Compare like-for-like states against the accepted reference, not whichever
other checkout happens to look right. Contracts can supersede a legacy comparison.

## Walk the page

| Surface | What must be observed |
| --- | --- |
| Navigation | active menu, correct destination/content, back/return, query retention, direct refresh |
| Lists | search, combined filters, reset, tab change, next/last page, counts, empty state, detail and return |
| Forms | native input semantics, required/invalid state, submit enablement, duplicate action protection, cancel, save and refreshed values |
| Drawers/dialogs | open/close, mask/Escape according to contract, scroll reachability, preserved/cancelled draft, restored focus |
| Selectors | selected/half-selected counts, nested groups, cross-tab selection, confirm versus cancel |
| System functions | entry permission, correct parameters, terminal iframe/tab/window, loading/failure/empty address and recovery |
| Visual states | layout, spacing, alignment, typography, icons/assets, clipping, overflow, contrast and readable theme states |
| Interaction states | hover, pressed, focus-visible, keyboard Tab/Enter/Escape, disabled hits, animation completion and click competition |

Observe actual page controls before selecting. Scope duplicate labels to the visible
dialog, row or section. After a failed action inspect current DOM and overlays before
changing strategy. A controlled input or editor must show the intended value before
calling it filled; use its native supported controls, not direct app-state mutation.

## UI evidence

For asynchronous overlays, exercise focus across loading, failure, retry, busy controls,
control replacement and close. Check applicable Tab/Shift+Tab containment and restored
focus against the accepted UI contract; non-modal overlays need not trap focus. Labels,
screenshots and disabled styling do not prove keyboard continuity or duplicate admission.

Use screenshots for appearance, computed geometry for dimensions, DOM/AX for semantics,
network for requests and console for runtime errors. Observe initial, intermediate
and final states required by the case; do not blur controls or inject CSS to improve
the capture. Confirm fonts/data are ready and the actual viewport matches the matrix.

Read back every retained capture. Blank, tiled, clipped, stale or wrong-theme images
fail that evidence item. A screenshot may prove a visible defect without proving its
cause. Same-state comparison after an authorized fix closes the affected visual claim;
repeat additional passes only when the accepted project rule requires them.

Continuous recording is conditional on the user's/project's acceptance requirement.
When required, first verify a short capture on the actual target: viewport, readable
frame, recorder lifecycle, retained output and playback. Fix capture failures before
replaying a long write journey. Then capture the planned actions through their settled
final state, correlating recording start/stop and action times with retained evidence.
Native change-frame streams may have idle gaps; preserve timestamps and capture origin.
Encoding their frames does not itself break continuity, while stitching independent
screenshots does not establish it. Media decoding alone proves neither capture
continuity nor business correctness. Missing capability blocks only the video claim.

Console warnings need attribution; no console errors does not mean no functional bug.
For downloads, correlate the click, response, observed browser download and actual
file bytes/content. An API-fetched file alone does not close browser delivery.

## Cleanup

Use task-owned tabs when prior user/other-task state would be disturbed. Restore only
temporary state owned by this run and close task-created tabs unless retention is
requested. Never stop another task, clear shared auth/storage or switch its account.
Report any unverified cleanup and retain evidence needed to resume the specific case.
