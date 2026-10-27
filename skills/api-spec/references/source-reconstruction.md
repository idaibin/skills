# Existing API Evidence Reconstruction

Use only for an explicitly requested, scoped existing-API evidence rebuild. This
profile observes implementation; normal api.contract.specify still requires accepted
business semantics before defining native wire behavior.

## Input And Scope

Fix the service/repository/content basis, candidate target and allowed backend routes,
DTO/serialization/validation, middleware/security, configuration and test paths.
Reuse repo-map navigation. Frontend wrappers, screenshots and old prose are secondary
leads, not backend truth. Do not run services, call real endpoints or inspect credentials
unless separately in scope. Missing essential source or basis drift stops that slice;
missing product authority leaves a candidate and named owner gaps rather than invented
business definitions.

## Evidence Procedure

Trace each scoped route through applicable middleware, binding, validation, handler,
serialization and errors. Record reachable observed behavior with source refs; separate
inferences, unknowns, contradictions, test-only assertions and accepted native contracts.
Retain coverage exclusions. Do not guess envelope, identity/data scope, field types,
requiredness, nullability, additional-field rejection, conditional rules or errors from
one frontend usage or happy-path response. Resolve clear ordinary technical consistency;
route material business ambiguity to product-spec/domain-modeling.

## Observed Projection Is Not Wire Authority

The capability `api.evidence.reconstruct` emits an observed projection, not a normative
OpenAPI schema. Keep unresolved dimensions explicitly unknown in the candidate's prose
or existing evidence convention. Do not use type:string, missing required, nullable
choices, additionalProperties:true/false or permissive any-schema to encode ignorance:
each makes a real acceptance/rejection claim for validators and generated clients.
Do not invent an x-* flag and assume every downstream validator will honor it.

Use a named candidate document beside the project's existing authorities only when
that target is authorized. Link observed endpoints/types to source; do not overwrite
accepted OpenAPI to mirror code. If a project already has an observed-projection format,
retain its native owner/validator. This portable IO adds no mandatory JSON/YAML sidecar.

## Output And Acceptance Boundary

Return candidate/native artifact ref and content hash, exact source basis, service/scope,
observed/inferred/unknown/conflicting dimensions, coverage, original accepted authority
refs if any, check results and next owner. Mark it candidate/observed and not fit for
wire validation, client generation, implementation acceptance or Ready promotion.

Only the native service/contract owner can qualify the exact scope, version, content,
current source basis and resolved wire semantics for normative use. Then follow the
existing code-first/contract-first, phase/status and separate verification dimensions
in contract-design. A parser pass, candidate metadata or self-declared accepted value
is not owner acceptance. A real machine consumer must refuse candidate, missing or
forged acceptance, stale basis and content drift before invoking wire validation.
Unchanged evidence/candidate may return a bounded no-op. Source changes, runtime
operations, Git, installation and external AI remain outside this profile.
