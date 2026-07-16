# Codex GPT-5.6 Routing Comparison — 2026-07-16

This is historical negative evidence, not a verified behavior or improvement
claim. The repository comparator returned `FAIL`.

## Bound Scope

- Host: `codex-cli 0.144.1`
- Model: `gpt-5.6-sol`
- Candidate and evaluation anchor:
  `9c7f6488bbcb858f19bb07b1051fc920509c2ec0`
- Previous revision: `abebbfc913753b5e67f43e49e47f2b3027391bf2`
- Dataset: [`evals/routing-held-out.jsonl`](../../../evals/routing-held-out.jsonl)
- Dataset SHA-256:
  `8167b423a035a5c0ec799e25e318c7144cba7e182411bf73d27525c0b3c8c607`
- Dataset Git revision: `c0ba6b09c8f6fdc55cd4bfdcb9b75642f2814595`
- Provenance:
  [`evals/routing-held-out-provenance.json`](../../../evals/routing-held-out-provenance.json)
- Provenance SHA-256:
  `39c8c4d58d0feebc2673881a49f81da89a2dc2f09451cdc07752d1992442aab4`
- Trials: 3 paired candidate/previous trials, 28 cases per side and trial,
  168 successful model calls total
- Pair IDs:
  `d64a2f22-b9b8-4a2e-b1a6-26eddd3fa40f`,
  `91c0598a-3dc2-45d1-9892-46c21b43e97e`, and
  `7e3797e6-0764-45c2-88aa-71d28e0feb3d`

Contemporaneous checks over the local artifacts reported six complete bundles,
28 results and 28 raw records per bundle, zero timeouts, zero non-zero exits,
and matching host, model, dataset, provenance, anchor, pair, trial, and revision
fields. The raw bundles were not committed, so those checks cannot now be
independently replayed from repository contents.

## Result

| Measure | Candidate | Previous | Comparison |
| --- | ---: | ---: | --- |
| Exact owner outcome | 83/84 (98.8095%) | 84/84 (100.0000%) | -1.1905 percentage points |
| Mean Token use per trial | 380,939 | 387,674 | 1.7374% reduction; required 15% |
| Forbidden handoffs | 9 | 4 | zero required |
| Mean duration per trial | 676,536 ms | 662,293 ms | candidate 2.15% slower; not a gate |

- `candidate_contracts_passed = false`
- `improvement_gate_met = false`
- All three candidate trials violated the zero-forbidden-handoff contract.
- Candidate trial 1 also routed one `audit-rust` case to `diagnose`, leaving
  `audit-rust` at 1/2 for that trial.
- Previous trials also failed the zero-forbidden-handoff contract, but their
  exact owner outcome remained 84/84.

The retained comparator-output copy is archived as
[`2026-07-16-codex-gpt56-routing-comparison-report.json`](2026-07-16-codex-gpt56-routing-comparison-report.json).
Its comparison self-hash is
`e7b8cf2bbd5b76fcac84bc9ebf0b48c1972269eed4084959e1b37a54dd222519`;
the archived file SHA-256 is
`7ce30a344f5e3cf5e1bf2be7c871fff83edc16a2ab3c3de408bb4cf8e55687f4`.

## Evidence Boundary

The six raw bundles were written under the ignored
`eval-results/routing/codex-gpt56-v3/` path, were not committed, and are not
present in this worktree. The archived report and its hashes can detect changes
to that retained copy, but cannot reconstruct the missing bundles, authenticate
their producer, or independently reproduce the comparison. Because the
candidate did not pass its normal contract, neither the bundles nor this
comparison are registered in `docs/quality/evidence-manifest.json`, whose
claims remain empty. The held-out cases were not used to tune the candidate
after this result.
