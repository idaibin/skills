# ChatGPT Routing And IO

## Routing Order

1. Explicit user URL or mode.
2. Session `chatgpt_default_url`.
3. Repository or user `chatgpt_default_url`.
4. Playwright with configured ChatGPT URL.
5. Playwright with `https://chatgpt.com/`.
6. Current Chrome ChatGPT tab only when explicitly selected or when Playwright is unavailable.

If generic ChatGPT is used, report that the review is not project-bound.

## Default Configuration

Default to Playwright for new bridge records.

Runtime defaults may come from a durable local config file:

```text
~/.agents/config/chatgpt-review-bridge/defaults.yaml
```

Read that file after explicit per-request and session settings, and before falling back to the generic ChatGPT URL. Do not store machine-specific defaults inside the installed skill package because package updates may overwrite them.

Supported fields:

- `default_browser_mode`: `playwright`, `current-chrome-explicit`, or `manual`
- `chatgpt_default_url`
- `profile_record_name`
- `profile_path`
- `repo_path`
- `branch_scope`

Example:

```yaml
default_browser_mode: playwright
chatgpt_default_url: https://chatgpt.com/g/<project-id>/project
```

Changing defaults is a persistent bridge-default change and requires explicit instruction.

## Current Chrome Routing

After the user chooses current Chrome mode:

1. Enumerate open ChatGPT tabs.
2. Present candidate tabs and require an explicit tab selection or confirmation.
3. Claim only the confirmed tab.
4. Stop before sending the review package.

Do not save a selected tab or URL as a default unless separately requested.

## Playwright Routing

After the user chooses Playwright mode:

1. Apply browser operation rules for session enumeration and reuse before opening anything new.
2. Reuse the mapped ChatGPT project or conversation when available.
3. Resolve configured Playwright route. Ask for a profile only when profile mode is explicit or a profile record exists.
4. Open configured `chatgpt_default_url`; otherwise open generic ChatGPT.
5. Mark project membership `Not verified` unless inspected.
6. Stop before sending content.

If no browser session, tab identity, account state, upload state, or response completion signal can be verified, stop or mark the affected field `Not verified`.

## Text And File Input

Use text input for compact packages and file/pasted attachments when size or structure matters. If pasted content becomes an attachment, treat it as the single intended upload for that round, verify the composer state, and do not paste or upload again unless the first attempt is removed or clearly failed. Never upload secrets, `.env`, private registry tokens, local keychains, browser profile data, or unrelated dirty files.

## Output Capture

Capture ChatGPT output into `review.md` by direct page extraction, download, or selected response text. Screenshots are supporting evidence only.

Accept a response only when it can be tied to:

- intended and final URL
- branch/commit/diff basis
- submitted input or attachment names/counts
- completion signal or `Not verified`
- latest assistant response extraction method

Reject or mark `Not verified` if the tab is ambiguous, generation is still streaming, output is empty/truncated, or the response predates the submitted prompt.

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
