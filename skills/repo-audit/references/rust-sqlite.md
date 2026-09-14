# SQLite

## Contents

- [Runtime And Connection Evidence](#runtime-and-connection-evidence)
- [Transactions And Writers](#transactions-and-writers)
- [WAL](#wal)
- [Schema And Indexes](#schema-and-indexes)
- [Migrations](#migrations)
- [Space And Maintenance](#space-and-maintenance)
- [`rusqlite` Versus SQLx](#rusqlite-versus-sqlx)

## Runtime And Connection Evidence

Inspect and report:

- actual runtime SQLite version and compile options
- bundled, system, or other linkage and the deployment consequences
- `rusqlite`, SQLx, raw FFI, or another wrapper and enabled features
- connection count, thread ownership, pooling or serial worker model
- `busy_timeout` or busy handler, foreign-key enforcement, journal mode,
  synchronous level, cache and mmap settings, and connection initialization
- async-runtime interaction and where blocking SQLite calls execute

Do not infer runtime version from a Cargo dependency alone.

## Transactions And Writers

- Group related or bulk writes in a transaction; compare against per-row commits.
- Keep transactions short and local. Exclude network calls, user interaction,
  long CPU work, and unrelated file I/O.
- Close row iterators, statements, and read transactions promptly so checkpoints,
  schema changes, and writers are not held back.
- Define rollback and error propagation for every failure path.
- Coordinate the single SQLite writer through the existing connection, pool, or
  worker model. WAL improves reader/writer concurrency but does not create
  multiple simultaneous writers.
- Handle `SQLITE_BUSY`/locked outcomes with bounded timeout or retry plus
  idempotency. Do not spin or retry an entire non-idempotent workflow blindly.

## WAL

Before enabling or changing WAL, inspect deployment filesystem, connection
topology, backup process, shutdown, and SQLite runtime support.

Review:

- automatic checkpoint configuration and whether it was disabled
- long-lived readers and checkpoint starvation
- large write transactions and expected WAL growth
- manual checkpoint owner, mode, latency, and reader impact
- `journal_size_limit`, restart/truncate behavior, and observability
- backup/recovery handling for the database, `-wal`, and `-shm` state
- whether the database is on a network filesystem or copied while active

Never delete `-wal` or `-shm` manually. Verify current SQLite release guidance
and known WAL issues against the actual runtime when data integrity matters.

## Schema And Indexes

Inspect migrations and the resulting schema for:

- primary keys, stable identifiers, unique constraints, and foreign keys
- cascade/restrict behavior and foreign-key enforcement on every connection
- column affinity, NULL semantics, defaults, checks, and timestamp/text encoding
- index prefix order matching equality, range, join, ordering, and grouping use
- duplicate or prefix-redundant indexes and write amplification
- covering and partial indexes only where workload and maintenance justify them
- FTS5 only for a real full-text workload and supported deployment

Do not create one index per filtered field. For each critical query, use
representative cardinality and parameters, current statistics, measured timing,
and:

```sql
EXPLAIN QUERY PLAN ...
```

Interpret `SCAN`, `SEARCH`, covering indexes, join nesting, and temporary
B-trees in context. Do not parse or persist the human-oriented plan format as a
stable application API.

## Migrations

- Keep migrations ordered, atomic where SQLite permits, and compatible with the
  application's supported upgrade paths.
- Test fresh install, supported upgrades with representative data, failure or
  interruption, restart/retry, and incompatible or corrupt-state handling.
- Define backup, restore, and version checks before destructive transforms.
- Avoid assuming every DDL operation has the same rollback behavior across the
  actual SQLite versions you support.
- Refresh statistics or run repository-approved optimization after schema/data
  changes when evidence requires it.

## Space And Maintenance

- Compare `page_count`, `freelist_count`, file sizes, WAL size, and workload
  before diagnosing space growth.
- Understand that deletion usually adds reusable pages to the freelist without
  shrinking the file.
- Use `PRAGMA optimize` according to current official guidance and connection
  lifetime; verify the actual application version and policy.
- Do not default to `auto_vacuum=FULL`; it changes write behavior and can
  increase fragmentation. Evaluate incremental mode only with a lifecycle plan.
- Run `VACUUM` only after estimating temporary free-space needs, outage/locking,
  I/O cost, rowid implications, and benefit. It can require substantial extra
  disk space.
- Verify backup restoration and an appropriate integrity check; a backup file's
  existence is not recovery proof.

## `rusqlite` Versus SQLx

Prefer evaluating `rusqlite` for a local single-process CLI or desktop app that
directly controls connection and transaction lifetime. Evaluate SQLx when the
project already uses async database abstractions, needs its compile-time query
workflow, pooling, streaming, or a shared multi-database toolchain.

Do not migrate because SQLx appears newer, or reject `rusqlite` because it is
synchronous. Choose from runtime, blocking boundary, connection/thread model,
transaction semantics, query tooling, binary/native linkage, and deployment.
