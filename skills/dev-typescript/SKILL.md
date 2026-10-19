---
name: dev-typescript
description: "Implement non-browser TypeScript or JavaScript changes for Node.js, Bun, or Deno."
---

# TypeScript Implementation

## Entry Gate

Implement the smallest authorized non-browser source slice in the repository's actual runtime and package-manager contract. Read effective guidance, identify the owning root and current basis, and stop if a decisive contract cannot be resolved.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any source change | [checklist](references/checklist.md) | Scoped implementation and credible validation |
| Node, Bun, Deno, ESM/CJS, package or runtime choice applies | [runtime profiles](references/runtime-profiles.md) | Runtime-compatible change |
| Public seam/testable behavior applies | [behavior first](references/behavior-first.md) | Bounded behavior evidence |
| Module/API design or quality risk applies | [codebase design](references/codebase-design.md) and/or [code quality](references/code-quality.md) | Reuse and maintainability decision |
| Cross-boundary signals apply | [project grounding](references/project-grounding.md) | Qualified boundary evidence |

## Invariants

- Before touching another business module, apply the [cross-module business gate](references/codebase-design.md#cross-module-business-gate); an implementation request alone does not authorize changing its existing behavior or code.

- Preserve existing runtime, package manager, module, source, and test owners; do not add a parallel stack.
- During development, do not invoke a standalone build, bundle, or package command as validation. Run the actual CLI entry point with `--help`, `doctor` when supported, representative commands, and focused non-build checks. A build is allowed only in an authorized release phase or when the user explicitly requests build, packaging, or artifacts; if installation requires a build without that authorization, keep installed-command validation `Not verified` and report the requirement.
- Keep source, static, build, runtime, artifact, and deployment claims separate.
- Do not implement browser UI, review, stage/commit/push, or infer unresolved behavior.

## Output Map

Report scope, authoritative inputs, runtime/profile, reuse decision, changed files, focused validation, Worktree drift, exclusions, and `Not verified` gaps.

## Reference Map

- Read [checklist](references/checklist.md) for the baseline workflow and stop conditions.
- Read [runtime profiles](references/runtime-profiles.md) only for runtime/package concerns.
- Read [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), and [project grounding](references/project-grounding.md) only when their condition applies.
- Read [usage](references/usage.md) for triggers and nearest boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
