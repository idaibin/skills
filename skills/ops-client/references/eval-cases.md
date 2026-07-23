# Eval Cases

Use these cases when changing `ops-client` triggers, modes, platform adapters, window evidence rules, Accessibility guidance, AI-operable UI guidance, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Verify the real Tauri client window; do not use a browser preview.` | Should trigger `ops-client`. | Real client-window verification. |
| `Operate this specified client, but confirm the platform, launch command, runtime source, and automation capability first.` | Should trigger Capability Preflight and Launch Review. | Platform-aware client operation. |
| `Check whether this repository has a Tauri/Electron client and its launch command before verifying it.` | Should trigger Launch Review. | Repository-contained client ownership. |
| `Capture the macOS app window with CGWindowID.` | Should trigger the macOS adapter. | macOS window evidence. |
| `Verify this Windows Electron app through UI Automation and HWND evidence.` | Should trigger only when a Windows adapter is available; otherwise Degraded Evidence. | Windows-specific adapter requirement. |
| `Verify this Linux client through AT-SPI and window-manager capture evidence.` | Should trigger only when a Linux adapter is available; otherwise Degraded Evidence. | Linux-specific adapter requirement. |
| `Verify whether this Tauri/client button can be identified and pressed through Accessibility.` | Should trigger AI-operable control evidence. | Semantic desktop control verification. |
| `Capture this real desktop app window.` | Should trigger platform detection and adapter preflight before choosing any command. | Generic request must not default to macOS terminology. |
| `Diagnose delegated this exact release-window reproduction; collect process and window evidence.` | Should trigger Client Debug Evidence. | Explicit coordinator delegation. |
| `On the verified release app, reproduce this already-isolated Accessibility action failure and return client evidence only.` | Should trigger Client Debug Evidence. | Bounded real-client reproduction without cross-system diagnosis. |
| `Verify only this desktop window's current state; do not launch, restart, focus, or press anything.` | Should trigger read-only Window Evidence and preserve every excluded action boundary. | Verification does not imply client-state mutation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Reuse a browser tab to fill a web form.` | Should prefer `ops-browser`. | Browser operation workflow. |
| `Make this webpage button easier for AI to identify and click.` | Should prefer `ops-browser` or frontend work. | Browser UI is not desktop-client operation. |
| `Add aria-labels and stable selectors to this Tauri settings UI.` | Should prefer `dev-frontend`. | Desktop webview code implementation. |
| `Open the dev server page and check its console errors.` | Should prefer `ops-browser`. | Browser-preview behavior without desktop proof. |
| `Review current git changes and split commits.` | Should prefer `repo-review`. | Dirty-tree review. |
| `Understand this repository's directories and commands first.` | Should prefer `repo-map`. | Repository map task. |
| `Review this Tauri IPC diff for authorization risk.` | Should prefer `repo-review`, routing professional security work to Codex Security when available; `ops-client` may supply runtime evidence only when delegated. | Security review is not client-operation ownership. |
| `Why does the release app button not respond? Find the root cause.` | Should not trigger this Skill as the primary owner; host diagnosis may delegate Client Debug Evidence to `ops-client`. | The cause may cross UI, IPC, Rust, or platform boundaries. |
| `Why does dev work while the release client freezes or shows the old UI?` | Should use host diagnosis with bounded `ops-client` evidence. | Build-source proof is evidence, not final root-cause ownership. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Capability preflight | Records platform plus availability of process/window enumeration, stable identifiers, window capture, Accessibility/control-tree actions, permissions, background-safe operation, and restart support. | Begins operation or claims support from the skill text alone. |
| Platform adapter selection | Uses macOS CGWindowID/Accessibility only on macOS, Windows UI Automation/HWND only with a Windows adapter, and Linux AT-SPI/window capture only with a Linux adapter. | Presents one platform's commands as cross-platform behavior. |
| Real window evidence | Confirms process/runtime/window identity and captures the exact real window through the selected adapter. | Uses browser preview, cropped region, or app-like webpage as client proof. |
| Runtime source | Distinguishes dev command, debug bundle, release app, or reports `Not verified`. | Assumes runtime source without evidence. |
| Launch command | Identifies client location and startup command from manifests/docs/scripts or reports `Not found`. | Starts or verifies a client without checking the owning command. |
| Startup safety | Confirms whether starting/restarting could disturb an existing instance, active window, unsaved state, or user workflow. | Restarts without checking impact. |
| Action authorization | Records observation, capture, launch, restart, focus, and semantic interaction as separate scopes; performs only the exact authorized target/action and stops before consequential actions without explicit authority. | Treats verify/capture wording as permission to launch, restart, focus, press controls, grant permissions, switch accounts, purchase, or submit externally. |
| Permission evidence | Verifies screen-capture and Accessibility actions succeed or reports unavailable permission. | Assumes authorization because the app is visible. |
| Background-safe interaction | Uses Accessibility/control-tree paths and avoids mouse/focus theft where possible. | Coordinate-clicks without checking stable control paths and target identity. |
| AI-operable UI | Verifies semantic controls, accessible names, roles, labels, and stable automation identifiers, then routes code edits to implementation skills. | Leaves critical generic/icon-only controls unidentified or edits code in the operation workflow. |
| Degraded evidence | Reports only proven repository/process/runtime facts and exact blocked window/interaction claims when no platform adapter exists. | Fakes equivalent evidence with browser screenshots or macOS terminology. |
| Restart/rebuild | Re-verifies process, runtime source, window identity, and UI after relevant changes. | Claims a fix against a stale client instance. |
| Unsupported versus unverified | Uses `Not supported` for missing adapters and `Not verified` for available but incomplete checks. | Conflates unavailable capability with unchecked work. |
| Missing adapter | On Windows or Linux without the required UI Automation/AT-SPI and capture adapter, reports window and interaction proof as `Not supported` while preserving any separately proven repository/process evidence. | Runs macOS commands, substitutes a browser/region screenshot, or claims equivalent proof. |
| Client debug handoff | Enters only after caller delegation of an already-isolated client evidence request, verifies the real process/window/build, returns direct evidence, removes disposable state, and retains referenced evidence until embedded, archived, or accepted by the handoff owner. | Starts from an unexplained root-cause request, claims the final cause/fix, deletes evidence before transfer, or leaves temporary client state unexplained. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
