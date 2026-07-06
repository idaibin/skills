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

- Pick the debugging path before choosing a browser surface. Use Playwright for local projects that can start from repo commands and run without manual login, or with available test credentials/seeded auth.
- Use Codex in-app Browser when the task benefits from a preserved Codex-owned login state, third-party login, or a user-completed sign-in inside Codex, and does not need the user's Arc/Chrome profile state.
- Use the user's default browser through CDP, Codex Remote, the Chrome plugin, or Computer Use when the user explicitly named that browser/page, the workflow needs that browser's existing account state, or the task involves user-owned uploads, downloads, or visible web operations.
- Enumerate browser surfaces and existing tabs before opening a page. Record available browser/window details, tab handle, URL/title, and whether the tab can be reused safely.
- Choose the browser in this order: requested or recorded session browser; browser/tab with the required session evidence; Codex in-app Browser when it is already signed in or the task does not require an external browser profile; user's default browser such as Arc; approved Chrome/Chromium fallback.
- Treat Codex Remote, extension tab inventory, and CDP as observed capabilities of a specific browser surface. Do not prefer or reject a browser by name alone, and do not treat documented capability as usable until the needed action works on the target tab.
- Operate by direct tab handle, session URL, DOM/page scripting, Playwright, or CDP when available. If that path times out or fails for the target tab, mark it unavailable for that operation before using a degraded fallback. Do not bring the browser forward, switch visible tabs, switch Spaces, or move the pointer just to read, type, upload, or send while target-scoped control works.
- Prefer Codex in-app Browser for Codex-owned browser work, localhost or file checks, repeatable visual evidence, and web sessions the user has explicitly signed into there. It is separate from the user's Arc/Chrome profiles, so do not use it when the task depends on those existing cookies, accounts, extensions, downloads, or tab state.
- When the needed logged-in session is in Arc, prefer Arc and reuse its existing tab or conversation. Use any extension-provided Arc browser state, tab metadata, session URL, or direct target-tab operation that works for the target tab, even if the exposed surface name is generic.
- Combine browser tools instead of treating them as exclusive: use Codex Remote or the Chrome plugin for browser/tab state and target-scoped read/write/click when those APIs work; use Computer Use only for UI steps that the remote browser API cannot expose. Report the exact split and whether Computer Use changed focus, selected tabs, windows, or visible state.
- For Chrome, use the Chrome plugin/Codex Chrome Extension when the user requested Chrome or approved Chrome as the controlled fallback. Verify that the extension-backed tab APIs can enumerate or claim the target tab before promising background read/write/click behavior.
- If the chosen browser lacks required control but Chrome/Chromium has it, explain the account/session risk and ask before switching. If fallback was pre-authorized, proceed and report it. If consent is unavailable, do not switch and mark the browser-dependent claim `Not verified`.
- Treat Computer Use and system-level visible selection as degraded fallback paths after target-scoped methods fail or are unavailable; report the focus risk and what visible state was changed.
- For repeatable web automation that should live in a repo or CI, prefer Playwright and the repository's existing test commands. If Playwright config or scripts are not present, say `Not found` before proposing to add them.
- Keep one-off browser checks in the chosen browser surface that owns the relevant login/session evidence; do not force those checks into Playwright if that would lose the session.
- For browser text entry, prefer direct DOM or Playwright `fill()` when the field can be targeted safely, then CDP text insertion such as `Input.insertText` after focusing the target. Use ordinary key typing only for short text. Use file upload only when the site should receive an attachment rather than inline prompt text.
- Avoid the system clipboard for browser input because it can race with the user's clipboard and other agents. If clipboard use is unavoidable, save the current clipboard, perform the smallest scoped paste, verify the target state, then restore the saved clipboard.
- For temporary file uploads, use a task-specific file under `/private/tmp`, avoid sensitive filenames, delete the local file after upload, and report that deleting the local file does not remove any server-side uploaded attachment.
- Keep one browser surface and one tab for the task whenever practical. Open extra windows or tabs only for a specific reason such as account/cache isolation, side-by-side comparison, destructive testing isolation, or required evidence.
- When extra browser surfaces are required, name their purpose and close task-only temporary pages/windows afterward.
- For persistent web conversations or workflows, create one browser session per task, record the stable session identifier when available, and reuse it for follow-up work on that same task.
- A session record should capture the task key, stable session id such as a conversation id, exact URL or title helper, tab handle when available, account/session note, last used date, and active/archived status.
- Treat the stable session id as the source of truth. Exact conversation URLs and tool-exposed tab handles are stronger lookup helpers than tab title or visible window state, but tab handles can be scoped to a browser, tool session, or runtime lifetime and must be revalidated before use.
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
