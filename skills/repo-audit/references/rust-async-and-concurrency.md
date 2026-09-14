# Async And Concurrency

## Runtime Model

Record the runtime owner, flavor, worker and blocking limits, nested-runtime
behavior, sync/async entry points, background-task registry, panic policy,
shutdown signal, and process termination path. Do not introduce a runtime or
make APIs async until the I/O and caller model justify it.

## Blocking Work

- Treat synchronous SQLite, filesystem traversal, compression, native calls,
  and CPU-heavy loops as blocking until measured otherwise.
- Recommend moving blocking work away from async executor workers with the repository's
  existing dedicated thread, serial worker, `spawn_blocking`, or equivalent.
- Bound the number and queue of blocking jobs. `spawn_blocking` is not automatic
  backpressure, and already-running blocking closures may not be cancellable.
- Keep transaction ownership on the correct thread/connection and do not move a
  non-thread-safe handle merely to satisfy an async signature.

## Tasks And Cancellation

For every spawned task, establish a lifecycle and outcome policy proportional
to its responsibility:

- Is it joined, supervised, intentionally detached, or owned by another runtime
  boundary, and why is that policy safe?
- When correctness, durable work, resources, shutdown, or caller-visible
  outcomes depend on it, how are success, error, cancellation, and panic
  observed?
- How is cancellation requested, and where are cancellation points?
- Does cancellation leave partial files, transactions, native handles, or
  progress state?
- Does shutdown stop intake, signal work, wait for critical tasks, enforce a
  deadline, and report unfinished work?

Dropping a future is not a complete cancellation design when external side
effects or blocking work continue.

- For `tokio::select!`, identify which branches are cancellation-safe and what
  state is lost when another branch wins. Pin or retain in-progress work when
  restarting it would duplicate side effects, lose messages, or violate
  protocol state.
- Require owned joining, cancellation, and result/panic observation when the
  task affects correctness, durable work, resource lifetime, shutdown, or a
  caller-visible outcome. Distinguish successful output, task-returned error,
  cancellation, and panic.
- Intentional detachment is acceptable when work is bounded and non-critical,
  retains no uncontrolled resource, and failure is irrelevant or independently
  observable. Dropping a `JoinHandle` is supported Tokio behavior, not proof by
  itself that the task lifecycle is correct.
- Prefer the repository's established task set, tracker, supervisor, or other
  structured owner when those responsibilities require one. A specific
  `JoinSet`, `TaskTracker`, or cancellation-token crate is a conditional
  implementation choice, not a universal requirement.

## Channels, Locks, And State

- Prefer bounded channels with a capacity derived from item size, burst,
  consumer throughput, and acceptable latency.
- Define full-channel behavior: await, reject, coalesce, drop with metrics, or
  shed load. Never leave overload semantics implicit.
- Avoid unbounded task creation and unordered fan-out without a concurrency
  limit.
- Inspect locks held across `.await`, lock order, critical-section work,
  poisoning/panic behavior, fairness needs, and contention evidence.
- Choose `std::sync` primitives for short synchronous critical sections and
  async-aware primitives only when a guard must participate in async waiting.
  Follow the repository's established model.
- Define whether timeout covers one attempt, queue wait, or the whole operation.
  Make retries consume the overall deadline rather than multiplying it silently.

## Concurrency Verification

Use deterministic tests for state transitions, cancellation, channel closure,
shutdown, and panic propagation. Use stress tests for workload behavior. Use
Loom only for a small model whose synchronization operations are represented by
Loom types; record its state-space and unsupported behavior. A passing Loom
model does not prove hidden external synchronization correct.

Report task count, channel capacity, lock path, timeout/retry scope, cancellation
owner, shutdown evidence, and any behavior that remains `Not verified`.
