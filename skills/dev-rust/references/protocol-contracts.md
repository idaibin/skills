# Rust Protocol Contracts

## Activation Gate

Use this profile only when current source/CI already defines an OpenAPI or generated
client pipeline, or the user explicitly requests a contract migration/trial. A REST
endpoint alone does not activate it. Preserve repository-native routes, DTOs,
clients, and focused tests when no executable exchange artifact is owned.
When inactive, report protocol-automation gates `Not applicable`.

## Select One Authority

Read [shared OpenAPI governance](openapi-contract-governance.md) before applying the
Rust-specific implementation chain.

When active, discover and record exactly one authoring authority:

- **Code-first**: Rust route, DTO, and contract declarations are authoritative;
  their clean generation produces normalized OpenAPI.
- **Contract-first**: the normalized OpenAPI artifact is authoritative; Rust
  implementation and tests prove conformance.

Do not infer the choice from a library name. Read repository commands, generated
markers, CI, ownership docs, and the actual route/DTO/OpenAPI chain. Java services
may use Swagger/OpenAPI annotations against the same language-neutral artifact;
frontend consumers must not depend on backend language.

## Implementation Chain

1. Fix the Git basis and baseline exchange artifact.
2. Record authority type, owning path, generator version, and exact commands.
3. Change the smallest route/DTO/handler/service/error chain.
4. Generate or conform to normalized OpenAPI.
5. Validate the artifact and run compatibility diff.
6. Regenerate the project-owned TypeScript client and verify no unexplained drift.
7. Run backend contract tests for applicable input/auth/success/error semantics.
8. Ensure CI can reproduce generation, validation, compatibility, client, backend
   contract tests, and downstream type/build checks from clean state.

## Minimum Live Evidence

- one service and one bounded feature with a real frontend consumer;
- at least one operation containing input, auth, success, and error behavior;
- unique authority, valid/rebuildable OpenAPI, and two clean identical generations;
- compatibility diff against a fixed Git basis;
- clean generated-client regeneration with no touched DTO duplicated by hand;
- backend runtime success, unauthenticated/unauthorized, validation, and business
  error paths when applicable;
- one real consumer plus the repository's runtime/browser evidence owner;
- clean-state CI reproduction.

If a required tool or runtime path is unavailable, finish the supported source
work but mark the missing gate `Not verified`; static validation is not a substitute.
When this profile is not active, report it `Not applicable` rather than creating an
OpenAPI artifact to satisfy the checklist.
