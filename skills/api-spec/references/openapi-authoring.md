# OpenAPI Authoring

Use this reference for the wire-level content and validation of an OpenAPI contract.

## Contents

- [Document Identity](#document-identity)
- [Operation Checklist](#operation-checklist)
- [Schema Semantics](#schema-semantics)
- [Responses And Errors](#responses-and-errors)
- [Security](#security)
- [Compatibility](#compatibility)
- [Validation And Evidence](#validation-and-evidence)

## Document Identity

- Use the OpenAPI version supported by the target project's named tooling.
- Give `info.title`, `info.version`, and descriptions stable project meaning.
- Put the service or gateway prefix in `servers`; do not repeat it ambiguously in prose.
- Keep lifecycle metadata in one project-native index or top-level extension rather than
  copying it into every operation.
- Use stable `operationId` values when a named generator, viewer, or automation consumes
  them. Otherwise follow the target project's established practice.

## Operation Checklist

For every operation, define only confirmed behavior:

1. HTTP method and path.
2. Path, query, header, and cookie parameters at their real locations.
3. Request media type and request-body requiredness.
4. Request fields, independently marking field requiredness.
5. Success HTTP status, response media type, and every non-empty consumed schema.
6. Only the business and protocol errors reachable from this operation.
7. Root or operation security and any operation-specific permission/data-scope rule.
8. Idempotency or concurrency behavior when consumers need it.

Do not infer `requestBody` from POST alone. Do not return an empty schema when downstream
operations consume an identifier or other value from the response.

## Schema Semantics

- Distinguish omitted, `null`, empty string, empty array, and empty object when they have
  different effects.
- Define `required`, `nullable` or null unions, enum/domain values, defaults, formats,
  minimum/maximum, length, pattern, uniqueness, and array bounds according to actual
  wire validation.
- Describe identifier ownership and date/time timezone semantics when not self-evident.
- Express conditional requirements, mutual exclusion, discriminators, or “at least one”
  rules with supported schema composition. When the selected OpenAPI dialect cannot
  express a rule reliably, add a concise description and an executable contract test.
- Use `additionalProperties: false` only when the server really rejects unknown fields.
- Mark stable response fields as required so consumers know what they may depend on.
- Inline operation-local schemas when this makes review clearer. Extract a shared schema
  only when multiple operations share one stable wire type or a real consumer requires
  it.
- Add examples when they improve review, fixtures, SDKs, or integration tests; validate
  that examples conform to their schemas.

## Responses And Errors

- Preserve real HTTP semantics; do not model every business failure as HTTP 200 unless
  that is an accepted project contract.
- Keep the project envelope and distinguish its business code from the HTTP status.
- Define error fields consumers may safely use. Do not require clients to match a
  human-readable message.
- Reuse an error schema only when its wire shape and required fields are genuinely
  stable. Do not mechanically attach every known error to every operation.
- Document delete, disable, conflict, stale-write, duplicate, permission, and referenced-
  resource behavior where those failures are reachable.

## Security

- Declare `components.securitySchemes` and root or operation `security` with standard
  OpenAPI fields.
- Use `security: []` for an intentionally anonymous operation.
- Record the project's real session, cookie, bearer, API-key, mTLS, or external identity
  mechanism. Do not introduce a sample authentication scheme as if it were implemented.
- Never accept caller-supplied user, role, tenant, owner, or data-scope identifiers as
  the authenticated actor unless the accepted contract explicitly defines delegation.
- Keep UI visibility rules separate from server authorization; document both only at
  their proper owner boundary.

## Compatibility

Classify a change against the accepted baseline before calling it safe:

- usually breaking: removing or renaming operations/fields, changing types or meanings,
  adding required inputs, narrowing accepted enums or bounds, removing success/error
  variants consumers use, or changing authentication;
- potentially compatible but consumer-sensitive: adding optional inputs, adding response
  fields, adding enum values, changing defaults, pagination, ordering, or rate limits;
- operational only when truly outside the wire contract: deployment, implementation,
  or documentation changes that do not alter observable behavior.

Use a compatibility tool when the project has adopted one, but do not replace semantic
review with a tool result.

## Validation And Evidence

A pinned generic parser/linter should fail on at least:

- invalid OpenAPI structure or unresolved references;
- missing or mismatched path parameters;
- duplicate or unsafe operation identities when operation IDs are active;
- examples whose values contradict schemas;
- undefined security schemes or missing security decisions;
- malformed request/response schemas.

For code-first, bind generation to a fixed source basis and require two clean normalized
generations to match. For contract-first, lint the accepted contract first, then prove
backend route, validation, security, and error conformance separately.

Report these dimensions independently as `Verified`, `Failed`, `Not verified`, or
`Not applicable`:

1. structural OpenAPI validation;
2. compatibility against the accepted baseline;
3. backend implementation conformance;
4. generated derivative/client drift;
5. consumer compile or adapter tests;
6. runtime and gateway integration;
7. deployment and production observation.
