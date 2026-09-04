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
authoring owner, non-LLM consumer, executable validator, drift policy, and retirement
rule as lifecycle gates. Require a producer only for an actual generated derivative
such as JSON, transport types, or a client; a human-authored contract-first YAML does
not need a source parser or generator to exist.

An audit inventory, reviewer report, controller list, or frontend call inventory is
evidence for resolving the authority; it is never itself an OpenAPI producer. A route
present in source is also not automatically a supported product API. When an accepted
business rule forbids a reachable route, record the artifact as `draft/conflict` and
stop promotion until the source route is removed, disabled, or explicitly constrained
by the owning backend. Do not hide the route only in documentation and do not publish
the forbidden capability under `paths` while calling the artifact authoritative.

## Wire Contract

Read [shared OpenAPI governance](openapi-contract-governance.md), then apply these
Java-specific rules:

- Map an accepted contract to Controller method/path and parameter location, boundary
  DTOs, Bean/application validation, security/data-scope enforcement, serialization,
  and global error mapping without introducing a parallel wire authority.
- A Java `Long`, nullable field, annotation default, or exception class does not by
  itself decide the public wire range, requiredness, default, or reachable status.
- Frontend calls and legacy prose can reveal missing or conflicting fields but cannot
  confirm backend DTO, authorization, error, or envelope semantics.

## Implementation And Verification

1. Fix the Git basis, service, authority path, owner role, and contract state.
2. Validate the OpenAPI with the pinned repository-owned generic parser/linter before
   relying on it. Contract-first document lint does not compile or start Java and does
   not require a Controller-parsing script.
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

For contract-first, promotion to `authoritative` MUST stop only when the selected
authoring owner or acceptance is invalid: the owner is wrong or ambiguous, the
acceptance is not bound to the exact scope/version/content hash, or an accepted
business-exposure rule still conflicts with a reachable source route. Owner acceptance
otherwise makes the contract authoritative before Java implementation; incomplete
implementation or lifecycle evidence does not demote that authority.

Implementation automation or delivery completion MUST stop when any applicable
condition is true:

- code-first generation has no executable producer bound to the fixed Git basis;
- contract-first Java routes/DTOs/security/errors do not conform to the accepted contract;
- only parser/schema validation has passed;
- no fixed legacy baseline or compatibility comparison exists for existing consumers;
- non-LLM consumer, validator, drift policy, or retirement rule is missing;
- an actual generated derivative has no declared producer;
- operation errors are mechanically copied rather than resolved from reachable code;
- unresolved handbook, UI, or decision content remains embedded in OpenAPI.

For code-first automation, provide a check-only repository command that fails closed.
It must run the producer twice from the same fixed basis, normalize volatile metadata,
and require byte-identical or canonical-hash-identical output. The same gate must cover
structural validity, route and DTO/validation conformance, security and data-scope
exposure, global error mapping, business exposure allow/deny rules, compatibility with
the fixed baseline, and declared consumer coverage. Compilation, an audit report, or a
successful YAML parse cannot substitute for these checks.
