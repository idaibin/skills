---
name: ops-browser
description: "Use when operating or verifying browser pages: screenshots, visual checks, responsive checks, data extraction, form/upload/download workflows, console/network/storage checks, or login/session-sensitive browser evidence."
---

# Ops Browser

## Overview

Operate browser pages as stateful user sessions and collect web evidence. Preserve existing tabs, windows, accounts, and foreground activity; leave frontend code and architecture changes to `frontend-implementation`.

## Workflow

1. Identify the target hostname, path, environment, account/session, and task goal.
2. Enumerate browser sessions and existing tabs exposed by available tooling before opening anything new.
3. Choose the mode: Inspect/Verify, Visual/Responsive, Form/Upload, or Debug.
4. Prefer browser/tool APIs, DOM inspection, selectors, and deterministic actions over manual guessing.
5. Keep work in the background when practical; avoid stealing focus, moving the pointer, or coordinate-clicking.
6. Gather task evidence such as UI state, DOM, console, network, storage/auth state, screenshots, viewport behavior, downloads, route changes, or submitted payloads.
7. Distinguish direct evidence from inference; mark unchecked visual, network, account, or runtime claims as `Not verified`.
8. Close task-only temporary pages/windows after finishing, and report any temporary browser session that remains open.

## Modes

- **Local Project Debug:** for local projects that can be started by repo commands and tested without manual login, or with test credentials/seeded auth.
- **Managed Browser Session:** for browser checks where the agent can own the session, including user-completed sign-in or third-party login in that session.
- **User Browser Session:** for user-specified pages, uploads, downloads, or account state that must stay in the user's existing browser profile.
- **Inspect/Verify:** confirm the page, account, and environment; collect visual or DOM/network evidence.
- **Visual/Responsive:** check layout, overflow, clipped text, dialogs, tables, hover/focus, and reachable loading/empty/error states across relevant viewports.
- **Form/Upload:** map fields by label, name, role, or test id; confirm file paths and final state before submission.
- **Debug:** build a tight browser feedback loop, reproduce the symptom, inspect evidence, test one hypothesis at a time, and keep page state changes minimal.

## Do Not Use For

- Real Tauri, Electron, or native desktop-client runtime/window proof; use `ops-client`.
- Frontend code changes, component architecture, design-system decisions, or UI implementation; use `frontend-implementation`.
- Repository onboarding, planning, local diff review, or security-only review; use the relevant `code-*` skill.
- Browser-only evidence when the user explicitly requested a real desktop app window.

## Hard Rules

- Choose the session by evidence ownership: requested or recorded session first; existing tab with required login/state second; managed browser session when external profile state is not required; user browser session when the task depends on the user's existing profile, downloads, extensions, or account state.
- Enumerate available browser sessions and tabs before opening anything. Record tab id/handle when exposed, URL, title, account/session note, and reuse suitability.
- Reuse the same tab and browser session for a task whenever practical. Do not repeatedly open new tabs or windows just because lookup failed; re-enumerate, search by session record, URL, title, and account note first.
- For persistent web conversations or workflows, keep one stable session record per task and reuse it for follow-up work. Treat the stable session id or exact conversation URL as stronger than visible tab title.
- When opening an external AI review or chat workflow for a repository or long-running task, use the task's mapped project/workspace and existing conversation before creating a generic new chat. If no mapping exists, ask or create a record before sending substantial content.
- Treat AI project/workspace display names as mutable labels. Match first by project/workspace URL or id when available, then task key, repository path, aliases, and account note; update the display name in the record after observing a rename.
- Operate the intended target tab, not whichever tab is currently active. Revalidate tab identity before typing, uploading, downloading, submitting, or navigating away.
- If the recorded tab was closed, replaced, logged out, navigated away, or cannot be identified, report the session break before starting a new session.
- Keep one browser session and one tab whenever practical; open extra or fresh pages only for named isolation, comparison, destructive-test, or evidence needs.
- For browser debugging, establish a repeatable feedback loop before proposing fixes: target URL, steps, expected symptom, observed symptom, and the evidence source that will turn red/green.
- Reproduce and minimize the browser issue before changing page state. Test one hypothesis at a time and capture the before/after evidence that confirms or rejects it.
- Tag temporary debug probes, logs, screenshots, downloads, and local artifacts so they can be removed or reported at cleanup.
- For text entry, prefer page-native field operations over the system clipboard; use clipboard only as a saved-and-restored fallback.
- Use file upload only when attachment semantics are correct. For temporary upload files, create a task-specific folder on the Desktop by default, report the exact local path, and delete temporary local files/folders after the upload or when no longer needed unless the user asks to keep them.
- After deleting temporary upload files, state that local deletion does not remove any server-side uploaded attachment.
- Stop before login, MFA, consent, account switching, permission grants, destructive submits, or irreversible state changes unless explicitly authorized.
- Do not submit forms, upload files, clear cache, log out, refresh, or navigate away from user-owned state unless the task requires it.
- Mark unavailable tab/window identity, unchecked visual behavior, network state, account state, or runtime claims as `Not verified`.

## Output Contract

Report the browser session used, why it matched the task/session, tab or session identity when available, whether visible focus or tab activation was required, viewport(s), debug loop or reproduction steps when relevant, state-changing actions, evidence produced, upload temp paths and cleanup status, `Not verified` gaps, and temporary tab/window cleanup.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
