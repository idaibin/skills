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

- Start by enumerating browser surfaces and existing tabs exposed by available tooling before opening a new page; record relevant tool-exposed browser/window information, tab id, URL, title, and whether it can be reused safely where available.
- Use the user's default browser or already-authenticated browser by default. Do not switch to Chrome just because Chrome automation is available if the expected login/session is in another browser.
- When Chrome is explicitly requested or required through the Codex Chrome Extension, use its tab inventory for existing Chrome sessions. Treat Computer Use as visible/key-window evidence, not as the primary way to enumerate all browser tabs.
- If a task needs a browser-specific capability that would move work away from the user's default or authenticated browser, state the reason and account/session risk before proceeding.
- For repeatable web automation that should live in a repo or CI, prefer Playwright and the repository's existing test commands. If Playwright config or scripts are not present, say `Not found` before proposing to add them.
- Keep one-off browser checks in the user's default or already-authenticated browser when login/session state is the evidence target; do not force those checks into Playwright if that would lose the session.
- For browser text entry, prefer direct DOM or Playwright `fill()` when the field can be targeted safely, then CDP text insertion such as `Input.insertText` after focusing the target. Use ordinary key typing only for short text. Use file upload only when the site should receive an attachment rather than inline prompt text.
- Avoid the system clipboard for browser input because it can race with the user's clipboard and other agents. If clipboard use is unavoidable, save the current clipboard, perform the smallest scoped paste, verify the target state, then restore the saved clipboard.
- For temporary file uploads, use a task-specific file under `/private/tmp`, avoid sensitive filenames, delete the local file after upload, and report that deleting the local file does not remove any server-side uploaded attachment.
- Keep one browser surface and one tab for the task whenever practical. Open extra windows or tabs only for a specific reason such as account/cache isolation, side-by-side comparison, destructive testing isolation, or required evidence.
- When extra browser surfaces are required, name their purpose and close task-only temporary pages/windows afterward.
- For persistent web conversations or workflows, create one browser session per task, record the stable session identifier when available, and reuse it for follow-up work on that same task.
- A session record should capture the task key, stable session id such as a conversation id, URL/title lookup helper, account/session note, browser tab/window note, created date, last used date, and active/archived status.
- Treat the stable session id as the source of truth. Tab title, URL, and visible window state are lookup helpers unless the browser tool exposes stronger identity.
- Do not reuse one persistent web conversation for unrelated tasks just because the tab is still open. Do not create a new conversation for follow-up work when an active session record already exists.
- If the recorded tab was closed, replaced, logged out, or navigated away, report the session break and ask whether to recover the original session or start a fresh one.
- Prefer selectors, roles, labels, DOM state, console, network, and storage evidence.
- Match evidence to the claim: use screenshots for visual/layout state, DOM or accessibility data for selectors and rendered text, console logs for client errors, network records for request/response behavior, storage/auth state for account/session claims, and file checks for downloads.
- For visible UI verification, check relevant viewports, overflow, clipped text, table/dialog layout, hover/focus behavior, and reachable loading/empty/error states.
- For interactive verification, capture or report before/after state for controls, navigation, forms, uploads, downloads, route changes, and generated payloads when relevant.
- Do not force a fixed number of issues; report observed issues, residual risk, and `Not verified` gaps.
- Stop before login, MFA, consent, account switch, purchase, permission grant, destructive submit, or irreversible state changes unless the user explicitly authorized that action.
- Treat form submit, upload, cache clearing, logout, refresh, and destructive navigation as state-changing actions.
- Use temporary pages for account/cache isolation, destructive checks, or when the existing tab is user-owned; avoid creating several temporary pages for the same purpose.
- Close pages/windows opened only for the task.
- If the browser tool exposes only partial tab or window metadata, report the available URL/title/session evidence and mark missing identity as `Not verified` instead of inferring it.
