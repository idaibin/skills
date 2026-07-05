# Ops Client Usage

## Summary

Use `ops-client` for real desktop client operation and verification. It is currently Tauri-focused, but it also applies to Electron and native shells when real app-window evidence matters. Use `frontend-implementation` for desktop webview code changes.

## Trigger Examples

- `Verify the real Tauri client window; do not use a browser preview.`
- `Operate this specified client, but confirm the launch command first.`
- `Check whether this repository contains a Tauri/Electron client and its launch command before verifying the app.`
- `Capture the real app window with CGWindowID.`
- `Confirm the visible Electron release app, not just the web preview.`
- `Press this client button with AXPress without stealing the mouse.`
- `Confirm whether the running app came from pnpm tauri dev or the release app.`
- `Verify whether this Tauri/client control is identifiable through DOM or Accessibility labels.`

## Non-Triggers

- Browser-only page inspection, form filling, upload/download, or console/network debugging; use `ops-browser`.
- Desktop webview code implementation, IPC layering, or component refactors; use `frontend-implementation`.
- Generic repository context discovery without client launch review or real-window verification; use `code-context`.
- Dirty-tree review or commit planning; use `code-review`.

## Operation Notes

- Process and runtime source are part of the evidence, not optional setup.
- When the task starts from a repository, identify the client app location and startup command before claiming verification.
- Before starting or restarting the client, confirm the command source and whether it may disturb an existing instance or active user workflow.
- Prefer `screencapture -x -l<CGWindowID>` over region capture.
- Prefer Accessibility actions on named controls over pointer movement or coordinate clicks.
- Treat multiple app instances and stale bundles as common failure modes.
- For Tauri webviews, make controls semantic and discoverable through DOM and Accessibility surfaces.
- For code edits that add semantic controls, labels, or stable selectors, use `frontend-implementation`; then return here for real-window proof.
- For Electron apps, first prove the real desktop runtime/window when the task asks for client evidence; use browser tooling only for plain web-preview behavior or after the real app identity is established.
