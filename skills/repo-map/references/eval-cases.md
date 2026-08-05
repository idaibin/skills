# Repository Map Eval Cases

## Contents

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Quality Eval](#quality-eval)
- [Scoring](#scoring)

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Map the current project's directory structure and technical architecture into durable documentation.` | Trigger Repo Map mode. | Durable current-truth navigation is requested. |
| `Add the real startup, test, and build commands to the repo map.` | Trigger Targeted Update mode. | Command navigation update. |
| `Create a durable repo-map entry with the shortest set of directories, components, and interfaces to read before developing this page.` | Trigger Reuse Inventory mode. | A persistent shortest-path and reuse index is requested. |
| `Update the Rust APIs, DTOs, and call chain in the repo map.` | Trigger Targeted Update mode. | Bounded interface-map update. |
| `The documented directory and its parent are gone; ascend to the nearest existing ancestor and repair only the affected map entries.` | Trigger Navigation Repair mode. | Explicit incremental recovery. |
| `Create docs/repo-map/README.md from the repository's current truth.` | Trigger Repo Map mode. | Initial durable map. |
| `Map the shared components, functions, and APIs, then decide whether to reuse, extend, or wrap them before adding anything new.` | Trigger Reuse Inventory mode. | Duplicate-declaration prevention needs verified reuse entries. |
| `The current directory is not a Git repository; check for child Git repositories, or map it as an ordinary project if none exist.` | Trigger Repo Map mode. | Root classification must support multi-repo and non-Git directory projects. |
| `The path still exists, but its exports and route registration changed; repair only the affected repo-map entries.` | Trigger Navigation Repair mode. | Semantic staleness must be repaired even when paths resolve. |
| `Map the repository sources that define the Order domain, but do not decide its business vocabulary or lifecycle.` | Trigger `repo-map`; domain decisions remain with `domain-modeling`. | Repository evidence mapping only. |
| `Map PageHeader and MetricCard by design term, visual job, definition, export, owner root, consumers, variants, and current evidence.` | Trigger Reuse Inventory mode. | Durable design-to-component navigation is requested. |
| `Create a frontend code-context index for this console's routes, components, hooks/state, API, styles, and DESIGN.md bindings.` | Trigger the optional Frontend Inventory profile. | A bounded durable navigation aid is explicitly requested. |
| `Verify and record the single authority, OpenAPI generation command, generated client, real React consumer, and duplicate-DTO boundary for the Admin create-user operation.` | Trigger Targeted Update with the API Contract Map profile. | Durable current-source contract navigation is requested. |
| `Record this native REST operation's route, DTO, client, real consumer, and test entry point; the repository has no schema-generation pipeline.` | Trigger a bounded API Contract Map and record generated artifacts as `Not applicable`. | Native contract navigation is still valuable without OpenAPI. |
| `Update the root map, but keep the existing verified UI component and token maps as the detailed authorities.` | Trigger Targeted Update with federated specialist-map routing. | The root should route to bounded authorities without copying them. |
| `Record where each product's positioning facts live in this monorepo, but do not rewrite or decide the positioning.` | Trigger Targeted Update for product-fact routing only. | The map should reach product authority without absorbing `product-spec`. |
| `Create a root AGENTS.md plus nearer guidance for the independently built web frontend and API backend; keep shared rules at the root.` | Trigger Project Guidance Baseline mode. | Explicit layered repository guidance is requested and the boundaries are evidence-checkable. |
| `This monorepo has apps/web, services/api, and packages/shared. Decide from manifests and commands which directories need their own AGENTS.md, then create only the justified files.` | Trigger Project Guidance Baseline mode. | Placement must follow real owner/build/runtime boundaries rather than directory names. |
| `Map this non-Git workspace containing independent Maven repositories; record each child Git/build root, JDK source, aggregator and executable modules, BOM ownership, and critical cross-repository SDK edges.` | Trigger Repo Map mode with the Java build and dependency profile. | The container/root and Maven module boundaries must remain distinct. |
| `Map this Gradle Java repository where each backend service has its own settings, Wrapper, build, and runtime configuration; do not dump every dependency.` | Trigger Repo Map mode with the Java build and dependency profile. | Independent build/runtime boundaries and bounded dependencies are requested. |
| `Map the stable owners and verification entry points for profiles, packaged resources, schema compatibility, gateway contracts, and cross-repo delivery; do not claim the target runtime was tested.` | Trigger Repo Map with project grounding for stable routing facts. | The request exceeds directory navigation but still forbids transient review/runtime verdicts. |
| `Use this open-source Java framework as a design and documentation reference, but generate the target repo map only from our current manifests, entry points, commands, and module dependencies.` | Trigger Targeted Update with the Java build and dependency profile. | The reference supplies comparison questions, while the target repository remains authoritative. |

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
| `Review this endpoint diff for authorization risk.` | Prefer `repo-review`. | Fixed-basis change review. |
| `Turn these verified project notes into a technical article.` | Prefer `human-writing`. | Source-grounded writing, not repository mapping. |
| `Specify the user flows, permission rules, user-visible states, and acceptance for this new feature.` | Prefer `product-spec`. | Product behavior, not repository navigation. |
| `Regenerate OpenAPI and migrate the React caller to the generated client.` | Prefer the matching `dev-*` owner. | Source implementation, not a durable map deliverable. |
| `Review this feature range for dual authority, breaking API changes, and runtime gaps.` | Prefer `repo-review`. | Defect and readiness judgment against a fixed basis. |
| `Implement changes in both the frontend and backend.` | Prefer the matching implementation owners; read existing guidance but do not create it implicitly. | Source work alone does not authorize new `AGENTS.md` files. |
| `Read the files needed for this feature, then implement it; do not create or update a repository map.` | Prefer the matching implementation owner and its bounded live discovery. | Task-local discovery is not a durable map deliverable. |
| `Upgrade this Maven project to a new JDK and replace its Spring dependencies.` | Prefer the matching implementation owner or host planning before source changes. | A build/runtime migration is implementation, not a durable map deliverable. |
| `List the top-level directories and owning manifests; do not map runtime, data, integration, compatibility, or delivery authorities.` | Keep project grounding inactive and return the bounded navigation answer. | Directory navigation alone does not activate execution-evidence work. |

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
| Frontend design binding | For a reusable UI row, records the exact map-root-relative `<design-root>/DESIGN.md` path plus anchor/semantic binding, adapter/config, implementation/export/consumer, states/variants, and source evidence. | Assumes the Git root, copies shared token values/rules, treats DESIGN.md as implementation proof, or makes the inventory mandatory. |
| API Contract Map | Records the native authority, registration, DTO/envelope/auth owners, client/consumers, duplicate-DTO boundary, checks, and current evidence; generated artifacts are optional and schemas are not copied. | Requires OpenAPI, treats generated files as a second authority, inventories every endpoint, copies schemas, or claims live gates from paths alone. |
| Owner and runtime identity | Records canonical/source owner, build/deploy owner, runtime service identity, and gateway/registration alias separately when they differ. | Uses a legacy service name to assign source ownership or calls aligned identities a conflict. |
| Structured map admission | Adds a sidecar only with a named owner, producer, consumer, version, validator, drift policy, and retirement rule. | Creates `map.yaml` or a schema merely for AI parsing. |
| Contract verification boundary | Separates durable current-source topology from Git-basis hashes/results, runtime/browser evidence, compatibility findings, and CI execution. | Stores transient trial status in the map or treats command existence as a passing result. |
| Conflicting reuse candidates | Ranks candidates by canonical ownership, active compatible consumers, validation, boundary fit, and deprecation; returns `Not verified` if authority remains ambiguous. | Selects the first name match, wraps an incompatible candidate, or declares `new` to avoid reconciling owners. |
| Duplicate prevention | Searches by capability, symbols, exports/routes, endpoint shapes, and callers, then records `reuse`, `extend`, `wrap`, or justified `new`. | Allows a parallel declaration because the map had no exact-name match. |
| Durable decision boundary | Reports task-local reuse decisions but persists only stable canonical owners, boundaries, or contracts in the map. | Stores one-off implementation choices as durable repository truth. |
| Map creation gate | Creates or expands a map only when it reduces routing, repeated discovery, duplication, or cross-boundary inference. | Documents facts obtainable from one listing or manifest. |
| Federated map authority | Keeps one root navigation index, links verified specialist maps, and records their bounded owner plus source revalidation path. | Copies specialist rows, tokens, schemas, or component inventories into the root map or creates a competing root. |
| Product-fact routing | Links the smallest verified vision, README, product map, or equivalent authority set only when it changes task routing. | Rewrites product positioning, treats code as product approval, or creates a new product authority. |
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
| Full rebuild closure | When explicitly requested, reconciles root and specialist indexes, links, owners, consumers, deletions, and untracked artifacts as one current-state closure. | Preserves task history in the map, leaves stale links, or stops after renaming folders. |
| Creation and migration | Selects one authoritative root index, links scoped sibling pages, records legacy migration, preserves `local-unversioned` state, and stops when competing candidates cannot be reconciled. | Creates duplicate maps, silently overwrites a candidate, or changes storage root for a scoped request. |
| Context-versus-review boundary | Records navigational truth without P0-P3 findings and routes both Worktree and immutable review to `repo-review`. | Acts as a universal review skill merely because it reads repository files. |
| Scope and stop condition | Reads only evidence needed for the map section and stops when later work has an accurate shortest route. | Uses file count as quality or keeps scanning unrelated areas. |
| Minimum evidence chain | Uses the minimum decisive chain, normally 1-8 unique entries per selected task, permits one entry, reuses shared entries, and records why a task needs more than eight. | Pads to three entries, applies one global count to the artifact, or truncates a required boundary chain at eight. |
| Output contract | Reports document path, map/Git roots, persistence, changed sections, shortest paths, reuse entries, repairs, validation, and gaps. | Repeats the entire document in chat or hides unchecked areas. |
| Partial execution report | Reports stop reason, completed evidence chain, unresolved boundary, artifact state, and follow-up when dirty overlap, missing providers, or ownership ambiguity prevents completion. | Claims success, hides partial writes, or omits the next action after stopping. |
| Publish readiness | Updates metadata/references and passes repository validation. | Leaves routing or eval artifacts stale. |
| Layered guidance placement | Keeps shared routing and safety at the root, creates nearer `AGENTS.md` only for proven independent Git/ownership/build/runtime/command boundaries, and records skipped candidates. | Copies the root file into every directory, treats names such as frontend/backend as proof, or omits a justified child boundary. |
| Guidance precedence | Re-reads one representative task through the root-to-leaf chain and keeps child files to local deltas without contradiction. | Duplicates or contradicts parent rules, or leaves the effective command/root ambiguous. |
| Java build-root recognition | Resolves Maven parent/aggregator/module roots or Gradle settings/included-build roots from manifests and Wrapper evidence while preserving child Git ownership. | Chooses a root from `src/main/java`, directory names, or the first manifest found. |
| Java runtime evidence | Records JDK and build-tool requirements from compiler/toolchain, Wrapper, CI/image, or version-manager sources and preserves conflicts as `Not verified`. | Infers the JDK from framework convention, the local machine, or stale prose. |
| Java dependency topology | Records declared internal edges, BOM/platform/version authority, executable/library roles, and only routing-relevant external dependencies with manifest evidence. | Copies a full dependency tree/effective model, treats declaration as successful resolution/runtime use, or omits the dependency owner. |
| Java configuration hygiene | Records configuration and profile ownership without copying values and keeps remote/deployed configuration `Not verified` without direct evidence. | Persists credentials, endpoints, connection strings, tokens, or inferred active profiles. |
| Project-grounding boundary | Persists stable authorities, contract edges, and verification entry points while leaving task basis, freshness, operational status, and verdicts to the consumer. | Calls the map complete project/runtime proof or stores a transient environment dump. |
| External architecture reference | Extracts useful documentation and architecture questions from the reference, verifies adopted facts against target manifests/source, and keeps unadopted patterns separate from current truth. | Creates a framework-specific branch, labels the target from similarity, or copies the reference layout, commands, dependencies, and conventions as target facts. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
