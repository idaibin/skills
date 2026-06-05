# API Contract Review

请使用 `api-contract-review` 流程审查当前接口相关改动，逐个验证后端接口和前端 API 是否真实对齐。

## Related Skill

- Related skill: `code-review` when API contract review is part of pre-commit review.
- This prompt is a standalone source asset for interface contract review.
- If this flow becomes part of a published skill, update that skill's `references/` files before upgrading the skill.

## 目标

重点不是泛泛看代码质量，而是确认每个接口从后端定义到前端页面使用的完整链路都一致、可运行、可验证。

## 语言

- 默认使用用户当前语言回复。
- 如果用户明确指定输出语言，按用户指定语言回复。
- 代码、命令、路径、API 名称、类型名和错误信息保持原文。

## 审查规则

1. 先只读，不改代码。
2. 读取相关 `AGENTS.md`、接口文档、后端路由、前端 API 封装、类型定义和页面调用代码。
3. 检查真实状态：
   - `git status`
   - `git diff`
   - `git diff --cached`
4. 按接口逐个审查，不要只看文件名或 API 函数名。
5. 不允许用推测代替真实路径、真实参数或真实返回结构。

## 每个接口必须检查

- 后端真实路径
- HTTP method
- path 参数
- query 参数
- body 参数
- 返回结构：
  - `code`
  - 项目真实消息字段，例如 `message` 或 `msg`
  - `data`
  - 分页字段
  - 错误字段
- 错误码和错误处理逻辑
- 前端 API 封装路径和 method
- 前端 API 参数映射
- TypeScript 类型定义
- 页面字段读取和提交逻辑
- 页面提交前的数据转换逻辑
- 空值处理
- 错误提示
- loading / empty / error 状态
- 是否存在旧接口、旧字段、mock、临时兼容或残留代码

## 输出接口审查表

最后必须输出接口审查表：

| 接口 | 后端状态 | 前端 API 状态 | 页面调用状态 | 问题 | 是否已修复 | 验证方式 |
| --- | --- | --- | --- | --- | --- | --- |

## 问题输出要求

每个问题必须包含：

- 严重程度
- 后端文件路径和位置
- 前端文件路径和位置
- 具体不一致点
- 真实影响
- 最小修复建议

## 修复和验证

如果发现真实接口问题：

1. 先列出最小范围修复计划。
2. 只修复接口契约相关问题。
3. 修复后运行合适的验证：
   - typecheck
   - build
   - tests
   - 接口调用
   - 运行日志
   - 页面操作验证
4. 说明每个接口的验证方式和验证结果。

如果无法完整验证：

- 明确说明未验证的接口、原因和剩余风险。
