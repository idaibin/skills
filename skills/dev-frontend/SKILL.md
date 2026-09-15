---
name: dev-frontend
description: "Use when an authorized frontend change must be implemented or refactored; owns frontend source edits and risk-matched validation, not audit-only work, UI specification, browser/client operation, or Git delivery."
---

# Frontend Implementation

## Entry Gate

Implement the smallest authorized frontend slice in the existing stack. Read effective guidance, current Worktree, target route/component, and only applicable Product/UI/DESIGN authorities. Stop when a decisive behavior or visual contract is unresolved.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any frontend source change | [checklist](references/checklist.md), [stack guidelines](references/stack-guidelines.md), and [framework profiles](references/framework-profiles.md) | Reuse-first implementation |
| No-op or accepted-baseline confirmation | [checklist](references/checklist.md) | Exact owner-symbol and baseline-check evidence |
| Behavior/public seam, ownership, or quality concern applies | [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), and/or [code quality](references/code-quality.md) | Scoped design/validation |
| Styling, tokens, component, layout, motion, or visual-direction change applies | [styling systems](references/styling-systems.md), [CSS governance](references/frontend-css-governance.md), [components/tokens](references/ui-components-and-tokens.md), [layout](references/frontend-layout-governance.md), [motion](references/interaction-motion-quality.md), and/or [visual direction](references/visual-direction-and-anti-slop.md) | Visual implementation contract |
| Selected-source visual closure applies | [specification authorities](references/specification-authorities.md) and [visual evidence](references/frontend-visual-evidence.md) | Two-pass evidence boundary |
| API/protocol or cross-boundary signal applies | [OpenAPI governance](references/openapi-contract-governance.md), [protocol contracts](references/protocol-contracts.md), and/or [project grounding](references/project-grounding.md) | Qualified integration work |

## Invariants

- Reuse the nearest maintained owner before creating; preserve routing, state/data, component, and styling ownership.
- A no-op confirmation still reads and reports the exact owner path and symbol plus its matching contract before running the current-baseline focused check.
- Keep Product behavior and UI visual readiness independent; source/build evidence does not prove browser/client/runtime acceptance.
- Do not generate visual assets, operate browser/client state, review, or mutate Git.

## Output Map

Report scope, authorities, reuse decision, selected profiles, changed files/contracts, focused validation, visual evidence state when applicable, exclusions, and gaps.

## Reference Map

- Read [checklist](references/checklist.md), [stack guidelines](references/stack-guidelines.md), and [framework profiles](references/framework-profiles.md) for baseline implementation.
- Load each condition-specific reference named in the Route Map only when its condition applies.
- Read [frontend visual gate example](references/frontend-visual-gate-example.md) only when constructing visual evidence.
- Read [usage](references/usage.md) for triggers and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
