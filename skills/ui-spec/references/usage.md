# UI Specification Usage

## Use this Skill for

- turning a selected Product Design result, screenshot, mockup, frame, or accepted current UI into an implementation-ready contract;
- specifying page/flow hierarchy, regions, states, transitions, responsive behavior, accessibility, assets, copy, and acceptance;
- mapping selected UI elements to current components and tokens or recording justified `adapt`/`new` decisions;
- preparing a bounded `dev-frontend` handoff;
- changing shared tokens, component semantics, variants, state vocabulary, or visual rules through the conditional Design System Spec profile;
- extracting, maintaining, or evaluating an accepted shared UI contract without editing product source.

Using existing shared components does not activate Design System Spec. A normal page or flow stays in Feature Spec and must reference current owners in the repo root `DESIGN.md`.

## Typical Chain

```text
visual exploration needed -> host Product Design -> selected visual source
root DESIGN.md + selected visual source + product facts -> ui-spec
  -> Feature Spec (reads DESIGN.md, does not rewrite it) -> dev-frontend
  -> Design System Spec (updates DESIGN.md) -> affected Feature Specs
  -> ops-browser or ops-client -> audit-frontend -> repo-review -> repo-delivery
```

A task with an already selected visual source may start directly with `ui-spec`. If the source is missing and the user is still choosing what the UI should look like, stop before specification and route to Product Design. Start with `product-spec` when behavior, permissions, failure semantics, or product acceptance remain unresolved. When only the UI contract remains ambiguous, resolve evidence first and ask one material layout, mapping, state/interaction, responsive/accessibility, or UI-acceptance question at a time. For more than one requested page, flow, or business domain, load [the multi-surface contract](multi-surface.md) before selecting artifact shape.

## Artifact Locations

Keep unfinished specifications directly under `.codex/artifacts/` as `ui-<YYYYMMDD-HHmmss>-<slice-id>.md`; do not create nested task directories. For explicitly approved durable publication, follow [the UI documentation boundaries](documentation-boundaries.md): keep shared visual semantics only in the repository-root `DESIGN.md`, write Feature Specs to `docs/ui/<slice-id>/spec.md`, use the same slice ID as related `docs/prd/` facts, and never add a `docs/specs/` wrapper or another shared visual authority.

## Handoff Examples

- `dev-frontend`: selected visual source and revision, target route/surface, facts, exact layout/state/interaction contract, current tokens/components to reuse, proposed deltas, responsive/accessibility rules, copy, assets, hard blockers, and acceptance checks.
- `ops-browser`: target URL, viewport/state matrix, exact assertions, console/network expectations, and screenshot paths after implementation.
- `ops-client`: launch command, expected app/window identity, target size, fixture, assertions, and screenshot path after implementation.
- Product Design: only when no visual source is selected or the user requests new visual alternatives, image generation, critique, or prototype exploration.

## Output Boundary

A UI specification proves that a selected direction has an explicit implementation contract. It does not prove visual exploration quality, source implementation, browser behavior, native-window behavior, accessibility, network behavior, or deployment.
