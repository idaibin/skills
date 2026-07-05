---
name: ops-browser
description: "Use when operating or verifying browser pages: screenshots, visual checks, responsive checks, data extraction, form/upload/download workflows, console/network/storage checks, or login/session-sensitive browser evidence."
---

# Ops Browser

## Overview

Operate browser pages as stateful user sessions and collect web evidence. Preserve existing tabs, windows, accounts, and foreground activity; leave frontend code and architecture changes to `frontend-implementation`.

## Workflow

1. Identify the target hostname, path, environment, account/session, and task goal.
2. Inspect existing browser tabs/windows before opening anything new.
3. Choose the mode: Inspect/Verify, Visual/Responsive, Form/Upload, or Debug.
4. Prefer browser/tool APIs, DOM inspection, selectors, and deterministic actions over manual guessing.
5. Keep work in the background when practical; avoid stealing focus, moving the pointer, or coordinate-clicking.
6. Gather task evidence such as UI state, DOM, console, network, storage/auth state, screenshots, viewport behavior, downloads, route changes, or submitted payloads.
7. Distinguish direct evidence from inference; mark unchecked visual, network, account, or runtime claims as `Not verified`.
8. Close task-only temporary pages/windows after finishing.

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

- Reuse a matching open tab when it is in the right environment/session and will not disturb unrelated user work.
- Open a fresh page/session when account, cache, auth, upload, or destructive-test isolation is required.
- For visible UI changes, check relevant viewport targets such as 375px mobile, 768px tablet for complex layouts, and 1440px desktop when practical.
- Stop before login, MFA, consent, account switching, purchase, permission grant, destructive submit, or irreversible state changes unless the user explicitly authorized that action.
- Do not submit forms, upload files, clear cache, log out, refresh, or navigate away from user-owned state unless the task requires it.
- Say `Not verified` for unchecked browser/runtime claims.

## Output Contract

Report the browser surface used, viewport(s), whether an existing tab was reused, state-changing actions performed, evidence or artifacts produced, visual/runtime gaps marked `Not verified`, and whether temporary pages/windows were closed.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
