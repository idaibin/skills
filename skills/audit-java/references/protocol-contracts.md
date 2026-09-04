# Java Protocol Contract Audit

Use this profile only when the selected Java surface owns or implements an OpenAPI
contract. Read [shared OpenAPI governance](openapi-contract-governance.md) before
applying this audit overlay.

## Audit Evidence

- Fix the contract path/state/content identity, Java basis, compatibility baseline,
  named consumers, and selected code-first or contract-first strategy.
- Run the repository-owned generic parser/linter in check-only mode. Separate core OAS
  structural validity from recommended-quality policy failures.
- Inventory operations, standard security schemes/requirements, path parameters,
  request bodies, success/error responses, examples, enums, constraints, empty schemas,
  required/nullable fields, and repeated response sets.
- For contract-first, review the accepted contract before comparing Controllers, DTOs,
  validation, security, and exception mapping. Source cannot repair or reinterpret a
  missing design decision.
- For code-first, verify the fixed-basis producer and deterministic generation before
  comparing generated OpenAPI.
- Treat absence of descriptions, constraints, required fields, examples, or enums as a
  finding only when it leaves a real consumer or implementation decision ambiguous.
  Conditional draft semantics may intentionally have few required fields but must still
  describe defaults, at-least-one rules, discriminator branches, and submission gates.
- A vendor `x-*` extension is valid metadata but cannot replace standard OpenAPI fields
  required by generic documentation, SDK, validation, or test consumers.

## Reporting

Report separately: contract authority/state, structural lint, design completeness,
compatibility, Java conformance, consumer coverage, runtime/gateway, deployment, and
production. Lead with evidence-backed blockers to authoritative promotion; do not edit
the contract or Java source in audit mode.
