# Frontend Decomposition

Load this reference when the authorized change touches a file, component, hook,
composable, store, service, or function that mixes independently changing
responsibilities. File or function length is a review signal only; cohesion,
ownership, coupling, lifecycle, and verification determine whether to split.

## Diagnose Before Splitting

Map the touched code into its actual roles before moving it:

- route/page composition and navigation;
- visual regions and interaction contracts;
- local or shared state and lifecycle;
- data loading, mutation, cancellation, caching, and error mapping;
- business validation, calculation, transformation, and permissions;
- platform or third-party adapters;
- public exports and focused verification seams.

When inexpensive evidence exists, inspect current responsibilities and relevant
co-change history in the authorized area:

- **Divergent change:** one owner changes for unrelated business reasons, indicating
  that it may contain multiple owners.
- **Shotgun surgery:** one business change repeatedly touches scattered owners,
  indicating that a rule or orchestration owner may be missing.

Neither signal follows from file count, line count, or one unusually broad change.

Split when two roles have independent change reasons, owners, lifecycles, consumers,
or tests and keeping them together materially increases navigation, regression, or
coordination cost. Keep a large but cohesive unit intact when extraction would only
add indirection.

Apply the deletion test before retaining an extracted unit: if removing it makes its
complexity reappear across real callers, it earns locality; if the complexity simply
vanishes, delete or inline the pass-through instead.

## Ownership Targets

- Keep a route/page file as a readable shell when it coordinates multiple independent
  business sections. It may own route context, page navigation, composition, and
  genuinely shared data or locks.
- Give an independently stateful section its own feature component when it owns an API
  flow, form, table, drawer/dialog, validation, action lifecycle, or loading/error
  state. Keep feature-private pieces inside that feature directory.
- Put deterministic business validation, calculation, normalization, and permission
  decisions in named pure functions or the existing domain owner. Do not bury them in
  render branches, watchers, Effects, or template expressions.
- Keep transport, response normalization, cancellation, caching, and external error
  mapping in the repository's existing service/query/adapter boundary. Do not create
  a parallel data layer merely to shorten a component.
- Extract a hook, composable, store, or controller only when it owns a real state or
  lifecycle boundary. Keep state local when no established shared owner needs it.
- Turn a long handler into a short orchestration sequence only when its steps have
  meaningful names and separable contracts, such as validate, transform, persist,
  reconcile, and report. Prefer pure steps; keep ordering and recovery visible.
- Extract types, constants, schemas, or helpers only to their existing or natural
  owner. Do not create generic dumping grounds such as `utils`, `common`, or `helpers`.

## Preserve Locality

- Follow repository-native directories, naming, exports, dependency direction, and
  framework style. Avoid circular imports and cross-feature imports of private files.
- Pass the smallest stable props, events, or repository-native context. Keep shared
  orchestration at the nearest common parent instead of duplicating it in children.
- Preserve public APIs and observable behavior unless the request explicitly changes
  them. Move matching tests and ownership records with structural changes.
- Introduce a cross-feature abstraction only for proven consumers and a stable common
  contract. Repetition with different change reasons may be safer than forced reuse.
- Do not hand-split generated, vendored, or machine-owned files. Change the producer or
  isolate the generated boundary when that work is authorized.

## Avoid Cosmetic Decomposition

Do not use any of these as a completion target:

- an arbitrary maximum line count, function count, or one-component-per-file rule;
- file-per-function layouts or chains of one-line pass-through wrappers;
- moving business logic into child components, stores, or hooks only to reduce lines;
- extracting markup fragments with no independent behavior, semantics, or reuse;
- speculative shared components or generic helpers without real consumers;
- broad cleanup of unrelated legacy large files outside the authorized slice.

## Completion Gate

- The entry page, component, or handler reads as orchestration rather than a mixture of
  unrelated implementation details.
- Every extracted unit has one named responsibility and a stable reason to change.
- Business rules, data effects, lifecycle state, and presentation have no competing or
  duplicated owners.
- Focused tests exercise the extracted public or behavior seam without depending on
  private markup or call order unless that order is the contract.
- Existing behavior, layout, accessibility, API semantics, and failure states remain
  unchanged unless explicitly authorized and verified.
- Report the resulting owners and any intentionally retained large cohesive unit; do
  not claim success from reduced line counts alone.
