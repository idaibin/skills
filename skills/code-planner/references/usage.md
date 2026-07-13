# Code Planner

## Summary

Turn future codebase work into executable, verifiable task packages before implementation. Classify it as Small, Coupled, or Parallelizable first; use subagents only for genuinely independent, auditable scopes.

## Best For

- Large implementation plans
- Refactors, migrations, or bugfix plans
- Work that must be split by module, page, API, or layer
- Subagent coordination with review and reject gates
- Contract-impact planning before `repo-review`
- Project-structure migrations and add/reuse/move/delete lifecycle planning

## Triggers

Use for prompts like:

- `Split this requirement into an executable plan.`
- `Plan first; do not edit yet.`
- `Split the approach first, then decide whether to execute.`
- `Every step must be verifiable.`
- `Which tasks can run in parallel?`
- `Classify this as Small, Coupled, or Parallelizable before assigning owners.`
- `Use multiple subagents.`
- `No subagents; keep it sequential in the main thread.`
- `Mark contract-impact and route the final review to repo-review.`
- `Plan this crate move and include Cargo membership, exports, CI, docs, and stale-reference checks.`

Do not use for first-pass repository onboarding, existing dirty-tree review, or commit grouping; prefer `repo-map` or `repo-review` for those.

## Output

Expect a justified complexity class and owner model followed by task packages with required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, reject criteria, and contract/structure integration gates.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
