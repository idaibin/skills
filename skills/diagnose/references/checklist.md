# Diagnose Checklist

Use this checklist when diagnosing concrete failures.

## Execution Boundary

- Select Diagnosis-only for explain, why, root-cause, investigate, or before-changing-code requests.
- Select Diagnose-and-fix only when the user explicitly asks to fix, resolve, repair, or apply the remediation.
- In Diagnosis-only mode, keep tracked repository files, index, checkout, and Git refs unchanged. Use read-only probes or ask before tracked instrumentation or Git-state mutation.
- Record the initial and final worktree status, `HEAD`, and branch/detached state so a read-only diagnosis is auditable.

## Required Context

- Read relevant repo guidance first.
- Run `git status --short`.
- Identify the exact user symptom, expected behavior, actual behavior, environment, command, URL, input, account state, or artifact.
- Read the full error output, stack trace, failing assertion, console message, or timing data before summarizing.
- Check recent local diffs, recent commits, dependency/config changes, and environment differences when relevant.

## Feedback Loop

- Prefer the smallest agent-runnable loop that can go red and green:
  - failing unit, integration, or e2e test
  - repo command with a focused assertion
  - curl or HTTP script against a dev server
  - CLI invocation with fixture input and expected output
  - browser script or DOM/console/network assertion
  - replayed request, payload, trace, or event log
  - minimal harness around the failing function or service
  - read-only differential comparison between known-good and known-bad states
- In Diagnosis-only mode, do not run `git bisect`, checkout/switch/reset, create a worktree, or mutate refs without separate authorization. When authorized, run checkout-based bisection in an isolated disposable worktree/clone and record its initial/final refs; never alter the target checkout implicitly.
- Make the loop specific to the user's symptom. A generic "command exits 0" is not enough.
- For flaky failures, loop the trigger, pin seeds/time where possible, stress the suspected path, and report reproduction rate.
- If no loop can be built, report what was tried and the missing artifact or access needed.

## Reproduce And Minimize

- Run the loop at least once before hypothesizing.
- Confirm the loop catches the same symptom the user reported.
- Remove steps, inputs, callers, config, data, viewport, account/cache state, or timing assumptions one at a time.
- Stop minimizing when every remaining element is load-bearing.

## Hypothesize And Probe

- Generate 3-5 ranked falsifiable hypotheses unless the evidence already proves one root cause.
- State the prediction for each hypothesis.
- Probe one variable at a time with debugger/REPL inspection, targeted logs, trace data, profiler output, query plans, or focused assertions.
- Tag temporary instrumentation with a unique prefix and remove it before delivery.
- For performance regressions, measure baseline first; do not use logs as the primary profiler when real timing or profile data is available.

## Recommend Or Fix

- In Diagnosis-only mode, report the smallest remediation and correct regression seam without applying them.
- In Diagnose-and-fix mode, fix the confirmed source of the bad value, state, contract, timing, or dependency.
- Add a regression test at the real seam only when fixes are authorized; otherwise recommend it.
- If no correct seam exists, document that gap as an architectural risk.
- After an authorized fix, rerun the original feedback loop, not only the minimized case, plus matching project-defined checks.
- Remove or report temporary probes, debug scripts, screenshots, downloads, local files, and tagged logs.

## Stop Conditions

- Stop and ask for evidence when the failure cannot be reproduced and no artifact is available.
- Stop after three failed fix attempts or when each fix reveals new coupling; report the architecture concern before continuing.
- Mark unverified root cause, runtime behavior, or missing regression coverage as `Not verified`.
