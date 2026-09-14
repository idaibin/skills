# Frontend Protocol Contract Audit

Use this profile only when the selected frontend surface consumes an adopted OpenAPI or
generated-client chain, or the audit explicitly asks whether frontend calls conform to
one. Read [shared OpenAPI governance](openapi-contract-governance.md) before applying
this frontend consumer overlay. REST usage alone does not activate it.

## Audit Evidence

- Fix the contract path, state and content identity, frontend basis, compatibility
  baseline, generator when present, generated client/types, adapter, and representative
  consumers.
- Verify the frontend preserves method/path, path/query/header/cookie/body placement,
  media type, security credentials, required/nullable fields, enums, status/error
  handling, and response shapes from the selected contract.
- Detect hand-maintained DTOs or endpoint constants that duplicate a generated owner,
  but do not require generation when the repository intentionally owns native client
  types and OpenAPI is inactive.
- Treat a `draft` contract as design evidence, not permission to claim consumer
  conformance. Do not use frontend behavior to fill missing backend security, validation,
  error, or conditional-schema decisions.
- Keep UI loading, empty, error, retry, notification, and view-model behavior outside the
  wire authority while checking that the adapter exposes enough information to implement
  the accepted Product behavior.

## Reporting

Report contract authority/state, structural lint evidence supplied by its owner,
compatibility, generated-client drift, frontend adapter/consumer coverage, runtime,
gateway, deployment, and production separately. Route contract defects to the API owner
and accepted frontend remediation to `dev-frontend`; do not edit either in audit mode.
