# Eval Cases

Use these cases when changing `diagnose` triggers, workflow, output contract, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Diagnose why this test fails before changing code.` | Should trigger `diagnose`. | Concrete failing test diagnosis. |
| `Debug this regression; do not guess a fix.` | Should trigger `diagnose`. | Root-cause workflow before implementation. |
| `This page is sometimes blank; make it reproducible.` | Should trigger `diagnose`. | Flaky or non-deterministic failure. |
| `The build started failing after the last change.` | Should trigger `diagnose`. | Build failure with likely recent cause. |
| `This endpoint got slow; measure first, then fix.` | Should trigger `diagnose`. | Performance regression requiring measurement. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding without concrete failure. |
| `Plan the implementation across three packages.` | Should prefer `code-planner`. | Future work planning. |
| `Review all dirty changes and split commits.` | Should prefer `code-review`. | Dirty-tree review and staging plan. |
| `Verify this page in the browser and collect console/network evidence.` | Should prefer `ops-browser`. | Browser operation task. |
| `Now implement the known frontend fix.` | Should prefer `frontend-implementation`. | Cause already known; implementation task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Feedback loop | Names a command, script, browser check, request replay, or harness that can go red/green on the user's exact symptom. | Proposes fixes from inspection alone. |
| Reproduction | Runs or documents the loop and confirms it catches the reported symptom. | Diagnoses a nearby failure and treats it as the same bug. |
| Minimization | Removes variables one at a time until remaining inputs or steps are load-bearing. | Changes several conditions at once or keeps broad setup unexplained. |
| Hypotheses | Lists ranked falsifiable hypotheses with predictions before probing. | Anchors on the first plausible cause without alternatives. |
| Instrumentation | Uses targeted probes or measurements, tags temporary instrumentation, and removes or reports it. | Adds broad logs or leaves debug artifacts behind. |
| Root-cause fix | Fixes the source of the bad value, state, contract, timing, or dependency. | Masks the symptom without proving the source. |
| Regression coverage | Adds a regression test at the real seam or documents why no correct seam exists. | Adds a shallow test that cannot catch the original bug. |
| Verification | Re-runs the original feedback loop and matching project checks, or marks gaps `Not verified`. | Claims completion from a narrow or unrelated check. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
