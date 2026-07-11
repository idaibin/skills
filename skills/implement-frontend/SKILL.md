---
name: implement-frontend
description: Use when implementing or modifying frontend UI, routes, components, forms, tables, dashboards, responsive behavior, DOM/CSS structure, layout ownership, scroll boundaries, or frontend architecture while preserving the existing stack, design system, state, API contracts, and verification flow.
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Detect the actual framework before applying framework-specific rules. Use `ops-browser` for web runtime evidence and `ops-client` for real desktop-window proof.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Identify the frontend project class, app boundary, package manager, runtime pin, script contract, directory/naming standard, and documented exceptions.
3. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing.
4. Consume a current `code-context` inventory or perform the same targeted search for existing routes, pages, layouts, components, hooks or composables, services, stores, shared UI, tests, and analogous implementations.
5. Decide in order: directly reuse, adapt the nearest reference, or create new. Record why existing candidates are insufficient before adding a file or abstraction.
6. Inspect only the selected target and reference files needed for the requested change.
7. Classify the existing UI system and layout model: framework, component library, state/data stack, utility/CSS strategy, shell/content/page boundaries, panels, and scroll regions.
8. Select the framework profile and preserve its native ownership model:
   - **React:** components, hooks, effects, context/store, route/data boundaries.
   - **Vue 3:** SFCs and the repository's `<script setup>`, Composition, or Options API style; ref/reactive/computed state; composables; Pinia or local stores; Router; component contracts; dependency injection; and lifecycle/scope cleanup.
   - **Other:** follow the repository's established native conventions and mark unsupported assumptions `Not verified`.
9. Preserve typography, spacing, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly asks to change them.
10. Implement with the smallest component, DOM, CSS, and ownership surface that matches existing patterns.
11. Update manifests, scripts, routes, tests, docs, indexes, generated route files, and stale references when adding, reusing, moving, renaming, or deleting structural frontend code.
12. Remove stale wrappers, duplicate declarations, late overrides, and temporary layout patches made obsolete by the change.
13. Run matching project-defined checks, then use `ops-browser` or `ops-client` when runtime UI evidence is required.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **Structure and style simplification:** reduce wrapper DOM, repeated utilities, duplicated CSS, unclear layout ownership, and competing scroll/overflow rules.
- **Implementation self-check:** verify the edited frontend surface for component-system, import, style, layout, ownership, route, and framework-native state drift.
- **Stack alignment:** decide how to use React, Vue, Next.js, Vite, TanStack Router, Vue Router, Tailwind, Ant Design, shadcn/ui, desktop webviews, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `code-context`.
- Future task decomposition or multi-agent implementation planning; use `code-planner`.
- Dirty-tree ownership, mixed-hunk review, staging plans, or commit readiness; use `code-review`.
- Actual staging, commit creation, rebase/squash, push, or delivery; use `code-delivery` after review.
- Systematic frontend architecture, reuse, state/data, accessibility, performance, or Tauri-boundary audit without requested edits; use `audit-frontend`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.
- Root-cause diagnosis before a frontend fix is known; use `diagnose`.

## Hard Rules

- Verify the actual stack before using Tailwind, Ant Design, shadcn/ui, React Router, Vue Router, Pinia, Zustand, Redux, React Query, Vue Query, form libraries, icon libraries, or routing helpers.
- Follow repository-pinned Node/package-manager versions, lockfile, dependency policy, script names, directory names, and file naming. Do not upgrade or normalize them during unrelated UI work.
- Keep framework-native structure: use the repository's React Router `routes`, Next.js `app`, Astro `pages`, Vue Router/views or feature convention, or documented equivalent. Preserve existing naming until alignment is explicit.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Do not create a page, component, hook, composable, helper, service, store, wrapper, or shared abstraction before checking the `code-context` inventory and performing a targeted file/symbol search.
- Create a new implementation only when reuse or adaptation would violate ownership or behavior. State the reason and place it in the existing directory and naming convention.
- Keep layout ownership explicit: app/window shell owns chrome and global clipping; content containers own the page's outer inset; page roots own page layout; components own only their internal spacing; panels own panel bounds; inner regions own scrolling or overflow.
- Keep the shortest valid layout path. Every wrapper must own semantics, layout, state, accessibility, animation, or reuse; flatten nested elements that do not.
- Prefer Flexbox for one-dimensional row/column layout and Grid for genuinely two-dimensional layout.
- Do not repeat page-edge margin, padding, inset, height, width, or overflow rules across shell/content/page/component layers.
- Prefer semantic HTML, existing components, component props, natural document flow, cascade, and inheritance over redundant wrappers and one-off overrides.
- Use project scale utilities for ordinary sizing and spacing; put real product geometry into named classes, tokens, variants, or CSS variables.
- Preserve route paths, query parameters, payload shapes, response unwrapping, loading states, permission-hidden entries, and accessibility behavior unless the task requires changes.
- For Vue 3, preserve the repository's chosen Composition or Options API style. Do not convert unrelated components to `<script setup>` or Composition API as incidental cleanup.
- For Vue 3 Composition API or `<script setup>`, use `ref`/`reactive` according to local ownership, keep pure derivation in `computed`, give `watch` an explicit source, and use `watchEffect` only for intentional bounded automatic dependencies. Define timing, invalidation, cleanup, cancellation, and loop prevention.
- For Vue 3 Options API, preserve `data`, `computed`, `watch` options or owned `this.$watch`, `methods`, `provide`/`inject`, component Router guards, and `mounted`/`unmounted`/`activated`/`deactivated` lifecycles. Do not require Composition imports or convert the component merely to apply a rule.
- For Vue 3, keep props read-only, define emits explicitly, and preserve `v-model`, slot, provide/inject, Router, guard, and keep-alive contracts. Keep provider/store ownership and native guard registration or teardown visible.
- For Vue 3 composables or Options-owned reusable behavior, make instance versus shared lifetime explicit; clean listeners, timers, subscriptions, guards, and requests at the native scope/component/route/keep-alive boundary; expose stable contracts without mixing API styles incidentally.
- Keep `lint`, `typecheck`, `test`, `check`, and formatting validation non-mutating; use an explicit fix/write command when source rewrites are intended.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.

## Output Contract

Report the branch, frontend project class, detected framework/profile and toolchain, existing implementations checked, direct reuse or reference candidate, new-file justification when applicable, touched UI surface, structural lifecycle updates, layout and outer-spacing owners, state/reactivity/store ownership, component/injection/router/lifetime contracts, cleanup and cancellation behavior, Flex/Grid decision, DOM/CSS simplification choices, preserved contracts, commands run, failed commands, browser/client evidence or `Not verified` gaps, and intentionally excluded stack changes.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for stack-specific boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
