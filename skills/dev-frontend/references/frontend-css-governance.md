# Frontend CSS Governance

Apply this reference to maintained, human-authored CSS, Sass, and Less. Generated,
vendored, compiled, and minified output follows its producer and is not reformatted or
hand-edited.

## Contents

- [Contract And Correction Gate](#contract-and-correction-gate)
- [Ownership](#ownership)
- [Markup Structure](#markup-structure)
- [Source Form And Selectors](#source-form-and-selectors)
- [Layout And Geometry](#layout-and-geometry)
- [Cascade And Deletion](#cascade-and-deletion)
- [Validation Boundary](#validation-boundary)

## Contract And Correction Gate

- For selected-source UI work, change the Product/UI contract before source. Preserve
  the selected source identity, raw measurements, `use`/`ignore` boundary, viewport and
  state, then map every material correction to an acceptance ID and a single source
  owner. A later screenshot, inspect value, or user correction creates a new contract
  revision; it does not authorize an unrecorded late CSS patch.
- Keep source target, current runtime, and accepted target distinct. Current computed
  CSS proves only the implementation state and must not rewrite a Lanhu, Figma,
  screenshot, prototype, or accepted-current-surface target.
- Do not call a visual slice complete from source declarations, lint, build, or one
  screenshot. Selected-source completion requires two same-viewport/state runtime
  comparisons and computed geometry/style evidence for the applicable acceptance IDs.

## Ownership

- Shells own viewport chrome, page background, global clipping, and overlay hosts.
- Content/page layout owners own page-edge inset, broad bounds, and sibling placement.
  Panels own panel bounds and internal spacing. Components own their internal layout,
  not outer margins or padding already supplied by a parent.
- Keep one inner scroll owner where practical. Every wrapper must own semantics,
  layout, state, accessibility, animation, or reuse; flatten wrappers that only repeat
  an existing boundary.
- Keep each layout, spacing, typography, state, overflow, and responsive responsibility
  in one selector, token, utility, variant, prop, or semantic parent.
- Before editing a layout chain, record the actual shell, content/page, panel/component,
  control, inner-scroll, and overlay owners. For each axis, one owner supplies the
  page-edge inset and one owner supplies each internal gap; descendants must not repeat
  either value merely to reach the design target.

## Markup Structure

- Prefer the smallest DOM tree that preserves semantics and ownership. A wrapper MUST
  independently own at least one of: document semantics or an accessible name, layout
  or containing-block behavior, scrolling/clipping/stacking, component state or event
  boundaries, transition/teleport behavior, a stable ref/test hook, or proven reuse.
- Flatten adjacent wrappers that only forward width, height, padding, background, or a
  class to the same child. Move that responsibility to the nearest semantic or layout
  owner instead of retaining `div > div` solely for styling.
- Use `main`, `nav`, `aside`, `header`, `section`, lists, headings, buttons, and links for
  their real semantics. Do not use an unnamed `section` as a generic `div`; each section
  should normally have a heading or accessible name. Preserve one valid page `main`
  boundary and never nest `main` elements.
- Do not flatten a wrapper until checking whether it is a flex/grid item, positioned
  containing block, scroll owner, stacking context, container-query owner, slot or
  attribute-fallthrough target, keyed/conditional/repeated boundary, event target, or
  accessibility relationship. Component boundaries alone do not justify a rendered
  DOM node when the framework supports fragments or attribute forwarding safely.
- Review the rendered DOM as well as the source template: component roots, fragments,
  portals/teleports, transitions, and third-party components can add or remove effective
  nesting that is not obvious from one file.

## Source Form And Selectors

- Keep maintained rules multiline with one declaration per line. Do not mass-format
  unrelated files during a scoped change.
- Use shallow preprocessor nesting for directly owned BEM elements, pseudo states,
  modifiers, and local media scopes only when the compiled selector remains shallow.
  Avoid DOM-shaped nesting, cross-component reach-through, and specificity escalation.
- BEM is a local convention, not a universal requirement for Tailwind, CSS Modules,
  CSS-in-JS, generated primitives, or components that already own another convention.

## Layout And Geometry

- Prefer Flexbox for one-dimensional row or column relationships and parent-owned
  alignment. Use Grid for real two-dimensional row/column relationships; never replace
  Grid with Flex merely to reduce declarations.
- Prefer parent-owned `gap` and padding over repeated child margins. Avoid fixed sizes
  where grow, shrink, basis, wrap, intrinsic size, or a minimum-size invariant owns the
  behavior.
- Use background alpha for a translucent surface. Do not add element-level `opacity`
  to reproduce an already translucent background, because it also fades text, icons,
  focus indicators, children, and composited states. Element opacity is reserved for a
  contractually intentional whole-subtree state such as disabled or ended content.
- Reuse the project token scale. Consolidate coordinated stable geometry into an
  existing token or component-local custom property; do not create a global token for
  one local coincidence.
- Centralize responsive breakpoints and prefer inherited font, color, and line-height
  where the parent or design system already owns them.

## Cascade And Deletion

- Before deleting or moving a declaration, classify its effective owner as active,
  inherited, user-agent default, project-reset duplicate, identical base duplicate,
  responsive override, computed no-op, or defensive invariant.
- Remove only proven duplicate, shadowed, default, or computed-no-op declarations from
  the touched owner. Keep explicit local resets when portability or injection order is
  an intentional contract.
- A repeated property is not automatically equivalent: compare its selector, cascade
  position, media/state scope, inherited value, and rendered owner. Conversely, two
  different properties that create the same effect, such as translucent background
  plus container opacity or parent padding plus child margin, are competing ownership
  and must be reconciled.
- Do not treat `min-width: 0`, `min-height: 0`, flex/grid basis, overflow, focus-visible,
  reduced-motion, or breakpoint rules as boilerplate without tracing their container,
  consumer, and rendered effect.

## Validation Boundary

- Compare effective selectors and declarations after structural cleanup, then run the
  nearest non-mutating style/component check.
- For wrapper removal, compare element order, landmark/heading structure, accessible
  names, class/attribute fallthrough, event targets, focus order, effective flex/grid
  item relationships, containing blocks, scroll owners, and selectors before and after.
- For selected-source cleanup, pass 1 records the mismatch before correction and pass 2
  replays the same viewport/state after correction. A responsive breakpoint, hover,
  focus-visible, loading, empty, error, disabled, or overflow state required by the UI
  contract is a separate target, not implied by the desktop default.
- Formatting, preprocessing, linting, and selector comparison prove source integrity
  only. Responsive geometry, wrapping, clipping, scroll ownership, focus behavior,
  submenu placement, and visual parity remain `Not verified` without browser evidence
  for the relevant viewport and state.
