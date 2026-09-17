---
name: ui-spec
description: "Turn selected visual evidence into a UI Feature Spec or shared DESIGN.md contract; not image generation or implementation."
---

# UI Specification

## Purpose

Produce an implementation-ready UI contract without replacing Product, shared design,
component/source, runtime-evidence, or delivery authority. This file is a routing map:
after selecting a branch, read only its referenced modules.

## Entry Gate

- Require either a source-grounded candidate brief or a selected/accepted visual
  source; otherwise stop as `evidence-incomplete`.
- Read effective repository guidance and current Worktree status before an authorized
  artifact write.
- Keep Product behavior, Feature UI Markdown, adopted `DESIGN.md`, component source,
  runtime evidence, and Git delivery as separate authorities.

## Route Map

| Request state | Load | Result |
| --- | --- | --- |
| Applicability or source selection is unclear | [usage](references/usage.md) and [visual source](references/visual-source.md) | Resolve scope/source or stop |
| Direction is exploratory and unapproved | [candidate direction](references/candidate-visual-direction.md) | Ignored local candidate spec plus synchronized complete generation prompt; `DESIGN.md` unchanged; `Not Ready` |
| A page, flow, or accepted surface is selected | [workflow](references/workflow.md) and [documentation boundaries](references/documentation-boundaries.md) | Feature Spec and per-slice readiness |
| Shared visual semantics are being adopted or changed | [DESIGN.md contract](references/design-md-contract.md) | Approved, linted `<design-root>/DESIGN.md`; Feature Specs reference it |
| Several independent surfaces are in scope | [multi-surface](references/multi-surface.md) | Shared index plus independently loadable slices/verdicts |

## Invariants

- Candidate handoffs bind candidate spec/prompt revisions and hashes. Accepted-contract
  handoffs and evidence bind the accepted comparison-basis revision.
- Do not invent product behavior, exact values, assets, component ownership, rights,
  runtime facts, or shared semantics. Tag unknowns with the defined evidence level.
- Do not duplicate shared tokens or component interfaces in a Feature Spec, introduce
  a parallel Registry/schema, or force `DESIGN.md` adoption for an unchanged local
  slice.
- A structured projection is conditional: use it only when a named owner, producer,
  non-LLM consumer, semantic version, executable validator, drift policy, and retirement rule
  already exist.
- Do not operate external AI, generate/edit images or SVG source, edit product source,
  operate browser/client state, or mutate Git. Route those actions to their owners.
- `Ready` covers only UI visual/interaction readiness. It is not Product approval,
  implementation, review, runtime, delivery, deployment, or production proof.

## Output Map

Return `ui.contract.specify@1.1.0` with lifecycle/profile, source identity and rights,
authority disposition, slice IDs, applicable layout/state/interaction/accessibility and
asset contracts, delta/evidence references, comparison basis, per-slice readiness, and
named gaps. Candidate output additionally returns both ignored paths/hashes and handoff
status. Store task-local evidence under verified ignored `.codex/artifacts/`. Include
DESIGN, viewport, SVG, or runtime-evidence fields only when the corresponding
module was activated.

## Reference Map

Load a module only when its condition applies:

| Condition | Module |
| --- | --- |
| Visual direction, theme, color, Preserve/Overhaul choice | [visual direction](references/visual-direction-and-anti-slop.md) |
| An accepted/candidate source names a scene archetype | [scene archetypes](references/scene-archetypes.md) |
| Layout ownership, inset, overlay, focus, hit order, or transition changes | [layout and interaction](references/frontend-layout-governance.md) |
| Repeated source measurements need normalization | [measurement normalization](references/measurement-normalization.md) |
| SVG/icon roles or fallback are part of acceptance | [SVG icon contract](references/svg-icon-system.md) |
| Current runtime is compared with a selected source | [visual evidence](references/frontend-visual-evidence.md) |
| Final readiness is being decided | [evaluation rubric](references/evaluation-rubric.md) |

Maintainers use [eval cases](references/eval-cases.md) for regression work; do not load
them during ordinary UI specification.
