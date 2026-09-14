# Memory

## Classification First

Do not call rising or non-returning RSS a leak until evidence distinguishes:

| Observation | Possible cause | Evidence to collect |
| --- | --- | --- |
| allocations remain unreachable | true leak or forgotten native allocation | allocation/lifetime profiler, Miri where supported, native ownership trace |
| objects remain reachable | live owner, task, subscription, `Arc`, cache | retention graph, strong counts, owner/task lifecycle |
| heap use falls but RSS stays high | allocator arenas or retained capacity | heap profile versus RSS, allocator stats, repeated workload plateau |
| address space or RSS tracks files | mmap or OS file cache | mapping list, file sizes, resident pages, drop/unmap behavior |
| database activity raises memory | SQLite page cache, prepared statements, rows | connection/cache settings, statement lifecycle, page/cache metrics |
| search/index memory persists | reader/writer generations or segment caches | reader/writer handles, reload/merge lifecycle, mapped files |

Without this evidence, write `memory growth observed; cause Not verified`.

## Review Checklist

- unbounded `Vec`, `HashMap`, queues, channels, caches, task registries, or
  per-key state
- large object or backing-buffer clones in repeated paths
- `collect` before another full iteration or sort when streaming is sufficient
- whole-file reads and full-row query materialization
- repeated `String`, `Vec`, serialization, and temporary-buffer allocation
- large enums/structs copied at high frequency
- rare large inputs leaving excessive retained capacity
- `Arc` ownership chains, cycles, subscriptions, callbacks, and task handles
- tasks or workers that never terminate or drain
- mmap and native-library allocations outside the Rust allocator
- SQLite page/statement cache and long-lived connections
- search-index reader/writer generations and merge buffers

## Measurement Plan

1. Define a workload with input size, duration, concurrency, and steady-state
   expectation.
2. Capture process RSS, heap allocations, mapped memory, task/thread count, open
   files, and application cache sizes over time.
3. Separate startup, warm-up, active workload, idle, cleanup, and shutdown.
4. Correlate retained objects with an owner and lifecycle event.
5. Define one owner, bound, or allocation-path experiment and route requested
   code or configuration changes to `dev-rust`.
6. Verify a rerun under the same conditions and compare peak, steady state,
   cleanup, and performance cost.

## Corrective Choices

- Recommend explicit capacity/TTL/eviction and observability for unbounded caches.
- Bound channels and producers; define overload behavior.
- Stream, paginate, or batch large data when full materialization is unnecessary.
- Reuse buffers only for measured hot allocation sites; shrink or replace
  buffers after exceptional inputs when retention matters.
- Break `Arc` cycles and give subscriptions/tasks an explicit close path.
- Close statements, rows, transactions, readers, and writers at the narrowest
  correct scope.
- Preserve mmap and cache behavior when it improves I/O and the reported RSS is
  explainable; do not optimize the metric at the expense of real performance.
