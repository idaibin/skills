# Code Context

## Summary

Ground an agent in a repository before it guesses. Use it to map real commands, paths, docs, and project conventions, or to preview context docs safely.

## Best For

- First-pass repository onboarding
- Real command and entry-point discovery
- `AGENTS.md` or project-map draft previews
- Doc/code alignment checks

## Triggers

Use for prompts like:

- `Understand this project first; do not guess.`
- `Initialize repository context.`
- `Confirm the real directories, commands, and entry points.`
- `Confirm real commands and real entry points before choosing a launch path.`
- `Check whether project docs match the code.`
- `Draft AGENTS.md first; preview before writing.`

Do not use for generic feature initialization, dirty-tree commit review, or implementation planning; prefer `code-review` or `code-planner` for those.

## Output

Expect verified current truth, real paths and commands, missing items as `Not found`, unchecked areas as `Not verified`, and previews before any write.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
