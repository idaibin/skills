---
name: audit-frontend
description: "Use when a known frontend surface needs a scoped, read-only audit of selected architecture, reuse, data/UI contract, build/tooling, accessibility, performance, selected-source visual fidelity, or desktop-boundary profiles; use repo-review when a Worktree or immutable change basis needs coordination."
---

# Frontend Audit

## Overview

Audit frontend engineering from repository evidence rather than a universal framework or folder template. Detect the real framework and local API style, then select only the profiles required by the request. This skill is read-only: use it directly for frontend domain audits or as a bounded specialist under `repo-review`; use `dev-frontend` for requested changes.

## Rule Priority

Resolve conflicts in this order:

1. The user's current explicit request.
2. Effective repository guidance, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
3. Declared and applicable product/UI contracts: product requirements or product
   Feature Specs define behavior and acceptance; selected-source UI Feature Specs
   and root `DESIGN.md` define applicable UI and shared visual semantics.
4. Live code, config, components, and the repository-declared visual system define
   current implementation facts. They do not override an applicable contract; report
   a conflict as implementation drift.
5. This skill.
6. External reference repositories.

Never rewrite a working local structure merely to match this skill or an external repository.
When a repository has not adopted root `DESIGN.md`, follow its declared visual-system
owner; do not invent one.

## Workflow

1. Read repository guidance, record the inspected revision plus relevant Worktree
   state for reproducibility, run `git status --short`, and identify the target
   app, project class, framework, package manager, scripts, documented
   architecture, and coordinating review owner when delegated. This inspection
   snapshot does not turn the audit into change attribution.
2. Consume current `repo-map` output or perform a targeted inventory of route/page entry, owning feature, analogous screens, UI primitives, layout/tokens, data/cache, forms/schema, state/store, tests, docs, and desktop adapter. Load `references/specification-authorities.md` when a selected profile depends on product or UI contracts; resolve them by meaning rather than filename, consume existing contracts directly, and hand off only unresolved decisions required by the audit outcome.
3. Classify the product surface as Web, high-density Console, or Tauri Desktop. Select exactly one framework profile per audited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles present in scope: **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, **shadcn/ui**, or a documented local system.
4. Select one or more audit profiles; explicitly mark the rest `Out of scope`:
   - **Architecture/reuse:** routes, features, shared layers, dependency direction, reuse, abstractions, structural lifecycle, and docs.
   - **State/data/contracts:** server/cache, URL, form, shared business, local UI, reactivity, stores, schemas, requests, errors, cancellation, and native IPC contracts.
   - **Component/layout/design system:** primitives, variants, tokens, density, DOM/CSS, spacing/scroll ownership, responsive behavior, and duplicated systems.
   - **Selected-source visual fidelity:** source identity/evidence, traceable targets versus current runtime, assets, typography, final contrast, geometry, section alignment, states, breakpoints, and comparison evidence.
   - **Accessibility:** semantics, keyboard, focus, labels, dialogs/popovers, errors, status communication, and async feedback.
   - **Performance:** render/reactivity/data paths, request duplication, fan-out, bundle/runtime/IPC cost, long tasks, and measurement quality.
   - **Build/tooling:** package/runtime pins, scripts, Vite/Rolldown, Webpack,
     Rspack, Next/Turbopack, plugins, resolution, environment, proxy, base,
     output, SSR/library, and deployment contracts.
   - **Desktop boundary:** frontend adapter, Tauri/native commands, DTO/errors, progress, cancellation, window/menu/shortcut behavior, and real-client evidence.
5. Map each selected responsibility to its page, feature, primitive, hook/composable, service, store, schema, local type, or desktop adapter owner.
6. Compare the target with direct reuse candidates, the nearest analogous feature, documented contracts, and the existing component/layout system. For a selected Component/Layout profile, load `references/frontend-layout-governance.md`, name the relevant geometry/scroll/layer owners, and trace only the applicable task-completion seam. When a root `DESIGN.md` contract is relevant, also load `references/design-md-compliance.md` for the bounded contract-to-runtime chain. For Selected-source visual fidelity, load [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md), keep source targets distinct from browser-computed runtime, and require reviewable source/runtime comparison plus computed evidence for exact runtime claims.
7. Trace only selected profiles without changing the repository. Do not perform shallow checks for excluded profiles merely to imply coverage. When code-quality concerns materially apply, load the shared code-quality reference with audit semantics and the selected framework/build reachability rules.
8. Audit applicable loading, empty, error, partial, retry, optimistic, stale, cancellation, keyboard, focus, and long-task behavior within the selected profiles.
9. Use non-mutating repository checks and request browser or real-client evidence only when a selected claim cannot be proven statically.
10. Report severity-ranked findings with exact location, framework-specific evidence, impact, remediation direction, validation gap, selected profiles, and excluded profiles.

## Modes

- **Focused profile audit:** one or two selected frontend profiles with bounded evidence.
- **Combined frontend audit:** interacting profiles such as state/data plus performance or layout plus accessibility, with explicit integration risk.
- **Baseline architecture audit:** architecture/reuse plus structural lifecycle and docs against real repository conventions.
- **Scoped specialist subreview:** inspect only the frontend paths or diff delegated by `repo-review`; return domain findings without taking review coordination or Git ownership.

## Hard Rules

- Select profiles before applying detailed checklists. Do not imply architecture, state, layout, accessibility, performance, and desktop were all reviewed when only some were evidenced.
- Do not recommend a shared component, hook, composable, store, service, schema, or layout system before searching existing implementations and recording why reuse or adaptation is insufficient.
- Load and apply only the selected framework, styling, architecture, state/data,
  build/tooling, accessibility/performance, desktop, or conditional
  code-quality reference. Do not cross-apply an unselected profile or imply its
  coverage.
- Require reachable source evidence for ownership and reuse, and direct runtime or
  measurement evidence when the selected claim cannot be established statically.
- Do not report spacing, density, fixed geometry, nested scrolling, or overlay
  behavior from taste or pattern matching alone. Require a contract violation,
  competing ownership, measured inconsistency, or concrete user impact; otherwise
  record the visual judgment as `Not verified`.
- For an applicable root `DESIGN.md`, trace contract token/component/layout/pattern
  to implementation adapter/config, live component/consumer, and static or runtime
  evidence. Do not infer exact values from pixels; without runtime evidence, mark
  responsive, scroll, accessibility, and rendered-compliance claims `Not verified`.
- Do not refactor unrelated legacy code. File length alone never justifies splitting.
- Do not call code dead from text-search absence alone or prescribe one
  component per file, named exports, memoization, or a bundler migration as a
  universal React rule.
- Do not edit, stage, commit, post review comments, or deliver code in audit mode. `repo-review` owns Worktree and immutable review coordination; `repo-delivery` alone owns Git mutation. Route accepted remediation to `dev-frontend`.
- Do not treat build/lint success, source CSS, current-runtime similarity, or a single screenshot as selected-source visual acceptance. Lead with P0-P3 visual findings and mark missing desktop/breakpoint/state evidence `Not verified`.

## Do Not Use For

- Repository orientation, commands, reuse inventory, or docs/code alignment without an audit request; use `repo-map`.
- Frontend implementation, modification, or refactoring; use `dev-frontend`.
- Creating a repository-root `DESIGN.md` or selected-source Feature Specs; use `ui-spec`.
- Root-cause diagnosis of a concrete failure; use the host's built-in diagnosis under effective instructions.
- Owning Worktree readiness or immutable repository/range/PR/release coordination; use `repo-review`, which may delegate a bounded frontend surface here.
- Actual staging, commit, rebase/squash, push, or delivery; use `repo-delivery`.
- Browser or real desktop runtime operation; use `ops-browser` or `ops-client`.
- A backend-only Rust implementation or audit; use `dev-rust` or `audit-rust`.

## Output Contract

Start with the inspection snapshot, selected product, framework, styling, and audit profiles; explicitly excluded audit profiles; coordinating owner when delegated; and severity-ranked findings. For Selected-source visual fidelity, state the source/revision/approval, evidence levels, target viewport/state, comparison passes available, and whether the `frontend-visual-evidence/v1` artifact validates. For each finding, report impact, exact location, profile-specific evidence, recommended remediation owner/direction, and validation gap. Then summarize inspected rules/files, existing candidates, ownership map, selected state/data/layout/accessibility/performance/build/desktop evidence, component/injection/router/lifetime contracts, Google `DESIGN.md` token/prose consistency, official lint evidence, implementation drift from source, commands/runtime evidence, and all `Not found` or `Not verified` residual risks.

## References

- Read [architecture-and-ownership.md](references/architecture-and-ownership.md) for discovery, directories, routes, pages, and file responsibility.
- Read [specification-authorities.md](references/specification-authorities.md) when
  product requirements, root `DESIGN.md`, slice UI contracts, or their drift are in
  the selected audit scope.
- Read [frontend-layout-governance.md](references/frontend-layout-governance.md)
  for evidence and false-positive rules when Component/Layout is selected.
- Read [design-md-compliance.md](references/design-md-compliance.md) only when an
  applicable Component/Layout audit includes root `DESIGN.md` consistency.
- Read [frontend-visual-evidence.md](references/frontend-visual-evidence.md) when a selected source or visual-completion claim is in scope; validate staged evidence offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json).
- Read [framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native audit rules.
- Read [component-system.md](references/component-system.md) for primitives, feature components, composition, variants, and reuse decisions.
- Read [state-data-and-forms.md](references/state-data-and-forms.md) for state classes, requests, caching, feedback states, services, schemas, and forms.
- Read [styling-and-layout.md](references/styling-and-layout.md) for tokens, spacing, responsive layout, Console density, DOM, and CSS ownership.
- Read [styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack audit rules.
- Read [desktop-tauri.md](references/desktop-tauri.md) for frontend adapters, commands, Rust boundaries, windows, shortcuts, progress, and cancellation.
- Read [accessibility-and-performance.md](references/accessibility-and-performance.md) for keyboard/focus checks and evidence-based performance review.
- Read [build-tooling.md](references/build-tooling.md) when package scripts,
  bundler configuration, Vite/Rolldown, framework build behavior, or deployment
  output is selected.
- Read [code-quality.md](references/code-quality.md) when duplication,
  dead/unused code, abstraction quality, hidden coupling, or maintainability is
  materially in scope.
- Read [review-checklist.md](references/review-checklist.md) for the profile-driven audit sequence.
- Read [anti-patterns.md](references/anti-patterns.md) for detectable failure patterns and corrective decisions.
- Read [reference-corpus.md](references/reference-corpus.md) for official source evidence, adopted rules, and rejected cargo-cult choices.
- Read [usage.md](references/usage.md) for trigger, routing, and profile examples.
- Read [eval-cases.md](references/eval-cases.md) for trigger, non-trigger, scenario, quality, and scoring evals.
- See [references/codebase-design.md](references/codebase-design.md) only for a selected public-module, seam, abstraction, locality, or testability audit.
