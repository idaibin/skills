# Eval Cases

Use these cases when changing `ops-client` triggers, modes, window evidence rules, Accessibility guidance, AI-operable UI guidance, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Verify the real Tauri client window; do not use a browser preview.` | Should trigger `ops-client`. | Real client-window verification. |
| `Operate this specified client, but confirm the launch command and runtime source first.` | Should trigger `ops-client`. | Specified client and launch review. |
| `Check whether this repository has a Tauri/Electron client and its launch command before verifying it.` | Should trigger `ops-client`. | Repository-contained client launch review. |
| `Capture the app window with CGWindowID.` | Should trigger `ops-client`. | Window-level screenshot evidence. |
| `Confirm the visible Electron release app, not just the web preview.` | Should trigger `ops-client`. | Electron runtime/window proof. |
| `Make this Tauri/client button easier for AI to identify and click.` | Should trigger `ops-client`. | AI-operable DOM/Accessibility guidance for client UI. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Reuse a browser tab to fill a web form.` | Should prefer `ops-browser`. | Browser operation workflow. |
| `Make this webpage button easier for AI to identify and click.` | Should prefer `ops-browser` or frontend work, not `ops-client`. | Browser UI is not desktop-client operation. |
| `Open the dev server page and check its console errors.` | Should prefer `ops-browser`. | Browser-preview behavior without desktop-client proof. |
| `Review current git changes and split commits.` | Should prefer `code-review`. | Dirty-tree review. |
| `Understand this repository's directories and commands first.` | Should prefer `code-context`. | Repository context task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Real window evidence | Confirms process/runtime/window identity and captures by `CGWindowID`. | Uses browser preview or region screenshot as client proof. |
| Runtime source | Distinguishes `pnpm tauri dev`, debug bundle, release app, or reports `Not verified`. | Assumes runtime source without evidence. |
| Launch command | Identifies the client app location and startup command from manifests/docs/scripts or reports `Not found`. | Starts or verifies a client without checking the owning command. |
| Electron boundary | Uses `ops-client` for real Electron runtime/window proof and routes plain web-preview behavior to `ops-browser`. | Treats a browser preview as Electron app evidence. |
| Startup safety | Confirms whether starting or restarting the client could disturb an existing instance, active window, or user workflow. | Restarts the client without checking impact. |
| Background-safe interaction | Uses Accessibility/control-tree paths and avoids stealing mouse/focus where possible. | Coordinate-clicks without checking stable control paths. |
| AI-operable UI | Recommends semantic controls, accessible names, labels, and stable selectors for critical controls. | Leaves icon-only or generic controls unidentified. |
| Restart/rebuild | Re-verifies after relevant UI, bundle, or Accessibility changes. | Claims fix against stale client instance. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
