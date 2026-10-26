---
name: ops-device
description: "Operate and verify a specified mobile physical device, emulator, or simulator and its installed app; use ops-browser for browser-page evidence."
---

# Device Operations

## Entry Gate

Use this Skill when the requested result depends on a mobile device, its guest OS,
installed app, permissions, lifecycle, or device-scoped capture. Bind the exact device
and app before changing state. A device listing, visible simulator window, or available
tool does not establish task ownership, authorization, or app acceptance.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any mobile device operation | [usage](references/usage.md) | Target, authority, capability and evidence boundary |
| Android Emulator or other virtual device | [simulator operations](references/simulator-operations.md) | Guest-bound controls and qualified host/guest result |
| Physical Android or iOS device | [physical devices](references/physical-devices.md) | Bound device/app operation with direct postcondition |
| App WebView or mobile browser crosses native/Web context | [hybrid surfaces](references/hybrid-surfaces.md) | Stable owner and explicit context handoff |

## Invariants

- Choose the owner from the result being verified, then choose an available authorized
  tool that can produce that evidence. Codex native computer controls, a device MCP,
  CLI, ADB, and a platform test harness are possible adapters, not permanent Skill
  boundaries. Preflight the actual adapter and its target support.
- Pin the device identifier and app/package identity for every state-changing or
  capture operation. Rebind after reconnect, restart, context switch, or identity
  drift. Stop a dependent operation when more than one target remains plausible.
- Observe current state, perform only the authorized action, and read back its
  postcondition. Keep device state, app state, UI, network, mock, screenshot and
  recording evidence separate; unavailable capture blocks only visual claims.
- Device control does not grant browser-session control, source edits, installation,
  account changes, external writes, or destructive cleanup. Route browser-page
  inspection to `ops-browser` with the bound device context; preserve this Skill's
  ownership of app container, device and guest state.

## Output Map

Return device kind and stable ID, OS/runtime and installed app identity, selected
adapter and supported actions, authorized effects, direct before/after evidence,
capture validity, cleanup ownership, and each `Not verified` claim. Distinguish
simulator from physical-device and host state from guest state.

## Reference Map

- Read [usage](references/usage.md) for target resolution, effects, evidence and
  routing. Read [simulator operations](references/simulator-operations.md) only for
  virtual-device setup, operation, headless/lock checks or recording.
- Read [physical devices](references/physical-devices.md) for connected-phone
  targeting, platform preflight and device-specific effects.
- Read [hybrid surfaces](references/hybrid-surfaces.md) for mobile browser, WebView,
  context switching and network evidence.
- Maintainers only: read [eval cases](references/eval-cases.md) when changing routing
  or behavior; do not load it during ordinary operation.
