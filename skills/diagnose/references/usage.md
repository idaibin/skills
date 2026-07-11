# Diagnose Usage

## Summary

Use `diagnose` when there is a concrete failure to understand. Diagnosis-only is the default for root-cause requests; Diagnose-and-fix requires an explicit request to apply the remediation.

## Best For

- Reproducing a reported bug before fixing it.
- Turning a failing command into a minimal red/green loop.
- Debugging flaky tests or timing-sensitive behavior.
- Investigating build, integration, or runtime regressions.
- Measuring and isolating a performance regression.

## Trigger Examples

- `Diagnose why this test fails before changing code.`
- `Debug this regression; do not guess a fix.`
- `Find the root cause and report the smallest fix, but leave the worktree unchanged.`
- `Diagnose and fix this failing build, then rerun the original command.`
- `This page is sometimes blank; find the root cause.`
- `The build started failing after the last change.`
- `This endpoint got slow; measure first, then fix.`
- `It only fails sometimes; make it reproducible.`

## Non-Triggers

- Repository onboarding or command discovery without a failure; use `code-context`.
- Planning a new feature; use `code-planner`.
- Reviewing existing local changes for commit safety; use `code-review`.
- Browser operation or screenshots without repository diagnosis; use `ops-browser`.
- Frontend implementation after the cause is known; use `implement-frontend`.

## Output

Expect the authorization boundary, named feedback loop, exact reproduction evidence, minimized scenario when needed, ranked hypotheses, probes, root cause or `Not verified`, recommended or applied fix scope, regression seam, initial/final worktree, index, checkout and ref state, cleanup status, and remaining risk.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`.
