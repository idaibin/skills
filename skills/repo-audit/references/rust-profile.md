# Rust Profile

## Contents

- [Selection](#selection)
- [Audit Profiles](#audit-profiles)
- [Profile Selection Table](#profile-selection-table)
- [Conditional References](#conditional-references)
- [Modes](#modes)
- [Output Additions](#output-additions)
- [Routing Examples](#routing-examples)

Audit Rust engineering from repository evidence. Select only the audit
profiles required by the task; do not load architecture, performance, memory,
SQLite, concurrency, and FFI review into every audit.

## Selection

1. Inspect only relevant manifests, entry points, modules, docs, tests,
   benches, migrations, CI, and runtime configuration that apply to the task.
   When delegated, record the exact Rust paths or diff and keep the caller as
   review coordinator.
2. Determine workspace/crate boundaries, library and binary entries, feature
   flags, MSRV, edition, runtime/thread model, error/tracing style, database
   linkage, migration strategy, quality commands, and unsafe/FFI/native
   dependencies.
3. Select one or more audit profiles; explicitly mark the rest `Out of scope`.
4. Classify applicable standards as portable governance, organization
   baseline, new-project template, repository contract, or documented legacy
   exception. Never turn a version snapshot or example tree into a universal
   rule.
5. Map governing invariants, resource owners, shutdown/cancellation paths,
   error boundaries, workload, baseline, and validation gaps for the selected
   profiles only. When an in-scope selected-profile change adds, reuses,
   moves, renames, or deletes a structural surface, audit every affected
   manifest, registration, export, feature, test, migration, generated file,
   deployment path, architecture document, and index; search for stale
   references.

## Audit Profiles

- **Architecture/baseline:** crate/module/API ownership, dependencies,
  toolchain policy, structural lifecycle, docs, and legacy exceptions.
- **Ownership/errors:** resource lifetime, copying/retention, typed errors,
  panic/log/retry boundaries, and applicable Axum HTTP or Tauri IPC
  contracts.
- **Agent Runtime:** a stateful local-agent workflow, typed protocol/schema,
  durable operation history/recovery, approval/policy/sandbox enforcement, or
  Tauri/local app-server IPC. A Rust async crate, SQLite dependency, or
  Tauri directory alone does not activate this profile; load
  [agent runtime](rust-agent-runtime-profile.md) only for a reachable
  lifecycle or boundary.
- **Concurrency/runtime:** Tokio/blocking work, tasks, channels, locks,
  backpressure, cancellation, panic propagation, and shutdown.
- **Performance/memory:** representative workload, release baseline, CPU,
  allocation, RSS, I/O, binary/compile cost, caches, mmap,
  allocator/native/OS retention.
- **SQLite:** runtime/linkage, connections, transactions, WAL, migrations,
  schema, indexes, plans, maintenance, backup, and recovery.
- **Unsafe/FFI:** invariants, ABI/layout, pointer ownership, callbacks,
  threads, panic containment, alloc/free symmetry, and native cleanup.

## Profile Selection Table

| Request surface | Selected profiles | Explicitly out of scope unless requested |
| --- | --- | --- |
| crate/module ownership and toolchain baseline | Architecture/baseline | ownership, concurrency, performance, SQLite, unsafe/FFI |
| SQLite migration or query plan | SQLite; add Ownership/errors or Concurrency/runtime only when the transaction/runtime boundary is part of the claim | performance/memory and unsafe/FFI unless independently relevant |
| Tokio service using SQLite | Concurrency/runtime + SQLite; add Ownership/errors when resource/error lifetime is material | architecture, performance/memory, unsafe/FFI unless independently relevant |
| unsafe native adapter | Unsafe/FFI; add Ownership/errors, Target/platform evidence, or Performance/memory only when the request requires them | SQLite and unrelated workspace architecture |
| stateful local-agent workflow or agent IPC | Agent Runtime; add Concurrency/runtime, SQLite, Ownership/errors, or Target/platform only when the selected path reaches them | unrelated performance, FFI, or whole-workspace architecture |

Unavailable evidence does not trigger a broad fallback audit. Keep the
selected profile, mark the exact claim `Not verified`, and state what
evidence or tool is needed.

## Conditional References

Load each linked reference independently when its named surface applies;
grouping links does not require paired loading.

- Read [architecture](rust-architecture-and-modules.md) for structural
  boundaries and [baseline/lifecycle](rust-project-baseline-and-lifecycle.md)
  for baseline classification, legacy policy, reuse, and lifecycle.
- Read [ownership](rust-ownership-and-resources.md) for ownership, clone,
  `Arc`, buffers, and caches and [errors/API](rust-errors-and-api-design.md)
  for invariants, panic, retry, logging, and boundary translation.
- Read [web/desktop boundaries](rust-web-and-desktop-boundaries.md) for Axum
  extractors/state/middleware/response testing and Tauri command, capability,
  permission, CSP, path, and webview trust boundaries.
- Read [async/concurrency](rust-async-and-concurrency.md) for runtime,
  blocking work, tasks, channels, locks, timeouts, cancellation, shutdown,
  and Loom.
- Read [performance](rust-performance.md) for workloads, CPU, I/O,
  binary/compile cost, and measurement and [memory](rust-memory.md) for
  allocation, retention, RSS, caches, mmap, and leak classification.
- Read [SQLite](rust-sqlite.md) for linkage, connections, transactions, WAL,
  migrations, schema, indexes, plans, maintenance, backup, and recovery.
- Read [testing](rust-testing-and-quality.md) for Cargo, Clippy, Miri,
  coverage, benchmarks, and risk-based gates and
  [unsafe/security](rust-unsafe-and-security.md) for unsafe, FFI,
  native-resource, dependency, and security checks.
- Read [project grounding](project-grounding.md) when selected Rust evidence
  crosses reachable runtime/configuration, packaging, API, persistence,
  compatibility, security, deployment, or cross-repository boundaries;
  mark unrelated risk classes `Not applicable` and unexercised runtime claims
  `Not verified`.
- Read [checklist](rust-review-checklist.md) for profile-scoped gates and
  [anti-patterns](rust-anti-patterns.md) for detectable failure patterns.
  Consult [sources](rust-reference-corpus.md) for official source evidence,
  adopted rules, and rejected cargo-cult choices.
- Load [codebase design](codebase-design.md) only for a selected
  public-module, seam, abstraction, locality, or testability audit.

Do not substitute `cargo check` for release, benchmark, concurrency,
migration, or runtime evidence.

## Modes

- **Focused profile audit:** one or two selected risk surfaces with bounded
  evidence and commands.
- **Combined risk audit:** multiple interacting profiles, such as Tokio plus
  SQLite or unsafe plus performance, with explicit integration risks.
- **Baseline audit:** compare toolchain, workspace, directory, naming,
  validation, documentation, and legacy-exception policy against real project
  evidence.
- **Performance experiment review:** define workload, baseline, measurement,
  one-factor experiment, and comparable before/after evidence; route
  experiment edits to `dev-rust`.
- **Scoped specialist subreview:** inspect only the Rust paths or diff
  delegated by `repo-review`; return domain findings without taking review
  coordination or Git/GitHub ownership.

## Output Additions

Lead with capability `rust.surface.audit`, the inspection snapshot, and
selected profiles. Report project class; coordinating owner when this is a
scoped specialist subreview; guidance/manifests/code/migrations/docs/tests/
commands inspected; adopted, adapted, and rejected baseline rules; owners and invariants; structural lifecycle; workload and
before/after data where applicable; explicitly excluded profiles; and `Not
found` or `Not verified` gaps. Lead with findings ordered by impact. Never
claim a benchmark, migration path, runtime version, release build, Miri/Loom
run, or recovery test that was not actually executed.

## Routing Examples

- Use `repo-map` first when the task is only repository orientation or when
  no Rust target is known.
- Use `dev-rust` for a change whose module, contracts, and validation are
  already established.
- Use `repo-review` for authentication, authorization, token, or input risks
  on a fixed Worktree or immutable change basis; use this profile for the
  same Rust concerns when no change basis exists.
- Use `repo-review` for local dirty-tree review, full-diff completeness,
  staging plans, and commit grouping. It may delegate a bounded changed Rust
  surface here for a read-only specialist subreview; the audit returns
  findings and does not stage or commit.
