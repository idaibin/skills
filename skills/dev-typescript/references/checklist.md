# Implementation Checklist

## Before Editing

- Authorization and symbolic scope are explicit.
- Guidance and dirty worktree state are known.
- Runtime, package manager, lockfile, module system, tsconfig, test runner, and command sources are evidenced.
- Acceptance, non-goals, compatibility, and focused validation seam are understood.
- Existing entry points, owners, schemas/types, callers, and analogous tests are traced.

## During Implementation

- Existing authority is reused or extended before a new interface is created.
- Runtime input is validated at the boundary.
- Strictness is not weakened through `any`, unchecked casts, broad ignores, or silent fallbacks.
- Async work has explicit failure, cancellation, cleanup, timeout, and retry semantics where applicable.
- Runtime-specific APIs match the selected profile and compatibility contract.
- Manifests, exports, generated artifacts, tests, docs, and configuration stay synchronized.

## Evidence

- Select existing checks closest to the change and complete required project gates.
  Add behavior tests only for a meaningful coverage gap, including relevant failure
  paths; a reversible low-impact edit needs no implementation-mirroring test.
- Use repository format/lint/type commands when applicable. Repeat or broaden checks
  only after a relevant change, failure, unresolved concern, or explicit requirement.
- Runtime, packaging, schema generation, integration, and multi-runtime parity checks are included only when reachable.
- Missing required evidence is `Not verified`; irrelevant checks are not applicable.
- Changed files, drift, exclusions, and remaining risks are reported before handoff.
