# Skill Live Canary Summary

## Basis

- Digest scope: all 17 packages declared by `skills-index.json`; the index owns the package set.
- Package digest: `sha256:52427685e87f4d5fc649b46cfc3d7e8211d48309e26bd365acfd8172c9c9a023`
- Change focus: move the generic API contract Skill into the catalog, expose
  `api.contract.specify`, and preserve one native contract authority with narrow
  product, implementation, review, and runtime boundaries.
- The other 16 package trees are unchanged from the preceding release. Prior live
  results do not certify the new API package. Raw task evidence stays private.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | 17 self-contained packages; local links and metadata validate. |
| Deterministic routing | Pass | 61/61 cases; no regressions against the immutable preceding baseline. |
| Context warnings | Pass | Zero warnings; estimates are not measured model tokens. |
| Final catalog gate | Pass | Canonical gate exited 0: 17 packages, 61 routes, 452 regressions, shared protocols, DESIGN.md contract checks, and whitespace. Source discovery returned the 17 catalog packages. |
| API host forward-test | Pass within fixture scope | Five requests exercised explicit/implicit invocation, a neighboring product owner, accepted no-op, and missing-authority stop. Parent readback confirmed one new contract and only one existing contract changed; source and no-op/blocked inputs stayed unchanged. YAML parsing and focused assertions passed; full OpenAPI lint was unavailable. Native task history and operation summaries are retained locally; no raw CLI JSONL run or cost comparison is claimed. |
| Installed-copy parity | Delivery-time check | Compare this package digest with the authorized installation after delivery; installation receipts remain local. |
| CLI model comparison | Not verified | The preceding attempt with CLI 0.150.0 failed before agent actions because the requested GPT-6 Astra model required a newer client; no model substitution or unchanged retry. |
| Backend, browser/client, deployment, and efficiency | Not verified | Contract fixtures do not establish these layers or a model-cost improvement. |

## Boundary

Package validation and deterministic routing establish catalog consistency. Registry
contracts do not prove a runtime adapter exists. Host fixtures can establish only their
observed selections and artifact effects. Installed bytes do not prove existing
sessions reloaded discovery.
