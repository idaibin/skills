---
name: ui-spec
description: "Use when a selected visual source or accepted UI surface must become a traceable implementation-ready Feature Spec or Google DESIGN.md shared visual contract, including source/runtime deltas, states, responsive/accessibility behavior, assets, and acceptance; do not use for visual exploration, browser operation, or frontend source edits."
compatibility: "Node.js + npm, with `@google/design.md@0.3.0` for DESIGN.md lint/diff/export."
---

# UI Specification

## Overview

Turn a selected visual source and verified product facts into an implementation-ready UI contract, then hand it to `dev-frontend`. This Skill specifies an accepted direction; it does not explore visual directions, generate images, build prototypes, or edit product source.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning an authorized artifact write.
2. Fix the selected visual source: a user-selected Product Design result, supplied screenshot/mockup/frame, accepted current surface, or accepted shared visual baseline. Record identity, revision/image ID, approval, rights status, `use` and `ignore` boundaries, target viewport/state, and source limitations. When a current runtime exists, load [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) and request same-round, same-viewport/state source and runtime captures from `ops-browser` without operating the browser here.
3. Require the repository-root `DESIGN.md` as the single source of truth for shared visual semantics. If it does not exist, copy [assets/DESIGN.md](assets/DESIGN.md) as the structural starter, replace every placeholder from verified sources, omit unverified token groups, obtain named human approval, and validate it before authoring Feature Specs or shared-system changes.
4. Define implementation slices: one Feature Spec per confirmed page/flow/domain; for multiple independent domains, create one shared index plus one independently loadable contract per slice and load [references/multi-surface.md](references/multi-surface.md).
5. Select one profile:
   - **Feature Spec (default):** reuse current shared systems unless shared semantics truly change.
   - **Design System Spec (conditional):** only when shared tokens, reusable component meaning/variants, state vocabulary, or cross-surface visual rules must change.
6. In Design System Spec, make the repository-root `DESIGN.md` the only durable shared output. Feature Specs reference shared visual semantics by exact path/anchor or semantic name; they do not repeat shared colors, spacing scales, global typography, radius, or shared-component semantics.
   - `DESIGN.md` is the only accepted shared product visual output.
   - Feature Spec never copies token values or component semantics from shared systems into its own artifacts.
7. Translate the selected source into concrete layout, state, interaction, and accessibility specifications for each slice. Use the exact evidence levels `source-extracted`, `browser-computed`, `visually-inferred`, `proposed`, and `Not verified`. Prefer design-tool selected-element/inspect-panel values for design targets; current runtime computed styles prove only the runtime column. A 200% screenshot check remains `visually-inferred` and cannot supply an exact verified value. When responsive or viewport-specific acceptance applies, define one per-slice viewport acceptance matrix using [references/workflow.md](references/workflow.md): required, optional, and excluded entries record size, environment, state, and acceptance-evidence source.
8. Add a traceable delta table for every material visual difference: acceptance ID, selected-source target, current runtime, target contract, priority, shared-or-local owner, evidence IDs, and verification. Keep source and runtime columns separate. Define real per-item asset ownership and an isolated failure fallback; never accept one generic placeholder as the normal asset for every product.
9. For every slice and multi-slice task, add one `Ready for dev-frontend <slice>`, `Partial`, or `Not Ready` verdict. Do not issue `Ready` when the selected source is unavailable or unapproved, rights/use are insufficient, target viewport/state is uncertain, a P1 asset has no accepted owner/fallback, or an exact proposed value lacks owner approval.
10. Before finalizing:
   - run official lint with `npx -p @google/design.md@0.3.0 designmd lint --format json DESIGN.md`;
   - treat duplicate H2 headings as hard blockers for repository contracts: do not accept any output if the contract contains duplicate H2 (even if `@google/design.md@0.3.0` only emits warnings and exits `0`);
   - for a Design System Spec update only, compare with the previous accepted source using `npx -p @google/design.md@0.3.0 designmd diff <before-DESIGN.md> DESIGN.md --format json`; record diff as `Not applicable` for a Feature Spec that leaves DESIGN.md unchanged or for the first accepted creation, with no fabricated baseline;
   - only export machine assets when explicitly required, and always as explicit derived outputs (`--format ...`) after acceptance of the updated `DESIGN.md`.
11. Do not claim lint, diff, export, or source comparison success without evidence output. If required tooling or network is blocked, report those checks `Not verified` and mark the affected slice `Not Ready` when the missing evidence controls implementation.
12. Hand the spec, delta rows, evidence limits, and a validated `frontend-visual-evidence/v1` `spec-ready` artifact to `dev-frontend`. Do not add implementation mapping, visual reviews, runtime coverage, final verdict, or claim runtime behavior in this Skill.

## Profiles

- **Feature Spec (default):** one selected page or flow contract; a multi-surface
  request may use a shared index plus independently loadable Feature Spec contracts,
  each with its own layout, mapping, states, interaction, responsive/accessibility
  rules, assets, acceptance, and readiness verdict.
- **Design System Spec (conditional):** accepted shared tokens, semantic components, variants, state vocabulary, or visual rules; may create, extract, maintain, or evaluate the repository-owned contract.

## Do Not Use For

- Visual exploration, image generation, redesign alternatives, UX research/critique, or shareable prototypes; use the host's Product Design capability when available.
- Unresolved product behavior, permissions, failure semantics, or acceptance; use `product-spec`.
- Frontend source changes or refactors; use `dev-frontend` with the accepted specification.
- Read-only frontend implementation audits; use `audit-frontend`.
- Browser screenshots, console/network evidence, or desktop-window operation; use `ops-browser` or `ops-client`.
- Git staging, commits, pushes, or branch cleanup; use `repo-delivery` after review.

## Hard Rules

- Require a selected visual source or accepted existing UI/design-system baseline before authoring a visual implementation contract.
- Do not generate or edit images, build prototype code, or edit product source.
- Do not invent metrics, features, routes, permissions, states, backend behavior, or runtime evidence.
- Do not treat pixels as proof of exact tokens, component ownership, behavior, accessibility, or implementation feasibility.
- Do not use current runtime computed geometry as the selected-source target or call it already aligned without independent source evidence.
- Do not activate Design System Spec merely because a feature reuses existing tokens or components.
- Do not create a parallel component library or token system when the project already has an owner.
- Do not author or rely on another structured UI package as shared visual authority.
- Keep Feature Specs page-local: they map the selected source to layout, states,
  interaction, components, and acceptance, but never restate the shared visual
  system already owned by root `DESIGN.md`.
- Treat the repository-root `DESIGN.md` as the single human-readable visual-semantic authority.
- Require named human approval before treating a newly created or changed `DESIGN.md` as accepted.
- Treat duplicate H2 headings as hard blockers in Design System Spec contracts, regardless of CLI warning wording or exit code.
- Require applicable loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules; justify exclusions.
- When responsive or viewport-specific acceptance applies, give every affected slice a
  viewport acceptance matrix. Required entries are mandatory downstream checks,
  optional entries are checked only when budget permits, and excluded entries define
  acceptance scope only; they never claim the UI is unsupported at that viewport.
- Treat the user's current viewport requirement as higher priority than an older
  specification. Do not turn one surface's viewport matrix into a catalog-wide rule.
- Do not merge independent business domains into one omnibus contract. Author only
  confirmed slice contracts, keep unconfirmed slices visible in the shared index,
  and mark the overall multi-surface result `Partial` until every requested slice has
  its own complete state, interaction, responsive/accessibility, mapping, and
  acceptance contract.
- Do not stage, commit, push, publish, or approve a shared baseline.

## Output Contract

Report the selected profile, source identity and approval, rights/use boundary,
target viewport/state, evidence basis and levels, target
surfaces and slice boundaries, source-extracted/browser-computed/visually-inferred/proposed decisions, layout and
state contract, traceable delta table, component/token mappings, responsive/accessibility rules, assets and
copy, shared-system changes or `None`, evaluation gates, one `Ready for dev-frontend
<slice>`, `Partial`, or `Not Ready` verdict per slice, overall `Complete`, `Partial`,
or `Not Ready`, and every
`Not found` or `Not verified` gap. Include at least:

- root `DESIGN.md` revision
- lint command and result
- diff command and regression verdict, or `Not applicable` when a Feature Spec leaves `DESIGN.md` unchanged or the authority is created for the first time
- per-slice spec IDs and readiness
- per-slice viewport acceptance matrix or a justified `Not applicable` verdict,
  including required/optional/excluded entries, size, environment, state, and
  acceptance-evidence source; hand the same matrix to `dev-frontend`,
  `audit-frontend`, and `ops-browser`/`ops-client` without redefining its schema

Never present a source image or specification as implemented or runtime-verified UI.

## References

- See [references/usage.md](references/usage.md) for routing and artifact examples.
- See [references/workflow.md](references/workflow.md) for profile-specific specification and handoff details.
- See [references/visual-source.md](references/visual-source.md) when qualifying and translating the selected visual source.
- Read [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) when a selected source controls exact visual acceptance or a current runtime must be compared; validate each stage offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json).
- See [references/multi-surface.md](references/multi-surface.md) when a request covers more than one page, flow, or business domain.
- See [references/documentation-boundaries.md](references/documentation-boundaries.md) for durable UI locations, PRD links, and consumer reads.
- See [references/design-md-contract.md](references/design-md-contract.md) for the official DESIGN.md format, validation gates, and derived exports.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
