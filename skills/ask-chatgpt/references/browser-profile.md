# Transport And Browser Profile

## Purpose

A review profile record stores transport preferences and browser-specific metadata.
Routing behavior belongs to `chatgpt-routing.md`; this record is never authorization
or current-state evidence.

## Record Fields

- `name`
- `repo_path`
- `default_transport_mode`: `codex-app-native`, `desktop-built-in-browser`, or
  `manual`. Current Chrome and standalone Playwright require a current-request
  selection and are not durable transport defaults.
- `default_browser_mode`: legacy browser-fallback preference; it does not override
  App-native-first transport selection. `capability-auto` also means App-native first.
- `chatgpt_surface`: `standard-chat` or `project`
- `chatgpt_project_name`: secondary discovery hint only
- `chatgpt_interface`: `chat` or `work`
- `chatgpt_model`
- `chatgpt_reasoning_mode`
- `chatgpt_reasoning_fallbacks`
- `account_workspace_note`
- `browser`
- `profile_path`
- `profile_directory`
- `account_note`
- `chatgpt_default_url`
- `last_verified_at`
- `status`

Never store secrets, cookies, tokens, or browser storage. These fields are local bridge records, not repository-safe review metadata. When review evidence is committed, reduce workspace identity to its category and replace a full ChatGPT URL with a sanitized conversation reference unless verified repository privacy and explicit user authorization permit the full values.

Store durable records at `~/.agents/config/ask-chatgpt/defaults.yaml`, never inside
the installed package. Explicit request values override this record. A stored Project
name, URL, conversation identifier, model, reasoning mode, browser tab, or profile
does not prove current availability or selection.

Only `default_transport_mode` changes the durable transport preference. Its
`codex-app-native` and `desktop-built-in-browser` values change which of those two
non-interrupting routes is tried first; `manual` stops before external action until
the current request selects a route. Preserve an existing `default_browser_mode` as
the browser choice used after the selected transport is unavailable or insufficient;
do not silently migrate it into a transport override. Legacy Chrome or standalone
values remain hints only and never authorize those routes without current confirmation.

Browser fields apply only to browser routes. Keep built-in, cloud/agent reviewer,
Chrome, and standalone profile identities separate; do not transfer cookies, login,
tabs, or capability evidence between them. A profile path is `Not verified` unless
the active control surface exposes it. Detailed mode selection and operation rules
belong to `chatgpt-routing.md`.

## Reset

Update durable defaults only after explicit instruction. Reset clears bridge records
such as transport mode, ChatGPT surface, profile record, URL, active conversation ID,
tab handle, account/workspace note, and verification timestamp.

Reset does not remove real Chrome profiles, cookies, local storage, history, downloads, extensions, ChatGPT conversations, review artifacts, commits, or code changes.

Delete means deleting the bridge record unless the user explicitly approves real browser data deletion with an exact path.
