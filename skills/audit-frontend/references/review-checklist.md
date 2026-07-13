# Frontend Audit Checklist

## 1. Grounding and Delegation

- Read all applicable guidance and status.
- Declare direct audit or bounded specialist review.
- When delegated, record exact paths/diff, questions, exclusions, and coordinating owner:
  - `repo-review` for local dirty-tree and commit-readiness review;
  - `repo-review` for repository snapshot, range, PR, release, or review-package review.
- Identify Web, Console, or Tauri Desktop.
- Identify React, Vue Composition, Vue Options, or repository-native framework profile.
- Identify only the styling profiles present in scope: Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, or a documented local system.
- Trace route/page, layout, feature owner, analogous implementation, UI primitives, tokens, request/cache, forms/schema, state, tests, docs, and desktop adapter only as required by selected profiles.
- Record direct-reuse, composition/variant, reference-only, unrelated, and `Not found` candidates.

## 2. Profile Selection

Select at least one profile and mark every other profile `Out of scope`:

- Architecture/Reuse
- State/Data/Contracts
- Component/Layout/Design System
- Accessibility
- Performance
- Desktop Boundary

Do not perform token checks, memoization advice, generic accessibility scanning, or Tauri review merely to make a focused audit look comprehensive.

## 3. Architecture/Reuse Profile

- Route/page files primarily compose rather than own unrelated workflows and transports.
- Business components stay in the feature; UI primitives stay business-neutral.
- Hooks/composables, services, stores, schemas, and types each own a real responsibility.
- Existing routes, components, variants, helpers, services, stores, schemas, tests, and docs were searched before recommending new layers.
- Dependency direction, public contracts, generated files, aliases, exports, tests, CI/build/deploy, architecture docs, project maps, and indexes remain synchronized.
- Add/reuse/move/rename/delete work has a complete structural lifecycle and stale-reference search.

## 4. State/Data/Contracts Profile

- Server/cache, URL, form, shared business, local UI, and native IPC state have distinct owners.
- One source of truth is not mirrored into another without an explicit synchronization contract.
- Requests, cache, schemas, errors, retry, cancellation, stale response, optimistic behavior, and feedback states follow existing project mechanisms.
- Public component, route, schema, request, response, and IPC contracts remain compatible or have an explicit migration.

- Apply the selected rules from `framework-profiles.md`; do not apply another framework's semantics.

## 5. Component/Layout/Design-System Profile

- Existing primitives, variants, tokens, layouts, tables, dialogs, forms, toasts, and feedback components are reused.
- Page-edge spacing, scrolling, breakpoints, panel bounds, and CSS declarations have one owner.
- Flexbox handles one-dimensional layout and Grid handles real two-dimensional layout.
- Wrappers own semantics, layout, state, accessibility, animation, or reuse; otherwise flatten them.
- No copied component system, duplicated token scale, repeated margin patch, or competing CSS mechanism exists in scope.
- Apply only the detected rules from `styling-systems.md`, including Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, or shadcn/ui when present.
- Runtime visual/responsive evidence is requested through `ops-browser` or `ops-client` when static evidence is insufficient.

## 6. Accessibility Profile

- Semantic elements, accessible names, labels, descriptions, and error associations are correct.
- Keyboard operation and visible focus cover interactive controls.
- Dialog, popover, menu, and focus-return behavior is verified.
- Status and validation do not rely on color alone.
- Loading, progress, errors, and async completion are communicated appropriately.
- Claims requiring rendered behavior are backed by browser/client evidence or marked `Not verified`.

## 7. Performance Profile

- Define the render/reactivity/data/request/bundle/IPC path being evaluated.
- Require measurement, request counts, profile evidence, or explicit complexity before memoization, computed/cache, virtualization, batching, or bundle changes.
- Check list bounds, request deduplication, cancellation, subscription fan-out, stale work, and long tasks.
- For Vue, inspect watcher/reactive fan-out, Pinia subscriptions, keep-alive refresh behavior, and request loops.
- For React, inspect render boundaries, context/store subscriptions, effects, and cache/request ownership.
- Do not treat component/file size as performance evidence.

## 8. Desktop-Boundary Profile

- Tauri pages use a typed frontend adapter or service.
- Commands expose stable transport DTOs and errors and delegate business logic to Rust owners.
- Long tasks expose real progress, cancellation, terminal states, cleanup, and listener lifecycle.
- Menus, shortcuts, windows, and platform behavior use real-client evidence when claimed.
- Frontend typing, command registration, and capability config do not substitute for native authorization or validation.

## 9. Validation and Read-Only Boundary

- Run only repository-defined non-mutating format checks, lint, typecheck, focused tests, builds, and generated-route checks relevant to selected profiles.
- Use `ops-browser` for browser/runtime evidence and `ops-client` for real desktop-window evidence.
- Report exact failures and `Not verified` gaps.
- Leave source files, generated files, docs, index, checkout, refs, branches, PRs, and remote state unchanged.
- Route accepted fixes to `implement-frontend`.
- Return specialist findings to the coordinating review owner.
- `repo-delivery` alone performs authorized staging, commit, rebase/squash, push, or cleanup.

## 10. Final Report

- State product/framework profile.
- State selected and excluded audit profiles.
- State delegated boundary and coordinating owner when applicable.
- Lead with severity-ranked findings.
- Include exact location, evidence, impact, remediation direction/owner, and validation gap.
- Summarize inspected candidates, ownership, selected profile evidence, structural/documentation drift, runtime evidence, and residual risks.
