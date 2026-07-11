# Usage

## Trigger Examples

- `Audit crate ownership for a local-first CLI and Tauri backend without imposing empty layers.`
- `Compare our Rust toolchain and directory baseline with this existing repository without forcing a migration.`
- `Audit our crate move/delete lifecycle policy across manifests, registrations, tests, migrations, deployment paths, and docs; there is no current Git change set.`
- `Audit this Tokio service for unbounded tasks, channels, locks, cancellation, panic propagation, and shutdown.`
- `Profile this Rust hot path and prove whether clones, allocations, mmap, or a custom allocator matter.`
- `Review SQLite migrations, WAL growth, query plans, indexes, backup, and recovery in this desktop app.`
- `Check unsafe FFI ownership and run the supported Rust quality gates.`
- `Compare rusqlite and SQLx for this existing runtime and deployment model.`
- `Verify Rust architecture docs against crates, commands, migrations, and real code.`
- `As the code-review Rust specialist, inspect only the changed Tokio and SQLite surface; return findings without staging or committing.`

## Routing Examples

- Use `code-context` first when the task is only repository orientation or when
  no Rust target is known.
- Use `implement-rust` for a change whose module,
  contracts, and validation are already established.
- Use `diagnose` when the root cause of a failure or regression is unknown.
- Use `code-security` for a security-only audit after the relevant Rust boundary
  is mapped.
- Use `code-review` for dirty-tree review, full-diff and contract-chain
  completeness, staging plans, and commit grouping. It may delegate a bounded changed
  Rust surface to `audit-rust` for a read-only specialist subreview; the audit
  returns findings and does not stage or commit.
- Use `code-delivery` only when the user explicitly requests commit, push,
  squash, branch cleanup, or remote proof. An existing diff does not by itself
  authorize or require delivery.

## Profile Selection

Every audit runs the common grounding, scope, read-only, evidence, and reporting
gates. Select only the domain profiles needed by the request:

| Request surface | Selected profiles | Explicitly out of scope unless requested |
| --- | --- | --- |
| crate/module ownership and toolchain baseline | Architecture/baseline | ownership, concurrency, performance, SQLite, unsafe/FFI |
| SQLite migration or query plan | SQLite; add Ownership/errors or Concurrency/runtime only when the transaction/runtime boundary is part of the claim | performance/memory and unsafe/FFI unless independently relevant |
| Tokio service using SQLite | Concurrency/runtime + SQLite; add Ownership/errors when resource/error lifetime is material | architecture, performance/memory, unsafe/FFI unless independently relevant |
| unsafe native adapter | Unsafe/FFI; add Ownership/errors, Target/platform evidence, or Performance/memory only when the request requires them | SQLite and unrelated workspace architecture |

Unavailable evidence does not trigger a broad fallback audit. Keep the selected
profile, mark the exact claim `Not verified`, and state what evidence or tool is
needed. Mark every unselected profile `Out of scope`.

## Expected Investigation Summary

```text
Audit mode and coordinating owner:
Selected profiles:
Excluded profiles (Out of scope):
Project class:
Repository guidance and status:
Applicable baseline class and legacy exceptions:
Existing analogous code and reuse candidates:
Structural lifecycle dependencies:
Tests, benchmarks, CI, and docs:
Selected-profile evidence only:
Unavailable required evidence (Not verified):
```

## Expected Final Report

```text
Decision, selected profiles, and scope:
Coordinating owner for a specialist subreview:
Adopted, adapted, and rejected baseline rules:
Owners and invariants:
Add/reuse/move/rename/delete lifecycle updates:
Findings with impact and location:
Selected-profile evidence and validation:
Excluded profiles: Out of scope
Not found / Not verified required evidence:
Residual risks:
```

Lead with findings ordered by impact. Never claim a benchmark,
migration path, runtime version, release build, Miri/Loom run, or recovery test
that was not actually executed. Do not include empty all-domain sections merely
to make a focused report look complete.
