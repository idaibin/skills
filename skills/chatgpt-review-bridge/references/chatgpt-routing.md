# ChatGPT Routing And IO

## Terminology Basis

- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)
  documents Projects across free and paid plan types; use `project` for durable
  project context rather than inventing another product surface.
- [ChatGPT Enterprise workspaces](https://help.openai.com/en/articles/8265430-what-is-a-workspace-how-can-i-switch-workspaces)
  documents account environments with separate conversations and files. Verify
  and record workspace identity independently from Project identity.

## Authorization Before Routing

Do not resolve or open a browser route for requests that only say prepare,
build, draft, package, or create review material. Generate
`<repo-root>/review-package.md` and stop. Continue below only when the user
explicitly authorizes an external send, use of ChatGPT now, or a bounded number
of external review rounds.

## Routing Order

1. Explicit user surface, URL, or browser mode.
2. Session surface and `chatgpt_default_url`.
3. Repository or user surface and `chatgpt_default_url`.
4. A Project through a verified browser-control capability exposed by the current environment.
5. A standard chat through a verified browser-control capability at `https://chatgpt.com/`.
6. Current Chrome or standalone Playwright only when explicitly selected and controllable.
7. Package-only when no route can be proven.

If generic ChatGPT is used, report that the review is not project-bound.

## Surface Resolution

- Resolve `project` for repository-bound, persistent, or multi-round review when a verified Project URL exists.
- Resolve `standard-chat` for one-off review or when no durable Project route exists.
- Resolve `codex` only as the executor or as an explicitly requested separate-agent review. Never count self-review as an independent ChatGPT pass.
- Treat UI labels as presentation details. Route by verified capability and URL so a label change does not silently change behavior.
- Verify and record the active account workspace independently. A Project is
  available across plan types, and its URL does not establish personal or
  organization workspace membership.

## Default Configuration

Default to `capability-auto` for new bridge records. This is a preference to use
an available verified browser capability, not proof that any browser tool is
installed.

Runtime defaults may come from a durable local config file:

```text
~/.agents/config/chatgpt-review-bridge/defaults.yaml
```

Read that file after explicit per-request and session settings, and before falling back to the generic ChatGPT URL. Do not store machine-specific defaults inside the installed skill package because package updates may overwrite them.

Supported fields:

- `default_browser_mode`: `capability-auto`, `codex-in-app-browser`, `current-chrome-explicit`, `standalone-playwright-explicit`, or `manual`
- `chatgpt_surface`: `standard-chat` or `project`
- `account_workspace_note`
- `chatgpt_default_url`
- `profile_record_name`
- `profile_path`
- `repo_path`
- `branch_scope`

Example:

```yaml
default_browser_mode: capability-auto
chatgpt_surface: project
account_workspace_note: Not verified
chatgpt_default_url: https://chatgpt.com/g/<project-id>/project
```

Changing defaults is a persistent bridge-default change and requires explicit instruction.

## Current Chrome Routing

After the user chooses current Chrome mode:

1. Enumerate open ChatGPT tabs.
2. Present candidate tabs and require an explicit tab selection or confirmation.
3. Claim only the confirmed tab.
4. Stop before sending unless the current authorization explicitly covers this selected tab, package scope, and round count.

Do not save a selected tab or URL as a default unless separately requested.

## Browser Capability Routing

After an external send is explicitly authorized:

1. Preflight the browser capabilities actually exposed by the environment.
2. Use `ops-browser` as the low-level browser operator for session/tab selection, navigation, composer/upload inspection, submission, completion evidence, and response extraction. The bridge continues to own package scope, authorization, surface, round count, conversation attribution, and archive paths.
3. Reuse the mapped ChatGPT Project conversation when available.
4. If the verified Project has no conversation and the user authorized sending, open the Project landing page and create exactly one conversation. Verify its stable URL/ID and empty composer state before submit when exposed. If the surface assigns identity only on first submit, record the pre-send Project/account evidence, make the one authorized submit, then verify and store the resulting URL/ID before accepting the response or continuing. Do not create a conversation for Package-only requests.
5. Otherwise open the configured Project URL or a standard chat through the selected capability.
6. Ask the user to sign in inside that controlled browser when authentication is required.
7. Mark Project identity and account workspace `Not verified` unless each is inspected.
8. Stop before sending unless the current authorization covers the resolved route, scope, and round count.

If the environment lacks the required control or evidence capability, do not load
or claim an unbundled browser helper. Return to Package-only.

## Standalone Playwright Routing

Use only when explicitly selected and verified for the authorized scope. If the in-app Browser is unavailable and standalone was not explicitly selected, return to Package-only instead of switching routes. Ask for a profile only when profile mode is explicit or a profile record exists. Do not install browser binaries merely because the in-app Browser route is available.

If no browser session, tab identity, account state, upload state, or response completion signal can be verified, stop or mark the affected field `Not verified`.

## Text And File Input

Use `<repo-root>/review-package.md` as the canonical outbound artifact unless the user names another path. Use text input for compact packages and file/pasted attachments when size or structure matters. If pasted content becomes an attachment, treat it as the single intended upload for that send action, verify the composer state, and do not paste or upload again unless the first attempt is removed or clearly failed. Never upload secrets, `.env`, private registry tokens, local keychains, browser profile data, or unrelated dirty files.

For a multipart artifact set, verify the manifest counts and SHA-256 values before browser work. Send the manifest with a wait-for-final instruction, then exactly one part per message in order. Verify each attachment and acknowledgement, retry only an inspected failed part, and send `FINAL PART` plus the review prompt only after the complete set matches the manifest. Treat early reviewer analysis, a missing acknowledgement, or any count/order/hash mismatch as an incomplete round.

## Output Capture

Capture only external ChatGPT responses into `<repo-root>/review.md` by direct page extraction, download, or selected response text. Do not put the outbound package in this file. Screenshots are supporting evidence only. Keep the artifact local-private and untracked by default; if repository delivery is explicitly requested, apply the visibility policy in `usage.md` and sanitize public or visibility-unknown output before staging.

Accept a response only when it can be tied to:

- intended and final URL
- branch/commit/diff basis
- submitted input or attachment names/counts
- completion signal or `Not verified`
- latest assistant response extraction method

Reject or mark `Not verified` if the tab is ambiguous, generation is still streaming, output is empty/truncated, or the response predates the submitted prompt.

For multiple rounds, append one attributed pass per round and verify Codex's
changes before sending the next package. Reuse the same Project conversation by
default; use separate conversations only when independence is requested.

## Prompt Template

```text
You are the reviewer. Codex is the executor.

Review the supplied branch/diff/files for concrete defects, regressions, missing tests, and unsafe assumptions. Prioritize actionable findings with file/path references when possible.

Return:
1. Findings ordered by severity
2. False-positive risks or assumptions
3. Suggested verification
4. Verdict: pass, needs changes, or blocked
```
