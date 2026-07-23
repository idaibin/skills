# UI Specification Workflow

## Contents

1. Visual source gate
2. Evidence boundary
3. Profile gate
4. Specification pass
5. Artifact pass
6. Evaluation and handoff

## Visual Source Gate

Require one selected source: a user-selected Product Design result, supplied screenshot/mockup/frame, accepted current surface, or accepted shared-system revision. Record its stable identity, revision, selection/approval status, rights status, `use`, and `ignore` rules. If the user still needs alternatives, image generation, redesign, critique, or an exploratory prototype, stop and route that work to the host's Product Design capability when available.

A visual source proves appearance only. It does not prove exact tokens, component ownership, product behavior, API data, accessibility, responsive behavior, or runtime state. Resolve conflicts in favor of verified product facts and accepted live owners; do not silently repair the source by invention.

## Evidence Boundary

Record confirmed product facts, available data/actions/states, current component and token owners, explicit exclusions, unresolved questions, and the source revision. Mark each specification decision `verified`, `extracted`, `proposed`, or `Not verified`.

## Profile Gate

Choose **Feature Spec** unless at least one answer is yes:

- Must a shared semantic token be added, removed, or redefined?
- Must a reusable component's meaning, public variant contract, or state vocabulary change?
- Must several surfaces adopt a changed shared rule?
- Is an accepted shared-system owner being created, extracted, maintained, or evaluated?

If not, reference existing owners and keep the specification local. If yes, load the Design System Spec artifact contract and change only the shared closure. Artifact presence does not prove acceptance: pending, rejected, or stale manifests locate candidates only; verify live owners before reuse and require approval before promotion.

## Specification Pass

Translate the selected source into implementable decisions:

- page regions, hierarchy, layout/scroll/focus ownership, dimensions, density, overflow, and target sizes;
- semantic colors, typography roles, spacing, geometry, surfaces, assets, copy, and localization behavior;
- current components/tokens to `reuse`, bounded adaptations, and justified new declarations;
- loading, empty, error, populated, permission, validation, success, disabled, hover, focus, and reduced-motion behavior where applicable;
- state transitions, action ownership, feedback placement, and precedence between independent async domains;
- responsive reflow, touch/keyboard targets, contrast, semantic structure, and acceptance assertions.

Do not infer exact CSS values or behavior from pixels alone. Trace exact values to live source or an accepted contract; otherwise label them proposed and require acceptance before implementation.

## Artifact Pass

| Profile | Primary artifact | Optional dependencies |
| --- | --- | --- |
| Feature Spec | one page/flow implementation specification | source annotations, component/token mapping, state matrix, acceptance checklist |
| Design System Spec | changed accepted shared contract | affected tokens/components, references, evaluation, rollback manifest |

Produce only what removes a real implementation ambiguity. Use a shared manifest only when establishing or changing an accepted Design System Spec revision.

## Evaluation And Handoff

Run source identity, product truth, rights, required-state, mapping, responsive, accessibility, overflow, approval, and implementation-budget gates first. Then compare source fidelity, task completion, information structure, interaction completeness, engineering fit, and evidence completeness. Hand accepted artifacts and unresolved gaps to `dev-frontend`; request runtime evidence from `ops-browser` or `ops-client` after implementation.
