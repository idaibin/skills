# Ownership And Resources

## Ownership Review

For each changed path, identify who creates, shares, mutates, closes, waits for,
and drops the resource. Cover files, sockets, native handles, mmap regions,
SQLite connections, transactions, statements, row iterators, tasks, channels,
subscriptions, locks, caches, buffers, and index readers or writers.

Use these questions:

- Can the value remain owned or borrowed locally?
- Is shared ownership real, or is `Arc` hiding an unclear owner?
- Does a clone copy bytes, increment a reference count, or retain a much larger
  backing allocation?
- Does a guard, statement, rows iterator, or read transaction live longer than
  intended?
- Can the background task terminate on success, failure, cancellation, and
  shutdown? Who awaits it and observes panic?
- Are channel capacity, cache size/TTL/eviction, buffer growth, and input size
  bounded?
- Is cleanup automatic and sufficient, or is a fallible explicit `close`,
  `flush`, `commit`, or `shutdown` path required?

## Clone And Allocation Findings

Do not flag a clone from syntax alone. Record:

1. cloned type and approximate payload or retained backing allocation
2. call frequency and representative workload
3. whether the call is on a measured hot or memory-retaining path
4. allocation/copy/reference-count behavior
5. before/after time, allocation, or RSS impact if changed
6. readability and lifetime complexity introduced by removal

Prefer the simpler clone when its measured cost is irrelevant. Do not replace a
clear owned design with fragile lifetimes merely to eliminate cloning.

## `Arc`, Locks, Channels, And Caches

- Use `Arc` only for shared ownership across tasks, threads, callbacks, or
  long-lived handles. Document what ends the shared lifetime.
- Avoid one `Arc<Mutex<HashMap<...>>>` conclusion for every workload. First
  measure contention and inspect access patterns, consistency needs, mutation
  frequency, and sharding or actor alternatives.
- Use bounded channels by default for producer/consumer work. If an unbounded
  channel is intentional, prove the producer rate, consumer capacity, memory
  ceiling, overload behavior, and shutdown drain policy.
- Keep locks out of slow I/O and `.await` regions unless the protected invariant
  requires it and deadlock/contention evidence is addressed.
- Give caches ownership, key/value cost, maximum size, TTL or eviction policy,
  invalidation behavior, observability, and shutdown semantics.

## Large Data And Buffers

- Stream, page, or batch large files, query results, network bodies, and index
  work when the full dataset is not required at once.
- Avoid `collect` followed immediately by another full traversal when an
  iterator or bounded batch preserves behavior.
- Reuse buffers only after allocation profiling shows value. Clear retained
  capacity when a rare large input would otherwise pin memory.
- Treat mmap as an ownership and OS-cache choice, not zero-memory I/O. Record
  file lifetime, mutation/truncation safety, address-space cost, and platform
  behavior.

## Evidence Contract

A finding must identify the owner, lifetime defect, workload, impact, code
location, bounded fix, and validation. Otherwise label it a hypothesis or
`Not verified`.
