# Stack Guidelines

Use these guidelines only after verifying the project actually uses the relevant stack.

## Toolchain And Script Contract

- Read `package.json`, lockfiles, workspace config, runtime pinning, and repository guidance before choosing commands or versions.
- Preserve the pinned Node/package-manager and dependency policy unless alignment is the requested task.
- Do not replace reviewed version ranges with `latest`.
- Prefer stable script names such as `dev`, `build`, `lint`, `typecheck`, `test`, and `check` when the repository standard defines them.
- Keep validation scripts read-only. Use explicit `:fix`, format-write, or equivalent commands for rewrites.

## Directory Classes

- React Router SPA projects normally route through their established `routes` layer.
- Next.js App Router projects keep `app`; Astro keeps `pages`; other frameworks keep their native router convention.
- Use repository-defined plural directories and kebab-case for new files when present. Preserve documented legacy naming until an explicit alignment task.
- Do not copy a Tauri, content-site, admin SPA, or web-monorepo layout into another class mechanically.

## Vite / Next.js / TanStack Router

- Treat `vite.config.*`, `tsconfig.*`, aliases, env prefixes, proxy config, and build targets as project contracts.
- Do not change alias, proxy, base path, env names, or build output paths for a component-level task.
- Preserve route paths, params, loaders/actions, query handling, layouts, and navigation conventions.
- Prefer existing scripts from `package.json`, docs, or repo guidance.

## Layout Selection

- Prefer Flexbox for one-dimensional horizontal or vertical composition, including parent-owned alignment and centering.
- Use Grid for real two-dimensional row/column relationships.
- Do not add wrappers only to apply `display`, alignment, centering, or duplicated spacing when the semantic parent can own it.
- Let children fill or contract through the project's grow, shrink, basis, wrapping, and minimum-size conventions; avoid fixed dimensions for naturally adaptive content.
- Keep page-edge spacing at one shell, content, or page owner. Reusable components should not reapply outer margins or padding already supplied by their parent.
- Keep each CSS responsibility in one selector, token, variant, or component prop; remove duplicate and shadowing declarations after consolidation.

## Desktop Webviews

- Treat Tauri/Electron frontend code as UI code plus a native boundary.
- Keep shell, file, platform, and process access inside established IPC, command, or platform helper layers.
- Validate inputs before invoking native commands and show native command errors in the UI.
- Use `ops-client` for process, launch-command, CGWindowID, and real-window evidence.
- Treat frontend files and `src-tauri` as separate ownership boundaries; use `implement-rust` for Rust shell/backend changes.
