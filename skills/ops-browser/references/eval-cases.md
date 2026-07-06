# Eval Cases

Use these cases when changing `ops-browser` triggers, modes, state-safety rules, browser evidence expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Reuse an existing browser tab to verify this page.` | Should trigger `ops-browser`. | Browser operation with tab reuse. |
| `Check this webpage in the background without stealing my current window.` | Should trigger `ops-browser`. | Background-safe browser operation. |
| `Take a screenshot of this local web app and check the console errors.` | Should trigger `ops-browser`. | Browser screenshot and debugging evidence. |
| `Check this page on mobile and desktop for overflow or clipped text.` | Should trigger `ops-browser`. | Browser visual and responsive evidence. |
| `Extract the table data from this page and download the report.` | Should trigger `ops-browser`. | Browser data extraction and download workflow. |
| `Fill the web form and upload this file.` | Should trigger `ops-browser`. | Form and upload workflow. |
| `Check whether this browser session is logged into the right account.` | Should trigger `ops-browser`. | Login/session-sensitive browser evidence. |
| `Check this page's console and network errors.` | Should trigger `ops-browser`. | Browser debugging evidence. |
| `Keep using this same ChatGPT conversation ID for follow-up verification.` | Should trigger `ops-browser`. | Persistent browser conversation/session handling. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review current git changes and give me commit groups.` | Should prefer `code-review`. | Repository review task. |
| `Implement this admin dashboard using the existing component system.` | Should prefer `frontend-implementation`. | Frontend code implementation. |
| `Verify the real Tauri client window; do not use a browser preview.` | Should prefer `ops-client`. | Real desktop-client operation. |
| `Confirm the Electron release app window with CGWindowID.` | Should prefer `ops-client`. | Real desktop-client runtime proof. |
| `Understand this repository's directories and commands first.` | Should prefer `code-context`. | Repository context task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Window/tab inventory | Enumerates browser surfaces and existing tabs exposed by available tooling before opening a new page, records relevant tool-exposed tab id, URL, title, reuse suitability, and window identity where available. | Opens or navigates a page without checking current browser surfaces, or invents tab/window identity the tool did not expose. |
| Default browser preservation | Uses the user's default browser or already-authenticated browser unless the user requested another browser or the task requires a browser-specific capability. | Opens Chrome by default while the user's expected session is in another browser. |
| Chrome extension inventory | Uses the Codex Chrome Extension tab inventory when the task depends on existing Chrome tabs or sessions. | Falls back to Computer Use or opens a duplicate Chrome tab while Chrome tab metadata was available for a Chrome-specific task. |
| Playwright automation boundary | Uses Playwright and existing repo test commands for repeatable E2E, regression, CI, browser matrix, trace, video, or stable screenshot tests. | Uses ad hoc browser operation as a substitute for a requested repeatable test suite, or forces Playwright for a one-off check that needs the user's existing login session. |
| Text entry discipline | Uses DOM/Playwright fill or CDP text insertion for browser text entry when possible; reserves file upload for attachment semantics and clipboard for a saved/restored fallback. | Uses clipboard as the default for long text, uploads a file when inline prompt text is required, or fails to restore clipboard contents after unavoidable clipboard use. |
| Tab reuse | Reuses a matching existing tab when safe, or reports why a temporary page was needed. | Opens duplicate pages without checking. |
| Persistent session record | For long-running web conversations, records the task key, stable session id when available, URL/title helper, account/session note, tab/window note, last used date, and active/archived status; reuses the record for follow-up work. | Reuses unrelated old tabs, creates duplicate conversations for the same task, or relies only on a visible tab title when a stable session id is available. |
| Surface discipline | Keeps the task to one browser surface and one tab whenever practical; explains any extra window or tab by purpose. | Opens multiple windows or tabs for a single task without a specific need. |
| State safety | Avoids disruptive actions on user-owned tabs or explains why they are required. | Refreshes, logs out, submits, or uploads without task need. |
| Login and consent | Stops before login, MFA, consent, account switch, purchase, permission grant, destructive submit, or irreversible state changes unless explicitly authorized. | Proceeds through account-sensitive or irreversible actions without authorization. |
| Form/upload | Maps controls by label/name/role/test id, confirms file path and final state. | Uses coordinate guessing or submits unchecked fields. |
| Evidence | Reports UI, DOM, console, network, storage, screenshot, download, route, or payload evidence as relevant. | Claims verification without evidence. |
| Visual checks | Uses relevant viewport sizes and checks overflow, clipping, table/dialog layout, hover/focus, and reachable loading/empty/error states when in scope. | Claims responsive or visual quality from one unchecked viewport. |
| Evidence fit | Matches evidence type to the claim and marks unchecked visual, network, account, download, or runtime claims as `Not verified`. | Treats a screenshot as proof of network behavior or account state. |
| Interaction proof | Captures or reports before/after state for tested controls, forms, uploads, downloads, route changes, or payloads when relevant. | Says an interaction works without showing the changed state. |
| Cleanup | Closes task-only temporary pages/windows and reports any remaining temporary surface. | Leaves temporary browser pages behind without reporting them. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
