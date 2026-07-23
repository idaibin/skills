# Eval Cases

## Contents

- [Trigger Eval](#trigger-eval)
- [Non-Trigger Eval](#non-trigger-eval)
- [Profile Selection Eval](#profile-selection-eval)
- [Scenario Eval](#scenario-eval)
- [Quality Eval](#quality-eval)
- [Scoring](#scoring)

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Audit a Tokio service for task leaks, backpressure, lock contention, cancellation, and shutdown.` | Trigger `audit-rust`. |
| `Profile CPU, allocations, RSS, I/O, binary size, and compile time before optimizing this Rust workspace.` | Trigger `audit-rust`. |
| `Review SQLite migrations, WAL growth, query plans, indexes, vacuum, backup, and recovery in a Tauri app.` | Trigger `audit-rust`. |
| `Audit crate boundaries and public APIs for a local-first Rust CLI and library.` | Trigger `audit-rust`. |
| `Audit unsafe FFI ownership and validate it with supported Rust tools.` | Trigger `audit-rust`. |
| `Compare our Rust baseline and audit legacy exceptions without mechanically renaming production code.` | Trigger `audit-rust`. |
| `Under repo-review, inspect only the changed Tokio/SQLite surface for concurrency and recovery findings without staging.` | Trigger `audit-rust` as a scoped read-only specialist; `repo-review` retains local Git-change review coordination. |
| `Under repo-review, inspect only the Rust paths in this immutable range.` | Trigger `audit-rust` as a scoped read-only specialist; `repo-review` retains immutable-review coordination. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Rename one known private Rust function and run its existing test.` | Prefer `dev-rust`. |
| `Find why this test started failing; the cause is unknown.` | Do not trigger this Skill; use the host's built-in diagnosis under effective instructions. |
| `Memory grows after each Rust import and nobody knows whether the cause is ownership, allocator retention, or the operating system.` | Use host diagnosis to reproduce the concrete symptom and isolate its cause before auditing a selected remediation surface. |
| `Map the repository and tell me whether it contains Rust.` | Prefer `repo-map`. |
| `Review my dirty tree and prepare exact commits.` | Prefer `repo-review`; it coordinates the local read-only Git-change review and may request a bounded Rust specialist subreview. |
| `Review the current Rust crate deletion diff across manifests, CI, tests, and docs.` | Prefer `repo-review` as the local read-only review coordinator; do not auto-route to delivery. |
| `Review this immutable branch range and coordinate Rust, frontend, security, CI, and docs.` | Prefer `repo-review`; it may delegate bounded Rust paths here. |
| `Run a professional security scan of this known Rust module with no diff basis.` | Prefer `codex-security:security-scan`. |

## Profile Selection Eval

| Prompt | Expected selection and scope | Reject if |
| --- | --- | --- |
| `Audit only crate ownership, workspace inheritance, and architecture docs for this Rust library.` | Focused audit: Architecture/baseline. Run common gates and that profile only; mark Ownership/errors, Concurrency/runtime, Performance/memory, SQLite, and Unsafe/FFI `Out of scope`. | Loads, reports, or scores all profiles; demands runtime, query-plan, or Miri evidence. |
| `Audit only this synchronous CLI's SQLite migration and critical query plan.` | Focused audit: SQLite. Verify applicable runtime/linkage, migration, representative data, plan, rollback/recovery, and common evidence; mark unrelated profiles `Out of scope`. | Automatically adds Tokio, performance/memory, unsafe/FFI, or workspace architecture because SQLite is implemented natively. |
| `Audit the Tokio worker that owns this SQLite connection for blocking work, cancellation, shutdown, transactions, and WAL recovery.` | Combined audit: Concurrency/runtime + SQLite. Keep both profiles' evidence and validate task/database failure, cancellation, shutdown/restart, and recovery interactions. | Treats one profile as satisfying the other, or expands into unrelated architecture, broad performance, or FFI review. |
| `Audit this unsafe FFI adapter, but the required target and sanitizer are unavailable here.` | Focused audit: Unsafe/FFI remains selected. Review static repository evidence, mark target/sanitizer-dependent claims exactly `Not verified`, state what would verify them, and mark other profiles `Out of scope`. | Claims the unavailable checks passed, substitutes unrelated commands, drops the profile, or broadens into every domain. |

## Scenario Eval

Each case must include the listed evidence, judgment, scope, validation, and
report. Commands are candidates only when the target repository defines or
supports them.

### 1. Clone In A Loop

- **Input:** A reviewer marks every `clone()` inside a parsing loop as a performance bug.
- **Investigate:** cloned type/backing allocation, item count, frequency, release profile, CPU/allocation profile, and lifetime/readability alternative.
- **Correct:** report a finding only when size, rate, hot-path evidence, and impact are material; otherwise keep the simpler ownership.
- **Reject:** clone-count heuristics or complex borrowing without measurement.
- **Acceptable scope:** the measured clone path, benchmark, and nearby ownership docs/tests.
- **Validation:** repository test plus same-workload release benchmark/allocation profile.
- **Final report:** type, frequency, baseline, result, trade-off, and residual `Not verified` paths.

### 2. Unbounded Tokio Channel

- **Input:** Producers outpace a consumer and process memory grows continuously.
- **Investigate:** message size/rate, consumer throughput, queue depth, producer count, overload policy, task lifecycle, and RSS/allocation timeline.
- **Correct:** add bounded capacity and explicit await/reject/coalesce/drop semantics with observability.
- **Reject:** only increasing memory, adding arbitrary capacity, or calling it a leak without owner evidence.
- **Acceptable scope:** channel owner, producers/consumer, metrics, lifecycle tests, and relevant docs.
- **Validation:** overload, channel-close, cancellation, shutdown tests and representative memory run.
- **Final report:** capacity derivation, backpressure behavior, before/after queue/RSS, and loss semantics.

### 3. Background Task Survives Shutdown

- **Input:** A worker continues after the application announces shutdown.
- **Investigate:** spawn site, join handle/tracker, cancellation signal and points, blocking work, panic path, cleanup, and process exit.
- **Correct:** stop intake, signal cancellation, clean partial state, await critical work with a defined deadline, and report failure.
- **Reject:** dropping the handle, abort-only cleanup, or sleeping before exit.
- **Acceptable scope:** task owner, shutdown coordinator, resource cleanup, tests, and runbook.
- **Validation:** deterministic success/error/panic/cancel/shutdown tests and real runtime check when needed.
- **Final report:** owner, cancellation path, wait/deadline, cleanup evidence, and remaining non-cancellable work.

### 4. `Arc<Mutex<HashMap>>`

- **Input:** Shared state uses `Arc<Mutex<HashMap<...>>>` and a reviewer demands sharding.
- **Investigate:** read/write ratio, critical-section work, `.await`, contention profile, consistency invariant, key distribution, and owner alternatives.
- **Correct:** keep it when simple and uncontended; otherwise shorten the lock, assign an owner/actor, or shard from measured contention.
- **Reject:** automatic replacement by a concurrent map or async mutex.
- **Acceptable scope:** measured shared-state boundary and tests.
- **Validation:** correctness plus contention/throughput comparison under representative concurrency.
- **Final report:** invariant, profile evidence, chosen ownership, and complexity trade-off.

### 5. SQLite Commit Per Row

- **Input:** Import writes each row in a separate transaction.
- **Investigate:** row count, fsync/journal mode, failure semantics, batch size, busy behavior, memory, and progress/cancellation.
- **Correct:** use an atomic or bounded batch transaction consistent with recovery and responsiveness.
- **Reject:** one huge transaction without failure/cancel analysis or merely adding a pool.
- **Acceptable scope:** import writer, transaction policy, progress, migration/test fixtures, and docs.
- **Validation:** result correctness, failure rollback/retry, same-data timing/I/O, and busy handling.
- **Final report:** transaction boundary, rows/batch, before/after time/I/O, and recovery semantics.

### 6. WAL File Keeps Growing

- **Input:** A WAL-mode database's `-wal` file grows over time.
- **Investigate:** runtime version, checkpoint settings/results, long readers, active statements/rows, write size, connection count, backup, and file metrics.
- **Correct:** close long readers, restore appropriate automatic/manual checkpoint policy, or bound large writes after proving cause.
- **Reject:** deleting `-wal`/`-shm`, assuming corruption, or forcing truncate checkpoints on every write.
- **Acceptable scope:** reader/writer/checkpoint owners, observability, lifecycle tests, and operations docs.
- **Validation:** representative concurrent run, checkpoint status, data integrity, restart, and backup/restore.
- **Final report:** cause evidence, runtime/linkage, checkpoint behavior, file-size timeline, and reader impact.

### 7. Database File Does Not Shrink After Delete

- **Input:** Rows are deleted but the main database file size is unchanged.
- **Investigate:** `page_count`, `freelist_count`, auto-vacuum mode, reuse workload, disk pressure, VACUUM space/locking, and rowid/backup implications.
- **Correct:** explain reusable freelist pages; vacuum or incremental maintenance only when measured benefit justifies cost.
- **Reject:** declaring a leak, defaulting to `auto_vacuum=FULL`, or scheduling full vacuum blindly.
- **Acceptable scope:** maintenance policy, telemetry, controlled operation, and runbook.
- **Validation:** copy/backup test, page/file metrics, free-space check, integrity and restore verification.
- **Final report:** page evidence, chosen maintenance, required disk/outage, and result.

### 8. Multiple Single-Column Indexes

- **Input:** A query filters and orders by several fields, each with its own index.
- **Investigate:** query predicates/order/grouping, cardinality, data distribution, current indexes/statistics, write rate, and plan.
- **Correct:** keep, remove, or replace indexes based on a representative plan and workload-shaped composite/partial/covering option.
- **Reject:** one index per field or assuming SQLite combines all indexes efficiently.
- **Acceptable scope:** relevant migration/indexes, query, fixtures, and performance docs.
- **Validation:** `EXPLAIN QUERY PLAN`, result correctness, representative read timing, write/storage cost, and migration upgrade.
- **Final report:** old/new plan, cardinality, timing, index size/write trade-off, and rollback.

### 9. Full Table Scan

- **Input:** `EXPLAIN QUERY PLAN` shows `SCAN` for a critical query.
- **Investigate:** table size, selected fraction, ordering, existing indexes/statistics, parameter values, temp B-tree, and actual latency.
- **Correct:** accept a rational small/broad scan or add/change an index when representative evidence shows benefit.
- **Reject:** treating every scan as defective or parsing plan output as a stable API.
- **Acceptable scope:** query, justified schema/index migration, data fixture, and benchmark.
- **Validation:** plan and same-data timing before/after plus write/storage impact.
- **Final report:** plan interpretation, workload, decision, and regression evidence.

### 10. Long `rusqlite` Query In Async Handler

- **Input:** An async request or Tauri command executes a long synchronous query directly.
- **Investigate:** runtime workers, query duration, connection `Send` rules, concurrent requests, transaction owner, cancellation, and existing DB worker pattern.
- **Correct:** route work through the existing bounded blocking or serial DB owner while preserving connection and cancellation semantics.
- **Reject:** assuming an async wrapper makes SQLite nonblocking or spawning unlimited blocking jobs.
- **Acceptable scope:** handler/command adapter, database owner, queue/backpressure, tests, and docs.
- **Validation:** executor responsiveness, concurrency limit, result/error/cancel/shutdown tests, and representative query timing.
- **Final report:** blocking boundary, owner/thread model, queue policy, and runtime evidence.

### 11. Network Request Inside Transaction

- **Input:** A transaction remains open while calling an external service.
- **Investigate:** lock duration, writer contention, failure/retry/idempotency, data dependencies, and consistency invariant.
- **Correct:** fetch/compute outside, then validate and commit the minimal atomic database change; use an explicit workflow when compensation is required.
- **Reject:** longer busy timeout as the primary fix or blind retry of the whole workflow.
- **Acceptable scope:** workflow boundary, transaction, error mapping, tests, and architecture docs.
- **Validation:** external failure, stale precondition, rollback, busy contention, idempotency, and success tests.
- **Final report:** old/new transaction duration and consistency/retry behavior.

### 12. SQLx Versus `rusqlite`

- **Input:** A team proposes migration because SQLx is newer and async.
- **Investigate:** current runtime, connection/thread ownership, query checking, pooling/streaming needs, supported databases, linkage, migrations, binary/compile cost, and callers.
- **Correct:** retain or choose the crate that matches actual needs; isolate blocking SQLite correctly either way.
- **Reject:** framework fashion, universal performance claims, or repo-wide migration without evidence.
- **Acceptable scope:** a documented decision or narrowly proven adapter migration.
- **Validation:** supported build/features, critical queries, migrations, runtime responsiveness, binary/compile and performance comparison if migrating.
- **Final report:** criteria matrix, decision, migration cost, evidence, and unresolved gaps.

### 13. Unsafe Optimization Without Proof

- **Input:** Bounds checks are replaced with unchecked pointer access to speed a parser.
- **Investigate:** release CPU profile, benchmark, input trust, safety invariant, safe alternatives, panic paths, supported Miri/sanitizer tests, and portability.
- **Correct:** keep safe code unless the measured hot path, meaningful gain, invariant, and regression checks justify minimal unsafe.
- **Reject:** intuition, debug benchmarks, or a `SAFETY` comment that restates syntax.
- **Acceptable scope:** isolated hot function, safety wrapper, tests/benchmarks, and invariant docs.
- **Validation:** same-input benchmark, property/fuzz tests, Miri where supported, and target builds.
- **Final report:** baseline/gain, invariant, unsafe surface, validation limits, and fallback.

### 14. RSS Does Not Fall

- **Input:** Rust heap work completes but process RSS remains high.
- **Investigate:** heap allocations, retained capacity, live `Arc` owners, tasks, caches, mmap, native allocations, SQLite page cache, OS cache, and workload phases.
- **Correct:** classify the retained memory and fix only an owner/bound that violates requirements.
- **Reject:** claiming a leak from RSS alone or swapping allocators first.
- **Acceptable scope:** proven owner/cache/buffer/task and instrumentation.
- **Validation:** repeated workload with peak/steady/cleanup heap, RSS, mappings, and owner counts.
- **Final report:** classification, evidence, before/after plateau, and remaining native/OS uncertainty.

### 15. Giant Rust File

- **Input:** A module exceeds an arbitrary line threshold.
- **Investigate:** responsibilities, invariants, lifecycle, callers, change reasons, private coupling, test seams, and navigation cost.
- **Correct:** keep cohesive code or split at a stable ownership/API boundary.
- **Reject:** line-count-only crates/modules or forwarding shells.
- **Acceptable scope:** the proven boundary, imports/re-exports, tests, and architecture docs.
- **Validation:** repository format/check/test/docs plus stale-reference search.
- **Final report:** responsibility map, split/keep rationale, dependency changes, and residual complexity.

### 16. Code And Architecture Docs Drift

- **Input:** Documentation shows crates, commands, migrations, or ownership that code no longer has.
- **Investigate:** manifests, entry points, registration, runtime path, migrations, CI/deploy config, docs/indexes, and generated artifacts.
- **Correct:** choose the verified source of truth and update code/docs together, or report a blocker when intent is ambiguous.
- **Reject:** changing only prose or only code while leaving a contradictory source.
- **Acceptable scope:** affected architecture and lifecycle artifacts only.
- **Validation:** project gates, links/indexes, stale-name search, and runtime check when needed.
- **Final report:** mismatches, authoritative evidence, synchronized files, and `Not verified` runtime claims.

### 17. Migration Fails Mid-Upgrade

- **Input:** An application may stop during a destructive SQLite migration.
- **Investigate:** actual SQLite version, DDL transaction behavior, migration runner, backup, disk space, failure points, version markers, retry/restart, and supported source versions.
- **Correct:** make the upgrade atomic or resumable, preserve/verify backup, and define incompatible/corrupt recovery.
- **Reject:** testing fresh databases only or assuming rollback covers all external effects.
- **Acceptable scope:** migration, runner/recovery, representative fixtures, backup/restore docs, and tests.
- **Validation:** fresh install, each supported upgrade, injected failure/restart, data checks, integrity, and restore.
- **Final report:** upgrade matrix, failure points, recovery evidence, required space/time, and unsupported versions.

### 18. SQLite Runtime Is Too Old

- **Input:** A required SQLite feature or known data-integrity fix may be absent at runtime.
- **Investigate:** runtime version/compile options, bundled/system linkage, supported OS packages, wrapper requirements, WAL topology, packaging, and upgrade compatibility.
- **Correct:** enforce a verified minimum, bundle when appropriate for the application, or provide a compatible fallback and clear startup error.
- **Reject:** reading only crate version or enabling bundled linkage in a generic library without consumer impact review.
- **Acceptable scope:** dependency/features, startup capability check, packaging, tests, and deployment docs.
- **Validation:** supported and rejected runtime versions, feature path, packaging target, migration/backup compatibility.
- **Final report:** detected versions, linkage decision, affected feature/risk, and deployment evidence.

### 19. Query Performance Tested On Empty Database

- **Input:** A query/index change is declared faster using an empty or tiny database.
- **Investigate:** production-like row counts, distribution, selectivity, page/cache state, parameters, query plan, repetitions, variance, and write workload.
- **Correct:** seed or capture representative sanitized data and compare warm/cold behavior under the same release conditions.
- **Reject:** extrapolating empty-database timings or one run.
- **Acceptable scope:** fixture/generator, query/index change, benchmark, and documented workload.
- **Validation:** result correctness, plan, repeated read timing, write/storage cost, and migration time.
- **Final report:** dataset/cardinality, environment, variance, old/new plan and timing, and limits.

### 20. Opportunistic Refactor

- **Input:** While fixing one Rust/SQLite issue, the agent wants to rename crates and rewrite unrelated modules.
- **Investigate:** user scope, dirty-tree ownership, dependency necessity, contract impact, and separate follow-up value.
- **Correct:** exclude unrelated work, preserve existing changes, and record a separate recommendation if useful.
- **Reject:** drive-by cleanup, broad formatting, dependency churn, or architecture migration.
- **Acceptable scope:** files/hunks required for the requested behavior, tests, and corresponding docs.
- **Validation:** path-limited diff review, repository gates for changed surface, and stale-reference check.
- **Final report:** exact included/excluded scope, validation, and separate non-blocking recommendations.

### 21. Universal Baseline Conflicts With An Existing Project

- **Input:** An organization proposal mandates Rust 1.94, edition 2024, resolver 3, `apps/` plus `crates/`, and layered `domain/application/infrastructure/interface` directories for every repository.
- **Investigate:** pinned/current toolchain, MSRV consumers, manifest inheritance, edition/resolver, CI, crate ownership, deployment, existing architecture docs, change risk, and whether the proposal is adopted for new or established projects.
- **Correct:** keep portable governance, apply an adopted template to new projects, preserve justified legacy contracts, and migrate established repositories only at evidence-backed boundaries.
- **Reject:** treating a stale stable release, one directory tree, all-pedantic Clippy, or visual consistency as universal Rust requirements.
- **Acceptable scope:** baseline policy, one explicitly selected project/template, documented exceptions, CI checks, and directly affected docs.
- **Validation:** actual toolchain/MSRV and target matrix, member inheritance checks, repository commands, compatibility/build evidence, and stale-policy search.
- **Final report:** adopted/adapted/rejected rules, current-version evidence, project class, exceptions, migration cost, validation, and residual drift.

### 22. Move Or Delete A Crate

- **Input:** A crate or feature directory is moved or deleted after its implementation appears unused.
- **Investigate:** workspace members/default-members, path dependencies, module declarations, public re-exports, feature flags, commands/routes, configs, downstream callers, migrations/persisted data, tests/fixtures, generated files, packaging/deployment, docs, and indexes.
- **Correct:** reuse or remove only after tracing the complete lifecycle; preserve required historical migrations and provide explicit data/compatibility handling.
- **Reject:** filesystem-only move/delete, broad search-and-replace, deleting old migrations, or leaving stale registrations and docs.
- **Acceptable scope:** the structural unit and every proven dependent manifest, registration, test, migration, deployment, generated, and documentation artifact.
- **Validation:** repository format/check/test/build, feature/target matrix, package/runtime verification, generated-file refresh, migration upgrade/recovery when applicable, and stale-reference search.
- **Final report:** ownership decision, dependency chain, moved/deleted files, preserved compatibility paths, updated lifecycle artifacts, validation, and `Not verified` consumers.

## Quality Eval

Score common rows for every audit and profile rows only when that profile is
selected. Mark unselected rows `Out of scope`; they are not zeroes and do not
reduce the score.

| Case | Applies when | Pass evidence | Reject if |
| --- | --- | --- | --- |
| Grounding | Common | reads guidance/status, declares selected/excluded profiles, consumes `repo-map` when useful, and maps only the evidence needed for selected claims | starts from a universal template or inventories every domain by default |
| Priority | Common | resolves conflicts in the declared order | external repos override local contracts |
| Scope | Common | preserves unrelated dirty work and stops at selected-profile evidence | performs opportunistic refactors or partially audits excluded profiles |
| Validation | Common + selected profiles | runs real non-mutating repository commands and selected-profile runtime/data checks; records unavailable required evidence `Not verified` | invents commands, substitutes a weaker unrelated check, or equates unit tests with full proof |
| Reporting | Common | leads with outcome/findings and includes selected profiles, excluded profiles, exact evidence, `Not found`, and `Not verified` | reports unsupported success or adds empty all-domain sections |
| Read-only/Git boundary | Common | leaves worktree and Git/GitHub state unchanged; under `repo-review`, returns only the scoped specialist findings | edits files, stages, commits, comments, takes over review coordination, or invokes delivery without an explicit delivery request |
| Baseline | Architecture/baseline | classifies portable, organization, template, repository, and legacy rules; verifies applicable toolchain and inheritance | hard-codes a version snapshot or directory tree |
| Architecture | Architecture/baseline | assigns stable crate/module/domain/adapter owners and justifies traits/layers | splits by file count or adds ceremonial layers |
| Lifecycle | Architecture/baseline, or a selected structural claim | identifies applicable drift across manifests, registrations, migrations, tests, docs, indexes, and runbooks | requires every lifecycle surface when unrelated, or leaves known selected-scope drift unreported |
| Ownership | Ownership/errors | names creation/share/close/drop owners and bounded growth | flags syntax without lifecycle evidence |
| Errors | Ownership/errors | classifies failures and traces typed context, retry, logging, and boundary mapping | panics expected errors or stringifies everything |
| Concurrency | Concurrency/runtime | proves async need, blocking boundary, capacity, locks, timeout, cancellation, panic, and shutdown | unbounded work or hidden task lifecycle |
| Performance | Performance/memory | uses representative release baseline/profile/comparison and records trade-offs | intuition, one run, or debug-only claim |
| Memory | Performance/memory | distinguishes leak/live/cache/allocator/mmap/SQLite/OS causes | calls RSS a leak without evidence |
| SQLite | SQLite | verifies applicable runtime/linkage/connections/transactions/WAL/migrations/schema/plans/maintenance/recovery | guesses from SQL or crate version |
| Unsafe/FFI | Unsafe/FFI | states invariants, ownership, ABI, panic, cleanup, and supported relevant dynamic checks | treats unsafe alone as a vulnerability or claims unsupported dynamic proof |
| Combined interaction | Two or more selected profiles | preserves every selected profile's obligations and validates cross-boundary failure, cleanup, shutdown/restart, or recovery | lets one profile stand in for another or reports only isolated happy paths |

## Scoring

Minimum pass: trigger/non-trigger routing and every profile-selection case are
correct; every scenario includes all seven required fields; and every common,
selected-profile, and applicable Combined row scores at least 8. Record
unselected profile rows `Out of scope` and do not score them. Unavailable
required evidence may remain `Not verified` without failing scope discipline,
but claiming or fabricating a command result, benchmark, runtime version, query
plan, migration recovery, or safety proof is an automatic fail.
