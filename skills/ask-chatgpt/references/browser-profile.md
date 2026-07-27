# Transport And Browser Profile

## Purpose

A review profile record stores transport preferences and browser-specific metadata.
Routing behavior belongs to `chatgpt-routing.md`; this record is never authorization
or current-state evidence.

## Record Fields

- `schema_version`: `ask-chatgpt-defaults/v2` for records that use
  `default_transport_mode`; an absent value is a legacy record
- `name`
- `repo_path`
- `default_transport_mode`: `codex-app-native`, `desktop-built-in-browser`, or
  `manual`. Current Chrome and standalone Playwright require a current-request
  selection and are not durable transport defaults.
- `default_browser_mode`: browser preference and legacy transport field; its meaning
  depends on the record version below
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

For `ask-chatgpt-defaults/v2`, `default_transport_mode` is required and changes the
durable transport preference. Its `codex-app-native` and
`desktop-built-in-browser` values change which of those two catalog-classified
non-interrupting routes is tried first; `manual` stops before external action until the
current request selects a route. `default_browser_mode` then selects only a browser
fallback. New v2 records must write `codex-app-native` explicitly when the user has not
selected another durable transport. A missing or unknown v2 transport value is
malformed and blocks external action pending explicit repair.

An existing record without `schema_version` is legacy and retains its previous route
meaning:

- missing mode, `desktop-built-in-browser`, and `capability-auto` remain built-in-first;
- `manual` stops before external action;
- `current-chrome-explicit` and `standalone-playwright-explicit` remain hints that
  require current-request confirmation; without it, preserve the legacy built-in-first
  fallback;
- `chatgpt-cloud-browser` is not a transport route in the current contract, so stop and
  request explicit migration instead of guessing its prior intent;
- any unknown value stops before external action pending explicit repair.

If an unversioned record already contains `default_transport_mode`, or a record has an
unknown schema version, treat it as an ambiguous configuration and stop before external
action. Do not guess which generation wrote it. Request an explicit migration or repair.

Do not reinterpret or rewrite a legacy record automatically. Migration is a persistent
configuration change and requires explicit instruction. Migrate atomically by adding
`schema_version: ask-chatgpt-defaults/v2`, adding the selected
`default_transport_mode`, and retaining `default_browser_mode` only as the browser
fallback. Report the before/after routing meaning.

Browser fields apply only to browser routes. Keep built-in, cloud/agent reviewer,
Chrome, and standalone profile identities separate; do not transfer cookies, login,
tabs, or capability evidence between them. A profile path is `Not verified` unless
the active control surface exposes it. Detailed mode selection and operation rules
belong to `chatgpt-routing.md`.

## Reset

Update or migrate durable defaults only after explicit instruction. Reset clears bridge
records such as schema version, transport mode, browser mode, ChatGPT surface, profile
record, URL, active conversation ID, tab handle, account/workspace note, and
verification timestamp.

Reset does not remove real Chrome profiles, cookies, local storage, history, downloads, extensions, ChatGPT conversations, review artifacts, commits, or code changes.

Delete means deleting the bridge record unless the user explicitly approves real browser data deletion with an exact path.
