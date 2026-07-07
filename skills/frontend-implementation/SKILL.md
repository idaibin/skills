---
name: frontend-implementation
description: Use when implementing, modifying, or reviewing frontend UI, routes, components, forms, tables, dashboards, responsive behavior, DOM/CSS structure, layout ownership, scroll boundaries, or frontend architecture while preserving the existing stack, design system, state, API contracts, and verification flow.
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Use this after repository context is clear; route browser evidence to `ops-browser` and real desktop-window proof to `ops-client`.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing.
3. Inspect only the target page, route, component, service, hook, style, shared UI, and layout owner files needed for the requested change.
4. Classify the existing UI system and layout model: component library, utility/CSS strategy, shell/content/page boundaries, panels, and scroll regions.
5. Preserve typography, spacing, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly asks to change them.
6. Implement with the smallest component, DOM, CSS, and ownership surface that matches existing patterns.
7. Remove stale wrappers, duplicate declarations, late overrides, and temporary layout patches made obsolete by the change.
8. Run matching project-defined checks, then use `ops-browser` or `ops-client` when runtime UI evidence is required.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **Structure and style simplification:** reduce wrapper DOM, repeated utilities, duplicated CSS, unclear layout ownership, and competing scroll/overflow rules.
- **UI consistency review:** inspect a frontend diff for component-system, import, style, layout, ownership, and route drift.
- **Stack alignment:** decide how to use React, Vue, Next.js, Vite, TanStack Router, Tailwind, Ant Design, shadcn/ui, desktop webviews, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `code-context`.
- Future task decomposition or multi-agent implementation planning; use `code-planner`.
- Dirty-tree ownership, mixed-hunk review, staging, or commit planning; use `code-review`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.
- Root-cause diagnosis before a frontend fix is known; use `diagnose`.

## Hard Rules

- Verify the actual stack before using Tailwind, Ant Design, shadcn/ui, React Router, Zustand, Redux, React Query, form libraries, icon libraries, or routing helpers.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Keep layout ownership explicit: app/window shell owns chrome and global clipping; content containers own inset; page roots own page layout; panels own panel bounds; inner regions own scrolling or overflow.
- Do not stack repeated `h-full`, `min-h-0`, `overflow-*`, padding, inset, or width rules across nested shell/content/page/panel layers.
- Collapse wrappers that only pass classes, hold one child, duplicate a component boundary, or exist only for animation. When safe, make the animated node the semantic page root.
- Prefer semantic HTML, existing components, component props, natural document flow, cascade, and inheritance over redundant wrappers, repeated declarations, and one-off overrides.
- Use project scale utilities for ordinary Tailwind sizing and spacing, such as `h-1`, `h-12`, or `w-22` when available; do not use arbitrary pixel utilities such as `h-[22px]` for routine dimensions.
- Use one named layout class or CSS variable for business-specific geometry such as split-pane widths; keep utility classes for ordinary spacing and icon sizing only when they match the local scale.
- Consolidate duplicate CSS declarations at the nearest owning selector or component, then delete stale patch rules and late overrides that shadow earlier design-system rules.
- Preserve route paths, query parameters, payload shapes, response unwrapping, loading states, permission-hidden entries, and accessibility behavior unless the task requires changes.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.

## Output Contract

Report the branch, detected stack, touched UI surface, layout ownership changes, DOM/CSS simplification choices, preserved contracts, commands run, failed commands, browser/client evidence or `Not verified` gaps, and any intentionally excluded layout or stack changes.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for Vite, React, Tailwind, Ant Design, and shadcn/ui boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
