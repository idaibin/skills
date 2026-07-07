# Eval Cases

Use these cases when changing `frontend-implementation` triggers, stack guidance, layout-ownership rules, validation expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Fix this React page without changing the layout.` | Should trigger `frontend-implementation`. | Targeted frontend implementation with layout constraint. |
| `Add this form to the existing AntD page using current patterns.` | Should trigger `frontend-implementation`. | Component-system consistency. |
| `Build this admin table page using the existing filters, row actions, and empty/error states.` | Should trigger `frontend-implementation`. | Admin UI implementation with existing patterns. |
| `This Vite page has messy imports and component organization; clean only what is needed.` | Should trigger `frontend-implementation`. | Frontend organization without broad refactor. |
| `Simplify this component: too many nested divs and repeated CSS rules.` | Should trigger `frontend-implementation`. | DOM and CSS simplification in frontend code. |
| `Review whether this diff uses the minimum useful DOM and CSS.` | Should trigger `frontend-implementation`. | Frontend structure and styling review. |
| `Clean up this page structure: shell, content container, animation wrapper, and page root are all fighting overflow.` | Should trigger `frontend-implementation`. | Layout ownership and DOM boundary cleanup. |
| `Merge this animation wrapper into the semantic page root and keep one scroll owner.` | Should trigger `frontend-implementation`. | Animation wrapper and scroll ownership cleanup. |
| `Move these split-pane widths out of JSX utilities into one layout class.` | Should trigger `frontend-implementation`. | Business geometry ownership cleanup. |
| `Replace h-[22px] and w-[88px] with project scale utilities or named CSS owners.` | Should trigger `frontend-implementation`. | Tailwind arbitrary pixel cleanup. |
| `Review whether this frontend diff mixed shadcn and AntD incorrectly.` | Should trigger `frontend-implementation`. | UI-stack consistency review. |
| `Use the existing Tailwind style conventions; do not redesign the page.` | Should trigger `frontend-implementation`. | Styling convention preservation. |
| `Fix this Tauri settings UI, but keep native commands behind IPC.` | Should trigger `frontend-implementation`. | Desktop webview UI implementation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Plan the frontend rewrite across three apps before anyone edits code.` | Should prefer `code-planner`. | Future cross-scope planning. |
| `Find the root cause before changing any code.` | Should prefer `diagnose`. | Diagnosis before implementation. |
| `Review all dirty changes and propose commit groups.` | Should prefer `code-review`. | Dirty-tree review and staging plan. |
| `Verify this page in the browser and check console/network.` | Should prefer `ops-browser`. | Runtime browser evidence. |
| `Capture the real Electron app window with CGWindowID.` | Should prefer `ops-client`. | Desktop-client evidence. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Stack detection | Reads manifests/config/imports and reports actual stack before choosing Tailwind, Ant Design, shadcn/ui, or local components. | Assumes a library is available because the user named it. |
| Layout preservation | Keeps layout, spacing, routes, copy, and visual system unchanged unless requested. | Redesigns or restyles adjacent UI. |
| Component consistency | Reuses existing components, wrappers, hooks, services, types, icons, aliases, and interaction helpers. | Introduces a parallel UI kit, helper layer, or icon library. |
| DOM minimality | Removes or avoids wrappers, fragments, components, and classes that do not provide layout, semantics, state, accessibility, animation ownership, or reuse value. | Adds nested `div`s or wrapper components only to pass class names or group a single child. |
| Layout ownership | Assigns shell chrome, content inset, page layout, panel bounds, and scroll/overflow to explicit owners without repeated competing rules. | Leaves multiple nested layers declaring the same height, padding, inset, width, or overflow behavior. |
| Animation wrapper collapse | Merges page-transition wrappers into a semantic page root when the wrapper has no independent layout, state, accessibility, or reuse role. | Keeps an animation-only wrapper around an inner container that immediately repeats the page layout class. |
| Scroll ownership | Keeps one main scroll region where practical and prevents headers, sidebars, inspectors, panels, and footers from competing for overflow control. | Uses broad `overflow-visible` or nested scroll patches to hide unclear ownership. |
| CSS minimality | Consolidates repeated declarations and relies on existing tokens, component props, cascade, and inheritance when safe. | Repeats the same CSS across selectors, restates browser defaults, or adds one-off overrides where inheritance or existing styles already work. |
| Tailwind scale discipline | Uses project scale utilities for routine sizing and spacing, and avoids arbitrary pixel utilities like `h-[22px]` for normal UI dimensions. | Leaves routine sizes as arbitrary Tailwind pixel utilities instead of using scale utilities or a named owner. |
| Geometry ownership | Keeps business-specific dimensions in a named layout class or CSS variable while preserving standard utility scale for ordinary sizing. | Scatters split-pane widths, offsets, or complex animation geometry across JSX utilities. |
| Stale patch cleanup | Deletes obsolete wrappers, duplicate class definitions, and late CSS overrides after moving responsibility to the correct owner. | Leaves dead rules or shadowing patches in place after structural cleanup. |
| Contract preservation | Traces and preserves route, query, payload, response, permission, loading, and error behavior. | Changes data contracts silently. |
| Desktop boundary | Keeps native access behind IPC/command helpers and routes real-window proof to `ops-client`. | Calls native APIs directly from generic UI or treats browser preview as desktop proof. |
| Validation | Runs matching project commands and uses `ops-browser` or `ops-client` for UI behavior evidence when needed, or marks gaps `Not verified`. | Claims UI correctness without checks or evidence. |
| Scope control | Changes only files and lines needed for the frontend request. | Performs unrelated cleanup or broad component reorganization. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
