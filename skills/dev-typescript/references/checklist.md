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

- Focused type-check and behavior tests cover success and relevant failure paths.
- Format/lint checks match repository commands.
- Runtime, packaging, schema generation, integration, and multi-runtime parity checks are included only when reachable.
- Every unavailable claim is marked `Not verified` with the exact blocker.
- Changed files, drift, exclusions, and remaining risks are reported before handoff.
