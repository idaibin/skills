# AICraft Quality Status

This page records verifiable repository evidence. It does not assign subjective
maturity labels and does not compare AICraft with a no-skill baseline.

## Evidence Basis

- Recorded: `2026-07-15`
- Previous baseline: `fac9f4efbb27e07094812114a042bc4937e2222c`
- Evidence revision: the commit containing this file; resolve with
  `git log -1 --format=%H -- docs/quality/status.md`
- Structure host: local repository validator on macOS
- Behavior host and model: `Not verified`
- Workflow host and model: `Not verified`

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
python3 scripts/test_validate_skills.py
python3 scripts/eval-skill-contracts.py --validate-only
git diff --check
```

Current structure evidence covers package shape, metadata, local references,
repository indexes, routing-graph consistency, documented static eval coverage,
shared protocol synchronization, and validator regression tests.

The behavior datasets currently contain 60 routing cases, 15 authority cases,
and 12 workflow smoke specifications. Their schemas and coverage validate, but
no model-bound result bundle has been recorded, so behavior and workflow remain
`not_verified`.

## Unverified Scope

- Live top-1 routing and neighboring non-trigger accuracy
- Authority enforcement under real model/tool execution
- Stop conditions and cross-skill handoff behavior
- End-to-end repository workflow completion and interruption recovery
- Claude Code compatibility
- Technology stacks outside the repository's future recorded workflow corpus

Future behavior or workflow verification must bind the raw result to the model,
host, committed Skill revision, dataset revision, and execution evidence. A
comparison against an unskilled model is not required.

See [`validation-plan.md`](validation-plan.md) for the routing, authority, and
workflow evidence phases.
