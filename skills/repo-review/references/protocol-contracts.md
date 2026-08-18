# Protocol-Contract Review Profile

## Activation Gate

Use this profile only when the repository already owns an OpenAPI/generated-client
pipeline or the review request explicitly names that contract gate. REST alone is
not sufficient. Otherwise review the repository-native route, DTO, error, client,
consumer, and test chain and report OpenAPI `Not applicable`.

## Fixed Contract Basis

Before findings, record:

- review mode and immutable Git basis or complete Worktree state;
- one bounded service and feature;
- authority type: code-first backend declarations or contract-first OpenAPI;
- authority path and ownership;
- contract state (`draft` or `authoritative`) and the evidence supporting that state;
- generator name/version and exact generation commands;
- baseline normalized OpenAPI artifact at the fixed Git basis;
- candidate artifact from retained generation/CI evidence or clean generation in a
  disposable isolated copy constructed from the fixed basis plus candidate changes.

Do not use a moving branch, framework name, edited generated file, or current
worktree contamination as authority evidence for another basis.

Never execute a write-mode generator in the reviewed checkout. Replay only inside
the disposable isolated copy and verify the original worktree/index/status plus
relevant file hashes remain unchanged. If isolation cannot be created, consume
existing evidence only and mark regeneration/idempotence `Not verified`.

## Review Chain

Trace product intent reference -> authority -> normalized OpenAPI -> backend
route/DTO/handler/error mapping -> generated TypeScript client -> representative
consumer -> tests and CI. The exchange artifact is language-neutral: Java
Swagger/OpenAPI and Rust libraries are authoring mechanisms, not frontend contracts.

Check:

1. exactly one authoring authority;
2. valid, reconstructable OpenAPI and, when generation exists, two identical clean
   generations replayed in the disposable isolated copy;
3. compatibility diff against the fixed baseline artifact;
4. isolated clean client regeneration with no unexplained drift or duplicate touched DTO;
5. backend success, unauthenticated/unauthorized, validation, and business-error
   conformance when applicable;
6. real consumer loading/success/error evidence when claimed;
7. clean-state CI reproduction of the complete chain.

For hand-authored contract-first OpenAPI, also check that every operation declares the
real path/query/header/body location, separates body requiredness from required fields,
models every non-empty consumed response, and keeps frontend wrappers/page behavior
outside the wire contract. Treat `operationId`, `tags`, shared components, `format`,
and `additionalProperties: false` as required only when a real consumer or server
semantic justifies them. Prefer readable local schemas over mechanical `$ref`
extraction when no generator owns reuse.

An OpenAPI file remains draft until the owner accepts its exact scope, version, and
content hash. Producer, non-LLM consumer, validator, drift policy, and retirement rule
are separate lifecycle gates: their absence limits automated consumption or delivery
claims but does not demote accepted authority. Review structural validity, backend
conformance, frontend consumption, runtime, gateway, deployment, and production as
independent dimensions. Frontend source and old Markdown may expose a discrepancy but
cannot confirm backend wire semantics.

## Finding Boundary

Schema validity and static package checks are structural evidence. They cannot
prove runtime conformance, UI behavior, or CI reproducibility. Report unavailable
live gates as `Not verified`; do not clear a compatibility or integration risk by
assuming the implementation matches the artifact.
