# UI Specification Evaluation Rubric

## Hard Blockers

Reject when any applicable blocker is present:

1. no selected visual source or accepted UI/design-system baseline exists;
2. source identity, revision, selection, rights, or use boundary is unknown;
3. product data, capability, permission, route, state, or business judgment is invented;
4. a material conflict between the source and verified product facts remains unresolved;
5. pixels are treated as proof of exact tokens, behavior, accessibility, or component ownership;
6. applicable loading, empty, error, populated, permission, focus, responsive, overflow, or reduced-motion behavior is absent without justification;
7. a parallel component or token system is created without evidence;
8. an accepted shared baseline is promoted without human approval;
9. implementation or runtime validation is claimed without evidence.

## Weighted Score

| Dimension | Points |
| --- | ---: |
| Product truth and boundaries | 15 |
| Selected-source fidelity | 15 |
| Information architecture and layout ownership | 10 |
| Interaction and required states | 15 |
| Responsive and accessibility contract | 15 |
| Component and token mapping | 15 |
| Engineering fit | 10 |
| Evidence completeness | 5 |

Pass requires at least 85/100, no hard blocker, and at least 11/15 in product truth, selected-source fidelity, interaction/states, responsive/accessibility, and component/token mapping. A model may propose scores; the named reviewer owns the final decision.

## Deterministic Evidence

Use repository-defined source, schema, and documentation checks for exact routes, component/token owners, required fields, source revisions, state coverage, target sizes, and approval. Mark runtime behavior, rendered fidelity, console/network state, accessibility execution, and deployment `Not verified` until the owning implementation or operations workflow proves them.
