# GitHub Branch Review Loop

## Before Review

Confirm:

- repository root and nearest guidance
- branch, upstream, base, and remote
- dirty state and unrelated changes
- allowed files and validation commands
- outbound `review-package.md` path and whether an existing file may be replaced
- inbound external-response `review.md` path

Use local `git` first. Use `gh` or GitHub tooling only when PR, CI, compare URL, or remote metadata is needed. Mark unchecked remote metadata `Not verified`.

## Loop

1. Confirm the fix branch and write the self-contained outbound package to `review-package.md`.
2. Stop here for prepare/build/draft/package-only requests.
3. Send the package to a standard chat or Project only after explicit external-send authorization or the relevant gate.
4. Write or append the attributed ChatGPT response to `review.md`; never copy the outbound package into it.
5. Verify every finding locally.
6. Fix confirmed issues only.
7. Run matching validation.
8. If delivery is requested, hand the verified scope to `code-delivery`; the bridge does not stage, commit, or push.
9. Repeat up to the explicitly authorized round count; require new authorization before additional external rounds.

ChatGPT may review and suggest patches, but Codex applies changes locally after inspection.

## Delivery Handoff

Before handing off to `code-delivery`:

- inspect changed paths and diff stat
- identify the exact related paths for delivery
- include `review.md` only when it is part of the requested artifact
- state that broad staging is forbidden

`code-delivery` owns staging, cached-diff verification, commit creation, and push.
Preserve exact user-supplied commit text; otherwise let that skill apply the
repository's commit convention.

## Artifacts

`review-package.md` is the outbound, manually sendable package. It contains the
task/scope, repository/branch/base/commit basis, review focus, selected evidence,
validation, exclusions/redactions, and requested response format.

`review.md` is inbound only: external ChatGPT responses plus Codex verification
notes. Do not create it in Package-only mode unless the user explicitly requests
an empty response log. Keep it local-private and untracked by default. Repository
delivery requires explicit authorization; use the sanitized visibility mode for
public or visibility-unknown repositories.

For repeated passes, append dated sections by default. Use numbered files only when the user asks for separate artifacts.

Each pass should include:

- pass timestamp or id
- branch and commit/diff basis
- ChatGPT URL or `Not verified`
- standard-chat or Project surface, plus verified account workspace or `Not verified`
- input method and size
- reviewer findings
- Codex verification notes
- fix commit SHA when available
- unresolved attribution gaps

## Stop Conditions

Stop when ChatGPT has no actionable findings and Codex agrees, the authorized round count is complete, validation needs user input, browser/account state is wrong, unrelated dirty work cannot be separated, content would expose secrets, or the next review/commit/push was not authorized.
