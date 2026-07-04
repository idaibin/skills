---
name: ops-browser
description: "Use when operating or verifying browser pages: screenshots, data extraction, local web app testing, form/upload/download workflows, console/network/storage checks, or login/session-sensitive browser evidence."
---

# Ops Browser

## Overview

Operate browser pages as stateful user sessions. Preserve existing tabs, windows, accounts, and foreground activity while collecting evidence from the right page.

## Workflow

1. Identify the target hostname, path, environment, account/session, and task goal.
2. Inspect existing browser tabs/windows before opening anything new.
3. Choose the mode: Inspect/Verify, Form/Upload, or Debug.
4. Prefer browser/tool APIs, DOM inspection, selectors, and deterministic actions over manual guessing.
5. Keep work in the background when practical; avoid stealing focus, moving the pointer, or coordinate-clicking.
6. Gather task evidence such as UI state, DOM, console, network, storage/auth state, screenshots, downloads, route changes, or submitted payloads.
7. Distinguish direct evidence from inference; mark unchecked visual, network, account, or runtime claims as `Not verified`.
8. Close task-only temporary pages/windows after finishing.

## Modes

- **Inspect/Verify:** confirm the page, account, and environment; collect visual or DOM/network evidence.
- **Form/Upload:** map fields by label, name, role, or test id; confirm file paths and final state before submission.
- **Debug:** reproduce or inspect the issue with the least disruptive page state changes; isolate cache/auth only when needed.

## Do Not Use For

- Real Tauri, Electron, or native desktop-client runtime/window proof; use `ops-client`.
- Repository onboarding, planning, local diff review, or security-only review; use the relevant `code-*` skill.
- Browser-only evidence when the user explicitly requested a real desktop app window.

## Hard Rules

- Reuse a matching open tab when it is in the right environment/session and will not disturb unrelated user work.
- Open a fresh page/session when account, cache, auth, upload, or destructive-test isolation is required.
- Stop before login, MFA, consent, account switching, purchase, permission grant, destructive submit, or irreversible state changes unless the user explicitly authorized that action.
- Do not submit forms, upload files, clear cache, log out, refresh, or navigate away from user-owned state unless the task requires it.
- Say `Not verified` for unchecked browser/runtime claims.

## Output Contract

Report the browser surface used, whether an existing tab was reused, state-changing actions performed, evidence or artifacts produced, and whether temporary pages/windows were closed.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` when trigger scope, modes, hard rules, or output contract changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
