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

- `先了解这个项目，不要猜`
- `做项目上下文初始化`
- `确认真实目录、命令和入口`
- `检查项目文档和代码是否匹配`
- `生成 AGENTS.md 草稿，先预览`
- `更新 code-context，先对比`

Do not use for generic feature initialization, dirty-tree commit review, or implementation planning; prefer `code-review` or `code-planner` for those.

## Output

Expect verified current truth, real paths and commands, missing items as `Not found`, unchecked areas as `Not verified`, and previews before any write.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; after publishing to GitHub, confirm discoverability with `npx skills add https://github.com/idaibin/aicraft --list`.
