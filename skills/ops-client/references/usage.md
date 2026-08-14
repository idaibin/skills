# Ops Client Usage

## Contents

- [Summary](#summary)
- [Trigger Examples](#trigger-examples)
- [Non-Triggers](#non-triggers)
- [Operation Notes](#operation-notes)
- [Screen-Session Gate](#screen-session-gate)
- [macOS Adapter](#macos-adapter)
- [Windows Adapter](#windows-adapter)
- [Linux Adapter](#linux-adapter)
- [Adapter Fallback](#adapter-fallback)

## Summary

Use `ops-client` for real desktop client operation, verification, and bounded Client Debug Evidence. It is currently Tauri-focused, but it also applies to Electron and native shells when real app-window evidence matters. Use the host's built-in diagnosis for cross-system root-cause coordination and `dev-frontend` for desktop webview code changes.

## Trigger Examples

- `Verify the real Tauri client window; do not use a browser preview.`
- `Operate this specified client, but confirm the platform and launch command first.`
- `Check whether this repository contains a Tauri/Electron client and its launch command before verifying the app.`
- `On macOS, capture the real app window with CGWindowID.`
- `On Windows, verify this Electron window through an available UI Automation/HWND adapter.`
- `On Linux, verify this client through an available AT-SPI/window-manager adapter.`
- `Confirm the visible Electron release app, not just the web preview.`
- `On macOS, press this client button with AXPress without stealing the mouse.`
- `Confirm whether the running app came from npm run tauri dev or the release app.`
- `Verify whether this Tauri/client control is identifiable through DOM or Accessibility labels.`
- `The desktop may be locked. Verify what you can without unlocking, waking, focusing, typing, or moving the pointer.`

## Non-Triggers

- Browser-only page inspection, form filling, upload/download, or console/network debugging; use `ops-browser`.
- Desktop webview code implementation, IPC layering, or component refactors; use `dev-frontend`.
- Generic repository map discovery without client launch review or real-window verification; use `repo-map`.
- Dirty-tree review or commit planning; use `repo-review`.
- Root-cause coordination for unexplained client failures; use the host's built-in diagnosis, which may delegate real-client reproduction and evidence collection here.

## Operation Notes

- Process and runtime source are part of the evidence, not optional setup.
- When the task starts from a repository, identify the client app location and startup command before claiming verification.
- Before starting or restarting the client, require explicit authorization for the
  exact target and action, then confirm the command source and whether it may disturb
  an existing instance or active user workflow. Relevant source changes alone do not
  authorize rebuild or restart.
- Treat multiple app instances and stale bundles as common failure modes.
- For Tauri webviews, make controls semantic and discoverable through DOM and Accessibility surfaces.
- For code edits that add semantic controls, labels, or stable selectors, use `dev-frontend`; then return here for real-window proof.
- For Electron apps, first prove the real desktop runtime/window when the task asks for client evidence; use browser tooling only for plain web-preview behavior or after the real app identity is established.
- Enter Client Debug Evidence only after the caller supplies an already-isolated client-layer evidence request. Otherwise route unexplained failures back to the caller for diagnosis before client operation. Reproduce only on the verified target process/window/build, return direct evidence, remove disposable probes and launched test instances, and retain referenced screenshots/logs/traces until embedded, archived, or accepted by the handoff owner. Do not infer a final cause across frontend, IPC, Rust, database, packaging, or platform layers.

## Screen-Session Gate

Record `screen_session` as `unlocked`, `locked`, or `unknown` from a direct
platform or adapter signal. App visibility, an existing window identifier, and a
previously successful capture do not establish the current screen-session state.

When `locked`, do not unlock or wake the display, activate or focus an app, send
keyboard input, move the pointer, or use pointer/coordinate clicks. A window-level
capture or read may proceed only when the adapter directly proves that the exact
operation is background-safe in the current locked session. If that property cannot
be proven, leave the visual, Accessibility, or interaction claim in Degraded Evidence.
Apply the same restraint to `unknown` whenever an operation could require a prohibited
effect.

For application state or semantic actions, prefer an app-owned non-UI control plane
that was documented by the owning repository and can be attributed to the running
client: a bounded CLI, authenticated same-user local HTTP/socket endpoint, or semantic
IPC adapter. Verify its process/runtime ownership, supported operation, authentication
boundary, before/after result, and cleanup. Do not use AppleScript GUI scripting,
Accessibility actions, keyboard events, pointer events, a generic eval endpoint, or an
unrestricted command bridge as a lock-screen workaround. Control-plane success proves
only the application operation; it does not prove a visible window or current pixels.

Classify lock impact separately from state:

- `confirmed blocker`: direct platform or adapter evidence attributes the required
  capability failure to the locked session;
- `possible blocker`: the session is locked or unknown, but evidence does not isolate
  the failure to the session state;
- `not a blocker`: the requested action succeeds through a proven lock-safe path, or
  the failure has an independently established cause;
- `Not verified`: neither the session state nor its effect was established.

Do not stop unrelated work merely because window evidence is degraded. Continue
repository ownership, source/configuration inspection, process enumeration,
runtime-source checks, and build/static verification when each is independently safe
and authorized. Report those results separately from blocked real-window claims.

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
