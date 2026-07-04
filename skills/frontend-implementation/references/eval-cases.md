# Eval Cases

Use these cases when changing `frontend-implementation` triggers, stack guidance, layout-preservation rules, validation expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Fix this React page without changing the layout.` | Should trigger `frontend-implementation`. | Targeted frontend implementation with layout constraint. |
| `Add this form to the existing AntD page using current patterns.` | Should trigger `frontend-implementation`. | Component-system consistency. |
| `This Vite page has messy imports and component organization; clean only what is needed.` | Should trigger `frontend-implementation`. | Frontend organization without broad refactor. |
| `Review whether this frontend diff mixed shadcn and AntD incorrectly.` | Should trigger `frontend-implementation`. | UI-stack consistency review. |
| `Use the existing Tailwind style conventions; do not redesign the page.` | Should trigger `frontend-implementation`. | Styling convention preservation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Plan the frontend rewrite across three apps before anyone edits code.` | Should prefer `code-planner`. | Future cross-scope planning. |
| `Review all dirty changes and propose commit groups.` | Should prefer `code-review`. | Dirty-tree review and staging plan. |
| `Verify this page in the browser and check console/network.` | Should prefer `ops-browser`. | Runtime browser evidence. |
| `Confirm this Tauri app window is the real client, not a browser preview.` | Should prefer `ops-client`. | Desktop-client evidence. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Stack detection | Reads manifests/config/imports and reports actual stack before choosing Tailwind, Ant Design, shadcn/ui, or local components. | Assumes a library is available because the user named it. |
| Layout preservation | Keeps layout, spacing, routes, copy, and visual system unchanged unless requested. | Redesigns or restyles adjacent UI. |
| Component consistency | Reuses existing components, wrappers, hooks, services, types, icons, and aliases. | Introduces a parallel UI kit, helper layer, or icon library. |
| Mixed stack boundary | Avoids mixing Ant Design and shadcn/ui unless existing local code already does so deliberately. | Adds shadcn controls into an Ant Design feature without precedent. |
| Contract preservation | Traces and preserves route, query, payload, response, permission, loading, and error behavior. | Changes data contracts silently. |
| Validation | Runs matching project commands and uses `ops-browser` for UI behavior evidence or marks gaps `Not verified`. | Claims UI correctness without checks or evidence. |
| Scope control | Changes only files and lines needed for the frontend request. | Performs unrelated cleanup or broad component reorganization. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
