# Frontend Implementation Usage

## Summary

Use `frontend-implementation` as the first frontend coding skill after repository context is known. It covers UI changes, forms, tables, dashboards, responsive fixes, component organization, desktop-webview UI, and structural DOM/CSS cleanup while preserving the current app's stack and contracts.

## Best For

- Implementing a UI fix without changing unrelated layout.
- Adding or changing forms, tables, modals, drawers, settings pages, or dashboards.
- Cleaning confused imports, duplicate component paths, oversized page files, or unclear component boundaries.
- Simplifying nested markup, animation-only wrappers, repeated utilities, duplicated CSS, or over-specified styles without redesigning the page.
- Converging shell/content/page/panel/scroll structure after repeated layout patches.
- Moving logic into existing hooks, services, helpers, features, commands, or types.
- Reviewing a frontend diff for layout ownership, component-system drift, stack mixing, or contract changes.
- Choosing between utility classes, design tokens, CSS modules, local components, Ant Design, or shadcn/ui based on the current app.
- Improving Tauri/Electron webview UI code while leaving real-window proof to `ops-client`.

## Trigger Examples

- `Fix this React page without changing the layout.`
- `Add this form to the existing AntD page using current patterns.`
- `Build this admin table page using the existing filters, table, and empty/error patterns.`
- `This Vite page has messy imports and component organization; clean only what is needed.`
- `Simplify this component: too many nested divs and repeated CSS rules.`
- `Review whether this frontend change uses the minimum useful DOM and CSS.`
- `Clean up this page structure: shell, content container, animation wrapper, and page root are all fighting overflow.`
- `Merge this animation wrapper into the semantic page root and keep one scroll owner.`
- `Move these scattered width utilities into one layout class or CSS variable.`
- `Replace h-[22px] and w-[88px] with project scale utilities or named CSS owners.`
- `Review whether this frontend diff mixed shadcn and AntD incorrectly.`
- `Use the existing Tailwind style conventions; do not redesign the page.`
- `Add a table action but preserve the current route and permission behavior.`
- `Fix this Tauri settings UI, but keep native commands behind the existing IPC layer.`

## Non-Triggers

- Repository onboarding or command discovery; use `code-context`.
- Large future planning before implementation; use `code-planner`.
- Root-cause diagnosis before a fix is known; use `diagnose`.
- Git diff ownership, staging, or commit planning; use `code-review`.
- Browser screenshots, console, network, uploads, downloads, account state, or runtime checks; use `ops-browser`.
- Real desktop-client launch, process, CGWindowID, or native runtime evidence; use `ops-client`.

## Output

Report branch, detected stack, files and UI surface touched, layout ownership model, patterns reused, DOM/CSS simplification choices, contracts preserved, validation run, failed commands, visual/client verification status, and `Not verified` areas.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`.
