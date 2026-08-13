---
name: ui-spec
description: "Use when a source-grounded candidate visual direction needs a local review spec and complete generation prompt, or a selected visual source or accepted UI surface must become a traceable Feature Spec or adopted Google DESIGN.md contract; route external-AI sending to ask-ai, visual generation to the host design capability, unresolved product behavior to product-spec, and source edits to dev-frontend."
---

# UI Specification

## Overview

Ground a candidate direction in current source truth, or turn an approved source into
an implementation-ready UI contract for `dev-frontend`. It may serialize a candidate
into a complete generation prompt, but never operates external AI, generates images,
builds prototypes, or edits product source.

Consume `urn:skills:ui-request:v1`; the portable typed handoff is
`urn:skills:ui-contract:v1`, with
`urn:frontend-visual-evidence:v1` retained as a typed attachment when applicable.
Product behavior, shared `DESIGN.md`, and Feature UI Markdown keep separate native
authority; the handoff references them and never copies shared token semantics.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning an authorized artifact write.
2. Before trusting a concept, inspect current product/source truth for real scope,
   data/actions/states, components, shared owners, and library mappings. Record
   conflicts and exclude every concept-only capability.
3. Choose one lifecycle stage:
   - **Candidate direction:** when the user has directed exploration but has not
     approved a visual result, load
     [references/candidate-visual-direction.md](references/candidate-visual-direction.md).
     Keep its spec and complete synchronized prompt under verified ignored
     `.codex/reviews/`; leave formal docs unchanged and remain `Not Ready`.
   - **Accepted contract:** fix the selected visual source: a user-selected Product
     Design result, supplied screenshot/mockup/frame, accepted current surface, or
     accepted shared visual baseline. Record identity, revision/image ID, approval,
     rights status, `use` and `ignore` boundaries, target viewport/state, and source
     limitations. When a current runtime exists, load
     [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md)
     and request same-round, same-viewport/state source and runtime captures from
     `ops-browser` without operating the browser here. If neither a source-grounded
     candidate brief nor a selected/accepted source exists, stop as
     `evidence-incomplete` instead of fabricating one.
4. For the accepted-contract stage, resolve whether the proven visual boundary has adopted `DESIGN.md` from effective
   guidance, build ownership, and shared consumers. When adopted, resolve the approved
   `<design-root>` and require `<design-root>/DESIGN.md` as that boundary's single
   source of truth for shared visual semantics; a monorepo does not imply automatic
   parent/child inheritance or one file per application. When the boundary has not
   adopted `DESIGN.md`, a Feature Spec that preserves existing shared semantics may
   use the accepted current surface and repository-native visual owners, record
   `DESIGN.md: Not adopted (not required for this slice)`, and continue without
   creating a new shared authority. First adoption is required only when the user
   explicitly requests it or the selected slice changes shared visual semantics. For
   first adoption, copy
   [assets/DESIGN.md](assets/DESIGN.md) as the structural starter, replace every
   placeholder from verified sources, then load
   [references/design-md-contract.md](references/design-md-contract.md). Official lint
   proves format only. Run the package completeness checker before requesting approval;
   a first-adoption candidate must be `ready-for-human-approval`. The local adopted
   check stops at `awaiting-trusted-approval-verification`; only a host-trusted
   approval receipt bound to the exact Result Package may satisfy the downstream
   `gate:ui-design-complete` claim. It never rewrites the producer result to
   `complete`. A later content-hash change
   makes the approval stale and returns `Not Ready`.
5. Define implementation slices: one Feature Spec per confirmed page/flow/domain; for multiple independent domains, create one shared index plus one independently loadable contract per slice and load [references/multi-surface.md](references/multi-surface.md).
6. Select one profile:
   - **Feature Spec (default):** reuse current shared systems unless shared semantics truly change.
   - **Design System Spec (conditional):** only when shared tokens, reusable component meaning/variants, state vocabulary, or cross-surface visual rules must change.
7. In Design System Spec, keep `<design-root>/DESIGN.md` as the only durable shared visual output; Feature Specs reference it instead of copying shared semantics.
8. Translate the selected source into concrete layout, state, interaction, and accessibility specifications for each slice. Name reusable and page-defining components only after checking current source and the project map when one exists; keep props, slots, events, types, and copied token values out of the page contract. Use the exact evidence levels `source-extracted`, `browser-computed`, `visually-inferred`, `proposed`, and `Not verified`. Load the visual-direction, layout-governance, measurement-normalization, and viewport workflow references only when their named conditions apply.
9. Add a traceable delta table for every material visual difference: acceptance ID, selected-source target, current runtime, target contract, priority, shared-or-local owner, evidence IDs, verification, and applicable asset owner/fallback.
10. For every slice and multi-slice task, add one `Ready for dev-frontend <slice>`, `Partial`, or `Not Ready` verdict. Do not issue `Ready` when the selected source is unavailable or unapproved, rights/use are insufficient, target viewport/state is uncertain, a P1 asset has no accepted owner/fallback, or an exact proposed value lacks owner approval.
11. For a shared `DESIGN.md` change, follow [references/design-md-contract.md](references/design-md-contract.md) for lint, diff, duplicate-heading, and explicit derived-export gates. Missing required evidence remains `Not verified` and keeps the affected slice `Not Ready`.
12. Keep the page UI contract and component guidance human-readable and authoritative
    for their own meanings. Markdown is the default durable UI artifact. A YAML/JSON
    projection is conditional: use it only when a named owner, producer, non-LLM
    consumer, semantic version, executable validator, drift policy, and retirement
    rule already exist. Never copy
    tokens, API/DTO schemas, props, slots, events, or source paths into a projection;
    otherwise omit it and let current source plus Markdown remain authoritative.
13. Hand the spec, delta rows, evidence limits, and a validated
    `frontend-visual-evidence/v1` `spec-ready` artifact to `dev-frontend`. Store that
    task evidence under a verified ignored `.codex/artifacts/` location by default;
    publish it with durable docs only when a named team consumer, accessible
    artifacts, schema/validator, drift policy, and revalidation owner justify it.
    Do not add implementation mapping, visual reviews, runtime coverage, final
    verdict, or claim runtime behavior in this Skill.
14. When a compatible Repository Asset Graph is available, resolve shared-design,
    feature-UI, route, component, and consumer refs and reject duplicate active
    authority claims. Never invent graph IDs or turn the graph into visual authority.
15. When Forgeway delivery integration is active, bind the invocation to an immutable
    Run input and input PackageManifest/basis. Let the package producer fingerprint
    authorized artifact writes, then attach the UI contract and visual-evidence
    payload as typed Observations against that exact result package. For adopted
    DESIGN authority, emit package-relative DESIGN.md, completeness JSON,
    selected-source artifact, and approval-record paths with hashes and byte lengths;
    the compatible consumer is `forgeway-ui-design-completeness/1` and its claim is
    `gate:ui-design-complete`. A `Ready` verdict or satisfied gate is not a review,
    delivery, deployment, or production Receipt.

## Profiles

- **Feature Spec (default):** one selected page or flow contract; a multi-surface
  request may use a shared index plus independently loadable Feature Spec contracts,
  each with its own layout, mapping, states, interaction, responsive/accessibility
  rules, assets, acceptance, and readiness verdict.
- **Design System Spec (conditional):** accepted shared tokens, semantic components, variants, state vocabulary, or visual rules; may create, extract, maintain, or evaluate the repository-owned contract.

## Do Not Use For

- Generating images, inventing redesign alternatives, UX research/critique, or shareable prototypes; use the host's Product Design or image capability. Preparing a source-grounded candidate specification and complete prompt remains in scope.
- Sending prompts, assets, or follow-up instructions to a named external model; use `ask-ai` with the frozen local artifacts.
- Unresolved product behavior, permissions, failure semantics, or acceptance; use `product-spec`.
- Frontend source changes or refactors; use `dev-frontend` with the accepted specification.
- Read-only frontend implementation audits; use `audit-frontend`.
- Browser screenshots, console/network evidence, or desktop-window operation; use `ops-browser` or `ops-client`.
- Git staging, commits, pushes, or branch cleanup; use `repo-delivery` after review.

## Hard Rules

- Require a selected visual source or accepted existing UI/design-system baseline before authoring a visual implementation contract.
- Treat the local candidate UI specification as the only candidate-direction source.
  Update it first, then rewrite the complete generation prompt from that revision.
  Never treat external-chat-only corrections as part of the candidate contract.
- Verify both candidate paths, ignore status, and hashes after edits and before
  handoff; any change makes the prior handoff stale.
- Do not generate or edit images, build prototype code, or edit product source.
- Do not invent metrics, features, routes, permissions, states, backend behavior, or runtime evidence.
- Do not treat pixels as proof of exact tokens, component ownership, behavior, accessibility, or implementation feasibility.
- Do not activate Design System Spec merely because a feature reuses existing tokens or components.
- Do not create a parallel component library or token system when the project already has an owner.
- Do not make page specs redefine reusable component interfaces. Record page composition and page-local state/interaction; route current component ownership through a validated project map when one exists, then recheck live source before implementation.
- Do not require a `ui-page/v1` or `ui-components/v1` Schema, project-local validator,
  or YAML/JSON companion for ordinary UI work. Admit a projection only when its named
  non-LLM consumer and complete lifecycle are already real and maintained.
- Treat `<design-root>/DESIGN.md` as the single human-readable visual-semantic authority for a proven boundary that has adopted it; do not force first adoption for a local slice that preserves shared semantics.
- Keep durable `DESIGN.md`, UI indexes, and Feature Specs current-only. Git retains
  formal history; task captures, comparison passes, superseded candidates, and
  validation timestamps belong in `.codex/` unless durable-evidence gates are met.
- Require named non-implementer human approval bound to the exact content hash before
  treating a newly created or changed `DESIGN.md` as accepted; never let the executor
  self-approve extracted current CSS as the target design.
- Require applicable loading, empty, error, populated, permission, focus, responsive, overflow, localization, and reduced-motion rules; justify exclusions.
- Give every applicable slice its own viewport matrix and readiness verdict; keep independent incomplete slices visible as `Partial` without turning one surface's viewport requirements into a catalog default.
- Do not stage, commit, push, publish, or approve a shared baseline.
- Keep default and interaction states distinct. Overlays are closed and absent from
  default acceptance unless explicitly defined as default; specify open state,
  trigger, focus, close, and layout separately.

## Output Contract

Report capability `ui.contract.specify@1.1.0`, typed result/attachment refs, Run and
input/result PackageManifest refs when integration is active, the lifecycle stage and selected profile,
source identity/approval and rights/use boundary, target viewport/state and slices,
evidence levels, layout/state contract, delta table, component/token mappings,
responsive/accessibility rules, assets/copy, shared-system changes or `None`,
evaluation gates, per-slice and overall readiness, and every `Not found` or `Not
verified` gap. Include at least:

- shared visual-authority disposition: adopted, first-adoption requested, or not adopted/not required for this slice
- resolved `<design-root>` and `DESIGN.md` revision or stable identity when adopted
- lint command and result when `DESIGN.md` is created or changed; otherwise `Not applicable`
- diff command and regression verdict, or `Not applicable` when a Feature Spec leaves `DESIGN.md` unchanged, the authority is created for the first time, or the boundary has not adopted it
- per-slice spec IDs and readiness
- for candidate direction: both paths/hashes, ignore status, generation owner,
  handoff status, and `DESIGN.md unchanged`
- raw selected-source measurement evidence and the normalization record for every
  applicable repeated spacing cluster
- per-slice viewport acceptance matrix or a justified `Not applicable` verdict,
  including required/optional/excluded entries, size, environment, state, and
  acceptance-evidence source; hand the same matrix to `dev-frontend`,
  `audit-frontend`, and `ops-browser`/`ops-client` without redefining its schema

## References

- See [references/usage.md](references/usage.md) for routing and artifact examples.
- See [references/workflow.md](references/workflow.md) for profile-specific specification and handoff details.
- Read [references/candidate-visual-direction.md](references/candidate-visual-direction.md) when visual direction is not yet approved and a local candidate specification plus complete generation prompt must drive exploration.
- Read [references/design-md-contract.md](references/design-md-contract.md) whenever
  first adoption, adopted shared-authority evaluation, or a Design System Spec creates
  or changes `DESIGN.md`; run its official-format and completeness gates in order.
- See [references/visual-source.md](references/visual-source.md) when qualifying and translating the selected visual source.
- Read [references/visual-direction-and-anti-slop.md](references/visual-direction-and-anti-slop.md) only when visual direction, redesign mode, theme/accent policy, density, or anti-slop acceptance is material.
- Read [references/frontend-layout-governance.md](references/frontend-layout-governance.md) when geometry, nested padding/insets, alignment, scrolling, or responsive ownership is material to the specification.
- Read [references/measurement-normalization.md](references/measurement-normalization.md) when selected-element evidence contains repeated spacing measurements or an even-grid policy applies.
- Read [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) when a selected source controls exact visual acceptance or a current runtime must be compared; validate each stage offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json).
- See [references/multi-surface.md](references/multi-surface.md) when a request covers more than one page, flow, or business domain.
- See [references/documentation-boundaries.md](references/documentation-boundaries.md) for durable UI locations, PRD links, and consumer reads.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
