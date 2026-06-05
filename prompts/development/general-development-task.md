# General Development Task

请使用通用开发任务流程处理当前需求。

## Related Skill

- Related skills: `code-context` for project context and `code-review` for review/commit planning.
- This prompt is a standalone source asset for implementation tasks.
- Do not treat this prompt as a runtime dependency of any skill.

## 任务

[在这里写具体需求]

## 语言

- 默认使用用户当前语言回复。
- 如果用户明确指定输出语言，按用户指定语言回复。
- 代码、命令、路径、API 名称、类型名和错误信息保持原文。

## 开始前

1. 读取相关 `AGENTS.md`、README、项目说明和任务相关代码。
2. 检查真实状态：
   - `git status`
   - 需要时查看 `git diff`
3. 明确本次改动边界：
   - 允许修改哪些文件或目录
   - 不应修改哪些文件或目录
   - 是否存在用户或他人已有本地改动
4. 先理解现有实现，再决定是否需要新增文件或抽离公共逻辑。

## 执行规则

- 优先复用现有组件、hooks、services、工具函数和样式体系。
- 保持现有代码风格、目录习惯、交互方式和业务逻辑一致。
- 不修改无关文件，不带入历史改动，不覆盖已有本地改动。
- 如果是继续上一轮任务，延续已有实现思路，不推翻前一轮结构；如发现前一轮风险，先指出再处理。
- 如果是功能开发，补齐 loading / empty / error、表单、列表、弹窗、接口和状态处理。
- 如果是 bug 修复，先定位根因，使用最小改动修复，不只做表面兜底。
- 如果是重构或优化，不改变已有行为，除非用户明确要求；抽公共逻辑前先判断复用价值。
- 如涉及接口或页面字段，确认前后端路径、参数、返回结构、类型定义和页面使用是否一致。

## 验证

修改后运行与改动匹配的检查，例如：

- typecheck
- lint
- tests
- build
- 接口调用
- 页面或运行日志验证

不能验证时，说明原因和剩余风险。

## 输出

最后输出：

1. 改了什么
2. 改了哪些文件
3. 跑了哪些检查
4. 还有哪些风险或待确认项
