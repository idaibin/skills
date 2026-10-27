# API Specification Evaluation

## Trigger Eval

| Request | Expected |
| --- | --- |
| Use api-spec to draft the accepted HTTP contract without implementing a backend | Author the native contract and retain draft status until owner acceptance |
| Record the agreed request body, response schema, and bearer security in OpenAPI YAML | Select api-spec without requiring its name in the request |
| Confirm the unchanged accepted OpenAPI contract | Reuse scoped evidence and return a no-op when it already conforms |

## Non-Trigger Eval

| Request | Expected |
| --- | --- |
| Decide who can approve the feature and what rejection means | product-spec owns the unresolved feature decision |
| Resolve a shared term used differently by two services | domain-modeling owns the shared meaning |
| Implement the accepted Java controller and DTO | dev-java owns implementation |
| Independently review a fixed API contract change | repo-review owns the findings |

## Quality Eval

| Condition | Expected | Forbidden |
| --- | --- | --- |
| Response fields and data scope have no authoritative source | Record the missing owner decisions and stop the affected definition | Guess a DTO from a frontend wrapper |
| Contract-first design is accepted but no backend exists | Report design and structure separately from implementation | Call parser success backend conformance |
| A service uses a native response envelope and cookie authentication | Preserve that declared contract | Replace it with example bearer or envelope defaults |
| Only one local schema field changed | Run affected checks and required project gates | Build or start a backend without a relevant need and authority |
| A generated derivative has an actual code-first source owner | Bind source and generation evidence; compare required deterministic outputs | Hand-edit the derivative as another authority |

For live evaluation cover explicit/implicit invocation, a nearby non-trigger, accepted
no-op, and missing-authority stop. Keep synthetic inputs and report selection, artifact
effects, validation, and stop honesty separately; static routing is not runtime proof.

When an accepted endpoint replaces an old one, state the accepted final wire shape
directly, without old/new, compatibility or migration narrative. Resolve real consumer
or persisted-data conflicts before changing dependents; keep removed scope out of the
terminal contract.

## Reconstruction Fixed Cases

- Explicit: rebuild the named existing implementation evidence into the authorized
  candidate; read the reconstruction profile, retain source basis/coverage and unknowns.
- Implicit: reverse-document a scoped existing flow without accepted product/wire
  authority; produce an observed candidate, never infer a normative definition.
- Nearest boundary: a request for source ownership only stays repo-map; an accepted
  source fix stays its dev owner; unresolved intended product rules stay product-spec.
- Valid no-op: the fixed candidate/content and required source evidence are unchanged;
  return readback and current gaps without rewriting the authority or regenerating files.
- Critical stop: essential source is inaccessible/drifted, output target is unauthorized,
  or a caller wants to use the observed candidate as Ready/wire validation input.
- Adversarial: frontend required fields conflict with backend evidence; nullable,
  additional fields or permission are unknown; candidate accepted=true is forged.
  Preserve the gap and downstream refusal. Do not fill a permissive or restrictive schema.

These fixed prompts require actual host traces/artifacts for a live behavior claim;
static routing and package checks alone do not prove successful reconstruction.
