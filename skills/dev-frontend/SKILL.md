---
name: dev-frontend
description: "Use when a frontend change must be implemented or refactored across UI, state, data, styling, build/tooling, accessibility, performance, or desktop integration; owns source edits and validation, not audit-only, browser-only, UI-spec, or Git-delivery work."
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Detect the actual framework before applying framework-specific rules. Use `ops-browser` for web runtime evidence and `ops-client` for real desktop-window proof.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Identify the frontend project class, app boundary, package manager, runtime pin, script contract, directory/naming standard, and documented exceptions.
3. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing. Load `references/specification-authorities.md`, resolve applicable product and UI authorities by meaning rather than filename, and read only the shared facts/indexes and target slice contracts needed for this change.
4. Confirm acceptance criteria, non-goals, affected contracts/files, and validation seams from usable approved requirements. Consume existing contracts directly; hand unresolved product decisions to `product-spec` or required selected-source/shared visual decisions to `ui-spec` without treating either Skill as a file detector. For complex work without a usable specification, use the host's built-in planning and effective repository instructions before editing.
5. Consume a current `repo-map` inventory or perform a targeted search for existing routes, UI, state, services, tests, and analogous implementations. For API callers, follow the repository's existing client/type authority. Load the protocol-contract profile only when an OpenAPI/generated-client chain already exists or the task explicitly introduces one.
6. Decide in order: directly reuse, adapt the nearest reference, or create new. Record why existing candidates are insufficient before adding a file or abstraction.
7. Inspect only the selected target and reference files needed for the requested change.
8. Classify the existing UI system and layout model: product surface, framework, component library, state/data stack, styling system, shell/content/page boundaries, panels, and scroll regions. When layout geometry, spacing, sizing, overflow, scrolling, layering, or responsive behavior is material, load `references/frontend-layout-governance.md` and identify the affected owners and task-completion seam.
9. Select exactly one framework profile per edited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles actually present, such as **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, or **shadcn/ui**.
10. Preserve typography, spacing, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly changes them. Do not duplicate a DTO or endpoint already owned by the repository's client/type authority.
11. When behavior is stable and a durable public seam exists, confirm that seam, then work one external behavior at a time: run one red-capable check, make the minimum green change, and continue as a vertical tracer bullet. Load `references/behavior-first.md`; do not force it onto exploratory visuals, generated code, or behavior without an honest seam.
12. Implement with the smallest component, DOM, CSS, and ownership surface that matches existing patterns. When the change materially involves duplication, dead/unused code, abstraction, coupling, or maintainability, load `references/code-quality.md` with implementation semantics and remove only code made obsolete by this task.
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
- Preserve existing user-visible behavior and repository-owned route, state, data,
  accessibility, and visual contracts unless the task explicitly changes them.
- Load and apply only the selected framework, styling, build/tooling, protocol,
  behavior-first, conditional code-quality, or codebase-design references. Do
  not cross-apply another stack profile.
- Keep `lint`, `typecheck`, `test`, `check`, and formatting validation non-mutating; use an explicit fix/write command when source rewrites are intended.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.
- Report OpenAPI gates only when that profile applies; otherwise mark them `Not
  applicable`, not `Not verified`.
- Do not add speculative shared layers, default memoization, export-style
  rewrites, or bundler migrations as incidental cleanup. Do not delete
  apparently unused frontend code until route, dynamic import, framework
  registration, build, test, and external-consumer reachability is resolved.

## Output Contract

Report the branch, detected project class/stack and selected profiles, existing implementations checked, reuse or new-surface decision, changed files and ownership/contracts, validation status, and intentionally excluded changes. Mark lint/runtime behavior as `Not verified` unless executed in scope; add detailed layout, state, protocol, desktop, or lifecycle evidence only when that profile materially affected the task. If the user explicitly requests independent external review/research, hand one fixed basis/question to `ask-chatgpt`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/specification-authorities.md](references/specification-authorities.md)
  when resolving product requirements, root `DESIGN.md`, slice UI contracts, and
  owner handoffs before implementation.
- See [references/frontend-layout-governance.md](references/frontend-layout-governance.md)
  when geometry, spacing, sizing, overflow, scrolling, layering, or responsive
  behavior is material to the change.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only for an existing or explicitly requested OpenAPI/generated-client chain.
- See [references/behavior-first.md](references/behavior-first.md) when a stable public seam supports vertical red-green slices.
- See [references/codebase-design.md](references/codebase-design.md) only when the change materially affects a public module/interface, seam, cross-caller abstraction, or testability.
- See [references/framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native framework rules.
- See [references/styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack rules.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for toolchain, routing, layout, and desktop-webview boundaries.
- See [references/code-quality.md](references/code-quality.md) when the requested
  change materially involves duplication, dead/unused code, abstraction
  quality, hidden coupling, or maintainability.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
