# Testing And Quality

Apply the common repository gates plus only the rows required by selected audit
profiles. A Focused audit does not inherit every command in this file. Mark an
unselected profile `Out of scope`; when selected-profile evidence is required
but its tool, target, runtime, or dataset is unavailable, mark that claim
`Not verified` rather than substituting another command.

## Choose Gates From The Repository

Read `justfile`, task runner, Cargo aliases, CI, contributor docs, manifests, and
toolchain files before running commands. Use existing command order and feature
matrices. Do not assume optional tools are installed.

Common candidates, only when repository-defined or otherwise supported and
relevant to the selected profiles:

```bash
cargo fmt --all --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo test --workspace --doc
cargo build --workspace --release
```

Use compiler and Clippy output as typed evidence, not a universal design
verdict. Distinguish correctness and suspicious lints from style, complexity,
performance, pedantic, nursery, cargo, and restriction groups. Do not enable the
entire restriction group; apply individual lints only with repository-owned
rationale. Before accepting an unused/dead-code conclusion, resolve public API,
features, targets, `cfg`, macros, derives, generated code, build scripts,
examples/benches, FFI exports, and known downstream consumers.

Additional project-supported gates may include, only for selected claims:

```bash
cargo nextest run --workspace --all-features
cargo audit
cargo deny check
cargo +nightly miri test
cargo llvm-cov
cargo bench
```

Record missing tools or unsupported targets as `Not found` or `Not verified`;
do not replace them silently.

## Risk-Based Validation

| Change | Minimum evidence beyond local unit tests |
| --- | --- |
| public API or feature | downstream/example compile, docs, feature matrix, compatibility check |
| CLI behavior | integration test for args, exit code, stdout/stderr, files and signals |
| async/task lifecycle | cancellation, panic, channel close, overload, timeout and shutdown tests |
| lock/atomic state | focused state-machine tests; Loom model when justified and supported |
| performance | representative before/after benchmark and profile evidence |
| memory | peak/steady/cleanup comparison with owner evidence |
| migration/schema | fresh DB, supported upgrades, failure/retry, representative data, backup restore |
| critical SQLite query | `EXPLAIN QUERY PLAN`, cardinality-aware timing, result correctness |
| unsafe/FFI | safety-invariant tests, Miri where supported, boundary/cleanup/panic checks |
| native/platform | supported target build and real runtime evidence |

## Test Design

- Prefer the nearest established integration or snapshot pattern for externally
  visible behavior; use unit tests for pure invariants and state transitions.
- Test failures and cleanup, not only success.
- Keep concurrency tests deterministic where possible. Stress tests complement
  but do not replace modeled state transitions.
- Use representative database sizes and distributions. Empty or tiny databases
  do not validate production query plans or migration cost.
- Benchmark release-equivalent code with stable inputs, warm/cold policy,
  repetitions, and variance. Do not report one run as improvement.
- Verify rustdoc and doc tests for public APIs when the repository treats them as
  contracts.

## Interpretation

- `cargo fmt` proves formatting only.
- `cargo check` does not prove a release binary links or runs.
- unit tests do not prove concurrency interleavings, resource cleanup,
  performance, migration recovery, or SQLite runtime behavior.
- Clippy warnings require context; repository lint policy wins, and explicit
  suppression needs a narrow reason.
- Miri does not support all FFI, OS, network, or concurrency behavior.
- A passing Loom model covers only represented operations and explored state.
- `cargo audit` reports known advisories in its database; it is not a complete
  dependency or application security review.

Report every command exactly, its result, relevant feature/profile/target, and
what it did not verify.
