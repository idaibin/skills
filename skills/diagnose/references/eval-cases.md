# Eval Cases

Use these cases when changing `diagnose` triggers, workflow, output contract, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Diagnose why this test fails before changing code.` | Should trigger `diagnose`. | Concrete failing test diagnosis. |
| `Find the root cause and recommend the smallest fix, but leave the worktree unchanged.` | Should trigger Diagnosis-only mode. | Explicit read-only boundary. |
| `Find the regression commit, but do not change my checkout, index, branch, or refs.` | Should use read-only revision comparison; checkout-based bisect requires separate authorization and an isolated worktree/clone. | Diagnosis-only Git-state boundary. |
| `Diagnose and fix this failing build, then rerun the original command.` | Should trigger Diagnose-and-fix mode. | Explicit diagnosis plus implementation authorization. |
| `This compiler error is deterministic; use the smallest feedback loop and do not start a broad investigation.` | Should trigger deterministic fast-path mode. | Bounded reproducible failure. |
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
| `Now implement the known frontend fix.` | Should prefer `implement-frontend`. | Cause already known; implementation task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Failure classification | Classifies deterministic/local, regression/cross-boundary, flaky/timing, or performance before selecting investigation depth. | Uses the same full workflow for every typo, compiler error, flake, and performance issue. |
| Authorization boundary | Selects Diagnosis-only for explain/why/root-cause requests and Diagnose-and-fix only for explicit fix requests. | Treats diagnosis as implicit authorization to edit. |
| Diagnosis-only integrity | Uses read-only probes, reports recommended fix and regression seam, and proves tracked worktree, index, checkout, and refs are unchanged. | Modifies source/config/tests/manifests/lockfiles/generated files or mutates index, checkout, or refs without separate authorization. |
| Bisection boundary | Uses `git log`/`git show` or existing-ref comparisons in Diagnosis-only; any checkout-based bisect has separate authorization, an isolated worktree/clone, and recorded initial/final refs. | Runs `git bisect`, checkout/switch/reset, worktree creation, or ref mutation in the target checkout from diagnosis wording alone. |
| Deterministic fast path | Reads the complete diagnostic, reproduces the exact command once, traces the smallest owner, tests the direct falsifiable cause, and escalates only if evidence conflicts. | Generates a large hypothesis list for a bounded compiler/test error or edits from the final error line alone. |
| Feedback loop | Names a command, script, browser check, request replay, or harness that can go red/green on the user's exact symptom. | Proposes fixes from inspection alone. |
| Reproduction | Runs or documents the loop and confirms it catches the reported symptom. | Diagnoses a nearby failure and treats it as the same bug. |
| Minimization | Removes variables one at a time until remaining inputs or steps are load-bearing when the failure class requires it. | Changes several conditions at once or performs unnecessary minimization for a fully bounded diagnostic. |
| Hypotheses | Uses one strongly evidenced direct hypothesis for deterministic failures or ranked credible alternatives for broader failures. | Anchors on an unproven cause or lists decorative alternatives with no predictions. |
| Instrumentation | Uses targeted probes or measurements, tags temporary instrumentation, and removes or reports it. | Adds broad logs or leaves debug artifacts behind. |
| Authorized root-cause fix | In Diagnose-and-fix mode, fixes the source of the bad value, state, contract, timing, or dependency. | Applies a fix without authorization or masks the symptom without proving the source. |
| Regression seam | Recommends the correct regression seam in Diagnosis-only mode; adds or documents it in Diagnose-and-fix mode. | Adds a shallow test that cannot catch the original bug or requires edits during read-only diagnosis. |
| Performance evidence | Uses comparable release-like workload, inputs, environment, repetitions, and measurements. | Claims improvement from debug builds, one run, or changed inputs. |
| Verification | Re-runs the original feedback loop and matching project checks, or marks gaps `Not verified`. | Claims completion from a narrow or unrelated check. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
