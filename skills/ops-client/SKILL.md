---
name: ops-client
description: "Operate desktop clients and mobile apps in emulators or simulators; capture runtime evidence within task authority."
---

# Client Operations

## Entry Gate

Operate a named desktop client only after confirming target process/window/build, adapter capability, screen-session state, foreground constraints, allowed side effects, and evidence boundary. Installation, process, window, menu, and runtime behavior are separate claims.
For an emulator-hosted app, bind the virtual device, guest OS and installed artifact
instead of requiring a host window; keep guest controls and host desktop state separate.

Reuse existing task authority for requested local client acceptance. An implementation
handoff does not require renewed approval; installs, account changes, external writes,
and destructive actions still require their own applicable authority.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Launch/inspect/interact/capture a client | [usage](references/usage.md) | Verified client-layer evidence or safe stop |
| Background or focus-preserving operation, including capability qualification | [background operations](references/background-operations.md), plus the applicable platform in usage | Per-operation capability, result, non-interference and cleanup evidence |
| Mobile app in Android Emulator or another simulator | [simulator operations](references/simulator-operations.md) | Device-bound interaction, capture, recording and qualified host-lock evidence |
| Need examples/edge cases | [usage](references/usage.md) | Correct mode/boundary |

## Invariants

- Do not substitute browser, build, process, or menu evidence for real native-window acceptance.
- Verify project navigation, text entry, submission and capture as separate requested operations. A failed capture blocks visual acceptance, while independently authorized semantic controls remain eligible for verification. Confirm navigation through application state such as a selected-project menu mark; require accepted text before testing submission.
- A named-app interaction authorizes the requested in-app action and its ordinary window activation; do not ask again solely because semantic targeting may focus it. Preserve an explicit foreground-app constraint, and stop without reclaiming focus if the user changes the active app. Launch, restart, another app, or broader input need their own authority.
- Background operation bypasses focus-dependent input. A writable attribute, advertised action, permission preflight or successful API return is not proof of application acceptance or uninterrupted foreground continuity. Never silently fall back to activation, global input or clipboard paste.
- Emulator guest input is device-scoped, not host desktop input. Pin the exact virtual device for every command; never select a connected physical device or change another task's emulator implicitly. A passing old APK cannot verify current source or a missing native plugin.
- Attempt the user-named app before aliasing; report checked sources rather than declaring machine-wide absence.
- Keep diagnostics, source fixes, browser behavior, and Git mutation with their owners; clean disposable probes.

## Output Map

Return app/process/window/build identity, authorized actions, direct evidence, cleanup, and `Not verified` claims.
For background work, separate capability discovery, actual state change, foreground/input continuity, capture and restoration; report each requested operation at the level directly observed.
For simulator work, include device/image/ABI, installed package identity, guest state,
host lock/sleep evidence, capture/recording validation and retention ownership.

## Reference Map

- Read [usage](references/usage.md) for client modes, targeting, safety, evidence, and stop conditions.
- Read [background operations](references/background-operations.md) when the user requires background execution or asks to qualify a focus-preserving route.
- Read [simulator operations](references/simulator-operations.md) for mobile apps running inside Android Emulator or another simulator, including headless and host-lock checks.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
