---
name: audit-frontend
description: "Use when a known frontend surface needs a scoped, read-only audit of selected architecture, reuse, data/UI contract, accessibility, performance, or desktop-boundary profiles."
---

# Frontend Audit

## Overview

Audit frontend engineering from repository evidence rather than a universal framework or folder template. Detect the real framework and local API style, then select only the profiles required by the request. This skill is read-only: use it directly for frontend domain audits or as a bounded specialist under `repo-review`; use `implement-frontend` for requested changes.

## Rule Priority

Resolve conflicts in this order:

1. The user's current explicit request.
2. Effective repository guidance, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
3. Existing project code, components, and design system.
4. Project documentation and interface contracts.
5. This skill.
6. External reference repositories.

Never rewrite a working local structure merely to match this skill or an external repository.

## Workflow

1. Read repository guidance, run `git status --short`, and identify the target app, project class, framework, package manager, scripts, documented architecture, and coordinating review owner when delegated.
2. Consume current `repo-map` output or perform a targeted inventory of route/page entry, owning feature, analogous screens, UI primitives, layout/tokens, data/cache, forms/schema, state/store, tests, docs, and desktop adapter.
3. Classify the product surface as Web, high-density Console, or Tauri Desktop. Select exactly one framework profile per audited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles present in scope: **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, **shadcn/ui**, or a documented local system.
4. Select one or more audit profiles; explicitly mark the rest `Out of scope`:
   - **Architecture/reuse:** routes, features, shared layers, dependency direction, reuse, abstractions, structural lifecycle, and docs.
   - **State/data/contracts:** server/cache, URL, form, shared business, local UI, reactivity, stores, schemas, requests, errors, cancellation, and native IPC contracts.
   - **Component/layout/design system:** primitives, variants, tokens, density, DOM/CSS, spacing/scroll ownership, responsive behavior, and duplicated systems.
   - **Accessibility:** semantics, keyboard, focus, labels, dialogs/popovers, errors, status communication, and async feedback.
   - **Performance:** render/reactivity/data paths, request duplication, fan-out, bundle/runtime/IPC cost, long tasks, and measurement quality.
   - **Desktop boundary:** frontend adapter, Tauri/native commands, DTO/errors, progress, cancellation, window/menu/shortcut behavior, and real-client evidence.
5. Map each selected responsibility to its page, feature, primitive, hook/composable, service, store, schema, local type, or desktop adapter owner.
6. Compare the target with direct reuse candidates, the nearest analogous feature, documented contracts, and the existing component/layout system.
7. Trace only selected profiles without changing the repository. Do not perform shallow checks for excluded profiles merely to imply coverage.
8. Audit applicable loading, empty, error, partial, retry, optimistic, stale, cancellation, keyboard, focus, and long-task behavior within the selected profiles.
9. Use non-mutating repository checks and request browser or real-client evidence only when a selected claim cannot be proven statically.
10. Report severity-ranked findings with exact location, framework-specific evidence, impact, remediation direction, validation gap, selected profiles, and excluded profiles.

## Modes

- **Focused profile audit:** one or two selected frontend profiles with bounded evidence.
- **Combined frontend audit:** interacting profiles such as state/data plus performance or layout plus accessibility, with explicit integration risk.
- **Baseline architecture audit:** architecture/reuse plus structural lifecycle and docs against real repository conventions.
- **Scoped specialist subreview:** inspect only the frontend paths or diff delegated by `repo-review`; return domain findings without taking review coordination or Git ownership.

## Hard Rules

- Select profiles before applying detailed checklists. Do not imply architecture, state, layout, accessibility, performance, and desktop were all reviewed when only some were evidenced.
- Do not recommend a shared component, hook, composable, store, service, schema, or layout system before searching existing implementations and recording why reuse or adaptation is insufficient.
- Keep route and page files primarily compositional. Move remote access, reusable behavior, business workflows, and cross-screen state to the existing owning boundary; do not create empty layers for visual neatness.
- Keep `components/ui` or its local equivalent business-neutral. Keep business components, types, and state with their feature until a stable cross-feature contract and real consumers justify promotion.
- Use hooks/composables only for real state, effects, subscriptions, lifecycle, or reusable behavior. Use services for remote/native boundaries, schemas for input/contract validation, and global stores only for genuinely cross-tree business state.
- Distinguish server/cache, URL/route, form, shared business, and local UI state. Do not mirror one source of truth into another without a synchronization contract.
- Reuse existing tokens, primitives, variants, layout owners, breakpoints, request/cache mechanisms, forms, toasts, and feedback states. Do not add a parallel system for a local feature.
- Keep DOM and CSS minimal: one owner for page-edge spacing and scrolling, Flexbox for one-dimensional layout, Grid for real two-dimensional layout, adaptive children, no empty wrappers, and no duplicate declarations or margin patches.
- Do not recommend React memoization, Vue computed/cache changes, virtualization, caching, or bundle changes by default. Require a traced path, measurement, request counts, or explicit complexity evidence under the Performance profile.
- Apply only the selected framework and styling references. Do not cross-apply framework semantics or imply coverage of an unselected styling system.
- Keep Tauri pages behind a typed frontend adapter or service. Commands expose stable transport DTOs and errors, delegate business logic to Rust owners, and provide real progress/cancellation for long work.
- Under Accessibility, preserve keyboard operation, visible focus, accessible names, focus management, form labels/errors, and non-color status communication.
- Do not refactor unrelated legacy code. File length alone never justifies splitting.
- Do not edit, stage, commit, post review comments, or deliver code in audit mode. `repo-review` owns Worktree and immutable review coordination; `repo-delivery` alone owns Git mutation. Route accepted remediation to `implement-frontend`.

## Do Not Use For

- Repository orientation, commands, reuse inventory, or docs/code alignment without an audit request; use `repo-map`.
- Frontend implementation, modification, or refactoring; use `implement-frontend`.
- Root-cause diagnosis before a fix is known; use `diagnose`.
- Owning Worktree readiness or immutable repository/range/PR/release coordination; use `repo-review`, which may delegate a bounded frontend surface here.
- Actual staging, commit, rebase/squash, push, or delivery; use `repo-delivery`.
- Browser or real desktop runtime operation; use `ops-browser` or `ops-client`.
- A backend-only Rust implementation or audit; use `implement-rust` or `audit-rust`.

## Output Contract

Start with selected product, framework, styling, and audit profiles; explicitly excluded audit profiles; coordinating owner when delegated; and severity-ranked findings. For each finding, report impact, exact location, profile-specific evidence, recommended remediation owner/direction, and validation gap. Then summarize inspected rules/files, existing candidates, ownership map, selected state/data/layout/accessibility/performance/desktop evidence, component/injection/router/lifetime contracts, structural/documentation drift, commands/runtime evidence, and all `Not found` or `Not verified` residual risks.

## References

- Read [architecture-and-ownership.md](references/architecture-and-ownership.md) for discovery, directories, routes, pages, and file responsibility.
- Read [framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native audit rules.
- Read [component-system.md](references/component-system.md) for primitives, feature components, composition, variants, and reuse decisions.
- Read [state-data-and-forms.md](references/state-data-and-forms.md) for state classes, requests, caching, feedback states, services, schemas, and forms.
- Read [styling-and-layout.md](references/styling-and-layout.md) for tokens, spacing, responsive layout, Console density, DOM, and CSS ownership.
- Read [styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack audit rules.
- Read [desktop-tauri.md](references/desktop-tauri.md) for frontend adapters, commands, Rust boundaries, windows, shortcuts, progress, and cancellation.
- Read [accessibility-and-performance.md](references/accessibility-and-performance.md) for keyboard/focus checks and evidence-based performance review.
- Read [review-checklist.md](references/review-checklist.md) for the profile-driven audit sequence.
- Read [anti-patterns.md](references/anti-patterns.md) for detectable failure patterns and corrective decisions.
- Read [reference-corpus.md](references/reference-corpus.md) for official source evidence, adopted rules, and rejected cargo-cult choices.
- Read [usage.md](references/usage.md) for trigger, routing, and profile examples.
- Read [eval-cases.md](references/eval-cases.md) for trigger, non-trigger, scenario, quality, and scoring evals.
