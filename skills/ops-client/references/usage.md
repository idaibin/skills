# Ops Client Usage

## Summary

Use `ops-client` for real desktop client operation and verification. It is currently Tauri-focused, but it also applies to Electron and native shells when real app-window evidence matters. Use `implement-frontend` for desktop webview code changes.

## Trigger Examples

- `Verify the real Tauri client window; do not use a browser preview.`
- `Operate this specified client, but confirm the platform and launch command first.`
- `Check whether this repository contains a Tauri/Electron client and its launch command before verifying the app.`
- `On macOS, capture the real app window with CGWindowID.`
- `On Windows, verify this Electron window through an available UI Automation/HWND adapter.`
- `On Linux, verify this client through an available AT-SPI/window-manager adapter.`
- `Confirm the visible Electron release app, not just the web preview.`
- `On macOS, press this client button with AXPress without stealing the mouse.`
- `Confirm whether the running app came from pnpm tauri dev or the release app.`
- `Verify whether this Tauri/client control is identifiable through DOM or Accessibility labels.`

## Non-Triggers

- Browser-only page inspection, form filling, upload/download, or console/network debugging; use `ops-browser`.
- Desktop webview code implementation, IPC layering, or component refactors; use `implement-frontend`.
- Generic repository context discovery without client launch review or real-window verification; use `code-context`.
- Dirty-tree review or commit planning; use `code-review`.

## Operation Notes

- Process and runtime source are part of the evidence, not optional setup.
- When the task starts from a repository, identify the client app location and startup command before claiming verification.
- Before starting or restarting the client, confirm the command source and whether it may disturb an existing instance or active user workflow.
- Treat multiple app instances and stale bundles as common failure modes.
- For Tauri webviews, make controls semantic and discoverable through DOM and Accessibility surfaces.
- For code edits that add semantic controls, labels, or stable selectors, use `implement-frontend`; then return here for real-window proof.
- For Electron apps, first prove the real desktop runtime/window when the task asks for client evidence; use browser tooling only for plain web-preview behavior or after the real app identity is established.

## macOS Adapter

Use only on macOS and only when the commands/APIs are exposed and permissions succeed:

- identify the target with process owner, PID, title, bounds, and `CGWindowID`;
- prefer `screencapture -x -l<CGWindowID>` over region capture;
- prefer macOS Accessibility actions such as `AXPress` on named controls over pointer movement or coordinate clicks;
- verify screen-recording and Accessibility permission through successful actions, not app visibility alone.

Do not reuse `CGWindowID`, `screencapture`, `AXPress`, or macOS Accessibility
terminology for Windows or Linux evidence.

## Windows Adapter

Require an available Windows UI Automation/window-capture adapter. Identify the
target through process/PID plus stable HWND or adapter-provided window identity,
capture provenance, and UI Automation control evidence. If the environment does
not expose such an adapter, report the requested window capture or interaction as
`Not supported`; process or repository evidence may still be reported separately.

## Linux Adapter

Require an available AT-SPI and window-manager capture adapter. Identify the
target through process/PID plus the adapter's stable window identity, capture
provenance, and accessible control evidence. If the environment does not expose
such an adapter, report the requested window capture or interaction as `Not supported`;
process or repository evidence may still be reported separately.

## Adapter Fallback

Do not substitute browser previews, cropped screen regions, or another platform's
commands for a missing adapter. Use `Not supported` when no suitable adapter
exists and `Not verified` only when the adapter exists but the requested check
was not completed.
