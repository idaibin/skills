# Axure Product Evidence

Load this reference for an authorized Axure prototype whose product requirements,
page inventory, or interaction behavior will be handed to `product-spec`.

## Source And Capability Gate

Record the exact share/export origin, prototype/project identity, version or revision,
account/workspace evidence when applicable, page-tree visibility, and whether the
active browser exposes semantic DOM, iframe, screenshot, and interaction control.
Treat another version, an unverified duplicate page name, or a stale tab as a
different source. Stop at login, permission, consent, or account switching.

Prefer an authorized hosted prototype. If the caller supplies a local Axure export,
record HTML, `data.js`, notes, and asset provenance separately. Do not claim that a
`file://` page or a listening port proves runnable interaction; require an actually
reachable HTTP page for browser behavior, and keep static-export facts distinct.

## Bounded Coverage Workflow

1. Freeze the source identity and declared page/version scope.
2. Expand every in-scope page group exposed by the page tree. Prefer Axure's exposed
   page target such as `nodeurl` as the page-local key, then bind it to the source
   ID/URL and group path. When no target is exposed, derive a stable key from source
   ID/URL plus group path; never deduplicate by visible title alone.
3. Record every page as `observed`, `blocked`, or `Not verified`, including its
   visible purpose, entry state, requirements/notes location, and evidence IDs.
4. Build a bounded interaction queue from visible links, hotspots, controls,
   annotations, requirement tables, and caller-named flows. For each item capture
   before state, exact action, destination/state change, and after evidence once.
5. Inventory dynamic panels, overlays, repeaters, conditional branches, validation,
   empty/error/permission states, and return paths only when exposed by the source.
   Never infer a hidden branch from pixels or one successful path.
6. Reconcile runtime observations with supplied notes/static export. Preserve
   conflicts as separate facts; do not let static metadata prove runtime behavior.
7. Stop when the declared page set and discovered queue are exhausted, or when a
   named capability/access blocker prevents closure. Report the blocker instead of
   calling the prototype complete.

## Product Handoff

Return `axure-product-evidence/v1` with:

- source identity, revision, declared scope, account/access status, and capture time;
- page-group and page ledger with stable keys, status, evidence, and requirements
  locations;
- user-flow and interaction ledger with entry/action/result, branch/state, and
  direct before/after evidence;
- observed copy, roles, business rules, permissions, validations, data effects,
  failure/recovery behavior, and explicit source location;
- static-export observations separated from live-browser observations;
- conflicts, assumptions, inaccessible content, undiscovered-hotspot risk, and every
  `Not verified` item;
- coverage totals for pages, requirement sources, interactions, and named states.

This handoff supplies observations, not product decisions. `product-spec` classifies
them as Confirmed, Assumption, Open Question, Rejected, or Deferred and writes only
authorized product artifacts. Route colors, typography, spacing, geometry, assets,
and other selected-source visual contracts to `ui-spec` rather than copying them into
the product specification.

Claim complete Axure coverage only when every declared page and requirement source is
accounted for, every caller-required flow/state has direct evidence, the discovered
interaction queue is exhausted, and no required item remains blocked or `Not
verified`. When hotspot enumeration is unavailable, interaction completeness remains
`Not verified` even if all visible pages were visited.
