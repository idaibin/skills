# Stack Guidelines

Use these guidelines only after verifying the project actually uses the relevant stack.

## Vite / Next.js / TanStack Router

- Treat `vite.config.*`, `tsconfig.*`, aliases, env prefixes, proxy config, and build targets as project contracts.
- Do not change alias, proxy, base path, env names, or build output paths for a component-level task.
- Preserve route paths, params, loaders/actions, query handling, layouts, and navigation conventions.
- Prefer existing scripts from `package.json`, docs, or repo guidance.

## React / Vue

- Follow the existing component style: function declarations vs arrow components, export style, memoization habits, hook placement, and file naming.
- Keep state close to the component unless existing patterns use global stores, route loaders, query libraries, or feature hooks.
- Avoid adding global state, context providers, or new data libraries for a local page change.
- Preserve effect dependencies and cleanup behavior; do not suppress lint rules casually.

## Tailwind

- Use Tailwind only where the project already uses utility classes for the same UI layer.
- Reuse existing class composition helpers, variants, tokens, breakpoints, and spacing scale.
- Do not add arbitrary values, theme changes, or global utility conventions when existing tokens/classes work.
- Do not fight component-library tokens with Tailwind overrides unless the existing page already uses that pattern.

## Ant Design

- Prefer existing Ant Design wrappers, theme tokens, `ConfigProvider`, table/form/modal/drawer conventions, and locale setup.
- Keep form validation, field names, table pagination, row keys, loading states, and modal lifecycle consistent with nearby code.
- Do not replace Ant Design controls with custom or shadcn/ui controls in an Ant Design page unless requested.
- Avoid brittle CSS overrides against generated class names when props, tokens, or wrapper components exist.

## shadcn/ui

- Use existing generated components and local variant patterns before adding or changing primitives.
- Confirm Radix, Tailwind, `cn`, component paths, and variant utilities before importing.
- Do not re-run generators or alter shared primitives for a single page unless that is the requested scope.
- Do not introduce shadcn/ui into an Ant Design or non-shadcn page without an existing local precedent or explicit request.

## Mixed Stacks

- Treat deliberate mixed stacks as local contracts: follow the page's nearest precedent rather than a global preference.
- Prefer the component system already used in the target feature.
- If a requested change crosses UI systems, state the boundary and keep each side using its existing components and styling.

## Desktop Webviews

- Treat Tauri/Electron frontend code as UI code plus a native boundary.
- Keep shell, file, platform, and process access inside established IPC, command, or platform helper layers.
- Validate inputs before invoking native commands and show native command errors in the UI.
- Use `ops-client` for process, launch-command, CGWindowID, and real-window evidence.
