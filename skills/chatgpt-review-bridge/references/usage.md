# Usage

## Trigger Examples

- `Prepare/build/draft a review package for ChatGPT, but do not send it.`
- `Use ChatGPT now to review this branch, save review.md, then fix confirmed issues.`
- `Send this review-package.md to ChatGPT for one review round.`
- `Use my ChatGPT Project to review this branch for three rounds, then let Codex verify and fix each round.`
- `Use Chat for a one-off independent review and save review.md.`
- `Use my Chrome profile and ChatGPT project for this repo review.`
- `Default to the Codex in-app Browser and open the ChatGPT project for this repo review.`
- `After ChatGPT review, run local Codex CLI to fix the findings, but ask which approval mode to use first.`
- `Reset the ChatGPT review bridge defaults for this repo.`

## Non-Triggers

- Local-only code review without ChatGPT Pro.
- Browser verification without a repository review loop.
- GitHub-native PR review only.
- Security-only audit without ChatGPT as reviewer.

## Local Collection

Before any external action, collect only local read-only context:

- repository path, branch, and dirty state
- review package scope and approximate size
- validation commands already run and results
- canonical outbound artifact path, normally `<repo-root>/review-package.md`
- bridge default record status
- local Chrome profile directory candidates
- cached ChatGPT tab candidates only if already available

Do not attach to Chrome, claim tabs, open browser profiles, create ChatGPT sessions, send content, start Codex CLI, or change defaults during this phase. The words prepare, build, draft, package, or create review material authorize only this local phase. Explicit send authorization removes a later duplicate route prompt; it does not skip package preparation, scope checks, or redaction.

## External Action Gate

Use the gate in `SKILL.md` only when external sending or route selection is not already authorized. Package-only wording never opens the gate and never authorizes a send. An explicit request such as `send/submit/upload this to ChatGPT`, `use ChatGPT now to review`, `ask ChatGPT to review now`, or `外部互审 3 轮` authorizes sending on the safely resolved route for the stated scope and round count; do not ask the same route question again.

Option handling:

- `1`: authorizes resolving and opening the Codex in-app Browser route; stop again before sending unless sending was also explicitly requested.
- `2`: ask before connecting to current Chrome; enumerate ChatGPT tabs; stop before claiming a tab or sending.
- `3`: generate/update the local package only.
- `4`: resolve the user-provided ChatGPT URL or surface; do not persist it unless separately requested.
- `0`: stop.

## Local Codex Gate

Use the exact Local Codex Gate in `SKILL.md` before `codex exec`.

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

## Standard Chat, Project, And Codex

- Use a standard chat for an isolated, one-off reviewer conversation.
- Use a Project for repository-bound durable context or repeated review rounds
  when its URL can be verified. Verify the account workspace separately.
- Use Codex to collect evidence, apply fixes, run tests, and challenge ChatGPT findings locally.
- For mutual review, alternate `standard chat or Project review -> Codex verification/fix -> next external round`. Count only completed, attributed ChatGPT responses as external review rounds.
- Let `chatgpt-review-bridge` own the package, send authorization, surface, round count, conversation mapping, and response archive. Use `ops-browser` only for low-level browser actions and evidence on the route the bridge selected.

For a verified Project with no mapped conversation, an explicit external send
authorizes creation of one conversation. Open the Project, create one
conversation, verify its stable URL/ID and empty composer state before send when
the surface exposes them, record it, and then send. If identity is assigned only
on first submit, record pre-send Project/account evidence and verify/store the
URL/ID immediately after the authorized submit before accepting the response.
Do not create conversations during Package-only work.

## Review Package

Write the outbound package to `<repo-root>/review-package.md` unless the user
names another path. If that file already exists, preserve it and request
overwrite approval or use an explicitly selected alternate path. The artifact
must be complete enough for the user to copy or upload manually without hidden
conversation context.

Include only in-scope evidence:

- task summary and review focus
- repo path, branch, base, commit, and remote when available
- `git diff --stat`, `git diff --name-status`, and selected diffs
- relevant files or excerpts
- validation output summaries
- explicit exclusions
- redactions and omitted sensitive/unrelated material
- requested reviewer response format and verdict

Prefer text input under 20,000 characters and a file/pasted attachment for 20,000-80,000 characters. Above 80,000 characters, 20 files, or 1 MB, keep `review-package.md` as the manifest and shared review contract, and write ordered sibling parts as `review-package.part-001.md`, `review-package.part-002.md`, and so on. The manifest must list the part count and, for every part, its byte and character count, SHA-256, covered paths or evidence, exclusions, order, and whether it is the final part. For a user-supplied path such as `custom.md`, use `custom.part-001.md`. Treat the manifest and every part as one artifact set: do not overwrite any existing member without authorization, and do not send a partial set as a complete package.

Use this manifest table shape so the sequence is mechanically inspectable:

```md
| Order | File | Bytes | Characters | SHA-256 | Covered paths/evidence | Final |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | review-package.part-001.md | ... | ... | ... | ... | no |
| N | review-package.part-00N.md | ... | ... | ... | ... | yes |
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

Request acknowledgements in the form `PART <order>/<count> RECEIVED: <filename>; sha256=<manifest hash>` and compare them with the manifest before continuing. The complete sequence is one review round even though it uses multiple messages. Do not accept or archive substantive reviewer output before the final marker. Missing, duplicate, reordered, hash-mismatched, or unacknowledged parts make the round incomplete. When ChatGPT turns pasted text into an attachment, verify exactly one intended attachment for that send action; do not paste or upload again unless the first attempt is removed or clearly failed.

## Review Artifact

Write external ChatGPT responses to `<repo-root>/review.md` unless the user names another path. Do not use it for the outbound package and do not create it in Package-only mode unless explicitly requested. Preserve previous useful passes by appending a dated pass.

Each pass should record:

- repository, branch, base, and commit/diff basis
- ChatGPT URL or `Not verified`
- browser/profile route
- input and output method
- reviewer findings
- Codex verification notes
- fix plan and validation
- attribution gaps

## Review Artifact Visibility

Choose and record one mode before writing or delivering `review.md`:

- `local-private` (default): keep the file untracked. A full conversation URL and verified workspace note may be retained locally when needed for attribution.
- `repository-private`: use only after the user explicitly authorizes committing the artifact and repository privacy is verified. Confirm whether full identifiers are allowed; otherwise sanitize.
- `repository-sanitized`: required for public or visibility-unknown repositories. Replace the conversation URL with a one-way fingerprint or final eight identifier characters, reduce workspace identity to `personal`, `organization`, or `Not verified`, and remove display names, email fragments, profile paths, and account notes.

External review authorization does not authorize committing `review.md`. Route any requested delivery through `code-delivery`, scan the staged artifact for full ChatGPT conversation URLs and concrete workspace display names, and preserve the local-private source outside Git when a sanitized repository copy is needed.
