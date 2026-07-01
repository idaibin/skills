---
name: ops-client
description: Use when operating or verifying a real desktop client app window, currently focused on Tauri apps, including screenshot evidence, process/window diagnosis, runtime-source checks, Accessibility/AXPress actions, AI-operable DOM/control design, or rejecting browser-preview substitutes. Triggers include 客户端操作, Tauri 调试, 真实窗口验证, CGWindowID, AXPress, and 不抢鼠标.
---

# Ops Client

## Overview

Operate and verify real desktop client windows. Current guidance is Tauri-focused, but the skill applies to client apps where browser previews are not valid evidence.

## Workflow

1. Identify the target app name, process, PID, visible window, and requested evidence.
2. Confirm runtime source: `pnpm tauri dev`, debug bundle, release app, or other explicit client runtime.
3. Enumerate real windows and identify the matching `CGWindowID` by owner, PID, title, and bounds.
4. Capture the real window without relying on foreground focus:
   `screencapture -x -l<CGWindowID> /private/tmp/desktop-client-window.png`
5. Inspect screenshots with `view_image` before claiming visual evidence.
6. Prefer background-safe inspection and Accessibility actions such as `AXPress` on named controls.
7. Rebuild/restart the intended client instance after relevant UI, bundle, or Accessibility changes before re-verifying.

## Modes

- **Window Evidence:** prove process, runtime, window identity, and screenshot source.
- **Interaction:** use Accessibility/control-tree paths before coordinate clicks.
- **AI-Operable UI:** improve DOM and Accessibility surfaces so agents can identify controls reliably.

## Hard Rules

- Do not treat browser previews, dev server pages, or region screenshots as desktop-client evidence unless the user explicitly asks for browser-only checking.
- Do not steal the user's mouse, move the pointer, activate unrelated windows, or coordinate-click unless no stable control path exists and the risk is acceptable.
- Prefer semantic controls, accessible names, `aria-label`, `title`, `sr-only`, associated form labels, and stable `data-testid` selectors for critical controls.
- Say `Not verified` when process, runtime, window source, or interaction evidence is unchecked.

## Output Contract

Report the target process/runtime, real-window evidence, screenshot source, interaction method, accessibility or DOM gaps, restart/rebuild status, and anything `Not verified`.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` when trigger scope, modes, hard rules, or output contract changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
