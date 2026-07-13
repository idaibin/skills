# Diagnose Usage

## Summary

Use `diagnose` when there is a concrete technical failure to understand. It owns reproduction, minimization, hypothesis testing, root-cause confirmation, and definition of the regression seam. It remains read-only for tracked repository and Git state. When the user also requests a fix, finish diagnosis and hand the verified remediation to the matching implementation skill.

## Best For

- Reproducing a reported bug before changing permanent code.
- Turning a failing command into a minimal red/green loop.
- Debugging flaky tests or timing-sensitive behavior.
- Investigating build, integration, runtime, or configuration regressions.
- Measuring and isolating a performance regression.
- Producing a verified implementation handoff rather than guessing a fix.

## Trigger Examples

- `Diagnose why this test fails before changing code.`
- `Debug this regression; do not guess a fix.`
- `Find the root cause and report the smallest fix, but leave the worktree unchanged.`
- `Diagnose this failing build, then hand the confirmed fix to the implementation workflow.`
- `This page is sometimes blank; make the problem reproducible.`
- `The build started failing after the last change.`
- `This endpoint got slow; measure and isolate the cause first.`

A request such as `diagnose and fix` authorizes the later implementation phase, but it does not merge implementation ownership into `diagnose`. The workflow transitions explicitly after root-cause confirmation.

## Non-Triggers

- Repository onboarding, command discovery, reuse inventory, or docs/code alignment without a failure; use `repo-map`.
- Planning a new feature; use `code-planner`.
- Reviewing existing local changes for commit safety; use `repo-review`.
- Browser operation or screenshots without repository diagnosis; use `ops-browser`.
- Implementing a fix whose cause is already known; use the matching `implement-*` skill.
- Staging, commit, push, or branch mutation; use `repo-delivery`.

## Implementation Handoff

When the user requested a fix, the diagnosis output should hand off:

- confirmed root cause and supporting evidence;
- affected owner, symbol, config, contract, or runtime boundary;
- smallest permanent remediation scope;
- original red/green loop and minimized reproduction;
- required regression test seam;
- constraints and do-not-touch boundaries;
- expected validation and remaining `Not verified` gaps.

The matching implementation skill applies the change and reruns the original loop. `diagnose` does not claim that work as its own.

## Output

Expect the failure class, named feedback loop, exact reproduction evidence, minimized scenario when needed, ranked hypotheses, probes, confirmed root cause or `Not verified`, remediation scope, regression seam, initial/final worktree/index/checkout/ref state, cleanup status, implementation handoff when requested, and remaining risk.

## Maintenance

Keep `SKILL.md`, this usage guide, checklist, eval cases, and `agents/openai.yaml` synchronized. Validate with `python3 scripts/validate-skills.py --skill diagnose`.
