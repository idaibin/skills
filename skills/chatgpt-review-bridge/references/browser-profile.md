# Browser Profile Management

## Purpose

A bridge profile record maps a repository or task to browser routing metadata. It is not permission to mutate or delete real browser data.

## Record Fields

- `name`
- `repo_path`
- `default_browser_mode`: `capability-auto`, `codex-in-app-browser`, `current-chrome-explicit`, `standalone-playwright-explicit`, or `manual`
- `chatgpt_surface`: `standard-chat` or `project`
- `account_workspace_note`
- `browser`
- `profile_path`
- `profile_directory`
- `account_note`
- `chatgpt_default_url`
- `last_verified_at`
- `status`

Never store secrets, cookies, tokens, or browser storage. These fields are local bridge records, not repository-safe review metadata. When review evidence is committed, reduce workspace identity to its category and replace a full ChatGPT URL with a sanitized conversation reference unless verified repository privacy and explicit user authorization permit the full values.

## Mode Resolution

Resolve modes only after external-send authorization and capability preflight:

1. Explicit per-request mode whose required capability is available.
2. Verified session default.
3. Verified repository or user default.
4. A browser-control capability exposed by the current environment, preferring a verified Project route over a generic standard chat.
5. Current Chrome or standalone Playwright only when explicitly selected and controllable.
6. Package-only when no route can be proven.

## Codex In-App Browser Mode

Use only when the active environment exposes and successfully preflights an in-app Browser capability.

- Use `ops-browser` for low-level session, tab, composer, upload, and response-state operations; the bridge retains external authorization, package, round, conversation-attribution, and archive ownership.
- Reuse a verified project/conversation tab when available.
- Keep the in-app Playwright control API distinct from standalone Playwright browser launch.
- Ask the user to sign in inside the in-app Browser when authentication is required.
- If no in-app Browser capability is exposed, do not invent or install one; resolve another explicitly allowed route or return to Package-only.

## Current Chrome Mode

Use when the user wants an already-open Chrome tab.

- Enumerate tabs only after the user chooses this route.
- Present ChatGPT tabs by title, URL, and project-bound status.
- Claim only the selected tab.
- Mark profile path `Not verified` unless tooling exposes it.
- Do not call this a Playwright-launched profile; Playwright is only the control surface for a claimed tab.

## Standalone Playwright Local Profile Mode

Use when the user chooses a local profile or profile path.

- Ask for the profile before launch/attach.
- Report profile path, directory, channel, and lock status when verified.
- If attach is blocked, ask whether to close the conflict, choose another profile, or switch modes.
- Do not copy, delete, or mutate profile directories except through ordinary browser use needed for the confirmed review.

## Defaults

Use `capability-auto` as the default browser preference. It selects only from
capabilities proven in the current preflight. Prefer `project` when a verified
Project URL exists and `standard-chat` otherwise. Verify the active account
workspace separately. Update durable defaults only after explicit instruction.
A successfully controlled tab proves task-local control, not durable ownership
or workspace identity.

Reset clears bridge defaults such as `default_browser_mode`, `chatgpt_surface`, profile record, URL, active conversation id, tab handle, account/workspace note, and verification timestamp.

Reset does not remove real Chrome profiles, cookies, local storage, history, downloads, extensions, ChatGPT conversations, review artifacts, commits, or code changes.

Delete means deleting the bridge record unless the user explicitly approves real browser data deletion with an exact path.
