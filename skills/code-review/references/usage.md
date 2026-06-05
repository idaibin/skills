# Usage

## What This Skill Does

Code Review reviews all local git changes before a commit. It inventories real staged and unstaged changes, classifies dirty-tree ownership, checks changed code against project structure, coding conventions, interface contract chains, related docs, validation commands, and unused-code risks, then groups files by feature intent and drafts exact path-limited staging commands with concise Conventional Commit messages. It can also compare and upgrade this skill from a trusted upstream source.

## When To Use

Use this skill when you need to:

- review all local changes before committing
- check changed code for project-structure, convention, doc, lint, type, build, unused import, or unused definition issues
- review interface or contract chains from backend route and fields through request helpers, types, callers, data shaping, and runtime payload evidence
- split one large change into multiple logical commits
- decide whether a file belongs in the commit or should be excluded
- protect unrelated local changes in a noisy worktree while marking needed pre-existing edits as `related-existing`
- produce a clean commit plan with file lists, staging scope, validation, and remaining risk
- update `code-review` from a GitHub repository, branch, tag, commit, directory, or file URL

## Trigger Keywords

- Direct: `code-review`, `$code-review`, `Code Review`
- Commit review: `提交前审查`, `审查所有改动`, `全量审查`, `检查本地改动`, `提交前检查`
- Contract review: `接口链路审查`, `接口契约审查`, `payload 审查`, `字段链路`
- Commit planning: `分类提交`, `拆分 commit`, `拆分提交`, `生成 commit message`, `Conventional Commit`, `暂存范围`
- Scope control: `只提交当前会话`, `只提交当前上下文`, `只提交本次修改`, `只暂存本次相关文件`
- Upgrade: `code-review 升级`, `更新 code-review`, `从 GitHub 更新 skill`, `同步 code-review`

## What It Outputs

A typical response includes:

- complete local change scope
- change classification
- dirty-tree ownership labels: `task-owned`, `related-existing`, `unrelated-existing`, or `unknown`
- code review findings, doc/code mismatches, failed checks, unused references, and unverified items
- interface chain status from route/fields to request helper, types, callers, data shaping, and runtime payload evidence or `Not verified`
- risks, blockers, and files that should not be committed
- split recommendation by semantic unit
- exact commit plan
- exact `git add` scope for each commit group
- validation already run or still needed
- remaining risk
- upgrade comparison with upstream URL, resolved version, proposed changes, and rejected candidates when using Upgrade mode

Final responses should be concise Chinese by default, unless the user asks for another language.

## Example Prompts

- `Use Code Review to review my current git changes and split them into clean commits.`
- `Use Code Review to check this worktree before I commit anything.`
- `Use Code Review to tell me which files should go into each commit.`
- `审查所有改动，分类提交，只暂存本次相关文件。`
- `只提交当前会话改动；先全量审查，但提交计划只包含当前会话相关文件。`
- `从 https://github.com/idaibin/aicraft 的 main 更新 code-review，先对比并预览，不要直接覆盖。`

## Non-Goals

- It does not commit automatically unless the user asks it to.
- It does not guess when information is missing.
- It does not turn commit review into implementation planning; it reports findings, validation, ownership, and commit groups from actual evidence.
- It does not include build outputs, caches, logs, or local machine files in commits.
- It does not use broad staging, directory-wide staging, wildcard staging, or revert unrelated user changes unless the user explicitly approves the exact full staging scope.
- It does not directly overwrite local skill files from upstream; remote content must be compared and confirmed first.
- It does not replace Code Context; use Code Context for repository onboarding, project-map generation, or doc bootstrapping.
