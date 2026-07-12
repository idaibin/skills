# Codex Setup Optimization

Use this prompt to audit and optimize a personal developer's local Codex setup. It covers Skills, GPT-5.6 model routing, custom Agents, global configuration, permissions, plugins, and validation in one executable workflow.

## Task

Audit the real local Codex installation, then make the smallest safe set of changes required to produce a simple, current, effective personal setup.

Do not stop at generic recommendations. Inspect the actual files and installed capabilities, apply safe in-scope improvements, and verify the resulting configuration. Ask before proceeding only when a decision would remove user-owned data, change an intentional security boundary, publish externally, or materially alter the user's workflow.

## Language

- Respond in the user's current language unless another language is requested.
- Keep model IDs, configuration keys, commands, paths, plugin names, Skill names, and errors unchanged.
- Keep progress updates and the final report concise.

## Default Scope

Inspect the relevant paths that exist on the current machine, normally including:

- `~/.codex/config.toml`
- `~/.codex/AGENTS.md`
- `~/.codex/agents/`
- `~/.codex/skills/`
- `~/.agents/skills/`
- enabled Codex plugins and their managed caches
- project `.codex/config.toml` and nested `AGENTS.md` files only when they affect the active task
- the user's reusable Codex workspace, when one is configured

Default personal writable roots, when these paths exist:

- `~/Projects`
- `~/Documents/Codex`

Use actual environment values instead of assuming these defaults on another machine.

## Sources of Truth

Use this ownership model:

- `~/.codex/AGENTS.md`: one concise source for durable personal execution preferences.
- Repository and nested `AGENTS.md`: repository-specific architecture, commands, validation, and local overrides.
- `~/.codex/config.toml`: global model, reasoning, permissions, plugins, MCP, hooks, and Agent registration.
- `~/.codex/agents/*.toml`: model, reasoning, read/write boundary, and instructions for each custom Agent.
- Project `.codex/config.toml`: real project differences only; do not copy the global configuration.
- Skills: reusable bounded workflows.
- Plugins: managed bundles for Skills, connectors, MCP, tools, and assets.
- Design documents: explanation and validation guidance only; they are not runtime instruction sources unless `AGENTS.md` explicitly routes to them.

Do not maintain the same behavioral rule in multiple surfaces.

## Execution Workflow

### 1. Establish Current Truth

1. Confirm the current directory and whether it is a Git repository.
2. Read the effective `AGENTS.md` chain.
3. Inspect the actual Codex version, help output, config keys, enabled features, plugins, custom Agents, Skill roots, and trusted projects.
4. Use current official OpenAI documentation for time-sensitive Codex behavior. Prefer the local CLI's accepted keys and verified runtime behavior when documentation and the installed version differ.
5. Preserve unrelated local changes and do not treat a workspace container as a Git repository when its child directories are the real repositories.

### 2. Audit Skills

Inventory Skills by source:

- Codex built-in/system Skills
- official OpenAI curated Skills
- plugin-provided Skills
- personal Skills
- project-local Skills
- stale install copies, broken links, backups, and orphaned plugin caches

For each non-system Skill, determine:

- source repository or managed plugin
- installed version or source hash when available
- whether an update mechanism exists
- whether its trigger overlaps another Skill
- whether it is still applicable to current projects
- whether it is active, disabled, stale, orphaned, or user-owned

Apply these priorities:

1. Prefer Codex built-in or official OpenAI capabilities when they fully cover the need.
2. Preserve distinct personal Skills that encode the user's real workflows.
3. Prefer one best Skill for one stable responsibility.
4. Merge or remove only clearly redundant third-party entry points after confirming the retained Skill covers the required behavior.
5. Keep low-frequency but distinct Skills available on demand; do not force them into default routing.

Update rules:

- Built-in/system Skills are updated with the Codex client; do not overwrite them manually.
- Official curated Skills must be compared with their current official upstream before replacement.
- Personal Skills must be updated through their recorded source and supported installer, such as the standard `skills` CLI and its lock file.
- Validate source packages and actual global installation state separately.
- Do not call a Skill current only because its directory exists.

Cleanup rules:

- Remove disabled plugins through `codex plugin remove`, not by editing managed plugin files.
- Delete only plugin cache versions proven unreferenced by current plugin, marketplace, and runtime state.
- Never classify `config.toml`, `AGENTS.md`, custom Agents, `~/.codex/skills/.system`, personal Skills, memories, sessions, state databases, credentials, or user-created plugins as disposable cache.
- Remove broken Skill symlinks and ignored project-local install copies only after confirming a canonical source and installation remain.
- Report any package without a verifiable current upstream instead of silently deleting it.

### 3. Optimize GPT-5.6 Model and Agent Routing

When the installed model catalog supports these model IDs, use this baseline:

- Main Agent: `gpt-5.6-sol`, medium reasoning; owns implementation, final decisions, verification, and delivery.
- Plan mode: high reasoning; used for ambiguous, cross-module, migration, architecture, and high-cost work.
- Explorer: `gpt-5.6-terra`, low reasoning, read-only; traces code paths and gathers evidence.
- Test Analyst: `gpt-5.6-terra`, medium reasoning, read-only; defines behavior boundaries and the smallest reliable test matrix.
- Reviewer: `gpt-5.6-sol`, high reasoning, read-only; independently checks correctness, regressions, security, and validation gaps.
- Batch Worker: `gpt-5.6-luna`, low reasoning, read-only and explicit-only; performs repeatable extraction, classification, transformation, and structured summaries.

Keep `gpt-5.6-sol` with medium reasoning as the global default. Do not replace it globally with Luna merely because a benchmark reports similar aggregate scores.

#### Long-context cost guardrail

When `gpt-5.6-sol` is the active model and the installed Codex version accepts the key, add an automatic compaction threshold to the global configuration:

```toml
# ~/.codex/config.toml
model_auto_compact_token_limit = 240000
```

This threshold leaves headroom before GPT-5.6's documented long-context pricing boundary at more than 272,000 input tokens. Treat the expected quota or cost reduction as an optimization hypothesis, not a guaranteed multiplier for a Codex subscription: the official model documentation defines API token pricing, while the installed Codex client and account plan determine the effective usage behavior.

Do not add `model_context_window = 272000` by default. It overrides Codex's view of the available context window instead of merely controlling compaction and can cause unnecessarily early truncation or compaction. Preserve the model's detected context window unless the installed client reports an incorrect value and the override is separately verified.

Keep the runtime threshold and the personal behavior rule on their respective owning surfaces:

- `~/.codex/config.toml` owns `model_auto_compact_token_limit = 240000`.
- `~/.codex/AGENTS.md` owns the reminder and handoff behavior below.

Add this concise personal rule when the user wants proactive long-session guidance:

```markdown
长会话上下文管理：
- 当自动压缩后，单次请求输入仍接近或超过 240000 tokens 时，主动提醒我当前会话已接近 GPT-5.6 的 272000 tokens 长上下文加价阈值。
- 如果继续任务预计仍会再次逼近该阈值，建议我新开会话窗口，并给出一段可直接复制的新会话续接摘要；不要自行创建新会话。
```

After changing either file, verify that a fresh Codex session accepts the configuration. During later work, do not claim that automatic compaction alone guarantees the next request will stay below 272,000 input tokens. If the compacted session remains near the threshold, stop expanding context, warn the user, and prepare a continuation summary containing the objective, completed work, unresolved decisions, relevant paths, current Git state, and the next verification command.

Use Luna as an explicit execution path when all of these conditions hold:

- scope and acceptance criteria are already clear
- the implementation does not require broad repository discovery or architecture decisions
- lint, tests, build, or another reliable check can verify the result
- failure is reversible and the main Agent can review the final diff

Choose the lowest Luna effort that works:

- low or medium for extraction, classification, formatting, documentation metadata, and mechanical transformations
- high for bounded implementation with straightforward validation
- extra high (`xhigh`) for difficult but still well-specified multi-step implementation

Keep Terra for everyday investigation and tool use. It remains useful when repository exploration, alternative-path discovery, or test-boundary analysis needs more breadth than Luna but not Sol's full depth.

Use Sol high for final review, security-sensitive work, architecture, migrations, concurrency, data integrity, and failures that survived a lower-cost attempt. Use Max or Ultra only when the task itself justifies them.

For the CLI, prefer an optional layered profile instead of changing the global default:

```toml
# ~/.codex/luna-exec.config.toml
model = "gpt-5.6-luna"
model_reasoning_effort = "xhigh"
```

Run it with `codex --profile luna-exec`. In an interactive client or CLI session, use the model control or `/model` when a one-off switch is sufficient.

If these models are unavailable or deprecated, use the current official equivalent and explain the mapping. Do not invent model IDs.

Agent rules:

- Small and ordinary tasks use no Subagent.
- Delegate only independent work with no ordering dependency and no overlapping writes, or completely read-only work.
- Prefer parallel read-only investigation followed by one main implementation path.
- Use no more than three concurrent child tasks by default.
- Keep `max_depth = 1`; child Agents must not recursively spawn Agents.
- The main Agent must inspect and synthesize all child results before claiming completion.
- Do not install Superpowers or another global orchestrator by default.
- Do not use Max, Ultra, repeated debate, or indefinite reflection merely because a prompt asks for the strongest result.
- Do not add a writable Luna Subagent by default. Keep one main writer unless the user explicitly requests parallel implementation and the work can be isolated without overlapping files.

### 4. Optimize Global Codex Configuration

Keep the global configuration small and valid for both the Codex client and CLI.

Preferred personal permission baseline:

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
writable_roots = [
  "~/Projects",
  "~/Documents/Codex",
]
```

Resolve `~` to supported real paths if the installed Codex version requires absolute paths.

Permission behavior:

- Allow autonomous reads, edits, builds, tests, and local Git operations inside approved writable roots.
- Keep other directories protected and request scoped authorization when access is necessary.
- Do not enable unrestricted outbound network access globally merely to avoid prompts.
- Publishing, production changes, secrets, tags, force pushes, data deletion, and external writes require explicit user authorization.
- Use `danger-full-access` only for a specifically authorized task; never combine it with `approval_policy = "never"` as the personal global default.

Global `AGENTS.md` should contain only durable behavior-changing rules, such as:

- concise ordinary answers
- minimal but sufficient context reads
- task-scoped changes and dirty-tree protection
- real validation evidence
- main Agent ownership and bounded Subagent routing
- review-first reporting
- Git branch, staging, commit, push, and PR defaults
- toolchain and browser preferences
- explicit authorization for irreversible or external operations

Do not add repository architecture, project build commands, temporary issue details, long prompt templates, or rules already owned by a Skill.

If the client provides a separate custom-instructions field, keep it as a pointer instead of copying all rules:

```text
~/.codex/AGENTS.md 是本机唯一的个人执行偏好来源。
请遵循当前任务路径下生效的 AGENTS.md；如有冲突，以我在当前对话中的明确要求为准。
```

### 5. Minimize Plugins and Connectors

- Keep only plugins and connectors that support demonstrated workflows.
- Prefer a connector when the need is live private data or external actions; do not install a large Skills plugin only to retain one connector capability.
- Preserve an authorized official Vercel Connector for deployment inspection, logs, and explicitly requested deployments without installing the large Vercel Skills plugin unless its additional workflows are needed.
- Keep Browser, Chrome, Computer Use, and GitHub when they are part of the user's verified workflow.
- Keep document, PDF, spreadsheet, presentation, Notion, and similar capabilities only when they are actually used or intentionally retained.
- Uninstall disabled plugins instead of leaving their Skills cached indefinitely.
- Do not modify official plugin cache contents in place.

### 6. Remove Configuration Drift

- Remove trusted-project entries whose paths no longer exist.
- Do not trust an entire home directory when narrower workspace roots are sufficient.
- Remove disabled duplicate MCP entries and approval overrides for capabilities that no longer exist.
- Preserve approval rules for connectors that remain installed and authorized.
- Remove project config copies that are identical to the global config.
- Allow project `.codex/config.toml` files to contain only genuine overrides.
- Keep explanatory workflow documentation synchronized with actual installed plugins, models, and Agents.

### 7. Validate the Result

Run checks supported by the installed environment, including:

1. Parse all changed TOML and YAML.
2. Run `codex --strict-config` through a harmless smoke test.
3. Run `codex doctor` or the available equivalent.
4. Confirm the effective model, reasoning, sandbox, approval policy, and writable roots.
5. If a Luna execution profile was added, confirm it loads without changing the base `Sol Medium` default.
6. Confirm every registered custom Agent resolves to an existing config file and remains read-only where required.
7. Run one non-ephemeral collaboration smoke test with Explorer and Test Analyst; verify the main Agent waits and synthesizes both results.
8. Confirm the Skill inventory has no unintended duplicate names, broken links, stale project install copies, or unreferenced plugin versions.
9. Confirm a fresh session does not report Skill-description context-budget truncation. If it does, reduce enabled plugins and overlapping Skills rather than shortening critical descriptions blindly.
10. Check final diffs and report all unverified behavior.

Do not use `codex exec --ephemeral` to validate Subagent collaboration if the installed release cannot preserve the parent thread in that mode.

## Done When

The optimization is complete only when:

- global and project configuration parse successfully
- the current Codex client accepts the configuration
- official and personal Skill update status is verified from real sources
- only necessary plugins and connectors remain enabled or installed
- stale trust entries, broken links, duplicate install copies, and proven orphan caches are removed
- model and Agent routing matches the installed model catalog
- approved writable roots work while other paths remain protected
- custom Agent collaboration succeeds in a real smoke test
- no unrelated user data or repository changes were removed
- remaining risks and intentional exceptions are explicitly reported

## Final Report

Return only the useful summary:

1. Configuration changes
2. Skill and plugin changes
3. Model and Agent routing
4. Permission boundaries
5. Validation results
6. Remaining risks or manual client-setting steps

Do not create a pull request, publish, deploy, or modify production systems unless the user explicitly asks.
