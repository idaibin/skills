# UI Specification Workflow

## Contents

1. Visual source gate
2. Evidence boundary
3. UI contract challenge
4. Profile gate
5. Specification pass
6. Artifact pass
7. Evaluation and handoff

## Visual Source Gate

Require one selected source: a user-selected Product Design result, supplied screenshot/mockup/frame, accepted current surface, or accepted shared-system revision. Record its stable identity, revision, selection/approval status, rights status, `use`, and `ignore` rules. If the user still needs alternatives, image generation, redesign, critique, or an exploratory prototype, stop and route that work to the host's Product Design capability when available.

A visual source proves appearance only. It does not prove exact tokens, component ownership, product behavior, API data, accessibility, responsive behavior, or runtime state. Resolve conflicts in favor of verified product facts and accepted live owners; do not silently repair the source by invention.

## Evidence Boundary

Record confirmed product facts, available data/actions/states, current component and token owners, explicit exclusions, unresolved questions, and the source revision. Mark each specification decision `verified`, `extracted`, `proposed`, or `Not verified`.

## UI Contract Challenge

After product facts and the selected visual source are fixed, resolve repository and
source evidence before asking a question. Challenge only a remaining decision that can
change layout or ownership, component/token mapping, required states or interaction,
responsive/accessibility behavior, or an executable UI acceptance result.

Ask one bounded question at a time. Include the recommended answer, reason, principal
trade-off, and affected slice. Stop when the slice passes its UI contract gates; do not
traverse its product decision tree or reopen accepted visual direction. Route behavior,
permission, failure semantics, or product acceptance to `product-spec`, and route
visual alternatives or an unselected direction to Product Design.

## Profile Gate

Choose **Feature Spec** unless at least one answer is yes:

- Must a shared semantic token be added, removed, or redefined?
- Must a reusable component's meaning, public variant contract, or state vocabulary change?
- Must several surfaces adopt a changed shared rule?
- Is an accepted shared-system owner being created, extracted, maintained, or evaluated?

If not, reference existing owners and keep the specification local. If yes, open and update the repo root `DESIGN.md` directly and change only the shared closure. Artifact presence does not prove acceptance: pending, rejected, or stale candidates are not proof; verify live owners before reuse and require approval before promotion.

## Specification Pass

Translate the selected source into implementable decisions:

- page regions, hierarchy, layout/scroll/focus ownership, dimensions, density, overflow, and target sizes;
- semantic colors, typography roles, spacing, geometry, surfaces, assets, copy, and localization behavior;
- current components/tokens to `reuse`, bounded adaptations, and justified new declarations;
- loading, empty, error, populated, permission, validation, success, disabled, hover, focus, and reduced-motion behavior where applicable;
- state transitions, action ownership, feedback placement, and precedence between independent async domains;
- responsive reflow, touch/keyboard targets, contrast, semantic structure, and acceptance assertions.

For the primary task, specify only applicable task-completion geometry: critical
actions, scroll and overlay ownership, intermediate-width behavior, state geometry,
long content/localization, and focus/zoom/touch behavior. Treat exact measurements as
verified only when an accepted authority provides them; otherwise mark them proposed
or `Not verified`.

Do not infer exact CSS values or behavior from pixels alone. Trace exact values to live source or an accepted contract; otherwise label them proposed and require acceptance before implementation.

## Artifact Pass

| Profile | Primary artifact | Optional dependencies |
| --- | --- | --- |
| Feature Spec, one slice | `docs/ui/<slice-id>/spec.md` | source annotations, component/token mapping, state matrix, acceptance checklist |
| Feature Spec, multiple domains | one short shared UI index plus one independently loadable contract per confirmed domain | only shared facts and per-slice links/status in the index |
| Design System Spec | repo root `DESIGN.md` (the only shared visual artifact) | feature-spec references and relevant owner approvals |

For multiple surfaces, apply [the multi-surface scope gate](multi-surface.md). Produce
only what removes a real implementation ambiguity. The shared System update should be
single-sourced in root `DESIGN.md`; do not create or maintain a separate Design System
manifest in this path.

## Lint And Diff Gates

The official lint and diff gates require external tool access and network authorization.
Run lint for every root `DESIGN.md`. Run diff against the previous accepted file for an
update; record diff as `Not applicable` for the first accepted creation instead of
inventing a baseline. If a required tool cannot run, mark the gate `Not verified` and
keep the readiness result `Not Ready`.

## Evaluation And Handoff

Run source identity, product truth, rights, required-state, mapping, responsive,
accessibility, overflow, approval, and implementation-budget gates per slice. Then
compare source fidelity, task completion, information structure, interaction
completeness, engineering fit, and evidence completeness. Emit one readiness verdict
per slice and mark an incomplete multi-surface result `Partial`. Hand accepted
artifacts and unresolved gaps to `dev-frontend`; request runtime evidence from
`ops-browser` or `ops-client` after implementation.
