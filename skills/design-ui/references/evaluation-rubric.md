# UI Evaluation Rubric

## Hard blockers

Reject when any applicable blocker is present:

1. invented product data, capability, permission, route, or business judgment;
2. primary user task cannot be completed;
3. required build or deterministic check fails;
4. target size has material clipping or horizontal overflow;
5. applicable loading, empty, error, populated, or permission state is missing;
6. current routing, data, accessibility, or native boundary is broken;
7. a second component or token system is created without evidence;
8. reference content is copied beyond its declared use or rights;
9. validation is claimed without evidence;
10. accepted baseline is promoted without human approval.

## Weighted score

| Dimension | Points |
| --- | ---: |
| Product truth and boundaries | 15 |
| User-task completion | 15 |
| Information architecture | 15 |
| Visual coherence and identity | 15 |
| Components and layout | 15 |
| Interaction and required states | 10 |
| Engineering fit | 10 |
| Evidence completeness | 5 |

Pass requires at least 85/100, no hard blocker, and at least 11/15 in both product truth and user-task completion. A model may propose scores; the named reviewer owns the final decision.

## Deterministic evidence

Use repository-defined commands and runtime assertions for build, lint, typecheck, tests, routes, exact text, required states, overflow, console errors, failed requests, keyboard reachability, window identity, and target dimensions. Mark unsupported evidence `Not verified`; do not replace it with visual opinion.
