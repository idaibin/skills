---
name: diagnose
description: Use when diagnosing bugs, failing tests, build failures, unexpected behavior, regressions, flaky behavior, or performance problems to reproduce, isolate, and confirm root causes before any requested fix.
---

# Diagnose

## Overview

Diagnose technical failures with a tight feedback loop and evidence-backed hypotheses. Scale the investigation to the uncertainty, and change code only when the user also requests a fix.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Record `git status --short --branch`, current `HEAD`, and the checked-out branch or detached state before experiments.
3. Select the execution boundary:
   - **Diagnosis-only:** default for `diagnose`, `find why`, `identify the root cause`, or `before changing code`; keep tracked repository files, checkout, index, and Git refs unchanged.
   - **Diagnose-and-fix:** use only when the user explicitly asks to fix, resolve, repair, or apply the confirmed remediation.
4. Classify the failure:
   - **Deterministic/local:** one command or test fails consistently with a specific error and bounded ownership.
   - **Regression/cross-boundary:** behavior changed across modules, interfaces, data, configuration, or runtime layers.
   - **Flaky/timing:** reproduction is intermittent or order-, load-, clock-, or concurrency-sensitive.
   - **Performance:** latency, throughput, CPU, allocation, I/O, or memory changed and needs a comparable baseline.
5. Build a red/green feedback loop that exercises the user's exact symptom.
6. For deterministic/local failures, read the complete error, reproduce once, trace the smallest owning path, and test the most direct falsifiable cause before expanding the investigation.
7. For regression, flaky, or performance failures, reproduce and minimize until remaining inputs, steps, config, and state are load-bearing.
8. Rank falsifiable hypotheses before proposing or testing remediation. A deterministic compiler or test error may start with one strongly evidenced hypothesis; broader failures require credible alternatives.
9. Inspect or instrument one variable at a time. In Diagnosis-only mode, use read-only probes; ask before changing tracked files, the index, checkout, or refs for instrumentation or bisection.
10. In Diagnosis-only mode, stop after confirming the root cause or exact evidence gap, describe the smallest fix and regression seam, clean temporary artifacts, and prove the tracked worktree, index, checkout, and refs remain at their recorded state.
11. In Diagnose-and-fix mode, apply the smallest confirmed fix, add or document a regression seam, rerun the original feedback loop, and remove temporary probes.

## Modes

- **Diagnosis-only:** reproduce, isolate, and confirm the cause without modifying tracked files, the index, checkout, or Git refs.
- **Diagnose-and-fix:** diagnose first, then apply and verify a fix only under explicit fix authorization.
- **Deterministic fast path:** reproduce the exact command, read the complete diagnostic, trace the owning symbol/config/contract, and test the direct cause. Fix and rerun only in Diagnose-and-fix mode.
- **Bug or build/test diagnosis:** reproduce, minimize when required, hypothesize, and confirm the root cause before any authorized fix.
- **Performance regression:** establish a production-like baseline first, then profile, compare existing revisions read-only, or run an authorized bisection in an isolated worktree/clone before changing code.
- **Flaky behavior:** raise reproduction rate with loops, stress, seeded inputs, controlled clocks, or narrowed timing windows before claiming cause.

## Do Not Use For

- First-pass repository discovery without a concrete failure; use `code-context`.
- Future implementation planning before a failure or bug exists; use `code-planner`.
- Existing local diff review, staging plans, commit grouping, or pre-commit review; use `code-review`. Actual staging or commits belong to `code-delivery` after review.
- Browser-only operation, screenshots, console, network, uploads, downloads, or session evidence; use `ops-browser`. Use this skill with browser evidence only when the root cause crosses code or runtime boundaries.
- Implementation after the root cause is already known and no diagnosis remains; use the matching `implement-*` skill.

## Hard Rules

- Treat diagnosis and implementation authorization separately. A request to explain or find a cause does not authorize edits.
- In Diagnosis-only mode, do not modify tracked source, config, tests, manifests, lockfiles, generated files, the index, checkout, or Git refs. Do not run `git bisect`, `checkout`, `switch`, `reset`, worktree creation, or another ref/checkout mutation without separate authorization; when authorized, isolate it in a disposable worktree/clone and record initial/final refs.
- Do not propose a fix until a feedback loop or explicit missing-evidence report exists.
- The loop must target the user's exact symptom, not a nearby crash or generic health check.
- Read the complete failing diagnostic before editing; do not react to the final line only.
- If the issue is non-deterministic, improve reproduction rate before claiming a cause.
- Test one hypothesis at a time; do not bundle cache clearing, dependency changes, code edits, and config changes into one experiment.
- When a fix is authorized, prefer the source of the bad value, state, contract, timing, or dependency over masking the symptom.
- Tag temporary logs, probes, scripts, screenshots, and artifacts so they can be removed or reported.
- Escalate from the deterministic fast path when the direct cause does not explain all observed evidence, the failure moves after the fix, or multiple owners share the contract.
- If three materially different fix attempts fail or each fix reveals new coupling, stop and report the architectural concern before continuing. Rewording or retrying the same unproven fix does not count as a new attempt.
- Mark unavailable commands, missing repro artifacts, unchecked runtime behavior, and unverified root causes as `Not verified`.
- Do not claim a performance improvement from debug builds, one run, changed inputs, or incomparable environments.

## Output Contract

Report the failure class, Diagnosis-only or Diagnose-and-fix boundary, selected depth, exact red/green loop, reproduction evidence, minimized scenario when required, ranked hypotheses, probes run, confirmed root cause or `Not verified` gap, recommended or applied fix scope, regression seam, commands run, initial/final worktree, index, checkout, and ref state, before/after evidence when a fix was authorized, cleanup status, escalation decisions, and remaining risk.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for the diagnosis loop checklist.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
