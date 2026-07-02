# Code Context

## Summary

Ground an agent in a repository before it guesses. Use it to map real commands, paths, docs, and project conventions, or to preview context docs and skill upgrades safely.

## Best For

- First-pass repository onboarding
- Real command and entry-point discovery
- `AGENTS.md` or project-map draft previews
- Doc/code alignment checks
- Safe `code-context` upgrades from a trusted source

## Triggers

Use for prompts like:

- `Understand this project first; do not guess.`
- `Initialize repository context.`
- `Confirm the real directories, commands, and entry points.`
- `Confirm real commands and real entry points before choosing a launch path.`
- `Check whether project docs match the code.`
- `Draft AGENTS.md first; preview before writing.`
- `Update code-context from GitHub; compare first.`

Do not use for generic feature initialization, dirty-tree commit review, or implementation planning; prefer `code-review` or `code-planner` for those.

## Output

Expect verified current truth, real paths and commands, missing items as `Not found`, unchecked areas as `Not verified`, and previews before any write.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; after publishing to GitHub, confirm discoverability with `npx skills add https://github.com/idaibin/aicraft --list`.
