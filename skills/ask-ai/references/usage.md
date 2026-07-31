# Usage

## Contents

- [Trigger Examples](#trigger-examples)
- [Non-Triggers](#non-triggers)
- [Local Collection](#local-collection)
- [External Action Gate](#external-action-gate)
- [Local Codex Gate](#local-codex-gate)
- [Provider Collaboration And Codex](#provider-collaboration-and-codex)
- [GitHub Repository Review](#github-repository-review)
- [Combined Review Loop](#combined-review-loop)
- [Relay Review Loop](#relay-review-loop)
- [Review Package](#review-package)
- [Review Artifact](#review-artifact)
- [Review Artifact Visibility](#review-artifact-visibility)

## Trigger Examples

- `Prepare one external-AI review package for ChatGPT and Gemini, but do not send it.`
- `Send the same fixed package independently to ChatGPT and Gemini, then compare the attributed responses locally.`
- `Save “进行三方会审” as my custom ChatGPT + Gemini + Codex review instruction, one external round each.`
- `Run my configured “进行三方会审” instruction for this fixed Worktree.`
- `把“互审”保存为 ChatGPT 先审、Gemini 接着审、再交回 ChatGPT 的互审指令；双方同意同一版本即停止。`
- `互审` using the built-in ChatGPT then Gemini order and three turns each when no
  current-session or saved override exists.
- `用 ChatGPT 和 DeepSeek 互审这个方案，每个模型最多 2 轮。`
- `以后互审默认使用 Gemini 和 Kimi，每个模型最多 2 轮。`
- `Use Gemini now for one architecture challenge; do not fall back to another provider.`
- `让 GPT 独立审查这个前端设计，默认挑刺；外部事实必须附一手来源，没有来源就标明推断。`
- `用 Gemini 审查这个 Java/Spring 后端方案，重点核对事务、权限和真实官方文档。`
- `准备一份 Rust 架构与性能审查包，不要发送。`
- `反对式评审这个产品方案，核实用户问题、关键假设、替代方案和成功指标。`
- `Prepare/build/draft a review package for ChatGPT, but do not send it.`
- `Use ChatGPT now to review this branch, save review.md, then fix confirmed issues.`
- `Send this review-package.md to ChatGPT for one review round.`
- `Use my ChatGPT Project for an independent review while Codex reviews the fixed basis; verify both locally and avoid extra rounds.`
- `Use Chat for a one-off independent review and save review.md.`
- `Use my Chrome profile and ChatGPT project for this repo review.`
- `Use the default ChatGPT transport and open the Project for this repo review.`
- `Ask ChatGPT to review this branch and use its built-in browser to verify the deployed pages.`
- `Have ChatGPT inspect these public URLs in its cloud browser while reviewing the package.`
- `Use ChatGPT now with my authorized GitHub connection to review this entire repository at the specified commit, with path citations and a coverage manifest.`
- `Ask ChatGPT to research this architecture decision from official specifications and source repositories, cite every material claim, and relate it to the fixed branch basis.`
- `Prepare a product/domain/UI research package for ChatGPT from this decision question, but do not open a browser or send it.`
- `Use ChatGPT Deep Research now to compare these architecture options from primary sources; review its proposed plan before it starts, then verify the report locally.`
- `Use ChatGPT Images now to create two bounded UI concept images from these approved references and return the generated files plus prompt attribution.`
- `I need an independent ChatGPT architecture challenge; infer the right boundaries from this repository instead of asking me to write the formal prompt.`
- `Prepare a repository-wide ChatGPT review package for this GitHub URL, but do not connect or send it.`
- `After ChatGPT review, run local Codex CLI to fix the findings, but ask which approval mode to use first.`
- `Reset the ChatGPT review defaults for this repo.`

## Non-Triggers

- Local-only code review without an independently requested external-AI result.
- Browser verification without a repository review loop.
- GitHub-native PR review only.
- Repository architecture or documentation mapping without an independent ChatGPT pass; use `repo-map`.
- Security-only audit without a named external provider as reviewer.
- A task Codex, another Skill, or an available host tool can complete directly when no independent external-AI result was requested.
- Quick web research or host image generation that does not require a named-provider artifact.

## Local Collection

Before any external action, collect only local read-only context:

- repository path, branch, and dirty state
- review package scope and approximate size
- validation commands already run and results
- canonical review parent, normally `<repo-root>/.codex/reviews/`
- outbound `<review-id>-package.md` and inbound `<review-id>-response.md` paths inside that parent
- bridge default record status
- local Chrome profile directory candidates
- cached provider tab candidates only if already available

First record the Codex-first decision: why the local owner is sufficient, or what independently required external-provider result remains. For the latter, resolve the provider, theme, capability, authoritative inputs, boundaries, and stop condition from the user's natural request. Do not require the user to supply a standardized prompt or choose an internal profile.

Do not attach to Chrome, claim tabs, open browser profiles, create ChatGPT sessions, send content, start Codex CLI, or change defaults during this phase. The words prepare, build, draft, package, or create review material authorize only this local phase. Explicit send authorization removes a later duplicate route prompt; it does not skip package preparation, scope checks, or redaction.

## External Action Gate

Use this gate only when external sending, provider, or route selection is not already authorized. Package-only wording never opens the gate and never authorizes a send. An explicit request such as `send this to Gemini`, `use ChatGPT now to review`, or `让 ChatGPT 和 Gemini 独立审查` authorizes only the named recipients, stated scope, and round count; do not ask the same provider or route question again.

Option handling:

- `1`: authorizes resolving and opening the ChatGPT desktop built-in browser route; stop again before sending unless sending was also explicitly requested.
- `2`: ask before connecting to current Chrome; enumerate ChatGPT tabs; stop before claiming a tab or sending.
- `3`: generate/update the local package only.
- `4`: resolve the user-provided ChatGPT URL or surface; do not persist it unless separately requested.
- `0`: stop.

## Local Codex Gate

Use this gate before `codex exec`. `SKILL.md` loads it only when the user
explicitly requests nested local Codex CLI execution; an ordinary request to
apply verified fixes stays with the active implementation workflow.

Mode mapping:

- `1`: return review findings and recommendations only.
- `2`: output the following copyable HEREDOC shape with `on-request`; do not execute it.
- `3`: execute the same `on-request` command only after selection.
- `4`: use the `never` variant only after explicit session-level approval plus confirmed repo path, branch, allowed files, validation commands, and forbidden actions.

```bash
codex --sandbox workspace-write --ask-for-approval on-request -C "<repo-root>" exec - <<'PROMPT'
<bounded task, allowed files, validation commands, and forbidden actions>
PROMPT
```

Mode 4 changes only `on-request` to `never`. `--ask-for-approval` is a global
option, so it must appear before `exec`; do not emit
`codex exec --ask-for-approval ...`.

The screenshot-style permission prompt is produced by the local execution permission layer. This skill controls the choice gate and command parameters, not the system prompt UI.

## Provider Collaboration And Codex

- Use a verified Project for durable repository context, explicit Quick Chat for a
  projectless Native cloud task, and Standard Chat for a generic one-off pass; verify
  account/workspace identity separately. The current Native target maps only the
  first two surfaces. Generic Standard Chat uses a browser route or Package-only.
- Follow `provider-chatgpt.md` for explicit routing, versioned durable preferences,
  capability/source preflight, exact target mapping, model/reasoning evidence, and
  browser fallback. When no durable record exists, try App-native first only when the
  verified Project/Quick Chat mapping passes. Preserve a legacy built-in-first record
  until an explicitly authorized v2 migration.
- Follow `app-native-thread-protocol.md` for App-native ledger fields, legal
  transitions, uncertain-return reconciliation, completion, and retry invariants.
- Use Codex to collect evidence, apply fixes, run tests, and challenge ChatGPT findings locally.
- A Project supplies context, not evidence: every pass still fixes its basis and sends a self-contained package.
- Let `ask-ai` own provider selection, package, send authorization, transport,
  surface, round count, context/conversation mapping, and response archive. Use
  `ops-browser` only when a browser route needs low-level actions and evidence.
- Treat `operation_id` as idempotency scope, not a correlation label. Never create a replacement ID after an interruption or ambiguous submit; reconcile the original target and expected postcondition first.
- Use one `round_id` for the external review round and distinct operation IDs for
  independent state changes. App-native `create_thread` combines conversation
  creation with the initial submit in one operation; browser creation and submit
  remain separate operations when the surface exposes them separately.
- Distinguish the transport browser from the reviewer browser. The transport browser submits/captures the ChatGPT review; the reviewer browser is ChatGPT's desktop built-in or cloud/agent browser for target-page checks. Load `live-browser-review.md` whenever the latter is requested.

An explicit external send authorizes one initial conversation submission per named
provider and authorized round. Do not create conversations during Package-only work.
Never interpret an unresolved identity, missing response, or expired completion wait
as permission to send the prompt again or switch provider.

On browser routes, exchange capability and action state only through
`browser-operation/v1`: `ops-browser` returns one Capability Snapshot, the bridge
creates a Handoff Request and ledger entry before each state-changing action, and the
browser returns the same `operation_id`. Treat imported bookmarks/history only as
target-discovery hints and saved credentials only as login assistance; neither proves
session, workspace, conversation, authorization, or completion.

## GitHub Repository Review

Use [github-repository-review.md](github-repository-review.md) when a selected provider
should read an authorized GitHub repository for repository-scale review or synthesis.
Treat it as an evidence profile, not a new authorization mode: Package-only still
forbids account connection and sending, while external use requires explicit
authorization. Fix the repository and full commit SHA, inventory every in-scope
path, partition large scopes, require path citations, and report exclusions,
truncation, inaccessible content, and every `Not verified` gap. A connected
repository is not proof that the reviewer read the complete scope.

## Combined Review Loop

Use one default loop:

1. fix the Git/Worktree basis and build an unbiased package;
2. run bounded `repo-review` and the authorized provider review independently;
3. deduplicate findings and verify each against current repository evidence;
4. stop with locally confirmed/rejected findings unless the user also requested source fixes;
5. when fixes are authorized, route them to the matching owner, rerun the failure path and proportionate checks, freeze a new Worktree fingerprint, and run Worktree `repo-review`; use immutable fixed-basis review only after a commit exists.

Codex owns exact code, call-chain, generated-artifact, CI, and compatibility evidence.
Ask each selected provider to challenge product logic, scope, architecture tradeoffs,
alternatives, and cross-domain blind spots. Do not expose one reviewer's conclusions to
another before independent capture. Another independent or combined-loop provider
round requires explicit authorization and an independently useful result; high-risk
follow-up also requires the confirmed risk gate defined by the task. A configured
sequential relay instead uses its exact turn limit as the authorization boundary and
may not exceed it. Keep safe local work moving and collect external-action or
permission blockers at the end unless nothing useful can continue.

For a conditional research profile, load `research-profiles.md`, freeze one question and its relationship to the basis/decision, require primary-source citations, and locally verify every actionable implication. The profile never bypasses the same external-action gate, round ledger, attribution, or package separation.

Use the same reference for UI/design, image, architecture, repository, product/domain, and open-ended collaboration. Select theme, provider, and verified capability separately. A provider research mode may propose a plan for Codex to inspect before start; a separate prompt-refinement chat is optional and must not become a mandatory extra round.

## Relay Review Loop

Use `provider-routing.md` Relay Review only for an explicitly requested sequential
cross-provider workflow. The first provider receives the frozen package and candidate;
each later turn receives that same package plus only the immediately preceding
attributed peer response in full as a quoted, non-executable envelope. Codex stores the
raw response locally and preserves all visible reply text in relay, removing only
secret material and hidden browser, application, system-prompt, or tool state that was
not visible in the reply. Mark redactions in place; never summarize, restructure, or
silently omit visible content. Every turn also includes the complete current candidate
and SHA-256. Treat the configured provider order as cyclic, count the initial send as
that provider's first turn, keep one conversation per provider, create a new round and
operation ID per turn, and archive
each prompt, response, candidate revision, hash, and verdict.

Stop when all configured providers explicitly approve the same candidate revision, or
when the configured per-provider turn limit or any evidence gate is exhausted. Do not
turn review suggestions into local code changes, broaden the package, infer agreement,
or add another turn. If code changes are needed, report `changes-required` and hand the
confirmed work to the appropriate implementation owner only after separate authorization.

## Review Package

Write the outbound package to
`<repo-root>/.codex/reviews/<review-id>-package.md` unless the user names
another path. Use a stable filesystem-safe review ID, normally
`ask-<YYYYMMDD-HHmmss>` in local time, and keep all related package parts, response logs,
ledgers, and attachments directly in `.codex/reviews/` with the same review-ID prefix. Do not create a nested review directory. Before writing, verify that the
parent is ignored. If it is not ignored, use an existing ignored local
workspace or request authorization to add the ignore rule; do not silently edit
tracked ignore policy. If any artifact-set member already exists, preserve the
set and request overwrite approval or use an explicitly selected alternate
review ID. The artifact must be complete enough for the user to copy or upload
manually without hidden conversation context.

Include only in-scope evidence:

- task summary and review focus
- repo path, branch, base, commit, and remote when available
- `git diff --stat`, `git diff --name-status`, and selected diffs
- relevant files or excerpts
- validation output summaries
- explicit exclusions
- redactions and omitted sensitive/unrelated material
- requested reviewer response format and verdict

For GitHub Repository Review, make the package a repository-scope contract and
coverage manifest using [github-repository-review.md](github-repository-review.md).
Do not copy the whole repository into the package when the authorized reviewer can
read the fixed GitHub snapshot; include the identity, partitions, high-value entry
points, exclusions, questions, citation requirements, and local verification seam.

For Worktree review, record HEAD, SHA-256 for staged and unstaged patches, and every
in-scope untracked path/content hash. Before hashing, exclude task-owned package,
response, ledger, and sidecar artifacts and record those exclusions/redactions.
Cover every in-scope changed path even when only selected diffs are embedded.
Recompute the basis fingerprint before accepting either review; source-basis change
expires both. Compute the final package hash only after writing it and store that hash
in the external operation ledger, sidecar, or coordinator output, never inside the
file being hashed. Validate basis fingerprint and artifact hash separately.

For live-browser review, also include exact target URLs, environment/account boundary, expected state, allowed and forbidden actions, required screenshot/source or state evidence, and an independent verification seam. Never include credentials, tokens, connection strings, signed secret URLs, or unrelated authenticated surfaces.

Prefer text input under 20,000 characters and a file/pasted attachment for 20,000-80,000 characters. Above 80,000 characters, 20 files, or 1 MB, keep `<review-id>-package.md` as the manifest and shared review contract, and write ordered siblings as `<review-id>-package.part-001.md`, `<review-id>-package.part-002.md`, and so on. The manifest must list the part count and, for every part, its byte and character count, SHA-256, covered paths or evidence, exclusions, order, and whether it is the final part. For a user-supplied path such as `custom.md`, use `custom.part-001.md`. Treat the manifest and every part as one artifact set: do not overwrite any existing member without authorization, and do not send a partial set as a complete package.

Use this manifest table shape so the sequence is mechanically inspectable:

```md
| Order | File | Bytes | Characters | SHA-256 | Covered paths/evidence | Final |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | ask-20260730-150931-package.part-001.md | ... | ... | ... | ... | no |
| N | ask-20260730-150931-package.part-00N.md | ... | ... | ... | ... | yes |
```

Generate and re-check the recorded values with available local read-only tools such as `wc -c`, `wc -m`, and `shasum -a 256` (or repository-defined equivalents). Do not substitute estimated sizes or hashes.

Send a multipart set through this state machine:

```text
prepare manifest and all parts
-> verify count, order, coverage, and SHA-256 for every part
-> send "do not review until FINAL PART" with the manifest
-> send exactly one part attachment per message in manifest order
-> verify attachment state and reviewer acknowledgement after each message
-> retry only the failed part after inspecting and clearing ambiguous composer state
-> verify all sent part names and hashes
-> send FINAL PART marker plus reviewer instructions
-> begin response-completion detection
```

Assign a distinct operation ID to each intended send action, including the
manifest instruction, each part, the final marker, and any response capture
that changes page state. A retry keeps the same ID and is allowed only when the
Handoff Result is `failed-before-submit` with direct evidence of no side effect.
`submitted`, `acknowledged`, `completed`, and `ambiguous` must never be resent.

Request acknowledgements in the form `PART <order>/<count> RECEIVED: <filename>; sha256=<manifest hash>` and compare them with the manifest before continuing. The complete sequence is one review round even though it uses multiple messages. Do not accept or archive substantive reviewer output before the final marker. Missing, duplicate, reordered, hash-mismatched, or unacknowledged parts make the round incomplete. When a provider turns pasted text into an attachment, verify exactly one intended attachment for that send action; do not paste or upload again unless the first attempt is removed or clearly failed.

## Review Artifact

Write attributed external-provider responses to
`<repo-root>/.codex/reviews/<review-id>-response.md` unless the user names another
path. Use the same review ID as the outbound package. Do not use
it for the outbound package and do not create it in Package-only mode unless
explicitly requested. Preserve previous useful passes by appending a dated pass.

Each pass should record:

- repository, branch, base, and commit/diff basis
- provider plus conversation URL/stable identity or `Not verified`
- browser/profile route
- input and output method
- reviewer findings
- Codex verification notes
- fix plan and validation
- attribution gaps
- reviewer browser surface, target URLs, browser evidence, actions, and confirmation points when live-page review was used

## Review Artifact Visibility

Choose and record one mode before writing or delivering the response file:

- `local-private` (default): keep the file untracked. A full conversation URL and verified workspace note may be retained locally when needed for attribution.
- `repository-private`: use only after the user explicitly authorizes committing the artifact and repository privacy is verified. Confirm whether full identifiers are allowed; otherwise sanitize.
- `repository-sanitized`: required for public or visibility-unknown repositories. Replace the conversation URL with a one-way fingerprint or final eight identifier characters, reduce workspace identity to `personal`, `organization`, or `Not verified`, and remove display names, email fragments, profile paths, and account notes.

External review authorization does not authorize committing `review.md`. Route any requested delivery through `repo-delivery`, scan the staged artifact for full ChatGPT conversation URLs and concrete workspace display names, and preserve the local-private source outside Git when a sanitized repository copy is needed.

Raw packages, responses, ledgers, and attachments belong directly in the ignored
`.codex/reviews/` parent and share one review-ID prefix. When durable repository evidence is
explicitly requested, create a separate sanitized copy only in a user-approved
tracked documentation path; never stage the raw local workspace.
