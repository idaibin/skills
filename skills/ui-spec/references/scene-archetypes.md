# Scene Archetypes and Layout Contracts

## Contents

- [Use and Ownership](#use-and-ownership)
- [Archetype Cues](#archetype-cues)
- [Acceptance](#acceptance)

## Use and Ownership

Load this reference only when an accepted source or candidate direction names a scene
archetype. An archetype is descriptive vocabulary, not a component API, token source,
framework choice, or catalog of fixed measurements.

- The selected source and accepted UI contract own geometry, density, breakpoints,
  states, and visual emphasis.
- The adopted design system or current repository owners determine tokens, components,
  layout primitives, and implementation syntax.
- `ui-spec` records composition and observable acceptance; `dev-frontend` chooses the
  repository-native implementation. Do not define props, slots, utility classes, or
  registry entries here.
- Values shown by one example remain evidence for that source only. Never convert them
  into global defaults or require DTCG, Tailwind, a Registry, Grid, Flexbox, or a UI kit
  unless the target repository has adopted that owner.

## Archetype Cues

Use only cues supported by the selected source:

### Operational dashboard

Prioritize scan order, stable navigation, comparable metrics, data density, and clear
status semantics. Dark presentation, column count, chart proportion, and panel sizing
remain source- and viewport-specific.

### Bento composition

Use varied card emphasis only when hierarchy benefits from it. Specify reading order,
content ownership, reflow, truncation, and interaction states without mandating a grid,
row height, card radius, or fixed slot API.

### Tactile or dimensional surface

Specify material hierarchy, contrast, focus, and motion purpose. Limit expensive or
dense effects where they reduce task clarity or accessibility; do not prescribe shadow
recipes, blur values, or promotional styling without source evidence.

### Mobile native-like surface

Respect the target platform's current accessibility, safe-area, typography, focus, and
input conventions. Record the actual platform and supported environment instead of
encoding one vendor's measurements or CSS adapter as a universal rule.

### Generated social or preview card

Freeze the requested renderer, canvas contract, font/assets, text bounds, and supported
layout subset. Canvas size and renderer restrictions come from the selected delivery
target, not this archetype. Keep generated-card acceptance separate from browser-page
acceptance.

## Acceptance

For any selected archetype:

1. Trace every exact target to selected-source evidence, an adopted owner, or explicit
   approval; otherwise mark it `proposed` or `Not verified`.
2. Verify the required viewport/state matrix, reading order, overflow, focus, input,
   localization, reduced motion, and task-completion geometry that actually apply.
3. Validate with the repository's existing component/style rules and the real target
   surface. Static source checks do not prove rendered fidelity.
4. Reject implementation-specific examples that conflict with current repository
   owners; adapt the archetype vocabulary instead of creating a parallel system.
