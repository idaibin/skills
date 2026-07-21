# Repository Map

## Summary

Create or maintain a durable semantic repo map from current source truth. It should reduce wrong-root routing, repeated discovery, duplicate declarations, and cross-boundary guesswork.

## Best For

- Initial `docs/repo-map/README.md` or repository-equivalent creation
- Workspace routing across multiple child Git roots
- Ordinary non-Git directory projects with no containing or child Git repository
- Directory ownership and technical architecture mapping
- Real command, runtime, and repository-convention documentation
- Shortest reading paths for common frontend, API, backend, CLI, or worker tasks
- Verified component, function, service, API client, route, handler, trait, type, or DTO reuse inventories
- Bounded API Contract Maps that connect native authority, client, consumers,
  duplicate-DTO ownership, and checks; add normalized OpenAPI/generated clients only
  for an existing or explicitly introduced pipeline
- Reuse/extend/wrap/new decisions before adding another contract
- Incremental repair when documented paths or parent directories have moved or disappeared

## Triggers

- `梳理当前项目的目录结构和技术架构，写到项目地图。`
- `把真实命令、规范、组件和接口入口整理成后续开发导航。`
- `找出开发这个页面最短要读哪些目录和组件。`
- `更新项目地图里的 API 和可复用组件。`
- `核查并记录这个服务唯一的 OpenAPI authority、生成链、前端消费者和重复 DTO 边界。`
- `文档里的目录找不到了，从最近存在的父目录局部扫描并修复。`
- `Create or update docs/repo-map/README.md from current repository truth.`
- `当前目录不是 Git；检查里面是否有子仓库，没有的话也按普通项目结构生成 repo map。`

Do not use for generic implementation, local dirty-tree review, immutable repository/range/PR review, or defect diagnosis. Use the matching Worktree or immutable basis mode in `repo-review` for review.

## Output

Expect an updated repo-map path plus a compact summary of initial working scope, map root, discovered Git roots and containment, `versioned` or `local-unversioned` persistence, scope level, changed sections, shortest task routes, verified reuse entries and decisions, mapped protocol authority/derived-consumer chain when requested, semantic/path repairs, preserved sections, validation, and `Not found` or `Not verified` gaps. Partial work also reports its stop reason, completed evidence, unresolved boundary, artifact state, and follow-up.
