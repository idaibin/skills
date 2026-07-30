# External AI Collaboration Profiles

Use this reference only after the Codex-first gate determines that an independent
external-AI result is requested. Theme, provider, capability, and prompt strategy are
separate choices.

## Codex-First Gate

1. Derive the real outcome from natural language.
2. Check whether Codex, an existing Skill, or an available host tool can complete it
   with equal or better evidence.
3. Use an external provider only for a distinct requested result: independent
   challenge, provider-connected context, provider-specific research or image output,
   or reviewer-side browser observation.
4. If external use is useful but not authorized, finish safe local work and request
   only the missing provider/send authorization.

## Theme Profiles

- **Review:** defects, regressions, missing tests, unsafe assumptions, alternatives,
  and a scoped verdict against one fixed basis.
- **Repository:** architecture, modules, docs, contracts, risks, and contradictions
  against a fixed SHA and coverage manifest.
- **Product/domain:** behavior, scope, policy, terminology, rules, lifecycle,
  compatibility, and evidence for one decision.
- **UI/design:** user task, target surface/device, states, visual direction,
  accessibility, reference use/ignore rules, provenance, and acceptance.
- **Architecture:** boundaries, quality attributes, official constraints, contracts,
  tradeoffs, alternatives, migration cost, and basis applicability.
- **Implementation/security/delivery:** official API/toolchain behavior,
  advisories, standards, deployment/release constraints, and operational evidence.
- **Open-ended:** one bounded cross-theme question with source classes, exclusions,
  budget, and stop conditions.

## Capability Selection

Select only a capability verified on the active provider route:

- **Standard Chat:** compact synthesis, critique, decision challenge, or review.
- **Search:** short cited current or niche facts.
- **Deep Research:** multi-step sourced report with a reviewable plan when the
  provider exposes it.
- **Images or media:** create/edit an artifact only when that named-provider result is
  independently requested.
- **Reviewer browser/tools:** inspect declared targets as supporting evidence; keep
  this separate from the transport browser used to operate the provider UI.

Provider capability names are not portable equivalence claims. ChatGPT Deep Research,
Gemini modes, and similarly labeled features may have different contracts. Verify the
selected provider reference and live controls; otherwise use an authorized
same-provider fallback or stop.

## Prompt Strategy

- **Direct:** Codex creates one bounded prompt from verified context; default.
- **Plan-assisted:** inspect a provider's proposed research plan before starting only
  when that capability and extra step are authorized.
- **Prompt refinement:** use a separate external operation only when its draft is an
  independently useful result and separately authorized.

Every request includes only outcome, authoritative inputs, theme boundary, provider,
selected capability, must-answer questions, evidence rules, exclusions, desired
artifact, and stop condition.

## Common Contract

Fix one question or artifact goal and its decision/basis relationship. Prefer primary
sources, require attributable citations when research is requested, label inference
and conflicts, and compare conclusions with the fixed local basis. Treat every output
as external advice until Codex verifies it. Research and visual work never authorize
source, product-fact, Git, external-system, or publication changes.

For multi-provider work, keep the prompt and basis identical, do not expose one
provider's response to another, capture every response independently, and compare only
after attribution.

## Output

Return Codex-first decision, provider, theme, verified capability, prompt strategy,
question or artifact goal, basis relationship, source/asset boundary, attributed
external output, locally confirmed/rejected implications, and Not found/Not verified
gaps.
