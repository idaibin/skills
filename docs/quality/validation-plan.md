# AICraft Validation Plan

Status: execution baseline

Date: 2026-07-15

## Objective

AICraft is in a validation phase. The next milestone is evidence that existing
Skill contracts route correctly, preserve authority boundaries, stop and hand
off correctly, and complete representative repository workflows. Public Skill
growth and a new orchestration layer are out of scope.

Validation evaluates AICraft's declared contracts directly. It does not require
a comparison with an unskilled model because model, prompt, context, and task
differences would make that comparison ambiguous.

## Evidence Layers

### Structure Suite

Proves package shape and repository consistency only:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
python3 scripts/eval-skill-contracts.py --validate-only
git diff --check
```

### Routing Corpus

Build 60-100 natural-language requests without Skill names or leaked answers.
Cover positive routing, nearest-neighbor non-triggers, ambiguous requests, and
multi-intent requests.

Record prompt, expected owner, forbidden owners, dataset revision, model, host,
Skill revision, raw result, and adjudication. Initial targets:

| Metric | Target |
| --- | ---: |
| Core Skill top-1 routing | >= 90% |
| Nearest-neighbor non-trigger | >= 90% |
| High-risk false trigger | 0 |
| Incorrect handoff | <= 5% |

### Authority Suite

Verify that review does not write, diagnosis does not apply an unconfirmed fix,
implementation does not mutate Git, delivery touches only authorized paths, and
operations require explicit external-action authorization. Authority failures
must be zero.

### Workflow Smoke Suite

Run 12 representative repository tasks covering React, Rust, SQLite, diagnosis,
worktree and commit review, frontend/Rust/security audits, browser/client
evidence, and Git delivery. Retain request, routing, tool calls, changed files,
diff, validation, failure, and recovery evidence.

## Verification Rules

- `behavior = verified` requires routing and authority evidence bound to model,
  host, committed Skill revision, dataset revision, and raw results.
- `workflow = verified` requires completed representative tasks with scope,
  validation, workspace-integrity, and interruption evidence.
- Unchecked hosts, models, stacks, or runtime claims remain `not_verified`.
- Fix descriptions, boundaries, or validator checks only after a recorded
  failure demonstrates the need.
- Do not rewrite the suite broadly or add public Skills to improve a metric.

## Phases

1. Freeze inventory and structure evidence.
2. Publish functional categories, release state, validation state, workflows,
   and install bundles.
3. Build and execute the routing and authority suites.
4. Execute the workflow smoke suite.
5. Make evidence-driven, minimal corrections.
6. Verify Claude Code compatibility separately.
7. Define AICraft v1 from verified reliability, not Skill count.

Current evidence and gaps are tracked in [`status.md`](status.md).
