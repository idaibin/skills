---
name: implement-rust
description: "Use when implementing, porting, modifying, or refactoring Rust APIs, crates, services, CLIs, libraries, Tauri backends, Cargo workspaces, FFI, unsafe code, ownership, errors, async behavior, tests, rustdoc, formatting, or Clippy alignment while preserving repository contracts."
---

# Rust Implementation

## Overview

Implement Rust changes against the repository's real toolchain, project class, crate boundaries, error model, and validation contract. Select validation by risk rather than applying native/FFI-level gates to every routine change.

## Workflow

1. Read repository guidance and run `git status --short` before edits.
2. Identify the Rust project class: library workspace, application workspace, HTTP service, CLI, Tauri/native backend, or compact single package.
3. Inspect the relevant `Cargo.toml`, lockfile, toolchain, formatter, lint, command source, modules, tests, architecture docs, and API/interface docs.
4. Consume a current `repo-map` inventory or perform the same targeted search across route registration, handlers, services, repositories, traits/impls, types/DTOs, errors, migrations, callers, tests, and analogous features.
5. Start with the **Baseline** validation contract, then select every applicable risk overlay. Overlays are composable, not severity levels:
   - **Contract:** public API, endpoint, DTO, error mapping, crate/module boundary, feature flag, or downstream consumer change.
   - **Concurrency/runtime:** Tokio tasks, channels, locks, cancellation, blocking work, overload, or shutdown.
   - **Persistence/SQLite:** migrations, transactions, schema/query changes, durable compatibility, backup, or recovery.
   - **Unsafe/FFI:** unsafe, ABI/layout, raw pointers, callbacks, allocators, native handles, or cross-language resource ownership.
   - **Porting/parity:** language port or large rewrite that must preserve observable behavior and release semantics.
   - **Target/platform:** `cfg`, target-specific APIs, packaging, native linkage, or supported-platform behavior.
   A routine change uses Baseline with no overlays. A mixed FFI plus SQLite change selects both overlays; a target-only change selects Target/platform without inheriting unrelated heavy tools.
6. Decide in order: directly reuse, extend an existing contract, adapt the nearest reference, or create new. Record why existing interfaces are insufficient before adding an endpoint, trait, type family, or module.
7. Trace ownership, dependency direction, and the complete interface chain before adding or moving code.
8. Implement the smallest idiomatic change that follows local ownership, borrowing, module, error, async, persistence, FFI, configuration, logging, documentation, and test patterns.
9. Update manifests, module exports, tests, commands, docs, CI/deploy paths, migrations, generated files, and indexes when the structural or public boundary changes.
10. Run the repository's baseline gates, then combine validation from every selected overlay. Use Miri, sanitizers, fuzzing, stress, or repeated-operation tools only when both supported by the target repository/environment and relevant to the changed invariant.

## Modes

- **Targeted implementation:** add or fix Rust behavior without broad architecture or toolchain changes.
- **Structure alignment:** align modules, crates, manifests, commands, and docs to an explicit repository standard.
- **Contract migration:** change an API, DTO, feature, persistence, or consumer boundary with compatibility and rollout evidence.
- **Native/porting implementation:** preserve observable behavior, ABI/resource semantics, supported targets, and release behavior before idiomatic cleanup.
- **Implementation self-check:** verify the edited Rust surface for ownership, errors, async behavior, safety, tests, dependencies, and structural drift before `repo-review` assesses commit readiness.

## Do Not Use For

- First-pass repository discovery; use `repo-map`.
- Future multi-step migration planning; use `code-planner`.
- Unknown root-cause investigation; use `diagnose`.
- Dirty-tree ownership, staging plans, or commit grouping; use `repo-review`. Use `repo-delivery` for actual staging or commits after review.
- Systematic Rust architecture, performance, memory, concurrency, SQLite, unsafe, or FFI audit without requested edits; use `audit-rust`.
- Security-only audit after the Rust surface is mapped; use `audit-security`.
- Frontend or webview UI changes; use `implement-frontend`.

## Hard Rules

- Follow repository-pinned Rust, edition, resolver, formatter, lint, dependency, and command contracts. Do not upgrade them during unrelated feature work.
- Keep directories consistent with the identified project class. Do not copy a Web/Rust, Tauri, CLI, library, or multi-process layout into another class without an explicit migration requirement.
- Do not create an endpoint, handler, service, repository, trait, DTO/type family, error model, or shared module before reading relevant docs and checking the existing interface chain. Reuse or extend first; follow the nearest feature's placement and naming when a new contract is justified.
- Preserve dependency direction. Entry modules stay thin; workflows belong in the established service/engine owner; deterministic domain logic avoids IO; persistence stays behind repository or storage boundaries when the project defines them.
- Prefer typed errors and `Result` propagation. Do not add runtime `unwrap`, `expect`, `panic!`, silent error swallowing, or fallback behavior unless the contract explicitly requires it.
- Do not add `unsafe`, broad feature flags, global mutable state, blocking work in async paths, or new dependencies without proving the need and validation.
- Keep FFI and raw-pointer work behind narrow reviewed adapters. Define ABI, layout, ownership, lifetime, thread, cleanup, callback, allocator, and panic behavior; make each `unsafe` site state the invariant that makes it sound.
- For language ports or large rewrites, preserve observable behavior before idiomatic cleanup. Record source-to-Rust mappings and lifetime/ownership decisions, prove a representative slice, and test release semantics and supported platforms. Compilation is only the first gate.
- Prefer borrowing and slices at read-only API boundaries; clone only when ownership is required. Prefer static dispatch until runtime polymorphism is a real requirement. Measure before performance optimization.
- Document public APIs with purpose, invariants, examples, and `# Errors`, `# Panics`, or `# Safety` sections when applicable. Keep comments for why; use types, naming, tests, rustdoc, and tracked issues instead of stale prose.
- Treat new warnings in the touched surface as defects. Do not broaden scope to clean unrelated legacy warnings; report them separately. Prefer a local justified `#[expect(...)]` over weakening workspace lints.
- Keep product-specific behavior in the product repository. Move code to a shared crate only after real reuse, stable API, named ownership, and consumer validation are established.
- When adding, reusing, moving, renaming, or deleting a crate, module, feature, binary, migration, or shared surface, update every owning manifest, export, command, test, doc, CI/deploy path, generated output, and index in the same task.
- Preserve unrelated local changes and generated files not owned by the task.

## Validation Model

- **Baseline:** repository-defined format/check plus focused behavior tests; Clippy only when it is part of the repository baseline.
- **Selected overlays:** add only the contract, concurrency/runtime, persistence/SQLite, unsafe/FFI, porting/parity, and target/platform evidence required by the changed surface. Combine overlays when risks interact; do not let one overlay erase another.
- **Optional heavy tools:** Miri, sanitizers, fuzzing, stress, leak, and repeated-operation gates are never inherited merely from a target-specific change. Run them only when supported and relevant, or record why they were excluded.

Do not claim Baseline or an overlay passed when a required tool, target, runtime, dataset, or external dependency was unavailable; mark the exact gap `Not verified`.

## Output Contract

Report project class, Baseline evidence, selected risk overlays, toolchain and command sources, existing docs/interfaces checked, reuse/extension/reference decision, new-interface justification, changed ownership and contract chain, manifests/docs updated, validation mapped to each selected overlay, failures, excluded optional checks with reasons, and `Not found` or `Not verified` gaps.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, update all references and `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/best-practices.md](references/best-practices.md) for idiomatic Rust API, ownership, error, test, docs, performance, dispatch, and concurrency rules.
- See [references/bun-production-patterns.md](references/bun-production-patterns.md) for source-backed migration, FFI, unsafe, resource-lifetime, lint, and validation patterns derived from Bun's production Rust rewrite.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
