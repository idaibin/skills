# Eval Cases

Use these cases when changing `code-context` triggers, workflow, outputs, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Understand this repository first, confirm real commands and entry points, and do not guess.` | Should trigger `code-context`. | Repository grounding. |
| `Do not guess the startup path; confirm the real commands and entry points first.` | Should trigger `code-context`. | Command and entry-point grounding. |
| `Check whether existing project docs match the code.` | Should trigger `code-context`. | Doc/code alignment. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Initialize a login feature and start implementing directly.` | Should not trigger `code-context`. | Generic implementation task. |
| `Review all local changes and split commits.` | Should prefer `code-review`. | Dirty-tree review. |
| `Split this migration into executable tasks.` | Should prefer `code-planner`. | Work planning. |
| `Verify this local web app in the browser and take a screenshot.` | Should prefer `ops-browser`. | Browser operation task. |
| `Review this API for authorization risk.` | Should prefer `code-security`. | Security review task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Onboarding | Reads repo guidance, checks `git status --short`, maps real commands and paths, and stops when enough evidence exists. | Invents commands or crawls unrelated areas. |
| Large monorepo | Reads root workspace evidence and relevant package boundaries only; marks unrelated areas `Not verified`. | Inspects every package without task need. |
| Bootstrap docs | Uses bundled templates, previews drafts, and writes only after confirmation. | Writes before preview approval. |
| Publish readiness | Keeps the package self-contained, updates eval cases and metadata, and validates with `python3 scripts/validate-skills.py`. | Requires repository-local prompts or skips source validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
