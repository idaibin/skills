# Frontend Implementation Usage

## Summary

Use `frontend-implementation` as the first frontend coding skill. It covers UI changes, forms, tables, dashboards, responsive fixes, component organization, frontend architecture, and desktop-webview UI code while preserving the current app's design system and contracts.

## Best For

- Implementing a UI fix without changing unrelated layout.
- Adding or changing forms, tables, modals, drawers, settings pages, or dashboards.
- Cleaning confused imports, duplicate component paths, or oversized page files.
- Simplifying nested markup, wrapper components, repeated CSS, or over-specified styles without redesigning the page.
- Moving logic into existing hooks, services, helpers, features, commands, or types.
- Reviewing a frontend diff for layout drift or UI-stack mixing.
- Choosing between Tailwind utilities, design tokens, CSS modules, local components, Ant Design, or shadcn/ui based on the current app.
- Improving Tauri/Electron webview UI code while leaving real-window proof to `ops-client`.

## Trigger Examples

- `Fix this React page without changing the layout.`
- `Add this form to the existing AntD page using current patterns.`
- `Build this admin table page using the existing filters, table, and empty/error patterns.`
- `This Vite page has messy imports and component organization; clean only what is needed.`
- `Simplify this component: too many nested divs and repeated CSS rules.`
- `Review whether this frontend change uses the minimum useful DOM and CSS.`
- `Review whether this frontend diff mixed shadcn and AntD incorrectly.`
- `Use the existing Tailwind style conventions; do not redesign the page.`
- `Add a table action but preserve the current route and permission behavior.`
- `Refactor this page so services/hooks/types follow the existing structure.`
- `Fix this Tauri settings UI, but keep native commands behind the existing IPC layer.`

## Non-Triggers

- Repository onboarding or command discovery; use `code-context`.
- Large future planning before implementation; use `code-planner`.
- Git diff ownership, staging, or commit planning; use `code-review`.
- Browser screenshots, console, network, uploads, downloads, account state, or runtime checks; use `ops-browser`.
- Real desktop-client launch, process, CGWindowID, or native runtime evidence; use `ops-client`.

## Output

Report branch, detected stack, files and UI surface touched, patterns reused, design/architecture decisions, validation run, failed commands, visual/client verification status, and `Not verified` areas.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`.
