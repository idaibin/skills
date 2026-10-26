# Hybrid Mobile Runtime Debugging

Use when Android native-shell / uni-app / WebView behavior crosses the installed
base, resource update, native plugin and backend boundary. Keep project-specific
commands and historical artifacts in their owning project; this reference captures
the reusable decision rules from device-debugging evidence.

## Contents

- [Runtime identity and reproduction](#runtime-identity-and-reproduction)
- [Install and resource-update boundary](#install-and-resource-update-boundary)
- [Logs, requests and performance](#logs-requests-and-performance)
- [WebView and network debugging](#webview-and-network-debugging)
- [Emulator coverage and cleanup](#emulator-coverage-and-cleanup)
- [Harmony and iOS evidence](#harmony-and-ios-evidence)

## Runtime identity and reproduction

Bind project checkout/commit, effective configuration/environment, installed package,
version/signing identity, native base and loaded resource bundle independently.
An APK, WGT and H5 build with similar names are different surfaces. An installed
custom debug base can load changed resources without proving the native base changed.
Verify platform, ABI, minimum SDK and native plugin availability against the artifact
before attributing a failure to page source. A stale or plugin-incomplete package may
verify a control chain only; it cannot certify the requested feature.

Use current project runtime docs and existing acceptance tools before inventing a
second business automation engine. Verify tool manifests, installed CLI help and
selected device ID. HBuilderX/uni-app CLI paths and flags are installed-runtime facts;
resolve them rather than copying a historical command. Starting a server, compiling,
rebuilding, running to a phone and installing a package are distinct effects and keep
their applicable authority. The generic Android helper only collects evidence and
executes a frozen device plan; it does not launch a project compiler or test suite.

## Install and resource-update boundary

When installation is explicitly authorized, inspect the exact artifact hash, package,
versionCode/versionName, signing certificates and ABI using available platform tools.
Record the existing installed package identity and the user's data-retention constraint.
Use an exact serial and the intended package, retain installer output, then read back
installed identity. For resource-only updates verify the accepted bundle and compatible
native base separately. Upload/push of a resource file alone is not activation proof.

Preserve a failed update/downgrade or signature mismatch as its actual failure. Never
silently add a downgrade flag, uninstall, clear data or substitute an older APK to
obtain a success. A separately authorized compatibility diagnostic can use another
artifact, but report its identity and narrower acceptance boundary. A generic install
success is not evidence that camera, push, payment, biometrics or proprietary SDKs work.

## Logs, requests and performance

Collect the smallest relevant time window/PID or tag set, correlate the visible action
with request start/end, route, response and UI state. Keep raw logs private; exclude
credentials and unrelated account data from deliverables. One system warning, empty
log filter, spinner or long request does not establish backend failure or its cause.
Compare runtime/environment and request observations before changing a timeout or API.
Mock responses and real endpoints remain separate; a mock UI pass is not live business
acceptance. Do not replay an order, approval, recharge or other consequential write to
obtain a cleaner trace after an uncertain result.

## WebView and network debugging

A native screenshot/UI tree works without WebView remote debugging. If actual DOM,
console or network instrumentation is needed, establish the separate browser/debugging
permission and actual running package/PID/socket. Current host restrictions and prior
applicable refusals govern whether a transport may be used. A prior successful socket
forward or injected script does not grant current authority or cancel a refusal.

Before an authorized ADB forward/reverse, list existing mappings and resolve exact
serial, direction, local/remote ports and owning process. Prefer an allocated free
port; retain the created mapping, and remove only that mapping after use. Do not
replace a user's mapping, expose a debug endpoint broadly, change proxy/TLS settings
or use privileged access merely to make inspection possible. A successful forward
proves transport setup only. Socket absence, native plugin absence, browser response
and application rendering require separate evidence.

## Emulator coverage and cleanup

Resolve image/ABI, boot state, installed native base and app state through the exact
emulator serial. Read-only collection can inspect an existing target; coordinate
input must not disrupt another task's active device. Prefer a task-owned isolated
instance when interaction would interfere. A valid no-op plan is useful for checking
guards and output but is reported as no-op. Do not install or restart another task's
instance to unblock validation. Emulator success cannot certify a physical vendor
store, OEM launcher, hardware integration or vendor push delivery.

Track task-owned temporary files, recordings, PID collectors, forwarding mappings and
started emulators independently. Stop only the verified owned resource and retain
referenced evidence until accepted. Failed/short recording, app handoff and cleanup
errors remain visible; shell exit, screenshot file existence and old screenshots do
not substitute for current UI or end-to-end acceptance.

## Harmony and iOS evidence

Historical cross-platform commands are rediscovery inputs, not a current adapter.
For Harmony, resolve installed HDC/DevEco tools, enumerate current targets and bind
the exact `-t` target before bundle/ability reads, screenshots, transfer or input.
Distinguish `bm` package metadata, `aa` application lifecycle and UI-tool controls.
Check installed help for syntax; a successful target listing proves no UI capability.
When collecting `snapshot_display` output and receiving it with `file recv`, inspect
the file signature and decode it rather than trusting the requested filename extension.
HAP installation, emulator creation/start and device input need their actual scope;
Android serials, APKs, ADB flags and resource paths are not Harmony equivalents.

For iOS, distinguish physical-device discovery from Xcode Simulator inventory.
Resolve current runtimes and available/booted devices, then bind an exact UDID rather
than a generic `booted` alias when another instance may exist. A successful `simctl`
listing or an installed runtime does not prove an app launched. A simulator-compatible
app artifact and supported UI harness are required for application interaction;
physical-device packages, trust/pairing and signing need their own verification.
Do not boot, pair, install or alter signing merely to unblock an inspection request.

The bundled Android helper does not dispatch HDC or Apple device tools. Preserve
these platform procedures and mark missing/unexercised adapters honestly rather than
reporting Android tests as cross-platform acceptance.
