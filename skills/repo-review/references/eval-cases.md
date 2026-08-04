# Eval Cases

## Contents

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Independent Review Outlet Eval](#independent-review-outlet-eval)
- [Scenario Eval](#scenario-eval)
- [Quality Eval](#quality-eval)
- [Scoring](#scoring)

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Review all local changes and split commits.` | Trigger Worktree `repo-review`. |
| `Review only this changed module for defects; inventory status but do not produce commit groups or staging guidance.` | Trigger Worktree findings-only. |
| `Review only this session's changes and prepare exact staging guidance.` | Trigger scoped Worktree mode after full dirty-tree inventory. |
| `Review this auth migration and public API deletion before commit.` | Trigger Worktree commit-readiness. |
| `Review the repository at this commit and return P0-P3 findings.` | Trigger Fixed-basis review after resolving the SHA. |
| `Independently review 23d30ccd..d1c5f0d8.` | Trigger Fixed-basis review after resolving immutable SHAs. |
| `Review PR 42 but do not post comments.` | Resolve the PR base/head SHAs, then trigger Fixed-basis review and keep GitHub state unchanged. |
| `Review this release candidate for migrations, CI, packaging, and rollback.` | Trigger Fixed-basis review with the conditional Release profile. |
| `Validate this multipart review package, then review it.` | Trigger Review-package basis only after integrity verification. |
| `Coordinate frontend, Java, and Rust review where relevant, including authorization risks.` | Trigger `repo-review`; use bounded language specialists only when their evidence is independently necessary. |
| `Review this auth diff for authorization bypasses and token exposure.` | Trigger `repo-review`; fix the change basis and assess the risks in the Standards axis. |
| `Review commit X against its parent across repository standards and requirements, including security risks.` | Trigger Fixed-basis `repo-review`; security remains one Standards axis of the broader review. |
| `Security-review commit X as a change set against its parent.` | Prefer the available host security diff-scan workflow; this is a security-only Git-backed review. |
| `Run a professional security diff scan for this fixed range.` | Prefer the available host security diff-scan workflow; do not collapse its scan phases into `repo-review`. |
| `Integrate this completed security-provider report into the broader review of the same fixed range.` | Trigger `repo-review`; verify report attribution, basis, native evidence, and proof gaps before mapping status or affecting the broader verdict. |
| `Review this branch against both repository standards and the originating specification.` | Trigger two-axis `repo-review`. |
| `Review this selected-source frontend change and verify whether its visual-complete claim is supported.` | Trigger `repo-review` with the conditional visual-completion profile and require the structured evidence plus cited runtime artifacts. |
| `Review this fixed range's OpenAPI authority, compatibility diff, generated client, backend conformance, consumer states, and clean CI.` | Trigger `repo-review` with protocol-contract profile. |
| `Review this REST change against its native route, DTO, client, consumers, and tests; no generated schema pipeline exists.` | Trigger ordinary `repo-review`; mark the OpenAPI profile `Not applicable`. |
| `Review this fixed diff for duplicated rules, unused declarations, and over-designed wrappers.` | Trigger `repo-review`; apply the shared quality gate with fixed-basis attribution and the applicable language profile. |
| `Review this fixed frontend visual diff against its product Feature Spec, selected-source UI Feature Spec, and root DESIGN.md.` | Trigger `repo-review` with the conditional frontend design-compliance subflow; use the map only for navigation and report authority/runtime gaps separately. |
| `Review this fixed UI diff that changes table-row transition timing, keyboard navigation feedback, and reduced-motion behavior.` | Trigger the existing frontend design-compliance subflow plus interaction/motion review; retain the fixed basis, evidence gates, and P0-P3 output. |
| `Review this fixed range that adds requirements, schema, implementation, tests, and a replacement route together.` | Trigger project grounding; treat same-basis artifacts as intent and require independent compatibility/migration evidence before readiness. |
| `Review this fixed range; after the final local verdict, apply my configured sanitized result-retention sync.` | Complete and freeze `repo-review` first, then hand only the terminal result to `ask-ai`; report receipt separately and never treat the retention provider as a reviewer. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Map the repository architecture and reusable contracts into docs/repo-map/README.md.` | Prefer `repo-map`. |
| `Find why this test fails.` | Do not trigger this Skill; use the host's built-in diagnosis under effective instructions. |
| `Audit this current Rust endpoint path for token leakage; there is no diff to review.` | Prefer `audit-rust`. |
| `Scan this current repository for vulnerabilities; there is no change basis.` | Prefer an available host security-scan capability; do not widen `repo-review` or recreate a scanner. |
| `Audit this frontend architecture for accessibility and performance without a review basis.` | Prefer `audit-frontend`. |
| `Audit this Java service for transaction and Spring Security risks without a review basis.` | Prefer `audit-java`. |
| `Audit this Rust service for concurrency and memory risks without a review basis.` | Prefer `audit-rust`. |
| `Find all duplicate and dead code currently in this React app; there is no change basis.` | Prefer `audit-frontend` with a bounded scope, not `repo-review`. |
| `Apply the accepted frontend findings.` | Prefer `dev-frontend`. |
| `Stage, commit, and push the reviewed files.` | Prefer `repo-delivery`. |
| `Split this future migration into tasks.` | Do not trigger this Skill; use the host's built-in planning. |
| `Send the review package to ChatGPT.` | Prefer `ask-ai`. |
| `Define the product behavior, permissions, user-visible errors, and acceptance before implementation.` | Prefer `product-spec`. |
| `Review this Markdown typo-only range; no executable contract changed.` | Keep runtime, schema, integration, and migration grounding `Not applicable`; do not inflate the review. |

## Independent Review Outlet Eval

| Prompt | Expected |
| --- | --- |
| `Review this fixed range locally, then explicitly prepare one independent ChatGPT architecture challenge against the same basis.` | Keep `repo-review` as owner and emit one lightweight `ask-ai` handoff. |
| `Review this fixed range locally; no external reviewer was requested.` | Emit no `ask-ai` handoff. |
| `Review this fixed range locally; there is no valid final-result-sync instruction.` | Emit no retention handoff; local review completion alone never authorizes an external send. |
| `The ChatGPT review request was submitted, but no attributed response arrived.` | Preserve the local findings and verdict; report the external review axis `Not verified` without creating or clearing a finding. |

## Scenario Eval

| Scenario | Correct decision | Reject if |
| --- | --- | --- |
| Small local helper diff | Use Worktree findings-only: inventory full status, then inspect the helper and necessary interface closure. | Skips status or performs commit-level classification of unrelated files. |
| User asks whether changes are ready to commit | Use Worktree commit-readiness and classify all changed files/mixed hunks before groups or staging guidance. | Emits broad staging or applies commit ceremony to findings-only review. |
| Local file contains unrelated hunks | Mark `mixed-hunk` and require hunk-level staging. | Recommends whole-file staging. |
| Current session is narrower than dirty tree | Review full ownership, then scope commit guidance to session-owned changes. | Ignores unrelated changes or includes them. |
| Branch names move during range review | Resolve base/head SHAs before findings. | Reviews moving names. |
| Current worktree differs from reviewed SHA | Treat worktree content as contamination. | Uses it to clear a finding. |
| Range touches React, Rust, docs, and CI | Delegate bounded specialist surfaces and consolidate root causes. | Runs every profile globally or concatenates reports. |
| Fixed diff changes authentication or tenant authorization | Inspect the reachable source, control, boundary, tests, and consumers in the ordinary Standards pass. | Skips the risk because no separate scanner was requested or available. |
| A scanner flags a dangerous API but attacker reachability and the trust boundary are incomplete | Record `suspected`, counterevidence, proof gaps, and the minimum next check; do not let P0-P3 severity imply confidence. | Calls the pattern a validated vulnerability or suppresses it without checking the cited path. |
| Static evidence proves source, missing control, sink, supported boundary, preconditions, and impact but no runtime check ran | Record `likely`, the static confidence basis, and the exact validation gap. | Calls it `validated` because the bug class is severe or the call chain looks complete. |
| A bounded test or realistic local interface reproduces the original security consequence | Record `validated` with the method, artifact/evidence, basis, and remaining limits. | Claims whole-system coverage or omits how the original path was exercised. |
| A patch exists and a new test passes, but the original vulnerable path was not replayed on the new basis | Do not record `fixed`; require the new fixed basis plus original-path replay and focused regression evidence. | Treats code presence, review approval, or a green unrelated test as fix validation. |
| Review package is incomplete | Stop package-based conclusions. | Treats partial evidence as complete. |
| Repo-map path is stale | Search from nearest existing ancestor at the basis and route map repair to `repo-map`. | Trusts the map or edits it. |
| Review request contains no Git mutation authorization | Keep files, Git, GitHub, and remotes unchanged. | Stages, commits, comments, or pushes. |
| Protocol generator writes files | Consume retained evidence or replay only in a disposable isolated copy and prove the reviewed worktree/index/hashes unchanged; otherwise mark regeneration `Not verified`. | Runs a write-mode generator in the reviewed checkout. |
| A validation command rewrites a tracked generated file after the candidate scope was fixed | Refresh full Worktree/index evidence, classify the new diff as candidate-owned, validation side effect, or unrelated contamination, and do not clear commit readiness until the basis and intended scope agree. | Silently includes the generated drift, reviews the stale pre-validation basis, or discards user-owned content. |
| No actionable finding exists | Say `No actionable findings` and report residual gaps. | Invents low-value findings. |
| External review is still pending or returned no response | Keep the local verdict unchanged and report only the external completion gap. | Treats waiting as approval, blocks a locally complete verdict, or invents external findings. |
| Diff adds a wrapper around one implementation | Inspect current responsibility, consumers, policy, lifecycle, and verification seam. Report only if the new layer lacks a current role and creates concrete cost. | Calls every single-implementation abstraction over-design. |
| Clippy or ESLint reports an unused declaration outside the changed path | Classify it as pre-existing and exclude it from the verdict unless the basis directly depends on it; verify language/framework reachability. | Attributes whole-repository lint debt to the diff. |
| A one-line label change wraps at an intermediate width and hides a critical action | Attribute the reachable regression to the basis and require proportional runtime proof; distinguish it from unrelated pre-existing layout debt. | Dismisses the impact because the diff is small or reports all nearby layout debt as introduced. |
| A visual diff has root DESIGN.md but no trustworthy product or selected-source UI Feature Spec, or browser proof | Inspect available authorities and adapters, then report each missing authority and rendered-runtime evidence separately `Not verified`. | Treats DESIGN.md alone as feature acceptance, uses one Feature Spec for both owners, uses a repo-map row as proof, or requires an audit-frontend handoff by default. |
| A `.tsx` or `.css` diff changes only data typing or an unreachable comment | Skip interaction/motion review unless semantic and reachable motion, gesture, transition, or feedback behavior changed. | Activates a frontend-quality profile from extension or directory names. |
| A fixed basis introduces `transition: all` on a high-frequency control | Treat it as a candidate; prove attribution, reachable animated properties, frequency, concrete impact, authority, and required runtime evidence before assigning P0-P3. | Reports a style preference automatically, copies a default severity, or claims perceived behavior from source alone. |
| Frontend diff builds cleanly but has one screenshot and no computed checks or breakpoint captures | Reject visual completion, report the evidence gap against the basis, and keep static validation separate. | Treats build/lint or source CSS as visual proof. |
| Runtime grid values were copied into the spec before later design inspect-panel evidence contradicted them | Use the selected-source inspect values as the Spec target, runtime values as current evidence, and report the false alignment claim. | Lets current runtime define its own acceptance target. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Basis selection | Selects current Worktree/index, fixed immutable SHA/range, or verified review-package basis before reading conclusions; resolves PR to base/head and loads Release only as a conditional profile. | Treats a moving PR/release ref or Release profile as a standalone basis, or mixes basis evidence. |
| Immutable basis | Records full SHA or verified package manifest before conclusions. | Reviews a moving or ambiguous target. |
| Worktree inventory | Runs status, diff stat/name-status, and cached equivalents when needed. | Reviews only named files without full dirty-tree ownership. |
| Ownership and mixed hunks | In commit-readiness, classifies all ownership and requires safe hunk handling; findings-only preserves unrelated state without exhaustive commit grouping. | Uses whole-file staging for mixed content or forces commit grouping on a bounded findings request. |
| Evidence isolation | Keeps current-worktree content out of another SHA basis. | Clears immutable findings with local files. |
| Context collaboration | Uses repo maps only for navigation and verifies facts at the basis. | Trusts or edits the map. |
| Specialist composition | Delegates bounded frontend/Java/Rust paths when needed and retains final scope, integration, severity, and report ownership for the review basis. | Hands off the whole review or concatenates reports. |
| Standards axis | Checks applicable repository guidance, architecture, correctness, security, performance, and maintainability with cited evidence. | Treats generic preferences as hard repository violations. |
| Security evidence | Keeps `suspected`, `likely`, `validated`, and `fixed` separate from P0-P3; records source/control/sink/path/boundary, counterevidence, proof gaps, confidence, method, and basis; verifies provider output before integration. | Promotes a scanner match or dangerous API directly, treats static confidence as runtime validation, or calls a patch fixed without replay. |
| Evidence-gated code quality | For applicable duplication, dead/unused code, abstraction, and coupling signals, proves reachability, impact, owner/location, basis attribution, and a falsifiable verification path. | Reports similarity, size, a single wrapper/trait/memo/clone, or optional lint advice by itself. |
| Spec axis | Checks requirements, decisions, acceptance criteria, missing behavior, wrong behavior, and scope creep; marks the axis `Not verified` when no trustworthy spec exists. | Infers a spec from the diff or claims compliance without a source. |
| Frontend design compliance | Only for visual/UI-contract changes, separately traces product requirements/product Feature Spec, selected-source UI Feature Spec, root DESIGN.md, adapter/config, and runtime/browser evidence while keeping repo-map navigation-only. | Creates a parallel review gateway, requires audit-frontend, lets Feature Spec types substitute for each other, or collapses authority and runtime gaps into one claim. |
| Interaction and motion review | Activates only for semantic changes to motion, gesture, transition ownership, or user-visible feedback; applies purpose, frequency, existing-contract, accessibility, interruption, and performance candidates through the normal basis attribution, reachable-impact, evidence, and P0-P3 gates. | Activates by extension, creates a new profile, treats exact timing/easing or library preference as authority, flags `transition: all` without impact, or replaces missing runtime proof with opinion. |
| Visual-completion profile | Validates the handoff shape, inspects source/revision/approval, separate source/current/target rows, mapping, two same-viewport/state passes, computed checks, real assets/fallback, states and specified breakpoints before supporting completion. | Approves from current similarity, a single screenshot, static checks, or generic fallback assets. |
| Axis independence | Collects Standards and Spec evidence independently, optionally in bounded parallel read-only passes, then verifies, deduplicates, labels, and severity-ranks findings centrally. | Lets one axis mask the other or concatenates unverified subagent output. |
| External-review independence | Uses only attributed, captured, locally verified external output; a submitted, pending, timed-out, empty, or missing response remains a separate `Not verified` status and cannot change the local verdict. | Treats submission or elapsed time as reviewer approval/rejection, or lets a missing response create/clear a finding. |
| Necessary handoff | Emits a frontend/Java/Rust audit handoff only when that specialist must inspect a bounded part of the current review; otherwise keeps the optional profile internal and returns no handoff. | Lists specialists merely because a repository contains frontend, Java, Rust, or authentication code. |
| Contract completeness | Traces manifests, exports, callers, types, migrations, generated files, tests, CI/deploy, docs, indexes, and stale references when applicable. | Reviews isolated source lines only. |
| Protocol activation | Selects the generated-contract profile only for an existing pipeline or explicit gate; otherwise reviews native route/DTO/client/test ownership and reports `Not applicable`. | Requires OpenAPI because the change uses REST. |
| Protocol contract basis and gate | When active, fixes Git basis, authority and generator details, baseline/candidate artifacts, then requires applicable generation, compatibility, client, conformance, consumer, and CI evidence or marks gaps `Not verified`. | Reviews a moving basis, treats an edited generated artifact as authority, or accepts static checks as live proof. |
| Protocol review isolation | Replays write-mode OpenAPI/client generation only in a disposable isolated copy built from the fixed basis plus candidate changes, verifies the original worktree/index/hashes remain unchanged, and reports `Not verified` when isolation is unavailable. | Mutates the reviewed checkout or changes the review basis while collecting evidence. |
| Duplicate control | Consolidates symptoms sharing one root cause. | Repeats one issue across profiles. |
| Read-only boundary | Leaves files, Git, GitHub, and remote state unchanged and routes mutation to `repo-delivery`. | Edits, formats, stages, commits, pushes, comments, or changes refs. |
| Commit readiness | Only the requested Worktree commit-readiness profile produces semantic groups, exact staging, validation, risk, and commit messages. | Uses broad staging, auto-commits, or adds delivery output to findings-only review. |
| Severity evidence | Uses concrete impact, reachability, and urgency for P0-P3. | Uses style, file size, or hypotheticals. |
| Coverage honesty | States exclusions, failed checks, and `Not verified` gaps. | Claims whole-repository or release safety from partial evidence. |
| Output contract | Adapts output to Worktree versus immutable mode while preserving findings-first evidence. | Omits basis or mode-specific results. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
