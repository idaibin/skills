# Frontend Inventory Profile

Use this optional profile only when a durable map must guide repeated frontend
discovery. It is not a prerequisite for a scoped implementation, audit, or review.

## Bounded Inventory

Index only the selected surface and its direct owner edges:

- route or entry registration, pages/screens, and feature boundary;
- reusable primitives and feature components;
- hooks/composables, local/shared state, and data/cache owners;
- API client, request types, and direct consumer boundary;
- styling/theme/config sources and layout owners;
- root `DESIGN.md` binding when the repository adopts it.

Do not turn this into a complete component catalog or duplicate live source. A map
miss means only that the index has no verified row: search the relevant owner root
before deciding `reuse`, `extend`, `wrap`, or justified `new`.

## Reusable UI Row

For a reusable UI entry, record:

1. the semantic job and the exact map-root-relative root `DESIGN.md` path plus
   heading anchor or named semantic binding, when applicable;
2. current implementation path and symbol, export or registration, provider root,
   and representative current consumer;
3. applicable states/variants and the reuse boundary; and
4. current-source evidence for each claimed edge.

Link to the shared semantic authority; do not copy token values, typography,
spacing, or component rules into the map. `DESIGN.md` does not prove implementation
is synchronized: record adapter/config and consumer evidence separately, or mark it
`Not verified`.
