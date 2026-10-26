# Android Debug Runner

Use the bundled dependency-free `scripts/android-debug.mjs` with Bun 1.4+. It serves
physical Android phones and already running Android emulators through the same exact
serial binding. Run from the Skill directory or use the script's absolute path.
The bundled `scripts/android-debug.test.mjs` tests parsing, selection, shell argument
binding, output integrity and stop behavior with disposable fake devices.

## Contents

- [One-command collection](#one-command-collection)
- [Bounded action plans](#bounded-action-plans)
- [Recording](#recording)
- [Emulator lifecycle](#emulator-lifecycle)
- [Outputs and boundaries](#outputs-and-boundaries)

## One-command collection

```sh
bun scripts/android-debug.mjs devices
bun scripts/android-debug.mjs collect --serial "$task_serial" --kind phone --package "$task_package" --out "$task_new_output"
bun scripts/android-debug.mjs collect --serial "$task_serial" --kind emulator --package "$task_package" --out "$task_new_output"
```

`devices` never selects a device. `collect` requires a current serial and kind,
creates a new private output directory, captures the foreground activity, screenshot,
UI tree, device properties, optional package metadata and bounded activity logs.
The output's parent must already exist. An existing output directory is rejected.
Collection is observational at the app level but writes/removes its unique guest XML
and writes private host evidence. It is not filesystem-read-only; confirm those
exact effects are within scope before invoking it.
ADB is discovered from PATH, configured SDK roots and the macOS SDK convention;
`--adb` selects an explicit absolute executable. Nothing is installed or unlocked.

## Bounded action plans

Freeze a task-owned JSON plan after reading the target's current UI and authority.
Select by exact `resourceId`, `text`, `description`, or a conjunction. The selector
must match one enabled clickable node. Parent/child duplicates fail rather than
choosing the first. A requested coordinate swipe must use original device pixels.

```json
{
  "schemaVersion": 1,
  "expectedPackage": "com.example.browser",
  "steps": [
    {
      "op": "tap",
      "selector": {"resourceId": "download"},
      "expectPackage": "com.example.store"
    },
    {"op": "back", "expectPackage": "com.example.browser"}
  ]
}
```

```sh
bun scripts/android-debug.mjs run --serial "$task_serial" --kind phone --plan "$task_plan" --allow-input --out "$task_new_output"
```

Use `--kind emulator` for a bound emulator. Steps are `tap`, `back`, `swipe`,
`launch`, `open-url` and bounded `wait`. See `--help` and plan validation for fields.
`launch` uses an explicit package/activity component. `open-url` accepts only HTTPS
and an explicit browser package; it is a diagnostic launch, not proof of a page click.
`--allow-input` acknowledges an already authorized plan; the flag grants no authority.

The runner checks the foreground package and device/guest unlock state before each
action, refreshes tap/swipe evidence, and checks the destination package afterward.
Foreground/keyguard parsing depends on Android/OEM dumpsys formats. An unknown lock
format or conflicting resumed packages refuses input; it does not prove the device
is locked or offline. Keep read-only collection and actual version-specific
qualification separate. Do not relax an unrecognized format into permission to act.
A command failure, unexpected app, locked device, missing/ambiguous control or invalid
capture stops the remaining plan. The failed attempt and previous evidence remain.
There is no automatic resume or replay. Resolve uncertain effects before a new run.
Package arrival is a technical postcondition; inspect the captured screen for the
expected listing/business state. A plan with only `wait` is a valid no-op probe and
must not be reported as a tap test. Logcat is a bounded tail, so use timestamps to
correlate it; missing/evicted events cannot be reconstructed by this runner.

## Recording

```sh
bun scripts/android-debug.mjs record --serial "$task_serial" --kind emulator --seconds 5 --out "$task_new_output"
```

Recording takes no UI input and does not unlock/wake the device. It checks device
screenrecord support, records 1–30 seconds to a unique guest file, pulls the MP4 and
removes only that file. It captures before/after images. The requested duration and
nonempty MP4 are not codec/frame/duration acceptance; validate with a supported media
decoder before making that claim. A timeout remains failed; no automatic retry.
The recording command has a duration-plus-10-second deadline; `--timeout` bounds
the surrounding device commands. Both deadlines are recorded with their commands.
If recording or transfer fails, retain the exact guest path for reconciliation and
report it in the manifest; do not delete the only remaining original recording.

## Emulator lifecycle

```sh
bun scripts/android-debug.mjs emulator-list
bun scripts/android-debug.mjs emulator-start --avd "$task_avd" --port "$task_even_port" --allow-start --out "$task_new_output"
```

Before any quiet-dependent launch or recovery, apply the [background and focus
contract](simulator-operations.md#background-and-focus-contract). Qualify this installed
emulator version and its supported `-no-window` route first; if that route is unknown
or cannot satisfy the required quiet operation, do not invoke this helper to probe it.
The helper requests no-window display, but does not observe host foreground/focus or
certify the full quiet lifecycle. Host-lock endpoint samples are not focus evidence.

`emulator-start` requests an existing authorized AVD with `-no-window`. It checks
current serials, running AVD names, both console/ADB ports and advertised AVDs. It
keeps vendor startup logs and a launch receipt with its PID and serial, then polls
boot readiness with a 90-second budget; in-flight bounded commands and waits can extend
the wall time beyond that budget. Vendor image/ABI/acceleration errors stay in the log;
boot readiness does not certify application functionality. The launched instance is
retained and reported, including an unfinished boot. Stop it only after verifying
that same owned PID/AVD/serial and obtaining scope to stop; there is no blanket kill.

The helper does not create AVDs, download SDK images, accept licenses, modify shared
images, install APKs or wipe data. Use the simulator procedure for those separately
authorized operations. A running task-owned emulator can go directly to `collect`,
`run` or `record`; it does not need to be restarted for the helper.

## Outputs and boundaries

`manifest.json` binds run ID, serial/kind, command outcomes, input steps, timestamps,
capture dimensions/hash, host-lock samples and guest cleanup. Images/XML/activity
files and optional package information remain local-private. The script validates
PNG structure and decompressed dimensions; a human/agent still reads actual pixels.
Output may contain device identifiers, notifications or app data; do not upload it
as part of a generic review package. Guest XML and recording paths are unique and
cleaned by exact path. The legacy `ops-client-` guest filename prefix is retained
for artifact compatibility; it does not change this helper's `ops-device` owner.
No shared log or device data is cleared.
When removal fails, `removed: null` and an explicit unverified status preserve the
uncertainty; they do not assert that a guest file was created or remains present.

This is a device-evidence helper. It does not replace a project's functional test
engine, network oracle, HBuilderX runtime owner or native-plugin acceptance. Installation,
resource updates, forwarding and authenticated writes remain separate operations in
[hybrid runtime debugging](hybrid-mobile-debugging.md). Browser DOM/CDP follows the
browser owner and effective host policy; the runner exposes no arbitrary shell/CDP
operation. Android support does not imply iOS/Harmony support.
