# Eval Cases

Use these cases when changing `implement-rust` triggers, workflow,
structure rules, validation expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Implement this Axum feature using the existing handler/service/repo structure.` | Should trigger `implement-rust`. | Rust implementation with repository layering. |
| `Add a crate to this Cargo workspace and update manifests, tests, docs, and checks.` | Should trigger `implement-rust`. | Structural Rust lifecycle work. |
| `Refactor this Tauri command and keep product logic in the core crate.` | Should trigger `implement-rust`. | Native shell and domain boundary. |
| `Remove this unused Rust module and close every export and CI reference.` | Should trigger `implement-rust`. | Deletion completeness. |
| `Before adding this endpoint, trace existing docs, routes, handlers, services, repos, DTOs, errors, callers, and tests.` | Should trigger `implement-rust`. | Reuse-first Rust interface work. |
| `Port this C++ subsystem to Rust without changing behavior, and review lifetimes plus release semantics.` | Should trigger `implement-rust`. | Source-compatible Rust migration. |
| `Fix this Rust/C FFI callback while preserving ABI layout, ownership, cleanup, panic, unsafe, and sanitizer coverage.` | Should trigger `implement-rust`. | Native boundary and resource-lifetime implementation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Plan the Rust migration across six repositories before editing.` | Should prefer `code-planner`. | Future cross-repository planning. |
| `Find why cargo test is failing before making changes.` | Should prefer `diagnose`. | Root cause unknown. |
| `Review all dirty changes and split commits.` | Should prefer `code-review`. | Dirty-tree review. |
| `Audit this Tokio and SQLite architecture for task leaks, contention, WAL growth, and query-plan risks.` | Should prefer `audit-rust`. | Read-only domain audit. |
| `Fix the React UI inside this Tauri app.` | Should prefer `implement-frontend`. | Frontend implementation. |

## Overlay Selection Eval

| Case | Expected selection and evidence | Reject if |
| --- | --- | --- |
| Routine: `Rename this private parser helper without changing behavior.` | Baseline only: repository format/check and the focused parser tests. Report no selected overlays. | Selects a higher or unrelated overlay, or runs native/stress tools by default. |
| Contract: `Add one public library method and preserve downstream compatibility.` | Baseline + Contract: public docs/doc tests, affected feature combinations, examples or downstream consumers, and compatibility fixtures where present. | Treats focused unit tests alone as public-contract proof. |
| SQLite: `Add a migration and change one durable query; no native code is involved.` | Baseline + Persistence/SQLite, plus Contract only if a public/durable consumer shape changes. Test fresh and supported upgrades, failure/restart or rollback, representative data, query behavior, and recovery evidence that applies. | Selects Unsafe/FFI merely because SQLite has a native implementation, or skips upgrade/recovery evidence. |
| FFI: `Fix ownership of a Rust/C callback; no database is involved.` | Baseline + Unsafe/FFI, plus Contract if caller-visible behavior changes. Verify ABI/layout, ownership/free symmetry, re-entry, panic containment, cleanup, and supported relevant dynamic tools. | Selects Persistence/SQLite or treats Miri/sanitizer availability as guaranteed. |
| FFI + SQLite: `Fix a native callback that owns rows imported into SQLite.` | Baseline + Unsafe/FFI + Persistence/SQLite, plus any independently applicable Contract or Concurrency/runtime overlay. Validate native lifetime and cleanup as well as transaction, rollback/restart, durability, and representative data. | Chooses one "highest" overlay, lets native checks replace migration/recovery checks, or lets database tests replace ABI/ownership checks. |
| Target-only: `Update the Windows-only path adapter without changing public behavior.` | Baseline + Target/platform: affected target build and real adapter behavior when available. Explicitly exclude Miri, sanitizer, fuzz, stress, leak, and repeated-operation checks unless another selected overlay makes one relevant and it is supported. | Inherits heavy native/porting tools solely because the code is target-specific, or claims other targets passed. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Project grounding | Reads guidance, status, Cargo/toolchain/command sources, and identifies the project class. | Assumes versions, commands, or one universal layout. |
| Toolchain preservation | Uses repository-pinned edition, resolver, Rust version, formatter, lints, and dependencies unless alignment is explicit. | Performs incidental upgrades or dependency churn. |
| Boundary ownership | Keeps entry, workflow, domain, persistence, and runtime responsibilities in documented owners. | Moves SQL or business rules into handlers/commands or creates empty layers. |
| Error and async safety | Uses the local typed error model, avoids runtime panics and blocking async work, and preserves cleanup/cancellation behavior. | Adds `unwrap`, silent fallback, unbounded work, or hidden global state without contract evidence. |
| Reuse gate | Reuses locally first and requires real consumers, stable API, named ownership, shared tests, and consumer validation before extraction. | Creates a shared crate for speculative reuse. |
| Interface inventory | Reads relevant docs and traces route, handler, service, repository, trait/type/DTO, error mapping, persistence, caller, test, and module placement before design. | Creates an endpoint or public API after inspecting one file. |
| Interface decision | Prefers reuse, extension, then reference adaptation; justifies a new interface and follows the nearest feature's naming, visibility, errors, docs, and tests. | Creates a parallel trait, DTO family, error model, or module convention. |
| Ownership and allocation | Prefers borrowing/slices, narrows visibility, avoids redundant clones/intermediate allocations, and passes small Copy values by value. | Clones to bypass API design or allocates without need. |
| Idiomatic errors | Uses the local typed error hierarchy, `Result`, `?`, lazy fallbacks, and tested error mapping without production panics. | Adds `unwrap`, `expect`, silent fallback, or erased library errors without contract reason. |
| Traits and dispatch | Uses concrete types/static dispatch by default and introduces traits, dyn dispatch, or type-state only for a real boundary or invalid-state guarantee. | Adds speculative traits, premature boxing, or clever type-state without benefit. |
| Docs and tests | Documents public APIs and invariants, adds focused behavior/error tests and doc tests where useful, and keeps comments rationale-only. | Leaves public contracts undocumented or uses comments instead of types/tests. |
| Concurrency and safety | Preserves Send/Sync, bounded work, cancellation/cleanup, correct pointer/lock choices, and minimal documented unsafe. | Blocks async work, creates unbounded tasks, misuses Rc/Arc/locks, or adds undocumented unsafe. |
| FFI contract | Centralizes raw operations behind narrow adapters and verifies ABI/layout, pointer validity, aliasing, ownership/free symmetry, callbacks, re-entry, threads, and panic behavior. | Spreads raw pointers across business code or assumes foreign enums, lifetimes, allocators, or callbacks are Rust-safe. |
| Porting discipline | Records type/ownership/lifetime mappings, proves a representative slice, preserves behavior before cleanup, and reviews source/Rust semantic differences. | Starts a bulk rewrite from syntax alone, mixes parity with redesign, or treats compilation as equivalence. |
| Lint and performance | Runs repository rustfmt/check/test/doc/Clippy gates, fixes warnings, and measures before optimization. | Silences lints broadly or adds guessed performance complexity. |
| Composable validation | Starts with Baseline, selects every applicable independent overlay, maps evidence to each overlay, and uses Miri, sanitizer/leak, fuzz, stress, or repeated-operation gates only when supported and relevant. | Chooses one "highest" profile, drops one side of a mixed FFI/SQLite risk, runs only `cargo check` for a selected high-risk invariant, or applies heavy tools to target-only/routine work without relevance. |
| Structural lifecycle | Updates manifests, exports, commands, tests, CI/deploy paths, docs, indexes, and stale references for add/move/delete work. | Changes directories or crates while leaving ownership records stale. |
| Validation | Runs repository-defined format/check/test/Clippy gates that match the change or records exact gaps. | Invents commands or claims success without evidence. |
| Publish readiness | Keeps the package self-contained, updates metadata and eval cases, and validates with `python3 scripts/validate-skills.py`. | Depends on repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: every quality case scores at least 7,
and all trigger/non-trigger and overlay-selection expectations are correct.
Selecting one highest profile for a mixed risk, or applying unrelated
heavy checks to Routine or target-only work, is an automatic selection failure.
