# Background Client Operations

Use this profile when another application must remain foreground or when the user
requests a bounded qualification of that capability. It does not promise universal
control of applications, custom canvases or every screen-session state.
For mobile apps inside a simulator, use `ops-device`'s device-bound route;
host AX and a host window are not prerequisites for an authorized headless guest.

## Contents

- [Scope and route](#scope-and-route)
- [Qualification and execution](#qualification-and-execution)
- [Window and session evidence](#window-and-session-evidence)
- [Result for the caller](#result-for-the-caller)

## Scope and route

Fix the exact app/build, PID, window, control, requested operation and expected
postcondition. Record the foreground app, screen-session signal, permitted side
effects and cleanup before acting. Resolve aliases from inventory, not spelling
guesses. Keep browser page/tab operations with the browser owner; native client AX
coverage does not prove DOM coverage or authorize existing user-tab manipulation.

Prefer an existing documented app-owned semantic API, then an accessible control
route whose focus behavior is established for this target. Bind to an existing
process without an app-selection helper that may launch or activate it. A generic
command/eval bridge is not evidence of a bounded app-owned control plane.

For app-owned session protocols, use the session-protocol profile for identity, tool
scope, submission reconciliation and progress. Protocol evidence does not establish
selected desktop project, visible conversation synchronization or window pixels.

Separate these operations:

- Background launch: when launch is authorized, use a documented non-activating
  configuration, such as macOS `open -g` or `NSWorkspace` with `activates=false`.
  This constrains the launch request, not subsequent app behavior. Hiding,
  minimizing, restarting and moving Spaces are separate effects.
- Read: traverse a bounded control tree; record node/depth/time limits, exclusions,
  failed attributes and unresolved controls. Empty results prove only that scope.
- Write: check enabled state, attribute type and writability; set the value
  directly, then verify both the readback and the requested application behavior.
- Action: enumerate supported actions and execute only the exact named action on
  a uniquely identified control. AXPress and UI Automation patterns can have
  application-defined side effects; their presence is not a no-activation guarantee.
- Capture: target one verified native window independently of desktop coordinates.
  Capture permission, readable controls and a returned image are separate facts.

## Qualification and execution

An established route must match the current app/build, control, operation and
window/session state. Do not reuse a successful read as proof of a safe write, or
one button's behavior as proof for all buttons. Without a suitable established
route, ordinary background work stops at capability discovery.

An explicit request to test background writes/actions permits a bounded qualification
on disposable content or an identified reversible control within that request.
State the probe and expected local side effects first. Exclude routes that are
known to activate, raise, focus or inject global input; qualification is not
authority to try them. Do not submit drafts, execute commands in a user's terminal, save user
files, change permissions or alter system session state merely to demonstrate control.
If a safe probe cannot be isolated, return the missing target or authority.

1. Preserve the exact preimage and relevant application state privately; do not
   expose draft or terminal contents in logs. Establish unique identity, current
   authorization, screen state and operation capability before mutation.
2. Observe app activation throughout the bounded probe when the platform permits,
   with before/after foreground, key/focused-window or focused-element observations.
   Record actual observer coverage and unavailable focus signals. Endpoint samples
   alone cannot exclude a brief switch; polling and notifications are bounded evidence,
   not a mathematical guarantee. Pointer position and clipboard change counters
   complement the trace; they do not prove absence of every input event.
3. Perform one operation, verify the requested postcondition, then restore test
   content/state while ownership and guards still hold. Before restoration, confirm
   the current value is still the probe's value; never overwrite concurrent user edits.
   Re-read restoration and account for task-created windows/tabs/files.
4. Stop further mutation if foreground ownership, target identity, screen state or
   user activity invalidates the probe. Do not reclaim focus, raise the window or
   replay an ambiguous side effect. Report any retained preimage and incomplete cleanup.

If a setter returns success but the value remains unchanged, record a failed
postcondition rather than successful input. Disabled terminal text, custom-rendered
editors and application-managed rich-text fields require their own evidence; do not
replace failed direct writes with click, paste or Enter. A new route needs a
diagnosed reason and its own bounded qualification, not repeated identical attempts.

## Window and session evidence

For macOS, correlate the AX window and ScreenCaptureKit/CG window by owning PID,
identity and geometry; title alone is insufficient when several windows match.
Use window-scoped capture such as ScreenCaptureKit's desktop-independent window
filter or a supported window-ID capture. Do not substitute a desktop crop.

Inspect the actual image. Empty, stale, distorted, thumbnail-sized or ambiguous
window output does not pass full-window visual acceptance. Workspace/window-manager
transformations can make AX geometry differ from capture geometry; record the
mismatch without raising, unminimizing or moving the window to obtain better pixels.
Keep readable controls, captured pixels and successful interaction independent.

Ordinary background, occluded, hidden, minimized, another Space and locked sessions
are separate conditions. Test only the requested, authorized conditions and preserve
the screen-session gate in usage. Do not lock/unlock the desktop or change Spaces
to fill a matrix under a non-interruption constraint. Permission preflights are
neither successful operations nor authorization to request or grant new access.

## Result for the caller

Return operation-specific results with target/build/window/control identity, route,
screen/window state, preconditions, actual call outcome, observed postcondition,
non-interference coverage, evidence locator, restoration and remaining gaps. Use
existing caller evidence formats; do not invent a parallel machine schema.

Distinguish a failed postcondition, a capability not supported for the inspected
control, a permission/environment block, and a check not run (`Not verified`).
Keep unknown separate from unsupported. The calling coordinator retains the same
acceptance item and consumes only the achieved evidence; it must not promote an
AX inventory, successful no-op or low-resolution capture into full client acceptance.
