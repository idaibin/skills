# UI Specification Evaluation Rubric

## Hard Blockers

Reject when any applicable blocker is present:

1. no selected visual source or accepted baseline exists;
2. an adopted, first-adoption, or shared-semantics-changing boundary lacks its resolved
   `<design-root>/DESIGN.md`; a local semantics-preserving non-adopted slice records
   `Not applicable` instead;
3. source identity, revision, selection, approval, rights, `use`, or `ignore` is unknown;
4. product behavior, permissions, route data, or acceptance claims are invented;
5. a material source vs product fact conflict remains unresolved;
6. pixels are treated as proof of exact tokens, runtime state, accessibility, or ownership;
7. required state/rule coverage is missing without justification (loading, empty, error,
   populated, permission, focus, responsive, overflow, localization, reduced motion);
8. shared semantics are copied into Feature Spec instead of referenced from `<design-root>/DESIGN.md`;
9. official DESIGN.md lint on `<design-root>/DESIGN.md` reports errors;
10. official lint passes but `ui-spec-design-completeness/1` is `not-ready` or missing
    for a first adoption, adopted shared authority, or Design System Spec;
11. a first-adoption candidate requests human approval before
    `ready-for-human-approval`, or an adopted authority lacks a satisfied downstream
    completeness gate from independently trusted, exact-hash human approval evidence;
12. an update to an existing shared visual authority lacks lint/diff evidence or has an unresolved regression;
13. implementation/runtimes are claimed without owning evidence;
14. a required tooling call is blocked but the affected slice is marked `Ready`.
15. critical actions, scroll/overlay ownership, state geometry, or long-content and
    intermediate-width behavior can materially affect task completion but lack an
    acceptance rule or justified exclusion.
16. SVG icons apply, but semantic roles, actual owner/library, rights, coherent family,
    rendering/state and source-backed coloring rules, accessibility, safe delivery
    constraints, accepted isolated fallback or evidenced `None` disposition, or
    focused acceptance are missing or invented.

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

Use source identity and product facts as primary checks. When shared visual authority
is adopted or changing, also use resolved `<design-root>/DESIGN.md` and gate it by:

- official DESIGN.md lint result
- DESIGN.md completeness policy version/result, token groups or reasoned omissions,
  source hash, and exact approval binding when adopted
- official DESIGN.md diff result and regression status
- per-slice source coverage and per-slice readiness
- applicable SVG icon role/owner/rights mapping plus gallery and same-state runtime
  acceptance status

Mark runtime execution, console/network screenshots, and deployment as `Not verified` unless
owned by the implementation and operations workflow.

## End-of-Work Readiness Checklist

Every applicable Feature Spec must pass each binary item before `Ready for dev-frontend <slice>`.
Report each item by name; do not collapse them into a prose `Ready` label.

| # | Item | Check |
| --- | --- | --- |
| 1 | Selected source fixed | source identity, revision, approval, and rights/use recorded |
| 2 | Shared visual authority disposition | adopted, first-adoption, or not-adopted/not-required is recorded; required DESIGN.md exists |
| 3 | DESIGN.md format | required DESIGN.md lint reports zero errors; otherwise `Not applicable` |
| 4 | DESIGN.md completeness | required shared authority passes its lifecycle gate; otherwise `Not applicable` |
| 5 | Delta table complete | every material visual difference has a row with acceptance ID, source target, current runtime, target contract, priority, owner, evidence IDs, verification, and asset owner/fallback |
| 6 | Viewport matrix complete | every required viewport/state entry is present with no missing required items; justified exclusions are named |
| 7 | P1 asset and icon owner | every P1 asset and applicable SVG icon role has an accepted owner, rights status, and either an accepted isolated fallback or evidenced `None` disposition; icon family/render/state/color/accessibility acceptance is complete |
| 8 | Required state coverage | loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules are present or justified-excluded |
| 9 | Evidence levels | every claim uses `source-extracted`, `browser-computed`, `visually-inferred`, `proposed`, or `Not verified`; no untagged claim |

Evaluate the nine items in numeric order:

1. If an item fails, stop at that item, report its number and name, and return
   `Not Ready`.
2. If all required items pass, report non-blocking `Not verified` gaps without
   downgrading the slice. Use `Partial` only when a multi-slice result contains both
   ready and blocked slices.
3. Return `Ready for dev-frontend <slice>` when every required item passes; readiness
   does not upgrade separately reported runtime or optional evidence.

A blocking `Not verified` condition must fail its owning checklist item; it cannot be
downgraded to `Partial`.
