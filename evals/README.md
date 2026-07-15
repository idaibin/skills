# AICraft Behavior Evaluation Data

These datasets evaluate declared Skill contracts directly. They do not compare
AICraft with a no-skill baseline.

## Files

- `routing.jsonl`: natural-language owner-selection and handoff cases.
- `authority.jsonl`: mutation and external-action boundary cases.
- `workflow-smoke.jsonl`: representative end-to-end task specifications.

Prompts in routing data must not name a Skill. Expected and forbidden owners are
labels used only by the evaluator after the model response is captured.

## Validate Datasets

```bash
python3 scripts/eval-skill-contracts.py --validate-only
```

Validation proves only schema, inventory, uniqueness, prompt leakage checks, and
coverage counts. It does not execute a model.

## Score Captured Results

Routing and authority result files are JSON objects:

```json
{
  "model": "exact model identifier",
  "host": "exact host and version",
  "skill_revision": "committed Git SHA",
  "dataset_revision": "committed Git SHA or dataset hash",
  "captured_at": "ISO-8601 timestamp",
  "results": [
    {
      "id": "route-001",
      "actual_owner": "repo-map",
      "handoffs": [],
      "raw_evidence": "raw/routing/route-001.json"
    }
  ]
}
```

Authority results use `observed_actions` instead of owner handoffs. Raw model
output and tool traces should be retained beside the result file; the scorer
does not invent or infer observations.

```bash
python3 scripts/eval-skill-contracts.py \
  --routing-results path/to/routing-results.json \
  --authority-results path/to/authority-results.json
```

Do not mark behavior or workflow verified until all required metadata and raw
evidence are present and the committed evidence is reflected in
`docs/quality/status.md`.
