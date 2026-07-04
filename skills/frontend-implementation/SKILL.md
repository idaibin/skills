---
name: frontend-implementation
description: Use when implementing, modifying, or reviewing frontend applications, especially Vite, React, Tailwind, Ant Design, or shadcn/ui projects, where the agent must preserve existing layout, component systems, imports, styling conventions, routes, state, and validation flow.
---

# Frontend Implementation

## Overview

Implement frontend changes while respecting the application's existing stack, layout, component boundaries, and verification path. Use this after repository context is clear and before browser/runtime verification.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Identify the actual frontend stack from manifests, config, lockfiles, routes, styles, component imports, and existing pages.
3. Inspect only the target page, route, component, service, hook, style, and shared UI files needed for the requested change.
4. Classify the existing UI system before editing: Ant Design, shadcn/ui, Tailwind-only, CSS modules, styled components, project-local components, or a deliberate mix.
5. Preserve current layout, spacing, routing, state, API contracts, and visual system unless the task explicitly asks to change them.
6. Implement with the smallest component and style surface that matches existing patterns.
7. Run project-defined type, lint, test, build, formatter, or route checks that match the change.
8. Use `ops-browser` for visual, interaction, console, network, or responsive evidence when UI behavior changes.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **UI consistency review:** inspect a frontend diff for component-system, import, style, layout, and route drift.
- **Stack alignment:** decide how to use Vite, React, Tailwind, Ant Design, shadcn/ui, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `code-context`.
- Future task decomposition or multi-agent implementation planning; use `code-planner`.
- Dirty-tree ownership, mixed-hunk review, staging, or commit planning; use `code-review`.
- Browser operation, screenshots, console, network, or responsive evidence collection; use `ops-browser`.
- Desktop-client window proof for Tauri, Electron, or native apps; use `ops-client`.

## Hard Rules

- Do not assume Tailwind, Ant Design, shadcn/ui, React Router, Zustand, Redux, React Query, or form libraries are available; verify from the project.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Do not mix Ant Design and shadcn/ui within the same feature unless the existing page already does so deliberately.
- Do not rewrite layouts, spacing, copy, color palette, navigation, or component hierarchy unless the task asks for that change.
- Keep page files thin when the project already uses services, hooks, types, helpers, or feature components.
- Preserve route paths, query parameters, payload shapes, response unwrapping, loading states, and permission-hidden entries unless the task requires changes.
- Prefer existing icons, tokens, utility classes, components, and file naming over new conventions.
- Mark unchecked visual, responsive, console, network, or accessibility behavior as `Not verified`.

## Output Contract

Report the detected stack, touched UI surface, preserved boundaries, implementation choices, validation commands, browser evidence or `Not verified` gaps, and any intentionally excluded layout or stack changes.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, `references/checklist.md`, `references/stack-guidelines.md`, and `agents/openai.yaml` with trigger, stack, boundary, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for Vite, React, Tailwind, Ant Design, and shadcn/ui boundaries.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
