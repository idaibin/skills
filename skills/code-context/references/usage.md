# Code Context

Establish codebase context from real files, not assumptions. Use bundled templates to bootstrap missing docs, optionally adapt local prompt assets when present, compare existing docs against current code and config, or upgrade this skill from a trusted upstream source.

## Best For

- First-pass onboarding to an unfamiliar repository
- Mapping the real project structure
- Finding the actual commands for dev, build, lint, typecheck, and test
- Orienting before code changes
- Bootstrapping missing docs such as `AGENTS.md` and `docs/project-map.md`
- Checking whether existing docs still match the codebase
- Updating `code-context` from a GitHub repository, branch, tag, commit, directory, or file URL

## Trigger Keywords

- Direct: `code-context`, `$code-context`, `Code Context`
- Project context: `项目上下文初始化`, `项目初始化`, `初始化`, `了解项目`, `熟悉项目`, `项目摸底`, `仓库上下文`, `项目上下文`
- Bootstrap docs: `生成 AGENTS.md`, `生成 docs/project-map.md`, `初始化项目文档`, `项目文档草稿`, `先预览再写入`
- Alignment: `项目文档对齐`, `文档和代码是否匹配`, `检查项目文档`, `文档过期`, `文档修改建议`
- Upgrade: `code-context 升级`, `更新 code-context`, `从 GitHub 更新 skill`, `更新内置模板`, `同步 skill 模板`

## What You Get

- Real stack and runtime details
- Directory map with actual paths
- Key file summary
- Project conventions inferred from code and config
- Baseline checks using only commands the repo already defines
- Dirty worktree state and scope risks when they matter
- Selected bundled templates and optional local prompt assets when docs need to be generated
- Draft doc previews before any file write
- Doc/code mismatch report when docs already exist
- Upgrade comparison with upstream URL, resolved version, proposed skill-package changes, and rejected candidates

## Guardrails

- No source code changes during context discovery or doc review
- No file writes unless the user approves a preview or explicitly asks for docs to be written
- No invented commands
- No guessed files or layers
- No generic best-practice filler when repo evidence exists
- No silent substitution when a required browser, tool, command, or runtime is unavailable
- No dependency on local `prompts/`; bundled templates must be enough after publishing
- No template or prompt content treated as repository truth
- No direct overwrite from upstream; remote content must be compared, previewed, and confirmed

## Example Prompts

- `Use $code-context to inspect this repository and preview AGENTS.md and docs/project-map.md drafts.`
- `Use $code-context to map the codebase and report the real commands and directory structure.`
- `Use $code-context to compare existing docs against current code and suggest fixes.`
- `用 code-context 做项目上下文初始化，先了解项目，再预览 AGENTS.md 和 docs/project-map.md 草稿。`
- `初始化这个项目，先了解项目结构和真实命令，不要直接写文件。`
- `了解项目，确认真实目录、命令和已有文档状态。`
- `这个项目没有 AGENTS.md，先用 code-context 内置模板生成草稿；如果本地 prompts 有更合适模板，可以参考，确认后再写入。`
- `检查现有项目文档和代码是否匹配，先给修改建议，不要直接改。`
- `Use $code-context to compare this GitHub repo against the local skill and preview an upgrade plan.`
- `从 https://github.com/idaibin/aicraft 的 main 更新 code-context，先对比并预览，不要直接覆盖。`

## Reporting Rule

If a file, layer, or command is missing, report `Not found`.
If an item was not checked, report `Not verified`.
Prefer concise Chinese final responses unless the user asks for another language.
