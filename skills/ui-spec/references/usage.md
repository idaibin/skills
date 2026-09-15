# UI Specification Usage

## Use this Skill for

- turning a selected Product Design result, screenshot, mockup, frame, or accepted current UI into an implementation-ready contract;
- grounding an unapproved candidate direction in current product/source facts and
  maintaining its complete local image-generation prompt before external exploration;
- specifying page/flow hierarchy, regions, states, transitions, responsive behavior, accessibility, assets, copy, and acceptance;
- mapping selected UI elements to current components and tokens or recording justified `adapt`/`new` decisions;
- preparing a bounded `dev-frontend` handoff;
- changing shared tokens, component semantics, variants, state vocabulary, or visual rules through the conditional Design System Spec profile;
- extracting, maintaining, or evaluating an accepted shared UI contract without editing product source.

Using existing shared components does not activate Design System Spec. A normal page
or flow stays in Feature Spec and must reference current owners in the resolved
`<design-root>/DESIGN.md`.

## Typical Chain

```text
candidate direction -> ui-spec candidate spec + complete prompt
  -> host Product Design/image capability, or ask-ai for named external transport
  -> user-approved selected visual source
resolved design-root DESIGN.md + selected visual source + product facts -> ui-spec
  -> Feature Spec (reads DESIGN.md, does not rewrite it) -> dev-frontend
  -> Design System Spec (updates DESIGN.md) -> affected Feature Specs
  -> ops-browser or ops-client -> repo-audit -> repo-review -> repo-delivery
```

A task with an already selected visual source may start directly with `ui-spec`. A
user-directed but unapproved direction may also start here to create the local
candidate pair; load [the candidate workflow](candidate-visual-direction.md). Route
actual alternatives/generation to Product Design or the applicable image capability,
and named external-model transport to `ask-ai`. Start with `product-spec` when
behavior, permissions, failure semantics, or product acceptance remain unresolved.
When only the UI contract remains ambiguous, resolve evidence first and ask one
material question at a time.

## Artifact Locations

Keep unapproved candidate specifications and full generation prompts under a verified
ignored `.codex/reviews/` path; keep other unfinished evidence under `.codex/artifacts/`.
For
explicitly approved durable publication, follow [the UI documentation boundaries](documentation-boundaries.md):
keep shared visual semantics only in the resolved `<design-root>/DESIGN.md`, write
Feature Specs to the project convention such as `docs/ui/<slice-id>/spec.md`, use the
same slice ID as related product facts, and never add another shared visual authority.

## Handoff Examples

- `dev-frontend`: selected visual source and revision, target route/surface, facts, exact layout/state/interaction contract, current tokens/components to reuse, proposed deltas, responsive/accessibility rules, copy, assets, hard blockers, and acceptance checks.
- Compatible typed consumer: capability `ui.contract.specify@1.1.0`, exact immutable
  input/result basis, package-relative artifacts, hashes and byte lengths, validation
  results, source/approval bindings, and trusted actor identity. Keep token values in
  `DESIGN.md`; the host adapter owns its own storage, traversal, and receipt protocol.
- `ops-browser`: target URL, viewport/state matrix, exact assertions, console/network expectations, and screenshot paths after implementation.
- `ops-client`: launch command, expected app/window identity, target size, fixture, assertions, and screenshot path after implementation.
- Product Design: only when no visual source is selected or the user requests new visual alternatives, image generation, critique, or prototype exploration.
- `ask-ai`: frozen candidate-spec and complete-prompt paths/hashes, named external
  recipient, allowed inputs, output contract, and explicit one-send boundary.

## Output Boundary

A UI specification proves that a selected direction has an explicit implementation contract. It does not prove visual exploration quality, source implementation, browser behavior, native-window behavior, accessibility, network behavior, or deployment.
Official DESIGN.md lint additionally proves format only. Adopted shared-authority
completeness requires the separate package policy result and exact-hash approval.
