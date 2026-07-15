# AICraft Behavior Evaluation Data

These datasets evaluate declared Skill contracts directly. Candidate-only
results can verify contract correctness. A claim that a changed Skill improves
outcomes or efficiency requires matched `candidate` and `baseline` or
`previous` trials as defined in
[`docs/quality/validation-plan.md`](../docs/quality/validation-plan.md).

## Files

- `routing.jsonl`: natural-language owner-selection and handoff cases.
- `routing-held-out.jsonl`: post-freeze routing holdout with two cases per Skill.
- `routing-held-out-provenance.json`: source revision, authorship, and host-use
  record for the holdout.
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
  "schema_version": 3,
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
    "pair_id": "UUID shared by this candidate/control trial pair",
    "held_out": true,
    "permissions": "read-only",
    "timeout_seconds": 120,
    "concurrency": 1,
    "host_name": "codex",
    "fixture": {"schema_version": 1, "task": "fixture descriptor"},
    "fixture_sha256": "sha256 of the canonical fixture object",
    "skills_installed": true,
    "skill_fixture_sha256": "sha256 of the committed exported Skill packages",
    "prompt_template_version": 1,
    "prompt_template": "Template with one <NATURAL_REQUEST_JSON> placeholder",
    "prompt_template_sha256": "sha256 of the exact prompt template",
    "host_config_sha256": "sha256 of the host configuration"
  },
  "adjudication": {
    "method": "deterministic",
    "reviewer": "exact verifier or reviewer identifier",
    "reviewer_version": "version",
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
        "output_tokens": null
      }
    }
  ]
}
```

Result schema `3` and routing-runner reviewer version `2` define the current
cache-inclusive Claude token-accounting semantics. Earlier result bundles fail
closed and cannot support a current token-efficiency claim.

Every raw routing record contains the matching run, case, source-prompt hash,
exact invocation prompt and hash, model, and host identifiers; verbatim stdout,
stderr, model output, and a transcript rebuilt from stdout/stderr; the exit
code; parsed `actual_owner` and `handoffs`; and the same metrics mirrored by the bundle. The
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
Each real case uses a unique temporary repository and isolated `HOME`, XDG, and
host configuration root. Only the host credential file is copied; global
Codex/Claude configuration and global Skill roots are excluded. Candidate and
previous variants install only the committed package export, while baseline
installs no Skills. Successful output is loaded and scored again through the
production evaluator before the runner reports success.

```bash
python3 scripts/run-skill-routing-eval.py --help
```

Use the same prompts, fixture, model, host, permissions, timeout, and rubric for
comparative variants. Use one `pair_id` for each candidate/control trial pair,
a versioned model identifier, and the same isolated environment policy. Run
matched conditions in parallel when the host supports it and record any
randomized-interleaving fallback. Use the contract-defined minimum trials per
condition and retain raw trace, duration, token counts when available, outcome
grade, verifier output, and workspace diff.

A held-out routing file and its provenance record must be introduced together
in one post-anchor commit, have no other post-anchor path history, and must not
exist at the frozen candidate `evaluation_anchor_revision`. Captures must
postdate that dataset/provenance commit. Candidate and baseline bundles use the
anchor as their Skill revision; a previous bundle must use a strict ancestor.
The dataset must not reuse any case ID or prompt hash from repository eval datasets
that existed at the frozen revision. The provenance file binds the dataset hash,
anchor/source revision, post-freeze independent authorship attestation,
`used_for_tuning=false`, and intended hosts; the runner binds its path and hash
to every bundle. The check requires full Git history. This prevents
copy/rename reuse and fails closed when the attestation is absent, but it still
cannot prove that a human never saw the prompts while tuning.

Generate a comparison report only from matched, scored bundles:

```bash
python3 scripts/compare-skill-evals.py \
  --kind routing \
  --dataset path/to/routing-held-out.jsonl \
  --candidate path/to/candidate-trial-1.json \
  --candidate path/to/candidate-trial-2.json \
  --candidate path/to/candidate-trial-3.json \
  --control path/to/previous-trial-1.json \
  --control path/to/previous-trial-2.json \
  --control path/to/previous-trial-3.json \
  --output path/to/comparison-report.json
```

The comparison passes only when every candidate trial passes the normal
contract and either outcome improves by the contract threshold, or outcome
does not regress while measured token use improves by the contract threshold.
Claude input-token totals include cache-creation and cache-read input tokens
when its CLI reports them; the verbatim host output retains that breakdown.
Duration is reported but is not a gate because paired wall-clock samples remain
vulnerable to host-load noise. Means, standard deviations, unavailable token
data, revisions, pair timing, and evidence hashes remain visible in the report.

Do not mark behavior or workflow verified until all required metadata and raw
evidence are present, pass the scorer, appear in the quality evidence manifest,
and are reflected in `docs/quality/status.md`.

The manifest records each dataset and bundle path plus its SHA-256. A comparison
record references validated candidate/control evidence IDs and a self-hashed
report. `claims` is a list of scoped verified assertions; each entry must match
one replayed passing comparison's kind, dimension, host name/version, exact
model, candidate/control revisions, dataset hash, and Skill inventory. Omit
unverified claims. Routing claims also bind the evaluation anchor, dataset Git
revision, and held-out provenance path/hash. The current contract permits
scoped routing outcome or token efficiency claims only; it rejects global
“improvement” wording and authority/workflow claims.
