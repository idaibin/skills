# Product Specification Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Define the users, flows, permission rules, failure behavior, and acceptance for this cross-stack feature before implementation.` | Trigger Feature Spec. |
| `We are launching a new product line; define its boundary, users, journeys, MVP, non-goals, and first ready slice.` | Trigger Foundation Spec. |
| `Update only our existing PRODUCT.md with these confirmed product decisions.` | Trigger Artifact Update after authorization and path verification. |
| `Clarify the one unresolved decision that changes subscription cancellation behavior, then produce the smallest feature spec.` | Trigger internal clarification within Feature Spec. |
| `Stress-test the permission, recovery, and acceptance decisions for this product slice before writing its spec.` | Trigger the internal decision pressure test, resolve the load-bearing frontier one question at a time, then synthesize only the selected slice. |
| `Use this fixed Axure version and its complete browser evidence to write implementation-ready product slices.` | Trigger Feature Spec composition after consuming the Axure coverage ledger; keep prototype coverage, product decisions, and UI-spec ownership distinct. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `The behavior is approved; split implementation into tasks, owners, dependencies, and validation commands.` | Use host planning, not `product-spec`. |
| `Implement the approved React form and tests now.` | Prefer `dev-frontend`. |
| `Implement the approved Rust change and tests now.` | Prefer `dev-rust`. |
| `Resolve conflicting shared business language and rules across three product areas, including lifecycle or context depth only where material.` | Prefer `domain-modeling`. |
| `Create a selected-source Feature Spec at docs/ui/<slice-id>/spec.md that references the root DESIGN.md.` | Prefer `ui-spec`. |
| `Map existing components, owners, exports, consumers, and reuse boundaries.` | Prefer `repo-map`. |
| `Map the current implementation interface, owner, callers, and consumers.` | Prefer `repo-map`; repository topology is outside `product-spec`. |
| `Review this feature branch against the approved spec.` | Prefer `repo-review`. |
| `Write a two-sentence acceptance check for this already-decided toggle.` | Use host planning; do not force a product artifact. |

## Independent Review Outlet Eval

| Prompt | Expected |
| --- | --- |
| `Finish the product spec, then prepare the explicitly requested independent ChatGPT product challenge against its fixed facts.` | Keep `product-spec` as owner and emit one lightweight `ask-chatgpt` handoff. |
| `Finish the product spec from local evidence only; no external review was requested.` | Emit no `ask-chatgpt` handoff. |

## Scenario Eval

| Scenario | Correct decision | Reject if |
| --- | --- | --- |
| One feature affects several product surfaces | Use one Feature Spec and include only relevant user-visible states and dependencies. | Exposes Brief/Standard as modes or splits files by default. |
| One connected feature uses several pages | Keep one Feature Spec when the pages share one job, behavior, and acceptance boundary. | Splits mechanically by page or treats every surface as an independent feature. |
| Home, tasks, contacts, and profile are requested together | Produce one short product index plus independently readable Feature Specs for confirmed slices. | Merges independent behavior into one omnibus Feature Spec. |
| Some requested features are confirmed and others remain open | Author confirmed slice facts and give each its own Ready verdict; keep open slices and blockers in the index. | Lets one open feature block all slices or invents unconfirmed behavior. |
| UI direction already exists | Link the applicable UI contract and keep only behavior, user-visible meaning, and acceptance. | Repeats colors, typography, components, tokens, or page geometry. |
| Axure pages, requirements, and named flows are the product source | Consume `axure-product-evidence/v1`, group evidence by user job, trace behavior to evidence IDs, and report prototype coverage separately from per-slice Ready. | Treats screenshots/page titles as complete, copies visual geometry into PRD, or hides inaccessible branches. |
| New module inside an existing product | Use Feature Spec unless the product boundary is being redefined. | Uses Foundation merely because work is large. |
| Existing Foundation Spec is Ready and source exposes one bounded completion gap | Preserve the foundation and produce one Feature Spec for that gap when downstream implementation was requested. | Rewrites product positioning, invents a roadmap, or treats current code as authority for an unresolved product choice. |
| Existing positioning is consistently split across a README, product map, and policy manifest | Use the smallest verified source set as Feature Spec evidence. | Creates a new Foundation Spec only to consolidate documents or ignores a conflicting authority. |
| Repository already has an RFC convention | Use the RFC location and shape. | Creates `docs/prd` in parallel. |
| No spec convention exists and one feature slice is authorized for durable publication | Preview `docs/prd/<slice-id>/spec.md`; do not create an index. | Adds `docs/specs/`, creates `docs/prd/index.md` for one slice, or creates a glossary, ADR, and handoff automatically. |
| No spec convention exists and several independent feature slices are authorized | Use `docs/prd/index.md` plus `docs/prd/<slice-id>/spec.md` for each confirmed slice. | Creates one omnibus PRD or adds a `docs/specs/` wrapper. |
| Related PRD and UI contracts exist for one slice | Use the same stable slice ID and cross-link `docs/prd/<slice-id>/spec.md` with `docs/ui/<slice-id>/spec.md` without duplicating authority. | Uses unrelated IDs or copies visual details into PRD. |
| Repository calls an approved RFC its product requirements authority | Preserve the RFC authority and do not create or require root `PRD.md`. | Classifies authority from filename alone or introduces a parallel PRD tree. |
| Discoverable answer exists in source/docs | Read it before asking. | Interviews the user about current repository facts. |
| A confirmed product fact changes one slice's user-visible result and data risk | Add one bounded two-column row linking the already classified/evidenced fact to that slice's observable acceptance consequence. | Duplicates decision state/evidence columns, builds an exhaustive fact inventory, defines a technical interface, or lets the fact silently change acceptance. |
| A confirmed product fact changes one slice's scope or acceptance but creates no data risk | Trace only the affected slice and observable acceptance consequence; omit any data-risk phrase rather than inventing one. | Adds a fictional risk, forces `N/A` ceremony, or omits the material acceptance impact. |
| Two material decisions remain and the second depends on the first | Ask the prerequisite decision first with a recommendation, trade-off, and affected slices; recompute the frontier after the answer. | Asks both questions together or guesses the dependent answer. |
| A vague request contains many conceivable branches but only permissions and recovery can change the selected slice | Pressure-test only permissions and recovery, then stop at the slice Ready gate. | Exhaustively interviews every preference or unrelated future branch. |
| The user stops before resolving a material decision for one of several slices | Preserve that decision as Open and keep only the affected slice not Ready; allow unrelated confirmed slices to proceed. | Invents confirmation, claims shared understanding, or blocks every slice. |
| The selected slice already passes its Ready gate | Synthesize without activating the pressure test. | Reopens settled product decisions without contradictory evidence. |
| Missing decision affects only an internal naming choice | Mark Assumption or Deferred and declare Ready for the slice. | Blocks implementation ceremony without behavioral impact. |
| Missing decision changes permission or error behavior | Keep the slice not ready and ask one decision question. | Lets implementation invent the behavior. |
| Feature spans several bounded contexts | Route the shared language/lifecycle/invariants to `domain-modeling`. | Builds a complete domain model inside the spec. |
| Feature changes shared component semantics/tokens | Route the root `DESIGN.md` update to `ui-spec`; keep product behavior in the product spec and add a Feature Spec only for affected implementation details. | Duplicates a design system. |
| Request asks for current implementation-interface facts | Route that mapping separately to `repo-map`; keep the product spec behavioral. | Adds technical interface definitions to the product spec. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Mode selection | Exposes only Feature Spec, Foundation Spec, and Artifact Update. | Publishes Discovery, grill, Brief, or Standard modes. |
| Decision pressure test | Activates only for material product choices, resolves facts first, asks the highest-impact frontier decision one at a time with recommendation/trade-off/affected slices, records the answer, and stops per slice at Ready. | Runs an exhaustive interview, asks dependent questions together, guesses decisions, or reopens a Ready slice. |
| Progressive scope | Produces one main document for one feature, or a short index plus slice documents for proven independent features. | Requires every UI/data/domain section, splits one cohesive feature by page, or merges independent features. |
| Ready gate | Names `Ready for <implementation slice>` for every slice and blocks only the affected slice on decision-changing ambiguity. | Uses one global Ready verdict, blocks unrelated slices, or blocks on harmless detail. |
| Consumer read contract | One slice requires only shared index facts and its target slice. | Requires every sibling Feature Spec to be loaded. |
| Documentation fallback | Uses repository convention first; otherwise writes directly under `docs/prd/`, adding its index only for multiple independent slices and never adding `docs/specs/`. | Creates a competing tree, an unnecessary index, or another wrapper layer. |
| Visual-detail boundary | Links UI contracts without duplicating colors, typography, components, tokens, or geometry. | Turns product facts into a visual specification. |
| Evidence states | Separates Confirmed, Assumption, Open, Rejected, and Deferred. | Hides assumptions as requirements. |
| Fact-to-acceptance trace | Adds the optional two-column trace only when a classified/evidenced fact materially affects scope, user outcome, data risk, or acceptance; links it to the affected slice and observable consequence. | Requires the table for every feature, duplicates the decision record, inventories harmless facts, or crosses into implementation/interface design. |
| Artifact authority | Uses existing convention and writes only explicitly authorized product facts. | Overwrites or invents an authority. |
| Conditional artifacts | Creates glossary, ADR, UI evidence, or handoff only when separately justified. | Treats them as minimum output. |
| Local handoff visibility | Writes an unfinished local continuation to a verified ignored `.codex/handoffs/<task-id>.md`; uses a repository-approved docs location only for explicitly requested team-shared continuation. | Tracks a local-private handoff, silently edits ignore policy, or treats a handoff as durable product authority. |
| Domain boundary | Keeps slice-local rules and routes deep shared modeling. | Absorbs `domain-modeling`. |
| UI contract boundary | Keeps product behavior and routes selected-source/shared visual-system specification ownership. | Absorbs `ui-spec`. |
| Planning boundary | Leaves technical decomposition to host planning when product behavior is decided. | Captures every planning request. |
| Implementation boundary | Stops before source and Git mutation. | Edits code, stages, commits, or runs implementation. |
| Interface boundary | Defines no technical interface; cites a verified existing interface fact only when the implementation handoff would otherwise be ambiguous, and routes current topology mapping to `repo-map`. | Designs a new interface, inventories implementation topology, or cites an interface without a handoff need. |
| Verification honesty | Marks behavior/workflow/live gates `Not verified` without direct evidence. | Treats static validation as live proof. |
| Prototype evidence coverage | Requires fixed source/revision, page and requirement ledgers, interaction evidence, conflicts, and coverage totals; blocks only affected slices when required evidence is missing. | Declares complete coverage with unknown hotspots, unvisited pages, static-only behavior, or missing required states. |
| Output | Reports evidence, decisions, slice, artifact, readiness, blockers, handoffs, validation, and gaps. | Omits material open decisions or claims runtime success. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger
expectations are correct, no authority violation occurs, and every quality case
scores at least 8.
