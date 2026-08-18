# Java Protocol Contracts

## Activation

Use this overlay only when the repository already owns an OpenAPI or generated-client
pipeline, or the user explicitly requests adopting one. Ordinary Java REST work keeps
the native controller, DTO, error mapping, client, and tests; report this overlay
`Not applicable` instead of introducing OpenAPI.

## One Authority

Select exactly one authoring authority for the bounded service:

- **Code-first:** Java routes, DTOs, validation, and error mappings are authoritative;
  generate or validate normalized OpenAPI from them.
- **Contract-first:** an accepted OpenAPI is authoritative; implement Java routes,
  DTOs, validation, and error mappings to conform to it.

For contract-first work, prefer a human-reviewable YAML authority. Generate JSON only
for a named consumer and never maintain it as a second hand-edited contract. Record the
backend service owner by role unless the project names a distinct IDL/contract owner.
Keep an artifact `draft` until the owner accepts its exact scope, version, and content
hash. That acceptance makes it `authoritative` before Java implementation. Record the
producer, non-LLM consumer, executable validator, drift policy, and retirement rule as
lifecycle gates; missing gates limit automation or delivery claims without demoting an
accepted contract.

## Wire Contract

Keep OpenAPI limited to the HTTP contract:

- service base URL, method/path, authentication, and actual status codes;
- path/query/header/cookie parameters and JSON or multipart request bodies;
- field type, requiredness, nullability, enum, constraints, and concise business
  descriptions;
- every non-empty success response and every confirmed error shape;
- response values reused by later operations, including upload identifiers and URLs.

Do not place page state, frontend wrappers, presentation behavior, retry UI,
deployment evidence, or unresolved review notes in OpenAPI. A POST does not imply a
body: verify the real parameter location. Request-body requiredness and required
fields are separate. Omit response content only for a genuinely empty body.

Inline an operation-local schema when that improves review. Extract a schema only
when a stable wire type is truly shared or a named generator benefits from the shared
owner. Require `operationId`, `tags`, or common response components only when an
actual generator/viewer consumes them. Use `format: int64` for a real wire-range
contract, not merely because Java uses `Long`; use `additionalProperties: false` only
when server validation rejects unknown fields.

Frontend calls and legacy prose can reveal missing or conflicting fields but cannot
confirm backend DTO, authorization, error, or envelope semantics. Resolve conflicts
through the selected backend/contract authority.

## Implementation And Verification

1. Fix the Git basis, service, authority path, owner role, and contract state.
2. Validate the OpenAPI with the repository-owned parser/linter before relying on it.
3. For code-first, generate twice in a clean or isolated environment and require
   identical normalized output. For contract-first, implement and test Java
   conformance without introducing a parallel DTO contract.
4. Compare compatibility with the fixed baseline when existing consumers may change.
5. Exercise applicable success, validation, authentication, authorization, business
   error, empty-body, multipart, and serialization behavior at the backend boundary.
6. Generate or verify frontend transport types only through the declared consumer
   chain; frontend UI behavior stays with its frontend owner.
7. Report structural validity, backend conformance, frontend consumption, runtime,
   gateway, browser, deployment, and production as separate dimensions; mark every
   unavailable applicable gate `Not verified`.
