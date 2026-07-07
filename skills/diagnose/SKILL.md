---
name: diagnose
description: Use when diagnosing bugs, failing tests, build failures, unexpected behavior, regressions, flaky behavior, or performance problems before proposing fixes.
---

# Diagnose

## Overview

Diagnose technical failures with a tight feedback loop, evidence-backed hypotheses, and minimal fixes. Use this before changing code for bugs, failures, regressions, or performance issues.

## Workflow

1. Read repo guidance first: root `AGENTS.md`, nearest subproject `AGENTS.md`, `AGENT.md`, or chat-supplied rules.
2. Run `git status --short` before edits or experiments.
3. Build a red/green feedback loop that exercises the user's exact symptom.
4. Reproduce and minimize the failure until remaining inputs, steps, config, and state are load-bearing.
5. Rank falsifiable hypotheses before testing fixes.
6. Instrument or inspect one variable at a time, tagged for cleanup.
7. Fix the confirmed root cause with the smallest scoped change.
8. Add or document a regression seam, rerun the original feedback loop, and remove temporary probes.

## Modes

- **Bug diagnosis:** reproduce, minimize, hypothesize, instrument, fix, and verify a functional failure.
- **Build/test failure:** read the full failure, reproduce the command, compare recent changes, and fix the root cause.
- **Performance regression:** establish baseline measurement first, then profile, bisect, or compare variants before changing code.
- **Flaky behavior:** raise reproduction rate with loops, stress, seeded inputs, or narrowed timing windows before claiming cause.

## Do Not Use For

- First-pass repository discovery without a concrete failure; use `code-context`.
- Future implementation planning before a failure or bug exists; use `code-planner`.
- Existing local diff review, staging, commit grouping, or pre-commit review; use `code-review`.
- Browser-only operation, screenshots, console, network, uploads, downloads, or session evidence; use `ops-browser`.
- Frontend implementation or style refactors after the root cause is known; use `frontend-implementation`.

## Hard Rules

- Do not propose fixes until a feedback loop or explicit missing-evidence report exists.
- The loop must target the user's exact symptom, not a nearby crash or generic health check.
- If the issue is non-deterministic, improve reproduction rate before hypothesizing.
- Test one hypothesis at a time; do not bundle cache clearing, dependency changes, code edits, and config changes into one experiment.
- Prefer fixing the source of the bad value, state, or contract over masking the symptom.
- Tag temporary logs, probes, scripts, screenshots, and artifacts so they can be removed or reported.
- If three fix attempts fail or each fix reveals new coupling, stop and report the architectural concern before continuing.
- Mark unavailable commands, missing repro artifacts, unchecked runtime behavior, and unverified root causes as `Not verified`.

## Output Contract

Report the failure loop, reproduction evidence, minimized scenario, ranked hypotheses, probes run, confirmed root cause or `Not verified` gap, fix scope, regression test or missing seam, commands run, cleanup status, and remaining risk.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for the diagnosis loop checklist.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
