# Frontend Implementation Checklist

Use this checklist when implementing or reviewing frontend changes.

## Required Context

- Read relevant repo guidance first.
- Run `git status --short` before edits.
- Identify actual package manager, scripts, frontend app boundary, target screen, route, component, framework, UI type, visual source, and style system.
- Inspect only target page, component, route, service, hook, type, style, and shared UI files needed for the request.
- Check existing imports before adding libraries, aliases, icons, helpers, or components.

## Stack And Structure

- Confirm whether the project uses React, Vue, Next.js, Vite, TanStack Router, TypeScript, Tailwind, Ant Design, shadcn/ui, CSS modules, Less/Sass, desktop webviews, project-local components, or a deliberate mix.
- Keep page files consistent with existing thickness: do not move logic unless the local pattern already uses hooks, services, helpers, or feature components.
- Put new files in the established layer: `pages`, `views`, `routes`, `components`, `features`, `hooks`, `services`, `api`, `types`, `utils`, or project-specific equivalents.
- Reuse existing request helpers, response unwrap helpers, route builders, permission checks, form wrappers, table wrappers, and modal/drawer patterns.
- Preserve path aliases and import ordering conventions.
- Keep local UI state local; introduce global state or new data libraries only when the existing app already requires that pattern.

## Layout And Styling

- Preserve existing layout, spacing, breakpoints, typography, palette, copy, nav, and component hierarchy unless requested.
- Do not introduce a new UI kit, theme provider, global CSS reset, Tailwind config, token system, icon library, radius scale, shadow style, or button style for a local change.
- Prefer existing tokens, class utilities, component props, and style files over one-off inline styles.
- Avoid mixing Ant Design and shadcn/ui inside one feature unless that mix already exists and is intentional.
- Avoid adding decorative UI, landing-page patterns, or marketing-style composition to operational/admin pages unless requested.
- Use semantic controls: buttons for actions, links for navigation, labels for fields, and visible focus states.
- For admin/dashboard pages, preserve table density, form density, filter placement, row actions, pagination, and loading/empty/error states.

## Behavior And Contracts

- Preserve routes, query params, hash behavior, permission-hidden entries, payload fields, response shapes, loading states, and error handling unless the task targets them.
- Trace API changes through request helper, service, type, caller, and page state.
- Keep form validation, controlled state, table pagination, sorting, filtering, modal lifecycle, and drawer lifecycle aligned with existing local patterns.
- Do not silently change date, currency, locale, enum, or status-display semantics.
- For Tauri/Electron UI, keep shell, file, platform, and native API access behind existing IPC/command wrappers and surface command errors in the UI.

## Validation

- Run project-defined type, lint, test, build, formatter, or route checks that match the change.
- Use `ops-browser` when visual layout, interaction, responsive behavior, console errors, network payloads, or route behavior need web evidence.
- Use `ops-client` when the task requires proof from a real Tauri, Electron, or native desktop window.
- Mark unchecked runtime, visual, responsive, console, network, accessibility, or permission behavior as `Not verified`.

## Review

- Check for duplicate imports, unused imports, dead components, parallel helper layers, inconsistent aliases, uncontrolled layout changes, and accidental global style impact.
- Check that every changed line belongs to the requested frontend change.
- Route final dirty-tree review and staging to `code-review`; route push or squash delivery to `code-delivery`.
