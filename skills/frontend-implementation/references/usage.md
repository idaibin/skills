# Frontend Implementation Usage

## Summary

Use `frontend-implementation` for frontend code changes where consistency matters more than inventing a new UI approach. It covers Vite, React, Tailwind, Ant Design, shadcn/ui, routes, components, hooks, services, types, and styles.

## Best For

- Implementing a UI fix without changing page layout.
- Adding a component to an existing Ant Design or shadcn/ui page.
- Cleaning confused imports or duplicate component paths.
- Moving logic into existing hooks, services, helpers, or types.
- Reviewing a frontend diff for layout drift or UI-stack mixing.
- Choosing between Tailwind utilities, design tokens, CSS modules, local components, Ant Design, or shadcn/ui based on the current app.

## Trigger Examples

- `Fix this React page without changing the layout.`
- `Add this form to the existing AntD page using current patterns.`
- `This Vite page has messy imports and component organization; clean only what is needed.`
- `Review whether this frontend diff mixed shadcn and AntD incorrectly.`
- `Use the existing Tailwind style conventions; do not redesign the page.`
- `Add a table action but preserve the current route and permission behavior.`
- `Refactor this page so services/hooks/types follow the existing structure.`

## Non-Triggers

- Repository onboarding or command discovery; use `code-context`.
- Large future planning before implementation; use `code-planner`.
- Git diff ownership, staging, or commit planning; use `code-review`.
- Browser screenshots, console, network, or responsive checks; use `ops-browser`.
- Real desktop-client evidence; use `ops-client`.

## Output

Report the detected stack, files and UI surface touched, patterns reused, layout and style boundaries preserved, validation run, browser verification status, and `Not verified` areas.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
