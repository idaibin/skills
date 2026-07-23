---
name: dev-frontend
description: "Use when a frontend change must be implemented or refactored across UI, state, data, styling, accessibility, performance, or desktop integration; owns source edits and validation, but no staging, commit, push, or other Git delivery."
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Detect the actual framework before applying framework-specific rules. Use `ops-browser` for web runtime evidence and `ops-client` for real desktop-window proof.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Identify the frontend project class, app boundary, package manager, runtime pin, script contract, directory/naming standard, and documented exceptions.
3. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing. When an accepted `ui-spec` package exists, verify its revisions and consume its selected-source identity, fact boundary, tokens, component map, state contract, and acceptance checks.
4. Read the approved requirement/specification when one exists. Confirm acceptance criteria, non-goals, affected contracts/files, and validation seams; for complex work without a usable specification, use the host's built-in planning and effective repository instructions before editing.
5. Consume a current `repo-map` inventory or perform a targeted search for existing routes, UI, state, services, tests, and analogous implementations. For API callers, follow the repository's existing client/type authority. Load the protocol-contract profile only when an OpenAPI/generated-client chain already exists or the task explicitly introduces one.
6. Decide in order: directly reuse, adapt the nearest reference, or create new. Record why existing candidates are insufficient before adding a file or abstraction.
7. Inspect only the selected target and reference files needed for the requested change.
8. Classify the existing UI system and layout model: product surface, framework, component library, state/data stack, styling system, shell/content/page boundaries, panels, and scroll regions.
9. Select exactly one framework profile per edited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles actually present, such as **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, or **shadcn/ui**.
10. Preserve typography, spacing, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly changes them. Do not duplicate a DTO or endpoint already owned by the repository's client/type authority.
11. When behavior is stable and a durable public seam exists, confirm that seam, then work one external behavior at a time: run one red-capable check, make the minimum green change, and continue as a vertical tracer bullet. Load `references/behavior-first.md`; do not force it onto exploratory visuals, generated code, or behavior without an honest seam.
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
- Planning-only requests without authorized frontend source changes; use the host's built-in planning.
- Shared cross-functional business language/rule or lifecycle conflicts; use `domain-modeling`. Route feature-local behavior, states, and acceptance to `product-spec`.
- UI specification, selected-source translation, shared visual contracts, task briefs, tokens, mappings, or acceptance rules without source edits; use `ui-spec`.
- Dirty-tree ownership, mixed-hunk review, staging plans, or commit readiness; use `repo-review`.
- Actual staging, commit creation, rebase/squash, push, or delivery; use `repo-delivery` after review.
- Systematic frontend architecture, reuse, state/data, accessibility, performance, or Tauri-boundary audit without requested edits; use `audit-frontend`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.
- Diagnosis-only requests without authorized frontend source changes; use the host's built-in diagnosis under effective instructions.

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
- Keep asynchronous query states distinct before applying empty defaults. Preserve
  last successful data during background refresh failures when the repository's
  cache contract does so, and make non-submit actions inside forms explicitly
  `type="button"` or the framework-native equivalent.
- Preserve the repository's API authority and nullability, optionality, enums, IDs,
  dates, money, pagination, auth, success, and error semantics. When an existing or
  explicitly requested OpenAPI/generated-client profile applies, use its generator
  and do not hand-maintain touched DTOs or endpoint paths.
- Apply only the selected framework and styling references. Preserve framework-native state, lifecycle, routing, component contracts, cleanup, and styling ownership without cross-applying another profile.
- Keep `lint`, `typecheck`, `test`, `check`, and formatting validation non-mutating; use an explicit fix/write command when source rewrites are intended.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.
- Report OpenAPI gates only when that profile applies; otherwise mark them `Not
  applicable`, not `Not verified`.

## Output Contract

Report the branch, frontend project class, detected framework/profile and toolchain, existing implementations checked, direct reuse or reference candidate, new-file justification when applicable, touched UI surface, structural lifecycle updates, layout and outer-spacing owners, state/reactivity/store ownership, component/injection/router/lifetime contracts, cleanup and cancellation behavior, Flex/Grid decision, DOM/CSS simplification choices, preserved contracts, commands run, failed commands, browser/client evidence or `Not verified` gaps, and intentionally excluded stack changes. If the user explicitly requests independent external review/research, hand one fixed basis/question to `ask-chatgpt`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only for an existing or explicitly requested OpenAPI/generated-client chain.
- See [references/behavior-first.md](references/behavior-first.md) when a stable public seam supports vertical red-green slices.
- See [references/codebase-design.md](references/codebase-design.md) only when the change materially affects a public module/interface, seam, cross-caller abstraction, or testability.
- See [references/framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native framework rules.
- See [references/styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack rules.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for toolchain, routing, layout, and desktop-webview boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
