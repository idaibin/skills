# Frontend Profile

## Contents

- [Selection](#selection)
- [Audit Profiles](#audit-profiles)
- [Conditional References](#conditional-references)
- [Modes](#modes)
- [Output Additions](#output-additions)
- [Trigger Examples](#trigger-examples)
- [Non-Triggers](#non-triggers)

Audit frontend engineering from repository evidence rather than a universal
framework or folder template. Detect the real framework and local API style,
then select only the profiles required by the request.

## Selection

1. Classify the product surface as Web, high-density Console, or Tauri
   Desktop. Select exactly one framework profile per audited boundary:
   **React**, **Vue Composition**, **Vue Options**, or **Repository-native
   Other**. Select only styling profiles present in scope: **Tailwind**,
   **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, **shadcn/ui**,
   or a documented local system. A styling technology is not a separate audit;
   it shares this profile's owner, read-only boundary, and report contract.
2. Select one or more audit profiles; explicitly mark the rest `Out of scope`.
3. Map each selected responsibility to its page, feature, primitive,
   hook/composable, service, store, schema, local type, or desktop adapter
   owner, and compare with direct reuse candidates, the nearest analogous
   feature, documented contracts, and the existing component/layout system.

## Audit Profiles

- **Architecture/reuse:** routes, features, shared layers, dependency
  direction, reuse, abstractions, structural lifecycle, and docs.
- **State/data/contracts:** server/cache, URL, form, shared business, local
  UI, reactivity, stores, schemas, requests, errors, cancellation, and native
  IPC contracts.
- **Component/layout/design system:** primitives, variants, tokens, density,
  DOM/CSS, spacing/scroll ownership, responsive behavior, and duplicated
  systems.
- **Selected-source visual fidelity:** source identity/evidence, traceable
  targets versus current runtime, assets, typography, final contrast,
  geometry, section alignment, states, breakpoints, and comparison evidence.
- **Accessibility:** semantics, keyboard, focus, labels, dialogs/popovers,
  errors, status communication, and async feedback.
- **Performance:** render/reactivity/data paths, request duplication, fan-out,
  bundle/runtime/IPC cost, long tasks, and measurement quality.
- **Build/tooling:** package/runtime pins, scripts, Vite/Rolldown, Webpack,
  Rspack, Next/Turbopack, plugins, resolution, environment, proxy, base,
  output, SSR/library, and deployment contracts.
- **Desktop boundary:** frontend adapter, Tauri/native commands, DTO/errors,
  progress, cancellation, window/menu/shortcut behavior, and real-client
  evidence.

## Conditional References

- Load [architecture](frontend-architecture-and-ownership.md) for ownership
  and authority mapping, and [frameworks](frontend-framework-profiles.md) for
  the selected framework's contracts.
- When Architecture/Reuse or Component/Layout examines component APIs,
  variants, or composition, load [components](frontend-component-system.md).
- For a selected Component/Layout profile, load
  [layout governance](frontend-layout-governance.md), name the relevant
  geometry/scroll/layer owners, trace nested effective padding by axis, and
  cover only the applicable task-completion seam. When maintained
  CSS/Sass/Less ownership, cascade, flex/grid choice, or wrapper structure is
  in scope, also load [CSS governance](frontend-css-governance.md). Load
  [layout/style](frontend-styling-and-layout.md) and
  [styling systems](frontend-styling-systems.md) for the selected styling
  surface.
- When the audit explicitly covers visual direction, an existing-surface
  redesign, theme/accent consistency, density, or anti-slop drift, load
  [visual direction](visual-direction-and-anti-slop.md); require an accepted
  direction, analogue, measurement, or user impact rather than treating taste
  as a finding.
- When a resolved `<design-root>/DESIGN.md` contract is relevant, load
  [DESIGN.md compliance](frontend-design-md-compliance.md) for the bounded
  contract-to-runtime chain. Load [specs](specification-authorities.md) when a
  selected profile depends on Product/UI contracts; resolve them by meaning
  rather than filename, consume Product Markdown, UI Markdown, and resolved
  `DESIGN.md` before comparing current source, and hand off only unresolved
  decisions required by the audit outcome.
- For Selected-source visual fidelity, load
  [visual evidence](frontend-visual-evidence.md), keep source targets distinct
  from browser-computed runtime, and require reviewable source/runtime
  comparison plus computed evidence for exact runtime claims. Do not treat
  build/lint success or one screenshot as visual acceptance.
- When adoption/completeness is in scope, verify official-format evidence
  separately from the `ui-spec-design-completeness/1` result and exact
  design-hash approval. A local `awaiting-trusted-approval-verification`
  result without a satisfied consumer claim is blocking; only a host-trusted
  approval receipt bound to the same Result Package clears it, without
  rewriting the producer result. Do not use lint zero, current theme/CSS, or
  PackageManifest integrity to clear a missing, untrusted, or `not-ready`
  shared authority.
- When State/data/contracts reaches an adopted OpenAPI or generated-client
  chain, load [protocol contracts](frontend-protocol-contracts.md) and audit
  only the frontend consumer boundary.
- When a selected profile exposes a structural UI projection, verify its named
  owner, producer, non-LLM consumer, semantic version, executable validator,
  drift policy, and retirement rule. Inspect current validator evidence,
  consumer read path, and Markdown/source parity without regenerating or
  repairing the projection. When no real projection exists, do not require
  project YAML/JSON, schema, or validator files.
- When the user supplies a new or replacement external contract, freeze that
  artifact and the stated replacement relation as part of the inspection basis
  before reading the older local copy. Audit against the selected incoming
  authority and report local drift; because this Skill is read-only, never
  land or overwrite the document. Stop on ambiguous owner or competing
  versions instead of reviewing a knowingly superseded basis.
- Audit applicable loading, empty, error, partial, retry, optimistic, stale,
  cancellation, keyboard, focus, and long-task behavior within the selected
  profiles; load
  [accessibility/performance](frontend-accessibility-and-performance.md),
  [build](frontend-build-tooling.md), and
  [Tauri](frontend-desktop-tauri.md) only when their profile is selected.

## Modes

- **Focused profile audit:** one or two selected frontend profiles with
  bounded evidence.
- **Combined frontend audit:** interacting profiles such as state/data plus
  performance or layout plus accessibility, with explicit integration risk.
- **Baseline architecture audit:** architecture/reuse plus structural
  lifecycle and docs against real repository conventions.
- **Scoped specialist subreview:** inspect only the frontend paths or diff
  delegated by `repo-review`; return domain findings without taking review
  coordination or Git ownership.

## Output Additions

Lead with capability `frontend.surface.audit`, the selected product surface,
framework profile, styling profile, and audit profiles. For Selected-source
visual fidelity, state the source/revision/approval, evidence levels, target
viewport/state, comparison passes available, and whether the
`frontend-visual-evidence/v1` artifact validates. Summarize ownership map,
selected state/data/layout/accessibility/performance/build/desktop evidence,
component/injection/router/lifetime contracts, DESIGN.md token/prose
consistency, implementation drift from source, and residual risks.

## Trigger Examples

- `Audit this Console for architecture/reuse and state/data only; leave accessibility and performance out of scope.`
- `Audit this Vue 3 feature for reactivity loss, watcher loops, composable lifetime, Pinia ownership, and Router contracts.`
- `Audit this frontend design system for duplicated primitives, variants, tokens, spacing, and scroll ownership.`
- `Audit this React and Tailwind table for scale drift, class conflicts, responsive behavior, and duplicated spacing ownership.`
- `Audit this Vue Options and Ant Design form without converting its API style or replacing its component system.`
- `Review accessibility and performance for this React table using browser evidence where static inspection is insufficient.`
- `Audit this Tauri frontend boundary for adapters, progress, cancellation, errors, menus, and shortcuts.`
- `Audit whether this Vite app needs Rolldown configuration and verify its production-output contract.`
- `Under repo-review, inspect only the changed frontend paths for selected state/data and layout profiles.`

## Non-Triggers

- `Change this button label in the known component.` — use `dev-frontend`.
- `Find why this page crashes.` — use the host's built-in diagnosis under
  effective instructions until the cause is confirmed.
- `Verify the page in a browser.` — use `ops-browser`.
- `Review the whole repository or a commit range and coordinate all domains.`
  — use `repo-review`, which may delegate a bounded frontend surface here.
- `Turn this selected visual source into a Feature Spec.` — use `ui-spec`.
- `Audit only a local CSS color token rename with no reachable API, build,
  runtime, or cross-repo effect.` — keep project grounding inactive and
  unrelated profiles out of scope.

Do not split frontend audits into separate `audit-react`, `audit-vue`, or
`audit-ui` skills: these concerns share the same repository guidance,
ownership map, read-only boundary, fix owner, and severity/report contract.
A future screenshot/Figma-first product-experience audit may justify a
separate owner; ordinary source-backed UI review remains a profile here.
