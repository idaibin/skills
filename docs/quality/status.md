# AICraft Quality Status

This page records verifiable repository evidence. It does not assign subjective
maturity labels or treat format validation as proof of model behavior.

## Evidence Basis

- Recorded: `2026-07-16`
- Evidence revision: the commit containing this file; resolve with
  `git log -1 --format=%H -- docs/quality/status.md`
- Structure host: local repository validator on macOS
- Behavior host and model: `codex-cli 0.144.5` / `gpt-5.6-sol`; the historical
  evaluation-v1 comparison failed, and three preregistered evaluation-v2
  campaign rounds were invalidated before a complete comparison was available
- Workflow host and model: `Not verified`
- Comparative run: historical candidate/previous comparison executed under v1;
  status `FAIL`; required v2 candidate/previous/no-Skill group is `Not verified`
- Held-out provenance: `v1, v2, v3, and v4 datasets are committed, hash-bound, and
  consumed; none is reusable for a successor campaign`

`Structure = verified` means the source package and repository consistency
checks passed. It does not prove live model routing, authority behavior, or
end-to-end task completion.

## Skill Status

| Skill | Functional category | Release | Structure | Behavior | Workflow |
| --- | --- | --- | --- | --- | --- |
| `repo-map` | Core Engineering | available | verified | not_verified | not_verified |
| `domain-modeling` | Core Engineering | available | verified | not_verified | not_verified |
| `code-planner` | Core Engineering | available | verified | not_verified | not_verified |
| `diagnose` | Core Engineering | available | verified | not_verified | not_verified |
| `repo-review` | Core Engineering | available | verified | not_verified | not_verified |
| `repo-delivery` | Core Engineering | available | verified | not_verified | not_verified |
| `design-ui` | Design | available | verified | not_verified | not_verified |
| `implement-rust` | Implementation | available | verified | not_verified | not_verified |
| `implement-frontend` | Implementation | available | verified | not_verified | not_verified |
| `audit-rust` | Specialist Audit | available | verified | not_verified | not_verified |
| `audit-frontend` | Specialist Audit | available | verified | not_verified | not_verified |
| `audit-security` | Specialist Audit | available | verified | not_verified | not_verified |
| `ops-browser` | Runtime Operations | available | verified | not_verified | not_verified |
| `ops-client` | Runtime Operations | available | verified | not_verified | not_verified |
| `chatgpt-review` | External Review | available | verified | not_verified | not_verified |
| `human-writing` | Writing Extension | available | verified | not_verified | not_verified |

Functional category states what a skill owns. Release states whether it is
offered for installation. Validation states only what current evidence proves.

## Structure Evidence

Run from the repository root:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/eval-skill-contracts.py --validate-only
git diff --check
```

Current structure evidence covers package shape, metadata, local references,
repository indexes, routing-graph consistency, documented static eval coverage,
shared protocol synchronization, and validator regression tests. Dataset
minimums, per-Skill coverage, score gates, result metadata, and official-source
freshness are defined by
[`contracts/skill-validation.json`](../../contracts/skill-validation.json).

The routing, authority, and workflow datasets satisfy static schema and coverage
validation at this revision. No passing model-bound evidence is recorded in the
manifest. The historical failed comparison is archived under
[`docs/history/evals/`](../history/evals/2026-07-16-codex-gpt56-routing-comparison.md),
and the three later non-scoring campaigns are recorded in the
[`infrastructure-failure record`](../history/evals/2026-07-16-codex-gpt56-routing-infrastructure-failures.md),
so behavior and workflow remain `not_verified`.

Authority/workflow raw hashes and trace/workspace/verifier bindings are
tamper-evident only under a trusted evidence producer. They do not authenticate
the originating host or independently prove the meaning of self-reported
action/evidence labels. The validator therefore prevents these suites from
setting behavior or workflow to `verified` until an independent semantic
verifier is added.

## Evaluation Contract v2 (No Valid Live Evidence)

The current contract upgrades routing success from primary-owner top-1 to the
complete owner-and-handoff case: accepted owner, every required direct handoff,
exactly one member of every required one-of group, and zero unauthorized or
optional handoffs. It reports unauthorized
handoff entries and affected cases separately and rejects held-out datasets
without both positive required-handoff and correct-empty-handoff coverage.

Improvement evaluation now requires matched candidate, previous, and no-Skill
conditions under one comparison group per trial. Previous establishes
non-regression; no-Skill establishes outcome contribution and removes fixed
host input from the marginal Skill-input metric. Total tokens and duration are
reported but are not discovery-efficiency gates. Formal runs must first commit
a post-anchor campaign that freezes revisions, dataset/provenance, exact trial
groups, canonical policies, a unique artifact root, and the full evaluation
  protocol. A frozen, exact capacity-only retry may retain at most two host
  attempts inside one formal slot; other failures consume their preregistered
  slots. Marginal input
claims require per-group non-increase, 15% relative reduction, and at least 50
  saved tokens per case on average.

Three preregistered evaluation-v2 campaign rounds were started, but none
produced valid comparison evidence. Round v2 made zero model-service calls
because a local Volta isolation defect prevented Codex from starting. After
that defect was fixed, round v3 made 210 host calls: 209 succeeded and one
returned the exact model-capacity error. Round v4 then wrote six attempt
ledgers and 210 raw records under campaign
`eb47a629-8c22-40f5-9c34-70f388f0b736`: five slots succeeded, while trial 2
candidate failed on `v4-heldout-034` after the 120-second timeout (209
exit-code-0 records, one exit-code-124 record, and zero retries). Trial 3 was
not started.
No v3 or v4 score, comparison report, or quality-manifest entry was created,
and complete bundles were not selected or recombined. The v2 and v3 runtime
roots were not committed, so their historical hashes identify capture-time
files but do not make those runs independently reproducible. The v4 failure
root is retained in evidence commit
`207e61c62df5fc044a68aa123707fe4caa56a7c7`. See the
[`2026-07-16 infrastructure-failure record`](../history/evals/2026-07-16-codex-gpt56-routing-infrastructure-failures.md).

## Deterministic Footprint Delta

Compared with repository revision `abebbfc913753b5e67f43e49e47f2b3027391bf2`,
the current source changes produce these deterministic reductions:

| Surface | Baseline | Current | Change |
| --- | ---: | ---: | ---: |
| Frontmatter descriptions | 4,216 characters | 2,999 characters | -28.9% |
| OpenAI default prompts | 7,682 characters | 2,137 characters | -72.2% |
| `SKILL.md` entrypoints | 1,344 lines | 1,169 lines | -13.0% |

Reproduce with
`python3 scripts/measure-skill-footprint.py --baseline-ref abebbfc913753b5e67f43e49e47f2b3027391bf2`.
This is a context-footprint measurement, not a model-behavior, quality, speed,
or token-usage result. Those claims remain `not_verified` until the controlled
comparison contract passes.

## Live Routing Comparison (Historical v1 Failed Gate)

On `2026-07-16`, the Codex runner executed three paired candidate/previous
trials over the 28-case held-out dataset: 168 successful model calls in total.
Contemporaneous local checks reported six complete bundles, with 28 raw
observations each, zero timeouts, zero non-zero exits, and matching host, model,
dataset, provenance, anchor, trial, pair, and revision fields. Those raw
bundles were not committed, so these checks cannot now be independently rerun
from repository contents.

| Measure | Candidate `9c7f6488` | Previous `abebbfc9` | Result |
| --- | ---: | ---: | --- |
| Exact owner outcome | 83/84 (98.81%) | 84/84 (100.00%) | -1.19 percentage points |
| Mean Token use per trial | 380,939 | 387,674 | 1.74% reduction; below the 15% gate |
| Forbidden handoffs | 9 | 4 | candidate did not pass the routing contract |
| Mean duration per trial | 676,536 ms | 662,293 ms | candidate 2.15% slower; duration is not a gate |

The retained comparison-report copy records status `FAIL` with comparison self-hash
`e7b8cf2bbd5b76fcac84bc9ebf0b48c1972269eed4084959e1b37a54dd222519`.
The candidate's first trial also had one owner error (`audit-rust` expected,
`diagnose` returned). The raw bundles were excluded from Git and are not
present in this worktree; only the historical report copy linked below is
retained. Its hashes can detect changes to that retained file, but cannot
reconstruct or authenticate the absent raw bundles. Neither the bundles nor
the failed comparison are registered in `evidence-manifest.json`, and no
verified behavior or improvement claim is made. The held-out cases must not be
used to tune this candidate.

See the
[`2026-07-16 Codex routing comparison`](../history/evals/2026-07-16-codex-gpt56-routing-comparison.md)
for the bound scope, retained report, and repository evidence boundary.

## Unverified Scope

- A passing live v2 full-case routing and neighboring non-trigger contract; v1
  failed its behavior gate, while the v2, v3, and v4 campaign rounds were
  invalidated and not scored
- Authority enforcement under real model/tool execution
- Stop conditions and cross-skill handoff behavior
- End-to-end repository workflow completion and interruption recovery
- Claude Code compatibility
- Technology stacks outside the repository's future recorded workflow corpus
- Scoped comparative routing outcome contribution or marginal Skill-input
  improvement from a v2 candidate/previous/no-Skill group
- Any time improvement claim; duration is reported but not a current gate

Future behavior or workflow verification must bind every raw result to the
model, host, committed Skill revision, exact dataset hash, trial configuration,
adjudication, metrics, and execution evidence, then independently derive the
semantic action/evidence result from the raw host events. A no-Skill baseline is
not required to evaluate contract correctness, but the complete three-condition
group is required before a scoped improvement claim.

See [`validation-plan.md`](validation-plan.md) for the routing, authority, and
workflow evidence phases, and
[`official-skill-alignment.md`](official-skill-alignment.md) for the current
portable, OpenAI, and Claude source baseline.
