# Bun-Derived Production Rust Prompts

Use this case study only when the selected Porting/parity or Unsafe/FFI overlay
needs an additional cross-language, resource-lifetime, or invariant-enforcement
challenge. It supplies review prompts, not another Rust standard or validation
model. Repository guidance, the local implementation, `SKILL.md` Baseline plus
selected overlays, and [best-practices.md](best-practices.md) remain authoritative.

## Source Boundary

The prompts were derived from Bun's official “Rewriting Bun in Rust” article and
`oven-sh/bun` at commit `90f8746301cc3ee56f7484bf9a8d40dd4aa0d715`, reviewed on
2026-07-10. The article's referenced porting and lifetime guides were not present in
that revision; do not claim their contents or current repository state without fresh
evidence.

## Applicable Prompts

### Ownership And Cleanup

- Name the owner of every allocation, handle, callback context, and borrowed value.
- Express routine cleanup through an owning type or narrow guard where possible.
- When cleanup depends on a flag, callback, re-entry, or foreign state transition,
  verify success, error, cancellation, final-callback, and exactly-once release paths.
- Use leak or repeated-operation evidence only when the repository supports it and
  the selected risk requires it.

### Unsafe And FFI

- Keep foreign calls and pointer operations behind the smallest reviewable adapter;
  record pointer source, nullability, alignment, initialized length, provenance,
  aliasing, lifetime, thread affinity, re-entry, allocator, and panic policy.
- Verify both sides agree on symbol, calling convention, field order, size, alignment,
  integer width, enum openness, ownership, and allocation/free symmetry.
- Model open foreign integer values without assuming every discriminant is a valid
  exhaustive Rust enum.
- Prefer audited safe wrappers over an arbitrary zero-unsafe target when native calls
  are required.

### Porting And Parity

- Preserve observable behavior before idiomatic cleanup; prove one representative
  slice before widening the migration.
- Compare assertion evaluation, eager versus lazy fallback, rounding and negative
  conversions, alignment/trailing bytes, bounds and overflow, destructor order,
  asynchronous callback ownership, and re-entry semantics.
- Never hide required mutation or I/O inside `debug_assert!`; optimized builds remove
  its expression.
- Reject compilation-only parity, stubs, placeholder constants, silently skipped
  tests, or architecture changes mixed into a mechanical port.

### Local Invariant Enforcement

- Encode a stable project invariant in lint or CI only when an approved replacement
  exists, the owning scope is clear, exceptions can be narrow, and the check does not
  force an unsuitable abstraction or dependency cycle.
- Treat project-specific prohibited APIs, allocator policy, nightly toolchain, panic
  mode, LTO, and crate layout as Bun decisions, not transferable defaults.

## Non-Transferable Conclusions

- Do not infer performance, safety, or architecture quality from the language choice,
  crate count, unsafe density, allocator, or build flags.
- Do not copy Bun's all-at-once rewrite strategy without a stable language-independent
  behavior suite, broad supported-platform coverage, a mechanical mapping, and enough
  capacity to complete the compatibility window.
- Do not duplicate the Baseline/overlay validation ladder here. Select and report
  validation through `SKILL.md` and the implementation checklist.
