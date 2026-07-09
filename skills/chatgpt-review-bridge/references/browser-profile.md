# Browser Profile Management

## Purpose

A bridge profile record maps a repository or task to browser routing metadata. It is not permission to mutate or delete real browser data.

## Record Fields

- `name`
- `repo_path`
- `default_browser_mode`: `playwright`, `current-chrome-explicit`, or `manual`
- `browser`
- `profile_path`
- `profile_directory`
- `account_note`
- `chatgpt_default_url`
- `last_verified_at`
- `status`

Never store secrets, cookies, tokens, or browser storage.

## Mode Resolution

1. Explicit per-request mode.
2. Session default.
3. Repository or user default.
4. Playwright with configured ChatGPT URL.
5. Playwright with generic ChatGPT.
6. Current Chrome ChatGPT tab only when explicitly selected or when Playwright is unavailable.

## Current Chrome Mode

Use when the user wants an already-open Chrome tab.

- Enumerate tabs only after the user chooses this route.
- Present ChatGPT tabs by title, URL, and project-bound status.
- Claim only the selected tab.
- Mark profile path `Not verified` unless tooling exposes it.
- Do not call this a Playwright-launched profile; Playwright is only the control surface for a claimed tab.

## Playwright Local Profile Mode

Use when the user chooses a local profile or profile path.

- Ask for the profile before launch/attach.
- Report profile path, directory, channel, and lock status when verified.
- If attach is blocked, ask whether to close the conflict, choose another profile, or switch modes.
- Do not copy, delete, or mutate profile directories except through ordinary browser use needed for the confirmed review.

## Defaults

Use `playwright` as the default browser mode unless a user, session, or repo record explicitly chooses another mode. Update defaults only after explicit instruction. A successfully claimed tab proves task-local control, not durable ownership.

Reset clears bridge defaults such as `default_browser_mode`, profile record, URL, active conversation id, tab handle, account note, and verification timestamp.

Reset does not remove real Chrome profiles, cookies, local storage, history, downloads, extensions, ChatGPT conversations, review artifacts, commits, or code changes.

Delete means deleting the bridge record unless the user explicitly approves real browser data deletion with an exact path.
