# Code Review

## Summary

Review existing local git changes before commit. It protects unrelated edits, checks contract chains, handles mixed hunks safely, and turns a dirty tree into scoped commit groups.

## Best For

- Pre-commit review
- Dirty-tree ownership classification
- API or payload contract-chain review
- Semantic commit grouping
- Exact staging plans and Conventional Commit messages
- Safe `code-review` upgrades from a trusted source

## Triggers

Use for prompts like:

- `Review all changes and split commits.`
- `Check whether these changes are safe to commit.`
- `Commit only the current session changes.`
- `Review the API contract chain.`
- `Generate a commit message, but confirm file scope first.`

Do not use for repo onboarding or future implementation planning before code exists; prefer `code-context` or `code-planner` for those.

## Output

Expect findings first, ownership labels, mixed-hunk risks, exact commit groups, path-limited or hunk-level staging guidance, validation status, risks, and concise Conventional Commit messages. It never commits unless explicitly asked.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; after publishing to GitHub, confirm discoverability with `npx skills add https://github.com/idaibin/aicraft --list`.
