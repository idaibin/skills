# Architecture And Ownership

Evidence basis: Twenty feature modules and UI packages; Outline's documented
`scenes/components/stores/shared` split; Appwrite Console's route co-location;
GitButler's app/package/API boundaries. See `reference-corpus.md`.

## Discovery Gate

Before proposing files, record:

- active `AGENTS.md` files and architecture docs;
- frontend app boundary, package/workspace manifests, aliases, generated paths,
  route generation, and validation scripts;
- target page and route entry, parent layouts, analogous features, and tests;
- shared primitives, feature components, hooks/composables, services, stores, schemas,
  types, request/cache clients, and feedback components;
- design tokens, spacing owner, responsive model, scroll owner, and desktop
  adapter if present.

Classify each candidate as direct reuse, compositional/variant extension,
reference-only, unrelated, or `Not found`. Do not infer `Not found` from one
directory.

## Project Class

| Class | Primary concern | Do not force |
| --- | --- | --- |
| Web app | routing, content flow, responsive behavior, server/cache contract | Console density or desktop chrome |
| High-density Console | consistent shell, tables/filters/actions, dense feedback, keyboard workflow | marketing layouts or one-off page primitives |
| Tauri Desktop | window/menu/shortcut/native lifecycle plus ordinary UI rules | direct native calls from presentation components |

Preserve framework-native routing and local names. A React/Vite/TanStack app,
SvelteKit console, Next.js app, or desktop webview may express the same
responsibilities with different directories.

## Responsibility Matrix

| Owner | Responsible for | Reject when |
| --- | --- | --- |
| Route/page | params/search validation, loaders, guards, page composition, page-level feedback | it embeds multiple API clients or a large business workflow |
| Feature | business components, feature hooks/types/state, workflow composition | feature code leaks into generic global components |
| UI primitive | business-neutral behavior, accessibility, tokens, variants/slots | it knows domain permissions, API payloads, or product entities |
| Hook/composable | framework-native stateful behavior, effects/watchers, subscriptions, lifecycle, or reusable orchestration | it only renames a function, hides trivial expressions, or creates unowned module-global state |
| Service/adapter | remote SDK, browser API, IPC/native boundary, error/DTO mapping | a page calls many low-level clients directly |
| Store | durable cross-tree business state or established shared cache | local dialog, hover, input, or one-page state is globalized |
| Schema | input, route, form, and transport validation at an owned boundary | UI, API helper, and backend drift into unrelated duplicate rules |
| Type | local feature vocabulary by default | types move global before a stable multi-feature contract exists |

## Vue 3 Ownership

- Record the SFC convention and whether the feature uses `<script setup>`, Composition API, or Options API. A mixed repository can have local conventions; do not convert the audited surface merely to make every file look alike.
- Treat a component instance, composable scope, Pinia store, router instance, application provider, and module scope as different lifetimes. Identify the owner before calling state or behavior “shared.”
- Keep `ref`/`reactive` state at its real owner and pure derivation in `computed`. Trace destructuring, spread, `toRef`/`toRefs`, `storeToRefs`, `shallowRef`, `markRaw`, class instances, and third-party objects only where they cross a reactivity boundary.
- Keep component contracts visible: read-only props, explicit emits, `v-model` arguments/modifiers, named/scoped slots, fallthrough attributes, and stable component names where keep-alive or tooling depends on them.
- For provide/inject, identify the provider, consumers, typed key or symbol, missing-provider/default behavior, reactive owner, allowed mutations, and disposal owner. Consumers should not become hidden owners of injected mutable state.
- Keep component-local state local. Use Pinia for established cross-tree or durable business state, with clear action and persistence ownership; do not promote a composable or store solely to avoid passing props.
- Register application/global Router guards at the router owner. Temporary global guards must retain and invoke their unregister callback; component guards stay component-owned and must not be duplicated by activation cycles.
- Distinguish unmount, scope disposal, route leave/update, and keep-alive activation/deactivation. Verify that each listener, timer, watcher, subscription, guard, and request cleans up at the lifetime boundary that actually ends it.

## Routes And Pages

- Keep route definitions discoverable and compatible with the current router.
- Keep URL-owned state in validated params/search rather than duplicating it in
  a global store.
- Let route/page files compose feature components and feedback states. Move
  stable workflows or remote/native access to their existing owners.
- Treat a very large route as a review signal, not an automatic defect. Inspect
  whether it mixes registration, permissions, data access, business behavior,
  rendering, and unrelated feature imports before splitting.
- Keep route-generated files and router manifests generated; update their source
  declarations through the repository command.

## Structural Lifecycle

For every add, reuse, move, rename, or deletion, check imports/exports, route
generation, manifests, aliases, tests, stories, fixtures, build/CI/deploy,
documentation, ownership maps, generated clients/types, and stale references.
