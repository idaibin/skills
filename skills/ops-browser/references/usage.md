# Ops Browser Usage

## Summary

Use `ops-browser` for browser-based operations where existing tabs, sessions, state, visual evidence, or artifacts matter. It covers inspection, visual/responsive verification, debugging, form filling, upload/download, and browser evidence collection. Use `frontend-implementation` for code changes.

## Trigger Examples

- `Reuse an existing page to inspect this issue.`
- `Open the page in the background and verify it without stealing focus.`
- `Take a screenshot of this local web app and check the console errors.`
- `Check the mobile and desktop layout for overflow or clipped text.`
- `Extract the table data from this page.`
- `Fill this form in a background page without disturbing my current tabs.`
- `Upload this file and confirm the page state afterward.`
- `Download the generated report and confirm the file exists.`
- `Check whether the current browser session is logged in to the right account.`
- `Check browser console/network to see why this failed.`
- `Verify this page, then close the temporary window afterward.`

## Non-Triggers

- Repository-only code review without browser execution.
- Pure API inspection that does not require a browser session.
- Frontend implementation, component refactors, or design-system choices; use `frontend-implementation`.
- Desktop client verification that must inspect a real app window; use `ops-client`.

## Operation Notes

- Start from existing tabs/windows before opening a new page.
- Prefer selectors, roles, labels, DOM state, console, network, and storage evidence.
- Match evidence to the claim: use screenshots for visual/layout state, DOM or accessibility data for selectors and rendered text, console logs for client errors, network records for request/response behavior, storage/auth state for account/session claims, and file checks for downloads.
- For visible UI verification, check relevant viewports, overflow, clipped text, table/dialog layout, hover/focus behavior, and reachable loading/empty/error states.
- For interactive verification, capture or report before/after state for controls, navigation, forms, uploads, downloads, route changes, and generated payloads when relevant.
- Do not force a fixed number of issues; report observed issues, residual risk, and `Not verified` gaps.
- Stop before login, MFA, consent, account switch, purchase, permission grant, destructive submit, or irreversible state changes unless the user explicitly authorized that action.
- Treat form submit, upload, cache clearing, logout, refresh, and destructive navigation as state-changing actions.
- Use temporary pages for account/cache isolation, destructive checks, or when the existing tab is user-owned.
- Close pages/windows opened only for the task.
