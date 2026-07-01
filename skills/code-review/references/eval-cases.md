# Eval Cases

Use these cases when changing `code-review` triggers, ownership labels, staging rules, commit behavior, contract-review scope, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `审查所有改动，分类提交。` | Should trigger `code-review`. | Full dirty-tree review. |
| `只提交当前会话改动，先全量审查。` | Should trigger `code-review`. | Scoped commit plan after full review. |
| `接口链路审查一下，字段从后端到页面都要看。` | Should trigger `code-review`. | Contract-chain review. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `先了解这个仓库真实命令和目录结构。` | Should prefer `code-context`. | Repository grounding. |
| `把这个需求拆成可执行任务。` | Should prefer `code-planner`. | Forward planning. |
| `这个功能还没写，先拆成实现计划。` | Should prefer `code-planner`. | Future implementation planning. |
| `直接实现这个功能，不需要审查。` | Should not require `code-review`. | Implementation task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Full dirty-tree review | Runs status, diff stat, name-status, and cached equivalents when staged files exist. | Reviews only a subset without reporting full scope. |
| Ownership and mixed hunks | Labels ownership, marks `mixed-hunk`, avoids whole-file staging, and verifies staged diff. | Stages mixed files with whole-file `git add`. |
| Contract-chain review | Traces route/method/fields to helpers, types, callers, shaping, and runtime evidence or `Not verified`. | Stops at endpoint names. |
| Commit plan | Groups by semantic unit with exact staging scope, validation status, risks, and commit messages. | Uses broad staging or auto-commits. |
| Upgrade/publish | Compares only `skills/code-review/`, previews before writing, and confirms discoverability with `npx skills add https://github.com/idaibin/aicraft --list` after publishing. | Overwrites directly or skips source validation or publishability checks. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
