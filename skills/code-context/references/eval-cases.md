# Eval Cases

Use these cases when changing `code-context` triggers, workflow, outputs, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `先了解这个仓库，确认真实命令和入口，不要猜。` | Should trigger `code-context`. | Repository grounding. |
| `检查现有项目文档和代码是否匹配。` | Should trigger `code-context`. | Doc/code alignment. |
| `从 GitHub 更新 code-context，先对比。` | Should trigger `code-context`. | Skill upgrade preview. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `初始化一个登录功能，直接开始实现。` | Should not trigger `code-context`. | Generic implementation task. |
| `审查所有改动，分类提交。` | Should prefer `code-review`. | Dirty-tree review. |
| `把这个迁移拆成可执行任务。` | Should prefer `code-planner`. | Work planning. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Onboarding | Reads repo guidance, checks `git status --short`, maps real commands and paths, and stops when enough evidence exists. | Invents commands or crawls unrelated areas. |
| Large monorepo | Reads root workspace evidence and relevant package boundaries only; marks unrelated areas `Not verified`. | Inspects every package without task need. |
| Bootstrap docs | Uses bundled templates, previews drafts, and writes only after confirmation. | Writes before preview approval. |
| Upgrade/install | Resolves version, compares only `skills/code-context/`, previews before writing, and uses `--check-target` after local install. | Overwrites directly or checks source only after install. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
