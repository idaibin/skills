# Ops Browser Usage

## Summary

Use `ops-browser` for browser-based operations where existing tabs, sessions, state, or artifacts matter. It covers inspection, verification, debugging, form filling, upload/download, and browser evidence collection.

## Trigger Examples

- `Reuse an existing page to inspect this issue.`
- `Open the page in the background and verify it without stealing focus.`
- `Take a screenshot of this local web app and check the console errors.`
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
- Desktop client verification that must inspect a real app window; use `ops-client`.

## Operation Notes

- Start from existing tabs/windows before opening a new page.
- Prefer selectors, roles, labels, DOM state, console, network, and storage evidence.
- Stop before login, MFA, consent, account switch, purchase, permission grant, destructive submit, or irreversible state changes unless the user explicitly authorized that action.
- Treat form submit, upload, cache clearing, logout, refresh, and destructive navigation as state-changing actions.
- Use temporary pages for account/cache isolation, destructive checks, or when the existing tab is user-owned.
- Close pages/windows opened only for the task.
