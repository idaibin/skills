---
name: frontend-implementation
description: Use when implementing, modifying, or reviewing frontend UI, routes, components, forms, tables, dashboards, responsive behavior, or frontend architecture while preserving the existing stack, design system, state, API contracts, and verification flow.
---

# Frontend Implementation

## Overview

Implement frontend changes with clear UI intent, existing design-system alignment, maintainable structure, and explicit verification. Use this after repository context is clear; route browser evidence to `ops-browser` and real desktop-window proof to `ops-client`.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing.
3. Inspect only the target page, route, component, service, hook, style, and shared UI files needed for the requested change.
4. Classify the existing UI system before editing: Ant Design, shadcn/ui, Tailwind-only, CSS modules, styled components, project-local components, or a deliberate mix.
5. Preserve current typography, spacing, radius, density, routing, state, API contracts, accessibility, and visual system unless the task explicitly asks to change them.
6. Implement with the smallest component and style surface that matches existing patterns.
7. Run project-defined type, lint, test, build, formatter, or route checks that match the change.
8. Use `ops-browser` for web visual, responsive, interaction, console, network, or route evidence when UI behavior changes; use `ops-client` when desktop-client runtime proof is required.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **UI consistency review:** inspect a frontend diff for component-system, import, style, layout, and route drift.
- **Stack alignment:** decide how to use React, Vue, Next.js, Vite, TanStack Router, Tailwind, Ant Design, shadcn/ui, desktop webviews, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `code-context`.
- Future task decomposition or multi-agent implementation planning; use `code-planner`.
- Dirty-tree ownership, mixed-hunk review, staging, or commit planning; use `code-review`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.

## Hard Rules

- Do not assume Tailwind, Ant Design, shadcn/ui, React Router, Zustand, Redux, React Query, or form libraries are available; verify from the project.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Do not mix Ant Design and shadcn/ui within the same feature unless the existing page already does so deliberately.
- Do not invent new colors, shadows, radius values, spacing scales, button styles, fake metrics, fake sections, or dashboard claims.
- Do not rewrite layouts, spacing, copy, color palette, navigation, component hierarchy, table density, or form density unless the task asks for that change.
- Keep page files thin when the project already uses services, hooks, types, helpers, or feature components.
- Preserve route paths, query parameters, payload shapes, response unwrapping, loading states, and permission-hidden entries unless the task requires changes.
- Prefer existing icons, tokens, utility classes, components, and file naming over new conventions.
- Use semantic HTML and accessible controls: actions are buttons, navigation is links, fields have labels, and focus states remain visible.
- For admin/dashboard work, prioritize compact information hierarchy over marketing-style hero sections or decorative card layouts.
- For desktop webview UI, keep native APIs behind IPC/command wrappers and validate inputs before invoking native commands.
- Mark unchecked visual, responsive, console, network, or accessibility behavior as `Not verified`.

## Output Contract

Report the branch, detected stack, touched UI surface, preserved boundaries, implementation choices, commands run, failed commands, browser/client evidence or `Not verified` gaps, and any intentionally excluded layout or stack changes.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for Vite, React, Tailwind, Ant Design, and shadcn/ui boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
