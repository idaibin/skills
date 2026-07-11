# Stack Guidelines

Use these guidelines only after verifying the project actually uses the relevant stack.

## Toolchain And Script Contract

- Read `package.json`, lockfiles, workspace config, runtime pinning, and repository guidance before choosing commands or versions.
- Preserve the pinned Node/package-manager and dependency policy unless alignment is the requested task.
- Do not replace reviewed version ranges with `latest`.
- Prefer stable script names such as `dev`, `build`, `lint`, `typecheck`, `test`, and `check` when the repository standard defines them.
- Keep validation scripts read-only. Use explicit `:fix`, format-write, or equivalent commands for rewrites.

## Directory Classes

- React Router SPA projects normally route through their established `routes` layer.
- Next.js App Router projects keep `app`; Astro keeps `pages`; other frameworks keep their native router convention.
- Use repository-defined plural directories and kebab-case for new files when present. Preserve documented legacy naming until an explicit alignment task.
- Do not copy a Tauri, content-site, admin SPA, or web-monorepo layout into another class mechanically.

## Vite / Next.js / TanStack Router

- Treat `vite.config.*`, `tsconfig.*`, aliases, env prefixes, proxy config, and build targets as project contracts.
- Do not change alias, proxy, base path, env names, or build output paths for a component-level task.
- Preserve route paths, params, loaders/actions, query handling, layouts, and navigation conventions.
- Prefer existing scripts from `package.json`, docs, or repo guidance.

## React

- Follow the existing function/arrow component, export, file naming, hook placement, and render-boundary conventions.
- Keep state close to the component unless established context/store, route loader, query, or feature-hook ownership applies.
- Avoid adding global state, context providers, or another data library for a local page change.
- Preserve hook ordering, effect dependencies, subscription cleanup, and repository lint rules. Add memoization only for an evidenced render or calculation boundary.

## Vue 3

- Preserve SFC structure and the repository's `<script setup>`, Composition API, or Options API style. Do not translate Vue ownership into React hooks, Context providers, or effect-dependency rules.
- For Composition API or `<script setup>`, keep `ref`/`reactive` ownership intentional and pure derivation in `computed`. Treat destructuring, spreads, Pinia extraction, class instances, and third-party objects as possible reactivity escapes; use local `toRef`/`toRefs`/`storeToRefs`/shallow-or-raw patterns only when needed.
- For Composition API or `<script setup>`, use `watch` with an explicit source and intentional deep, immediate, and flush behavior. Use `watchEffect` only for a bounded effect whose automatically collected dependencies are appropriate; its dependencies are collected during synchronous execution, so reads after an `await` must not be assumed to retrigger it.
- For Options API, preserve native `data`, `computed`, watch options or owned `this.$watch`, `methods`, `provide`/`inject`, component Router guards, and `mounted`/`unmounted`/`activated`/`deactivated` lifecycles. Do not add Composition imports or convert the component merely to apply a rule.
- Clean watchers, listeners, timers, subscriptions, guards, and async work through invalidation, `onScopeDispose`, component lifecycle, route lifecycle, or request cancellation according to the actual owner.
- Preserve props/emits typing, event payloads, `v-model` argument/modifier contracts, named and scoped slots, fallthrough attributes, and component-name conventions.
- For provide/inject, use the established typed key—preferably a `Symbol`/`InjectionKey` where the codebase does—define missing/default behavior, retain reactive ownership in the provider, and expose explicit mutation commands instead of letting consumers mutate shared state implicitly.
- Use Pinia only for state with established cross-tree or durable ownership. Keep component-only state local, keep business mutations in store actions where that is the local contract, and avoid hidden module-level singleton state in composables.
- Preserve Router params/query/meta, redirects, lazy routes, and scroll behavior. Register global guards at the router owner, unregister temporary guards, and use component guards for component-owned navigation behavior.
- For cached components, pair `onActivated` with `onDeactivated`; unmount cleanup alone does not cover keep-alive deactivation. Cancel or invalidate requests when route, scope, or activation ownership ends, and prevent duplicate registration on reactivation.

## Layout Selection

- Prefer Flexbox for one-dimensional horizontal or vertical composition, including parent-owned alignment and centering.
- Use Grid for real two-dimensional row/column relationships.
- Do not add wrappers only to apply `display`, alignment, centering, or duplicated spacing when the semantic parent can own it.
- Let children fill or contract through the project's grow, shrink, basis, wrapping, and minimum-size conventions; avoid fixed dimensions for naturally adaptive content.
- Keep page-edge spacing at one shell, content, or page owner. Reusable components should not reapply outer margins or padding already supplied by their parent.
- Keep each CSS responsibility in one selector, token, variant, or component prop; remove duplicate and shadowing declarations after consolidation.

## Tailwind

- Use Tailwind only where the project already uses utility classes for the same UI layer.
- Reuse existing class composition helpers, variants, tokens, breakpoints, and spacing scale.
- Use scale utilities for normal sizing and spacing, such as `h-1`, `h-12`, `w-22`, `gap-3`, or `px-4` when available.
- Do not use arbitrary pixel utilities such as `h-[22px]`, `w-[88px]`, `mt-[7px]`, or `rounded-[13px]` for routine UI dimensions.
- Put real product/layout constants into named classes, component variants, tokens, or CSS variables instead of scattering arbitrary Tailwind values through JSX.
- Do not add theme changes or global utility conventions when existing tokens/classes work.
- Do not fight component-library tokens with Tailwind overrides unless the existing page already uses that pattern.

## Ant Design

- Prefer existing Ant Design wrappers, theme tokens, `ConfigProvider`, table/form/modal/drawer conventions, and locale setup.
- Keep form validation, field names, table pagination, row keys, loading states, and modal lifecycle consistent with nearby code.
- Do not replace Ant Design controls with custom or shadcn/ui controls in an Ant Design page unless requested.
- Avoid brittle CSS overrides against generated class names when props, tokens, or wrapper components exist.

## shadcn/ui

- Use existing generated components and local variant patterns before adding or changing primitives.
- Confirm Radix, Tailwind, `cn`, component paths, and variant utilities before importing.
- Do not re-run generators or alter shared primitives for a single page unless that is the requested scope.
- Do not introduce shadcn/ui into an Ant Design or non-shadcn page without an existing local precedent or explicit request.

## Mixed Stacks

- Treat deliberate mixed stacks as local contracts: follow the page's nearest precedent rather than a global preference.
- Prefer the component system already used in the target feature.
- If a requested change crosses UI systems, state the boundary and keep each side using its existing components and styling.

## Desktop Webviews

- Treat Tauri/Electron frontend code as UI code plus a native boundary.
- Keep shell, file, platform, and process access inside established IPC, command, or platform helper layers.
- Validate inputs before invoking native commands and show native command errors in the UI.
- Use `ops-client` for process, launch-command, CGWindowID, and real-window evidence.
- Treat frontend files and `src-tauri` as separate ownership boundaries; use `implement-rust` for Rust shell/backend changes.
