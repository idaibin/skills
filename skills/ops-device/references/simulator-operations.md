# Simulator Operations

Use for mobile apps inside an emulator or simulator. Select the guest-device control
channel before desktop-window automation. Android Emulator headless mode uses the
official emulator with no host window and ADB for guest operations; it is not a
separate product or proof of physical-device, vendor-ROM or long-duration coverage.

## Contents

- [Target and authority](#target-and-authority)
- [Android readiness and artifact identity](#android-readiness-and-artifact-identity)
- [Background and focus contract](#background-and-focus-contract)
- [Device operation loop](#device-operation-loop)
- [Host lock and sleep](#host-lock-and-sleep)
- [Recording](#recording)
- [Storage and lifecycle](#storage-and-lifecycle)
- [Other simulators and handoff](#other-simulators-and-handoff)
- [iOS Simulator](#ios-simulator)

## Target and authority

Resolve the SDK/tool executable and version, host architecture, AVD name, emulator
process/port, exact ADB serial, Android API/image variant/ABI and device state.
Inventory connected devices before mutation. Use `adb -s "$task_serial"` for every
targeted operation, including capture, pull and shutdown. Never use the first device,
an unqualified `adb`, or `-e` when multiple emulators could match. A remembered serial
or port is not ownership proof; rebind after restart, reconnect or target drift.

A linked conversation supplies evidence to inspect, not permission to operate its
device. Reuse only a currently authorized task-owned device. Provisioning SDKs,
accepting licenses, creating/starting/replacing AVDs, installing APKs, changing accounts,
locking the host and deleting device data each retain their applicable authority.
Do not reuse a phone, stop another emulator, run `adb kill-server`, wipe data or change
shared images merely to unblock this task. Existing authorization for the exact
operation remains valid; do not ask again at a skill handoff.

## Android readiness and artifact identity

Check the current tool's help and the project's supported runtime before using flags.
List AVDs and inspect actual image/configuration files: an SDK installed-package entry
does not prove that `system.img`, boot files or the configured image path exist.
Match host acceleration, image ABI, APK native libraries and supported API levels.
Choose AOSP, Google APIs or Play images from the feature's actual dependencies and
user preference, not a fixed "latest" label; recheck official availability when changing
versions. Do not silently replace the selected Android version or image family.

When launch is authorized, use a task-owned AVD with a non-conflicting port and
documented `-no-window` behavior. Select audio, snapshot, GPU, CPU, memory, resolution
and density only when supported and needed; do not copy another run's flags or sizes.
Bound startup by a deadline. A process or `adb wait-for-device` is insufficient:
require the intended serial online, boot completion and a usable guest state.

Before installation, inspect the actual APK hash, package/version, signing identity,
ABI, minimum/target SDK and relevant endpoint/environment. For split packages or
resource updates, verify the complete accepted artifact set and its native base.
Install only the authorized artifact on the bound device, then read installed package
identity back. Keep source commit, APK/WGT contents, native plugins and installed
runtime as separate facts. An older APK may prove the operation chain but not a new
feature; an absent plugin or unavailable account keeps its acceptance unverified.
Builds belong to separately authorized artifact production, not an implicit test step.

## Background and focus contract

When background-only testing is requested, distinguish three independent claims:
no emulator window is shown, device actions do not use host mouse/keyboard input,
and the complete observed lifecycle preserves the user's foreground and focus.
A CLI, guest screenshot, hidden window or successful test alone proves none of the
other claims. Apply the quiet constraint before launch, not only after boot.

Bind the host/tool version and task-owned device, then qualify each platform route:

- Android: use the installed tool's documented no-window mode with target-bound ADB.
  The official `emulator -no-window` option disables its graphical display; it is not
  an assurance about IDE launchers, prompts or host focus. Check current tool help;
  do not assume legacy flags transfer to a newer launcher or upgrade tools implicitly.
- HarmonyOS: resolve the actual DevEco/emulator, HDC and UITest versions and exact
  target. Device-bound HDC/UITest operations do not establish that startup or recovery
  hides the host emulator window. OpenHarmony command documentation is not evidence
  for every commercial HarmonyOS build. Keep full quiet operation unverified until
  this installed route is observed; do not invent a headless flag.
- iOS: use the bound Simulator UDID and supported simctl/XCTest/XCUITest route, not
  host cursor or keyboard events. CLI test execution does not guarantee that boot,
  test-runner launch, dialogs or recovery preserve host focus. Verify this Xcode and
  runtime combination; do not open or activate Simulator.app merely to make it work.

Check and retain time-bound host window/foreground/focus evidence alongside guest
results at startup, normal execution, any exercised failure/recovery, and completion
or owned cleanup. Prefer non-interfering observation; do not steal focus to measure
it. Record observer coverage: endpoint snapshots do not prove an uninterrupted
interval, and an unexercised recovery path remains unverified. Launch configuration,
commands and versions must be bound to the same lifecycle evidence. Missing safe
observation blocks the quiet claim, not independent artifact or guest-state evidence.

If a task action opens, raises or focuses a host window, needs host input, or cannot
satisfy the required quiet mode, stop that affected platform operation. Report the
boundary and continue independently qualified platforms. Do not silently switch to
foreground automation, minimize/close the user's windows, change focus settings,
restart shared ADB/HDC services or kill user processes. Recovery and cleanup may
address only the exact task-owned resources within existing authority; do not claim
that hiding a window afterwards repaired a silent-lifecycle violation.

Official sources: [Android emulator CLI](https://developer.android.com/studio/run/emulator-commandline),
[OpenHarmony HDC](https://github.com/openharmony/developtools_hdc/blob/master/README_zh.md),
[OpenHarmony UiTest](https://github.com/openharmony/testfwk_arkxtest/blob/master/README_zh.md),
and [Xcode command-line testing](https://developer.apple.com/library/archive/technotes/tn2339/_index.html).
These document available command routes, not universal host-focus guarantees.

## Device operation loop

The bundled [Android runner](android-debug-runner.md) supports an explicit serial for
collection, guarded plans and short recordings. Its optional existing-AVD start route
remains subject to the background/focus contract above and current launch authority;
it does not provision images, install applications or prove host focus preservation.

The following commands are examples after executable, serial, artifact, component,
paths and operation authority have been resolved. Apply bounded host-side timeouts.

```sh
"$task_adb" -s "$task_serial" get-state
"$task_adb" -s "$task_serial" shell getprop sys.boot_completed
"$task_adb" -s "$task_serial" install "$task_apk"
"$task_adb" -s "$task_serial" shell am start -W -n "$task_component"
"$task_adb" -s "$task_serial" shell uiautomator dump "$task_guest_xml"
"$task_adb" -s "$task_serial" pull "$task_guest_xml" "$task_local_xml"
"$task_adb" -s "$task_serial" exec-out screencap -p > "$task_capture"
```

Identify the resumed guest package/activity and read a fresh UI hierarchy or guest
screenshot. Prefer stable resource IDs, labels and the project's existing UI harness.
For an ADB tap/swipe, derive guest coordinates from current bounds or the actual
screenshot, including resolution, rotation, insets and any image scaling. Do not reuse
host-window coordinates or old screen positions. Guest `shell input` targets Android;
it must not be replaced by host mouse/keyboard events. Use only the device-command
allowlist needed by this task, not arbitrary shell, root or permission-grant actions.

Perform one bounded action, then re-read the relevant state and capture its visible
postcondition before choosing the next action. Exit 0, changed PNG hashes and a
successful activity launch alone do not prove the expected business transition.
Handle consent, authentication, external writes and destructive effects at their
actual boundary; entering a login page is not permission to submit credentials.

Stream screenshot bytes directly to a file, or use an explicitly bounded binary
buffer sized for the image. Validate and decode the PNG, inspect the actual image and
record serial, guest state, dimensions, time and evidence locator. Avoid default text
buffers, encoding conversions and screenshots of the host desktop. After a capture
failure, preserve its terminal result; repair only the diagnosed capture issue and
re-read current device/host state before claiming the recovered boundary.

## Host lock and sleep

The desktop screen-session gate governs host interaction. A documented, authorized
device-bound ADB route can operate the guest without host AX, focus, mouse or keyboard;
host lock alone does not prohibit that route. Conversely, readable ADB state does not
prove continued host execution, network reachability, guest unlock or agent/tool access.
Keep host lock, host sleep, guest lock and target-app authentication separate.

Use a fresh direct host-lock signal, such as macOS IORegistry `IOConsoleLocked`,
before and after each claimed locked operation, with timestamps and guest results.
Do not lock/unlock or wake the host without its own authorization. If the host is
unlocked before recovery, count the recovery only in that observed state. Unknown
state remains unknown. Two locked endpoints support the bounded observed interval,
not uninterrupted long-term lock or unattended reliability; record observer coverage.
Test agent/tool continuation, recording and longer duration independently when required.

Check host sleep/network policy without silently changing system settings. When
authorized, a task-owned temporary sleep inhibitor has a bounded lifetime and owned
PID; stop only that process at cleanup. Do not infer that screen lock prevents sleep,
that the agent will continue indefinitely, or that a locked guest may be bypassed.

## Recording

Inspect the bound device's `screenrecord --help` and actual support first. Start a
bounded recording to a task-owned guest path, confirm the recorder is running, perform
authorized actions, let it finalize or stop only its owned recorder, then pull the file
and inspect the exit status. Validate codec, dimensions, actual duration and decoded
frames spanning the transition; file existence and requested duration are insufficient.
Report audio support, secure-surface omissions, rotation and segment limits from the
observed tool/device, not universal assumptions. Segment long flows only as needed;
do not relabel an unlocked sample as locked recording or full-flow acceptance.

## Storage and lifecycle

When storage or optimization is requested, separate shared SDK tools/images, owned AVD
writable data/snapshots, downloads, original artifacts and captures/recordings. Report
allocated versus logical size and avoid counting parents and children twice. Disk
cleanup or image optimization needs its own scope: preserve original inputs and other
device dependencies, verify replacement content and boot before retiring owned assets.
Do not embed a previous run's API version, disk total or device configuration as a rule.

Return the created/reused AVD, process/serial, recordings, guest temporary files and
sleep-inhibitor ownership with cleanup or explicitly authorized retention. Keep failed
attempt evidence until reconciled. Do not remove another task's ongoing environment.

## Other simulators and handoff

Android ADB commands and success do not establish iOS support; ordinary device
packages are not simulator-compatible artifacts. Do not substitute host clicks or
a physical device for a missing virtual-device route.

Return device and artifact identity, scoped commands/results, guest postconditions,
screenshots/decoded recording evidence, host state intervals, failed attempts, cleanup
and remaining capability/feature gaps through the caller's existing result format.
The caller retains its acceptance IDs and separates emulator runtime from physical
device, vendor launcher, hardware SDK, backend and deployed-environment verification.

Official references: [emulator CLI](https://developer.android.com/studio/run/emulator-commandline),
[ADB](https://developer.android.com/tools/adb),
[AVD images and configuration](https://developer.android.com/studio/run/managing-avds).

## iOS Simulator

Bind the requested Simulator by current device ID/UDID, runtime and boot state;
`booted` alone may identify more than one target. Verify a simulator-compatible
artifact, bundle ID, installed version and target environment before launch.
Select a supported `simctl`, XCTest/XCUITest or current device tool by its actual
capability. Use an explicit target ID for install, launch, UI interaction, screenshot
and recording rather than the unqualified `booted` shortcut when ambiguity exists.

Inspect the current UI/accessibility tree or screenshot, perform a bounded authorized
action, then assert the requested guest result. Decode captured images and inspect
recorded frames; file creation alone is not visual proof. Keep Simulator behavior,
host window state, and physical iPhone behavior separate. If no supported UI adapter
can bind the requested target, return that operation `Not verified` while preserving
independent build/installed-app evidence.

Official references: [Simulator CLI and capture](https://developer.apple.com/library/archive/documentation/IDEs/Conceptual/iOS_Simulator_Guide/InteractingwiththeiOSSimulator/InteractingwiththeiOSSimulator.html),
[Xcode command-line tools](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference).
