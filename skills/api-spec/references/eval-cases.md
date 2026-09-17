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
