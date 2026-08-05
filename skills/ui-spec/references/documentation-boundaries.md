# UI Documentation Boundaries

## Location Order

1. Resolve `<design-root>` from effective guidance, shared-system ownership, and
   actual consumers; use `<design-root>/DESIGN.md` as that boundary's sole shared
   visual authority.
2. Use the project's established UI-spec location for one page domain or connected
   flow contract; only as a fallback use `docs/ui/<slice-id>/spec.md`.
3. Use the project-declared UI index for several independent slices; only as a
   fallback use `docs/ui/index.md` or `docs/ui/README.md`.

Do not infer `<design-root>` from the Git root alone, mechanically create one
`DESIGN.md` per application, or create a parallel shared design contract. Monorepo
inheritance exists only when current guidance and consumers prove it.

`DESIGN.md` is the human-readable and machine-readable semantic authority for shared visual decisions: YAML frontmatter owns normative token values, while Markdown owns their application guidance.

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
3. `<design-root>/DESIGN.md` (required shared visual authority);
4. the project-declared UI index when the request has several UI slices;
5. the project-declared target UI slice.

Do not require sibling PRD or UI contracts. Keep unfinished task-local work and
visual-evidence JSON under the repository's verified ignored task workspace, such as
`.codex/artifacts/ui-<slice-id>/`, until durable publication is explicitly approved.

Durable UI indexes, Feature Specs, and `DESIGN.md` describe only the current accepted
contract. Git stores their history. Candidate directions, comparison passes,
implementation logs, captured timestamps, and superseded specs remain task evidence.
A durable evidence artifact additionally requires a named team consumer, accessible
source artifacts, schema and validator, drift policy, revalidation owner, and
retirement condition.
