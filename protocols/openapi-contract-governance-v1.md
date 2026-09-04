# OpenAPI Contract Governance

Apply this reference only when a project has adopted OpenAPI or explicitly requests
adoption. Keep exactly one wire-contract authority per bounded service.

## Authority And Lifecycle

- **Contract-first:** design and review a human-readable OpenAPI before implementation.
  Keep it `draft` until the contract owner accepts the exact scope, version, and content
  hash; acceptance makes the contract authoritative before Controller/handler work.
- **Code-first:** routes, wire DTOs, validation, security, and error mappings are the
  authority; OpenAPI is a generated derivative bound to a fixed source basis.
- A controller inventory, audit, frontend caller list, legacy document, or successful
  parse is evidence, not an authoring authority.
- Record the authoring owner, real non-LLM consumers, executable validator, compatibility
  baseline when applicable, drift policy, and retirement rule. Require a producer only
  for an actual generated derivative such as JSON, transport types, or a client.

## Wire Completeness

- Define method/path, server prefix, parameter location, media type, request body,
  response body, and actual success/error statuses for every operation.
- Model field descriptions, requiredness, nullability, enum/domain values, defaults,
  conditional rules, IDs, date/time, pagination, bounds, patterns, arrays, and nested
  objects according to wire semantics. Request-body requiredness and field requiredness
  are independent.
- Conditional business rules such as “at least one field”, discriminator-dependent
  requirements, and mutually exclusive fields must be expressed with supported schema
  composition or concise operation/schema descriptions plus executable contract tests;
  do not silently leave them in implementation comments.
- Define every non-empty response schema and the stable required fields consumers may
  rely on. Add representative examples where they materially improve review, docs,
  fixtures, SDKs, or integration tests.
- Extract only stable shared schemas. Inline operation-local shapes when that improves
  review; do not create references merely to shorten the file.

## Security And Errors

- Declare standard `components.securitySchemes` and root or operation `security`.
  Explicitly use `security: []` for intentionally anonymous operations. A vendor
  extension may add deployment nuance but cannot replace standard security semantics.
- Model callback signatures, API keys, bearer/session schemes, permission/data-scope
  requirements, and security errors at the actual operation boundary.
- Declare only errors reachable from that operation. Do not mechanically attach one
  response set to every operation; `413` belongs only to request paths that can reach
  payload-size enforcement.
- Keep UI behavior, retries, deployment evidence, unresolved decisions, changelogs, and
  integration handbooks outside OpenAPI.

## Generic Validation

- Use a pinned, project-owned generic OpenAPI parser/linter configuration. It should at
  minimum fail on invalid structure, unresolved references, duplicate or unsafe
  `operationId`, missing path parameters, invalid examples/schema types, undefined
  security schemes, and missing security declarations.
- Linting a contract does not require compiling or starting the backend and does not
  justify a project script that parses Controllers. Adding an API changes the contract,
  not the generic validator.
- Keep structural lint, compatibility diff, backend conformance, generated-client drift,
  consumer coverage, runtime/gateway, deployment, and production as separate evidence
  dimensions.
- For code-first only, run the producer twice from one fixed basis and require identical
  normalized output. For contract-first, validate the accepted contract first, then
  implement and test backend conformance without a parallel DTO authority.
