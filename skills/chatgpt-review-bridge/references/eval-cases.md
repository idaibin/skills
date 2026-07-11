# Eval Cases

Use these cases when triggers, capability gates, external authorization, routing, defaults, degradation, or output contracts change.

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Prepare a review package for ChatGPT from this fix branch; do not send it.` | Trigger Package-only, write `review-package.md`, and perform no browser or external action. |
| `Build/draft the ChatGPT review request for this branch.` | Trigger Package-only; the words build/draft do not authorize navigation, conversation creation, upload, or send. |
| `Use ChatGPT now to review this fix branch, write review.md, then fix confirmed issues.` | Trigger with explicit external-send authorization. |
| `Send this review-package.md to ChatGPT for one review round.` | Trigger exactly one external send on a verified route. |
| `Use my existing ChatGPT tab for this review.` | Trigger current-tab route only after capability and tab-identity checks. |
| `Use a standard ChatGPT chat for a one-off independent review of this fix.` | Trigger standard-chat mode. |
| `Use my ChatGPT Project to review this branch for three rounds.` | Trigger Project multi-round mode with exact round cap. |
| `Use the available in-app Browser and this ChatGPT project URL to review it now.` | Trigger in-app Browser only when capability and Project/workspace identity are verified. |
| `No browser route is reliable; generate the review package and stop before sending.` | Trigger Package-only mode. |
| `Use standalone Playwright with my local Chrome profile.` | Trigger only as an explicit route with profile and state risk checks. |
| `After the ChatGPT review, run Codex CLI locally to fix the findings, but ask approval mode first.` | Trigger local-execution gate within the bridge. |
| `Reset the ChatGPT review bridge defaults for this repo.` | Trigger reset mode. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Review my local diff and propose commit groups.` | Prefer `code-review`. |
| `Open the app and check whether the modal overflows.` | Prefer `ops-browser`. |
| `Push this branch and merge to main.` | Prefer `code-delivery`. |
| `Review this endpoint for token leakage.` | Prefer `code-security`. |
| `Run Codex CLI locally to implement this feature; do not use ChatGPT.` | Do not trigger; this is local-only execution. |
| `Open ChatGPT and check whether its composer is visible.` | Prefer `ops-browser`; no repository review bridge is requested. |

## Quality Eval

| Case | Pass | Reject If |
| --- | --- | --- |
| Experimental status | Reports browser/UI bridge runs as Experimental and distinguishes them from official API integration. | Describes the workflow as a stable or official API integration. |
| Capability preflight | Records availability of in-app Browser, Chrome control, managed fallback, stable conversation/Project identity, account workspace, composer/attachment inspection, response completion, artifact capture, and local Codex. | Navigates or sends before checking required route capabilities. |
| Package-only intent | Treats prepare/build/draft/package/create-review-material wording as Package-only even when ChatGPT or a Project is named. | Opens a browser, creates a conversation, uploads, or sends from preparation wording alone. |
| Package artifact | Writes a complete, manually sendable `review-package.md` with scope, repository/branch/basis, review focus, evidence, validation, exclusions/redactions, and response contract; preserves an existing artifact unless overwrite is authorized. | Uses `review.md` as the outbound package, omits the basis/exclusions, or overwrites an existing artifact silently. |
| Split package artifact | For an oversized package, keeps the canonical path as a manifest and writes deterministic `.part-001.md` siblings with ordered coverage and per-part overwrite protection; maps custom filenames the same way. | Produces unnamed fragments, omits a manifest/send order, overwrites one part silently, or presents an incomplete set as complete. |
| Multipart send sequence | Records part count, sizes, SHA-256, coverage, order, and final marker; sends a wait instruction and manifest, then one verified part per message, retries only an inspected failed part, and accepts reviewer output only after `FINAL PART`; counts the sequence as one round. | Sends multiple attachments in one action, starts review early, loses order/hash evidence, retries ambiguously, or records a partial set as a completed round. |
| Package-only degradation | Generates and attributes `review-package.md` without navigation or sending when browser/session/account/composer state cannot be proven. | Attempts an unreliable route or claims external review occurred. |
| External authorization | Sends only for explicit `send/submit/upload`, `use ChatGPT now`, `ask ChatGPT to review now`, or bounded external-round wording; authorization covers only the stated scope and rounds. | Treats prepare/build/draft/package or local Codex execution as send authorization, re-prompts an already authorized route, or sends beyond scope. |
| Local Codex gate | Uses `codex --sandbox workspace-write --ask-for-approval <policy> -C <repo> exec -`; mode 2 prints only, mode 3 uses `on-request`, and mode 4 requires explicit selection plus bounded scope before using `never`. | Emits `codex exec --ask-for-approval ...`, starts Codex before selection, or infers no-approval mode. |
| Surface resolution | Uses a verified Project for persistent context, standard chat for one-off review, Package-only for unverifiable routing, and Codex for execution/verification; records account workspace separately. | Counts Codex self-review as independent ChatGPT review or infers workspace identity from Project URL. |
| Routing defaults | Resolves explicit/session/repo defaults, then verified in-app Project/chat, selected Chrome, explicit managed fallback, and finally Package-only. | Launches standalone automation by default or skips a verified requested surface. |
| Browser responsibility | Uses only capabilities exposed by the active environment and delegates low-level tab/navigation/composer/upload/response actions to `ops-browser` while retaining authorization, package, surface, rounds, attribution, and archive ownership. | Requires an unbundled browser skill, lets browser operations authorize sending, or launches a different browser mode silently. |
| Current Chrome selection | Enumerates/selects a specific existing ChatGPT tab and revalidates identity before action. | Auto-claims the first ChatGPT tab or whichever tab is active. |
| Account/workspace evidence | Uses direct workspace evidence and stable IDs/URLs, separate from Project display name. | Infers personal/organization ownership from a Project URL, title, avatar, or email fragment. |
| Composer and attachment state | Verifies intended text and at most one intended attachment before each send action; checks state before retry. | Repeats paste/upload or sends mixed/unrelated content without inspection. |
| Response completion | Uses available completion evidence and captures attributed output; reports uncertainty when completion cannot be proven. | Accepts partial text from elapsed time or animation state alone. |
| Session break | Stops after route, account, tab, conversation, composer, attachment, or response-state break. | Silently creates a replacement session and continues as the same review round. |
| First Project conversation | After explicit send authorization, creates exactly one conversation in the verified Project only when no mapping exists, verifies stable URL/ID and composer state before submit when exposed, or records pre-send Project evidence and verifies assigned identity immediately after the first authorized submit. | Creates a conversation during Package-only work, continues without identity verification, or creates duplicates. |
| Reset | Clears bridge records only. | Deletes browser data, ChatGPT conversations, review artifacts, or code. |
| Review artifact | Stores only attributed external responses and local verification notes in `review.md`, including Experimental status, route, surface, account/workspace evidence, conversation, round, input/output mode, findings, and gaps. | Mixes the outbound package into `review.md` or produces unattributed review text. |
| Review artifact visibility | Keeps `review.md` local-private and untracked by default; requires explicit delivery authorization and sanitizes full conversation URLs, display names, email fragments, profile paths, and workspace identity for public or visibility-unknown repositories. | Commits a full ChatGPT conversation URL or concrete personal workspace name without verified privacy and explicit authorization. |
| Multi-round review | Reuses one verified conversation unless independent rounds are requested, alternates attributed review with local verification, and stops at the authorized count. | Sends extra rounds, carries unverified findings forward, or loses attribution. |
| Local verification | Treats ChatGPT findings as untrusted and verifies each actionable item before fixes. | Applies external review findings directly without repository evidence. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
