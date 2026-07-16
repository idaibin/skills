# AICraft v2 Method Integration

## Difference Table

| Matt capability | AICraft owner | Action |
| --- | --- | --- |
| `grill-me` / `grill-with-docs` | `code-planner`, `domain-modeling` | absorb readiness and domain clarification; no duplicate interview skill |
| `to-spec` | `code-planner` | add requirements, decisions, technical design, acceptance, and validation contract |
| `to-tickets` | `code-planner` | add vertical slices and blocking edges |
| `domain-modeling` | missing | add distinct public owner |
| `diagnosing-bugs` | `diagnose` | strengthen feedback-loop and hypothesis gates |
| `tdd` | `implement-frontend`, `implement-rust` | add opt-in behavior-first vertical-slice references |
| `implement` | `implement-*` | retain domain-specific implementation owners |
| `code-review` | `repo-review` | add independent Standards and Spec axes under one severity owner |
| `codebase-design` | `code-planner` and existing audit profiles | add internal deep-module design guidance; do not create another owner |
| `handoff` | `repo-delivery` | borrow compact references and redaction; use the AICraft plan's Git Delivery Report |

## AICraft v2 Lifecycle

```text
Discovery: repo-map when repository truth is unknown
  -> Domain: domain-modeling when language, lifecycle, or business rules are unclear
  -> Design: code-planner for technical design and executable tasks
  -> Implementation: implement-frontend or implement-rust
  -> Quality: repo-review with bounded audit specialists
  -> Delivery: repo-delivery
```

This is composable, not mandatory ceremony. Start at the earliest unresolved owner and stop at the last outcome the user requested.

## Profile Placement

The proposal's Rust, frontend, Tauri, and content profiles remain internal references because they do not create distinct authority or output contracts:

- Rust: `implement-rust` and `audit-rust` references.
- Frontend and Tauri: `implement-frontend` and `audit-frontend` references.
- Content: `human-writing` references.
- TDD guidance: package-local implementation references.
- Deep-module guidance: `code-planner` technical-design reference, with architecture review remaining inside existing audit and `repo-review` surfaces.

No `.aicraft/skills` mirror is added. Published packages remain under `skills/`, with detailed guidance one level down in `references/`.

## Acceptance Boundary

- One public owner per user intent and mutation boundary.
- Domain modeling is independent from repository mapping and technical planning.
- Requirements and acceptance criteria precede complex implementation.
- Implementations consume confirmed scope, use behavior-first tests when the seam warrants it, and stop before Git mutation.
- Review covers both repository standards and originating requirements.
- Delivery reports completed scope, changed files, validation, known issues, next state, and Git proof.
