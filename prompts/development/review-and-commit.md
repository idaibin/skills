# Review And Commit

请使用 `review-and-commit` 流程审查当前代码。

## Related Skill

- Related skill: `code-review`.
- Prefer `code-review` for full local change review, feature-based commit grouping, path-limited staging plans, and skill upgrade behavior.
- This prompt remains a standalone source asset for review-and-commit task language.
- If prompt changes are required by `code-review`, update `skills/code-review/references/` in the skill package before upgrading the skill.

## 目标

这不是普通代码质量审查。重点检查当前变更是否真实可交付、是否误扩大范围、是否破坏已有细节，以及是否可以安全提交。

## 语言

- 默认使用用户当前语言回复。
- 如果用户明确指定输出语言，按用户指定语言回复。
- 代码、命令、路径、API 名称、类型名和错误信息保持原文。

## 审查规则

1. 先只读，不改代码。
2. 先读取相关 `AGENTS.md`、项目说明、任务相关代码和已有实现。
3. 检查真实状态：
   - `git status`
   - `git diff`
   - `git diff --cached`
4. 明确区分：
   - 本次任务相关改动
   - 历史改动
   - 用户或他人已有本地改动
   - 生成物、临时文件、不应提交文件
5. 不允许把无关改动纳入修复或提交。

## 重点检查

按严重程度优先检查：

1. 功能行为是否错误或不完整。
2. 接口契约是否真实对齐：
   - 后端路径
   - method
   - path/query/body 参数
   - 返回结构
   - 错误码和错误字段
   - 前端 API 封装
   - TypeScript 类型
   - 页面调用和字段使用
3. 是否误改无关文件或扩大范围。
4. 是否丢失已有细节：
   - UI 宽度
   - 样式
   - 交互行为
   - 用户调过的细节
   - 既有业务逻辑
5. 错误处理、空值、边界条件、权限或状态判断是否完整。
6. 是否缺少必要测试或验证。
7. 是否已经验证真实运行结果，而不只是静态看代码。

## 输出要求

每个问题必须包含：

- 严重程度
- 文件路径和具体位置
- 问题说明
- 为什么这是问题
- 建议修复方式

如果发现真实问题：

1. 先列出最小范围修复计划。
2. 只修复本次任务相关问题。
3. 修复后运行项目合适的验证命令。
4. 说明哪些验证已覆盖，哪些仍未覆盖。

如果未发现阻塞问题：

- 明确说明“未发现阻塞问题”。
- 说明仍未覆盖的验证风险。

## 提交规则

如果用户要求提交：

1. 先判断是否适合 1 次提交还是多次提交，依据包括：
   - 可读性
   - 可回滚性
   - 审查成本
   - 提交语义清晰度
2. 如果拆分提交，输出每个 commit 的：
   - commit 目的
   - 文件清单
   - 为什么这样分
   - 建议 commit message
3. 只暂存本次任务相关文件。
4. 提交前再次检查暂存区：
   - `git diff --cached`
   - 暂存文件列表
5. commit message 必须简洁、语义明确，优先使用 Conventional Commits。
6. 不提交无关本地改动、历史改动、生成物或临时文件。

## 最终结论

最后说明：

- 当前是否达到可提交状态
- 缺失项清单
- 推荐提交顺序
- 高风险文件或区域
- 如果用户下一步继续处理，最有效的一句指令
