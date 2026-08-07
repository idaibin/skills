# UI Specification Evaluation Rubric

## Hard Blockers

Reject when any applicable blocker is present:

1. no selected visual source or accepted baseline exists;
2. the resolved `<design-root>/DESIGN.md` is missing;
3. source identity, revision, selection, approval, rights, `use`, or `ignore` is unknown;
4. product behavior, permissions, route data, or acceptance claims are invented;
5. a material source vs product fact conflict remains unresolved;
6. pixels are treated as proof of exact tokens, runtime state, accessibility, or ownership;
7. required state/rule coverage is missing without justification (loading, empty, error,
   populated, permission, focus, responsive, overflow, localization, reduced motion);
8. shared semantics are copied into Feature Spec instead of referenced from `<design-root>/DESIGN.md`;
9. official DESIGN.md lint on `<design-root>/DESIGN.md` reports errors;
10. an update to an existing shared visual authority lacks lint/diff evidence or has an unresolved regression;
11. implementation/runtimes are claimed without owning evidence;
12. a required tooling call is blocked but the affected slice is marked `Ready`.
13. critical actions, scroll/overlay ownership, state geometry, or long-content and
    intermediate-width behavior can materially affect task completion but lack an
    acceptance rule or justified exclusion.

## Weighted Score

| Dimension | Points |
| --- | ---: |
| Product truth and boundaries | 15 |
| Selected-source fidelity | 15 |
| Layout and hierarchy | 10 |
| Interaction and required states | 15 |
| Responsive/accessibility contract | 15 |
| Component/token mapping | 15 |
| Engineering fit | 10 |
| Evidence completeness | 5 |

Pass requires at least 85/100, no hard blocker, and at least 11/15 in product truth,
selected-source fidelity, interaction/states, responsive/accessibility, and mapping.

## Deterministic Evidence

Use source identity, product facts, and resolved `<design-root>/DESIGN.md` as primary checks, then gate shared changes by:

- official DESIGN.md lint result
- official DESIGN.md diff result and regression status
- per-slice source coverage and per-slice readiness

Mark runtime execution, console/network screenshots, and deployment as `Not verified` unless
owned by the implementation and operations workflow.

## End-of-Work Readiness Checklist

Every applicable Feature Spec must pass each binary item before `Ready for dev-frontend <slice>`.
Report each item by name; do not collapse them into a prose `Ready` label.

| # | Item | Check |
| --- | --- | --- |
| 1 | Selected source fixed | source identity, revision, approval, and rights/use recorded |
| 2 | DESIGN.md resolved | `<design-root>/DESIGN.md` exists or is created and validated under named human approval |
| 3 | DESIGN.md lint | official lint reports zero errors on `<design-root>/DESIGN.md` |
| 4 | Delta table complete | every material visual difference has a row with acceptance ID, source target, current runtime, target contract, priority, owner, evidence IDs, verification, and asset owner/fallback |
| 5 | Viewport matrix complete | every required viewport/state entry is present with no missing required items; justified exclusions are named |
| 6 | P1 asset owner | every P1 asset has an accepted owner or fallback |
| 7 | Required state coverage | loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules are present or justified-excluded |
| 8 | Evidence levels | every claim uses `source-extracted`, `browser-computed`, `visually-inferred`, `proposed`, or `Not verified`; no untagged claim |

Evaluate the eight items in numeric order:

1. If an item fails, stop at that item, report its number and name, and return
   `Not Ready`.
2. If all eight pass but one or more explicitly non-blocking claims remain
   `Not verified`, report the first such gap and return `Partial`.
3. Return `Ready for dev-frontend <slice>` only when all eight pass and no
   `Not verified` gap remains.

A blocking `Not verified` condition must fail its owning checklist item; it cannot be
downgraded to `Partial`.
