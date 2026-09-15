# Viewport Policy

Resolve the browser viewport for every operation before opening the target content or,
when the surface cannot configure a blank tab, before the first business interaction
or capture.

## Resolution Order

Use the first applicable source:

1. exact dimensions or device profile in the current user request;
2. an accepted viewport matrix for the target surface and state;
3. an explicit repository convention;
4. an effective host or personal default;
5. the package fallback: `1920 x 1080` CSS pixels for desktop Web and the named
   `iPhone 15` portrait device profile for mobile Web. For another user-named category,
   choose one minimal representative viewport and report it as an assumption.

Do not add unrequested breakpoint coverage. A current explicit user value overrides
every older or broader default.

## Application

- Prefer creating a task-owned blank tab, applying the resolved viewport or device
  profile, and then navigating to the target. If that sequence is unavailable, apply
  it immediately after tab creation and reload only when reloading is authorized and
  required for the page to initialize under the target viewport.
- For mobile Web, use the complete named `iPhone 15` profile when the backend exposes
  it, including its mobile, touch, scale, user-agent, and orientation behavior. Do not
  substitute another iPhone variant. If only dimensions are available, use the
  backend's dimensions for that named profile and keep the unexposed device-emulation
  fields `Not verified`.
- Do not resize a pre-existing user tab without authority and a restoration record.
  Use a task-owned tab when required session state is preserved; otherwise leave the
  viewport requirement `Not verified`.

## Readback

After applying the setting, read the effective page viewport, such as
`window.innerWidth` and `window.innerHeight`, and record it with the browser surface,
device profile when applicable, zoom, orientation, and target state. A successful
setter call or matching width and height alone does not prove that a complete mobile
device profile is active.

If the active surface cannot apply or read back the resolved setting, continue only
with work that does not depend on that viewport and report the dependent visual or
responsive claim as `Not verified`.
