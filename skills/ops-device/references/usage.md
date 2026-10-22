# Ops Device Usage

## Summary

The owner is the requested acceptance target, not the automation product. Use
`ops-device` for mobile device setup, app/container lifecycle, native UI, permissions,
guest state and device-scoped evidence. A plain web page remains `ops-browser` even
when displayed in a phone browser; the browser owner may request a bounded device
action here. A desktop client remains `ops-client`, including its embedded WebView.
Cross-layer diagnosis stays with the calling task; this Skill returns device evidence.

## Target and effect gate

Record platform, physical/virtual kind, stable serial or UDID, OS/runtime, current
connection/boot state, app bundle/package, installed build and target environment.
Select the exact device in every command or tool call. Names, list order, `booted`,
an active simulator window, and previous-run IDs are hints, not unambiguous binding.
For a multi-device request, keep each target and its evidence separate. If a device
reconnects or restarts, refresh identity before the next action.

Choose from currently supported adapters by target reachability and evidence need:
semantic device API/accessibility for identifiable controls, a project test harness
for repeatable assertions, browser protocol for page DOM/network when available,
and current-screen visual interaction when semantic data is missing. Native Codex
computer control remains eligible if it can bind and verify the required target.
No adapter's presence grants authority. Avoid a lower-fidelity fallback that changes
the target, app, account, host foreground, or permission scope silently.

Inventory and observation are distinct from device provisioning, launch, install,
permission changes, credential entry, external submission, account changes, data
reset, or shutdown. Apply current user and host authority at each effect. Reuse
already valid task authority without asking again at a Skill handoff. Do not operate
another task's active device, change shared tooling, or bypass a refusal by changing
adapter.

## Operation and evidence loop

1. Read the current device, app and visible/semantic state; record the target ID,
   source, time, and selected context.
2. Perform one bounded authorized action using current selectors or current-screen
   coordinates; serialize mutations to the same device.
3. Re-read the relevant state and verify the requested postcondition. A successful
   command, changed screenshot hash or launched activity is insufficient by itself.
4. Label each observation as device/OS, installed artifact, app process, native UI,
   Web context, real network, synthetic network, log, screenshot or recording. A
   device screenshot proves a visible moment, not backend success; a semantic API
   result does not prove the window rendered.
5. On capture failure, preserve the failure and continue independent semantic checks.
   Repair the diagnosed capture path only within current authority, then rebind the
   target and decode/inspect the recovered artifact before visual acceptance.

Read [simulator operations](simulator-operations.md) for virtual-device details,
[physical devices](physical-devices.md) for connected phones, and
[hybrid surfaces](hybrid-surfaces.md) when the target crosses browser/WebView contexts.

## Stop and recovery

Stop the affected action on unresolved device/app/context identity, missing adapter
capability, absent authority, target drift, guest lock/authentication, or uncertain
side effect. Preserve an uncertain submission and reconcile its exact target before
any retry. Continue independently authorized read-only evidence. Report simulator,
physical-device, vendor-ROM, hardware, network and long-duration coverage only at the
level directly observed.
