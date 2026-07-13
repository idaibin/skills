# Rust Implementation Usage

## Summary

Use `implement-rust` after repository context is known and the task needs
Rust code, Cargo, crate, module, test, or toolchain work. It preserves the real
project class and repository standard instead of forcing one layout everywhere.

## Best For

- Implementing or refactoring a Rust feature, service, CLI, library, or Tauri backend.
- Aligning Cargo workspace membership, crate ownership, or module boundaries.
- Self-checking edited error handling, async behavior, persistence layering, or shared extraction.
- Applying an explicit repository Rust standard with matching docs and commands.
- Removing a Rust module or crate and closing every manifest, export, test, and doc reference.
- Adding a Rust endpoint or public interface only after tracing and reusing the existing contract chain.
- Applying idiomatic Rust ownership, errors, tests, rustdoc, dispatch, performance, and concurrency practices.
- Porting a native component to Rust while preserving behavior and making
  lifetime, cleanup, FFI, and release/platform semantics explicit.
- Implementing changes around `unsafe`, raw pointers, native handles, callbacks,
  ABI layout, or cross-language generated bindings.

## Trigger Examples

- `Implement this Axum feature using the repository's handler/service/repo pattern.`
- `Add a crate to this workspace and update every required manifest and check.`
- `Refactor this Rust module without changing the public API.`
- `Refactor this Tauri command boundary and keep business logic in the core crate.`
- `Remove this unused crate and update workspace membership, docs, and CI.`
- `Align this repository to its documented Rust toolchain and Clippy standard.`
- `Before adding this endpoint, inspect the existing docs, route, handler, service, repo, DTOs, errors, callers, and tests.`
- `Extend the nearest existing trait or interface if it can own this behavior; justify any new public API.`
- `Port this C++ or Zig module to Rust, preserve the existing behavior suite, and review lifetime and semantic differences before cleanup.`
- `Fix this Rust/C FFI boundary while preserving layout, ownership, callbacks, panic behavior, and unsafe containment.`
- `Update this Windows-only adapter and verify the supported target without running unrelated native stress tools.`
- `Change the SQLite-backed FFI import path and combine database recovery with native ownership validation.`

## Non-Triggers

- Repository orientation before the Rust surface is known; use `repo-map`.
- Planning a cross-repository migration before implementation; use `code-planner`.
- Diagnosing an unknown failing test or performance regression; use `diagnose`.
- Reviewing staged ownership or producing commit groups; use `repo-review`. Use `repo-delivery` for actual staging or commits after review.
- Systematic read-only Rust architecture, performance, memory, concurrency,
  SQLite, unsafe, or FFI audit; use `audit-rust`.
- Security-only audit after the Rust surface is mapped; use `audit-security`.
- Frontend UI work around a Tauri backend; use `implement-frontend`.

## Output

Report detected project class, Baseline evidence, selected risk overlays,
toolchain, Cargo and command sources, existing docs/interfaces checked,
reuse/extension/reference decision, new-interface justification, changed
contract and crate/module ownership, Rust best-practice decisions, structural
documentation updates, validation mapped to each overlay, failures, excluded
optional checks with reasons, and `Not verified` areas.

Examples of valid selection:

- routine private helper: Baseline only;
- public API: Baseline + Contract;
- SQLite migration: Baseline + Persistence/SQLite, plus Contract only when a
  public or durable consumer contract changes;
- FFI callback: Baseline + Unsafe/FFI, plus Contract when callers change;
- FFI-backed SQLite import: Baseline + Unsafe/FFI + Persistence/SQLite;
- target-specific adapter only: Baseline + Target/platform. Do not add Miri,
  sanitizers, fuzzing, stress, leak, or repeated-operation checks unless another
  selected overlay makes them relevant and the repository supports them.

## Maintenance

Keep this file, `references/checklist.md`, `references/eval-cases.md`,
`references/best-practices.md`, `references/bun-production-patterns.md`,
`SKILL.md`, and `agents/openai.yaml` synchronized. Validate with
`python3 scripts/validate-skills.py`.
