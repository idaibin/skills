---
name: diagnose
description: "Use when a concrete bug, failed check, regression, flake, or performance symptom needs read-only root-cause isolation before any fix; reproduce it, test falsifiable hypotheses, and confirm the cause or exact evidence gap."
---

# Diagnose

## Overview

Diagnose technical failures with a tight evidence loop. Reproduce the user's exact symptom, minimize the failing conditions when necessary, test one falsifiable hypothesis at a time, and confirm the root cause or the precise evidence gap. This skill owns investigation, not permanent remediation: when the user also requested a fix, hand the confirmed cause and regression seam to the matching implementation skill.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Record `git status --short --branch`, current `HEAD`, and the checked-out branch or detached state before experiments.
3. Identify the exact symptom, expected behavior, observed behavior, environment, input, command, URL, runtime state, or artifact.
4. Classify the failure:
   - **Deterministic/local:** one command or test fails consistently with a specific error and bounded ownership.
   - **Regression/cross-boundary:** behavior changed across modules, interfaces, data, configuration, or runtime layers.
   - **Flaky/timing:** reproduction is intermittent or order-, load-, clock-, or concurrency-sensitive.
   - **Performance:** latency, throughput, CPU, allocation, I/O, or memory changed and needs a comparable baseline.
5. Build the smallest red/green feedback loop that exercises the user's exact symptom.
6. For deterministic/local failures, read the complete diagnostic, reproduce once, trace the smallest owning path, and test the most direct falsifiable cause before expanding.
7. For regression, flaky, or performance failures, reproduce and minimize until the remaining inputs, steps, configuration, and state are load-bearing.
8. Rank falsifiable hypotheses before probing. A deterministic compiler or test error may start with one strongly evidenced hypothesis; broader failures require credible alternatives with distinct predictions.
9. Inspect or instrument one variable at a time using read-only probes or task-owned temporary artifacts. Do not modify tracked repository files, the index, checkout, or refs under this skill.
10. Stop after confirming the root cause or exact evidence gap. Remove temporary artifacts, prove tracked worktree/index/checkout/refs remain at their recorded state, and define the smallest remediation plus regression seam.
11. If the user explicitly requested a fix, transition to the matching `implement-*` skill with a handoff containing the confirmed cause, affected owner, required change, regression test seam, original feedback loop, constraints, and validation. Do not apply the permanent fix inside `diagnose`.

## Modes

- **Deterministic fast path:** reproduce the exact command, read the complete diagnostic, trace the owning symbol/config/contract, and test the direct cause.
- **Regression investigation:** compare known-good and known-bad evidence without mutating the target checkout; use checkout-based bisection only through a separately authorized isolated workflow.
- **Flaky investigation:** raise reproduction rate with loops, stress, seeded inputs, controlled clocks, or narrowed timing windows before claiming cause.
- **Performance investigation:** establish a production-like baseline, then profile or compare one variable at a time with comparable inputs and environments.
- **Implementation handoff:** when the original request includes fixing, return a verified handoff to the matching implementation skill after diagnosis completes.

## Do Not Use For

- First-pass repository discovery without a concrete failure; use `repo-map`.
- Future implementation planning before a failure or bug exists; use `code-planner`.
- Existing local diff review, staging plans, commit grouping, or pre-commit review; use `repo-review`.
- Browser-only operation, screenshots, console, network, uploads, downloads, or session evidence; use `ops-browser`. Combine browser evidence with this skill only when the root cause crosses code or runtime boundaries.
- Implementing a known fix when no diagnosis remains; use the matching `implement-*` skill.
- Staging, commits, pushes, branch changes, or delivery; use `repo-delivery` after implementation and review.

## Hard Rules

- A request to explain, debug, find, diagnose, or confirm a cause never authorizes permanent code changes.
- Even when the user asks to diagnose and fix in one request, complete diagnosis first and explicitly transition ownership to the matching implementation skill before edits.
- Do not modify tracked source, config, tests, manifests, lockfiles, generated files, documentation, the index, checkout, or Git refs under this skill.
- Do not run `git bisect`, `checkout`, `switch`, `reset`, worktree creation, or another ref/checkout mutation in the target checkout. A separately authorized isolated bisection workflow must record initial/final refs and leave the target checkout untouched.
- Do not recommend a fix until a feedback loop or explicit missing-evidence report exists.
- The loop must target the user's exact symptom, not a nearby crash or generic health check.
- Read the complete failing diagnostic before drawing conclusions; do not react to the final line only.
- If the issue is non-deterministic, improve reproduction rate before claiming a cause.
- Test one hypothesis at a time; do not bundle cache clearing, dependency changes, code edits, and configuration changes into one experiment.
- Prefer the source of the bad value, state, contract, timing, or dependency over masking the symptom in the remediation handoff.
- Tag temporary logs, probes, scripts, screenshots, and artifacts so they can be removed or reported.
- Escalate from the deterministic fast path when the direct cause does not explain all observed evidence, the failure moves, or multiple owners share the contract.
- If three materially different diagnostic hypotheses are falsified or each probe reveals new coupling, stop and report the architectural concern before broadening further.
- Mark unavailable commands, missing repro artifacts, unchecked runtime behavior, and unconfirmed root causes as `Not verified`.
- Do not claim a performance improvement from debug builds, one run, changed inputs, or incomparable environments.

## Output Contract

Report the failure class, exact red/green loop, reproduction evidence, minimized scenario when required, ranked hypotheses, probes run, confirmed root cause or `Not verified` gap, smallest remediation scope, regression seam, commands run, initial/final worktree/index/checkout/ref state, temporary-artifact cleanup, escalation decisions, and remaining risk. When a fix was requested, include the target implementation skill and a bounded implementation handoff; do not claim the fix was applied under `diagnose`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for the diagnosis loop and handoff checklist.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, non-trigger, and quality evals.
