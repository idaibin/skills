# Eval Cases

## Contents

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Quality Eval](#quality-eval)
- [Scoring](#scoring)

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Audit a TanStack Router Console feature for architecture/reuse and query-state contracts; leave accessibility out of scope.` | Trigger `repo-audit` with the frontend profile's Architecture/Reuse and State/Data/Contracts profiles. |
| `Audit this Vue app's client route against the backend controller, gateway context, auth scope, production config, and failure states.` | Trigger State/Data plus Build/Tooling and project grounding for the bounded provider/consumer chain. |
| `Audit this Java Spring service for build, security, transactions, and persistence risks.` | Trigger `repo-audit` with the Java profile. |
| `Audit this Java service's current transaction and Redis consistency.` | Trigger `repo-audit` with the Java profile's Persistence and Integration profiles. |
| `Audit whether this Java service's source profiles, packaged resources, startup exclusions, and target service registration resolve consistently.` | Trigger Build/Migration plus project grounding; keep source, artifact, and runtime evidence distinct. |
| `Audit this Rust workspace for ownership, concurrency, persistence, and unsafe risks.` | Trigger `repo-audit` with the Rust profile. |
| `Audit a Tokio service for task leaks, backpressure, lock contention, cancellation, and shutdown.` | Trigger `repo-audit` with the Rust profile's Concurrency/runtime profile. |
| `Audit this Rust service's packaged configuration, startup registration, durable migration compatibility, and consumer handoff.` | Trigger `repo-audit` with project grounding; keep source, artifact, and runtime evidence distinct. |
| `This attached API contract explicitly replaces the stale repository copy; audit the frontend against the replacement without editing files.` | Freeze the incoming contract as the audit basis, report local-copy drift, and remain read-only. |
| `Under repo-review, perform a read-only specialist audit of only the changed Vue SFCs for state, lifecycle, accessibility, and performance.` | Trigger bounded `repo-audit`; keep `repo-review` as local Git-change review owner. |
| `Under repo-review, inspect only the changed Tokio/SQLite surface for concurrency and recovery findings without staging.` | Trigger `repo-audit` as a scoped read-only specialist; `repo-review` retains review coordination. |
| `Audit this Tauri frontend/Rust boundary for progress, cancellation, errors, menus, and shortcuts.` | Trigger the frontend Desktop Boundary profile plus applicable Rust-profile surface. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Change one known component's copy and keep everything else unchanged.` | Prefer `dev-frontend`. |
| `Implement the confirmed Java fix.` | Route to `dev-java`. |
| `Rename one known private Rust function and run its existing test.` | Prefer `dev-rust`. |
| `Map repository roots, runtime identities, and shared dependencies.` | Prefer `repo-map`. |
| `Review the whole local dirty tree and prepare exact staging.` | Prefer `repo-review`, which may delegate bounded paths. |
| `Review this immutable branch range and coordinate Rust, frontend, security, CI, and docs.` | Prefer `repo-review`; it may delegate bounded paths here. |
| `Prove this dependency is exploitable.` | Route to an available security validation workflow. |
| `Run a full vulnerability scan and validate exploitability across this repository.` | Prefer an available host security-scan workflow; `repo-audit` may supply bounded domain evidence but does not own scan coverage or PoC validation. |
| `Audit this Kotlin Spring coroutine service.` | Do not claim Kotlin semantics; route to a language-capable workflow unless the request explicitly limits scope to Java-owned Spring/build configuration. |
| `Find the unknown cause of this failing test.` | Use the host's built-in diagnosis under effective instructions. |
| `Operate the real Tauri window and capture evidence.` | Prefer `ops-client`. |
| `Turn this selected visual source into a Feature Spec.` | Prefer `ui-spec`. |
| `Audit only a local CSS color token rename with no reachable API, build, runtime, or cross-repo effect.` | Keep project grounding inactive and unrelated profiles out of scope. |
| `Audit this Java DTO naming only; no runtime, persistence, public contract, or cross-repo behavior is in scope.` | Keep project grounding inactive; do not scan profiles, schemas, or sibling repositories. |
| `Audit only a private Rust naming cleanup with no reachable runtime, packaging, API, persistence, or cross-repository effect.` | Keep project grounding inactive and unrelated profiles out of scope. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Grounding | reads guidance/status and inventories only evidence needed for selected language and risk profiles | starts from a universal template or scans everything |
| Language profile | selects exactly the frontend, Java, and/or Rust profiles that the audited surface reaches and marks the others `Out of scope` | audits a language with no selected profile or bundles every language into one sweep |
| Risk profile selection | declares selected risk profiles per language and marks the rest `Out of scope` | implies every dimension was reviewed when only some were evidenced |
| Inspection snapshot | records revision and relevant Worktree state for reproducibility without claiming diff attribution | audits an unrecorded moving tree or says the snapshot introduced an issue |
| Evidence-gated quality | applies audit semantics and proves reachability, impact, owner/location and verification for duplication, dead/unused code, abstraction and coupling findings | treats similarity, file size, one wrapper, or optional lint advice as a finding |
| Contract priority | applies declared product/UI contracts to semantics and acceptance, treats code/config as implementation facts, and reports conflicts as drift | lets the current adapter override a resolved contract |
| Validation drift | avoids known write-capable commands; stops on unexpected tracked drift, marks evidence contaminated and `Not verified`, and does not revert it | silently changes the review basis or reports the command as valid read-only evidence |
| Validation | runs relevant real commands/runtime proof through the selected profile or reports `Not verified` | invented commands or unsupported pass claim |
| Reporting | leads with outcome/findings and includes selected profiles, excluded profiles, exact evidence, `Not found`, and `Not verified` | reports unsupported success or adds empty all-domain sections |
| Read-only boundary | leaves code and Git/GitHub state unchanged, routes fixes to the matching `dev-*` owner, and returns bounded findings to the coordinating reviewer | edits, stages, commits, comments, claims readiness, or expands scope |
| Coordinator boundary | keeps Worktree and immutable basis ownership inside `repo-review` while the specialist remains path-bounded | lets the specialist take over whole review, staging, or final cross-domain severity |
| Security-provider boundary | keeps domain semantic evidence in the selected profile and routes explicit vulnerability scanning or PoC validation to the host security workflow | recreates a general scanner or treats a domain signal as validated exploitability |
| Scope | preserves unrelated work and does not run excluded profiles | drive-by audit or cleanup |

Language-specific scenarios, profile-selection cases, and rubric rows live in
[frontend scenarios](frontend-eval-scenarios.md),
[Java scenarios](java-eval-scenarios.md), and
[Rust scenarios](rust-eval-scenarios.md); score them only with their selected
language profile.

## Scoring

Minimum pass: trigger/non-trigger routing is correct for every language
prompt, and every applicable quality row scores at least 8. Language rows are
`Out of scope` when that profile is not selected; unavailable required
evidence may remain `Not verified`, but a fabricated command result,
benchmark, runtime version, or recovery proof is an automatic fail.
