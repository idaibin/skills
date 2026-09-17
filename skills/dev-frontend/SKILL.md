---
name: dev-frontend
description: "Implement frontend UI changes in the existing stack. Use repo-review for review-only requests."
---

# Frontend Implementation

## Entry Gate

Implement the smallest authorized frontend slice in the existing stack. Read effective guidance, current Worktree, target route/component, and only applicable Product/UI/DESIGN authorities. Stop when a decisive behavior or visual contract is unresolved.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any frontend source change | Applicable sections of [checklist](references/checklist.md) | Reuse-first implementation |
| Toolchain, dependencies, routing, stack migration, or render/effect semantics change | Relevant section of [stack guidelines](references/stack-guidelines.md) | Stack-specific constraints |
| Framework state, lifecycle, routing, or component API semantics change | Selected [framework profile](references/framework-profiles.md) | Framework-compatible change |
| No-op or accepted-baseline confirmation | [checklist](references/checklist.md) | Exact owner-symbol and baseline-check evidence |
| Behavior/public seam, ownership, or quality concern applies | [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), and/or [code quality](references/code-quality.md) | Scoped design/validation |
| A touched file, component, or function mixes independent UI, state, data, side-effect, or business responsibilities | [decomposition](references/decomposition.md) | Cohesive owners and readable orchestration |
| Styling system or CSS ownership changes | [styling systems](references/styling-systems.md) or [CSS governance](references/frontend-css-governance.md) for the changed concern | Scoped styling |
| Shared components/tokens or layout ownership changes | [components/tokens](references/ui-components-and-tokens.md) or [layout](references/frontend-layout-governance.md) | Applicable visual contract |
| Animation or visual direction changes | [motion](references/interaction-motion-quality.md) or [visual direction](references/visual-direction-and-anti-slop.md) | Applicable interaction/visual contract |
| Selected-source visual closure applies | [specification authorities](references/specification-authorities.md) and [visual evidence](references/frontend-visual-evidence.md) | Runtime comparison boundary |
| API/protocol or cross-boundary signal applies | [OpenAPI governance](references/openapi-contract-governance.md), [protocol contracts](references/protocol-contracts.md), and/or [project grounding](references/project-grounding.md) | Qualified integration work |

## Invariants

- Reuse the nearest maintained owner before creating; preserve routing, state/data, component, and styling ownership.
- Treat size as a review signal, not a line-count rule; split only at a stable ownership, behavior, lifecycle, side-effect, or verification boundary.
- A no-op confirmation still reads and reports the exact owner path and symbol plus its matching contract before running the current-baseline focused check.
- Use the lowest-cost evidence closest to the changed behavior: source/diff checks, an already-running development surface with hot reload, focused tests, then a full production build only when its boundary or the delivery stage requires it.
- Keep Product behavior and UI visual readiness independent; source/build evidence does not prove browser/client/runtime acceptance.
- Do not generate visual assets, operate browser/client state, review, or mutate Git.
- Return this phase's evidence to the coordinator, who continues already-authorized
  runtime acceptance, fixes, and delivery through their owners. An owner switch alone
  requires neither a new task/subagent nor renewed approval.

## Output Map

Report scope, authorities, reuse decision, selected profiles, changed files/contracts, focused validation, development-surface evidence and production-build status independently when applicable, exclusions, and gaps.

## Reference Map

- Read only applicable [checklist](references/checklist.md) sections for baseline implementation; use the Route Map for stack and framework detail.
- Load each condition-specific reference named in the Route Map only when its condition applies.
- Read [frontend visual gate example](references/frontend-visual-gate-example.md) only when constructing visual evidence.
- Read [usage](references/usage.md) for triggers and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
