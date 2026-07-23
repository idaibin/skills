---
name: ui-spec
description: "Use when a selected visual source or accepted UI surface must become an implementation-ready specification covering layout, states, interaction, responsive/accessibility behavior, component/token mappings, shared visual contracts, and acceptance before frontend source changes."
---

# UI Specification

## Overview

Turn a selected visual source and verified product facts into an implementation-ready UI contract, then hand it to `dev-frontend`. This Skill specifies an accepted direction; it does not explore visual directions, generate images, build prototypes, or edit product source.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning an authorized artifact write.
2. Fix the selected visual source: a user-selected Product Design result, supplied screenshot/mockup/frame, accepted current surface, or accepted shared design-system revision. Record its identity, revision, approval, rights, `use`, and `ignore` boundaries. If no visual source has been selected and the user wants exploration, redesign, images, or a prototype, stop and route that work to the host's Product Design capability when available.
3. Fix the target page or flow, audience, user job, product facts, available actions, required states, platform, current UI owners, evidence gaps, and forbidden inventions. Route unresolved behavior, permissions, failure semantics, or acceptance to `product-spec`.
4. Select one profile:
   - **Feature Spec (default):** specify one selected page or flow without changing shared semantics.
   - **Design System Spec (conditional):** specify an accepted revision only when shared tokens, component semantics, variants, state vocabulary, or product-wide visual rules must change.
5. Inspect only the selected visual source, live routes/components/tokens, DTO-shaped facts, accepted product artifacts, and scoped references needed for the profile. Treat pending, rejected, or stale artifacts as leads only; revalidate live owners and do not promote them implicitly.
6. Translate the selected direction into explicit hierarchy, regions, layout ownership, density, semantic colors, typography roles, spacing and geometry, material, assets, copy, component/token mappings, required states and transitions, feedback ownership, responsive rules, focus, reduced motion, overflow, and acceptance checks. Mark every value as verified, extracted, proposed, or `Not verified`; an image does not prove exact tokens, behavior, accessibility, or runtime state.
7. Reuse current owners before declaring `adapt` or `new`. Keep Feature Spec changes local unless shared meaning actually changes; preserve one accepted shared-system owner and rollback path.
8. Apply deterministic truth, rights, required-state, mapping, responsive, accessibility, overflow, approval, and implementation-budget gates. Human rejection cannot be averaged away.
9. Produce the smallest specification artifact that removes implementation ambiguity. Use the package schema and manifest only for a shared Design System Spec revision, not every feature task.
10. Validate authored artifacts with applicable local checks, then hand source work to `dev-frontend` and runtime evidence to `ops-browser` or `ops-client` without claiming implementation or runtime verification.

## Profiles

- **Feature Spec (default):** one selected page or flow; implementation-ready layout, component/token mapping, states, interaction, responsive/accessibility rules, assets, and acceptance.
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
- Do not activate Design System Spec merely because a feature reuses existing tokens or components.
- Do not create a parallel component library or token system when the project already has an owner.
- Do not promote a present manifest when approval is absent, pending, rejected, or stale.
- Require applicable loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules; justify exclusions.
- Do not stage, commit, push, publish, or approve a shared baseline.

## Output Contract

Report the selected profile, source identity and approval, evidence basis, target page/flow, specification artifact, verified/extracted/proposed decisions, layout and state contract, component/token mappings, responsive/accessibility rules, assets and copy, shared-system changes or `None`, evaluation gates, `dev-frontend` handoff, validation, and every `Not found` or `Not verified` gap. Never present a source image or specification as implemented or runtime-verified UI.

## References

- See [references/usage.md](references/usage.md) for routing and artifact examples.
- See [references/workflow.md](references/workflow.md) for profile-specific specification and handoff details.
- See [references/visual-source.md](references/visual-source.md) when qualifying and translating the selected visual source.
- See [references/artifact-contract.md](references/artifact-contract.md) only for a shared Design System Spec package or accepted revision.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
