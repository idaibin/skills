# Frontend Audit Checklist

## Grounding

- Read all applicable guidance and status.
- Declare direct audit or scoped specialist subreview. For a changed tree,
  record the delegated frontend paths and keep `code-review` as the read-only
  Git-change review owner.
- Identify Web, Console, or Tauri Desktop.
- Trace route/page, layout, feature owner, analogous implementation, UI
  primitives, tokens, request/cache, forms/schema, state, tests, docs, and
  desktop adapter.
- Record direct-reuse, composition/variant, reference-only, unrelated, and
  `Not found` candidates.
- Check whether new files and abstractions have evidence-backed justification.

## Ownership

- Page/route composes rather than owning unrelated workflow and transports.
- Business components stay in the feature; UI primitives stay business-neutral.
- Hooks/composables, services, stores, schemas, and types each own a real responsibility.
- Local UI state remains local; URL and server state keep their source of truth.
- Tauri pages use an adapter; commands delegate to Rust domain/API owners.

## Vue 3 Profile

- Confirm SFC structure and the local `<script setup>`, Composition API, or
  Options API convention before applying framework-specific rules.
- For Composition API or `<script setup>`, trace `ref`, `reactive`, `computed`,
  destructuring/spread, `toRef`/`toRefs`, Pinia extraction/`storeToRefs`,
  shallow/raw values, and third-party objects at actual reactivity boundaries.
- For Composition API or `<script setup>`, require explicit `watch` sources. For
  `watchEffect`, enumerate intentional synchronous dependencies and do not
  assume reads after `await` retrigger it. Check invalidation, request
  abort/stale-response handling, feedback loops, flush timing, and duplicated
  derived state.
- For Options API, audit native `data`, `computed`, watch keys/getters/handlers
  and `deep`/`immediate`/timing behavior, owned dynamic `this.$watch` unwatch
  handles, `methods`, `provide`/`inject`, component Router guards, and
  `mounted`/`unmounted`/`activated`/`deactivated` cleanup. Do not require
  Composition imports or convert the component to satisfy this checklist.
- Check composable instance/shared/effect-scope lifetime and Pinia store/action,
  persistence/reset, consumer, and disposal ownership.
- Preserve props/emits, event payloads, `v-model` arguments/modifiers, named and
  scoped slots, fallthrough attributes, and component naming contracts.
- Check provide/inject key/default behavior, reactive and mutation owner, and
  provider/consumer cleanup. Prefer typed symbol keys when that is the local
  convention.
- Check Router params/query/meta, global versus component guard ownership,
  temporary guard teardown, navigation failure, and duplicate registration.
- Check unmount/scope disposal plus keep-alive activation/deactivation,
  listener/timer/subscription cleanup, request cancellation, and refresh/reset
  behavior.

## UI And Data

- Existing primitives, variants, tokens, page layouts, tables, dialogs, empty
  states, forms, requests, cache, toasts, and errors are reused.
- Loading, empty, error, partial, retry, optimistic, stale, and cancellation
  paths are explicit where applicable.
- Page-edge spacing, scrolling, breakpoints, and CSS declarations have one owner.
- No meaningless wrappers, copied components, or competing systems exist in the
  audited scope.

## Accessibility And Performance

- Keyboard, focus, dialogs/popovers/menus, form associations, icon names,
  non-color status, and async announcements are covered.
- Lists are bounded; requests deduplicate; React contexts or framework-native
  shared stores are scoped according to the detected framework.
- Memoization and bundle/IPC conclusions have measurement or path evidence.
- Vue computed/cache, watcher, reactive fan-out, Pinia subscription, and
  keep-alive request conclusions have profiling, request counts, or explicit
  path/complexity evidence.
- Desktop long tasks expose progress, cancellation, error, cleanup, and listener
  lifecycle.

## Structural And Documentation Lifecycle

- Identify required updates across routes, exports, manifests, aliases,
  generated files, tests, stories, fixtures, CI/build/deploy, architecture
  docs, project maps, and indexes that describe the boundary.
- Search for stale names, copies, imports, styles, docs, and command identifiers.

## Validation

- Run repository-defined formatting check, lint, typecheck, focused tests, and
  build/route generation that match the change.
- Validate browser behavior when layout, interaction, responsiveness, network,
  accessibility, or performance claims require it.
- Validate the real desktop client for native commands, menus, shortcuts,
  windows, progress, cancellation, and platform behavior.
- Report exact failures and `Not verified` gaps; never convert an unchecked
  assumption into a pass.
- Leave the worktree unchanged. A specialist subreview returns findings to
  `code-review` and never stages, commits, or claims Git readiness. `code-review`
  may produce the staging plan and readiness decision; `code-delivery` alone
  performs authorized staging, commit, rebase/squash, push, or delivery.
