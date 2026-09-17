---
name: dev-java
description: "Implement Java source and Java-owned Maven or Gradle changes."
---

# Java Implementation

## Entry Gate

Implement Java changes against the actual build root, JDK, module, framework, and contract owners. Read effective guidance and current Worktree state; stop before edits if the target module or decisive build/runtime contract is unresolved.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any Java change | [checklist](references/checklist.md) and [Java engineering](references/java-engineering.md) | Scoped implementation/validation |
| Public seam supports a vertical behavior slice | [behavior first](references/behavior-first.md) | Behavior-first evidence |
| Module/interface/testability or quality concern applies | [codebase design](references/codebase-design.md) and/or [code quality](references/code-quality.md) | Design/quality decision |
| API, config, persistence, security, integration, packaging, or cross-project signal applies | [project grounding](references/project-grounding.md) | Boundary evidence/disposition |
| Existing or explicitly adopted OpenAPI pipeline applies | [protocol contracts](references/protocol-contracts.md) and [OpenAPI governance](references/openapi-contract-governance.md) | Native-authority-compatible protocol work |

## Invariants

- Preserve the pinned JDK/build/framework and existing controller/service/data/security owners.
- Do not introduce OpenAPI, persistence abstractions, generated clients, or architecture merely by analogy.
- Keep source, tests, build, migration, integration, runtime, and deployment evidence distinct; do not mutate Git.

## Output Map

Report scope, build/module/JDK basis, selected overlays, changed contracts/files, validation, exclusions, and `Not verified` evidence.

## Reference Map

- Read [checklist](references/checklist.md) and [Java engineering](references/java-engineering.md) for baseline procedure.
- Read [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), and [project grounding](references/project-grounding.md) only when applicable.
- Read [protocol contracts](references/protocol-contracts.md) and [OpenAPI governance](references/openapi-contract-governance.md) only for an actual protocol pipeline.
- Read [usage](references/usage.md) for overlay selection and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
