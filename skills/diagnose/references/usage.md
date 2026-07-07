# Diagnose Usage

## Summary

Use `diagnose` when there is a concrete failure to understand before editing code. It covers bugs, failed tests, build failures, regressions, flaky behavior, and performance problems.

## Best For

- Reproducing a reported bug before fixing it.
- Turning a failing command into a minimal red/green loop.
- Debugging flaky tests or timing-sensitive behavior.
- Investigating build, integration, or runtime regressions.
- Measuring and isolating a performance regression.

## Trigger Examples

- `Diagnose why this test fails before changing code.`
- `Debug this regression; do not guess a fix.`
- `This page is sometimes blank; find the root cause.`
- `The build started failing after the last change.`
- `This endpoint got slow; measure first, then fix.`
- `It only fails sometimes; make it reproducible.`

## Non-Triggers

- Repository onboarding or command discovery without a failure; use `code-context`.
- Planning a new feature; use `code-planner`.
- Reviewing existing local changes for commit safety; use `code-review`.
- Browser operation or screenshots without repository diagnosis; use `ops-browser`.
- Frontend implementation after the cause is known; use `frontend-implementation`.

## Output

Expect a named feedback loop, exact reproduction evidence, minimized scenario, ranked hypotheses, probes, root cause or `Not verified`, fix scope, regression coverage, cleanup status, and remaining risk.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`.
