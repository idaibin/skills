# Performance

## Required Method

```text
define workload
→ establish baseline
→ profile
→ identify hot path
→ define a one-factor experiment
→ route code/config changes to dev-rust
→ verify comparable rerun evidence
→ record trade-offs
```

Before requesting an experiment, record representative input size and shape, machine and
OS, Rust/toolchain, feature set, build profile, warm/cold cache state,
concurrency, repetitions, variance, and metric. Separate debug behavior from
release behavior.

## Measurement Surface

Choose only metrics relevant to the claim:

- end-to-end latency, throughput, tail latency, and cold start
- CPU samples, instructions, syscalls, blocking time, and lock contention
- allocation count/bytes, peak and steady RSS, retained memory, and task count
- file/network bytes, query count, fsync/checkpoint behavior, and temporary I/O
- binary size, link time, clean/incremental compile time, and feature cost

Prefer production-like workloads. Microbenchmarks can isolate a mechanism but
must not replace an end-to-end comparison when the user-facing claim is broader.

## Profiling Decisions

- Use a platform-appropriate profiler already supported by the repository or
  environment. Capture the command, profile/build settings, and raw artifact.
- Recommend release debug line tables or frame pointers only when needed for
  profiling; route configuration edits to `dev-rust` and keep them scoped.
- Use allocation profiling before rewriting clones, collections, buffers, or
  allocators. Report allocation rate and call path, not just a source count.
- Measure I/O and syscalls before introducing buffering, mmap, caching, or
  parallelism.
- Measure contention before replacing a lock or sharding state.
- Measure clean and incremental builds before changing workspace boundaries,
  feature sets, generics, codegen units, LTO, or proc-macro use.

## Optimization Gate

Do not introduce these without a measured hot path, a same-workload comparison,
and regression coverage:

- `#[inline]` or `#[inline(always)]`
- unsafe indexing or pointer code
- SIMD or architecture-specific implementations
- custom allocators or object pools
- mmap, `SmallVec`, string interning, custom caches
- parallel iterators, extra threads, or larger runtime pools

When an implemented optimization is audited, report the baseline, new result,
variance, resource trade-offs, binary/compile impact, portability constraints,
and the benchmark or test that prevents regression. Reject unsupported proposals;
route any requested implementation or revert to `dev-rust`.

## Common Misreadings

- Faster debug execution does not prove release improvement.
- One run does not establish a baseline.
- An isolated nanosecond gain does not prove end-to-end impact.
- Fewer allocations can still be slower or use more retained memory.
- More threads can reduce throughput through contention or I/O saturation.
- A smaller binary can start slower, and LTO can increase build cost.
- A full table scan can be correct for a tiny table or broad result set; combine
  query plan, representative cardinality, and measured latency.
