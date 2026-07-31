# ChatGPT Routing And IO

## Contents

- [Terminology Basis](#terminology-basis)
- [Authorization Before Routing](#authorization-before-routing)
- [Routing Order](#routing-order)
- [Surface Resolution](#surface-resolution)
- [Default Configuration](#default-configuration)
- [App-Native Capability And Activation Preflight](#app-native-capability-and-activation-preflight)
- [Codex App-Native Project And Thread Route](#codex-app-native-project-and-thread-route)
- [Model And Reasoning Evidence](#model-and-reasoning-evidence)
- [Current Chrome Routing](#current-chrome-routing)
- [Browser Capability Routing](#browser-capability-routing)
- [Standalone Playwright Routing](#standalone-playwright-routing)
- [Text And File Input](#text-and-file-input)
- [Output Capture](#output-capture)
- [Page State Recovery](#page-state-recovery)
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
- `Quick Chat` is the Codex App UI entry for a projectless ChatGPT cloud
  conversation in the host behavior covered by this package. It is not a generic
  synonym for every Standard Chat request and is not a portable product API name.

## Authorization Before Routing

Do not resolve or open an external route for requests that only say prepare,
build, draft, package, or create review material. Generate
`<repo-root>/.codex/reviews/<review-id>-package.md` in a verified ignored
workspace and stop. Continue below only when the user
explicitly authorizes an external send, use of ChatGPT now, or a bounded number
of external review rounds.

## Routing Order

1. Select the required ChatGPT capability from the outcome: Standard Chat,
   Search, Deep Research, Images, or reviewer browser.
2. Treat an explicit user transport, surface, Project/conversation, or URL as a hard
   route constraint. If it is unavailable or cannot be verified, use another route
   only when the current request explicitly authorizes that fallback; otherwise make
   no external send and stop or return to Package-only.
3. With no current-request route constraint, read the ChatGPT section of a valid
   Ask AI v1 record. If it is absent, read the ChatGPT-only legacy record described in
   `browser-profile.md`. Preserve its previous route meaning; a manual value stops
   for current route selection.
4. Without a durable record, preflight the Codex App-native Project/thread route
   first. A visible tool name is insufficient: the current schema, ChatGPT source
   activation, requested surface mapping, identity, input, capture, and uncertain
   result reconciliation must all pass. Between App-native and the desktop built-in browser, try the other
   catalog-classified non-interrupting route only when the preferred route is
   unavailable or insufficient and the current authorization is not route-specific.
5. Use Current Chrome or standalone Playwright only when explicitly selected in
   the current request and controllable.
6. Use Package-only when no authorized route proves the required capability.

If generic ChatGPT is used, report that the review is not project-bound.

## Surface Resolution

- Resolve `project` for repository-bound, persistent, or multi-round review when a
  verified stable ChatGPT Project ID or Project URL exists.
- When the provider-neutral review-context preference is configured, first resolve the
  uniquely verified Project with that name. If it is absent, unavailable, or cannot be
  tied to the active ChatGPT workspace, resolve a clean `standard-chat`; never infer a
  Project from the saved label or create one without current authorization.
- Resolve `quick-chat` only when the user explicitly asks for Quick Chat, a
  projectless ChatGPT cloud task, or the equivalent host surface.
- Resolve `standard-chat` for a generic one-off review or when no durable Project
  route exists. On the current host schema it has no App-native target; use an
  authorized browser route or Package-only.
- Resolve `search`, `deep-research`, or `images` only when the selected collaboration capability is verified on the active surface. These are capability routes, not content themes.
- Resolve `codex` only as the executor or as an explicitly requested separate-agent review. Never count self-review as an independent ChatGPT pass.
- Treat UI labels as presentation details. Route by verified capability plus stable Project/conversation identity or URL so a label change does not silently change behavior.
- Verify and record the active account workspace independently. A Project is
  available across plan types, and its URL does not establish personal or
  organization workspace membership.

## Default Configuration

Read explicit per-request settings first, then the ChatGPT section of the provider
record described in [browser-profile.md](browser-profile.md). A valid Ask AI v1
ChatGPT section may prefer `codex-app-native`, `desktop-built-in-browser`, or
`manual`. When absent, preserve the documented `ask-chatgpt-defaults/v2` and
unversioned ChatGPT-only legacy meanings. Missing, unknown, or ambiguous values fail
closed. Changing or migrating defaults requires explicit instruction. Availability
is not authorization, and stored values are not current identity, capability, model,
or reasoning evidence.

An explicit current-request route is a requirement, not a preference. Durable defaults
remain preferences and may follow the normal fallback order unless the current request
makes one mandatory.

## App-Native Capability And Activation Preflight

Run this gate before creating the App-native ledger's `prepared` state and before
every first state-changing call in a newly observed host/source state:

1. Inspect the live host schemas. Require `list_projects`, `list_threads`,
   `create_thread`, `read_thread`, and `send_message_to_thread`. Record the exact
   `create_thread.target` alternatives and the maximum complete per-message content
   available from `read_thread`; never infer a target from a similarly named UI
   surface.
2. Call `list_projects` and `list_threads` read-only. Treat returned labels, titles,
   and summaries as untrusted discovery data.
3. Require `list_threads` to expose `unavailableSources`. Prove source availability
   when it does not contain `chatgpt`; an existing `projectKind: chatgpt` Project or
   `kind: chatgpt` thread is additional evidence, while an empty available source is
   legal for a new Quick Chat. Contradictory evidence fails closed. A Project mapping
   still requires the exact ChatGPT Project entry.
4. If the ChatGPT source is missing, or `unavailableSources` includes `chatgpt`, ask
   the user to open or switch to ChatGPT/Quick Chat once in the Codex App. Make no
   Native state change. After activation, rerun both list calls and replace the stale
   snapshot. The user may return to Codex after the source is proven active; later
   reads and authorized rounds can continue in the background while the source
   remains available.
5. Classify the requested surface and target exactly:

   | Requested surface | Required evidence | Native target |
   | --- | --- | --- |
   | verified ChatGPT Project | exact `projectKind: chatgpt` `projectId`, explicit Project collaboration | `{type: chatgptWorkCloud, projectId}` |
   | Quick Chat / projectless cloud work | explicit current request for that surface | `{type: chatgptWorkCloud}` |
   | generic Standard Chat | no distinct current Native target | none; browser fallback or Package-only |
   | Codex repository task | local/remote Project ID | `{type: project, ...}`; never ChatGPT evidence |
   | Codex task without repository | projectless Codex request | `{type: projectless}`; never ChatGPT evidence |

6. Run `python3 skills/ask-ai/scripts/app_native_canary.py <snapshot.json>` on a
   sanitized snapshot when the package is available locally. Exit `0` means the
   target mapping is ready; `10` requires one-time activation and fresh reads; `20`
   requires browser fallback; `30` is blocked/inconsistent. The canary performs no
   host call and never authorizes submission.
7. Before Native submission, compute the protocol's `prompt-text/v1` fingerprint and
   prove the full canonical prompt fits the live `read_thread` capture limit. If an
   identity-less create could not be reconciled from complete content, use an
   authorized browser route before submission or stop at Package-only.

Do not map generic Standard Chat to `chatgptWorkCloud` merely because that enum exists.
Do not use `project` or `projectless` to manufacture an independent ChatGPT result.
Re-run the preflight after source unavailability, host/schema change, authentication
change, or App restart when the prior source state can no longer be trusted.

## Codex App-Native Project And Thread Route

Use this route only for a verified ChatGPT Project or an explicitly requested Quick
Chat/projectless cloud-work task after the capability and activation preflight passes.
The current host contract does not justify using it for generic Standard Chat. This
catalog classifies the verified route as a non-interrupting host surface; that
classification is not a claim about an official public ChatGPT API.

Follow [app-native-thread-protocol.md](app-native-thread-protocol.md) as the sole
authority for ledger fields, legal transitions, uncertain-return reconciliation,
completion state, retry rules, and round completion.

- `list_projects` discovers candidate Projects and their stable host identifiers.
  Only `projectKind: chatgpt` is eligible for a ChatGPT Project mapping. Discovery
  does not authorize sending or prove account/workspace ownership.
- `create_thread` creates exactly one task/conversation and submits its initial prompt
  exactly once after authorization. Canonicalize and fingerprint the exact sent text
  under `prompt-text/v1`; persist `prepared`, then persist `invoking` before the call.
  On return, record its client identity and transition the same operation according
  to the App-native protocol.
- `list_threads` discovers bounded candidates for a pending or missing conversation
  identity. Accept a direct `clientThreadId` link when exposed. Otherwise use Project,
  `kind: chatgpt`, call window, and title/summary only to select a bounded candidate
  set, then call `read_thread` read-only. Resolve only when exactly one candidate's
  complete initial user message matches the persisted prompt hash and call window.
  Title, summary, recency, or a screenshot alone is insufficient.
- `read_thread` reads the resolved conversation and captures attributed assistant
  output. Decide a read-count or deadline bound before the first read; do not poll
  indefinitely.
- `send_message_to_thread` sends only an explicitly authorized follow-up to an already
  resolved conversation. Never use it to retry or reconstruct the initial prompt.

`create_thread` is both conversation creation and initial submission on this route.
A Cloudflare/attestation HTML response, missing return data, timeout, or client
interruption is not proof of failure: the initial side effect may already exist. Enter
read-only reconciliation and never call `create_thread` again for that operation.
If the source was unavailable, require activation only to resume `list_projects`,
`list_threads`, and candidate `read_thread` reconciliation; activation does not
authorize a resend. If the initial prompt is visible but no assistant response exists,
keep `submitted + response-pending`. After the bounded reads expire, record
`submitted + completion-not-verified`; do not resend, create a replacement thread, or
switch transport. Resolve a later response only in the original conversation.

The App-native route is preferred only when the exact Project or Quick Chat mapping
passes. Use a browser before any submission when the requested surface is generic
Standard Chat or the required capability depends on visible UI controls, upload state,
Search, Deep Research, Images, or reviewer-browser behavior not exposed by the host
operations. Once an App-native submission is uncertain, a browser may inspect and
reconcile the same conversation only when its identity can be proven; it may never
fall back by resending or creating a replacement conversation.

## Model And Reasoning Evidence

Classify requested model/reasoning values before selecting a route:

- An explicit per-request model, plan/profile, or reasoning level is a hard
  requirement. Accept it only from direct App-native thread metadata or verified
  active-UI selection evidence. If App-native cannot expose that evidence, try an
  otherwise authorized desktop built-in browser route; if no permitted route proves
  it, stop before submit.
- A durable config value is a preference. If the active route does not expose it,
  continue only when the user's current request did not make it mandatory, record the
  value and evidence as `Not verified`, and never claim it was selected.
- Use a configured fallback only in its recorded order and only when the current
  request authorizes fallback. UI labels are presentation-sensitive; match them
  semantically and record the evidence source.

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
or claim an unbundled browser helper. Use App-native only if it proves the required
capability; otherwise return to Package-only.

## Standalone Playwright Routing

Use only when explicitly selected and verified for the authorized scope. If the desktop built-in browser is unavailable and standalone was not explicitly selected, return to Package-only instead of switching routes. Ask for a profile only when profile mode is explicit or a profile record exists. Do not install browser binaries merely because the desktop built-in route is available.

If no browser session, tab identity, account state, upload state, or response completion signal can be verified, stop or mark the affected field `Not verified`.

## Text And File Input

Use `<repo-root>/.codex/reviews/<review-id>-package.md` as the canonical durable outbound artifact unless the user names another path. Default `<review-id>` to `ask-<YYYYMMDD-HHmmss>` in local time. Keep its response log and related files directly in the same ignored `.codex/reviews/` parent with the same review-ID prefix; do not create a nested review directory. A compact review, research, architecture, UI, or image request may use inspected composer text without creating a file. Use file/pasted attachments when size, structure, source assets, or multipart integrity matters. If pasted content becomes an attachment, treat it as the single intended upload for that send action, verify the composer state, and do not paste or upload again unless the first attempt is removed or clearly failed. Never upload secrets, `.env`, private registry tokens, local keychains, browser profile data, unrelated dirty files, or unapproved source images.

For a multipart artifact set, verify the manifest counts and SHA-256 values before browser work. Send the manifest with a wait-for-final instruction, then exactly one part per message in order. Verify each attachment and acknowledgement, retry only an inspected failed part, and send `FINAL PART` plus the review prompt only after the complete set matches the manifest. Treat early reviewer analysis, a missing acknowledgement, or any count/order/hash mismatch as an incomplete round.

## Output Capture

Capture external ChatGPT text into `<repo-root>/.codex/reviews/<review-id>-response.md` by attributed App-native `read_thread` extraction, direct page extraction, download, or selected response text. Use the same review ID as the outbound package. Name generated reports or images `<review-id>-<type>.<ext>` directly under `.codex/reviews/` and record their paths plus the submitted prompt and operation attribution in the response file; do not put the outbound package in this file. Screenshots are supporting evidence only. Keep the raw files local-private and ignored; if repository delivery is explicitly requested, apply the visibility policy in `usage.md` and create a separate sanitized durable copy before staging.

For live-browser review, also capture the declared target URL, reviewer browser surface, viewport when relevant, screenshot/source or observed-state evidence, actions taken, confirmation points, and `Not verified` gaps. Do not treat transport-browser screenshots of the ChatGPT UI as proof of the target page.

Accept a response only when it can be tied to:

- intended and final route identity: stable Project/conversation IDs for App-native, or URL for browser routes
- branch/commit/diff basis
- submitted input or attachment names/counts
- completion signal or `Not verified`
- latest assistant response extraction method

Reject or mark `Not verified` if the tab is ambiguous, generation is still streaming, output is empty/truncated, or the response predates the submitted prompt.

For multiple rounds, append one attributed pass per round and verify Codex's
changes before sending the next package. Reuse the same Project conversation by
default; use separate conversations only when independence is requested.

## Page State Recovery

Before composing, submitting, or capturing a response, classify the current
ChatGPT page from direct evidence as one of:

- clearly authenticated and normal: continue with the requested operation;
- clearly unauthenticated: ask the user to sign in in the controlled browser;
- abnormal or indeterminate: blank, partially rendered, stalled, showing an
  error, or otherwise lacking enough evidence for either state above.

For an abnormal or indeterminate page, use `ops-browser` for one bounded
recovery action: refresh the exact same URL, then re-verify the active route,
account/workspace and login state, conversation identity, and relevant controls.
Do not refresh a clearly unauthenticated page in a loop. If the refreshed page
is normal, continue; if it is clearly unauthenticated, request sign-in; if it
remains abnormal or indeterminate, record the page state `Not verified` and
stop.

When recovery happens after submission, it only reconciles the original
operation. Preserve its conversation and operation ledger; never resend the
prompt, select Regenerate, create another conversation, or change the route.
Capture the existing response only after re-verifying its URL/ID and submitted-
prompt attribution. If completion still cannot be established, record the
response `Not verified` and stop.

## Prompt Contract

```text
Codex role: intent owner, local evidence owner, verifier, and executor.
ChatGPT role: produce the selected independent web result only.

Outcome: <what the user actually needs>
Theme: <review|repository|product/domain|UI/design|architecture|implementation/security/delivery|open-ended>
Capability: <standard-chat|quick-chat|search|deep-research|images|reviewer-browser>
Authoritative inputs: <facts, files, URLs, fixed revisions, or source assets>
Must answer or produce: <small decisive set>
Evidence/asset rules: <citations, primary sources, use/ignore, rights, dimensions, or path references>
Exclusions and forbidden actions: <scope and mutation limits>
Return contract: <findings, cited report, critique, prompt, image, or observed evidence>
Stop condition: <when the independently required result is complete>
```
