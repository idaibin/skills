# Eval Cases

Use these cases when changing `code-planner` triggers, task contracts, owner models, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `把这个迁移拆成可执行、可验证的任务。` | Should trigger `code-planner`. | Planning and validation gates. |
| `分多个子代理处理：实现、review、判断是否可以提交。` | Should trigger `code-planner`. | Delegated planning. |
| `禁止子代理，主线程逐个完成，但先给计划。` | Should trigger sequential mode. | Explicit no-delegation override. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `审查所有本地改动并拆分 commit。` | Should prefer `code-review`. | Dirty-tree review. |
| `先了解这个仓库真实命令和目录结构。` | Should prefer `code-context`. | Repository grounding. |
| `直接修这个按钮样式。` | Should not require `code-planner` unless planning is requested. | Simple implementation. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Task package | Includes required reads, owned scope, do-not-touch, dependencies, steps, validation, done criteria, and reject criteria. | Leaves hidden decisions or no validation. |
| Subagent plan | Uses subagents only when tools are available, scopes independent, ownership clear, and audit possible. | Delegates forbidden, unnecessary, unclear, or tightly coupled work. |
| Contract-impact | Marks risk and routes final chain review to `code-review`. | Pretends planning replaces commit review. |
| Upgrade/install | Compares only `skills/code-planner/`, previews before writing, and uses `--check-target` after local install. | Overwrites directly or skips installed-target validation. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
