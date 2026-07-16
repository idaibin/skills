# AICraft Behavior Evaluation Data

These datasets evaluate declared Skill contracts directly. Candidate-only
results can verify contract correctness. A claim that a changed Skill improves
outcomes or efficiency requires matched `candidate`, `previous`, and no-Skill
`baseline` trials as defined in
[`docs/quality/validation-plan.md`](../docs/quality/validation-plan.md).

## Files

- `routing.jsonl`: natural-language owner-selection and handoff cases.
- `routing-held-out.jsonl`: consumed round-one holdout retained only for the
  archived failed comparison; never reuse it for tuning or a new claim.
- `routing-held-out-provenance.json`: immutable round-one source revision,
  authorship, and host-use record.
- `routing-held-out-v2.jsonl` and `routing-held-out-v2-provenance.json`:
  consumed holdout whose campaign failed before reaching the model service.
- `routing-held-out-v3.jsonl` and `routing-held-out-v3-provenance.json`:
  consumed holdout whose campaign ended on one capacity failure. The historical
  `v3-heldout-002` owner label has a no-rescore, no-reuse erratum in the failure
  record linked below; do not edit the consumed dataset.
- `routing-held-out-v4.jsonl` and `routing-held-out-v4-provenance.json`:
  consumed holdout for campaign `eb47a629-8c22-40f5-9c34-70f388f0b736`.
  Its six attempt ledgers contain 210 raw host records: five slots succeeded,
  while trial 2 candidate `v4-heldout-034` timed out after 120 seconds (209
  exit-code-0 records, one exit-code-124 record, and zero retries). Trial 3 was
  not started, and no score, comparison report, or quality-manifest entry was
  created.
- `routing-held-out-v2-campaign.json`, `routing-held-out-v3-campaign.json`, and
  `routing-held-out-v4-campaign.json`: preregistrations retained for those
  non-scoring campaigns. See the
  [`2026-07-16 infrastructure-failure record`](../docs/history/evals/2026-07-16-codex-gpt56-routing-infrastructure-failures.md).
- `authority.jsonl`: mutation and external-action boundary cases.
- `workflow-smoke.jsonl`: representative end-to-end task specifications.

Prompts in routing data must not name a Skill. Expected and forbidden owners are
labels used only by the evaluator after the model response is captured.

## Validate Datasets

```bash
python3 scripts/eval-skill-contracts.py --validate-only
```

Validation proves only schema, inventory, uniqueness, prompt leakage checks, and
contract-defined coverage. It does not execute a model. Case minimums, score
gates, and result schema versions are authoritative in
[`contracts/skill-validation.json`](../contracts/skill-validation.json).

## Score Captured Results

Routing, authority, and workflow result files are JSON objects. Each bundle
covers one dataset, condition, and trial. The bundle contains hashes and
metrics; scored observations come from the referenced raw evidence file:

```json
{
  "schema_version": 6,
  "complete": true,
  "run_id": "UUID",
  "model": "exact model identifier",
  "host": "exact host and version",
  "skill_revision": "40-character committed Git SHA",
  "skill_tree_sha": "Git tree hash for <revision>:skills",
  "dataset_revision": "exact dataset sha256",
  "captured_at": "ISO-8601 timestamp",
  "run_config": {
    "variant": "candidate",
    "trial": 1,
    "dataset_path": "evals/routing-held-out.jsonl",
    "dataset_git_revision": "single post-anchor commit for dataset and provenance",
    "evaluation_anchor_revision": "frozen candidate Skill commit shared by every variant",
    "held_out_provenance_path": "evals/routing-held-out-provenance.json",
    "held_out_provenance_sha256": "sha256 of the committed provenance record",
    "prompt_set_sha256": "same value as dataset_revision",
    "case_set_sha256": "sha256 of the ordered id/prompt-hash set",
    "case_ids": ["held-out-001", "held-out-002"],
    "comparison_group_id": "UUID shared by candidate, previous, and no-Skill for this trial",
    "attempt_id": "UUID for this preregistered attempt",
    "attempt_path": "attempt.json",
    "campaign_id": "UUID from the committed campaign",
    "campaign_path": "evals/<fresh-campaign>.json",
    "campaign_sha256": "sha256 of the exact committed campaign",
    "evaluation_protocol_revision": "frozen anchor commit",
    "evaluation_protocol_sha256": "sha256 of the anchor protocol-file manifest",
    "held_out": true,
    "permissions": "read-only",
    "timeout_seconds": 120,
    "concurrency": 1,
    "host_name": "codex",
    "fixture": {"schema_version": 1, "task": "fixture descriptor"},
    "fixture_sha256": "sha256 of the canonical fixture object",
    "skills_installed": true,
    "skill_fixture_sha256": "sha256 of the committed exported Skill packages",
    "prompt_template_version": 2,
    "prompt_template": "Template with one <NATURAL_REQUEST_JSON> placeholder",
    "prompt_template_sha256": "sha256 of the exact prompt template",
    "host_config_sha256": "sha256 of the canonical host configuration",
    "environment_policy_sha256": "sha256 of allowed variable names and isolated overrides, never secret values",
    "retry_policy_sha256": "sha256 of the canonical host-specific transient retry policy"
  },
  "adjudication": {
    "method": "deterministic",
    "reviewer": "exact verifier or reviewer identifier",
    "reviewer_version": "6",
    "config_sha256": "sha256 of the adjudication configuration"
  },
  "results": [
    {
      "id": "route-001",
      "raw_evidence": "raw/routing/route-001.json",
      "raw_evidence_sha256": "sha256 of the evidence file",
      "metrics": {
        "duration_ms": 1250,
        "input_tokens": null,
        "output_tokens": null,
        "attempt_count": 1,
        "retry_count": 0
      }
    }
  ]
}
```

Result schema `6`, raw-evidence schema `3`, campaign schema `2`, comparison
report schema `4`, and routing-runner reviewer version `6` define the current
three-condition comparison group, necessary-handoff prompt semantics,
cache-inclusive token accounting, preregistered campaign, frozen protocol,
attempt ledger, bounded transient-capacity retry, and OpenAI-supported
response-schema subset.
Earlier result bundles fail closed and cannot support a current marginal
Skill-input efficiency claim.

Every raw routing record contains the matching run, case, source-prompt hash,
exact invocation prompt and hash, model, and host identifiers; verbatim stdout,
stderr, model output, start/completion timestamps, and a transcript rebuilt from stdout/stderr; the exit
code; parsed `actual_owner` and `handoffs`; the frozen `retry_policy_sha256`;
and an ordered `host_attempts` list containing the timestamps, transcript and
hash, response, observations, error classification, backoff, and token metrics
for every host invocation. Top-level raw output and tokens mirror the terminal
host attempt, while `attempt_count` and `retry_count` expose whether the single
permitted retry occurred. The same metrics are mirrored by the bundle. The
runner atomically checkpoints each completed host attempt before any backoff or
next invocation, so an interrupted formal slot retains the last completed call.
loader rebuilds the invocation from the recorded template and dataset prompt,
then recomputes cache-aware token usage from stdout before accepting metrics.
Authority and workflow records additionally retain the execution trace,
before/after manifests and diff, and verifier output. Evidence paths are
relative to the bundle, cannot escape it, and are verified by hash. The scorer
uses only loader-verified raw observations; mirrored summary fields cannot
override them.

These hashes are tamper-evident under a trusted evidence producer. They do not
authenticate which CLI or model emitted the record and do not prove that a
self-reported action/evidence label is semantically true. Until an independent
event mapper or verifier binds raw host events to each authority/workflow case,
those suites remain producer-attested and cannot set behavior or workflow to
`verified`.

```bash
python3 scripts/eval-skill-contracts.py \
  --routing-dataset path/to/routing-held-out.jsonl \
  --routing-results path/to/routing-results.json \
  --authority-results path/to/authority-results.json \
  --workflow-results path/to/workflow-results.json
```

The routing runner is dry-run by default. It prints the planned condition,
case IDs, revisions, and configuration hashes without exposing credentials or
calling a model; `--execute` is an explicit cost and side-effect gate.
Its `model_call_budget` reports `scored_slots` and `maximum_model_calls` for
the `selected_run` and, when present, the complete `campaign`, plus the frozen
retry policy's `maximum_attempts_per_scored_slot`. The campaign budget is the
dataset case count times three variants times the preregistered trial count;
the model-call ceiling is that slot count times the per-case attempt limit.
Atomic campaign-slot claiming and the enforced per-case attempt limit prevent
execution from exceeding this bound. For v4, `35 × 3 × 3` is 315 scored slots
and at most two attempts per slot is 630 model calls. This is an upper-bound
audit record; it neither says calls occurred nor grants execution authority.
Each real case uses a unique temporary repository and isolated `HOME`, XDG, and
host configuration root. Only the host credential file is copied; global
Codex/Claude configuration and global Skill roots are excluded. Candidate and
previous variants install only the committed package export, while baseline
installs no Skills. Codex runs also disable the remote plugin catalog while
retaining the project-local committed Skill fixture. Successful output is
loaded and scored again through the production evaluator before the runner
reports success.

Formal held-out execution requires `--campaign`. A schema-v2 campaign is a
committed JSON file created after the candidate anchor. It fixes the campaign
UUID, unique repository-relative artifact root, candidate/evaluation anchor,
one explicit strict-ancestor previous revision, no-Skill baseline revision,
dataset and provenance paths/hashes/commits, exact host/model/timeout/concurrency,
the complete ordered trial-to-group-ID set, canonical prompt/adjudication/host
and environment-policy hashes, the canonical `retry_policy_sha256`, and the
evaluation-protocol manifest. The
protocol hashes the contract, runner, evaluator, comparator, validator, and
shared protocol module at the anchor. Formal run, score, comparison, and
manifest replay fail if any current protocol blob differs from that anchor.

```bash
python3 scripts/create-skill-routing-campaign.py \
  --candidate-anchor <frozen-candidate-sha> \
  --previous-skill-revision <explicit-previous-sha> \
  --dataset evals/<fresh-held-out>.jsonl \
  --provenance evals/<fresh-held-out-provenance>.json \
  --host codex \
  --model <versioned-model-id> \
  --trials 3 \
  --output evals/<fresh-campaign>.json \
  --dry-run
```

The creator is local-only and self-validates every canonical hash without
calling a model. Omit `--dry-run` to atomically write the reviewed campaign,
then commit it before any `--execute` call. It creates a fresh campaign UUID by
default, so an infrastructure-invalid campaign can be retained and superseded
without reusing slots; `--campaign-id` exists only for explicit deterministic
fixtures.

```bash
python3 scripts/run-skill-routing-eval.py --help
```

Use the same prompts, fixture, model, host, permissions, timeout, and rubric for
all comparative variants. Use one `comparison_group_id` for the candidate,
previous, and no-Skill runs in each trial, a versioned model identifier, and the
same canonical isolated-environment policy. The policy hash binds the source
variable names that may be copied, fixed isolation placeholders, and the
credential-copy rule. It does not bind or record the copied PATH, `VOLTA_HOME`,
proxy, locale, certificate, or temporary-directory values. A matching policy
hash therefore proves policy identity, not runtime-environment identity or the
absence of drift. Run the group from one controlled parent environment; do not
claim that runtime drift was measured unless separate non-secret evidence was
captured. Run matched groups in parallel when the host supports it and record
any randomized-interleaving fallback. Each
campaign slot permits one formal attempt. Within that attempt, the canonical
policy permits at most one additional host invocation, after a five-second
backoff, only when Codex exits with code `1` and contains the exact normalized JSON
`message` `Selected model is at capacity. Please try a different model.`, no
valid structured result exists, and no input or output token count was exposed.
Claude currently has no retryable error class. Timeouts, behavior failures,
invalid structured output, generic host failures, near-match messages, valid
results, and token-bearing failures are never retried. Both host invocations
remain in the raw record; the retry does not create or replace a campaign slot.

The runner writes `attempt.json` before calling the host; a failed or
interrupted formal attempt consumes that slot. Preserve the complete artifact
root and create a new post-anchor campaign instead of retrying under a
different group ID or selecting a replacement result. The comparator requires
exactly every planned
candidate/previous/baseline slot, no extra or failed attempt, and the exact
campaign revisions and group IDs. Use the contract-defined minimum trials per
condition and retain raw trace,
duration, token counts when available, outcome grade, verifier output, and
workspace diff.

Formal-attempt status and Skill score are different.
`attempt.status=success` means a complete, schema-valid bundle was captured;
the Skill can still score `FAIL`, and behavior or scoring failure is never a
retry trigger. If the one exact capacity retry is exhausted, or the capture is
interrupted or invalid for any other reason, the formal attempt remains failed
and consumes the campaign slot. Retain the failed campaign and record its
successor in the evaluation notes; do not choose among multiple campaigns
after inspecting scores.

A held-out routing file and its provenance record must be introduced together
in one post-anchor commit, have no other post-anchor path history, and must not
exist at the frozen candidate `evaluation_anchor_revision`. Captures must
postdate that dataset/provenance commit. Candidate and baseline bundles use the
anchor as their Skill revision; a previous bundle must use a strict ancestor.
The dataset must not reuse any case ID or canonical prompt fingerprint from
repository eval datasets or `skills/*/references/eval-cases.md` present at the
frozen revision. Prompt fingerprints apply NFKC normalization, trimming,
whitespace collapse, and case folding. Retain consumed held-out datasets so
their prompts remain in this seen registry. The provenance file binds the
dataset hash, anchor/source revision, post-freeze independent authorship
attestation, `used_for_tuning=false`, and intended hosts; the runner binds its
path and hash to every bundle. This prevents exact copy/rename and low-level
textual rewrites and fails closed when the attestation is absent, but it cannot
detect semantic paraphrases or prove that a human never saw the prompts while
tuning.

Generate a comparison report only from matched, scored bundles:

```bash
python3 scripts/compare-skill-evals.py \
  --kind routing \
  --campaign evals/<fresh-campaign>.json \
  --dataset path/to/routing-held-out.jsonl \
  --candidate path/to/candidate-trial-1.json \
  --candidate path/to/candidate-trial-2.json \
  --candidate path/to/candidate-trial-3.json \
  --previous path/to/previous-trial-1.json \
  --previous path/to/previous-trial-2.json \
  --previous path/to/previous-trial-3.json \
  --baseline path/to/no-skill-trial-1.json \
  --baseline path/to/no-skill-trial-2.json \
  --baseline path/to/no-skill-trial-3.json \
  --output path/to/comparison-report.json
```

Routing outcome is full-case success, not primary-owner top-1 alone: an accepted
owner, every required direct handoff, exactly one member of every required
one-of group, and zero unauthorized or optional handoffs are all required. The
comparison passes only when every candidate trial passes
the contract, full-case outcome does not regress against the previous Skill,
and at least one scoped improvement dimension reaches its preregistered gate.

Reported input and output token counts must be positive; zero is unavailable or
invalid for a successful non-empty model invocation. A capacity response is
retryable only when both token counts are `null`; if either count is present,
the failure is retained without retry. The case-level token fields mirror the
terminal host attempt, and every host attempt retains its own fields. Therefore
the earlier capacity invocation contributes no tokens to the case total only
because the host exposed none; its raw evidence and retry count remain visible.
Total tokens remain visible but are not a discovery-efficiency gate. The live
Skill-context metric uses input tokens only and subtracts the matched no-Skill
condition from both candidate and previous totals. It is available only when
all three conditions expose tokens, every per-group marginal overhead is
non-negative, the candidate overhead is no greater than previous in every
group, and the previous mean marginal overhead is positive. A claim also
requires at least 15% relative reduction and at least 50 saved input tokens per
case on average, preventing tiny-denominator wins. This can
support only a scoped marginal Skill-input claim, not an end-to-end statement
that all AI work is faster or cheaper. Claude input totals include reported
cache-creation and cache-read tokens; OpenAI cached-input details remain a
subset of input tokens. Duration is reported but is not a gate because wall
clock samples remain vulnerable to host-load noise. Means, standard deviations,
unavailable data, revisions, group timing, and evidence hashes remain visible.

Do not mark behavior or workflow verified until all required metadata and raw
evidence are present, pass the scorer, appear in the quality evidence manifest,
and are reflected in `docs/quality/status.md`.

Manifest schema `6` records each campaign, dataset, and bundle path plus its
SHA-256. A comparison
record references validated candidate, previous, and baseline evidence IDs and
a self-hashed report. `claims` is a list of scoped verified assertions; each
entry must match one replayed passing comparison's kind, exact claim dimension,
host name/version, model, three revisions, dataset hash, and Skill inventory.
Omit unverified claims. Routing claims also bind the campaign ID/path/hash,
evaluation-protocol revision/hash, evaluation anchor, dataset Git revision,
and held-out provenance path/hash. The current contract permits
only scoped routing outcome versus previous, routing contribution versus
no-Skill, or marginal Skill-input efficiency claims; it rejects global
“improvement” wording and authority/workflow claims.

Failed comparison reports are ineligible for the quality manifest. Archive an
exact failed report and a clearly labeled non-claim summary under
`docs/history/evals/`, and state whether the raw bundles are committed and
replayable from repository contents.

The artifact-root and attempt-ledger checks assume a trusted executor preserves
the campaign directory. Git hashes and replay detect retained tampering, but no
local process can prevent an operator from deleting an uncommitted failed
directory, hiding unreported preliminary model calls, or choosing among
multiple campaigns after seeing results. Publish or commit every campaign's
complete artifact root before making a claim; deliberate deletion or omission
remains a trust-boundary violation, not a property these hashes can
cryptographically prevent.
