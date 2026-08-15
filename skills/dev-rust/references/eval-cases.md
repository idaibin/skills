# Eval Cases

## Contents

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Independent Review Outlet Eval](#independent-review-outlet-eval)
- [Overlay Selection Eval](#overlay-selection-eval)
- [Quality Eval](#quality-eval)
- [Agent Runtime Critical Boundary Eval](#agent-runtime-critical-boundary-eval)
- [Scoring](#scoring)

Use these cases when changing `dev-rust` triggers, workflow,
structure rules, validation expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Implement this Axum feature using the existing handler/service/repo structure.` | Should trigger `dev-rust`. | Rust implementation with repository layering. |
| `Fix this Axum handler's body extractor order, typed rejection mapping, and router service test without broad CORS.` | Should trigger `dev-rust`. | Axum transport-boundary implementation. |
| `Add a crate to this Cargo workspace and update manifests, tests, docs, and checks.` | Should trigger `dev-rust`. | Structural Rust lifecycle work. |
| `Refactor this Tauri command and keep product logic in the core crate.` | Should trigger `dev-rust`. | Native shell and domain boundary. |
| `Add this Tauri file command with Rust-side path validation, least-privilege capability/permission scope, typed errors, and real-client verification.` | Should trigger `dev-rust` plus applicable target/platform evidence. | Native IPC trust-boundary implementation. |
| `Implement a resumable local agent turn with typed tool operations, bounded async work, approval before a file mutation, and recovery after an uncertain IPC response.` | Should trigger `dev-rust` with the Agent Runtime profile plus only the reachable Concurrency/runtime, Target/platform, and persistence/protocol overlays. | Stateful agent lifecycle and side-effect boundary are implementation scope; do not copy a generic runtime or claim host sandbox proof. |
| `Implement Tauri authorization for a custom command: generate allow/deny app-command permissions, assign only the intended window capability, scope paths, and reject an unauthorized business user in the Rust domain.` | Should trigger `dev-rust` plus applicable target/platform and contract evidence. | Custom-command ACL setup, resource scope, and domain policy are distinct enforcement layers. |
| `Remove this unused Rust module and close every export and CI reference.` | Should trigger `dev-rust`. | Deletion completeness. |
| `Remove the Rust declarations made obsolete by this change after checking cfg, features, macros, FFI exports, examples, and downstream use.` | Should trigger `dev-rust` with shared code-quality reachability. | Scoped implementation cleanup. |
| `Before adding this endpoint, trace existing docs, routes, handlers, services, repos, DTOs, errors, callers, and tests.` | Should trigger `dev-rust`. | Reuse-first Rust interface work. |
| `Port this C++ subsystem to Rust without changing behavior, and review lifetimes plus release semantics.` | Should trigger `dev-rust`. | Source-compatible Rust migration. |
| `Fix this Rust/C FFI callback while preserving ABI layout, ownership, cleanup, panic, unsafe, and sanitizer coverage.` | Should trigger `dev-rust`. | Native boundary and resource-lifetime implementation. |
| `Add this HTTP operation using the service's code-first Rust authority, regenerate normalized OpenAPI and the TypeScript client, and prove compatibility plus auth/error conformance.` | Should trigger `dev-rust` with Protocol-contract overlay. | Rust source and contract generation are requested. |
| `Add this REST handler using the repository's native route, DTO, client, and tests; do not introduce schema generation.` | Should trigger `dev-rust` with Baseline only and mark protocol automation `Not applicable`. | HTTP implementation does not itself require OpenAPI. |
| `Implement a macOS cleanup command that discovers app-owned residuals, asks before deletion, and rescans afterward.` | Should trigger `dev-rust` with Target/platform evidence and destructive-operation safeguards. | Rust implementation owns candidate attribution, bounded deletion behavior, confirmation, recovery policy, and result reconciliation. |
| `Change this Rust service's startup configuration, packaged resource precedence, and compatible consumer rollout.` | Trigger `dev-rust` with project grounding before edits. | The change crosses runtime, artifact, compatibility, and delivery boundaries. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and structure first.` | Should prefer `repo-map`. | Repository mapping. |
| `Plan the Rust migration across six repositories before editing.` | Should not trigger this Skill; use the host's built-in planning. | Future cross-repository planning. |
| `Find why cargo test is failing before making changes.` | Should not trigger this Skill; use the host's built-in diagnosis under effective instructions. | Root cause unknown. |
| `Review all dirty changes and split commits.` | Should prefer `repo-review`. | Dirty-tree review. |
| `Audit this Tokio and SQLite architecture for task leaks, contention, WAL growth, and query-plan risks.` | Should prefer `audit-rust`. | Read-only domain audit. |
| `Review this Axum endpoint diff for authorization and token exposure.` | Should prefer `repo-review`. | Fixed-basis review, not implementation. |
| `Fix the React UI inside this Tauri app.` | Should prefer `dev-frontend`. | Frontend implementation. |
| `Define the product behavior, permission rules, user-visible outcomes, and acceptance before writing the endpoint.` | Should prefer `product-spec`. | Product decisions are unresolved. |
| `Rename only a private Rust helper; no reachable runtime, packaging, API, persistence, or cross-repository behavior changes.` | Keep project-grounding risk classes `Not applicable`; do not scan deployment or consumer repositories. | A local refactor is not a semantic grounding trigger. |
| `Implement a synchronous Rust parser with a typed return value; it has no agent thread/turn state, durable operation history, async work, or IPC.` | Trigger `dev-rust` Baseline only; do not load the Agent Runtime profile. | A Rust type or ordinary function is not an agent runtime boundary. |

## Independent Review Outlet Eval

| User prompt | Expected result |
| --- | --- |
| `Implement the Rust slice, then explicitly prepare an independent ChatGPT security challenge without applying its findings.` | Keep `dev-rust` as owner and emit one lightweight `ask-ai` handoff. |
| `Implement and validate the Rust slice locally; no external review was requested.` | Emit no `ask-ai` handoff. |

## Overlay Selection Eval

| Case | Expected selection and evidence | Reject if |
| --- | --- | --- |
| Routine: `Rename this private parser helper without changing behavior.` | Baseline only: repository format/check and the focused parser tests. Report no selected overlays. | Selects a higher or unrelated overlay, or runs native/stress tools by default. |
| Contract: `Add one public library method and preserve downstream compatibility.` | Baseline + Contract: public docs/doc tests, affected feature combinations, examples or downstream consumers, and compatibility fixtures where present. | Treats focused unit tests alone as public-contract proof. |
| Protocol automation: `Extend the existing OpenAPI pipeline with one authenticated operation.` | Baseline + Protocol automation: identify one code-first or contract-first authority, validate and rebuild normalized OpenAPI twice, diff compatibility at a fixed basis, regenerate the TS client, and verify applicable backend success/auth/validation/business-error behavior. | Activates from REST alone, assumes a library, permits dual authorities, or treats static schema validation as live conformance. |
| SQLite: `Add a migration and change one durable query; no native code is involved.` | Baseline + Persistence/SQLite, plus Contract only if a public/durable consumer shape changes. Test fresh and supported upgrades, failure/restart or rollback, representative data, query behavior, and recovery evidence that applies. | Selects Unsafe/FFI merely because SQLite has a native implementation, or skips upgrade/recovery evidence. |
| FFI: `Fix ownership of a Rust/C callback; no database is involved.` | Baseline + Unsafe/FFI, plus Contract if caller-visible behavior changes. Verify ABI/layout, ownership/free symmetry, re-entry, panic containment, cleanup, and supported relevant dynamic tools. | Selects Persistence/SQLite or treats Miri/sanitizer availability as guaranteed. |
| FFI + SQLite: `Fix a native callback that owns rows imported into SQLite.` | Baseline + Unsafe/FFI + Persistence/SQLite, plus any independently applicable Contract or Concurrency/runtime overlay. Validate native lifetime and cleanup as well as transaction, rollback/restart, durability, and representative data. | Chooses one "highest" overlay, lets native checks replace migration/recovery checks, or lets database tests replace ABI/ownership checks. |
| Target-only: `Update the Windows-only path adapter without changing public behavior.` | Baseline + Target/platform: affected target build and real adapter behavior when available. Explicitly exclude Miri, sanitizer, fuzz, stress, leak, and repeated-operation checks unless another selected overlay makes one relevant and it is supported. | Inherits heavy native/porting tools solely because the code is target-specific, or claims other targets passed. |
| Source-derived case study: `Fix this Rust/C ownership port and compare its cleanup semantics with the source implementation.` | Baseline + applicable Porting/parity and Unsafe/FFI overlays; load Bun-derived prompts only for relevant cross-language, cleanup, or invariant questions, while keeping local repository contracts authoritative. | Loads the case study for a routine Rust task, copies Bun's architecture/toolchain, or lets it redefine the validation model. |
| Tokio cancellation: `Fix a select loop that restarts a non-cancellation-safe operation and drops spawned task failures.` | Baseline + Concurrency/runtime: preserve in-progress state, observe output/error/cancel/panic, and test shutdown/cancellation behavior. | Adds a token/JoinSet mechanically, drops handles, or assumes every losing future is safe to restart. |
| Tokio intentional detachment: `Keep this bounded best-effort telemetry task detached; failures already reach metrics and it owns no shutdown resource.` | Baseline + Concurrency/runtime: record the explicit lifecycle/outcome policy and verify bounded work, non-critical impact, resource ownership, and independent observability. | Saves/joins the handle mechanically or declares every detached task defective. |
| Agent Runtime: `Add a resumable local-agent operation that crosses a typed IPC boundary and writes durable history.` | Baseline + Agent Runtime; compose Protocol automation, Concurrency/runtime, Persistence/SQLite, and Target/platform only when the repository/task actually owns those seams. Define the minimum Thread/Turn/Operation correlation, one schema authority, uncertain-write recovery, approval/policy/sandbox separation, and IPC evidence. | Introduces a generic runtime, requires all overlays unconditionally, treats generated types as runtime proof, or retries a non-idempotent write after an uncertain response. |
| Agent Runtime non-trigger: `Add a stateless local command with no durable history, task lifecycle, approval, or cross-process transport.` | Baseline only; the Agent Runtime profile is `Not applicable`. | Adds a ledger, JSONL/SQLite projection, or thread/turn hierarchy solely because the command is called an agent. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Validation proportionality | Starts with crate/module-focused Baseline checks, composes only applicable overlays, and reserves workspace-wide/release gates for final lifecycle stages, explicit requests, or missing credible focused coverage. | Runs the entire workspace or heavy tools by default for a bounded Rust edit, or calls focused evidence release proof. |
| Project grounding | Reads guidance, status, Cargo/toolchain/command sources, and identifies the project class. | Assumes versions, commands, or one universal layout. |
| Specification readiness | Reads available requirements, acceptance criteria, non-goals, affected crates/modules/files, compatibility, and validation seams; uses host planning for unresolved complex work before editing. | Implements a complex ambiguous request without a usable specification or explicit assumptions. |
| Behavior-first slices | When a stable public seam exists, works one failing behavior test and minimal vertical slice at a time; skips TDD with a stated reason when only brittle internal assertions are possible. | Writes horizontal test batches, duplicates implementation logic in expectations, or claims TDD without observing red before green. |
| Evidence-gated code quality | Avoids duplicate authorities and speculative layers, preserves justified trait/newtype/adapter seams, and removes only code made obsolete by the task after Rust reachability checks. | Treats one implementation, clone, Arc/Mutex, optional lint or text-search absence as sufficient evidence, or cleans unrelated legacy code. |
| Toolchain preservation | Uses repository-pinned edition, resolver, Rust version, formatter, lints, and dependencies unless alignment is explicit. | Performs incidental upgrades or dependency churn. |
| Boundary ownership | Keeps entry, workflow, domain, persistence, and runtime responsibilities in documented owners. | Moves SQL or business rules into handlers/commands or creates empty layers. |
| Error and async safety | Uses the local typed error model, avoids runtime panics and blocking async work, and preserves cleanup/cancellation behavior. | Adds `unwrap`, silent fallback, unbounded work, or hidden global state without contract evidence. |
| Reuse gate | Reuses locally first and requires real consumers, stable API, named ownership, shared tests, and consumer validation before extraction. | Creates a shared crate for speculative reuse. |
| Interface inventory | Consumes a current `repo-map` inventory or reads relevant docs and traces route, handler, service, repository, trait/type/DTO, error mapping, persistence, caller, test, and module placement before design. | Creates an endpoint or public API after inspecting one file. |
| Interface decision | Prefers reuse, extension, then reference adaptation; justifies a new interface and follows the nearest feature's naming, visibility, errors, docs, and tests. | Creates a parallel trait, DTO family, error model, or module convention. |
| Protocol activation | Uses the generated-contract profile only for an existing pipeline or explicit migration/trial; otherwise follows the native route/DTO/client contract and reports `Not applicable`. | Requires OpenAPI merely because an HTTP endpoint changed. |
| Protocol authority and live gate | When active, traces one authority through normalized OpenAPI and generated client with actual commands, then proves applicable generation, compatibility, conformance, and clean-state gates or marks them `Not verified`. | Infers authority, maintains dual sources, or claims live proof from static checks. |
| Ownership and allocation | Prefers borrowing/slices, narrows visibility, avoids redundant clones/intermediate allocations, and passes small Copy values by value. | Clones to bypass API design or allocates without need. |
| Idiomatic errors | Uses the local typed error hierarchy, `Result`, `?`, lazy fallbacks, and tested error mapping without production panics. | Adds `unwrap`, `expect`, silent fallback, or erased library errors without contract reason. |
| Traits and dispatch | Uses concrete types/static dispatch by default and introduces traits, dyn dispatch, or type-state only for a real boundary or invalid-state guarantee. | Adds speculative traits, premature boxing, or clever type-state without benefit. |
| Docs and tests | Documents public APIs and invariants, adds focused behavior/error tests and doc tests where useful, and keeps comments rationale-only. | Leaves public contracts undocumented or uses comments instead of types/tests. |
| Concurrency and safety | Preserves Send/Sync, bounded work, cancellation/cleanup, correct pointer/lock choices, explicit task lifecycle/outcome policy, and minimal documented unsafe; intentional detachment is limited to bounded non-critical work without uncontrolled resources and with irrelevant or independent failure observation. | Blocks async work, creates unbounded tasks, misuses Rc/Arc/locks, mandates structured-task machinery without responsibility evidence, or adds undocumented unsafe. |
| FFI contract | Centralizes raw operations behind narrow adapters and verifies ABI/layout, pointer validity, aliasing, ownership/free symmetry, callbacks, re-entry, threads, and panic behavior. | Spreads raw pointers across business code or assumes foreign enums, lifetimes, allocators, or callbacks are Rust-safe. |
| Porting discipline | Records type/ownership/lifetime mappings, proves a representative slice, preserves behavior before cleanup, and reviews source/Rust semantic differences. | Starts a bulk rewrite from syntax alone, mixes parity with redesign, or treats compilation as equivalence. |
| Lint and performance | Runs repository rustfmt/check/test/doc/Clippy gates, fixes warnings, and measures before optimization. | Silences lints broadly or adds guessed performance complexity. |
| Composable validation | Starts with Baseline, selects every applicable independent overlay, maps evidence to each overlay, and uses Miri, sanitizer/leak, fuzz, stress, or repeated-operation gates only when supported and relevant. | Chooses one "highest" profile, drops one side of a mixed FFI/SQLite risk, runs only `cargo check` for a selected high-risk invariant, or applies heavy tools to target-only/routine work without relevance. |
| Structural lifecycle | Updates manifests, exports, commands, tests, CI/deploy paths, docs, indexes, and stale references for add/move/delete work. | Changes directories or crates while leaving ownership records stale. |
| Destructive cleanup behavior | Tests candidate discovery, ownership and scope checks, confirmation or policy authorization, recoverability where allowed, bounded action, partial failure, and post-action rescan. | Deletes a broad directory from path matching alone, treats discovery as ownership proof, skips confirmation, or reports success without reconciliation. |
| Validation | Runs repository-defined format/check/test/Clippy gates that match the change or records exact gaps. | Invents commands or claims success without evidence. |
| Publish readiness | Keeps the package self-contained, updates metadata and eval cases, and runs the repository-authoritative source validation. | Depends on repository-local prompts or skips source validation. |
| Source-derived reference boundary | Loads the Bun-derived case study only for applicable Porting/parity or Unsafe/FFI questions and uses it as prompts, not a second rule or validation authority. | Applies it to routine work, repeats its former validation ladder, or copies Bun-specific policy. |
| Common implementation report | Reports scope, detected boundaries, authorities/owners, selected Rust risks, changed files/contracts, Baseline/overlay validation, Worktree drift, excluded work, and `Not verified`; adds FFI/persistence/target evidence only when applicable. | Uses an unrelated report shape, omits drift/exclusions, or requires high-risk fields for a routine change. |
| Agent Runtime contract | Names the existing runtime/transport/persistence authority; records the smallest legal Thread/Turn/Operation state machine, operation idempotency and uncertain-result stop path, typed schema generation/compatibility evidence, and selected async, approval/policy/sandbox, durable, or IPC gates. | Treats a title, display ID, generated schema, unit test, or local compile as identity, authorization, sandbox, deployment, or recovery proof. |
| Agent Runtime scope discipline | Reuses the nearest owner and selects only reachable sections; records target/host/client evidence as `Not verified` when unavailable and keeps unrelated profiles out of scope. | Copies a large external agent architecture, adds JSONL/SQLite without replay/recovery need, or applies a sandbox/approval claim based on Rust prose. |

## Agent Runtime Critical Boundary Eval

| Case | Expected behavior | Reject if |
| --- | --- | --- |
| An IPC write reaches the host but the process receives no response. | Persist `operation_id` before the call, mark the result `uncertain`, reconcile with bounded read-only evidence under the same ID, and stop without resending a non-idempotent operation. | Treats timeout as failure and blindly retries, creates a new operation ID, or reports success without evidence. |
| A Tauri custom command mutates a file but has no generated app-command permission or assigned capability. | Stop the implementation at the authorization boundary; distinguish command registration, capability/permission, configured scope, Rust domain policy, and host/client evidence. | Assumes frontend typing, CSP, or `invoke_handler` registration supplies per-window authorization or sandboxing. |
| A JSONL event is durable but the SQLite projection update is interrupted. | Keep the source log authoritative, replay idempotently from the event/sequence watermark, and test duplicate/restart behavior before claiming recovery. | Makes SQLite a second writer, deletes the log, or claims consistency from one successful append. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: every quality case scores at least 8,
and all trigger/non-trigger and overlay-selection expectations are correct.
Selecting one highest profile for a mixed risk, or applying unrelated
heavy checks to Routine or target-only work, is an automatic selection failure.
