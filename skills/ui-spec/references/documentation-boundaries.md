# UI Documentation Boundaries

## Location Order

1. Resolve accepted shared visual guidance, token/variable sources and component
   contracts from effective guidance and actual consumers. Reuse those owners for
   both local slices and shared updates. When `DESIGN.md` is the adopted authority,
   resolve its `<design-root>` and scope; its filename alone does not adopt Google's
   format or the additional completeness policy. Record the applicable disposition
   using [the profile gate](workflow.md#profile-gate).
2. Use the project's established UI-spec location for one page domain or connected
   flow contract; only as a fallback use `docs/ui/<slice-id>/spec.md`.
3. Use the project-declared UI index for several independent slices; only as a
   fallback use `docs/ui/index.md` or `docs/ui/README.md`.

Do not infer `<design-root>` from the Git root alone, mechanically create one
`DESIGN.md` per application, or create a parallel shared design contract. Monorepo
inheritance exists only when current guidance and consumers prove it.

Project-declared guidance owns accepted shared visual decisions. Real component
source/types own interfaces and the declared token/variable source owns values.
Google-format `DESIGN.md` owns only its adopted scope: optional YAML carries its
normative token values and Markdown their application guidance. Avoid duplicating
values already owned elsewhere or promoting observed source into accepted design
decisions without the applicable acceptance.

Any durable structured projection is conditional: use it only when a named owner,
producer, non-LLM consumer, semantic version, executable validator, drift policy, and
retirement rule already exist. Otherwise read existing human guidance and source
owners directly.

## PRD Relationship

Use the same stable `<slice-id>` as the related project product-spec location when
both artifacts exist; `docs/prd/<slice-id>/spec.md` is a fallback example, not a hard
path. Cross-link them instead of copying facts. PRD owns user behavior,
business rules, permissions, failure semantics, and product acceptance. UI owns the
selected source, layout, component/token mapping, states and interaction,
responsive/accessibility rules, and UI acceptance.

## Consumer Read Contract

To implement one UI slice, read in order:

1. effective repository guidance and its declared authority paths or exceptions;
2. applicable project-declared product foundation/index and target product slice;
3. the project-declared shared visual guidance and relevant token/component owners;
   use `<design-root>/DESIGN.md` when adopted or explicitly being adopted;
4. the project-declared UI index when the request has several UI slices;
5. the project-declared target UI slice.
6. the component guidance and project-map entries referenced by that slice, followed
   by live source owners when implementation work begins.

Do not require sibling PRD or UI contracts. Keep unfinished task-local work and
visual-evidence JSON under the repository's verified ignored task workspace, such as
`.codex/artifacts/ui-<slice-id>/`, until durable publication is explicitly approved.
Keep an unapproved candidate UI specification and its complete generation prompt
under the repository's verified ignored `.codex/reviews/` convention. They are one
candidate pair, not a second shared visual authority, and they never update the
accepted shared contract before explicit promotion approval.

Durable UI indexes, Feature Specs, and shared visual guidance describe only the current accepted
contract. Git stores their history. Candidate directions, comparison passes,
implementation logs, captured timestamps, and superseded specs remain task evidence.
A durable evidence artifact additionally requires a named team consumer, accessible
source artifacts, schema and validator, drift policy, revalidation owner, and
retirement condition.

## Page And Component Binding

A page contract should answer which reusable or page-defining component roles compose
the surface and which page states and interactions apply. Human-readable component
guidance owns cross-page usage semantics; the project map points to high-value source
owners, and implementation revalidates symbols, registration, consumers, and current
states in live source. Keep props, slots, events, types, token values, and API schemas
in their source owners. Do not create a component registry solely to make the page
contract machine-readable.
