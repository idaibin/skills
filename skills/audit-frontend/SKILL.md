---
name: audit-frontend
description: "Use when auditing complex or cross-cutting frontend architecture across React, Vue, TypeScript, Vite, router/state/component systems, high-density consoles, and Tauri desktops, or when code-review delegates an explicit frontend surface for a read-only specialist subreview, especially for reuse, ownership, reactivity/state/data boundaries, layout, accessibility, performance, and documentation alignment."
---

# Frontend Audit

## Overview

Audit complex frontend work from repository evidence rather than a universal folder template. Detect the actual framework before applying framework-specific review rules. This skill is read-only: use it directly for domain audits, or as a scoped specialist subreview while `code-review` remains the read-only Git-change review owner. Use `implement-frontend` when the requested outcome includes code changes.

## Rule Priority

Resolve conflicts in this order:

1. The user's current explicit request.
2. The nearest applicable `AGENTS.md` or repository guidance.
3. Existing project code, components, and design system.
4. Project documentation and interface contracts.
5. This skill.
6. External reference repositories.

Never rewrite a working local structure merely to match this skill or an external repository.

## Workflow

1. Read repository guidance, run `git status --short`, and identify the target app, project class, framework, package manager, scripts, and documented architecture.
2. Consume current `code-context` output or perform a targeted inventory of the route/page entry, owning feature, analogous screens, UI primitives, layout and tokens, data/cache, forms/schema, state/store, tests, and docs.
3. Classify the task as Web, high-density Console, or Tauri Desktop, then select the framework profile:
   - **React:** hooks/effects, context/store subscriptions, render boundaries, React Router/Next/TanStack contracts.
   - **Vue 3:** SFC and `<script setup>`/Composition/Options style, ref/reactive/computed/watch/watchEffect, composables, Pinia or local stores, Vue Router/guards, component and provide/inject contracts, keep-alive, lifecycle, scope disposal, and request cancellation.
   - **Other:** use repository-native concepts and mark unsupported assumptions `Not verified`.
4. Map each responsibility to its page, feature, primitive, hook or composable, service, store, schema, or local type owner.
5. Compare the target with direct reuse candidates, the nearest analogous feature, documented contracts, and the existing component/layout system.
6. Trace routing, data, state/reactivity, styling, accessibility, performance, and native boundaries without changing the repository.
7. Audit loading, empty, error, partial, retry, optimistic, stale, cancellation, keyboard, focus, and long-task behavior that applies to the feature.
8. Use non-mutating repository checks and collect browser or real-client evidence when behavior cannot be proven statically.
9. Report findings first with severity, impact, exact location, evidence, recommended owner, remediation direction, and validation gaps.

## Modes

- **Architecture and ownership audit:** review routes, features, shared layers, reuse decisions, dependency direction, docs, and structural lifecycle.
- **Component and layout audit:** review component-system consistency, minimal DOM/CSS, spacing and scroll ownership, responsiveness, and duplicate rules.
- **State, reactivity, and contract audit:** review server, URL, form, shared business, local UI, Vue reactive, and native IPC state plus request/schema/error boundaries.
- **Accessibility and performance audit:** review keyboard/focus behavior, semantics, feedback states, render/reactivity/data paths, evidence, and validation gaps.
- **Scoped specialist subreview:** inspect only the frontend surface delegated by `code-review`; return domain findings and gaps without taking dirty-tree review or Git-mutation ownership or expanding into unrelated files.

## Hard Rules

- Do not recommend a shared component, hook, composable, store, service, schema, or layout system before searching existing implementations and recording why reuse or adaptation is insufficient.
- Keep route and page files primarily compositional. Move remote access, reusable behavior, business workflows, and cross-screen state to the existing owning boundary; do not create empty layers for visual neatness.
- Keep `components/ui` or its local equivalent business-neutral. Keep business components, types, and state with their feature until a stable cross-feature contract and real consumers justify promotion.
- Use hooks/composables only for real state, effects, subscriptions, lifecycle, or reusable behavior. Use services for remote/native boundaries, schemas for input/contract validation, and global stores only for genuinely cross-tree business state.
- Distinguish server/cache, URL/route, form, shared business, and local UI state. Do not mirror one source of truth into another without a synchronization contract.
- Reuse existing tokens, primitives, variants, layout owners, breakpoints, request/cache mechanisms, forms, toasts, and feedback states. Do not add a parallel system for a local feature.
- Keep DOM and CSS minimal: one owner for page-edge spacing and scrolling, Flexbox for one-dimensional layout, Grid for real two-dimensional layout, adaptive children, no empty wrappers, and no duplicate declarations or margin patches.
- Do not recommend React memoization or Vue computed/cache changes by default. Optimize only from a traced render/reactivity/data path, measurement, or explicit complexity evidence.
- For Vue 3 Composition API or `<script setup>`, verify that destructuring, spreads, class instances, third-party objects, and store extraction do not silently break reactivity; require `toRef`, `toRefs`, `storeToRefs`, or another repository-approved pattern only when evidence shows it is needed.
- For Vue 3 Composition API or `<script setup>`, distinguish pure derivation from side effects. Require an explicit source for `watch`; treat `watchEffect` as automatic dependency collection and inspect whether its synchronous dependency window is bounded. Report either only when breadth, timing, cleanup, feedback loops, duplicated state, or network effects create concrete risk.
- For Vue 3 Options API, audit native `data`, `computed`, `watch` options or owned `this.$watch`, `methods`, `provide`/`inject`, component Router guards, and `mounted`/`unmounted`/`activated`/`deactivated` lifecycles. Do not require Composition helpers or recommend conversion merely to apply a rule.
- For Vue 3 composables, identify instance versus shared lifetime, effect scope, listener/timer/request cleanup, SSR assumptions, and whether state is accidentally global.
- For Vue 3, preserve explicit props/emits, `v-model` argument/modifier contracts, slot names and scoped values, typed provide/inject keys/defaults/reactive ownership, route params/meta/guards and registration teardown, keep-alive activation behavior, request cancellation, and async component/error boundaries.
- Keep Tauri pages behind a typed frontend adapter or service. Commands expose stable transport DTOs and errors, delegate business logic to Rust domain owners, and stream progress with cancellation for long work.
- Preserve keyboard operation, visible focus, accessible names, dialog/popover focus behavior, form labels/errors, and non-color status communication.
- Do not refactor unrelated legacy code. No file-length threshold alone can justify splitting; split only when ownership or behavior becomes clearer.
- Do not edit, stage, commit, or deliver code in audit mode. In a changed-tree review, `code-review` owns dirty-file inventory, scope, diff completeness, staging plans, commit readiness, and specialist orchestration without mutating Git; `audit-frontend` may only return a read-only assessment of the explicitly delegated frontend surface. `code-delivery` is the sole owner of actual staging, commit, rebase/squash, push, and delivery. If the user asks to apply a finding, hand the scoped remediation to `implement-frontend`.

## Do Not Use For

- Repository orientation without a frontend task; use `code-context`.
- Frontend implementation, modification, or refactoring; use `implement-frontend`.
- Root-cause diagnosis before a fix is known; use `diagnose`.
- Owning an existing frontend Git change review, dirty-tree classification, staging plan, specialist orchestration, or commit readiness; use `code-review`. A read-only scoped specialist subreview is allowed when `code-review` remains the review owner.
- Actual staging, commit, rebase/squash, push, or delivery; use `code-delivery` after review.
- Browser or real desktop runtime operation; use `ops-browser` or `ops-client`.
- A backend-only Rust implementation or audit; use `implement-rust` or `audit-rust`.

## Output Contract

Start with severity-ranked findings. For each finding, report impact, exact location, framework-specific evidence, recommended owner and remediation direction, and validation gap. Then summarize the audit mode and, for a specialist subreview, the delegated path/diff boundary and `code-review` read-only review owner; project class and framework profile; rules and files inspected; existing candidates; ownership map; state/reactivity/data and native boundaries; component/injection/router/lifetime contracts; layout and token owners; applicable feedback/accessibility/performance states; documentation drift; validation evidence; and `Not verified` residual risks.

## Skill Maintenance

Keep this entry concise. When triggers or rules change, update references, `agents/openai.yaml`, eval cases, README/install indexes, and run `python3 scripts/validate-skills.py`.

## References

- Read [architecture-and-ownership.md](references/architecture-and-ownership.md) for discovery, directories, routes, pages, and file responsibility.
- Read [component-system.md](references/component-system.md) for primitives, feature components, composition, variants, and reuse decisions.
- Read [state-data-and-forms.md](references/state-data-and-forms.md) for state classes, requests, caching, feedback states, services, schemas, and forms.
- Read [styling-and-layout.md](references/styling-and-layout.md) for tokens, spacing, responsive layout, Console density, DOM, and CSS ownership.
- Read [desktop-tauri.md](references/desktop-tauri.md) for frontend adapters, commands, Rust boundaries, windows, shortcuts, progress, and cancellation.
- Read [accessibility-and-performance.md](references/accessibility-and-performance.md) for keyboard/focus checks and evidence-based performance review.
- Read [review-checklist.md](references/review-checklist.md) for the systematic audit sequence.
- Read [anti-patterns.md](references/anti-patterns.md) for detectable failure patterns and corrective decisions.
- Read [reference-corpus.md](references/reference-corpus.md) for official source evidence, adopted rules, and rejected cargo-cult choices.
- Read [usage.md](references/usage.md) for trigger and routing examples.
- Read [eval-cases.md](references/eval-cases.md) for trigger, non-trigger, scenario, quality, and scoring evals.
