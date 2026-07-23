# Product Specification Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Define the users, flows, permission rules, failure behavior, and acceptance for this cross-stack feature before implementation.` | Trigger Feature Spec. |
| `We are launching a new product line; define its boundary, users, journeys, MVP, non-goals, and first ready slice.` | Trigger Foundation Spec. |
| `Update only our existing PRODUCT.md with these confirmed product decisions.` | Trigger Artifact Update after authorization and path verification. |
| `Clarify the one unresolved decision that changes subscription cancellation behavior, then produce the smallest feature spec.` | Trigger internal clarification within Feature Spec. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `The behavior is approved; split implementation into tasks, owners, dependencies, and validation commands.` | Use host planning, not `product-spec`. |
| `Implement the approved React form and tests now.` | Prefer `dev-frontend`. |
| `Implement the approved Rust change and tests now.` | Prefer `dev-rust`. |
| `Resolve conflicting shared business language and rules across three product areas, including lifecycle or context depth only where material.` | Prefer `domain-modeling`. |
| `Create the selected-source UI contract, shared tokens, component semantics, variants, and evaluation rules.` | Prefer `ui-spec`. |
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
| New module inside an existing product | Use Feature Spec unless the product boundary is being redefined. | Uses Foundation merely because work is large. |
| Existing Foundation Spec is Ready and source exposes one bounded completion gap | Preserve the foundation and produce one Feature Spec for that gap when downstream implementation was requested. | Rewrites product positioning, invents a roadmap, or treats current code as authority for an unresolved product choice. |
| Existing positioning is consistently split across a README, product map, and policy manifest | Use the smallest verified source set as Feature Spec evidence. | Creates a new Foundation Spec only to consolidate documents or ignores a conflicting authority. |
| Repository already has an RFC convention | Use the RFC location and shape. | Creates `docs/product` in parallel. |
| No spec convention exists | Preview one fallback only after explicit write authorization. | Creates a tree, glossary, ADR, and handoff automatically. |
| Discoverable answer exists in source/docs | Read it before asking. | Interviews the user about current repository facts. |
| Missing decision affects only an internal naming choice | Mark Assumption or Deferred and declare Ready for the slice. | Blocks implementation ceremony without behavioral impact. |
| Missing decision changes permission or error behavior | Keep the slice not ready and ask one decision question. | Lets implementation invent the behavior. |
| Feature spans several bounded contexts | Route the shared language/lifecycle/invariants to `domain-modeling`. | Builds a complete domain model inside the spec. |
| Feature changes shared component semantics/tokens | Route the shared contract to `ui-spec`; keep product behavior in the product spec. | Duplicates a design system. |
| Request asks for current implementation-interface facts | Route that mapping separately to `repo-map`; keep the product spec behavioral. | Adds technical interface definitions to the product spec. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Mode selection | Exposes only Feature Spec, Foundation Spec, and Artifact Update. | Publishes Discovery, grill, Brief, or Standard modes. |
| Clarification | Searches repository facts, asks one material question with recommendation and trade-offs, and stops at the Ready gate. | Runs an open-ended interview or starts implementation. |
| Progressive scope | Produces one main document and includes only applicable detail. | Requires every UI/data/domain section or splits by default. |
| Ready gate | Names `Ready for <implementation slice>` and blocks only decision-changing ambiguity. | Uses one global Ready verdict or blocks on harmless detail. |
| Evidence states | Separates Confirmed, Assumption, Open, Rejected, and Deferred. | Hides assumptions as requirements. |
| Artifact authority | Uses existing convention and writes only explicitly authorized product facts. | Overwrites or invents an authority. |
| Conditional artifacts | Creates glossary, ADR, UI evidence, or handoff only when separately justified. | Treats them as minimum output. |
| Local handoff visibility | Writes an unfinished local continuation to a verified ignored `.codex/handoffs/<task-id>.md`; uses a repository-approved docs location only for explicitly requested team-shared continuation. | Tracks a local-private handoff, silently edits ignore policy, or treats a handoff as durable product authority. |
| Domain boundary | Keeps slice-local rules and routes deep shared modeling. | Absorbs `domain-modeling`. |
| UI contract boundary | Keeps product behavior and routes selected-source/shared visual-system specification ownership. | Absorbs `ui-spec`. |
| Planning boundary | Leaves technical decomposition to host planning when product behavior is decided. | Captures every planning request. |
| Implementation boundary | Stops before source and Git mutation. | Edits code, stages, commits, or runs implementation. |
| Interface boundary | Contains no technical interface definitions or references and routes current topology mapping to `repo-map`. | Defines or references a technical interface. |
| Verification honesty | Marks behavior/workflow/live gates `Not verified` without direct evidence. | Treats static validation as live proof. |
| Output | Reports evidence, decisions, slice, artifact, readiness, blockers, handoffs, validation, and gaps. | Omits material open decisions or claims runtime success. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger
expectations are correct, no authority violation occurs, and every quality case
scores at least 8.
