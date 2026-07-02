---
name: ops-client
description: Use when operating or verifying a specified real desktop client window, proving Tauri/Electron/native runtime source, reviewing launch commands, capturing CGWindowID evidence, or improving AI-operable client controls.
---

# Ops Client

## Overview

Operate and verify real desktop client windows. Current guidance is Tauri-focused, but the skill applies to client apps where browser previews are not valid evidence.

## Workflow

1. Identify the specified client target: app name, repository path, package/app directory, process, PID, visible window, and requested evidence.
2. If working from a repository, confirm whether it contains a desktop/client app by checking manifests and source layout such as `src-tauri/`, `tauri.conf.*`, Electron configs, native app targets, package scripts, justfile tasks, or README run instructions.
3. Confirm the startup command and runtime source before verification: `pnpm tauri dev`, debug bundle, release app, Electron/native run command, or `Not found`/`Not verified` when unclear.
4. Enumerate real windows and identify the matching `CGWindowID` by owner, PID, title, and bounds.
5. Capture the real window without relying on foreground focus:
   `screencapture -x -l<CGWindowID> /private/tmp/desktop-client-window.png`
6. Inspect screenshots with `view_image` before claiming visual evidence.
7. Prefer background-safe inspection and Accessibility actions such as `AXPress` on named controls.
8. Rebuild/restart the intended client instance after relevant UI, bundle, or Accessibility changes before re-verifying.

## Modes

- **Launch Review:** identify the repository-owned client app and its startup command before running or verifying it.
- **Window Evidence:** prove process, runtime, window identity, and screenshot source.
- **Interaction:** use Accessibility/control-tree paths before coordinate clicks.
- **AI-Operable UI:** improve DOM and Accessibility surfaces so agents can identify controls reliably.

## Do Not Use For

- Plain browser pages, web previews, form workflows, downloads, or browser console/network checks; use `ops-browser`.
- Ordinary repository discovery unless the user asks for client launch review, real-window verification, or browser-preview invalidation.
- Browser preview evidence when the task requires proof from a Tauri, Electron, or native desktop runtime.
- Local diff review, planning, or security-only review; use the relevant `code-*` skill.

## Hard Rules

- Do not treat browser previews, dev server pages, or region screenshots as desktop-client evidence unless the user explicitly asks for browser-only checking.
- Do not start or restart a client before confirming the startup command source and whether it could disturb an existing app instance, active window, or user workflow.
- Do not steal the user's mouse, move the pointer, activate unrelated windows, or coordinate-click unless no stable control path exists and the risk is acceptable.
- Prefer semantic controls, accessible names, `aria-label`, `title`, `sr-only`, associated form labels, and stable `data-testid` selectors for critical controls.
- Say `Not verified` when process, runtime, window source, or interaction evidence is unchecked.

## Output Contract

Report the specified client target, repository/client ownership evidence, startup command or `Not found`, target process/runtime, real-window evidence, screenshot source, interaction method, accessibility or DOM gaps, restart/rebuild status, and anything `Not verified`.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` when trigger scope, modes, hard rules, or output contract changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
