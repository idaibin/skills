# Eval Cases

Use these cases when changing `implement-frontend` triggers, stack guidance, layout-ownership rules, validation expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Fix this React page without changing the layout.` | Should trigger `implement-frontend`. | Targeted frontend implementation with layout constraint. |
| `Add this Vue 3 settings form using the existing script setup, Pinia, Router, and component patterns.` | Should trigger `implement-frontend`. | Vue-native implementation and state ownership. |
| `Fix this Vue SFC's watchEffect request loop, provide/inject ownership, temporary Router guard, and keep-alive cancellation without converting its Options API style.` | Should trigger `implement-frontend`. | Vue-native reactivity, component contracts, Router lifetime, and cleanup. |
| `Fix this pure Options API component using data, computed, watch, this.$watch, activated/deactivated, and beforeRouteLeave; do not add Composition imports.` | Should trigger the Vue Options API branch. | Native Options reactivity and lifecycle. |
| `Add this form to the existing AntD page using current patterns.` | Should trigger `implement-frontend`. | Component-system consistency. |
| `Build this admin table page using the existing filters, row actions, and empty/error states.` | Should trigger `implement-frontend`. | Admin UI implementation with existing patterns. |
| `This Vite page has messy imports and component organization; clean only what is needed.` | Should trigger `implement-frontend`. | Frontend organization without broad refactor. |
| `Simplify this component: too many nested divs and repeated CSS rules.` | Should trigger `implement-frontend`. | DOM and CSS simplification in frontend code. |
| `Clean up this page structure: shell, content container, animation wrapper, and page root are all fighting overflow.` | Should trigger `implement-frontend`. | Layout ownership and DOM boundary cleanup. |
| `Merge this animation wrapper into the semantic page root and keep one scroll owner.` | Should trigger `implement-frontend`. | Animation wrapper and scroll ownership cleanup. |
| `Move these split-pane widths out of JSX utilities into one layout class.` | Should trigger `implement-frontend`. | Business geometry ownership cleanup. |
| `Replace h-[22px] and w-[88px] with project scale utilities or named CSS owners.` | Should trigger `implement-frontend`. | Tailwind arbitrary pixel cleanup. |
| `Use the existing Tailwind style conventions; do not redesign the page.` | Should trigger `implement-frontend`. | Styling convention preservation. |
| `Fix this Tauri settings UI, but keep native commands behind IPC.` | Should trigger `implement-frontend`. | Desktop webview UI implementation. |
| `Align this React app to its documented route, component, store, script, and file-naming standard.` | Should trigger `implement-frontend`. | Explicit frontend structure alignment. |
| `Flatten these nested divs, use one flex owner for centering, and keep the children adaptive.` | Should trigger `implement-frontend`. | Minimal DOM and Flex ownership. |
| `Remove repeated CSS and stop the component from duplicating the page container padding.` | Should trigger `implement-frontend`. | CSS and outer-spacing ownership. |
| `Before creating this page, inspect existing routes and components and reuse the closest implementation.` | Should trigger `implement-frontend`. | Reuse-first page development. |
| `Use the nearest existing component as a reference and justify any new file.` | Should trigger `implement-frontend`. | Reference-first component development. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Plan the frontend rewrite across three apps before anyone edits code.` | Should prefer `code-planner`. | Future cross-scope planning. |
| `Find the root cause before changing any code.` | Should prefer `diagnose`. | Diagnosis before implementation. |
| `Review all dirty changes and propose commit groups.` | Should prefer `code-review`. | Dirty-tree review and staging plan. |
| `Audit this frontend architecture for duplicated components, state boundaries, accessibility, and performance.` | Should prefer `audit-frontend`. | Read-only domain audit. |
| `Verify this page in the browser and check console/network.` | Should prefer `ops-browser`. | Runtime browser evidence. |
| `Capture the real Electron app window with platform-specific window evidence.` | Should prefer `ops-client`. | Desktop-client evidence. |
| `These frontend changes are reviewed; stage, commit, and push them.` | Should prefer `code-delivery`. | Authorized Git mutation after review. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Stack detection | Reads manifests/config/imports and reports actual framework and stack before choosing libraries or conventions. | Assumes a library or framework pattern is available because the user named it. |
| Framework-native implementation | Preserves React hooks/effects or Vue SFC/API/composable/store/router conventions according to the detected project. | Applies React concepts to Vue, rewrites Vue API style incidentally, or imposes one framework pattern universally. |
| Vue SFC and API style | Preserves the repository's SFC layout and `<script setup>`, Composition API, or Options API choice for the touched component. | Converts API style incidentally or applies React hook/Context/effect rules to Vue. |
| Vue Options API | Uses `data`/`computed`/`watch` or owned `this.$watch`, native component/Router guards, and mounted/unmounted/activated/deactivated lifecycles without requiring Composition helpers. | Injects `ref`, `watchEffect`, `onScopeDispose`, or a `<script setup>` conversion into a valid pure Options component. |
| Vue API-native reactivity | For Composition, preserves `ref`/`reactive`/`computed`, handles reactivity escapes, gives `watch` an explicit source, and bounds `watchEffect` dependencies; for Options, preserves native `data`/`computed`/watch options or owned `this.$watch` without requiring Composition helpers. | Cross-applies the other API style, mirrors derivation through watchers, loses reactivity, or hides request loops, stale work, and post-`await` dependency assumptions. |
| Vue component and injection contracts | Preserves read-only props, explicit emits, `v-model` arguments/modifiers, slots, fallthrough behavior, and typed provide/inject keys, defaults, reactive ownership, and mutation authority. | Mutates props/injected state implicitly, changes payload/slot contracts, or creates an unowned injected singleton. |
| Vue store, Router, and lifetime | Keeps local state local, uses Pinia for established shared ownership, registers global/component guards at the correct owner, unregisters temporary guards, and cleans watchers/listeners/requests for scope, route, and keep-alive activation lifetimes. | Globalizes component state, duplicates guard/listener registration, relies on unmount for keep-alive cleanup, or lets stale requests win after navigation/deactivation. |
| Project-class alignment | Preserves framework-native routing and applies repository-defined toolchain, script, directory, and naming rules without incidental upgrades. | Forces one SPA layout across Next.js, Astro, Vue, Tauri, and other project classes. |
| Reuse and lifecycle | Reuses locally first and updates manifests, exports, routes, scripts, tests, CI/build/deploy paths, docs, indexes, and stale references for structural changes. | Extracts speculative shared packages or moves/deletes source paths without closing ownership records. |
| Layout preservation | Keeps layout, spacing, routes, copy, and visual system unchanged unless requested. | Redesigns or restyles adjacent UI. |
| Component consistency | Reuses existing components, wrappers, hooks/composables, services, stores, types, icons, aliases, and interaction helpers. | Introduces a parallel UI kit, helper layer, state layer, or icon library. |
| Existing implementation search | Consumes a current `code-context` inventory or performs targeted file/symbol search across relevant pages, routes, layouts, components, hooks/composables, services, stores, shared UI, tests, and exports. | Starts coding from a guessed path or creates a file before checking existing code. |
| Reuse decision | Classifies candidates as direct reuse, reference-only, unrelated, or `Not found`; prefers reuse, then adaptation, then justified creation. | Duplicates an existing component or ignores the nearest established pattern. |
| New-file placement | Explains why existing candidates are insufficient and follows the current directory, naming, props, state, styling, export, and test conventions. | Creates a parallel `shared`, `common`, `ui`, `components`, hook/composable, store, or service layer. |
| DOM minimality | Removes or avoids wrappers, fragments, components, and classes that do not provide layout, semantics, state, accessibility, animation ownership, or reuse value. | Adds nested wrappers only to pass class names or group a single child. |
| Layout path | Uses the shortest valid DOM path, prefers Flexbox for one-dimensional composition, and uses Grid only for genuine two-dimensional relationships. | Adds wrappers for simple alignment or uses multiple layout systems for one flow. |
| Alignment ownership | Applies horizontal/vertical alignment or centering at the owning parent without adding a centering-only child wrapper. | Repeats alignment across parent and child layers or centers content that should follow normal flow. |
| Adaptive children | Uses local grow/shrink/basis/wrapping/minimum-size conventions so children adapt to available space. | Hardcodes widths/heights or adds wrappers to compensate for missing flex constraints. |
| Layout ownership | Assigns shell chrome, content inset, page layout, panel bounds, and scroll/overflow to explicit owners without repeated competing rules. | Leaves multiple nested layers declaring the same height, padding, inset, width, or overflow behavior. |
| Outer-spacing ownership | Keeps page-edge margin/padding/inset at one shell, content, or page owner and limits reusable components to internal spacing. | Applies outer spacing in both the parent container and inner component. |
| Animation wrapper collapse | Merges page-transition wrappers into a semantic page root when the wrapper has no independent layout, state, accessibility, or reuse role. | Keeps an animation-only wrapper around an inner container that repeats page layout. |
| Scroll ownership | Keeps one main scroll region where practical and prevents headers, sidebars, inspectors, panels, and footers from competing for overflow control. | Uses broad overflow patches or nested scroll fixes to hide unclear ownership. |
| CSS minimality | Consolidates repeated declarations and relies on existing tokens, component props, cascade, and inheritance when safe. | Repeats CSS, restates defaults, or adds one-off overrides where existing styles work. |
| Tailwind scale discipline | Uses project scale utilities for routine sizing and spacing, and named owners for real product geometry. | Leaves routine sizes as arbitrary pixel utilities without justification. |
| Contract preservation | Traces and preserves route, query, payload, response, permission, loading, and error behavior. | Changes data contracts silently. |
| Desktop boundary | Keeps native access behind IPC/command helpers and routes real-window proof to `ops-client`. | Calls native APIs directly from generic UI or treats browser preview as desktop proof. |
| Validation integrity | Uses repository-defined non-mutating checks and explicit fix/write commands only when rewrites are in scope. | Runs a write-mode check as ordinary validation or hides source rewrites. |
| Validation | Runs matching project commands and uses `ops-browser` or `ops-client` for UI behavior evidence when needed, or marks gaps `Not verified`. | Claims UI correctness without checks or evidence. |
| Scope control | Changes only files and lines needed for the frontend request. | Performs unrelated cleanup or broad component reorganization. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
