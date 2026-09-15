---
name: product-spec
description: "Use when product behavior, scope, states, rules, or acceptance must be defined in a named product artifact; not for shared domain modeling, UI visual specification, implementation, review, or delivery."
---

# Product Specification

## Entry Gate

Own current product facts and acceptance, not implementation architecture or visual
semantics. Require a named product authority or authorized artifact target; resolve
only decisions needed for the requested slice.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| One feature needs behavior, states, and acceptance | [workflow](references/workflow.md) and [template](references/template.md) | Progressive Feature Spec |
| New product line/boundary reset is explicit | [workflow](references/workflow.md) | Foundation Spec |
| Confirmed changes update a named fact source | [documentation boundaries](references/documentation-boundaries.md) | Bounded artifact update |
| A material product decision needs challenge | [decision pressure test](references/decision-pressure-test.md) | Decision disposition |
| Prototype evidence is decisive | [prototype evidence](references/prototype-evidence.md) | Qualified product facts |

## Invariants

- Do not infer behavior from UI appearance, source, or tests when product authority is absent.
- Keep product behavior separate from shared visual semantics, technical design, implementation, and runtime proof.
- Stop each slice at its Ready gate; unknowns remain named, not silently decided.

## Output Map

Return the one applicable current product artifact, source basis, decisions/states,
acceptance, non-goals, unresolved questions, and next owner.

## Reference Map

- Read [workflow](references/workflow.md) for Feature/Foundation/update procedure and gates.
- Read [template](references/template.md) when creating an artifact.
- Read [documentation boundaries](references/documentation-boundaries.md) for authority and placement.
- Read [prototype evidence](references/prototype-evidence.md) only when prototype evidence applies.
- Read [decision pressure test](references/decision-pressure-test.md) only for a material decision challenge.
- Read [usage](references/usage.md) for public modes and nearest owners.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
