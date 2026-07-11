---
name: ops-client
description: Use when operating or verifying a specified real desktop client window, proving Tauri/Electron/native runtime source, reviewing launch commands, capturing platform-specific window evidence, or validating AI-operable desktop controls.
---

# Ops Client

## Overview

Operate and verify real desktop client windows. Treat platform automation as adapter-specific: the current built-in evidence path is macOS-first, while Windows and Linux require an available platform adapter before equivalent claims can be made. Use `implement-frontend` for UI code changes.

## Workflow

1. Identify the specified client target: app name, repository path, package/app directory, process, PID, visible window, platform, and requested evidence.
2. Run a capability preflight and record available/unavailable/unknown for:
   - process enumeration and runtime-source inspection;
   - window enumeration with stable window identifiers;
   - window-specific screenshot capture;
   - Accessibility/control-tree inspection and semantic actions;
   - background-safe operation without stealing mouse/focus;
   - app launch/restart and permission state.
3. If working from a repository, confirm whether it contains a desktop/client app by checking manifests and source layout such as `src-tauri/`, `tauri.conf.*`, Electron configs, native targets, package scripts, justfile tasks, or README run instructions.
4. Confirm the startup command and runtime source before verification: dev command, debug bundle, release app, Electron/native run command, or `Not found`/`Not verified` when unclear.
5. Select the platform adapter:
   - **macOS:** identify process/PID and matching `CGWindowID`; capture with `screencapture -x -l<CGWindowID>` when available; use macOS Accessibility for semantic controls.
   - **Windows:** require an available UI Automation/window-capture adapter and stable HWND/process evidence; otherwise use Degraded Evidence mode.
   - **Linux:** require an available AT-SPI/window-manager capture adapter and stable window/process evidence; otherwise use Degraded Evidence mode.
6. Identify the exact real window by process owner, PID, title, bounds, and platform identifier. Do not substitute browser preview evidence.
7. Capture and inspect the real window using the selected adapter before making visual claims.
8. Prefer background-safe Accessibility/control-tree actions on named controls over coordinate clicks.
9. Rebuild/restart the intended client instance after relevant UI, bundle, native, or Accessibility changes before re-verifying.
10. Report unsupported platform claims explicitly rather than emulating them with a browser page or cropped screenshot.

## Modes

- **Capability Preflight:** verify platform, permissions, process/window enumeration, capture, Accessibility, and restart support before operation.
- **Launch Review:** identify the repository-owned client app and startup command before running or verifying it.
- **Window Evidence:** prove process, runtime, real-window identity, platform adapter, and screenshot source.
- **Interaction:** use Accessibility/control-tree paths before coordinate clicks.
- **AI-Operable UI Evidence:** verify semantic controls and stable names so agents can identify critical actions reliably.
- **Degraded Evidence:** when the required platform adapter or permission is missing, report only process/repository evidence that can be proven and list exact blocked claims.

## Do Not Use For

- Plain browser pages, web previews, form workflows, downloads, or browser console/network checks; use `ops-browser`.
- Frontend implementation, desktop webview architecture, IPC layering, or design-system work; use `implement-frontend`.
- Ordinary repository discovery unless the user asks for client launch review, real-window verification, or browser-preview invalidation.
- Browser preview evidence when the task requires proof from a Tauri, Electron, or native desktop runtime.
- Local diff review, planning, or security-only review; use the relevant `code-*` skill.

## Hard Rules

- Do not claim cross-platform support from a macOS-only procedure.
- Do not treat browser previews, dev server pages, region screenshots, or app-like web tabs as desktop-client evidence unless the user explicitly asks for browser-only checking.
- Do not start or restart a client before confirming the startup command source and whether it could disturb an existing app instance, active window, unsaved state, or user workflow.
- Do not assume Accessibility or screen-capture permission. Verify the action succeeds or mark it unavailable.
- Do not steal the user's mouse, move the pointer, activate unrelated windows, or coordinate-click unless no stable control path exists, the target window is revalidated, and the risk is acceptable.
- Prefer semantic controls, accessible names, labels, roles, stable automation identifiers, and repository-supported test ids for critical controls.
- On macOS, verify `CGWindowID`, owner/PID/title/bounds, and capture result before calling a screenshot real-window evidence.
- On Windows or Linux, require the platform adapter's stable window/process identifier and capture provenance; do not reuse macOS terminology or commands.
- If only a process can be proven, do not infer that the requested window is visible, current, or running the new build.
- For code changes that add accessibility or automation surfaces, use `implement-frontend` or the relevant native implementation skill; return here for runtime verification.
- Re-verify the target process, runtime source, and window after rebuild/restart; stale windows do not prove current code.
- Say `Not supported` when no adapter exists for the requested platform capability and `Not verified` when the adapter exists but the check was not completed.

## Output Contract

Report platform and selected adapter, capability preflight, specified client target, repository/client ownership evidence, startup command or `Not found`, target process/runtime, stable real-window identity, screenshot source/provenance, interaction method, permission or adapter gaps, restart/rebuild status, and all `Not supported` or `Not verified` claims.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move platform-specific procedures to `references/` when they grow, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
