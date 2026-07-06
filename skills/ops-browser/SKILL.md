---
name: ops-browser
description: "Use when operating or verifying browser pages: screenshots, visual checks, responsive checks, data extraction, form/upload/download workflows, console/network/storage checks, or login/session-sensitive browser evidence."
---

# Ops Browser

## Overview

Operate browser pages as stateful user sessions and collect web evidence. Preserve existing tabs, windows, accounts, and foreground activity; leave frontend code and architecture changes to `frontend-implementation`.

## Workflow

1. Identify the target hostname, path, environment, account/session, and task goal.
2. Enumerate browser surfaces and existing tabs exposed by available tooling before opening anything new.
3. Choose the mode: Inspect/Verify, Visual/Responsive, Form/Upload, or Debug.
4. Prefer browser/tool APIs, DOM inspection, selectors, and deterministic actions over manual guessing.
5. Keep work in the background when practical; avoid stealing focus, moving the pointer, or coordinate-clicking.
6. Gather task evidence such as UI state, DOM, console, network, storage/auth state, screenshots, viewport behavior, downloads, route changes, or submitted payloads.
7. Distinguish direct evidence from inference; mark unchecked visual, network, account, or runtime claims as `Not verified`.
8. Close task-only temporary pages/windows after finishing, and report any temporary browser surface that remains open.

## Modes

- **Inspect/Verify:** confirm the page, account, and environment; collect visual or DOM/network evidence.
- **Visual/Responsive:** check layout, overflow, clipped text, dialogs, tables, hover/focus, and reachable loading/empty/error states across relevant viewports.
- **Form/Upload:** map fields by label, name, role, or test id; confirm file paths and final state before submission.
- **Debug:** reproduce or inspect the issue with the least disruptive page state changes; isolate cache/auth only when needed.

## Do Not Use For

- Real Tauri, Electron, or native desktop-client runtime/window proof; use `ops-client`.
- Frontend code changes, component architecture, design-system decisions, or UI implementation; use `frontend-implementation`.
- Repository onboarding, planning, local diff review, or security-only review; use the relevant `code-*` skill.
- Browser-only evidence when the user explicitly requested a real desktop app window.

## Hard Rules

- Prefer a matching open tab in the user's default or already-authenticated browser; do not switch to Chrome just because Chrome automation is available.
- Use browser or Chrome-extension APIs for matching tab inventory; use Computer Use only for visible/key-window state or desktop-level operation.
- Prefer Playwright for repeatable web automation that belongs in a repository or CI; keep one-off login/session checks in the browser that owns the required state.
- For persistent web conversations or workflows, record and reuse a stable session identifier for follow-up work on the same task.
- Keep one browser surface and one tab whenever practical; open extra or fresh pages only for named isolation, comparison, destructive-test, or evidence needs.
- Stop before login, MFA, consent, account switching, permission grants, destructive submits, or irreversible state changes unless explicitly authorized.
- Do not submit forms, upload files, clear cache, log out, refresh, or navigate away from user-owned state unless the task requires it.
- Mark unavailable tab/window identity, unchecked visual behavior, network state, account state, or runtime claims as `Not verified`.

## Output Contract

Report the browser surface used, why it matched the default/requested/session browser, tab or session identity when available, viewport(s), state-changing actions, evidence produced, `Not verified` gaps, and temporary page/window cleanup.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
