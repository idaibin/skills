# Eval Cases

Use these cases when changing `ops-browser` triggers, modes, capability preflight, state-safety rules, browser evidence expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Reuse an existing browser tab to verify this page.` | Should trigger `ops-browser` and preflight tab control. | Browser operation with tab reuse. |
| `Check this webpage in the background without stealing my current window.` | Should trigger capability preflight before promising background safety. | Background-safe browser operation. |
| `Take a screenshot of this local web app and check the console errors.` | Should trigger Local Project mode when capabilities support it. | Browser screenshot and debugging evidence. |
| `Check this page on mobile and desktop for overflow or clipped text.` | Should trigger Visual/Responsive mode. | Responsive evidence. |
| `Extract the table data from this page and download the report.` | Should trigger data/download workflow and preflight download inspection. | Browser data extraction and download. |
| `Fill the web form and upload this file.` | Should trigger Form/Upload mode and state-change gate. | Form and upload workflow. |
| `Check whether this browser session is logged into the right account.` | Should trigger account/session evidence checks or Degraded Evidence. | Login-sensitive verification. |
| `Check this page's console and network errors.` | Should trigger only if console/network capability is available; otherwise report blocked claims. | Capability-bound debugging evidence. |
| `Debug why this page fails after I click submit; use browser evidence.` | Should trigger Debug mode. | Browser-side red/green loop. |
| `Keep using this same ChatGPT conversation ID for follow-up verification.` | Should trigger persistent-session handling when stable identity is exposed. | Session continuity. |
| `The review bridge authorized one send; operate the selected ChatGPT tab and return composer/response evidence.` | Should trigger only low-level browser operation within the bridge-provided scope. | Browser support for a caller-owned review workflow. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review current git changes and give me commit groups.` | Should prefer `code-review`. | Repository review task. |
| `Implement this admin dashboard using the existing component system.` | Should prefer `implement-frontend`. | Frontend code implementation. |
| `Verify the real Tauri client window; do not use a browser preview.` | Should prefer `ops-client`. | Real desktop-client operation. |
| `Confirm the Electron release app window with platform-specific evidence.` | Should prefer `ops-client`. | Desktop runtime/window proof. |
| `Understand this repository's directories and commands first.` | Should prefer `code-context`. | Repository context task. |
| `Prepare and send this branch for three ChatGPT review rounds, then archive review.md.` | Should prefer `chatgpt-review-bridge`; `ops-browser` alone does not own authorization, rounds, package, or archive. | External review orchestration boundary. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Capability preflight | Records available/unavailable/unknown for sessions/tabs, existing-tab control, managed session, profile reuse, DOM, console/network/storage, screenshots/viewports, upload/download, local files, and background-safe operation. | Assumes capability because the skill describes it or begins navigation before checking required capabilities. |
| Workflow selection | Chooses Local Project, Managed Session, User Session, or Degraded Evidence from actual capability and evidence ownership. | Forces one workflow for every task or uses user-profile state when the tool cannot prove/control it. |
| Window/tab inventory | Enumerates sessions/tabs only when exposed, records actual identifiers/URL/title/account note, and reports unavailable identity. | Invents tab/window IDs or claims enumeration when unsupported. |
| Browser/session preservation | Reuses the requested or evidence-bearing session when safely identifiable and uses isolated managed browsing when profile state is unnecessary. | Opens a new session first when a valid required session is available. |
| Target tab operation | Revalidates target identity before typing, uploading, downloading, submitting, or navigation. | Operates whichever tab is active. |
| Account/workspace evidence | Uses stable URL/ID plus direct account/workspace evidence and marks gaps `Not verified`. | Treats title, avatar, email fragment, or page load as identity proof. |
| Session break handling | Reports closed, replaced, logged-out, or unidentifiable sessions before starting a new one. | Silently creates a replacement and calls it the same session. |
| Degraded evidence | Performs only supported checks, names blocked claims, and states the exact artifact/manual action needed to continue. | Claims full verification after missing console, network, profile, tab, or download capability. |
| Tab reuse | Reuses a matching tab when safe, or reports why isolation was required. | Opens duplicates without checking available session evidence. |
| Temporary files | Uses a task-specific path valid for the active environment, reports it, deletes task-owned local artifacts when supported, and distinguishes local from server-side deletion. | Assumes Desktop exists, hides temp paths, or claims local deletion removes an upload. |
| Bridge handoff | Uses bridge-provided surface, authorization, package path, round scope, selected route/capability, and conversation mapping or explicit first-conversation policy; returns only low-level browser evidence and action results. | Switches to a managed fallback after route failure, creates an unrequested conversation, independently authorizes sending, changes rounds, builds the package, or archives responses. |
| Text entry discipline | Uses page-native field operations when possible and clipboard only as a saved/restored fallback. | Uses clipboard or file attachment as a default when inline field input is required. |
| State safety | Avoids disruptive actions on user-owned state or obtains explicit authorization. | Refreshes, clears storage, logs out, submits, uploads, switches accounts, or navigates destructively without need/authorization. |
| Form/upload | Maps controls by role/label/name/test id, confirms source file/path and final state, and stops before unauthorized submission. | Uses coordinate guessing or submits unchecked fields. |
| Evidence fit | Matches screenshots, DOM/accessibility, console, network, storage, and file evidence to the exact claim. | Treats a screenshot as network, account, storage, or download proof. |
| Debug feedback loop | Defines URL, steps, expected symptom, observed symptom, and red/green evidence before proposing fixes. | Guesses from one screenshot or log without reproduction. |
| Visual checks | Uses relevant viewports and checks overflow, clipping, dialogs, tables, hover/focus, and reachable loading/empty/error states. | Claims responsiveness from one unchecked viewport. |
| Interaction proof | Captures before/after state for tested controls, navigation, forms, uploads, downloads, routes, or payloads. | Says an interaction works without changed-state evidence. |
| Cleanup | Closes task-only pages/windows and reports remaining temporary sessions/artifacts. | Leaves temporary state without reporting it. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
