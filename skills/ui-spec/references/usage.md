# UI Specification Usage

## Use this Skill for

- turning a selected Product Design result, screenshot, mockup, frame, or accepted current UI into an implementation-ready contract;
- specifying page/flow hierarchy, regions, states, transitions, responsive behavior, accessibility, assets, copy, and acceptance;
- mapping selected UI elements to current components and tokens or recording justified `adapt`/`new` decisions;
- preparing a bounded `dev-frontend` handoff;
- changing shared tokens, component semantics, variants, state vocabulary, or visual rules through the conditional Design System Spec profile;
- extracting, maintaining, or evaluating an accepted shared UI contract without editing product source.

Using existing shared components does not activate Design System Spec. A normal page or flow stays in Feature Spec and references current owners.

## Typical Chain

```text
visual exploration needed -> host Product Design -> selected visual source
selected visual source + product facts -> ui-spec -> dev-frontend
                                             -> ops-browser or ops-client
                                             -> audit-frontend -> repo-review -> repo-delivery
```

A task with an already selected visual source may start directly with `ui-spec`. If the source is missing and the user is still choosing what the UI should look like, stop before specification and route to Product Design. Start with `product-spec` only when behavior, permissions, failure semantics, or acceptance remain unresolved.

## Artifact Locations

Prefer repository-defined locations. Otherwise keep task-local specifications under `.codex/artifacts/<task-id>/`. Promote only an explicitly approved, sanitized, durable shared contract into the repository's established `docs/` structure. A Feature Spec should not create a shared manifest or rewrite the accepted system unless shared ownership actually changes.

## Handoff Examples

- `dev-frontend`: selected visual source and revision, target route/surface, facts, exact layout/state/interaction contract, current tokens/components to reuse, proposed deltas, responsive/accessibility rules, copy, assets, hard blockers, and acceptance checks.
- `ops-browser`: target URL, viewport/state matrix, exact assertions, console/network expectations, and screenshot paths after implementation.
- `ops-client`: launch command, expected app/window identity, target size, fixture, assertions, and screenshot path after implementation.
- Product Design: only when no visual source is selected or the user requests new visual alternatives, image generation, critique, or prototype exploration.

## Output Boundary

A UI specification proves that a selected direction has an explicit implementation contract. It does not prove visual exploration quality, source implementation, browser behavior, native-window behavior, accessibility, network behavior, or deployment.
