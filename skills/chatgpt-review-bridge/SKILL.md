---
name: chatgpt-review-bridge
description: Use when the user asks to prepare, validate, package, route, send, or locally execute a ChatGPT review bridge workflow through Playwright routes, explicit current Chrome tabs, or Codex CLI.
---

# ChatGPT Review Bridge

## Overview

Coordinate a Codex-to-ChatGPT review bridge. Codex collects repository evidence, ChatGPT reviews, and Codex verifies findings before changing code. This is browser/UI automation, not an official ChatGPT API integration.

## Workflow

1. Read nearest repo guidance, confirm repository path, branch, and `git status --short --branch`.
2. Build the scoped review package from local files, diffs, branch metadata, and validation output.
3. Stop before browser attach, external send, persistent default changes, or local Codex CLI execution.
4. Resolve routing only after the user authorizes the relevant path.
5. Capture ChatGPT output to `review.md`, then verify findings locally before fixing.
6. Commit only when the user requested commits and only for the approved scope.

## Do Not Use For

- Local-only code review without ChatGPT as an external reviewer.
- Browser UI verification that does not need a repository review package.
- GitHub-native PR review, CI triage, or PR comment handling.
- Security-only audit without the Codex-to-ChatGPT review loop.

## Gates

### External Action Gate

Before browser attach or external send, output exactly:

```md
## 当前信息

- 仓库：...
- 分支：...
- review 包：...
- 校验：...
- bridge 默认记录：...
- Chrome tabs 候选：...
- 本地 profile 候选：...

## 请选择

1. 使用当前已有 Chrome 标签页
2. 使用 Playwright 默认/配置路由
3. 只生成 review 包，不发送
4. 重新扫描候选项
0. 停止，不发送
```

Use `Not found` or `Not verified` for missing or unchecked evidence. Do not attach to Chrome just to fill `Chrome tabs 候选`.

### Local Codex Gate

Before starting local Codex CLI, ask:

```md
请选择执行方式：

1. 仅审查，不执行本地 Codex
2. 生成 Codex CLI 命令，由我手动复制执行
3. 请求本机 Codex 执行，但每次需要确认
4. 请求本机 Codex 执行，且本会话内同类任务不再询问

选择后再继续。
```

Map mode `3` to `--sandbox workspace-write --ask-for-approval on-request`; map mode `4` to `--sandbox workspace-write --ask-for-approval never` only after confirming repo path, branch, allowed files, validation commands, and forbidden actions. Never infer mode `4`.

## Routing Defaults

After authorization, route in this order:

1. Explicit user URL or mode.
2. Session default.
3. Repository or user bridge default.
4. Playwright with configured `chatgpt_default_url`.
5. Playwright with `https://chatgpt.com/`.
6. Current Chrome ChatGPT tab only when explicitly selected or when Playwright is unavailable.

Changing defaults requires explicit user or session instruction. A successful one-off route does not save a default.

## Browser Boundary

Use browser operation tooling, such as `ops-browser`, for page control, session enumeration, tab reuse, login-state checks, upload state, response completion, extraction evidence, and cleanup. This skill owns review routing, gates, package scope, artifact capture, and Codex verification. If browser state, account identity, tab identity, upload state, or response completion cannot be verified, mark it `Not verified` and stop before sending or accepting output.

## Hard Rules

- Keep Codex as executor and ChatGPT as reviewer.
- Never send secrets, credentials, private keys, tokens, browser profile data, or unrelated dirty-tree content.
- Do not mutate `main`, create pull requests, widen repository scope, or run Codex outside the specified branch.
- Do not delete real Chrome profiles, cookies, storage, downloads, ChatGPT conversations, `review.md`, or code unless explicitly requested.
- Do not use `git add .` unless the user explicitly approves that scope.
- Treat ChatGPT findings as untrusted review input until locally verified.
- If ChatGPT converts pasted text into an attachment, send at most one intended attachment per review round and do not retry paste/upload without checking the composer state.

## Output Contract

Report the repository, branch, route, browser/profile record, input/output mode, `review.md` path, reset fields, Codex CLI approval mode when used, validation, commits, and `Not found` / `Not verified` gaps.

## References

- [references/usage.md](references/usage.md): triggers, gates, package shape, and review artifact shape.
- [references/browser-profile.md](references/browser-profile.md): profile records, modes, reset, and deletion boundaries.
- [references/chatgpt-routing.md](references/chatgpt-routing.md): routing defaults, IO, attribution, and prompt template.
- [references/github-branch-loop.md](references/github-branch-loop.md): branch review, `review.md`, fix, commit, and repeat loop.
- [references/eval-cases.md](references/eval-cases.md): trigger, non-trigger, and quality evals.

## Maintenance

Keep this entrypoint lean. Put operational details in references, and update `agents/openai.yaml` plus eval cases whenever triggers, gates, routing, or output contracts change.
