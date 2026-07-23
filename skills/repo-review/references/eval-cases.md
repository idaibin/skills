# Eval Cases

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
| `Coordinate frontend, Rust, and professional security review where relevant.` | Trigger `repo-review`; use bounded frontend/Rust specialists and route security evidence to Codex Security when available. |
| `Review this auth diff and run the professional security checks that apply.` | Trigger `repo-review`; fix the change basis and route security work to `codex-security:security-diff-scan` when available. |
| `Security-review commit X as a change set against its parent.` | Trigger Fixed-basis `repo-review` and route the explicit commit diff to `codex-security:security-diff-scan`. |
| `Security-scan the complete repository snapshot at commit X.` | Trigger Fixed-snapshot `repo-review`; safely materialize the full tree and route it to `codex-security:security-scan`, or mark snapshot security coverage `Not verified`. |
| `Review this branch against both repository standards and the originating specification.` | Trigger two-axis `repo-review`. |
| `Review this fixed range's OpenAPI authority, compatibility diff, generated client, backend conformance, consumer states, and clean CI.` | Trigger `repo-review` with protocol-contract profile. |
| `Review this REST change against its native route, DTO, client, consumers, and tests; no generated schema pipeline exists.` | Trigger ordinary `repo-review`; mark the OpenAPI profile `Not applicable`. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Map the repository architecture and reusable contracts into docs/repo-map/README.md.` | Prefer `repo-map`. |
| `Find why this test fails.` | Do not trigger this Skill; use the host's built-in diagnosis under effective instructions. |
| `Scan this current-source endpoint path for token leakage; there is no diff to review.` | Prefer `codex-security:security-scan`. |
| `Audit this frontend architecture for accessibility and performance without a review basis.` | Prefer `audit-frontend`. |
| `Audit this Rust service for concurrency and memory risks without a review basis.` | Prefer `audit-rust`. |
| `Apply the accepted frontend findings.` | Prefer `dev-frontend`. |
| `Stage, commit, and push the reviewed files.` | Prefer `repo-delivery`. |
| `Split this future migration into tasks.` | Do not trigger this Skill; use the host's built-in planning. |
| `Send the review package to ChatGPT.` | Prefer `ask-chatgpt`. |
| `Define the product behavior, permissions, user-visible errors, and acceptance before implementation.` | Prefer `product-spec`. |

## Independent Review Outlet Eval

| Prompt | Expected |
| --- | --- |
| `Review this fixed range locally, then explicitly prepare one independent ChatGPT architecture challenge against the same basis.` | Keep `repo-review` as owner and emit one lightweight `ask-chatgpt` handoff. |
| `Review this fixed range locally; no external reviewer was requested.` | Emit no `ask-chatgpt` handoff. |

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
| Fixed diff changes authentication or tenant authorization | Route professional security evidence to `codex-security:security-diff-scan`, then verify basis and consolidate findings in `repo-review`. | Reimplements a generic scanner, silently skips security, or treats plugin output as automatically valid. |
| Fixed commit request means complete snapshot | Materialize the exact full tree read-only and use `codex-security:security-scan`; preserve the original checkout. | Scans only the commit diff or mutates the reviewed checkout. |
| Required Codex Security workflow is unavailable | Continue only the requested ordinary review and mark the named security scope `Not verified`. | Claims equivalent internal coverage or blocks unrelated review evidence. |
| Direct repository/path scan and Codex Security is unavailable | Name `codex-security:security-scan`, mark the requested path `Not verified`, and stop that scan. | Routes to a deleted local Skill or silently performs an internal approximation. |
| Review package is incomplete | Stop package-based conclusions. | Treats partial evidence as complete. |
| Repo-map path is stale | Search from nearest existing ancestor at the basis and route map repair to `repo-map`. | Trusts the map or edits it. |
| Review request contains no Git mutation authorization | Keep files, Git, GitHub, and remotes unchanged. | Stages, commits, comments, or pushes. |
| Protocol generator writes files | Consume retained evidence or replay only in a disposable isolated copy and prove the reviewed worktree/index/hashes unchanged; otherwise mark regeneration `Not verified`. | Runs a write-mode generator in the reviewed checkout. |
| No actionable finding exists | Say `No actionable findings` and report residual gaps. | Invents low-value findings. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Basis selection | Selects current Worktree/index, fixed immutable SHA/range, or verified review-package basis before reading conclusions; resolves PR to base/head and loads Release only as a conditional profile. | Treats a moving PR/release ref or Release profile as a standalone basis, or mixes basis evidence. |
| Immutable basis | Records full SHA or verified package manifest before conclusions. | Reviews a moving or ambiguous target. |
| Worktree inventory | Runs status, diff stat/name-status, and cached equivalents when needed. | Reviews only named files without full dirty-tree ownership. |
| Ownership and mixed hunks | In commit-readiness, classifies all ownership and requires safe hunk handling; findings-only preserves unrelated state without exhaustive commit grouping. | Uses whole-file staging for mixed content or forces commit grouping on a bounded findings request. |
| Evidence isolation | Keeps current-worktree content out of another SHA basis. | Clears immutable findings with local files. |
| Context collaboration | Uses repo maps only for navigation and verifies facts at the basis. | Trusts or edits the map. |
| Specialist composition | Delegates bounded frontend/Rust paths when needed, routes professional security work to Codex Security, and retains final scope, integration, severity, and report ownership for the review basis. | Hands off the whole review, recreates a security scanner, or concatenates reports. |
| Standards axis | Checks applicable repository guidance, architecture, correctness, security, performance, and maintainability with cited evidence. | Treats generic preferences as hard repository violations. |
| Spec axis | Checks requirements, decisions, acceptance criteria, missing behavior, wrong behavior, and scope creep; marks the axis `Not verified` when no trustworthy spec exists. | Infers a spec from the diff or claims compliance without a source. |
| Axis independence | Collects Standards and Spec evidence independently, optionally in bounded parallel read-only passes, then verifies, deduplicates, labels, and severity-ranks findings centrally. | Lets one axis mask the other or concatenates unverified subagent output. |
| Necessary handoff | Emits a frontend/Rust audit handoff or Codex Security route only when that specialist must inspect a bounded part of the current review; otherwise keeps the optional profile internal and returns no handoff. | Lists specialists merely because a repository contains frontend, Rust, or security-sensitive code. |
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
