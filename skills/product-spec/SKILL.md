---
name: product-spec
description: "Use when an ambiguous product feature, new product boundary, or named product fact source must become the smallest implementation-ready specification; owns product decisions and authorized spec artifacts, not implementation."
---

# Product Specification

## Overview

Turn product ambiguity into the smallest repository-grounded specification that
can authorize one implementation slice. Own product behavior, scope, business
rules, user-visible states, acceptance, and explicitly authorized product-fact
writes. Keep technical design and source mutation with their existing owners.

## Workflow

1. Read effective repository and host guidance, then inspect the requested scope,
   existing product facts, conventions, affected consumers, and `git status --short`
   before proposing a write.
2. Select exactly one public mode:
   - **Feature Spec** (default): specify one feature and include only the user-visible
     states, data effects, dependencies, and acceptance needed for that slice.
   - **Foundation Spec**: use only for a new product, new product line, or explicit
     redefinition of the product boundary.
   - **Artifact Update**: update only an existing, explicitly named product fact
     source after write authorization.
   When an existing Foundation Spec already fixes the product boundary and passes
   its applicable Ready gate, preserve it. For a requested downstream implementation,
   select the smallest source-proven feature gap and write only its Feature Spec;
   do not reopen product positioning without contradictory evidence.
3. Clarify internally before synthesis. Search discoverable repository facts first,
   then ask one decision-changing question at a time with a recommendation and
   trade-offs. Do not expose Discovery or grilling as a mode and do not implement.
4. Classify material statements as Confirmed, Assumption, Open Question, Rejected,
   or Deferred. Never silently convert an assumption into product behavior.
5. Produce one main feature or foundation document by default. Follow repository
   convention first; use the fallback locations in `references/documentation-boundaries.md`
   only when no equivalent exists and the user explicitly authorizes the write.
6. Apply **Ready for `<implementation slice>`**. Block only when a missing decision
   could change user behavior, business rules, permission or security boundaries,
   failure semantics, or acceptance results.
7. Hand off only the unresolved owner that must act now: deep cross-context domain
   work to `domain-modeling`, shared visual-system contracts to `ui-spec`, source
   changes to the matching `dev-*`, and review to `repo-review` when requested.
8. Preview product-document changes before writing unless the user explicitly
   requested implementation of the document edit. Validate links and repository
   checks that apply to the changed artifact.

## Do Not Use For

- Simple task decomposition, technical planning, or acceptance checks when product
  behavior is already decided; use host planning and repository instructions.
- Source implementation with a usable approved requirement; use `dev-frontend`
  or `dev-rust`.
- Business language, shared lifecycle, invariants, complex state machines, or
  multiple bounded contexts as the primary object; use `domain-modeling`.
- Selected-source UI specifications, shared tokens, component semantics, visual
  profiles, or `ui-spec` ownership; use `ui-spec`.
- Repository mapping or component inventory; use `repo-map`.
- Reviewing an existing change basis; use `repo-review`.

## Hard Rules

- Preserve repository product-document conventions and unrelated local changes.
- Write only explicitly authorized product artifacts. Do not edit source, stage,
  commit, push, create PRs, run implementation, or claim runtime verification.
- Do not require every implementation task to pass through this Skill.
- Do not invent users, rules, metrics, permissions, UI states, compatibility, or
  failure behavior. Keep unresolved material decisions visible.
- Keep one main document unless a repository convention or proven complexity needs
  a split. Glossaries, ADRs, UI evidence, and handoffs are conditional outputs.
- Do not specify or reference technical interfaces. When current implementation
  ownership or topology must be recorded, route that separate request to `repo-map`.
- Do not own source code, Git state, runtime evidence, a complete domain model, a
  shared design system, or repository-wide maps.
- Treat static checks as structure evidence only. Mark behavior, workflow, runtime,
  and consumer claims `Not verified` until directly evidenced.

## Output Contract

Report mode, repository evidence and convention used, implementation slice, main
artifact path or preview-only result, Confirmed/Assumption/Open/Rejected/Deferred
decisions, user flows and failure states, scope/non-goals, user-visible UI/data
effects that are actually applicable, acceptance criteria, Ready verdict and blockers,
conditional artifacts created or skipped, handoffs, validation, and every `Not found`
or `Not verified` gap. When the user explicitly requests an independent external
challenge or primary-source research, hand one fixed question/basis to
`ask-chatgpt`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for routing and mode examples.
- See [references/workflow.md](references/workflow.md) for clarification and Ready gates.
- See [references/template.md](references/template.md) for progressive document templates.
- See [references/documentation-boundaries.md](references/documentation-boundaries.md) for artifact ownership and fallback locations.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
