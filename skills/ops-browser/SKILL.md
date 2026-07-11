---
name: ops-browser
description: "Use when operating or verifying browser pages: screenshots, visual checks, responsive checks, data extraction, form/upload/download workflows, console/network/storage checks, or login/session-sensitive browser evidence."
---

# Ops Browser

## Overview

Operate browser pages as stateful user sessions and collect web evidence. Start with a capability preflight so the workflow degrades explicitly when tab control, profile reuse, console/network access, uploads, downloads, or background operation are unavailable. Leave frontend code changes to `implement-frontend`.

## Workflow

1. Identify the target hostname, path, environment, account/session, and task goal.
2. Run a capability preflight before navigation or claims. Record available/unavailable/unknown for:
   - browser session and tab enumeration;
   - existing-tab control and stable tab/session identifiers;
   - managed browser creation;
   - user-profile or authenticated-session reuse;
   - DOM/accessibility inspection and deterministic selectors;
   - console, network, storage, cookie, and download inspection;
   - screenshot and viewport control;
   - file upload and local artifact access;
   - background-safe operation without stealing focus.
3. Enumerate browser sessions and existing tabs only when the available tool exposes them; never invent missing tab/window identity.
4. Choose the mode and evidence plan based on capability and ownership: Local Project, Managed Session, User Session, Inspect/Verify, Visual/Responsive, Form/Upload, or Debug.
5. Reuse the evidence-bearing session and target tab when it can be identified safely. Otherwise open an isolated managed page only when the task does not depend on unavailable user-profile state.
6. Prefer browser/tool APIs, DOM inspection, roles, labels, test ids, and deterministic actions over manual guessing.
7. Gather only evidence the tool can actually expose: UI state, DOM/accessibility, console, network, storage/auth state, screenshots, viewport behavior, downloads, route changes, or submitted payloads.
8. Distinguish direct evidence from inference; mark unavailable or unchecked claims `Not verified`.
9. Close task-only temporary pages/windows and clean temporary local artifacts when the tool supports it; report anything left open or undeleted.

## Modes

- **Local Project:** for repository-startable apps with deterministic commands and no required external user-profile login, or with explicit test credentials/seeded auth.
- **Managed Browser Session:** for agent-owned browsing, isolated verification, or user-completed login inside that managed session.
- **User Browser Session:** only when tooling can safely identify and control the user's requested existing browser/profile and the task requires its account, extension, download, or tab state.
- **Inspect/Verify:** confirm page, environment, rendered state, account/session evidence, and requested behavior.
- **Visual/Responsive:** check relevant viewports, overflow, clipping, dialogs, tables, hover/focus, and reachable feedback states.
- **Form/Upload:** map controls semantically, verify source file/path and final state, and stop before unauthorized submission.
- **Debug:** define a repeatable browser red/green loop, reproduce and minimize the symptom, test one hypothesis at a time, and clean probes.
- **Degraded evidence:** when required browser capabilities are missing, perform only supported checks, state the blocked claims, and provide the exact artifact or manual action needed to continue.

## Do Not Use For

- Real Tauri, Electron, or native desktop-client runtime/window proof; use `ops-client`.
- Frontend code changes, component architecture, design-system decisions, or UI implementation; use `implement-frontend`.
- Repository onboarding, planning, local diff review, or security-only review; use the relevant `code-*` skill.
- Browser-only evidence when the user explicitly requested a real desktop app window.
- External ChatGPT review orchestration, package construction, send authorization, round counting, conversation attribution, or response archiving; use `chatgpt-review-bridge`. This skill may perform only the low-level browser actions that bridge explicitly routes.

## Hard Rules

- Do not claim a capability from the skill text. Capability exists only when the active tool exposes and successfully performs it.
- When called by `chatgpt-review-bridge`, require the bridge-provided surface, authorization state, package path, round scope, selected browser route/capability, and conversation mapping or explicit first-conversation policy. Follow that route exactly. If its capability or identity evidence fails, return the blocked state to the bridge; do not switch sessions or create a managed fallback independently.
- Choose the session by evidence ownership: requested/recorded session first when identifiable; existing tab with required state second; managed session when external profile state is unnecessary; user session only when supported and required.
- Enumerate sessions/tabs before opening anything only when enumeration is available. If unavailable, state that limitation and avoid claiming reuse or account identity.
- Reuse the same tab/session whenever practical. Revalidate target identity before typing, uploading, downloading, submitting, or navigating away.
- Stable session/conversation IDs and exact URLs are stronger than visible titles; tool-specific handles may expire and must be revalidated.
- Do not treat page title, avatar, visible email fragment, or successful page load as sufficient account/workspace proof.
- If a recorded session is closed, logged out, replaced, or cannot be identified, report the break. Do not silently create a new page and call it the same session.
- Keep extra tabs/windows only for named isolation, comparison, destructive-test, or evidence needs.
- For debugging, establish exact URL, steps, expected symptom, observed symptom, and red/green evidence before proposing fixes.
- Test one browser hypothesis at a time. Do not bundle refresh, cache clearing, account switch, viewport changes, and code edits.
- Prefer page-native field operations. Use the system clipboard only as a saved-and-restored fallback.
- Use file upload only when attachment semantics are correct. Temporary files must use a task-specific path appropriate to the active environment; do not assume Desktop exists in remote/container runtimes.
- Report exact temp paths and delete task-owned local artifacts when supported. Local deletion never removes a server-side attachment.
- Stop before login credentials, MFA, consent, account switching, permission grants, purchases, destructive submits, or irreversible state changes unless explicitly authorized.
- Do not refresh, clear cache/storage, log out, submit, upload, or navigate away from user-owned state unless required and authorized.
- Match evidence to claims: screenshots prove visual state, DOM/accessibility proves rendered semantics, console proves client logs, network proves requests/responses, storage proves stored state, and file checks prove downloads.
- Mark unsupported tab/window identity, account state, console/network/storage, background safety, viewport behavior, downloads, or runtime claims `Not verified`.

## Output Contract

Report the capability preflight, selected mode, browser/session and tab identity evidence, account/workspace evidence or `Not verified`, whether visible focus was required, viewport(s), state-changing actions, debug loop when relevant, evidence produced, upload/download temp paths and cleanup, degraded or blocked claims, caller-owned orchestration fields left unchanged, and temporary page/window cleanup.

## Skill Maintenance

When maintaining this package, keep `SKILL.md` concise, move detailed examples to `references/`, update `agents/openai.yaml`, and run `python3 scripts/validate-skills.py`.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and workflow details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
