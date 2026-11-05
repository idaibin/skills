# Multi-Surface UI Contracts

Use this reference only when one task covers multiple pages, flows, or business domains.

## Scope Gate

- A **surface** is a separate reachable page, modal, panel, or embedded UI region.
- A **flow** is one connected user job whose states and acceptance can be evaluated together.
- A **domain** owns distinct behavior, data, permissions, failure semantics, or acceptance.

Several requested pages stay in one slice only when they share the same flow, state model,
implementer, and acceptance. Home, tasks, contacts, and profile are independent domains by
default unless facts prove they are one domain.

## Shared Index Scope

| Scope | Required artifact |
| --- | --- |
| One page/flow | One Feature Spec contract |
| Multiple connected surfaces in one domain | One domain-level Feature Spec contract |
| Multiple independent domains with shared visual rules | One short shared index + one independently loadable Feature Spec per domain |
| Shared token/component semantic change across slices | Design System Spec update to the project-declared shared visual authority |

The shared index contains only source identity, the shared visual authority link and accepted
revision, inventory, per-slice links, per-slice status, exclusions, and dependencies.
Do not copy shared visual rules into the index.

Each slice contract must include:

1. selected source identity and boundaries (`use`/`ignore`)
2. hierarchy, regions, and responsive behavior
3. states, transitions, feedback ownership, overflow, and loading/error/empty/success paths
4. keyboard/focus, reduced-motion, localization, and accessibility rules
5. component mapping and acceptance checks with per-slice blockers

## Consumer Read Order

Read only this order when implementing one slice:

1. effective repository guidance and declared authority paths or exceptions
2. applicable product foundation/index facts and target product slice
3. project-declared shared visual guidance and relevant source owners
4. shared UI index (for multi-slice tasks only)
5. target UI slice contract

Do not require sibling slice contracts for implementation.

## Readiness and Partial Results

Evaluate every requested slice independently.

- Emit `Ready for dev-frontend <slice>` only when that slice passes all gates.
- Unconfirmed slices remain listed in the shared index with blockers.
- One incomplete slice does not block unrelated ready slices.
- Mark overall result `Partial` only when it contains both ready and blocked slices,
  as defined by the [readiness checklist](evaluation-rubric.md#end-of-work-readiness-checklist).
- Mark overall result `Complete` only when all requested slices are ready.

## Design System Change Gate for Multi-Slice

When a request requires shared token/component change:

- Resolve the affected shared contract and consumers, then update that existing owner.
- Apply [the profile gate](workflow.md#profile-gate): project-native checks by default,
  Google lint/diff only for explicit format adoption, and strict completeness only
  when the project or an accepted consumer requires that policy.
- Preserve existing acceptance and approval requirements. Missing required evidence
  blocks the dependent slices, not unrelated surfaces.

No additional machine artifact is required for this gate.
