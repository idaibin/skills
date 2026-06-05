# Code Planner

Plan codebase work as independent, verifiable tasks and coordinate subagents only when explicitly allowed.

## Best For

- Large implementation plans
- Phased migrations or refactors
- Code review follow-up plans
- Bugfix plans that need reproduction and regression gates
- Work that must be split by feature, module, page, API family, or layer
- Requests that require each task to be `可执行`, `可验证`, or closed-loop
- Multi-agent workflows with implementation, review, and submit-readiness gates
- Main-thread review flows that must reject incomplete subagent output

## Trigger Keywords

- Direct: `code-planner`, `$code-planner`, `Code Planner`
- Planning: `代码计划`, `任务拆分`, `后续计划`, `完整计划`, `分阶段`, `可执行`, `可验证`, `可量化`
- Delegation: `子代理`, `分多个代理`, `多代理`, `分别处理`, `分别验证`
- Review gates: `审查`, `review`, `判断是否可以提交`, `打回`, `验收`, `提交前判断`
- Sequential fallback: `禁止使用子代理`, `不要子代理`, `主线程逐个完成`
## What You Get

- Verified current-state summary
- Independent task boundaries
- Required reads before each task starts
- Clear owned scopes, do-not-touch boundaries, and dependencies
- Dirty-tree ownership labels: `task-owned`, `related-existing`, `unrelated-existing`, or `unknown`
- Exact validation commands or probes
- Done and reject criteria for every task
- Subagent prompts or sequential main-thread steps
- Main-thread integration and final review gates
- Explicit `Not found` and `Not verified` items

## Example Prompts

- `Use $code-planner to split this migration into independent executable and verifiable tasks.`
- `用 code-planner 把这个大功能拆成多个闭环任务，每个任务都要可测试验证。`
- `分多个子代理处理：一个实现，一个 review，一个判断是否可以提交。`
- `禁止使用子代理，主线程逐个完成，但每个任务仍然要可执行可验证。`
- `先审查当前改动，再给可量化可验证的后续计划。`
- `这个改动影响接口契约，先标记 contract-impact，提交前再用 code-review 做完整链路审查。`

## Minimal Task Package Shape

```text
Task: update example API consumer
Type: contract-impact
Owner model: sequential-main-thread
Objective: align the page consumer with the changed response field.
Required reads:
  - AGENTS.md or chat-supplied repo rules
  - git status --short
  - request helper, response type, affected page call site, existing tests
Owned scope:
  - src/api/example.ts
  - src/pages/example/*
  - related-existing diff required for this task, if present
Do not touch:
  - unrelated-existing local changes
  - neighboring API families
  - generated files unless explicitly required
Validation:
  - exact lint/test/build command for the touched surface
  - manual or runtime check when behavior depends on live payloads
Reject conditions:
  - validation failed or skipped without reason
  - unrelated file changed
  - contract-impact not handed to code-review before commit
```

This is a planning shape, not a commit review replacement. For `contract-impact`, `code-planner` marks the risk and routes the final full-chain pre-commit review to `code-review`.

## Reporting Rule

Prefer concise Chinese final responses unless the user asks for another language. Use real files, commands, APIs, and evidence. If something was not checked, say `Not verified`.
