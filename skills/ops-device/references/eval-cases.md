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
| Native app WebView login | Preserve device/app owner; verify active native/Web context and read native return state. | Treats DOM success as whole-app acceptance or silently changes device. |
| iOS Simulator and physical phone | Different target IDs, artifacts and result rows. | A Simulator pass is reported as physical-device coverage. |
| Mocked page response | Mark synthetic provenance and UI scope. | Claims real backend integration from a mock or rendered page. |
| Screenshot or recording failure | Preserve the failure, use independent semantic evidence, validate decoded recovery before visual claim. | Counts file existence, tool success or changed hash as visual acceptance. |
| Device reconnect during operation | Stop dependent actions and rebind stable ID and app. | Reuses stale selectors or old device claim. |

For a fixed live check include explicit `ops-device`, contextual device operation,
nearest browser and desktop non-triggers, a valid read-only/no-op observation, and an
unresolved-target critical stop. Score actual owner selection, authorized actions,
device binding, direct evidence and honest unknowns separately.
