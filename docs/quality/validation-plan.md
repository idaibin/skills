# AICraft Validation Plan

Status: active evidence plan

Date: 2026-07-15

## Objective

AICraft validates existing Skill contracts before expanding the public suite.
The plan must answer four different questions without collapsing them into one
score:

1. Does each package match the current portable and provider-specific format?
2. Does a model route, stop, and hand off according to the declared contract?
3. Does the Skill complete representative repository work without crossing its
   authority boundary?
4. Does the changed Skill improve outcomes or efficiency over the previous or
   no-Skill condition?

The machine-readable case minimums, coverage requirements, score gates, result
schema, and official-source review dates live in
[`contracts/skill-validation.json`](../../contracts/skill-validation.json).
Documents and scripts must consume that contract rather than maintain a second
set of numeric thresholds.

## Evidence Layers

### Structure Suite

Run from the repository root:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/eval-skill-contracts.py --validate-only
python3 scripts/measure-skill-footprint.py --baseline-ref <comparison-ref>
git diff --check
```

This layer proves package shape, metadata, references, routing inventory,
dataset schemas, shared-protocol synchronization, and validator regressions.
The footprint command measures deterministic context size only. This layer does
not execute a model and cannot prove behavior, workflow quality, time savings,
or token savings.

### Routing And Handoff Suite

Use natural-language requests that do not name a Skill or leak the expected
owner. Cover positive routing, nearest-neighbor non-triggers, high-risk false
triggers, ambiguous requests, and multi-intent requests with required and
forbidden handoffs. Every published Skill and every live nearest-neighbor edge
must meet the coverage rules in the contract.

Retain the prompt, dataset hash, exact model and host, committed Skill revision,
selected owner, handoffs, adjudication, raw output, duration, token counts when
the host exposes them, prompt template, fixture, pair identity, and isolated
host-environment policy.

### Authority Suite

Use real tool-capable runs to verify that read-only skills do not write,
diagnosis does not apply a permanent fix, implementation does not mutate Git,
delivery touches only authorized paths, and browser, client, or external review
actions require the declared authorization. Score observed behavior, not the
model's stated intention.

The current trace contract is producer-attested: it makes a retained trace and
verifier output tamper-evident, but it does not authenticate the producer or
derive action/evidence labels independently from raw host events. Record these
runs for audit and contract development, but do not set behavior to `verified`
until an independent semantic verifier is implemented.

### Workflow Suite

Run representative repository tasks for every published Skill. Retain the
request, route, tool calls, changed files, raw trace, validation output,
workspace diff, stop or recovery state, duration, and token counts when
available. A successful narrative without the required evidence is a failed
workflow result.

Workflow traces have the same producer-attested boundary as authority traces.
They cannot set workflow to `verified` until an independent event-to-action and
verifier mapping is enforced.

## Contract Verification And Improvement Comparison

Contract verification and comparative improvement are separate experiments.

- A candidate-only run can verify that the current Skill meets its routing,
  authority, and workflow contracts. It does not prove improvement.
- A claim that a Skill noticeably improves collaboration, quality, time, or
  token use requires a controlled previous-Skill or no-Skill baseline.
- Candidate and baseline use the same task prompts, repository fixture, host,
  model, tool permissions, timeout, and adjudication rubric. Run matched
  conditions with isolated HOME/config/Skill roots and a shared pair ID. Run
  them in parallel. If the host cannot do that, use randomized interleaving and
  record the limitation.
- Run the contract-defined minimum number of trials per condition. Report pass
  rate, duration, and token mean plus variation; retain every trial rather than
  selecting the best run.
- Changes to `name`, `description`, or discovery metadata require a held-out
  routing set committed after the frozen candidate
  `evaluation_anchor_revision`, absent at that revision, and
  disjoint by case ID and prompt hash from existing eval datasets. Commit an
  exact-hashed provenance record with the dataset that attests independent
  post-freeze authorship and `used_for_tuning=false`; every bundle and claim
  must bind the same anchor and provenance. Candidate and baseline use the
  anchor revision; previous controls must be strict ancestors. Git chronology
  and an attestation still cannot prove human blindness.
- Grade task outcomes and authority violations independently from style. Store
  raw traces, verifier output, and workspace diffs so a score can be audited.
- When a host does not expose token counts, record `null`; do not estimate them.
  Claude normalized input totals include reported cache-creation and cache-read
  input tokens; OpenAI cached-input detail remains a subset of `input_tokens`
  and is not added again. Retain the verbatim host output for audit.
- Report duration but do not use it as an improvement gate. Host-load noise is
  not controlled tightly enough; only outcome or non-regressing token
  efficiency can pass the current comparison gate.

## Verification Rules

- `structure = verified` requires the full structure suite at the recorded
  repository revision.
- Routing results may support a narrowly scoped model/host/revision claim after
  their raw evidence and comparison replay pass.
- Authority and workflow bundles are currently producer-attested only, so
  `behavior` and `workflow` remain `not_verified` even when their schema and
  scorer pass. Enabling either state requires an independent semantic verifier
  and a contract update.
- An improvement claim additionally requires a passing comparison report built
  from manifest-recorded candidate and control bundles. Repository validation
  replays the comparator and rejects a report whose content, hash, conditions,
  source revisions, or evidence selection no longer matches.
- Every verified claim is scoped to one dimension, kind, host name/version,
  exact model, candidate/control revisions, dataset hash, and Skill inventory.
  Routing claims additionally bind the evaluation anchor, dataset commit, and
  held-out provenance path/hash. A single comparison cannot establish a global
  quality or collaboration claim.
- Unchecked hosts, models, stacks, or runtime claims remain `not_verified`.
- Update descriptions, contracts, fixtures, and regression tests when official
  standards change or recorded evidence demonstrates drift. Do not preserve a
  stale validator merely because its old fixtures still pass.
- Do not add public Skills or weaken score gates to improve a metric.

## Execution Phases

1. Pin and periodically refresh the official alignment record.
2. Keep package, metadata, routing, and dataset validation deterministic.
3. Execute routing and authority trials with complete raw evidence.
4. Execute per-Skill workflow trials in isolated repository fixtures.
5. Run controlled previous/no-Skill comparisons for improvement claims.
6. Make evidence-driven corrections and rerun held-out regressions.
7. Verify OpenAI Codex and Claude Code behavior separately without turning
   provider-specific features into portable requirements.

Current evidence and gaps are tracked in [`status.md`](status.md). The external
baseline and provider lanes are recorded in
[`official-skill-alignment.md`](official-skill-alignment.md).
