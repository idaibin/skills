---
name: ops-client
description: "Use when directly operating or verifying a specified real desktop client, or gathering evidence for an isolated client-layer failure; require a verified target, window, and capability, not browser-page verification, source changes, or cross-system diagnosis."
---

# Ops Client

## Overview

Operate and verify real desktop client windows. Treat platform automation as adapter-specific: the current built-in evidence path is macOS-first, while Windows and Linux require an available platform adapter before equivalent claims can be made. Use `dev-frontend` for UI code changes.

## Workflow

1. Identify the specified client target and action scope: app name, known aliases,
   bundle/package identifier, repository path, package/app directory, process, PID,
   visible window, platform, requested evidence, and whether observation, capture,
   launch, restart, focus, or a named semantic interaction is explicitly authorized.
2. Keep application-presence states separate. Record which installation locations or
   registries, process sources, windows, and menu/status surfaces were actually checked.
   Resolve known display-name, bundle-name, helper-process, and executable aliases before
   reporting a match or absence, using only discovery routes allowed by the selected
   adapter. Tool-specific targeting and discovery rules take precedence over generic
   platform suggestions. Use `installed`, `running`, `window observed`, and `menu/status
   item observed` only for the layer directly proved; otherwise say `not found in the
   checked sources` or `Not verified`.
3. Run a capability preflight and record available/unavailable/unknown for:
   - process enumeration and runtime-source inspection;
   - window enumeration with stable window identifiers;
   - window-specific screenshot capture;
   - Accessibility/control-tree inspection and semantic actions;
   - background-safe operation without stealing mouse/focus;
   - an app-owned non-UI control plane such as a documented CLI, authenticated local
     HTTP/socket endpoint, or semantic IPC adapter, including its operation and auth
     boundaries;
   - app launch/restart and permission state;
   - screen-session state as `unlocked`, `locked`, or `unknown`, with the evidence source.
4. Apply the screen-session gate before any window operation. When locked, do not
   unlock or wake the display, focus or activate a window, send keyboard input, move
   the pointer, or click through pointer/coordinate automation. Permit window-level
   capture or inspection only when the selected adapter directly proves that exact
   action is background-safe and does not require those effects; otherwise enter
   Degraded Evidence for the blocked claim. Continue repository, source, process,
   runtime-source, and build verification that does not depend on the screen session.
   Prefer a verified app-owned non-UI control plane for supported state reads or
   explicitly authorized semantic actions. It must not activate a window, synthesize
   GUI input, bypass authentication, or expose a generic command/eval surface. Its
   result is application-control evidence, never real-window or visual evidence.
5. If working from a repository, confirm whether it contains a desktop/client app by checking manifests and source layout such as `src-tauri/`, `tauri.conf.*`, Electron configs, native targets, package scripts, justfile tasks, or README run instructions.
6. Confirm the startup command and runtime source before verification: dev command, debug bundle, release app, Electron/native run command, or `Not found`/`Not verified` when unclear.
7. Select the platform adapter:
   - **macOS:** identify process/PID and matching `CGWindowID`; capture with `screencapture -x -l<CGWindowID>` when available; use macOS Accessibility for semantic controls.
   - **Windows:** require an available UI Automation/window-capture adapter and stable HWND/process evidence; otherwise use Degraded Evidence mode.
   - **Linux:** require an available AT-SPI/window-manager capture adapter and stable window/process evidence; otherwise use Degraded Evidence mode.
8. Identify the exact real window by process owner, PID, title, bounds, and platform identifier. Do not substitute browser preview evidence.
9. Capture and inspect the real window using the selected adapter before making visual claims.
10. Within the explicitly authorized action scope, prefer background-safe Accessibility/control-tree actions on named controls over coordinate clicks. Verification or capture alone never authorizes pressing a control.
11. Classify every interaction result from the tool's explicit terminal evidence:
    `succeeded`, `failed`, `cancelled/not executed`, or `outcome unknown`. A cancelled
    or unexecuted call does not prove that the user denied a permission prompt. Claim
    permission denial only when the tool or platform reports that exact cause. After an
    ambiguous result, inspect the current target state before deciding whether the action
    took effect. If the authorized goal remains incomplete, make at most one bounded,
    low-impact recovery through a verified alternative semantic path. Do not repeat an
    unknown-side-effect action. Continue independently safe checks, and report the exact
    terminal state and unresolved UI state when recovery is unavailable.
12. When rebuild/restart is explicitly authorized for the exact client target, apply
    the startup-safety gate, rebuild/restart after relevant UI, bundle, native, or
    Accessibility changes, and then re-verify. Without that authorization, preserve
    the running client, continue independently safe checks, and report new-build
    runtime verification as `Not verified`.
13. Report unsupported platform claims explicitly rather than emulating them with a browser page or cropped screenshot.
14. Use Client Debug Evidence only when the caller supplies an already-isolated client-layer reproduction whose requested output is direct client evidence. Otherwise route unexplained or cross-system root-cause requests back to the caller for diagnosis before operating the client. For an accepted evidence task, verify the real process/window/build source, collect direct client evidence, clean disposable task state, and return the evidence to the caller.

## Modes

- **Capability Preflight:** verify platform, screen-session state, permissions, process/window enumeration, capture, Accessibility, background-safe behavior, and restart support before operation.
- **Launch Review:** identify the repository-owned client app and startup command before running or verifying it.
- **Window Evidence:** prove process, runtime, real-window identity, platform adapter, and screenshot source.
- **Interaction:** use Accessibility/control-tree paths before coordinate clicks.
- **AI-Operable UI Evidence:** verify semantic controls and stable names so agents can identify critical actions reliably.
- **Locked-session control plane:** use only a documented, authenticated app-owned CLI, local API/socket, or semantic IPC adapter that directly proves operation without waking, focusing, or GUI input. Keep window capture, Accessibility, and visual claims separate.
- **Client Debug Evidence:** only after caller delegation of an already-isolated client-layer evidence request, reproduce on the verified real client instance, capture process/window/build/control evidence, test one client-layer hypothesis at a time, and return evidence to the caller without owning the final cross-system root cause.
- **Degraded Evidence:** when the required platform adapter, permission, or screen-session-safe capability is missing, report only the evidence that can be proven and list exact blocked claims while continuing checks that do not depend on the blocked capability.

## Do Not Use For

- Plain browser pages, web previews, form workflows, downloads, or browser console/network checks; use `ops-browser`.
- Frontend implementation, desktop webview architecture, or IPC layering; use `dev-frontend`. UI specification work belongs to `ui-spec`.
- Ordinary repository discovery unless the user asks for client launch review, real-window verification, or browser-preview invalidation.
- Browser preview evidence when the task requires proof from a Tauri, Electron, or native desktop runtime.
- Repository onboarding or map discovery; use `repo-map`.
- Future implementation planning; use the host's built-in planning.
- Local dirty-tree review or commit readiness; use `repo-review`.
- Review of a fixed desktop-client code change, including IPC authorization risks; use `repo-review`.
- Cross-system root-cause coordination for a frozen, stale, non-responsive, or dev-versus-release failure; use the host's built-in diagnosis, which may delegate real-client evidence collection here.

## Hard Rules

- Do not claim cross-platform support from a macOS-only procedure.
- Treat observation, capture, launch, restart, focus, and control interaction as separate scopes. A verification request does not authorize launch, restart, focus change, or pressing controls; require an exact target and action before changing client state.
- Stop before credentials, account switching, permission grants, destructive or irreversible actions, purchases, or external submission unless the user explicitly authorizes that exact action and target.
- Do not treat browser previews, dev server pages, region screenshots, or app-like web tabs as desktop-client evidence unless the user explicitly asks for browser-only checking.
- Do not start or restart a client before confirming the startup command source and whether it could disturb an existing app instance, active window, unsaved state, or user workflow.
- Do not assume Accessibility or screen-capture permission. Verify the action succeeds or mark it unavailable.
- Do not translate `cancelled`, `not executed`, transport interruption, or an unknown
  terminal result into `permission denied` or `user rejected`. Preserve the tool's exact
  result unless direct evidence establishes the cause.
- Do not stop and ask the user to perform a routine reversible recovery while the
  existing authorization still covers a verified safe path. Revalidate state, try one
  bounded alternative when available, and stop only when the remaining path is unsafe,
  consequential, unsupported, or outside scope.
- Never unlock the screen, wake the display, focus or activate a window, send keyboard input, move the pointer, or perform pointer/coordinate clicks while the screen session is `locked`. Treat `unknown` as insufficient authorization for an action that could require any of those effects.
- A window identifier or capture API name alone does not prove lock-safe behavior. Require direct adapter evidence that the exact capture/read action remains background-safe in the current screen-session state, or use Degraded Evidence.
- A running process or local port does not prove an app-owned control plane. Require
  repository/runtime ownership, documented operations, authentication or same-user
  access control, and a bounded semantic command set. Never add or use a generic shell,
  JavaScript eval, SQL, or unrestricted IPC endpoint to bypass the lock screen.
- Do not steal the user's mouse, move the pointer, activate unrelated windows, or coordinate-click unless no stable control path exists, the target window is revalidated, and the risk is acceptable.
- Prefer semantic controls, accessible names, labels, roles, stable automation identifiers, and repository-supported test ids for critical controls.
- On macOS, verify `CGWindowID`, owner/PID/title/bounds, and capture result before calling a screenshot real-window evidence.
- On Windows or Linux, require the platform adapter's stable window/process identifier and capture provenance; do not reuse macOS terminology or commands.
- If only a process can be proven, do not infer that the requested window is visible, current, or running the new build.
- Absence from a running-process list proves only that no matching process was observed.
  Absence from a menu bar, status area, Dock, taskbar, or window inventory proves only
  absence from that inspected surface. Do not conclude that an app is uninstalled until
  the platform's relevant installation sources have been checked under resolved aliases;
  even then report the checked scope instead of a universal machine-wide absence.
- When a client-operation adapter requires the user-supplied app name to be attempted
  first, follow that contract. Do not open Finder, Spotlight, or another GUI search as an
  alias-resolution workaround. Adapter-provided inventory may supply one documented
  bundle/package retry after the named attempt fails. An independently authorized
  read-only installation audit may inspect platform inventory outside the UI adapter,
  but report it as separate system evidence and never as proof that the adapter targeted
  or opened the app.
- For code changes that add accessibility or automation surfaces, use `dev-frontend` or the relevant native implementation skill; return here for runtime verification.
- Re-verify the target process, runtime source, and window after rebuild/restart; stale windows do not prove current code.
- Confirm only direct client facts. Do not claim a final cause across frontend, IPC, Rust, database, packaging, or platform layers, and do not decide a permanent fix; return the evidence to the caller.
- Remove disposable task state such as temporary probes, injected instrumentation, test windows, and launched test instances when safe. Retain screenshots, logs, traces, and other handoff evidence until they are embedded, archived, or explicitly accepted by the handoff owner; report retained artifact paths/identifiers, embedded evidence, removed disposable state, and anything left running.
- Say `Not supported` when no adapter exists for the requested platform capability and `Not verified` when the adapter exists but the check was not completed.
- Report whether the screen session is a `confirmed blocker`, `possible blocker`, `not a blocker`, or `Not verified`. Claim `confirmed blocker` only when direct platform/adapter evidence attributes the requested capability failure to the locked session; do not infer causality merely because the screen is locked.

## Output Contract

Report platform and selected adapter, screen-session state and evidence source, screen-session impact classification, capability preflight, specified client target and resolved aliases, authorized action scope, checked installation/process/window/menu sources, repository/client ownership evidence, startup command or `Not found`, target process/runtime, stable real-window identity, screenshot source/provenance, interaction method, exact interaction terminal state and bounded recovery, Client Debug Evidence and handoff owner when relevant, permission or adapter gaps, unaffected checks that continued, restart/rebuild status, cleanup status, and all `Not supported` or `Not verified` claims.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
