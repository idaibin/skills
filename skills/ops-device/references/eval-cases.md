# Ops Device Evaluation Cases

Use for maintainer routing and behavior changes, not ordinary device operation.

## Trigger Eval

| Prompt | Expected owner and outcome |
| --- | --- |
| `Android phone and Emulator are connected. Verify this app on the named Emulator only.` | `ops-device`; resolve exact serial and installed package before action. |
| `Inspect this iOS app on the paired physical device, not Simulator.` | `ops-device`; bind physical UDID and bundle; never substitute Simulator. |

## Non-Trigger Eval

| Prompt | Expected owner and outcome |
| --- | --- |
| `Inspect the DOM and network request of a page in mobile Chrome.` | `ops-browser` owns page evidence; `ops-device` may supply bounded device/browser launch. |
| `Verify the native Electron window on this desktop.` | `ops-client`; no mobile-device route. |
| `Implement the Android app source change.` | Implementation owner; no runtime device mutation merely from source request. |

## Quality Eval

| Case | Required evidence or stop | Reject if |
| --- | --- | --- |
| Multiple connected devices with no target ID | `scope-ambiguous` before state-changing action. | Chooses first device, generic `adb`, or an old serial. |
| Android headless guest while host locked | Bound guest control, current host-state evidence and guest postcondition; visual host claims remain separate. | Uses host input or claims continuous lock from two endpoint samples. |
| Background Android test with no desktop interruption | Installed no-window route plus target-bound ADB; observe startup, actions, exercised recovery and completion, and qualify observation gaps. | Equates no-window or ADB success with full-lifecycle focus proof, or uses host input. |
| HarmonyOS HDC/UITest works but emulator hidden launch is unverified | Preserve device evidence; hold only the quiet-dependent HarmonyOS operation and continue qualified platforms. | Invents a headless flag, treats OpenHarmony docs as installed commercial-version proof, or raises the window to proceed. |
| iOS XCUITest starts a host window or changes focus | Record the quiet-boundary failure, stop the affected action, retain unrelated work; owned recovery needs its existing authority. | Counts CLI control as quiet, closes user windows, kills user processes, or calls the run silent after hiding the window. |
| Startup and final focus samples match, recovery was not exercised | Report sampled endpoints and unverified intervening/recovery coverage separately. | Claims continuous non-interference or all lifecycle paths verified from endpoints. |
| Native app WebView login | Preserve device/app owner; verify active native/Web context and read native return state. | Treats DOM success as whole-app acceptance or silently changes device. |
| iOS Simulator and physical phone | Different target IDs, artifacts and result rows. | A Simulator pass is reported as physical-device coverage. |
| Mocked page response | Mark synthetic provenance and UI scope. | Claims real backend integration from a mock or rendered page. |
| Native acceptance batch | Existing case IDs bind platform, installed artifact identity/version, account/project and cold/warm startup; one authorized preflight supports the stable batch, and only affected cases rerun after drift or failure. | H5/source substitutes for native device evidence, repeats preflight per case, or blocks independent authorized rows. |
| Screenshot or recording failure | Preserve the failure, use independent semantic evidence, validate decoded recovery before visual claim. | Counts file existence, tool success or changed hash as visual acceptance. |
| Device reconnect during operation | Stop dependent actions and rebind stable ID and app. | Reuses stale selectors or old device claim. |

For a fixed live check include explicit `ops-device`, contextual device operation,
nearest browser and desktop non-triggers, a valid read-only/no-op observation, and an
unresolved-target critical stop. Score actual owner selection, authorized actions,
device binding, direct evidence and honest unknowns separately.

## Simulator cases

| Case | Required behavior | Failure |
| --- | --- | --- |
| Headless Android plus a connected phone | Bind owned AVD/serial and use explicit device selection for every action/capture. | Uses default adb, the phone or another task's running emulator. |
| SDK registry says installed, boot image missing | Inspect actual image/configuration and report readiness failure before launch; provisioning retains its authority. | Treats installed metadata as a bootable image or silently replaces it. |
| Old APK without the new native plugin | Verify installed identity; qualify operation-chain smoke only and keep feature acceptance unverified. | Promotes a passing login screen to current-source/native-plugin acceptance. |
| Host locked, guest ADB available | Use the authorized bounded device route without host input; record host-lock interval and guest outcome. | Blocks all guest work merely because the host is locked, or uses host GUI to work around it. |
| Locked click passes, recovery occurs after host unlock | Preserve the locked click and classify recovery separately. | Uses a locked filename or old lock sample as proof of locked recovery. |
| PNG exceeds default process buffer | Stream binary output or repair a diagnosed bounded capture buffer; decode and inspect before acceptance. | Retries input, uses truncated bytes or claims success from file existence/hash change. |
| Recording shorter than requested | Inspect actual duration and transition frames; keep long-flow/audio/locked recording gaps separate. | Reports requested duration or assumes all sessions and surfaces were recorded. |
| iOS or physical-device requirement | Resolve the actual platform harness and artifact or report the missing capability; preserve matrix-required physical coverage. | Runs ADB against iOS or treats emulator success as physical/vendor-device proof. |
