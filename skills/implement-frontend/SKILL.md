---
name: implement-frontend
description: "Use when a frontend change must be implemented or refactored across UI, state, data, styling, accessibility, performance, or desktop integration; owns source edits and validation, but no staging, commit, push, or other Git delivery."
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Detect the actual framework before applying framework-specific rules. Use `ops-browser` for web runtime evidence and `ops-client` for real desktop-window proof.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Identify the frontend project class, app boundary, package manager, runtime pin, script contract, directory/naming standard, and documented exceptions.
3. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing. When an accepted `design-ui` package exists, verify its revisions and consume its fact boundary, tokens, component map, and acceptance contract.
4. Read the approved requirement/specification when one exists. Confirm acceptance criteria, non-goals, affected contracts/files, and validation seams; for complex work without a usable specification, stop and route planning to `code-planner`.
5. Consume a current `repo-map` inventory or perform the same targeted search for existing routes, pages, layouts, components, hooks or composables, services, stores, shared UI, tests, and analogous implementations.
6. Decide in order: directly reuse, adapt the nearest reference, or create new. Record why existing candidates are insufficient before adding a file or abstraction.
7. Inspect only the selected target and reference files needed for the requested change.
8. Classify the existing UI system and layout model: product surface, framework, component library, state/data stack, styling system, shell/content/page boundaries, panels, and scroll regions.
9. Select exactly one framework profile per edited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles actually present, such as **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, or **shadcn/ui**.
10. Preserve typography, spacing, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly asks to change them.
11. When behavior is stable enough to specify and a durable public seam exists, work in behavior-first vertical slices: one failing test or executable check, the minimum implementation, then the next slice. Do not force TDD onto exploratory visuals, generated code, or behavior without a reliable seam.
12. Implement with the smallest component, DOM, CSS, and ownership surface that matches existing patterns.
13. Update manifests, scripts, routes, tests, docs, indexes, generated route files, and stale references when adding, reusing, moving, renaming, or deleting structural frontend code.
14. Remove stale wrappers, duplicate declarations, late overrides, and temporary layout patches made obsolete by the change.
15. Run focused checks after each slice, then matching project-defined gates; use `ops-browser` or `ops-client` when runtime UI evidence is required.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **Structure and style simplification:** reduce wrapper DOM, repeated utilities, duplicated CSS, unclear layout ownership, and competing scroll/overflow rules.
- **Implementation self-check:** verify the edited frontend surface for component-system, import, style, layout, ownership, route, and framework-native state drift.
- **Stack alignment:** decide how to use React, Vue, Next.js, Vite, TanStack Router, Vue Router, Tailwind, Ant Design, shadcn/ui, desktop webviews, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `repo-map`.
- Future task decomposition or multi-agent implementation planning; use `code-planner`.
- Business terminology, lifecycle, or invariant modeling; use `domain-modeling` before planning when those questions remain unresolved.
- UI direction, project profiles, reference responsibilities, task briefs, tokens, or evaluation contracts without source edits; use `design-ui`.
- Dirty-tree ownership, mixed-hunk review, staging plans, or commit readiness; use `repo-review`.
- Actual staging, commit creation, rebase/squash, push, or delivery; use `repo-delivery` after review.
- Systematic frontend architecture, reuse, state/data, accessibility, performance, or Tauri-boundary audit without requested edits; use `audit-frontend`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.
- Root-cause diagnosis before a frontend fix is known; use `diagnose`.

## Hard Rules

- Verify the actual stack before using Tailwind, Ant Design, shadcn/ui, React Router, Vue Router, Pinia, Zustand, Redux, React Query, Vue Query, form libraries, icon libraries, or routing helpers.
- Follow repository-pinned Node/package-manager versions, lockfile, dependency policy, script names, directory names, and file naming. Do not upgrade or normalize them during unrelated UI work.
- Keep framework-native structure: use the repository's React Router `routes`, Next.js `app`, Astro `pages`, Vue Router/views or feature convention, or documented equivalent. Preserve existing naming until alignment is explicit.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Do not create a page, component, hook, composable, helper, service, store, wrapper, or shared abstraction before checking the `repo-map` inventory and performing a targeted file/symbol search.
- Create a new implementation only when reuse or adaptation would violate ownership or behavior. State the reason and place it in the existing directory and naming convention.
- Keep layout ownership explicit: app/window shell owns chrome and global clipping; content containers own the page's outer inset; page roots own page layout; components own only their internal spacing; panels own panel bounds; inner regions own scrolling or overflow.
- Keep the shortest valid layout path. Every wrapper must own semantics, layout, state, accessibility, animation, or reuse; flatten nested elements that do not.
- Prefer Flexbox for one-dimensional row/column layout and Grid for genuinely two-dimensional layout.
- Do not repeat page-edge margin, padding, inset, height, width, or overflow rules across shell/content/page/component layers.
- Prefer semantic HTML, existing components, component props, natural document flow, cascade, and inheritance over redundant wrappers and one-off overrides.
- Use project scale utilities for ordinary sizing and spacing; put real product geometry into named classes, tokens, variants, or CSS variables.
- Preserve route paths, query parameters, payload shapes, response unwrapping, loading states, permission-hidden entries, and accessibility behavior unless the task requires changes.
- Apply only the selected framework and styling references. Preserve framework-native state, lifecycle, routing, component contracts, cleanup, and styling ownership without cross-applying another profile.
- Keep `lint`, `typecheck`, `test`, `check`, and formatting validation non-mutating; use an explicit fix/write command when source rewrites are intended.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.

## Output Contract

Report the branch, frontend project class, detected framework/profile and toolchain, existing implementations checked, direct reuse or reference candidate, new-file justification when applicable, touched UI surface, structural lifecycle updates, layout and outer-spacing owners, state/reactivity/store ownership, component/injection/router/lifetime contracts, cleanup and cancellation behavior, Flex/Grid decision, DOM/CSS simplification choices, preserved contracts, commands run, failed commands, browser/client evidence or `Not verified` gaps, and intentionally excluded stack changes.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/tdd.md](references/tdd.md) for behavior-first seam selection and vertical red-green slices.
- See [references/framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native framework rules.
- See [references/styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack rules.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for toolchain, routing, layout, and desktop-webview boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
