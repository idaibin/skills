# UI Documentation Boundaries

## Location Order

1. Use the repository-root `DESIGN.md` as the sole shared visual authority.
2. Use `docs/ui/<slice-id>/spec.md` for one page domain or connected flow contract.
3. Use `docs/ui/index.md` only for several independent UI slices.

Do not use another DESIGN.md location or create a parallel shared design contract.

`DESIGN.md` is the human-readable and machine-readable semantic authority for shared visual decisions: YAML frontmatter owns normative token values, while Markdown owns their application guidance.

## PRD Relationship

Use the same stable `<slice-id>` as the related `docs/prd/<slice-id>/spec.md` when both
artifacts exist. Cross-link them instead of copying facts. PRD owns user behavior,
business rules, permissions, failure semantics, and product acceptance. UI owns the
selected source, layout, component/token mapping, states and interaction,
responsive/accessibility rules, and UI acceptance.

## Consumer Read Contract

To implement one UI slice, read in order:

1. effective repository guidance and its declared authority paths or exceptions;
2. applicable product foundation/index facts and `docs/prd/<slice-id>/spec.md`;
3. `DESIGN.md` (required shared visual authority);
4. `docs/ui/index.md` when the request has several UI slices;
5. `docs/ui/<slice-id>/spec.md`.

Do not require sibling PRD or UI contracts. Keep unfinished task-local work under the
repository's ignored task workspace, such as `.codex/artifacts/ui-<YYYYMMDD-HHmmss>-<slice-id>.md`, until
durable publication is explicitly approved.
