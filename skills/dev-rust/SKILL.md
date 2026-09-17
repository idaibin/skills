---
name: dev-rust
description: "Implement, port, or refactor Rust source in the existing Cargo workspace."
---

# Rust Implementation

## Entry Gate

Implement a bounded Rust change in the repository's actual Cargo workspace, toolchain, crate boundaries, and interface contracts. Read guidance and current Worktree state; stop before edits if the target crate, build contract, or decisive interface is unknown.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any Rust source change | [checklist](references/checklist.md) and [best practices](references/best-practices.md) | Scoped implementation/validation |
| Public seam/testable behavior applies | [behavior first](references/behavior-first.md) | Behavior evidence |
| Architecture or quality risk applies | [codebase design](references/codebase-design.md) and/or [code quality](references/code-quality.md) | Reuse/quality decision |
| FFI, native, agent runtime, or production Bun bridge applies | [agent runtime](references/agent-runtime-profile.md) and/or [Bun patterns](references/bun-production-patterns.md) | Applicable boundary procedure |
| Integration, persistence, packaging, compatibility, or cross-project signal applies | [project grounding](references/project-grounding.md) | Qualified evidence |
| Existing/adopted protocol automation applies | [protocol contracts](references/protocol-contracts.md) and [OpenAPI governance](references/openapi-contract-governance.md) | Native-authority protocol work |

## Invariants

- Preserve real crate, ownership/error, async, unsafe/FFI, toolchain, and test conventions.
- Do not add a framework, generated client, or protocol pipeline without an existing/adopted owner.
- Keep source, lint/build, native/runtime, artifact, and deployment proof separate; do not mutate Git.

## Output Map

Report basis, crate/toolchain/profile, changed files/contracts, focused validation, exclusions, and `Not verified` gaps.

## Reference Map

- Read [checklist](references/checklist.md) and [best practices](references/best-practices.md) for the baseline.
- Read [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), and [project grounding](references/project-grounding.md) only when applicable.
- Read [agent runtime](references/agent-runtime-profile.md), [Bun patterns](references/bun-production-patterns.md), [protocol contracts](references/protocol-contracts.md), and [OpenAPI governance](references/openapi-contract-governance.md) only for those profiles.
- Read [usage](references/usage.md) for triggers and nearest boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
