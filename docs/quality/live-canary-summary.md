# Skill Live Canary Summary

## Basis

- Digest scope: all 18 packages declared by `skills-index.json`; the index owns the package set.
- Package digest: `sha256:21d613b4cbfbb6b695995349f88cba1528ee3bed98fb730b34d030766d6fe6ba`
- Change focus: Product recovery decisions and UI failure-state contracts, accepted
  no-change evaluation, and bounded readiness. Raw live-Agent records remain local.

- Added scope: Product submission-recovery semantics and UI retained-input visibility,
  accepted-contract no-op evaluation, and separate contract/runtime readiness. Ten
  fixed synthetic cases cover explicit/contextual use, owner neighbors, no-change
  results, and unresolved recovery rules. Automated route/process verdicts require
  case-specific semantic readback; they do not establish contract correctness alone.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Product/UI recovery live cases | Partial | Ten fixed cases on gpt-5.6-terra medium, 24 total executions. Latest applicable semantic readback: 6 pass, 3 partial, 1 fail; automated route/process checks pass but do not grade specification content. Accepted-contract no-op is corrected. Remaining gaps concern workflow consumption, Product recovery handoff, unsupported UI details, and a missing actual preview. Raw traces and per-case adjudication remain local; no whole-system or efficiency claim. |
| Package structure | Pass | 18 self-contained packages; local links and metadata validate. |
| Deterministic routing | Pass | 64/64 cases; no regressions against the immutable preceding baseline. |
| Context warnings | Pass | Zero warnings; estimates are not measured model tokens. |
| Final catalog gate | Pass | Canonical gate exited 0: 18 packages, 64 routes, 452 regressions, shared protocols, DESIGN.md contract checks, and whitespace. |
| Selection host forward-test | Pass within decision scope | An independent Agent read the runtime references and handled three supplied host states: mode-limited synchronous tool with eligible asynchronous alternative, accepted submission without user answer, and no eligible structured tool. It selected the alternative or fallback correctly and kept dependent Git actions paused. This exercised Agent decisions, not real conflict resolution or UI execution. |
| API host forward-test | Pass within fixture scope | Five requests exercised explicit/implicit invocation, a neighboring product owner, accepted no-op, and missing-authority stop. Parent readback confirmed one new contract and only one existing contract changed; source and no-op/blocked inputs stayed unchanged. YAML parsing and focused assertions passed; full OpenAPI lint was unavailable. Native task history and operation summaries are retained locally; no raw CLI JSONL run or cost comparison is claimed. |
| Tests live cases | Pass within synthetic scope | Five fixed explicit/contextual/nearest/no-op/authorization-stop cases ran on gpt-5.6-terra medium. Three initial rubric failures were corrected to require gap/stop evidence and rerun; initial traces remain local. Final evidence-retention and API-runner permission clarifications were independently checked; the former against actual project records, the latter against bounded decision scenarios. |
| Tests project application | Sample completed with findings | Real browser operation against an existing Mock: 11 PASS, 3 FAIL, 1 BLOCKED. This establishes the sampled execution, not production API or whole-system acceptance. |
| Installed-copy parity | Delivery-time check | Compare this package digest with the authorized installation after delivery; installation receipts remain local. |
| CLI model comparison | Not verified | The preceding attempt with CLI 0.150.0 failed before agent actions because the requested GPT-6 Astra model required a newer client; no model substitution or unchanged retry. |
| Backend, browser/client, deployment, and efficiency | Not verified | Contract fixtures do not establish these layers or a model-cost improvement. |

## Boundary

Package validation and deterministic routing establish catalog consistency. Registry
contracts do not prove a runtime adapter exists. Host fixtures can establish only their
observed selections and artifact effects. Installed bytes do not prove existing
sessions reloaded discovery.
