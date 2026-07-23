# Skills Catalog Method Integration

## Difference Table

| Matt capability | Catalog owner | Action |
| --- | --- | --- |
| `grill-me` / `grill-with-docs` | `product-spec`, `domain-modeling` | keep decision-changing clarification internal; route deep shared domain work separately |
| `to-spec` | `product-spec` | own product behavior, scope, states, acceptance, and Ready-for-slice; interface topology stays with `repo-map` |
| `to-tickets` | host planning | keep technical slices, owners, dependencies, and validation in built-in planning |
| `domain-modeling` | `domain-modeling` | retain the distinct public owner |
| `prototype` | Codex Product Design plus conditional host experiments | keep visual/prototype exploration outside `ui-spec`; never auto-promote it into product source |
| `writing-great-skills` | catalog standards | prune context/cognitive load, use checkable steps, single-source protocols, branch disclosure, and leading words |
| `diagnosing-bugs` | Global diagnosis rules | require a run red-capable command before hypotheses; do not restore a public diagnosis Skill |
| `tdd` | `dev-frontend`, `dev-rust` | add opt-in behavior-first vertical-slice references |
| `implement` | `dev-*` | retain domain-specific implementation owners |
| `code-review` | `repo-review` | add independent Standards and Spec axes under one severity owner |
| `codebase-design` | host planning and existing audit profiles | keep technical design in built-in planning; do not create another owner |
| `handoff` | Global continuation rules | borrow compact basis/scope/evidence/redaction; do not create a public handoff Skill |

## Catalog Lifecycle

```text
Discovery: repo-map when repository truth is unknown
  -> Domain: domain-modeling when language, lifecycle, or business rules are unclear
  -> Product: product-spec when product behavior or acceptance is unresolved
  -> Visual: Codex Product Design when a direction or prototype must be explored
  -> UI contract: ui-spec when a selected source must become implementation-ready
  -> Design: host planning for technical design and executable tasks
  -> Implementation: dev-frontend or dev-rust
  -> Quality: repo-review with bounded audit specialists
  -> Delivery: repo-delivery
```

This is composable, not mandatory ceremony. Start at the earliest unresolved owner and stop at the last outcome the user requested.

## Profile Placement

The proposal's Rust, frontend, Tauri, and content profiles remain internal references because they do not create distinct authority or output contracts:

- Rust: `dev-rust` and `audit-rust` references.
- Frontend and Tauri: `dev-frontend` and `audit-frontend` references.
- Content: `human-writing` references.
- TDD guidance: package-local implementation references.
- Deep-module guidance: host technical planning, with architecture review remaining inside existing audit and `repo-review` surfaces.

No provider-specific mirror is added. Published packages remain under `skills/`, with detailed guidance one level down in `references/`.

## Acceptance Boundary

- One public owner per user intent and mutation boundary.
- Domain modeling is independent from repository mapping and technical planning.
- Requirements and acceptance criteria precede complex implementation.
- Implementations consume confirmed scope, use behavior-first tests when the seam warrants it, and stop before Git mutation.
- Review covers both repository standards and originating requirements.
- Delivery reports completed scope, changed files, validation, known issues, next state, and Git proof.
