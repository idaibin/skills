# ChatGPT Routing And IO

## Contents

- [Terminology Basis](#terminology-basis)
- [Authorization Before Routing](#authorization-before-routing)
- [Routing Order](#routing-order)
- [Surface Resolution](#surface-resolution)
- [Default Configuration](#default-configuration)
- [Current Chrome Routing](#current-chrome-routing)
- [Browser Capability Routing](#browser-capability-routing)
- [Standalone Playwright Routing](#standalone-playwright-routing)
- [Text And File Input](#text-and-file-input)
- [Output Capture](#output-capture)
- [Prompt Template](#prompt-template)

## Terminology Basis

- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)
  documents Projects across free and paid plan types; use `project` for durable
  project context rather than inventing another product surface.
- [ChatGPT Enterprise workspaces](https://help.openai.com/en/articles/8265430-what-is-a-workspace-how-can-i-switch-workspaces)
  documents account environments with separate conversations and files. Verify
  and record workspace identity independently from Project identity.
- [ChatGPT desktop built-in browser](https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app), [cloud browser](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt), and [ChatGPT agent](https://help.openai.com/en/articles/11752874-chatgpt-agent/) document distinct reviewer browser surfaces. Treat their browser state and limits separately.
- [Deep research in ChatGPT](https://help.openai.com/en/articles/10500283-deep-research) documents a reviewable research plan, selectable public-web/site/app sources, and a cited report. Use it for multi-step synthesis; use Search or Standard Chat for shorter work.
- [Images in ChatGPT](https://help.openai.com/en/articles/11084440-chatgpt-images-faq) documents image creation and editing in a conversation or Images surface. Treat the generated asset, its prompt, and any edit selection as a distinct collaboration result.

## Authorization Before Routing

Do not resolve or open a browser route for requests that only say prepare,
build, draft, package, or create review material. Generate
`<repo-root>/.codex/reviews/<review-id>/review-package.md` in a verified ignored
workspace and stop. Continue below only when the user
explicitly authorizes an external send, use of ChatGPT now, or a bounded number
of external review rounds.

## Routing Order

1. Required ChatGPT capability selected from the requested outcome: Standard Chat, Search, Deep Research, Images, or reviewer browser.
2. Explicit user surface or URL and any browser mode explicitly selected in the current request.
3. Session, repository, or user `chatgpt_default_url` through the desktop built-in browser.
4. A standard chat through the desktop built-in browser at `https://chatgpt.com/` when no specialized capability is required.
5. Current Chrome or standalone Playwright only when explicitly selected in the current request and controllable.
6. Package-only when the required capability or route cannot be proven and no authorized fallback satisfies the outcome.

If generic ChatGPT is used, report that the review is not project-bound.

## Surface Resolution

- Resolve `project` for repository-bound, persistent, or multi-round review when a verified Project URL exists.
- Resolve `standard-chat` for one-off review or when no durable Project route exists.
- Resolve `search`, `deep-research`, or `images` only when the selected collaboration capability is verified on the active surface. These are capability routes, not content themes.
- Resolve `codex` only as the executor or as an explicitly requested separate-agent review. Never count self-review as an independent ChatGPT pass.
- Treat UI labels as presentation details. Route by verified capability and URL so a label change does not silently change behavior.
- Verify and record the active account workspace independently. A Project is
  available across plan types, and its URL does not establish personal or
  organization workspace membership.

## Default Configuration

Default new review records to `desktop-built-in-browser`. Legacy
`capability-auto` means built-in-first and must not silently select Current
Chrome or standalone Playwright. Availability is not proof of authorization.

Runtime defaults may come from a durable local config file:

```text
~/.agents/config/ask-chatgpt/defaults.yaml
```

Read that file after explicit per-request settings and before falling back to the generic ChatGPT URL. Surface, Project, interface, model, and reasoning defaults may be reused only after verification on the active page. A stored Current Chrome or standalone mode never replaces a current explicit request to use the user's browser. Do not store machine-specific defaults inside the installed skill package because package updates may overwrite them.

Supported fields:

- `default_browser_mode`: `capability-auto`, `desktop-built-in-browser`, `chatgpt-cloud-browser`, `current-chrome-explicit`, `standalone-playwright-explicit`, or `manual`
- `chatgpt_surface`: `standard-chat` or `project`
- `chatgpt_project_name`: expected Project display name used only as secondary identity evidence
- `chatgpt_interface`: `chat` or `work`
- `chatgpt_model`: expected model label or stable identifier
- `chatgpt_reasoning_mode`: preferred reasoning/profile label
- `chatgpt_reasoning_fallbacks`: ordered list of authorized fallback labels
- `account_workspace_note`
- `chatgpt_default_url`
- `profile_record_name`
- `profile_path`
- `repo_path`
- `branch_scope`

Example:

```yaml
default_browser_mode: desktop-built-in-browser
chatgpt_surface: project
chatgpt_project_name: <project-name>
chatgpt_interface: chat
chatgpt_model: <model-label-or-id>
chatgpt_reasoning_mode: <preferred-reasoning-label>
chatgpt_reasoning_fallbacks:
  - <authorized-fallback-label>
account_workspace_note: Not verified
chatgpt_default_url: https://chatgpt.com/g/<project-id>/project
```

Changing defaults is a persistent bridge-default change and requires explicit instruction. Project name is never sufficient identity evidence; verify the configured URL plus current rendered Project state. Model and reasoning labels are presentation-sensitive preferences, not capability claims. Match the active UI semantically (for example, localized `极高` for `xhigh`), prove the selected state before submit, and use a fallback only in the configured order when the preferred option is unavailable.

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
2. Use `ops-browser` as the low-level browser operator for session/tab selection, navigation, Chat/Work and model/reasoning selection, composer/upload inspection, submission, completion evidence, and response extraction. The bridge continues to own package scope, authorization, surface, preferences and fallback order, round count, conversation attribution, and archive paths.
3. Verify configured Project URL/rendered identity, Chat/Work interface, and model/reasoning selection before submit. Reuse the mapped ChatGPT Project conversation when available.
4. If the verified Project has no conversation and the user authorized sending, open the Project landing page and create exactly one conversation. Verify its stable URL/ID and empty composer state before submit when exposed. If the surface assigns identity only on first submit, record the pre-send Project/account evidence, make the one authorized submit, then verify and store the resulting URL/ID before accepting the response or continuing. Do not create a conversation for Package-only requests.
5. Otherwise open the configured Project URL or a standard chat through the selected capability.
6. Ask the user to sign in inside that controlled browser when authentication is required.
7. Mark Project identity and account workspace `Not verified` unless each is inspected.
8. Stop before sending unless the current authorization covers the resolved route, scope, and round count.

When ChatGPT itself will browse a target page, record that as a separate reviewer-browser route. Do not infer its cookies, account, tabs, or action permissions from the transport browser that opened the ChatGPT conversation. Load and follow `live-browser-review.md` for target and evidence contracts.

If the environment lacks the required control or evidence capability, do not load
or claim an unbundled browser helper. Return to Package-only.

## Standalone Playwright Routing

Use only when explicitly selected and verified for the authorized scope. If the desktop built-in browser is unavailable and standalone was not explicitly selected, return to Package-only instead of switching routes. Ask for a profile only when profile mode is explicit or a profile record exists. Do not install browser binaries merely because the desktop built-in route is available.

If no browser session, tab identity, account state, upload state, or response completion signal can be verified, stop or mark the affected field `Not verified`.

## Text And File Input

Use `<repo-root>/.codex/reviews/<review-id>/review-package.md` as the canonical durable outbound artifact unless the user names another path. Keep its response log and related files in the same ignored review directory. A compact review, research, architecture, UI, or image request may use inspected composer text without creating a file. Use file/pasted attachments when size, structure, source assets, or multipart integrity matters. If pasted content becomes an attachment, treat it as the single intended upload for that send action, verify the composer state, and do not paste or upload again unless the first attempt is removed or clearly failed. Never upload secrets, `.env`, private registry tokens, local keychains, browser profile data, unrelated dirty files, or unapproved source images.

For a multipart artifact set, verify the manifest counts and SHA-256 values before browser work. Send the manifest with a wait-for-final instruction, then exactly one part per message in order. Verify each attachment and acknowledgement, retry only an inspected failed part, and send `FINAL PART` plus the review prompt only after the complete set matches the manifest. Treat early reviewer analysis, a missing acknowledgement, or any count/order/hash mismatch as an incomplete round.

## Output Capture

Capture external ChatGPT text into `<repo-root>/.codex/reviews/<review-id>/review.md` by direct page extraction, download, or selected response text. Use the same review ID as the outbound package. Capture generated reports or images in that task-owned directory and record their paths plus the submitted prompt and operation attribution in `review.md`; do not put the outbound package in this file. Screenshots are supporting evidence only. Keep the raw directory local-private and ignored; if repository delivery is explicitly requested, apply the visibility policy in `usage.md` and create a separate sanitized durable copy before staging.

For live-browser review, also capture the declared target URL, reviewer browser surface, viewport when relevant, screenshot/source or observed-state evidence, actions taken, confirmation points, and `Not verified` gaps. Do not treat transport-browser screenshots of the ChatGPT UI as proof of the target page.

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

## Prompt Contract

```text
Codex role: intent owner, local evidence owner, verifier, and executor.
ChatGPT role: produce the selected independent web result only.

Outcome: <what the user actually needs>
Theme: <review|repository|product/domain|UI/design|architecture|implementation/security/delivery|open-ended>
Capability: <standard-chat|search|deep-research|images|reviewer-browser>
Authoritative inputs: <facts, files, URLs, fixed revisions, or source assets>
Must answer or produce: <small decisive set>
Evidence/asset rules: <citations, primary sources, use/ignore, rights, dimensions, or path references>
Exclusions and forbidden actions: <scope and mutation limits>
Return contract: <findings, cited report, critique, prompt, image, or observed evidence>
Stop condition: <when the independently required result is complete>
```
