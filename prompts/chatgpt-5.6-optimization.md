# ChatGPT 5.6 Optimization

Use this prompt to audit and simplify a personal Codex setup for GPT-5.6. Work from the real installation, make only justified changes, and verify the effective result.

## Task

Inspect the current Codex client and CLI configuration, then produce the smallest setup that preserves the user's real workflows while improving model routing, context control, permissions, Skills, plugins, and validation.

Do not stop at recommendations when safe in-scope changes can be applied. Ask before removing user-owned data, weakening a security boundary, publishing externally, or changing an intentional workflow.

## Working Rules

- Respond in the user's language and keep identifiers, paths, commands, model IDs, and errors unchanged.
- Read the effective `AGENTS.md` chain and preserve unrelated working-tree changes.
- Prefer the installed CLI's accepted keys and observed runtime behavior. Use current official OpenAI documentation for model availability, context limits, pricing, and time-sensitive Codex behavior.
- Distinguish documented API behavior from Codex subscription or credit behavior. Do not promise a fixed savings multiplier.
- Keep durable rules on one owning surface; do not duplicate full instruction blocks across personalization, `AGENTS.md`, Skills, and project configuration.

## Sources of Truth

- `~/.codex/AGENTS.md`: concise personal execution preferences.
- Repository and nested `AGENTS.md`: project-specific rules and validation.
- `~/.codex/config.toml`: global model, reasoning, permissions, features, plugins, MCP, hooks, and Agent registration.
- `~/.codex/agents/*.toml`: explicit model, reasoning, permissions, and role instructions for custom Agents.
- Project `.codex/config.toml`: genuine project overrides only.
- Skills: reusable bounded workflows.
- Plugins and connectors: managed capabilities and live external data or actions.

## Workflow

### 1. Establish Current Truth

1. Confirm the current directory, Git root, branch, dirty state, Codex version, and effective `AGENTS.md` files.
2. Inspect the relevant paths that exist:
   - `~/.codex/config.toml`
   - `~/.codex/AGENTS.md`
   - `~/.codex/agents/`
   - `~/.codex/skills/` and `~/.agents/skills/`
   - enabled plugins, connectors, MCP servers, hooks, and trusted projects
   - project `.codex/config.toml` only when it affects the active task
3. Check current official documentation when a model, key, price, feature, or client behavior may have changed.
4. Report conflicting configuration layers before editing them.

### 2. Simplify Skills and Plugins

- Prefer built-in or official capabilities when they fully cover the need.
- Preserve personal Skills that encode distinct, proven workflows.
- Keep one clear owner for each stable responsibility; report overlapping or stale packages before removing them.
- Update personal Skills through their recorded source and installer. Do not overwrite system Skills or managed plugin caches manually.
- Remove plugins through supported commands only after confirming they are disabled or no longer used.
- Never classify configuration, Agents, personal Skills, memories, sessions, credentials, state databases, or user-created plugins as disposable cache.
- Keep connectors only when live private data or external actions are part of the user's workflow.

### 3. Configure GPT-5.6 Routing

First inspect the installed model catalog. If the following models are available, use this personal baseline:

- Interactive execution: `gpt-5.6-luna`, high reasoning.
- Planning and final review: `gpt-5.6-sol`, `xhigh`, read-only.
- Bounded execution Agents: `gpt-5.6-luna`, `xhigh`, with the minimum required permissions.
- Main Agent: owns integration, returned-output inspection, final verification, acceptance, and delivery.

Pin every automatic Agent explicitly. Do not rely on an undocumented model fallback. Keep `max_depth = 1`; use child Agents only for independent read-only work or disjoint writes with explicit acceptance checks. Small tasks should use no Subagent when delegation adds no value.

Use three to five execution children only when the task is substantial, clearly decomposable, and within the configured concurrency cap. Never assign overlapping writes or independent interface decisions to multiple children.

If a named model is unavailable or deprecated, map it to the current official equivalent and explain the change. Do not invent model IDs or treat this personal routing policy as a universal recommendation.

### 4. Protect Long Sessions

When GPT-5.6 is active and the installed Codex version accepts the key, add:

```toml
# ~/.codex/config.toml
model_auto_compact_token_limit = 240000
```

This leaves headroom before GPT-5.6's documented long-context pricing boundary above 272,000 input tokens. Verify the current official model documentation before repeating that threshold publicly.

Do not set `model_context_window = 272000` by default. Preserve the model's detected context window unless the installed client reports an incorrect value and the override is separately verified.

Keep the numeric threshold in `~/.codex/config.toml`. Put only the behavior below in `~/.codex/AGENTS.md`:

```markdown
长会话上下文管理：
- 当自动压缩后，单次请求输入仍接近或超过 240000 tokens 时，主动提醒我当前会话已接近 GPT-5.6 的 272000 tokens 长上下文加价阈值。
- 如果继续任务预计仍会再次逼近该阈值，并且当前 Codex 客户端提供创建新任务的能力，无需再次确认：自动在同一项目和目录中创建独立任务，发送完整续接摘要作为首条指令，并让新任务继续执行。
- 续接摘要必须包含原目标、已完成工作、未完成事项、关键决策、相关路径、当前 Git 状态、验证结果和下一步命令。
- 新任务创建成功后提供任务入口；如果客户端不能自动切换或聚焦新窗口，明确提示用户点击“打开任务”，不要声称已经打开窗口。
- 只有在当前环境没有创建新任务能力、创建失败，或后续操作需要重新授权时，才退回为提供可直接复制的续接摘要。
```

Automatic compaction does not guarantee that the next request stays below the pricing boundary. When the compacted context remains near the threshold, stop loading new context into the old task and hand off promptly.

### 5. Keep Permissions Narrow

Use the installed client's supported syntax. A typical personal baseline is:

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
writable_roots = [
  "/absolute/path/to/Projects",
  "/absolute/path/to/Documents/Codex",
]
```

- Allow routine reads, task-scoped edits, builds, tests, and local Git work inside approved roots.
- Require explicit authorization for production changes, publishing, secrets, tags, force pushes, deletion, and external writes.
- Do not trust the whole home directory when narrower roots work.
- Do not use `danger-full-access` with `approval_policy = "never"` as a personal default.

If the client has a separate personalization or custom-instructions field, replace its existing content with exactly this pointer:

```text
~/.codex/AGENTS.md 是本机唯一的个人执行偏好来源。
请遵循当前任务路径下生效的 AGENTS.md；如有冲突，以我在当前对话中的明确要求为准。
```

Do not copy the long-session block or other durable personal rules into that field. The field is only an entry pointer; `~/.codex/AGENTS.md` remains the single editable source. If the field is account-synced or available only through the Codex settings UI, prepare the exact text but do not claim it was changed unless the saved UI state was verified.

### 6. Remove Drift

- Remove nonexistent trusted-project paths, disabled duplicate MCP entries, broken Skill links, and project config copies identical to global config.
- Preserve approval rules for installed and authorized connectors.
- Keep explanatory documentation synchronized with the models, Agents, plugins, and commands that are actually installed.
- Do not delete anything whose ownership or replacement is uncertain; report it instead.

### 7. Validate

Run the checks supported by the installed release:

1. Parse changed TOML and YAML.
2. Run `codex --strict-config` through a harmless smoke test when supported.
3. Run `codex doctor` or the available equivalent.
4. Confirm the effective model, reasoning, sandbox, approval policy, writable roots, plugins, and Agent files.
5. Verify each automatic Agent reports its explicitly configured model and permissions.
6. Run one real collaboration smoke test only when Agent configuration changed.
7. Check for broken Skill links, unintended duplicate names, stale project install copies, and configuration errors in a fresh session.
8. Inspect the final diff and state every runtime or external behavior that was not verified.

## Done When

- Changed configuration parses and the current client accepts it.
- Model and Agent routing matches the installed catalog.
- Long-session compaction and handoff rules are installed on the correct surfaces.
- Writable roots work without broadening unrelated access.
- Skills and plugins have a verified owner or are explicitly reported as unresolved.
- No unrelated user data or repository changes were removed.

## Final Report

Return only:

1. Configuration changes
2. Model and Agent routing
3. Context compaction and handoff behavior
4. Skill and plugin changes
5. Permission boundaries
6. Validation results
7. Remaining risks or manual client steps

Do not create a pull request, publish, deploy, or modify production systems unless explicitly requested.
