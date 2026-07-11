# State, Data, And Forms

Evidence basis: Twenty's local hooks/Jotai/Apollo separation, Outline's MobX
stores with fetch logic, Appwrite's route stores/SDK/dependency invalidation,
and GitButler's loadable query/services. The rule is ownership separation, not
adoption of those libraries.

## State Classification

| State | Preferred owner | Review questions |
| --- | --- | --- |
| Server/cache | existing query/cache/loader layer | key, freshness, invalidation, retry, cancellation, optimistic rollback |
| URL/route | typed params/search | shareability, back/forward, reload, validation |
| Form | form library/component plus schema | dirty/submitting/errors/reset, server errors |
| Shared business | feature/global store only when cross-tree and durable | owner, consumers, lifecycle, persistence |
| Local UI | component or feature hook | why would another screen need it? |

Avoid mirrored derived state. Compute from the owning source unless caching is
measured and invalidation is explicit.

## Vue 3 Reactivity And Shared State

Apply Vue rules only after confirming the app and the local SFC/API convention.

For Composition API or `<script setup>`:

- Trace `ref`, `reactive`, and `computed` from declaration through template,
  composable, store, and service use. Keep pure derivation in `computed`; do not
  mirror it into mutable state with a watcher.
- Treat destructuring and spreading reactive objects, extracting Pinia state,
  passing class instances or third-party objects, and crossing shallow/raw
  boundaries as possible reactivity escapes. Verify the concrete value before
  recommending `toRef`, `toRefs`, `storeToRefs`, `shallowRef`, or `markRaw`.
- For `watch`, record the explicit ref/getter/reactive/source-array input plus
  intentional `deep`, `immediate`, and `flush` semantics. Reject broad deep
  watches or feedback loops without a concrete ownership need.
- For `watchEffect`, enumerate the values read during synchronous execution and
  verify that automatic dependency collection is intentional. Reads after the
  first `await` are not part of that synchronous dependency window; do not
  claim they retrigger the effect without evidence.
- For any watcher/effect that starts async work, inspect invalidation cleanup,
  abort/cancel support, stale-response ordering, and error ownership. Navigation,
  scope disposal, or keep-alive deactivation must not allow an older response to
  overwrite current state.
- Identify whether each composable owns per-instance state, accepts an external
  owner, uses an effect scope, or deliberately shares module-level state. Hidden
  singletons and duplicated listener/timer/request registration are findings
  only when the traced lifetime makes them unsafe.
- Keep component-only state out of Pinia. For real shared stores, inspect store
  creation, action/mutation ownership, persistence and reset/logout behavior,
  `storeToRefs` extraction, consumers, and disposal or HMR behavior.
- For provide/inject, record the typed `InjectionKey`/symbol or local equivalent,
  missing/default behavior, whether provided values remain reactive, who may
  mutate them, and which provider/scope owns cleanup.
- Trace Vue Router params/query/meta as URL-owned state. Review global guard
  registration and unregister callbacks, component guard ownership, navigation
  failure handling, and duplicate registration across mount/activation cycles.
- For keep-alive components, review `onActivated`/`onDeactivated` in addition to
  unmount/scope disposal. Decide whether cache preservation, request refresh,
  cancellation, subscriptions, and form reset behavior match the feature.

For Options API, preserve and audit its native surface instead of requiring
Composition helpers:

- trace state from `data`, pure derivation from `computed`, and effects from the
  `watch` option or dynamically owned `this.$watch` handle;
- review watch key/getter/handler form plus `deep`, `immediate`, and relevant
  timing behavior without requiring `ref`, `watchEffect`, or `onScopeDispose`;
- trace `methods`, `provide`/`inject`, props/emits, component registration, and
  injected/store mutation ownership through `this` according to local style;
- map `mounted`/`beforeUnmount`/`unmounted`, `activated`/`deactivated`, and
  `beforeRouteEnter`/`beforeRouteUpdate`/`beforeRouteLeave` to listener, watcher,
  request, and guard ownership; retain/call unwatch or unregister handles for
  dynamically registered work;
- do not recommend an Options-to-Composition conversion merely to express an
  otherwise valid lifecycle, reactivity, or cleanup fix.

## Request And Cache Contract

Trace page → hook/composable/loader → service/client → endpoint/command → cache update.
Verify:

- request identity, deduplication, stale response handling, and abort/cancel;
- loading for initial and incremental work;
- empty versus filtered-empty;
- typed error with retry or recovery;
- partial data and per-region failure where applicable;
- optimistic update, rollback, invalidation, and reconciliation;
- pagination/virtualization for unbounded collections;
- permission and feature-gate behavior;
- cleanup when route, component, project, or window changes.

Do not add a second request wrapper or cache because one call is inconvenient.
Extend the established boundary or document why it cannot represent the case.

## Services

Services/adapters own SDK, fetch, browser, and native integration. They map
transport DTOs/errors to feature concepts and expose cancellation when the
transport supports it. Pages should not coordinate several low-level APIs
directly.

## Forms And Schemas

- Use the established form and schema stack.
- Keep client validation for immediate UX and backend validation authoritative.
- Share or generate stable transport schemas when the repository supports it;
  otherwise test that frontend constraints and backend contract agree.
- Do not copy validation into field components, submit handlers, API helpers,
  and Rust commands with different messages or constraints.
- Associate labels, descriptions, errors, required state, and submission state
  with their controls.
- Disable or guard duplicate submission, surface server field/general errors,
  and define reset/close behavior after success and failure.
