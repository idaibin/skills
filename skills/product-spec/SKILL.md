---
name: product-spec
description: "Use when an ambiguous product feature, new product boundary, or named product fact source must become the smallest implementation-ready specification; owns product decisions and authorized spec artifacts, not selected-source UI specification or implementation."
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
3. Apply the product scope gate before synthesis. Distinguish several surfaces of one
   connected feature from several independent features with different user jobs,
   behavior, rules, or acceptance. Keep one Feature Spec for the former. For the
   latter, produce one short product index and maintain one independently ready fact
   slice per confirmed feature; never default home, tasks, contacts, and profile into
   one omnibus Feature Spec.
4. Clarify internally before synthesis. Search discoverable repository facts first.
   When Axure is a named product source, load
   [references/prototype-evidence.md](references/prototype-evidence.md), consume a
   coverage-ledger handoff from `ops-browser`, and keep prototype coverage separate
   from product readiness.
   When material product decisions remain, load
   [references/decision-pressure-test.md](references/decision-pressure-test.md) and
   resolve only the target slices' load-bearing decision tree. Do not expose
   Discovery or grilling as a public mode and do not implement.
5. Classify material statements as Confirmed, Assumption, Open Question, Rejected,
   or Deferred. Never silently convert an assumption into product behavior. When a
   fact materially changes scope, user outcome, data risk, or acceptance, trace it to
   the affected slice and observable acceptance consequence without defining a
   technical interface.
6. Produce one main feature or foundation document by default, or a short index plus
   slice documents for a proven multi-feature request. Follow repository convention
   first; use the fallback locations in `references/documentation-boundaries.md` only
   when no equivalent exists and the user explicitly authorizes the write.
7. Apply **Ready for `<implementation slice>`** to every product slice. Block only
   that slice when a missing decision
   could change user behavior, business rules, permission or security boundaries,
   failure semantics, or acceptance results.
8. Hand off only the unresolved owner that must act now: deep cross-context domain
   work to `domain-modeling`, shared visual-system contracts to `ui-spec`, source
   changes to the matching `dev-*`, and review to `repo-review` when requested.
9. Preview product-document changes before writing unless the user explicitly
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
- Do not infer complete product behavior from prototype screenshots, visited page
  titles, static export alone, or an interaction set whose coverage is unknown.
- Keep one main document unless a repository convention or proven complexity needs
  a split. Independent features are proven complexity: use a short index and separate
  slice facts, not one large specification. Glossaries, ADRs, UI evidence, and
  handoffs are conditional outputs.
- Do not duplicate colors, typography, component choices, token values, or page
  geometry. Link the applicable `ui-spec` contract and keep only product behavior,
  user-visible meaning, and acceptance here.
- Make every product slice independently consumable: implementation reads shared
  index facts plus the target slice only, never every sibling specification.
- Do not define technical interfaces. Cite a verified existing dependency, owner, or
  interface fact only when it is necessary to make the implementation handoff
  unambiguous; route current topology mapping to `repo-map` and new technical design
  to host planning.
- Do not own source code, Git state, runtime evidence, a complete domain model, a
  shared design system, or repository-wide maps.
- Treat static checks as structure evidence only. Mark behavior, workflow, runtime,
  and consumer claims `Not verified` until directly evidenced.

## Output Contract

Report mode, repository evidence and convention used, product scope classification,
shared index and slice artifact paths or preview-only result, Confirmed/Assumption/Open/Rejected/Deferred
decisions, user flows and failure states, scope/non-goals, user-visible UI/data
effects that are actually applicable, acceptance criteria, one Ready verdict and
blockers per slice,
conditional artifacts created or skipped, handoffs, validation, and every `Not found`
or `Not verified` gap. For a prototype source, also report fixed source identity,
coverage verdict/totals, conflicts, and affected slices. When the user explicitly requests an independent external
challenge or primary-source research, hand one fixed question/basis to
`ask-ai`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for routing and mode examples.
- See [references/workflow.md](references/workflow.md) for clarification and Ready gates.
- See [references/decision-pressure-test.md](references/decision-pressure-test.md)
  when evidence leaves material product decisions unresolved or the user explicitly
  requests a product stress test.
- See [references/template.md](references/template.md) for progressive document templates.
- See [references/documentation-boundaries.md](references/documentation-boundaries.md) for artifact ownership and fallback locations.
- Read [references/prototype-evidence.md](references/prototype-evidence.md) when Axure supplies product facts.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
