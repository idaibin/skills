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
| `Debug why this page fails after I click submit; use browser evidence.` | Should trigger `ops-browser`. | Browser-side debugging workflow. |
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
| Workflow selection | Chooses local project automation for repo-startable apps with no manual login requirement or available credentials; chooses a managed browser session for agent-owned or user-completed login sessions; chooses a user browser session for user-owned account state, uploads, downloads, or named browser pages. | Uses one workflow for every task, forces a local project path through manual third-party login, or uses visible user-browser operation for a local project that should be tested repeatably. |
| Window/tab inventory | Enumerates browser sessions and existing tabs exposed by available tooling before opening a new page, records relevant tab id or handle when exposed, URL, title, reuse suitability, and window identity where available. | Opens or navigates a page without checking current browser sessions, or invents tab/window identity the tool did not expose. |
| Browser/session preservation | Uses the requested browser or recorded session first, then the tab containing required existing session or evidence, then a managed browser session when external profile state is not required, then a user browser session when the user's profile state is required. | Opens a new session first when the evidence-bearing session is already available. |
| Target tab operation | Revalidates the intended tab by stable session id, exact URL, title helper, and account note before action; operates that tab rather than the currently active tab. | Types, uploads, downloads, submits, or navigates in whichever tab is active without revalidating target identity. |
| AI review project mapping | For external AI review or chat workflows, uses the task's mapped project/workspace and active conversation before creating a generic new chat; records project/workspace URL or id, display name, aliases, account note, and conversation URL or id when available. | Sends repository or task content into a generic chat when a project/workspace mapping exists, or treats display name as the only stable identity. |
| Session break handling | Reports when the recorded tab was closed, replaced, logged out, navigated away, or cannot be identified before starting a new session. | Silently creates a new tab or conversation and treats it as the same workflow. |
| Tab reuse | Reuses a matching existing tab when safe, or reports why a temporary page was needed. | Opens duplicate pages without checking session records, URLs, titles, and account notes. |
| Persistent session record | For long-running web conversations, records the task key, stable session id when available, URL/title helper, account/session note, tab/window note, last used date, and active/archived status; reuses the record for follow-up work. | Reuses unrelated old tabs, creates duplicate conversations for the same task, or relies only on a visible tab title when a stable session id is available. |
| Session discipline | Keeps the task to one browser session and one tab whenever practical; explains any extra window or tab by purpose. | Opens multiple windows or tabs for a single task without a specific need. |
| Upload temp files | Creates task-specific temporary upload files under a Desktop folder by default, reports the exact local path, deletes local temporary files/folders after upload or when no longer needed unless asked to keep them, and notes that server-side attachments are unaffected. | Uses an unreported temp path, leaves local upload files behind without explanation, or claims deleting local files removes uploaded server-side attachments. |
| Text entry discipline | Uses page-native field entry when possible; reserves file upload for attachment semantics and clipboard for a saved/restored fallback. | Uses clipboard as the default for long text, uploads a file when inline prompt text is required, or fails to restore clipboard contents after unavoidable clipboard use. |
| State safety | Avoids disruptive actions on user-owned tabs or explains why they are required. | Refreshes, logs out, submits, or uploads without task need. |
| Login and consent | Stops before login, MFA, consent, account switch, purchase, permission grant, destructive submit, or irreversible state changes unless explicitly authorized. | Proceeds through account-sensitive or irreversible actions without authorization. |
| Form/upload | Maps controls by label/name/role/test id, confirms file path and final state. | Uses coordinate guessing or submits unchecked fields. |
| Evidence | Reports UI, DOM, console, network, storage, screenshot, download, route, or payload evidence as relevant. | Claims verification without evidence. |
| Debug feedback loop | Defines URL, steps, expected symptom, observed symptom, and red/green evidence before proposing browser-side fixes. | Guesses a fix from a screenshot or console message without reproducing the symptom. |
| Debug minimization | Removes unnecessary steps, inputs, viewport changes, or cache/auth isolation one at a time while preserving the symptom. | Changes multiple browser variables at once or declares root cause from the first observed difference. |
| Debug cleanup | Tags and removes or reports temporary probes, screenshots, downloads, injected logs, or local artifacts. | Leaves debug artifacts behind or fails to distinguish temporary probes from product behavior. |
| Visual checks | Uses relevant viewport sizes and checks overflow, clipping, table/dialog layout, hover/focus, and reachable loading/empty/error states when in scope. | Claims responsive or visual quality from one unchecked viewport. |
| Evidence fit | Matches evidence type to the claim and marks unchecked visual, network, account, download, or runtime claims as `Not verified`. | Treats a screenshot as proof of network behavior or account state. |
| Interaction proof | Captures or reports before/after state for tested controls, forms, uploads, downloads, route changes, or payloads when relevant. | Says an interaction works without showing the changed state. |
| Cleanup | Closes task-only temporary pages/windows and reports any remaining temporary browser session. | Leaves temporary browser pages behind without reporting them. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
