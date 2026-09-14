# Architecture And Modules

## Investigation

Before proposing files or crates, inspect:

- root and member `Cargo.toml`, `Cargo.lock`, `.cargo/config.toml`,
  `rust-toolchain*`, formatter and lint configuration
- workspace members, default members, resolver, shared dependencies, profiles,
  features, targets, examples, benches, build scripts, and native dependencies
- `src/lib.rs`, every relevant `src/main.rs`, Tauri command registration,
  service startup, configuration, shutdown, and public re-exports
- the nearest analogous module, API, trait, database adapter, test, benchmark,
  architecture document, and downstream caller
- CI commands and supported platforms, including MSRV and feature combinations

Mark missing evidence `Not found` and unchecked areas `Not verified`.

## Boundary Decisions

- Split a crate when responsibility, release/deployment, feature isolation,
  compile-time cost, platform boundary, or independent reuse is stable enough to
  justify a public dependency edge.
- Keep code in a module when it shares lifecycle, invariants, deployment, and
  change reasons with its current crate.
- Keep a binary entry point thin: parse configuration or CLI inputs, assemble
  dependencies, start the runtime, map terminal errors, and coordinate shutdown.
- Keep domain behavior independent of CLI arguments, HTTP extractors, Tauri
  transport DTOs, SQL rows, and concrete persistence clients.
- Put adapters at boundaries. Convert transport and storage representations into
  domain types once, and keep dependency direction toward stable policy.
- Introduce a trait only for a real alternate implementation, stable test seam,
  plugin boundary, or public polymorphic contract. Prefer a concrete type for a
  single implementation.
- Promote a type to a common crate only after multiple crates share a stable
  invariant. Shared location alone is not a reason.
- Use semantic enums or configuration types instead of boolean parameters when
  call sites otherwise hide meaning or invalid combinations.

## Project-Class Notes

- **CLI or single binary:** prefer direct composition, bounded background work,
  explicit exit mapping, and minimal dependency surface.
- **Library:** protect semver, public invariants, feature behavior, MSRV, docs,
  and downstream implementors. Avoid process exits and runtime ownership.
- **Tokio service:** make runtime, task supervision, cancellation, backpressure,
  and graceful shutdown visible in the architecture.
- **Tauri backend:** keep commands thin and transport-safe; place long-running
  work, database policy, and business invariants in Rust owners below commands.
- **SQLite-first local app:** keep the connection and writer model explicit.
  Prefer a simple local design over a server-style abstraction stack.

## Reject

- a crate per directory or large file
- one repository/service/manager per struct
- common crates that collect unrelated types
- circular dependencies or forwarding-only shell crates
- global runtimes or pools hidden behind convenience functions
- copying a reference repository's workspace shape without a matching need

When structure changes, update crate maps, dependency diagrams, public API docs,
feature documentation, command registration, packaging, and architecture indexes.
