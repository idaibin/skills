# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Audit a TanStack Router Console feature for architecture/reuse and query-state contracts; leave accessibility out of scope.` | Trigger `audit-frontend` with Architecture/Reuse and State/Data/Contracts profiles. |
| `Audit a Vue 3 feature for reactivity loss, watcher loops, composable lifetime, Pinia ownership, and Router contracts.` | Trigger State/Data/Contracts with the Vue Composition API framework profile. |
| `Under repo-review, perform a read-only specialist audit of only the changed Vue SFCs for state, lifecycle, accessibility, and performance.` | Trigger bounded `audit-frontend`; keep `repo-review` as local Git-change review owner. |
| `Under repo-review, inspect only the changed frontend paths for design-system duplication and accessibility.` | Trigger bounded `audit-frontend`; keep `repo-review` as repository/range review owner. |
| `Audit the Tauri frontend/Rust boundary for progress, cancellation, errors, menus, and shortcuts.` | Trigger Desktop Boundary plus applicable State/Data/Contracts. |
| `Audit this frontend design system for duplicated primitives, variants, tokens, spacing, and scroll ownership.` | Trigger Component/Layout/Design System. |
| `Audit this React and Tailwind table for scale drift, class conflicts, responsive behavior, and duplicated spacing ownership.` | Trigger React plus Tailwind with Component/Layout/Design System; add Performance only when evidence warrants it. |
| `Audit this Vue Composition and Pinia feature for reactive ownership, Router teardown, and stale requests.` | Trigger Vue Composition plus State/Data/Contracts. |
| `Audit this Vue Options and Ant Design form without recommending Composition conversion or component replacement.` | Trigger Vue Options plus Ant Design with State/Data/Contracts and Component/Layout/Design System. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Change one known component's copy and keep everything else unchanged.` | Prefer `implement-frontend`. |
| `Find the unknown cause of this failing frontend test.` | Prefer `diagnose`. |
| `Operate the real Tauri window and capture evidence.` | Prefer `ops-client`. |
| `Review the whole local dirty tree and prepare exact staging.` | Prefer `repo-review`. |
| `Review this entire repository range and coordinate frontend, Rust, security, CI, and docs.` | Prefer `repo-review`, which may delegate bounded frontend paths. |
| `Stage and commit the accepted frontend fix.` | Prefer `repo-delivery`. |

## Scenario Eval

Each scenario must produce the listed investigation, decision, rejection, and report evidence.

| # | Input scenario | Investigate | Correct decision | Reject | Final report |
| --- | --- | --- | --- | --- | --- |
| 1 | Pages each implement Button, Dialog, Table, and spacing | select Architecture/Reuse and Component/Layout profiles; imports, primitives, variants, tokens, behavior differences | identify reuse/composition candidates and stable variants | copy-and-restyle or forced merger of unrelated workflows | selected/excluded profiles, candidates, owner, duplicates, validation gaps |
| 2 | New feature directory is unclear | Architecture/Reuse; router, adjacent features, aliases, docs, exports, business owner | follow nearest ownership pattern; justify every new layer | new shared/common tree for neatness | ownership map, new-file reasons, lifecycle updates |
| 3 | Component is large but splitting adds navigation | selected architecture/state/layout evidence, responsibilities, state/data/layout coupling, tests | keep cohesive or split only at stable ownership seam | line-count-based extraction | evidence for keeping/splitting and residual complexity |
| 4 | Global store holds local dialog state | State/Data; consumers, persistence, route/window lifetime, existing local pattern | move local unless durable cross-tree behavior is proven | globalize to avoid props | state class, owner, affected consumers/tests |
| 5 | TanStack route file contains business logic | Architecture/Reuse and State/Data; params/search/loader contract, services, tests | keep route composition/guards; move stable workflow to owner | empty wrappers or router contract changes | route contract, owner, generated checks |
| 6 | Vue Composition API component destructures reactive/Pinia state and uses broad watchEffect for API calls | State/Data; refs/computed/storeToRefs, synchronous watchEffect dependencies, invalidation, Router/keep-alive lifetime, cancellation | preserve reactivity with local convention; computed for derivation; intentional dependencies and stale-work cancellation | React effect rules, mechanical toRefs, hidden global composable state, watcher request loops | reactivity break, dependency window, lifetime owner, cancellation evidence |
| 7 | UI, API helper, and Rust validate a form differently | State/Data; schemas, DTO, backend authority, error mapping | align authoritative contract and compatibility | three drifting copies or client-only authority | schema owners, compatibility, field/general error tests |
| 8 | Tauri page invokes Rust on every keypress | State/Data, Performance, Desktop; frequency, payload, latency, cache/batch/stream options | debounce/batch/cache or adapter/subscription from evidence | direct high-frequency invokes or optimization by intuition | selected profiles, path/frequency evidence, native gap |
| 9 | SQLite task freezes UI without progress | Desktop and Performance; command execution, milestones, cancel path, cleanup | async domain task with real progress, cancellation, terminal states | fake timer progress or uncancellable blocking invoke | channel/events, cancel semantics, real-client verification |
| 10 | Similar pages use inconsistent spacing | Component/Layout; shell/page/layout primitives, tokens, duplicated margins/breakpoints | assign one spacing/token owner and remove patches | new page-specific magic values | owner, token/primitive reused, responsive proof |
| 11 | Agent wants unrelated refactor | request scope, delegated boundary, dirty ownership | exclude unrelated changes and note separately | opportunistic cleanup | exact scope and excluded ideas |
| 12 | Project convention conflicts with skill | user request, nearest guidance, existing code/docs | follow rule priority and preserve local contract | enforce external reference or skill preference | conflict, winning rule, preserved exception |
| 13 | Code and architecture docs disagree | Architecture/Reuse; runtime/source, docs/indexes, ownership history | identify authority and complete synchronized remediation scope | change code only and leave stale docs | mismatch, authority, required files, validation |
| 14 | Vue feature has injected mutable state, temporary global guards, and cached routes | State/Data; injection owner, guard registration/removal, activated/deactivated cleanup, duplicate listeners and stale requests | provider/store owns mutation, guards unregister, cleanup matches route/cache lifetime | string injection, consumer-owned shared mutation, duplicated guards, unmount-only cleanup | provider/store/router owners, teardown/cancellation evidence |
| 15 | `repo-review` delegates changed frontend paths for domain review | delegated paths, local dirty-tree owner, framework/profile evidence, relevant diff | inspect only delegated paths and return specialist findings to `repo-review` | reclassify dirty tree, stage, commit, or claim readiness | specialist mode, path boundary, profiles, findings, untouched Git state |
| 16 | Pure Options API component uses data, computed, watch options, dynamic this.$watch, keep-alive, and component guards | State/Data; local API convention, unwatch handle, lifecycle, guards, cancellation | audit native Options semantics and retain API style | require Composition helpers or incidental conversion | Options owners, cleanup, guard/request lifetime, runtime gap |
| 17 | `repo-review` delegates a frontend range while Rust and CI are reviewed elsewhere | delegated immutable range/paths, selected profiles, cross-domain interfaces | return bounded frontend findings and gaps to `repo-review` | take final P0-P3 integration ownership or review unrelated backend paths | coordinator, range/path boundary, selected/excluded profiles, findings |
| 18 | User asks only for accessibility audit of a stable page | Accessibility evidence, semantics, keyboard/focus, forms/status, browser capability | select Accessibility only and request runtime proof where needed | perform architecture/state/performance audit without evidence | selected Accessibility, excluded profiles, static/runtime gaps |
| 19 | React table uses Tailwind with repeated arbitrary widths and conflicting responsive utilities | React plus Tailwind; Component/Layout; configured scale, class helpers, breakpoints, parent/child spacing, rendered evidence | use existing scale or named geometry owner and remove conflicting ownership | global Tailwind config expansion or performance claims without evidence | framework/styling profiles, exact class evidence, layout owner, runtime gap |
| 20 | Vue Options form uses Ant Design and local Less overrides | Vue Options plus Ant Design and Less; State/Data and Component/Layout; native watchers/lifecycle, form contracts, tokens, selector specificity | preserve Options API and AntD ownership; prefer tokens/props over brittle overrides | Composition conversion, shadcn replacement, or deeper generated-class selectors | API/style profiles, form and styling owners, exact overrides, verification gap |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Grounding | reads guidance/status and inventories only evidence needed for selected profiles | starts from a universal template or scans everything |
| Profile selection | declares selected Architecture/Reuse, State/Data/Contracts, Component/Layout/Design System, Accessibility, Performance, or Desktop profiles and marks others Out of scope | implies every frontend dimension was reviewed |
| Framework profile | identifies React, Vue Composition, Vue Options, or repository-native concepts before framework rules | applies React semantics to Vue or assumes framework behavior |
| Styling profile | identifies only Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, or local systems present in scope | applies Tailwind or another styling checklist without evidence or implies every styling system was audited |
| Priority | resolves conflicts using the declared order | overrides local conventions with reference choices |
| Reuse | classifies candidates and justifies creation | creates parallel systems before search |
| Ownership | assigns route/page, feature, primitive, hook/composable, service, store, schema, type, and adapter only where selected | uses vague global buckets or ceremonial wrappers |
| State/reactivity | under State/Data, separates state classes and verifies framework-native reactivity, lifetime, cleanup, cancellation, Router and component contracts | duplicates truth, loses reactivity, cross-applies API styles, or leaves stale work |
| Vue API-style fidelity | audits Composition with refs/watchers/scopes and Options with data/computed/watch/this.$watch and native lifecycle/guards without forced conversion | requires Composition imports in Options code or mechanically translates APIs |
| Layout/design system | under Component/Layout, uses tokens, one spacing/scroll owner, minimal DOM/CSS, and centralized breakpoints | margin patches, duplicate CSS, or parallel styling system |
| Performance | under Performance, traces and measures render/reactivity/data/request/bundle/IPC paths | default memoization/computed/cache advice or file-size claims |
| Accessibility | under Accessibility, verifies keyboard, focus, labels, non-color and async status with runtime evidence or gaps | visual-only approval or unselected shallow checklist |
| Desktop | under Desktop, verifies adapter-command-domain and long-task lifecycle | direct page invokes, blocking work, leaked Rust internals, or browser-only proof |
| Lifecycle | under Architecture/Reuse, identifies route/export/generated/test/doc/index drift and complete remediation scope | structural code and docs disagree without a finding |
| Coordinator boundary | keeps Worktree and immutable basis ownership inside `repo-review` while the specialist remains path-bounded | lets specialist take over whole review, staging, or final cross-domain severity |
| Scope | preserves unrelated work and does not run excluded profiles | drive-by audit or cleanup |
| Validation | runs relevant real commands/runtime proof or reports Not verified | invented commands or unsupported pass claim |
| Read-only boundary | leaves code and Git/GitHub state unchanged, routes fixes to `implement-frontend`, and returns bounded findings to the coordinating reviewer | edits, stages, commits, comments, claims readiness, or expands scope |

## Scoring

Minimum pass: score each quality case 0–10. Pass only when trigger/non-trigger routing is correct and every quality case scores at least 8.
