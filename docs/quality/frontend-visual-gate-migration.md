# Frontend Visual Gate Migration

## Basis

This change generalizes a failure pattern in which a selected visual source was
translated into a UI contract and implementation, but structural similarity was
accepted without traceable element targets, approved asset mapping, or immediate
same-viewport computed-style review. This document contains no real project, person,
repository, product, design-source identifier, copy, path, date, or measurement.

The central correction is that source targets and runtime values are different facts.
Inspectable source metadata has priority for exact targets. A zoomed screenshot can
support visual comparison only, and browser-computed values describe only the
captured runtime.

## Behavior Changes

| Owner | New gate | Stop or failure condition |
| --- | --- | --- |
| `ui-spec` | Freeze source revision, approval, rights, viewport, and state; label evidence; separate selected source, runtime, and target contract; emit traceable deltas and asset strategy. | Unavailable source, uncertain viewport/state, unapproved proposed exact value, missing critical asset owner, `Partial`, or `Not Ready`. |
| `dev-frontend` | Read applicable contracts and source evidence; map every acceptance ID before editing; preserve confirmed structure; close critical deltas before polish; run two visual passes. | Missing mapping, source/runtime conflation, generic fallback used as normal content, or missing target, breakpoint, or runtime evidence. |
| `ops-browser` | Capture source and runtime at the same viewport/state; retain side-by-side, overlay, or diff evidence; read computed font, final contrast, geometry, alignment, and states; restore user browser state. | Missing capability, source identity, viewport, or state; unsupported claim; or runtime/screenshot inference relabeled as source-extracted. |
| `audit-frontend` | Apply selected-source visual fidelity as a bounded profile and lead with P0-P3 findings. | Build, lint, source styles, structural similarity, or one screenshot offered as visual acceptance. |
| `repo-review` | Apply a fixed-basis visual-completion profile; validate handoff structure and inspect cited evidence. | Missing mapping, fewer than two same-state passes, absent computed evidence, unresolved P0/P1, or required state marked `Not verified`. |

No duplicate public Skill is introduced. These owners share the
`frontend-visual-evidence/v1` protocol and package-local Schema and validator copies.

## Evidence Precedence

For exact visual targets, use selected-element inspect values or equivalent source
metadata. Enlarged screenshot inspection can confirm hierarchy and approximate
alignment only; it remains `visually-inferred`. Browser-computed values are exact for
the captured runtime only and never become source targets by reuse or similarity.

The evidence labels are `source-extracted`, `browser-computed`,
`visually-inferred`, `proposed`, and `Not verified`.

## Offline Contract

- Canonical protocol: `protocols/frontend-visual-evidence-v1.md`
- Canonical schema: `protocols/frontend-visual-evidence-v1.schema.json`
- Stage model: `spec-ready` → `mapped` → `pass-1` → `final`
- Readiness: only an approved source with no blockers can be `Ready`; later stages
  require `Ready`; `Partial` and `Not Ready` require explicit blockers.
- Package copies: `ui-spec`, `dev-frontend`, `audit-frontend`, `repo-review`, and
  `ops-browser`
- Sanitized fixture: `skills/dev-frontend/assets/frontend-visual-evidence.example.json`
- Generic example: `skills/dev-frontend/references/frontend-visual-gate-example.md`
- Validator: `scripts/validate-frontend-visual-evidence.py`

`bash scripts/check-skills.sh` checks synchronized copies, validates the fixture
offline, runs stage and negative-completion regressions, and executes the existing
package checks. Validity proves structure and cross-evidence semantics, not the
authenticity of screenshots or claims.

## Compatibility

Non-visual frontend work is unchanged. The gate activates only when a selected visual
source materially controls acceptance or a change claims visual completion.
