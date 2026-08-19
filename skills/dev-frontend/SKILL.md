---
name: dev-frontend
description: "Use when an authorized frontend change must be implemented or refactored; owns frontend source edits and risk-matched validation, not audit-only work, UI specification, browser/client operation, or Git delivery."
---

# Frontend Implementation

## Overview

Implement the requested frontend behavior in the repository's existing stack. Reuse
the nearest proven component, hook, service, style, and page structure by default;
extend before creating, and create only when current owners cannot satisfy the task.

Consume `urn:skills:frontend-change-request:v1` and produce
`urn:skills:source-change-result:v1`. Typed Task, authority, graph, or package inputs
are used when supplied; they do not replace current source and repository contracts.

## Workflow

1. Read effective repository guidance, identify the real frontend root, package
   manager, runtime, target route/component, and current Worktree state.
2. Read only the authorities and source needed for the target slice. Start with the
   user requirement and current implementation; use Product/UI specs and the resolved
   `<design-root>/DESIGN.md` only when they apply. A missing optional artifact or graph
   does not create a prerequisite ceremony.
3. Complete the [reuse and page-ownership checklist](references/checklist.md): search
   existing components and analogous pages, choose `reuse`, `extend`, `wrap`, or a
   justified `new` owner, and keep route/tab shells declarative. Independent tabs or
   sections with their own data, actions, forms, validation, or lifecycle belong in
   feature components instead of one large conditional page.
4. Confirm the observable acceptance, non-goals, affected contracts, and smallest
   credible validation seam. Load [project grounding](references/project-grounding.md)
   only when the change crosses a real API/auth, environment/build, durable-data,
   desktop/native, compatibility, deployment, or cross-repository boundary. Keep
   unrelated risk classes out of scope.
5. Make the smallest coherent source change. Preserve established framework, routing,
   state/data, component, styling, and test owners; do not introduce a parallel stack
   or speculative shared layer.
6. Run the nearest focused repository-owned check during iteration. Expand only for a
   changed shared contract, generated/build chain, runtime boundary, or affected
   consumer. Reserve full builds and full suites for final delivery, release,
   deployment, explicit requests, or when no narrower credible check exists.
7. Report changed owners, reuse decisions, validation, remaining Worktree content, and
   every applicable runtime or external gap as `Not verified`. Source implementation
   does not authorize browser/client operation or Git delivery.

## Conditional Profiles

- **Selected visual source:** load [authorities](references/specification-authorities.md)
  and [visual evidence](references/frontend-visual-evidence.md) only when an accepted
  source and implementation-ready UI contract actually govern the task. Map applicable
  acceptance IDs before editing; use `ops-browser` or `ops-client` for required runtime
  evidence. Two-pass same-state comparison is a visual-completion gate, not a default
  requirement for ordinary frontend changes.
- **Layout or responsive behavior:** load
  [layout governance](references/frontend-layout-governance.md) when geometry,
  overflow, scrolling, layering, or breakpoints materially change.
- **Protocol or generated client:** load [protocol contracts](references/protocol-contracts.md)
  only for an existing or explicitly introduced contract chain.
- **Behavior-first implementation:** load [behavior first](references/behavior-first.md)
  when a stable public seam can support one red-capable check per behavior.
- **Framework, styling, state, desktop, tooling, quality:** load only the matching
  [framework](references/framework-profiles.md), [styling](references/styling-systems.md),
  [stack](references/stack-guidelines.md), or [code-quality](references/code-quality.md)
  profile required by the current change.
- **Forgeway integration:** when an immutable Run and input PackageManifest are
  supplied, bind the changed result and observations to that basis. Do not require a
  Forgeway Run for normal repository development.

For a maintained non-LLM UI projection: Require a named owner, producer, non-LLM
consumer, semantic version, executable validator, drift policy, and retirement rule.
Run the repository-defined non-mutating validator before relying on it, then verify
referenced routes and components in current source. Otherwise ignore the projection
rather than creating or repairing one for ordinary implementation.

## Hard Rules

- Follow repository-pinned versions, lockfiles, scripts, directories, and dependency
  policy; do not normalize unrelated tooling.
- Existing components, adapters, stores, utilities, tokens, and interaction patterns
  are the default. A new owner needs a targeted search and a concrete behavior or
  ownership reason.
- Keep page/tab shells responsible for navigation and composition, not section-specific
  APIs, forms, tables, drawers, validation, and lifecycle branches.
- Prefer non-mutating validation. Compare Worktree state around tools that may generate
  or rewrite files and never absorb unexplained drift.
- A build, lint pass, source inspection, or browser preview proves only its own layer.
  Mark unexercised visual, responsive, accessibility, network, desktop, deployment, and
  production behavior `Not verified`.
- Stop on missing source-edit authorization, an unresolved governing contract, or a
  second failure of the same frozen runtime acceptance; preserve evidence and return to
  diagnosis instead of adding speculative patches.
- Do not stage, commit, push, deploy, or open a pull request from this Skill.

## Output

Return capability `frontend.source.implement` with scope, project/stack, authority and
reuse decisions, changed files/contracts, focused and expanded validation, Worktree
drift, exclusions, and `Not verified` gaps. Include visual mapping and runtime passes
only when the selected-source profile was active.

## References

- Core: [usage](references/usage.md), [checklist](references/checklist.md),
  [authorities](references/specification-authorities.md),
  [grounding](references/project-grounding.md), [evals](references/eval-cases.md).
- Conditional: [layout](references/frontend-layout-governance.md),
  [visual direction](references/visual-direction-and-anti-slop.md),
  [motion](references/interaction-motion-quality.md),
  [visual evidence](references/frontend-visual-evidence.md),
  [visual example](references/frontend-visual-gate-example.md),
  [protocols](references/protocol-contracts.md),
  [behavior first](references/behavior-first.md),
  [codebase design](references/codebase-design.md),
  [frameworks](references/framework-profiles.md), [styling](references/styling-systems.md),
  [stack](references/stack-guidelines.md), [quality](references/code-quality.md).
