# Code Review

## Summary

Review local git changes before commit. It protects unrelated edits, checks contract chains, handles mixed hunks safely, and turns a dirty tree into scoped commit groups.

## Best For

- Pre-commit review
- Dirty-tree ownership classification
- API or payload contract-chain review
- Semantic commit grouping
- Exact staging plans and Conventional Commit messages
- Safe `code-review` upgrades from a trusted source

## Triggers

Use for prompts like:

- `审查所有改动，分类提交`
- `看下这些改动能不能提交`
- `只提交当前会话改动`
- `接口链路审查一下`
- `帮我生成 commit message，但先确认文件范围`

Do not use for repo onboarding or forward implementation planning; prefer `code-context` or `code-planner` for those.

## Output

Expect findings first, ownership labels, mixed-hunk risks, exact commit groups, path-limited or hunk-level staging guidance, validation status, risks, and concise Conventional Commit messages. It never commits unless explicitly asked.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/sync-skills.py --validate-only`; after local install or upgrade, add `--check-target`.
