---
name: ui-spec
description: "Use when a selected visual source or accepted UI surface must become a traceable current Feature Spec or Google DESIGN.md contract at a resolved shared design root, including evidence lifecycle, source/runtime deltas, states, responsive/accessibility behavior, assets, and acceptance; route unresolved product behavior to product-spec, current-state audits to audit-frontend, and source edits to dev-frontend."
compatibility: "Node.js + npm, with `@google/design.md@0.3.0` for DESIGN.md lint/diff/export."
---

# UI Specification

## Overview

Turn a selected visual source and verified product facts into an implementation-ready UI contract, then hand it to `dev-frontend`. This Skill specifies an accepted direction; it does not explore visual directions, generate images, build prototypes, or edit product source.

Consume `urn:skills:ui-request:v1`; the portable typed handoff is
`urn:skills:ui-contract:v1`, with
`urn:frontend-visual-evidence:v1` retained as a typed attachment when applicable.
Product behavior, shared `DESIGN.md`, and Feature UI Markdown keep separate native
authority; the handoff references them and never copies shared token semantics.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning an authorized artifact write.
2. Fix the selected visual source: a user-selected Product Design result, supplied screenshot/mockup/frame, accepted current surface, or accepted shared visual baseline. Record identity, revision/image ID, approval, rights status, `use` and `ignore` boundaries, target viewport/state, and source limitations. When a current runtime exists, load [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) and request same-round, same-viewport/state source and runtime captures from `ops-browser` without operating the browser here. For implicit routing, do not trigger this Skill when no selected visual source or accepted existing UI surface is available; route to `product-spec` for unresolved behavior or host Product Design for visual exploration. If this Skill is already explicitly invoked without that source, stop as `evidence-incomplete` instead of fabricating one.
3. Resolve the approved `<design-root>` from effective guidance, build ownership,
   and shared consumers. Require `<design-root>/DESIGN.md` as that boundary's single
   source of truth for shared visual semantics; a monorepo does not imply automatic
   parent/child inheritance or one file per application. A missing pre-existing
   `DESIGN.md` is not a non-trigger once a selected visual source is fixed; it is an
   authorized artifact-creation path. If it does not exist, copy
   [assets/DESIGN.md](assets/DESIGN.md) as the structural starter, replace every
   placeholder from verified sources, omit unverified token groups, obtain named
   human approval from someone other than the proposer/implementer, bind that approval
   to the exact content hash, and validate it before authoring Feature Specs or shared-
   system changes. A later content-hash change makes the approval stale.
4. Define implementation slices: one Feature Spec per confirmed page/flow/domain; for multiple independent domains, create one shared index plus one independently loadable contract per slice and load [references/multi-surface.md](references/multi-surface.md).
5. Select one profile:
   - **Feature Spec (default):** reuse current shared systems unless shared semantics truly change.
   - **Design System Spec (conditional):** only when shared tokens, reusable component meaning/variants, state vocabulary, or cross-surface visual rules must change.
6. In Design System Spec, keep `<design-root>/DESIGN.md` as the only durable shared visual output; Feature Specs reference it instead of copying shared semantics.
7. Translate the selected source into concrete layout, state, interaction, and accessibility specifications for each slice. Name reusable and page-defining components only after checking current source and the project map when one exists; keep props, slots, events, types, and copied token values out of the page contract. Use the exact evidence levels `source-extracted`, `browser-computed`, `visually-inferred`, `proposed`, and `Not verified`. Load the visual-direction, layout-governance, measurement-normalization, and viewport workflow references only when their named conditions apply.
8. Add a traceable delta table for every material visual difference: acceptance ID, selected-source target, current runtime, target contract, priority, shared-or-local owner, evidence IDs, verification, and applicable asset owner/fallback.
9. For every slice and multi-slice task, add one `Ready for dev-frontend <slice>`, `Partial`, or `Not Ready` verdict. Do not issue `Ready` when the selected source is unavailable or unapproved, rights/use are insufficient, target viewport/state is uncertain, a P1 asset has no accepted owner/fallback, or an exact proposed value lacks owner approval.
10. For a shared `DESIGN.md` change, follow [references/design-md-contract.md](references/design-md-contract.md) for lint, diff, duplicate-heading, and explicit derived-export gates. Missing required evidence remains `Not verified` and keeps the affected slice `Not Ready`.
11. Keep the page UI contract and component guidance human-readable and authoritative
    for their own meanings. Markdown is the default durable UI artifact. A YAML/JSON
    projection is conditional: use it only when a named owner, producer, non-LLM
    consumer, semantic version, executable validator, drift policy, and retirement
    rule already exist. Never copy
    tokens, API/DTO schemas, props, slots, events, or source paths into a projection;
    otherwise omit it and let current source plus Markdown remain authoritative.
12. Hand the spec, delta rows, evidence limits, and a validated
    `frontend-visual-evidence/v1` `spec-ready` artifact to `dev-frontend`. Store that
    task evidence under a verified ignored `.codex/artifacts/` location by default;
    publish it with durable docs only when a named team consumer, accessible
    artifacts, schema/validator, drift policy, and revalidation owner justify it.
    Do not add implementation mapping, visual reviews, runtime coverage, final
    verdict, or claim runtime behavior in this Skill.
13. When a compatible Repository Asset Graph is available, resolve shared-design,
    feature-UI, route, component, and consumer refs and reject duplicate active
    authority claims. Never invent graph IDs or turn the graph into visual authority.
14. When Forgeway delivery integration is active, bind the invocation to an immutable
    Run input and input PackageManifest/basis. Let the package producer fingerprint
    authorized artifact writes, then attach the UI contract and visual-evidence
    payload as typed Observations against that exact result package. A `Ready` verdict
    is not a review, delivery, deployment, or production Receipt.

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
- Do not activate Design System Spec merely because a feature reuses existing tokens or components.
- Do not create a parallel component library or token system when the project already has an owner.
- Do not make page specs redefine reusable component interfaces. Record page composition and page-local state/interaction; route current component ownership through a validated project map when one exists, then recheck live source before implementation.
- Do not require a `ui-page/v1` or `ui-components/v1` Schema, project-local validator,
  or YAML/JSON companion for ordinary UI work. Admit a projection only when its named
  non-LLM consumer and complete lifecycle are already real and maintained.
- Treat `<design-root>/DESIGN.md` as the single human-readable visual-semantic authority for its proven shared boundary.
- Keep durable `DESIGN.md`, UI indexes, and Feature Specs current-only. Git retains
  formal history; task captures, comparison passes, superseded candidates, and
  validation timestamps belong in `.codex/` unless durable-evidence gates are met.
- Require named non-implementer human approval bound to the exact content hash before
  treating a newly created or changed `DESIGN.md` as accepted; never let the executor
  self-approve extracted current CSS as the target design.
- Require applicable loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules; justify exclusions.
- Give every applicable slice its own viewport matrix and readiness verdict; keep independent incomplete slices visible as `Partial` without turning one surface's viewport requirements into a catalog default.
- Do not stage, commit, push, publish, or approve a shared baseline.

## Output Contract

Report capability `ui.contract.specify`, typed result/attachment refs, Run and
input/result PackageManifest refs when integration is active, the selected profile,
source identity/approval and rights/use boundary, target viewport/state and slices,
evidence levels, layout/state contract, delta table, component/token mappings,
responsive/accessibility rules, assets/copy, shared-system changes or `None`,
evaluation gates, per-slice and overall readiness, and every `Not found` or `Not
verified` gap. Include at least:

- resolved `<design-root>` and `DESIGN.md` revision or stable identity
- lint command and result
- diff command and regression verdict, or `Not applicable` when a Feature Spec leaves `DESIGN.md` unchanged or the authority is created for the first time
- per-slice spec IDs and readiness
- raw selected-source measurement evidence and the normalization record for every
  applicable repeated spacing cluster
- per-slice viewport acceptance matrix or a justified `Not applicable` verdict,
  including required/optional/excluded entries, size, environment, state, and
  acceptance-evidence source; hand the same matrix to `dev-frontend`,
  `audit-frontend`, and `ops-browser`/`ops-client` without redefining its schema

## References

- See [references/usage.md](references/usage.md) for routing and artifact examples.
- See [references/workflow.md](references/workflow.md) for profile-specific specification and handoff details.
- See [references/visual-source.md](references/visual-source.md) when qualifying and translating the selected visual source.
- Read [references/visual-direction-and-anti-slop.md](references/visual-direction-and-anti-slop.md) only when visual direction, redesign mode, theme/accent policy, density, or anti-slop acceptance is material.
- Read [references/frontend-layout-governance.md](references/frontend-layout-governance.md) when geometry, nested padding/insets, alignment, scrolling, or responsive ownership is material to the specification.
- Read [references/measurement-normalization.md](references/measurement-normalization.md) when selected-element evidence contains repeated spacing measurements or an even-grid policy applies.
- Read [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) when a selected source controls exact visual acceptance or a current runtime must be compared; validate each stage offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json).
- See [references/multi-surface.md](references/multi-surface.md) when a request covers more than one page, flow, or business domain.
- See [references/documentation-boundaries.md](references/documentation-boundaries.md) for durable UI locations, PRD links, and consumer reads.
- See [references/design-md-contract.md](references/design-md-contract.md) for the official DESIGN.md format, validation gates, and derived exports.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
