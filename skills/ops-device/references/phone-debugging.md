# Physical Phone Debugging

Use for an authorized connected phone: inspect its current screen, interact with a
named app/page, or collect evidence across browser, app-store and native-app transitions.
For emulators, use the simulator route. iOS requires an available, authorized iOS
device harness; Android ADB support does not establish iOS capability.

## Contents

- [Select the surface](#select-the-surface)
- [Bind and inspect Android](#bind-and-inspect-android)
- [Act and correlate the result](#act-and-correlate-the-result)
- [Failure scope and finish](#failure-scope-and-finish)

## Select the surface

- A request to inspect or operate the phone itself selects the physical-device route.
  Page content, DOM and browser-state acceptance still belongs to `ops-browser`;
  it can hand off a bounded phone-screen action here. On Android, first qualify
  the existing ADB route; device pixels do not require desktop Chrome inspection.
- DOM, JavaScript, console and browser-network inspection are a separate browser
  debugging route. Use it only when needed and permitted by the current host and
  task. Do not open `chrome://inspect`, enable a debugging port, forward a socket,
  or attach CDP merely to obtain phone pixels or perform a screen tap.
- Existing same-task authority covers the requested observation or bounded input;
  do not ask the user for screenshots or repeated approval before checking an
  available permitted device route. A screenshot request alone authorizes no tap.
  Clicking an authorized link covers its ordinary app handoff, not installation,
  login, consent, payment, publishing or unrelated app/data access.

## Bind and inspect Android

For repeatable collection or a frozen action plan, use the bundled helper described
in [Android runner](android-debug-runner.md); commands below remain diagnostic examples.

Resolve the current ADB executable from PATH, the declared SDK or project tooling;
record checked locations if unavailable. Run `adb devices -l`, then select the
authorized serial by device type/model and task context. A phone and emulator may
both be online. If multiple phones still match, resolve that ambiguity before
targeted commands. Rebind after reconnect or target drift; never reuse a historical
serial as ownership proof. `unauthorized` and `offline` are distinct device states;
do not grant debugging permission, reconnect, kill the shared ADB server or reset it
as an implicit repair.

Use `-s` on every device command. Read current foreground package/activity and a
fresh UI hierarchy or screenshot. Include OS/model and installed app/browser version
when relevant to the diagnosis. Keep device lock, host lock, connection and app login
separate. Device-bound ADB does not require host mouse/focus; it does not authorize
unlocking or waking the phone, bypassing secure surfaces or changing host settings.
For hybrid/uni-app diagnosis, distinguish the installed native base, loaded resource
update/WGT, WebView/runtime and configured environment from current source or H5.
Use relevant app/request logs to correlate a symptom; an unrelated global log line
or an old package's success cannot verify the new source, plugin or backend cause.

Examples after variables, authority and task-local paths have been resolved:

```sh
"$task_adb" -s "$task_serial" get-state
"$task_adb" -s "$task_serial" shell dumpsys activity activities
"$task_adb" -s "$task_serial" shell uiautomator dump "$task_guest_xml"
"$task_adb" -s "$task_serial" pull "$task_guest_xml" "$task_local_xml"
"$task_adb" -s "$task_serial" exec-out screencap -p > "$task_capture"
```

Stream PNG bytes directly; decode and inspect the actual image before claiming
visual evidence. XML may omit WebView content, a secure surface may be blank, and a
capture may fail independently of input. Report that exact gap. Historical captures
prove only their recorded state, not the current screen or permission.

## Act and correlate the result

Derive a control from the fresh hierarchy's label/resource ID and bounds. When a
device tap is needed, use original device pixels, accounting for rotation, insets
and any displayed-image resizing. Perform one bounded action, then read the new
activity/UI and capture its postcondition before deciding the next action. If the
user changes the target, stop input and re-establish task context without reclaiming it.
An app handoff caused by the authorized click is an expected transition to inspect;
it is not itself evidence that the user switched targets.

For browser-to-store diagnosis, capture the page URL, mode, visible UA/model/cache
and exact button before clicking. Correlate current deployed branch logic with those
values and a bounded activity-log interval around that click. Record incoming URI,
caller package, destination activity and rendered result. Redact tokens and unrelated
content from shared logs; do not clear shared logcat. Stop only the task's collector.

An activity URI shows what Android received, not all preceding Web redirects.
OneLink can itself produce a store intent. Distinguish OneLink versus direct intent
using the source page's actual branch inputs and navigation evidence; if insufficient,
report a likely branch and the missing proof rather than asserting the whole chain.
Directly launching a URI with `am start` is a separate diagnostic, not evidence that
the page button emitted it. Address-bar paste also does not test a user-gesture link.

Assess these outcomes independently: branch selected, OS handoff accepted, correct
listing usable, APK request started, download completed, install completed, app opened.
A resolved intent can open a deprecated/error listing; browser fallback need not fire
after a handler accepts it. A toast or resolved download promise is not completion.
Manual return or direct APK click is not automatic fallback. Simulated UA/UACH is
diagnostic input, not real-device identification or production acceptance.

For store-error diagnosis, preserve exact text and inspect relevant official help
within scope. Check protocol/parameters, app listing and current integration requirements
before recommending a change. An “old details page” message does not alone prove
the app is outdated, delisted, the package name is wrong, or every scheme is obsolete.
One failed branch cannot certify an untested replacement or justify “only/best route”.

## Failure scope and finish

Apply [interaction outcome and recovery](usage.md#stop-and-recovery)
to the original tool result. Distinguish a browser URL-policy refusal, device permission
failure, missing adapter, capture failure and ordinary cancellation. A refusal to open
a desktop browser inspection URL does not prove ADB is broken or revoke all phone
access. Preserve any explicit anti-circumvention instruction: do not change adapters
to reproduce a prohibited outcome. A materially safer alternative must avoid that
blocked action and remain independently authorized; uncertainty blocks only its
dependent operation. Historical assistant explanations are not the policy authority.

Return evidence at its observed layer, failed attempts and unverified paths. Account
for guest XML, local captures/logs and owned collectors. Preserve referenced evidence;
remove only disposable task-owned probes. Restore navigation only when authorized and
safe, then verify it; never claim return-to-page from a Back key's exit code alone.
