# API Contract Design

Use for bounded API contract authoring or revision after business semantics are accepted.

## Authority Decision

Declare exactly one strategy for each bounded service before changing request or
response definitions:

- **Contract-first:** human-readable OpenAPI is the wire authority. Keep it `draft`
  until the API owner accepts the exact scope, version, and content hash; implementation
  then conforms to that accepted artifact.
- **Code-first:** backend routes, wire DTOs, validation, security, and error mappings are
  the authority. OpenAPI is a generated derivative tied to a fixed source basis.

Do not maintain parallel handwritten endpoint, DTO, response, or error authorities.
Frontend wrappers, screenshots, legacy prose, repository inventories, and successful
parsing may reveal conflicts but cannot establish backend truth.

## Workflow

1. Fix the service boundary, owner, consumers, current source basis, and applicable
   product/domain decisions.
2. Declare `authority_strategy: code-first|contract-first`,
   `phase: design|implementation`, and `status: draft|authoritative`.
3. Preserve the target project's native envelope, authentication, gateway prefix,
   naming, pagination, and error conventions. Treat external standards as defaults,
   never as evidence that the project implements them.
4. Author or revise the native OpenAPI artifact using
   [OpenAPI authoring](openapi-authoring.md). Prefer YAML for handwritten
   contract-first specifications unless a named consumer requires JSON.
5. Keep product behavior, UI handling, retries, deployment state, changelog, unresolved
   decisions, and verification logs outside OpenAPI. Create a Markdown companion only
   when a real reader needs context; link to schemas instead of copying them.
6. Validate with the project's pinned check-only parser/linter. If none exists, identify
   the gap and use an available generic validator without claiming project adoption.
7. Report structural validation, compatibility, backend conformance, generated-client
   drift, consumer coverage, runtime/gateway, deployment, and production as separate
   evidence dimensions.

## Existing Baseline

If the accepted contract already satisfies the request, preserve it and report a no-op
with the relevant readback or check. Reuse valid validation evidence on the same basis;
repeat only for a relevant change, failure, unresolved concern, or required project gate.

Unresolved product behavior belongs to product-spec; shared business terms belong to
domain-modeling. API authoring never accepts its own draft on behalf of the native owner.
