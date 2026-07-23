# Repository Map Eval Cases

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Map the current project's directory structure and technical architecture into durable documentation.` | Trigger Repo Map mode. | Durable current-truth navigation is requested. |
| `Add the real startup, test, and build commands to the repo map.` | Trigger Targeted Update mode. | Command navigation update. |
| `List the shortest set of directories, components, and interfaces to read before developing this page.` | Trigger Reuse Inventory mode. | Shortest development path and reuse entries. |
| `Update the Rust APIs, DTOs, and call chain in the repo map.` | Trigger Targeted Update mode. | Bounded interface-map update. |
| `The documented directory and its parent are gone; ascend to the nearest existing ancestor and repair only the affected map entries.` | Trigger Navigation Repair mode. | Explicit incremental recovery. |
| `Create docs/repo-map/README.md from the repository's current truth.` | Trigger Repo Map mode. | Initial durable map. |
| `Map the shared components, functions, and APIs, then decide whether to reuse, extend, or wrap them before adding anything new.` | Trigger Reuse Inventory mode. | Duplicate-declaration prevention needs verified reuse entries. |
| `The current directory is not a Git repository; check for child Git repositories, or map it as an ordinary project if none exist.` | Trigger Repo Map mode. | Root classification must support multi-repo and non-Git directory projects. |
| `The path still exists, but its exports and route registration changed; repair only the affected repo-map entries.` | Trigger Navigation Repair mode. | Semantic staleness must be repaired even when paths resolve. |
| `Map the repository sources that define the Order domain, but do not decide its business vocabulary or lifecycle.` | Trigger `repo-map`; domain decisions remain with `domain-modeling`. | Repository evidence mapping only. |
| `Map PageHeader and MetricCard by design term, visual job, definition, export, owner root, consumers, variants, and current evidence.` | Trigger Reuse Inventory mode. | Durable design-to-component navigation is requested. |
| `Verify and record the single authority, OpenAPI generation command, generated client, real React consumer, and duplicate-DTO boundary for the Admin create-user operation.` | Trigger Targeted Update with the API Contract Map profile. | Durable current-source contract navigation is requested. |
| `Record this native REST operation's route, DTO, client, real consumer, and test entry point; the repository has no schema-generation pipeline.` | Trigger a bounded API Contract Map and record generated artifacts as `Not applicable`. | Native contract navigation is still valuable without OpenAPI. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Implement this login page now.` | Prefer `dev-frontend`. | No separate map deliverable. |
| `Implement this Rust API now.` | Prefer `dev-rust`. | No separate map deliverable. |
| `Review all local changes before commit.` | Prefer `repo-review`. | Dirty-tree readiness. |
| `Review main..feature for P0-P3 findings.` | Prefer `repo-review`. | Immutable range review. |
| `Find why the build fails.` | Do not trigger this Skill; use the host's built-in diagnosis under effective instructions. | Concrete failure. |
| `Split this migration into tasks.` | Do not trigger this Skill; use the host's built-in planning. | Future work planning. |
| `Define the entities, relationships, lifecycle, invariants, and bounded contexts for this product domain.` | Prefer `domain-modeling`. | Business model, not repository semantics. |
| `Review this endpoint diff for authorization risk.` | Prefer `repo-review`, routing professional security work to Codex Security when available. | Security-only change review. |
| `Turn these verified project notes into a technical article.` | Prefer `human-writing`. | Source-grounded writing, not repository mapping. |
| `Specify the user flows, permission rules, user-visible states, and acceptance for this new feature.` | Prefer `product-spec`. | Product behavior, not repository navigation. |
| `Regenerate OpenAPI and migrate the React caller to the generated client.` | Prefer the matching `dev-*` owner. | Source implementation, not a durable map deliverable. |
| `Review this feature range for dual authority, breaking API changes, and runtime gaps.` | Prefer `repo-review`. | Defect and readiness judgment against a fixed basis. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Current truth | Verifies paths, commands, architecture, and conventions from current repository evidence. | Copies stale prose or invents missing layers. |
| Directory map | Documents ownership and boundaries with exact paths, not an exhaustive tree. | Dumps every file without explaining ownership. |
| Shortest reading path | Gives the minimum ordered files/areas needed for common task types. | Produces a broad reading list with no order. |
| Reuse navigation | Names definitions, access/registration entries, representative callers, and new-contract gate. | Suggests new components or interfaces before searching. |
| Reuse inventory | Lists the relevant reusable and reference implementations with exact entry paths and ownership. | Scans unrelated code or omits the nearest reuse candidate. |
| Reuse evidence | Records canonical definition, actual access/registration visibility, representative consumers, boundary, and live evidence. | Treats a name or map row as proof without checking source. |
| Component-map shape | Records design/semantic name, visual job, canonical path, symbol, export/registration, owner/provider root, consumers, states/variants, reuse boundary, and current-source evidence. | Stores only a component name/path or generates an exhaustive catalog. |
| API Contract Map | Records the native authority, registration, DTO/envelope/auth owners, client/consumers, duplicate-DTO boundary, checks, and current evidence; generated artifacts are optional and schemas are not copied. | Requires OpenAPI, treats generated files as a second authority, inventories every endpoint, copies schemas, or claims live gates from paths alone. |
| Contract verification boundary | Separates durable current-source topology from Git-basis hashes/results, runtime/browser evidence, compatibility findings, and CI execution. | Stores transient trial status in the map or treats command existence as a passing result. |
| Conflicting reuse candidates | Ranks candidates by canonical ownership, active compatible consumers, validation, boundary fit, and deprecation; returns `Not verified` if authority remains ambiguous. | Selects the first name match, wraps an incompatible candidate, or declares `new` to avoid reconciling owners. |
| Duplicate prevention | Searches by capability, symbols, exports/routes, endpoint shapes, and callers, then records `reuse`, `extend`, `wrap`, or justified `new`. | Allows a parallel declaration because the map had no exact-name match. |
| Durable decision boundary | Reports task-local reuse decisions but persists only stable canonical owners, boundaries, or contracts in the map. | Stores one-off implementation choices as durable repository truth. |
| Map creation gate | Creates or expands a map only when it reduces routing, repeated discovery, duplication, or cross-boundary inference. | Documents facts obtainable from one listing or manifest. |
| Map granularity | Uses workspace, repository, and scoped levels based on real Git-root/ownership/build/deploy/runtime boundaries, including Git containers with independent nested repositories. | Mirrors directories or splits only because `src` and `src-tauri` both exist. |
| Root resolution | Uses the containing Git root when present; otherwise keeps the requested directory as map root, discovers child Git roots, or maps an ordinary non-Git directory project and records `local-unversioned`. | Assumes the current directory is a Git root, chooses an arbitrary child root as owner, or refuses to map because Git is absent. |
| Requested scope preservation | Keeps the requested subdirectory as initial working scope while recording its containing Git root, then selects repository or scoped map level from real ownership/build/deploy/runtime boundaries. | Automatically turns every subdirectory request into a repository-wide scan or invents a scoped map from directory shape alone. |
| Nested Git ownership | Records nested-root containment, assigns files to the deepest Git root by default, and overrides that default only with manifest/contract evidence. | Duplicates ownership between parent and nested repositories or silently treats a submodule as parent-owned source. |
| New-file gate | Names the closest existing implementation and explains why reuse or extension is insufficient before proposing a new path. | Creates a parallel component or interface without checking existing contracts. |
| Monorepo scope | Maps workspace and owning child/package boundaries, leaving unrelated areas unchecked. | Scans every package by default. |
| Cross-root duplicate prevention | Searches the owning root, first-order mapped provider/shared roots, and explicitly owned transitive contract roots, then stops at external or exhausted owner edges. | Approves `new` while an applicable provider root is unchecked, unavailable, or ambiguously owned, or scans unrelated dependency graphs. |
| Internal shared access | Records actual access or registration visibility, including module-private, framework-registered, generated, Rust `pub(crate)`, or Java package/module entries without widening visibility. | Omits a valid shared contract or makes it public solely to satisfy the map. |
| Incremental repair | Ascends to the nearest existing ancestor, scans only the relevant subtree, and patches the smallest stale unit. | Declares missing after one lookup or rescans/rebuilds everything. |
| Owner-root fallback | Ascends and searches only inside the recorded owner/provider root; if the root is absent, marks stale and performs ordinary bounded live discovery from current ownership. | Crosses the owner root or treats a stale root as authority. |
| History boundary | Uses Git history only to explain a move/rename already proved by current definition, registration, and consumers. | Uses a historical definition or consumer to claim current reuse. |
| Semantic repair | Detects still-resolving entries whose definition, access/registration, command, schema, owner, or runtime role changed and updates the smallest dependent consistency closure. | Treats a resolving path as current truth or patches one row while leaving derived routes and edges stale. |
| Consistency-closure bound | Updates the changed entry and directly dependent entries/declared edges, then stops when no changed dependency edge remains. | Rewrites unrelated sections or stops while a declared dependent remains stale. |
| Preservation | Keeps verified sections unchanged during a targeted refresh. | Rewrites the whole map for one stale path. |
| Dirty target preservation | Inspects staged and unstaged target diffs, preserves unrelated hunks, and stops on unsafe overlap. | Overwrites, normalizes, or reverts unrelated map edits. |
| Rebuild gate | Rebuilds only when the document is missing, corrupt, unusable, or explicitly requested. | Treats any revision or path change as a rebuild trigger. |
| Creation and migration | Selects one authoritative root index, links scoped sibling pages, records legacy migration, preserves `local-unversioned` state, and stops when competing candidates cannot be reconciled. | Creates duplicate maps, silently overwrites a candidate, or changes storage root for a scoped request. |
| Context-versus-review boundary | Records navigational truth without P0-P3 findings and routes both Worktree and immutable review to `repo-review`. | Acts as a universal review skill merely because it reads repository files. |
| Scope and stop condition | Reads only evidence needed for the map section and stops when later work has an accurate shortest route. | Uses file count as quality or keeps scanning unrelated areas. |
| Minimum evidence chain | Uses the minimum decisive chain, normally 1-8 unique entries per selected task, permits one entry, reuses shared entries, and records why a task needs more than eight. | Pads to three entries, applies one global count to the artifact, or truncates a required boundary chain at eight. |
| Output contract | Reports document path, map/Git roots, persistence, changed sections, shortest paths, reuse entries, repairs, validation, and gaps. | Repeats the entire document in chat or hides unchecked areas. |
| Partial execution report | Reports stop reason, completed evidence chain, unresolved boundary, artifact state, and follow-up when dirty overlap, missing providers, or ownership ambiguity prevents completion. | Claims success, hides partial writes, or omits the next action after stopping. |
| Publish readiness | Updates metadata/references and passes repository validation. | Leaves routing or eval artifacts stale. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
