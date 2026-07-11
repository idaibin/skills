# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Audit a TanStack Router Console feature for shadcn reuse, ownership, and query-state boundaries.` | Trigger `audit-frontend`. |
| `Audit a Vue 3 feature for reactivity loss, watcher loops, composable lifetime, Pinia ownership, and Router contracts.` | Trigger `audit-frontend`. |
| `Under code-review, perform a read-only specialist audit of only the changed Vue SFCs for reactivity, lifecycle, accessibility, and performance.` | Trigger `audit-frontend` as a scoped specialist; keep `code-review` as the read-only Git-change review owner. |
| `Audit the Tauri frontend/Rust boundary for progress, cancellation, errors, menus, and shortcuts.` | Trigger `audit-frontend`. |
| `Check this frontend architecture for duplicated components, stores, services, spacing, and stale docs.` | Trigger `audit-frontend`. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Change one known component's copy and keep everything else unchanged.` | Prefer `implement-frontend`. |
| `Find the unknown cause of this failing frontend test.` | Prefer `diagnose`. |
| `Operate the real Tauri window and capture evidence.` | Prefer `ops-client`. |
| `Review the whole dirty tree and prepare commits.` | Prefer `code-review`. |
| `Own the current frontend diff, classify dirty files, stage it, and decide commit readiness.` | Use `code-review` for read-only classification, staging plan, and readiness, then `code-delivery` for authorized staging; do not route either ownership to `audit-frontend`. |

## Scenario Eval

Each scenario must produce the listed investigation, decision, rejection, and report evidence.

| # | Input scenario | Investigate | Correct decision | Reject | Final report |
| --- | --- | --- | --- | --- | --- |
| 1 | Pages each implement Button, Dialog, Table, and spacing | imports, primitives, variants, tokens, interaction/accessibility differences | identify reuse or composition candidates and stable variants | copy-and-restyle or forced merger of unrelated workflows | candidates, recommended owner, duplicates, validation gaps |
| 2 | New feature directory is unclear | router, adjacent features, aliases, docs, exports, business owner | follow nearest ownership pattern; justify every new layer | new `common/shared` tree for neatness | ownership map, new-file reasons, lifecycle updates |
| 3 | Component is large but splitting adds navigation | responsibilities, change reasons, state/data/layout coupling, tests | keep cohesive or split only at a stable ownership seam | line-count-based extraction | evidence for keeping/splitting and residual complexity |
| 4 | Global store holds local dialog state | consumers, persistence, route/window lifetime, existing local pattern | move local unless durable cross-tree behavior is proven | globalize to avoid props | state class, owner, affected consumers/tests |
| 5 | TanStack route file contains business logic | params/search/loader contract, services, feature workflows, test seams | keep route composition/guards; move stable workflow to owner | empty wrapper layers or router contract changes | route contract preserved, moved owner, generated checks |
| 6 | Vue Composition API component destructures reactive/Pinia state and uses broad watchEffect for API calls | SFC/API style; ref/reactive/computed and storeToRefs boundaries; synchronous watchEffect dependencies; invalidation; Router and keep-alive lifetime; request cancellation | preserve reactivity with local convention; use computed for derivation; keep automatic dependencies intentional and cancel stale work | React effect rules, mechanical `toRefs`, hidden global composable state, watcher-driven request loops, or assuming post-await reads are dependencies | exact reactivity break, dependency window, lifetime owner, request/cancel evidence, recommended fix owner |
| 7 | UI, API helper, and Rust validate a form differently | schemas, transport DTO, authoritative backend constraints, error mapping | align on authoritative contract; share/generate when supported | three drifting rule copies or client-only authority | schema owners, compatibility, field/general error tests |
| 8 | Tauri page invokes Rust on every keypress | call frequency, payload, latency, cache/batch/stream options | debounce/batch/cache or move/subscribe through adapter | direct high-frequency page invokes | before/after path, frequency evidence, native test gap |
| 9 | SQLite task freezes UI without progress | command sync/async, task identity, milestones, cancel path, cleanup | async domain task with real progress, cancellation, terminal states | fake timer progress or uncancellable blocking invoke | channel/events, cancel semantics, real-client verification |
| 10 | Similar pages use inconsistent spacing | shell/page/layout primitives, tokens, duplicated margins/breakpoints | assign one spacing/token owner and remove patches | new per-page magic values | owner, token/primitive reused, responsive visual proof |
| 11 | Agent wants unrelated refactor | request scope, dirty ownership, dependency necessity | exclude unrelated changes and note separately | opportunistic cleanup | exact scope and excluded files/ideas |
| 12 | Project convention conflicts with skill | user request, nearest guidance, existing code/docs, intent | follow rule priority and preserve local contract | enforce external reference or this skill | conflict, winning rule, preserved exception |
| 13 | Code and architecture docs disagree | current runtime/source, docs/indexes, ownership history | identify authoritative evidence and report synchronized remediation scope or blocker | change code only and leave stale docs | mismatches, authority, required files, validation |
| 14 | Vue feature has injected mutable state, temporary global guards, and cached routes | injection key/default/reactive and mutation owner; global/component guard registration/removal; activated/deactivated versus unmounted cleanup; duplicate listeners and stale requests | keep mutations with provider/store owner, unregister temporary guards, and align cleanup/cancellation with the real route/cache lifetime | untyped string injection, consumer-owned shared mutation, guard duplication, or unmount-only cleanup for keep-alive | provider/store/router owners, component contracts, teardown/cancellation evidence, runtime gap |
| 15 | `code-review` delegates changed frontend paths for domain review | delegated paths, read-only Git review owner, framework evidence, relevant diff context, unrelated dirty files | inspect only delegated paths and return read-only specialist findings/gaps to `code-review` | reclassify whole dirty tree, stage, commit, claim readiness, or expand scope | specialist mode, path boundary, domain findings, validations, untouched Git state |
| 16 | Pure Options API component uses `data`, `computed`, watch options, dynamic `this.$watch`, keep-alive, and component Router guards | local API convention; data/computed/watch ownership; unwatch handle; mounted/unmounted/activated/deactivated; beforeRouteUpdate/Leave; async cancellation | audit native Options semantics and retain the API style | require Composition helpers, treat watch options as Composition sources, or recommend incidental conversion | Options owners, dynamic cleanup, guard/request lifetime, runtime gap |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Grounding | reads guidance/status and inventories real framework, route, feature, primitives, data/state/reactivity, styles, tests, and docs | starts from a template |
| Framework profile | identifies React, Vue 3, or repository-native concepts before reviewing hooks/composables, state, routing, and render/reactivity behavior | applies React memo/hook guidance to Vue or assumes framework semantics |
| Priority | resolves conflicts using the declared order | overrides local conventions with reference-repo choices |
| Reuse | classifies candidates and justifies creation | creates parallel components/layers before search |
| Ownership | assigns page, feature, primitive, hook/composable, service, store, schema, and type responsibilities | uses vague global buckets or ceremonial wrappers |
| State/reactivity | separates state classes; for Vue Composition verifies ref/reactive/computed, explicit watch sources, bounded synchronous watchEffect dependencies, reactivity escapes, store/composable scope, and cleanup; for Options verifies data/computed/watch/this.$watch, native lifecycle and guards; for both checks component, injection, Router, keep-alive, and cancellation contracts | cross-applies API styles, duplicates sources of truth, loses reactivity, applies React effect rules, hides global state, duplicates guards/listeners, or leaves stale requests |
| Vue API-style fidelity | Audits Composition with its native refs/watchers/scopes and Options with data/computed/watch/this.$watch plus component lifecycle/guards, without cross-applying helper APIs. | Requires Composition imports in Options code, translates Options watchers mechanically, or converts API style without task evidence. |
| Layout | uses tokens, one spacing/scroll owner, minimal DOM/CSS, centralized breakpoints | margin patches, duplicate CSS, or forced styling system |
| Performance | traces and measures render/reactivity/data/bundle/IPC path | default memoization/computed changes or component-size claims |
| Accessibility | verifies keyboard, focus, labels, non-color and async status | visual-only approval |
| Desktop | uses adapter → command → Rust domain and long-task lifecycle | direct page invokes, blocking work, leaked Rust internals |
| Lifecycle | identifies drift across routes/exports/generated files/tests/docs/indexes and the complete remediation scope | structural code and docs disagree without a finding |
| Scope | preserves unrelated dirty work | performs drive-by cleanup |
| Validation | runs real project commands and runtime proof or reports `Not verified` | invented commands or unsupported success claim |
| Read-only boundary | leaves code and Git state unchanged and routes requested fixes to `implement-frontend`; in specialist mode reports only delegated frontend paths while `code-review` retains dirty-tree review, staging-plan, and commit-readiness ownership and `code-delivery` owns all Git mutation | edits, stages, commits, claims a fix/readiness, or takes ownership of unrelated dirty files during the audit |

## Scoring

Minimum pass: score each quality case 0–10. Pass only when trigger/non-trigger routing is correct and every quality case scores at least 7.
