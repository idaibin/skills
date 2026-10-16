# Portal Experience And Performance

Use for authorized local or shared loading, responsiveness, rendering or memory changes. Keep the current stack and business contracts. A slow recording identifies measured operations, not the complete product scope.

## Coverage And Ownership

For portal-wide scope, build a route/feature matrix from the current router and navigation configuration. Cover the shared shell plus each reachable page and embedded surface. For each row record owner, first entry, cached return, changed URL/data context, loading/empty/error states, and observed evidence. Mark unvisited routes Not verified; inaccessible or unauthorized routes are exclusions, not passes.

For local scope, cover only the changed owner and affected consumers; do not expand
to every page merely because this reference applies.

Inspect common costs before page-local changes: navigation and route resolution, KeepAlive activation, request interception, reactive subscriptions and persistence, shared floating primitives, layout observers and animation. Then map page-specific initialization, lists, charts and iframes. Confirm the active deployed source identity before attributing an old trace to the current implementation.

## Hypothesis And Choice

Bind the proposed correction to an observed bottleneck and a falsifiable prediction:
which work should decrease and which user-task endpoint should improve. Rank candidates
by bottleneck contribution, frequency/population, evidence confidence, cost and risk;
a framework guide's static priority is a discovery aid, not a project priority.
Choose reducing, deferring, moving off the critical path or caching only when that
mechanism explains the cost. Account for first-use delay, freshness, memory, failure
recovery and keyboard continuity. Use the accepted measurement plan supplied by the
testing owner; reducing a local counter alone does not prove user improvement.

## Business-Preserving Changes

- Freeze existing filter/page/selection/permission semantics, local feedback, save/cancel/close confirmation, detail cache, polling/realtime behavior, and request formats. Optimize execution without silently changing those contracts.
- Follow data aliases through actual handlers. A list may share objects with a persisted response; nested read flags, loading flags or optimistic updates can be writes even when no handler names the Store. Narrowing a deep subscription to root replacement alone can lose those updates.
- If per-entry subscriptions are justified, retain nested changes within that entry; detach replaced/deleted entries and release live subscriptions on Store disposal. Preserve storage keys, JSON shape, restoration, pending-value reads and logout clearing. Deferring serialization alone does not remove deep reactive traversal; changing subscriptions alone does not remove synchronous serialization.
- Only build encryption payloads when used. Keep proof generation, encoding, null/string rules and encrypted-mode inputs intact. Compare deterministic fields and encryption inputs; randomized ciphertext equality is not a useful invariant.
- Pass cancellation as transport options, not business query/body fields. Preserve manual operations, polling intervals and realtime invalidation; late cancelled responses must not change data/cache/error state. Do not add a universal delay or request queue to every API without evidence and a business-compatible boundary.
- Reuse first-paint initialization scheduling where measured synchronous startup fan-out warrants it. A nextTick is a DOM-flush boundary, not proof that a frame was painted. Keep progress across deactivation; suppress duplicate mounted/activated starts. Coordinate the initial queue with pagination, resize and URL-driven requests so skipping an initial task cannot suppress necessary subsequent requests.
- Stable cache identity is separate from query identity. Resume the correct page context; a real page/page-size/filter change may require a new request even when the instance is cached. Keep existing draft, selection, scroll and detail behavior.
- Inspect actual animated properties. Transform/opacity may already be used; long main-thread tasks can still delay animation start. Treat transition: all as a candidate, not an automatic defect. Changing durations, scale, hover colors or visibility delays requires the owning UI contract; do not disguise that as a timing-only optimization.
- Stabilize floating configuration references where unrelated renders cause repeated positioning updates. Preserve placement, offsets, teleporting, triggers, focus, outside clicks, reopen and cache behavior. Necessary geometry reads cannot be removed just because Popper appears in a stack.

## Interaction Matrix

| Surface | Meaningful checks |
| --- | --- |
| Shared navigation | cold destination, cached return, rapid competing navigation, failure recovery, overflow menu, query updates |
| Mouse/keyboard | hover and pressed feedback, input focus/typing, scroll, keyboard selection, no unrelated blocking overlay |
| Select/tree | first open, options/data readiness, selection echo, close/reopen, changed selection context, positioning |
| Dialog/drawer | first open, close during initialization, close/reopen while leaving, cancel confirmation, stale result exclusion, selected people/detail cache |
| Lists/search | page/filter changes, cleared query, repeated query, empty/error/retry, returning to the same URL context |
| Background work | deactivation, in-flight completion/cancellation, pending realtime invalidation, interval restoration, queued persistence |

## Validation And Result

Use tests closest to the changed seam, plus actual browser states through the runtime operations owner. Count requests by endpoint and page/filter/page-size, and separate a duplicate from a necessary changed-context refresh. Test no-cache first entry, leaving before the first task, leaving after it starts, resize before return, subsequent pagination/resize, nested cache updates, reload, clearing and disposal with live entries.

Keep source, test doubles, real browser, backend, deployment and performance evidence separate. If browser actions cannot reach the precise pre-start race, report that boundary as Not verified even if normal rapid navigation passes. Do not claim all pages smooth from one route, a build, a recording frame rate or a source change. Complete only the authorized slice and state remaining coverage with recovery conditions.

## Overlay Feedback And Preparation

Separate input-to-shell feedback, shell/mask presentation, content readiness and the
transition itself. If a panel appears before its mask or becomes usable only after
loading, trace the shared overlay owner, teleport/mount ordering and synchronous work
before changing animation duration. A nextTick, module preload or zero-duration CSS
rule alone does not prove the first painted state or lower interaction latency.

Choose preparation from measured repeated work: module caching, a retained shell,
conditional content mounting and data prefetch have different costs and permissions.
Loading a module need not start business requests; retaining a shell need not retain a
form session. Preserve target-specific drafts, permissions, empty/error/retry states
and failure recovery. Compare cold first open and warm reopen, then close or navigate
away before preparation finishes. Qualify CPU, memory, request and user-outcome evidence
separately; a warm-cache improvement does not establish cold-path improvement.
