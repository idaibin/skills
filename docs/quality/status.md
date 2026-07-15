# AICraft Quality Status

This page records verifiable repository evidence. It does not assign subjective
maturity labels or treat format validation as proof of model behavior.

## Evidence Basis

- Recorded: `2026-07-16`
- Evidence revision: the commit containing this file; resolve with
  `git log -1 --format=%H -- docs/quality/status.md`
- Structure host: local repository validator on macOS
- Behavior host and model: `Not verified`
- Workflow host and model: `Not verified`
- Comparative previous/no-Skill run: `Not verified`
- Held-out provenance: `Committed and hash-bound; live evaluation not verified`

`Structure = verified` means the source package and repository consistency
checks passed. It does not prove live model routing, authority behavior, or
end-to-end task completion.

## Skill Status

| Skill | Functional category | Release | Structure | Behavior | Workflow |
| --- | --- | --- | --- | --- | --- |
| `repo-map` | Core Engineering | available | verified | not_verified | not_verified |
| `code-planner` | Core Engineering | available | verified | not_verified | not_verified |
| `diagnose` | Core Engineering | available | verified | not_verified | not_verified |
| `repo-review` | Core Engineering | available | verified | not_verified | not_verified |
| `repo-delivery` | Core Engineering | available | verified | not_verified | not_verified |
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
validation at this revision. No model-bound evidence manifest is recorded, so
behavior and workflow remain `not_verified`.

Authority/workflow raw hashes and trace/workspace/verifier bindings are
tamper-evident only under a trusted evidence producer. They do not authenticate
the originating host or independently prove the meaning of self-reported
action/evidence labels. The validator therefore prevents these suites from
setting behavior or workflow to `verified` until an independent semantic
verifier is added.

## Deterministic Footprint Delta

Compared with repository revision `abebbfc913753b5e67f43e49e47f2b3027391bf2`,
the current source changes produce these deterministic reductions:

| Surface | Baseline | Current | Change |
| --- | ---: | ---: | ---: |
| Frontmatter descriptions | 4,216 characters | 3,135 characters | -25.6% |
| OpenAI default prompts | 7,682 characters | 2,077 characters | -73.0% |
| `SKILL.md` entrypoints | 1,344 lines | 1,169 lines | -13.0% |

Reproduce with
`python3 scripts/measure-skill-footprint.py --baseline-ref abebbfc913753b5e67f43e49e47f2b3027391bf2`.
This is a context-footprint measurement, not a model-behavior, quality, speed,
or token-usage result. Those claims remain `not_verified` until the controlled
comparison contract passes.

## Unverified Scope

- Live top-1 routing and neighboring non-trigger accuracy
- Authority enforcement under real model/tool execution
- Stop conditions and cross-skill handoff behavior
- End-to-end repository workflow completion and interruption recovery
- Claude Code compatibility
- Technology stacks outside the repository's future recorded workflow corpus
- Scoped comparative routing outcome or token improvement over a previous/no-Skill run
- Any time improvement claim; duration is reported but not a current gate

Future behavior or workflow verification must bind every raw result to the
model, host, committed Skill revision, exact dataset hash, trial configuration,
adjudication, metrics, and execution evidence, then independently derive the
semantic action/evidence result from the raw host events. A baseline is not
required to evaluate contract correctness, but it is required before a scoped
improvement claim over the previous or no-Skill condition.

See [`validation-plan.md`](validation-plan.md) for the routing, authority, and
workflow evidence phases, and
[`official-skill-alignment.md`](official-skill-alignment.md) for the current
portable, OpenAI, and Claude source baseline.
