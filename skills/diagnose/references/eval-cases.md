# Eval Cases

Use these cases when changing `diagnose` triggers, investigation workflow, implementation handoff, output contract, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Diagnose why this test fails before changing code.` | Trigger `diagnose`. | Concrete failing-test investigation. |
| `Find the root cause and recommend the smallest fix, but leave the worktree unchanged.` | Trigger `diagnose` and remain read-only. | Explicit investigation boundary. |
| `Find the regression commit, but do not change my checkout, index, branch, or refs.` | Use read-only revision comparison; checkout-based bisection requires a separately authorized isolated workflow. | Git-state boundary. |
| `Diagnose and fix this failing build, then rerun the original command.` | Trigger `diagnose` first, then hand the confirmed cause to the matching implementation skill before any permanent edit. | One request authorizes two explicit phases, not mixed ownership. |
| `This compiler error is deterministic; use the smallest feedback loop and do not start a broad investigation.` | Trigger deterministic fast path. | Bounded reproducible failure. |
| `Debug this regression; do not guess a fix.` | Trigger `diagnose`. | Root-cause workflow before implementation. |
| `This page is sometimes blank; make it reproducible.` | Trigger flaky/timing investigation. | Non-deterministic failure. |
| `This endpoint got slow; measure the cause before changing it.` | Trigger performance investigation. | Comparable baseline required. |
| `This Rust import path keeps growing in memory; reproduce it and distinguish a leak from allocator or OS retention before proposing changes.` | Trigger `diagnose`. | A concrete observed symptom has an unknown cause. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository's real commands and directory structure first.` | Prefer `repo-map`. | Repository mapping without concrete failure. |
| `Plan the implementation across three packages.` | Prefer `code-planner`. | Future work planning. |
| `Review all dirty changes and split commits.` | Prefer `repo-review`. | Dirty-tree review and staging plan. |
| `Verify this page in the browser and collect console/network evidence.` | Prefer `ops-browser`. | Browser operation task. |
| `The cause is already confirmed; implement the frontend fix now.` | Prefer `implement-frontend`. | No diagnosis remains. |
| `The cause is already confirmed; implement the Rust fix now.` | Prefer `implement-rust`. | No diagnosis remains. |
| `Reproduce this already-isolated release-client window failure and return process/window evidence only.` | Prefer `ops-client`. | Bounded client operation after isolation. |
| `Audit this already selected Rust memory path and assess whether the profiling and benchmark design can support a performance claim.` | Prefer `audit-rust`. | The Rust surface is known and the request is a scoped audit of measurement design, not root-cause isolation of a symptom. |
| `Stage and commit the verified fix.` | Prefer `repo-delivery`. | Git mutation is not diagnosis. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Failure classification | Classifies deterministic/local, regression/cross-boundary, flaky/timing, or performance before selecting depth. | Uses the same broad workflow for every compiler error, flake, and performance issue. |
| Read-only ownership | Keeps tracked files, index, checkout, refs, branches, and permanent docs/tests unchanged under `diagnose`. | Treats diagnosis or diagnose-and-fix wording as permission to edit inside this skill. |
| Two-phase fix request | For a combined diagnose-and-fix request, confirms the root cause and then explicitly transitions to the matching implementation skill with a bounded handoff. | Applies permanent remediation before confirmation or claims implementation ownership. |
| Git investigation boundary | Uses logs, shows, diffs, and existing-ref comparisons read-only; isolates separately authorized checkout-based bisection away from the target checkout. | Runs bisect/checkout/reset/worktree/ref mutation in the target checkout. |
| Deterministic fast path | Reads the complete diagnostic, reproduces the exact command once, traces the smallest owner, and tests the direct cause before expanding. | Generates decorative hypotheses or edits from the final error line. |
| Feedback loop | Names a command, request, browser/client evidence loop, replay, or harness that goes red/green on the exact symptom. | Proposes remediation from inspection alone. |
| Reproduction | Confirms the loop catches the reported symptom. | Diagnoses a nearby failure and treats it as equivalent. |
| Minimization | Removes variables one at a time only when the failure class requires it. | Bundles condition changes or over-minimizes a fully bounded error. |
| Hypotheses | Uses one direct evidenced hypothesis for bounded failures or ranked alternatives with distinct predictions for broader failures. | Anchors on an unproven cause or lists hypotheses with no falsification condition. |
| Instrumentation | Uses read-only probes or task-owned temporary artifacts, tags them, and cleans or reports them. | Edits tracked files or leaves unexplained artifacts. |
| Root-cause evidence | Connects the confirmed cause to the exact bad value, state, contract, timing, dependency, ownership, or runtime boundary. | Labels correlation as cause. |
| Regression seam | Identifies the test or assertion that fails before and passes after the proposed fix. | Recommends a shallow test unrelated to the original symptom. |
| Implementation handoff | Includes confirmed cause, affected owner, bounded scope, do-not-touch paths, original loop, regression seam, validation, and gaps. | Hands off a vague `fix it` instruction. |
| Performance evidence | Uses comparable release-like workload, inputs, environment, repetitions, and measurements. | Claims a cause or improvement from debug builds, one run, or changed inputs. |
| Final integrity | Reports initial/final worktree, index, checkout, refs, cleanup, and `Not verified` gaps. | Claims completion without proving investigation state remained intact. |
| Publish readiness | Keeps `SKILL.md`, references, metadata, and evals synchronized and validates the package. | Updates only one surface or preserves stale Diagnose-and-fix semantics. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
