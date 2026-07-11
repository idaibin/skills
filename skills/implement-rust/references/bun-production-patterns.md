# Bun-Derived Production Rust Patterns

This reference records transferable lessons from Bun's Rust rewrite. It is
evidence, not a template: repository guidance and the local risk model still
decide which practices apply.

## Source Basis

Reviewed on 2026-07-10:

- Bun's official article, [Rewriting Bun in Rust](https://bun.com/blog/bun-in-rust).
- `oven-sh/bun` at commit
  [`90f8746301cc3ee56f7484bf9a8d40dd4aa0d715`](https://github.com/oven-sh/bun/tree/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715).
- Workspace policy and release profiles in
  [`Cargo.toml`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/Cargo.toml).
- Project-specific prohibited APIs in
  [`clippy.toml`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/clippy.toml).
- Raw-pointer abstraction and safety contracts in
  [`src/ptr/lib.rs`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/src/ptr/lib.rs).
- Resource cleanup in
  [`src/sourcemap/ParsedSourceMap.rs`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/src/sourcemap/ParsedSourceMap.rs).
- FFI layout and safe wrappers in
  [`src/uws_sys/lib.rs`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/src/uws_sys/lib.rs).
- Generated host-function glue in
  [`src/jsc_macros/lib.rs`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/src/jsc_macros/lib.rs).
- Rust validation entry points in
  [`package.json`](https://github.com/oven-sh/bun/blob/90f8746301cc3ee56f7484bf9a8d40dd4aa0d715/package.json).

The porting and lifetime guides discussed in the article were not present in
that checked-out commit. Do not claim their current repository contents without
new evidence.

## What Transfers

### 1. Make Ownership Executable

Bun's stated reason for the rewrite was recurring use-after-free, double-free,
and missed cleanup paths. The code uses `Drop`, owning containers, reference
counting, and narrow raw-pointer wrappers so cleanup and lifetime assumptions
are attached to types rather than repeated at every call site.

Apply this as follows:

- name the owner of every allocation, handle, callback context, and reference;
- encode routine cleanup in RAII/`Drop` guards;
- keep ownership transfer explicit and one-way;
- test success, error, cancellation, re-entry, and final-callback cleanup paths;
- use leak tooling for resources Rust cannot fully observe.

`Drop` is not enough when ownership depends on a flag or a foreign callback.
Document that state transition and verify the resource is reclaimed exactly
once.

### 2. Make Unsafe Small, Greppable, And Reviewable

Bun's workspace denies undocumented unsafe blocks and several pointer, leak,
alignment, and uninitialized-memory lints. The code commonly places one foreign
call or dereference in a small `unsafe` block with an adjacent `SAFETY` comment,
then exposes a safe wrapper tied to slices, references, `NonNull`, or an owner.

For each unsafe boundary, review:

- pointer source, nullability, alignment, provenance, and initialized length;
- pointee lifetime and address stability;
- shared versus exclusive aliasing, including re-entrant callbacks;
- thread affinity and `Send`/`Sync` behavior;
- foreign layout, discriminants, calling convention, and panic policy;
- allocator identity and the matching destructor/free function.

Do not use an arbitrary zero-unsafe target for systems that must call native
libraries. Reduce open-coded unsafe and grow audited safe adapters instead.

### 3. Treat FFI As A Public Contract

The Bun sources use explicit layout representations, opaque handles, byte-slice
wrappers, generated shims, and platform-specific ABI handling. A notable pattern
models foreign values that may contain unknown integers as transparent newtypes
rather than exhaustive Rust enums, avoiding invalid discriminants.

An FFI change is incomplete until both sides agree on:

- symbol and calling convention;
- field order, size, alignment, integer width, and enum openness;
- nullable and borrowed versus owned values;
- allocation/free symmetry and callback lifecycle;
- error and panic conversion;
- platform/architecture variations;
- generated declarations and cross-language tests.

### 4. Separate Parity From Cleanup

Bun deliberately performed a mechanical translation that preserved its existing
architecture and test surface, planning idiomatic cleanup and unsafe reduction
after compatibility. That separation is broadly useful even when migration is
incremental: first preserve behavior, then refactor with a green baseline.

Before scaling a port:

1. map source types, pointers, cleanup, errors, and special language semantics;
2. inventory complex field lifetimes and callback ownership;
3. port a small representative slice;
4. compare old and new behavior through the same external tests;
5. review differences independently from the implementer context;
6. only then widen the batch.

Compilation does not prove parity. Reject stubs, placeholder constants, skipped
tests, or broad comments that merely justify a workaround.

### 5. Review Cross-Language Semantic Traps

The Bun article documents regressions that compiled successfully but changed
behavior. Turn those into explicit checks:

- never hide required mutation or IO inside `debug_assert!`;
- distinguish eager `unwrap_or` from lazy `unwrap_or_else`;
- specify rounding and negative-value behavior for numeric conversion;
- decide what happens to odd-length, misaligned, truncated, or trailing input;
- compare bounds-check and overflow behavior in debug and release builds;
- preserve destructor order and asynchronous callback ownership;
- treat re-entry as an aliasing and lifetime event, not only a control-flow event.

### 6. Build A Risk-Layered Validation Ladder

Bun exposes repository commands for workspace checking, Clippy, cross-target
checking, and Miri, then supplements them with sanitizers, leak tests, stress
tests, fuzzing, platform CI, and end-to-end compatibility tests.

Select gates from Baseline plus every applicable risk overlay. Within the
selected overlays, order feedback from fast and focused to expensive and broad:

1. format and focused static checks for fast feedback;
2. focused unit and contract tests;
3. link and smoke the real binary or library boundary;
4. release-mode tests where assertions, overflow, layout, or performance differ;
5. supported target/feature builds for gated code;
6. Miri for supported unsafe-sensitive crates;
7. ASAN/LSAN or equivalent for FFI and allocator/resource lifetimes;
8. fuzzing for parsers, protocols, decoders, and adversarial bytes;
9. stress and repeated-operation tests for races, resource limits, and leaks;
10. full cross-platform behavior suite with proof that tests were not skipped.

Use the repository's own commands. Miri, sanitizers, fuzzing, stress, leak, and
repeated-operation gates apply only when supported and relevant to a selected
overlay. Record unavailable required evidence as `Not verified`; do not make a
target-only change inherit unrelated native or stress tooling.

### 7. Enforce Local Architecture With Tooling

Bun's lint configuration goes beyond generic Clippy by prohibiting APIs and
types that bypass project-owned filesystem, threading, collection, allocation,
and output abstractions. The transferable rule is not Bun's exact deny list.
It is to encode stable project invariants in workspace lints or checks so review
does not rely on memory alone.

Add a custom restriction only when:

- the approved replacement is real and documented;
- the rule applies consistently across the owning scope;
- exceptions can be narrow and justified;
- CI runs the check;
- the restriction does not force a dependency cycle or unsuitable abstraction.

## What Does Not Transfer Automatically

- Bun's pinned nightly toolchain, allocator choices, panic-abort policy, crate
  count, cross-language LTO flags, and disallowed APIs are product decisions.
- Bun's all-at-once rewrite depended on a stable language-independent suite with
  roughly a million assertions, broad platform coverage, a mechanical mapping,
  and unusually high execution capacity. Default to incremental migration when
  those preconditions are absent.
- More crates do not automatically mean better architecture or faster builds.
  Split only along stable ownership and dependency directions, and check for
  cycles and build-time impact.
- Unsafe density is a trend and review aid, not a quality score. Soundness
  depends on invariants and testing, not the raw keyword count.
- Performance claims require representative release benchmarks on the target
  hardware. Do not infer gains from the language choice or LTO setting alone.
