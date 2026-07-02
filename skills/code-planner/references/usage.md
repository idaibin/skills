# Code Planner

## Summary

Turn future codebase work into executable, verifiable task packages before implementation. Use subagents by default only when tools are available, scopes are independent, ownership is clear, and the main thread can audit outputs.

## Best For

- Large implementation plans
- Refactors, migrations, or bugfix plans
- Work that must be split by module, page, API, or layer
- Subagent coordination with review and reject gates
- Contract-impact planning before `code-review`

## Triggers

Use for prompts like:

- `Split this requirement into an executable plan.`
- `Plan first; do not edit yet.`
- `Split the approach first, then decide whether to execute.`
- `Every step must be verifiable.`
- `Which tasks can run in parallel?`
- `Use multiple subagents.`
- `No subagents; keep it sequential in the main thread.`
- `Mark contract-impact and route the final review to code-review.`

Do not use for first-pass repo onboarding, existing dirty-tree review, or commit grouping; prefer `code-context` or `code-review` for those.

## Output

Expect task packages with required reads, owned scope, do-not-touch boundaries, dependencies, implementation steps, validation, done criteria, reject criteria, owner model, and integration gates.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; after publishing to GitHub, confirm discoverability with `npx skills add https://github.com/idaibin/aicraft --list`.
