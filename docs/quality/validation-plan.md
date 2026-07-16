# AICraft Validation Plan

Status: active evidence plan

Date: 2026-07-16

## Objective

AICraft validates existing Skill contracts before expanding the public suite.
The plan must answer four different questions without collapsing them into one
score:

1. Does each package match the current portable and provider-specific format?
2. Does a model route, stop, and hand off according to the declared contract?
3. Does the Skill complete representative repository work without crossing its
   authority boundary?
4. Does the changed Skill preserve the previous contract, contribute beyond a
   no-Skill condition, or reduce Skill-attributable input overhead?

The machine-readable case minimums, coverage requirements, score gates, result
schema, and official-source review dates live in
[`contracts/skill-validation.json`](../../contracts/skill-validation.json).
Documents and scripts must consume that contract rather than maintain a second
set of numeric thresholds.

## Evaluation Architecture

AICraft retains its domain-specific owner, authority, and handoff contract
rather than replacing it with a generic benchmark. Its evaluation surfaces use
the separation established by mature agent-evaluation systems:

- **Task:** versioned natural-language case, labels, fixture, and required or
  forbidden observable behavior.
- **Solver:** exact host, model, committed Skill tree, prompt template,
  permissions, isolation policy, and installed/no-Skill condition.
- **Scorer:** deterministic owner, handoff, authority, and workflow assertions
  derived independently from the Solver configuration.

This follows the observable-assertion and matched with/without-Skill guidance
in [Agent Skills evaluation](https://agentskills.io/skill-creation/evaluating-skills)
and the dataset/solver/scorer separation in
[Inspect AI Tasks](https://inspect.aisi.org.uk/tasks.html). Future authority and
workflow verification should adopt the end-to-end trace and grader separation
described by
[OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals).
These references guide execution and evidence design; AICraft's
machine-readable contract remains authoritative for its Skill boundaries.

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

A routing case succeeds only when the selected owner is accepted, every
required direct handoff and exactly one member of every required one-of group
is present, and no undeclared, optional, or forbidden handoff appears. Report
unauthorized handoff entries, affected-case rate,
handoff-contract failure cases, and required-handoff recall separately. A
dataset with no positive handoff cases cannot report `0/0` as successful
recall.

Retain the prompt, dataset hash, exact model and host, committed Skill revision,
selected owner, handoffs, adjudication, raw output, duration, token counts when
the host exposes them, prompt template, fixture, comparison-group identity,
isolated host-environment policy, frozen retry-policy hash, ordered host-attempt
evidence, and case-level attempt/retry counts. Rebuild the prompt,
adjudication, host policy, transient retry policy, and non-sensitive
environment allowlist policy from the machine contract; a bundle cannot
introduce an arbitrary self-consistent hash.

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
- A claim that a Skill noticeably improves routing or Skill-context efficiency
  requires one controlled three-condition group: candidate, previous Skill,
  and no-Skill baseline.
- All three conditions use the same task prompts, repository fixture, host,
  model, tool permissions, timeout, and adjudication rubric. Run them with
  isolated HOME/config/Skill roots and one shared `comparison_group_id` per
  trial. Run matched groups in parallel when possible. If the host cannot do
  that, use randomized interleaving and record the limitation.
- Before any held-out call, commit a schema-v2 campaign after the candidate
  anchor. It fixes the exact previous revision, no-Skill baseline revision,
  artifact root, dataset/provenance, condition, complete trial/group set, and
  protocol and retry-policy hashes. Each planned variant/trial slot permits one
  retained formal attempt. Within that slot, the frozen policy permits at most
  one additional Codex host invocation after a five-second backoff, and only
  for the exact normalized JSON model-capacity message when the failed
  invocation exits with code `1`, has no valid structured result, and no exposed
  input or output token count. Both host invocations remain in raw schema `3`;
  the retry does not create or replace a campaign slot. Timeouts, behavior or
  scoring failures, invalid structured output, generic host failures,
  near-match errors, valid results, and token-bearing failures are not
  retried. An exhausted or otherwise failed formal attempt consumes the slot
  and requires a new campaign, not selection of a replacement run.
- Run the contract-defined minimum number of trials per condition. Report pass
  rate, duration, and token mean plus variation; retain every trial rather than
  selecting the best run.
- Changes to `name`, `description`, or discovery metadata require a held-out
  routing set committed after the frozen candidate
  `evaluation_anchor_revision`, absent at that revision, and
  disjoint by case ID and canonical prompt fingerprint from existing eval
  datasets and Skill `references/eval-cases.md`. The fingerprint uses NFKC,
  trimming, whitespace collapse, and case folding; semantic paraphrases remain
  an independent-review risk. Commit an exact-hashed provenance record with the
  dataset that attests independent post-freeze authorship and
  `used_for_tuning=false`; every bundle and claim must bind the same anchor and
  provenance. Candidate and baseline use the anchor revision; previous
  controls must be strict ancestors. Git chronology and an attestation still
  cannot prove human blindness.
- The new held-out set must meet the contract-defined positive required-handoff
  and empty-handoff coverage, primary-owner diversity, per-Skill trigger and
  neighbor coverage, and global multi-intent coverage. Consumed held-out cases,
  IDs, and canonical prompt fingerprints are never reused for a new claim.
- Grade task outcomes and authority violations independently from style. Store
  raw traces, verifier output, and workspace diffs so a score can be audited.
- When a host does not expose token counts, record `null`; do not estimate them.
  Reported input and output counts must be positive; zero is unavailable or
  invalid for a successful non-empty model invocation. Total tokens are
  reported but are not the Skill-discovery efficiency gate. A capacity failure
  is retryable only when both counts are `null`; token-bearing failures remain
  terminal. Every host attempt keeps its own token fields, while case-level
  tokens mirror the terminal attempt and `attempt_count`/`retry_count` disclose
  the retry separately.
  Subtract the matched no-Skill input total from candidate and previous input
  totals, then compare those marginal Skill overheads. The metric is unavailable
  if any group member lacks token data, any marginal overhead is negative, or
  previous mean overhead is not positive. Candidate overhead must be no greater
  than previous in every trial, and a claim needs both the contract's 15%
  relative reduction and 50-token-per-case mean absolute saving. Claude normalized input totals
  include reported cache-creation and cache-read input tokens; OpenAI
  cached-input detail remains a subset of `input_tokens` and is not added again.
  Retain verbatim host output for audit.
- Report duration but do not use it as an improvement gate. Host-load noise is
  not controlled tightly enough.

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
  from manifest-recorded candidate, previous, and no-Skill bundles. Repository validation
  replays the comparator and rejects a report whose content, hash, conditions,
  source revisions, or evidence selection no longer matches.
- Formal held-out scoring and replay require the contract, runner, evaluator,
  comparator, validator, and shared protocol module to match their blobs at the
  campaign's evaluation anchor. The manifest and every claim bind the campaign
  and protocol revision/hash; each bundle and raw record must also match the
  campaign's canonical `retry_policy_sha256`.
- Every verified claim is scoped to one dimension, kind, host name/version,
  exact model, candidate/previous/baseline revisions, dataset hash, and Skill inventory.
  Routing claims additionally bind the evaluation anchor, dataset commit, and
  held-out provenance path/hash. A single comparison cannot establish a global
  quality or collaboration claim.
- Unchecked hosts, models, stacks, or runtime claims remain `not_verified`.
- Update descriptions, contracts, fixtures, and regression tests when official
  standards change or recorded evidence demonstrates drift. Do not preserve a
  stale validator merely because its old fixtures still pass.
- Do not add public Skills or weaken score gates to improve a metric.

The campaign artifact root is append-only under the trusted evaluator process:
the comparator rejects missing, extra, duplicate, or failed formal attempts.
Raw evidence schema `3` preserves every within-slot host attempt, and result
schema `6`, comparison report schema `4`, plus reviewer version `6` validate
its classification, backoff, terminal mirrors, retry counts, and token
semantics. Local
hashes cannot stop an operator from deleting an uncommitted failed directory;
nor can they discover unreported preliminary calls or selection among multiple
campaigns. Every campaign and complete artifact root must be preserved and
published before a claim, and deliberate deletion or omission is outside the
trusted-producer boundary. A captured schema-valid bundle consumes the slot
even when the subsequent Skill score is `FAIL`; only infrastructure-invalid
captures move to a new campaign, with lineage recorded in evaluation notes.

## Execution Phases

1. Pin and periodically refresh the official alignment record.
2. Keep package, metadata, routing, and dataset validation deterministic.
3. Execute routing and authority trials with complete raw evidence.
4. Execute per-Skill workflow trials in isolated repository fixtures.
5. Run controlled candidate/previous/no-Skill groups for improvement claims.
6. Make evidence-driven corrections and rerun held-out regressions.
7. Verify OpenAI Codex and Claude Code behavior separately without turning
   provider-specific features into portable requirements.

Current evidence and gaps are tracked in [`status.md`](status.md). The external
baseline and provider lanes are recorded in
[`official-skill-alignment.md`](official-skill-alignment.md).
