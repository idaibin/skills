# Physical Devices

## Android

For Android screen/app-store handoffs and bounded device plans, read
[phone debugging](phone-debugging.md) and the [Android runner](android-debug-runner.md).
Keep browser-page acceptance with the browser owner; these provide device evidence.

Enumerate connected Android targets and bind the requested physical device by its
current ADB serial plus package identity. The Android documentation requires a
specific target when multiple devices are connected; use `adb -s "$task_serial"`
for every command, including inspect, input, capture and pull. Do not use `-d` or a
remembered first device as an ownership shortcut. A connected phone may be locked,
unauthorized for debugging, on a different network, or running a different build;
check each condition only when it matters to the requested operation. `adb devices`
alone proves none of them.

Reuse the operation loop in [usage](usage.md). Install, grant permissions, change
network settings, clear app data, unlock the guest or enter credentials only within
their specific authority. Check the installed package/version/signature and backend
environment before a feature claim. Re-read the current UI or app state after each
bounded action; a successful transport call is not business acceptance.

## iOS and iPadOS

Distinguish a paired physical device from a Simulator. Bind the exact device ID/UDID,
bundle ID, signing/deployment target and installed build through the supported
current Xcode/device or test adapter. Inspect current tool help and device trust,
pairing and developer-mode requirements rather than assuming Android ADB semantics.
If a required physical-device adapter or pairing is absent, report that physical
operation `Not verified`; a Simulator pass is a separate result.

Capture and UI automation depend on the actual device, OS, app permissions and
adapter. Use the app's or platform's supported semantic/test route when available;
choose native computer interaction only when it directly binds the requested device
and can verify the result. Never infer that Simulator screenshots, gestures or
permissions behave identically on hardware.

## Evidence boundary

Return the exact device, app and build, before/after guest state, adapter result,
decoded capture or test assertion, and the scope of physical-device coverage.
The host's unlocked screen, a device listing, and a tool's claimed platform support
do not verify a phone flow.

Official references: [Android Debug Bridge](https://developer.android.com/tools/adb),
[running on simulated or physical Apple devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices),
[XCTest](https://developer.apple.com/documentation/xctest).
