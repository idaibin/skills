# Viewport Policy

Determine the viewport required for a claim before opening target content. Distinguish
that requirement from the observed viewport and from permission to change it.

## Resolution Order

Use the first applicable source:

1. exact dimensions or device profile in the current user request;
2. an accepted viewport matrix for the target surface and state;
3. an explicit repository convention;
4. an effective host or personal default;
5. for an independently isolated browser only, the package fallback:
   `1920 x 1080` CSS pixels for desktop Web and the named
   `iPhone 15` portrait device profile for mobile Web. For another user-named category,
   choose one minimal representative viewport and report it as an assumption.

Do not add unrequested breakpoint coverage. A current explicit user value overrides
every older or broader default.

## Application

- Resolve permission to change shared browser state from effective host policy and
  explicit user authorization; a requested viewport or task-owned tab is insufficient.
  Bind each restriction to its named surface, operation, and task condition. Do not
  extend a scoped host restriction to other surfaces or states; verify their actual
  permissions separately. Shared state alone is not a prohibition when the applicable
  policy and task authority permit the specific change.
  When policy prohibits changes or permission is absent, use passive observation.
- Before opening, capturing, or closing a tab, establish the scope and side effects
  of the tool lifecycle. Stop affected operations when shared-state effects are
  unknown or exceed authority. Prefer an independently isolated authorized browser;
  otherwise mark the dependent viewport claim `Not verified`.
- On an independently isolated browser, prefer creating a task-owned blank tab, applying
  the resolved viewport or device
  profile, and then navigating to the target. If that sequence is unavailable, apply
  it immediately after tab creation and reload only when reloading is authorized and
  required for the page to initialize under the target viewport.
- For mobile Web, apply the complete device profile resolved above when the backend
  exposes it, including mobile, touch, scale, user-agent, and orientation behavior.
  Do not substitute another device for the resolved target. If only dimensions are
  available, use the backend's dimensions for that target and keep the unexposed
  device-emulation fields `Not verified`.
- Preserve pre-existing user tabs and their device, zoom, orientation, and scroll
  state. Changes require verified authority and a restoration plan; package defaults
  apply only to independently isolated browsers.

## Readback

Passively read the effective page viewport, such as
`window.innerWidth` and `window.innerHeight`, and record it with the browser surface,
device profile when applicable, zoom, orientation, and target state. A successful
setter call or matching width and height alone does not prove that a complete mobile
device profile is active.

If the active surface cannot safely provide or read back the required setting, continue only
with work that does not depend on that viewport and report the dependent visual or
responsive claim as `Not verified`.
