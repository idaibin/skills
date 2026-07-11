# Ops Browser Usage

## Summary

Use `ops-browser` for browser-based operations where existing tabs, sessions, state, visual evidence, or artifacts matter. It covers inspection, visual/responsive verification, debugging, form filling, upload/download, and browser evidence collection. Use `implement-frontend` for code changes.

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
- Frontend implementation, component refactors, or design-system choices; use `implement-frontend`.
- Desktop client verification that must inspect a real app window; use `ops-client`.

## Operation Notes

- Pick the workflow type before choosing a browser session. Use local project automation for repo-startable apps that do not need manual login or have available test credentials. Use a managed browser session when the agent can own the session or the user signs in there. Use a user browser session when the task depends on the user's existing profile, downloads, extensions, tab state, or account state.
- Enumerate browser sessions and existing tabs before opening a page only when the active tool exposes enumeration. Record only available browser/window details, tab handle when exposed, URL/title, account or session note, and whether the tab can be reused safely. If enumeration is unavailable, do not claim reuse or identity; for ordinary browser work use a safely isolated managed page only when profile state is unnecessary. For a bridge handoff, never change the bridge-selected route: return the blocked capability/identity claim instead.
- Choose the session in this order: user-requested or recorded session; tab with required login/state evidence; managed browser session when external profile state is not required; user browser session when the task depends on the user's profile, downloads, extensions, or account state.
- Reuse the same tab and browser session for one task whenever practical. Before opening a new tab, re-enumerate tabs and search by session record, exact URL, stable session id, title helper, and account note.
- For external ChatGPT review, accept the surface, authorization state, package path, round scope, selected browser route/capability, and conversation mapping—or the bridge's explicit policy to create exactly one first conversation—from `chatgpt-review-bridge`. Perform only low-level actions on that route and return evidence. If the route or mapping cannot be revalidated, stop and return the break; do not switch sessions, create an unrequested conversation, package repository content, decide that sending is authorized, add rounds, or write the response archive.
- Operate the intended target tab, not whichever tab is currently active. Revalidate tab identity before typing, uploading, downloading, submitting, or navigating away.
- If the recorded tab was closed, replaced, logged out, navigated away, or cannot be identified, report the session break and ask whether to recover the original session or start a fresh one.
- Keep one-off browser checks in the browser session that owns the relevant login/session evidence; do not move them to a separate automation context when that would lose the session.
- For browser text entry, prefer page-native field operations when the field can be targeted safely. Use ordinary key typing only for short text. Use file upload only when the site should receive an attachment rather than inline prompt text.
- Avoid the system clipboard for browser input because it can race with the user's clipboard and other agents. If clipboard use is unavoidable, save the current clipboard, perform the smallest scoped paste, verify the target state, then restore the saved clipboard.
- For temporary file uploads, choose a task-specific path that the active browser tool can access: prefer a tool-provided artifact directory, then a repository-approved task temp directory, then the operating system temp directory. Use Desktop only when it exists, is writable, is tool-accessible, and the user or environment explicitly selects it. Avoid sensitive filenames, report the exact local path before upload, delete task-owned temporary files and folders after upload or when no longer needed unless the user asks to keep them, and report cleanup status. Deleting local temporary files does not remove any server-side uploaded attachment.
- Keep one browser session and one tab for the task whenever practical. Open extra windows or tabs only for a specific reason such as account/cache isolation, side-by-side comparison, destructive testing isolation, or required evidence.
- When extra browser sessions are required, name their purpose and close task-only temporary pages/windows afterward.
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

## Debug Notes

- Build the browser feedback loop first: exact target URL, viewport or account state if relevant, action sequence, expected symptom, observed symptom, and the evidence source that can prove red/green.
- Prefer a short repeatable browser script, deterministic DOM/console/network check, or documented manual sequence over exploratory clicking.
- Wait for the page state that matters before inspecting dynamic apps; do not inspect stale DOM or pre-hydration markup and treat it as final.
- Minimize the reproduction by removing steps, inputs, cache/auth isolation, and viewport changes one at a time while the symptom still appears.
- Form one browser hypothesis at a time, then test it with the smallest safe action. Do not bundle cache clearing, reloads, account switches, and code changes into one experiment.
- Tag temporary probes and artifacts with a unique task prefix so screenshots, downloads, console filters, local files, or injected logs can be removed or reported at the end.
- If the issue cannot be reproduced, report the loop attempts, missing evidence, and what artifact would unblock diagnosis instead of guessing at a fix.
