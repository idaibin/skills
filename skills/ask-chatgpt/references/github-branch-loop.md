# GitHub Branch Review Loop

## Before Review

Confirm:

- repository root and nearest guidance
- branch, upstream, base, and remote
- dirty state and unrelated changes
- allowed files and validation commands
- ignored review directory, normally `.codex/reviews/<review-id>/`
- outbound `review-package.md` and inbound external-response `review.md` paths inside it, plus whether an existing artifact set may be replaced

Use local `git` first. Use `gh` or GitHub tooling only when PR, CI, compare URL, or remote metadata is needed. Mark unchecked remote metadata `Not verified`.

## Combined Loop

1. Fix the branch/commit/diff basis and write an unbiased `review-package.md`.
2. Stop for package-only requests.
3. Run a bounded `repo-review` and, only when authorized, an independent ChatGPT review. Neither receives the other's conclusions before reporting.
4. Append attributed ChatGPT output to `review.md`; locally verify and deduplicate both finding sets.
5. Stop with locally confirmed/rejected findings unless the user also requested source fixes.
6. When fixes are authorized, route confirmed issues to the matching owner, rerun the original failure path and proportionate validation, freeze a new Worktree fingerprint, and run Worktree `repo-review`; use immutable fixed-basis review only after a commit exists.
7. Repeat ChatGPT only with explicit authorization plus a confirmed P0/P1, permission/privacy/security, migration/irreversible, public-compatibility, production/release, or equivalent new risk.
8. If delivery is requested, hand exact verified paths to `repo-delivery`; this skill never stages, commits, or pushes.

Codex is strongest at exact code, call-chain, generated-artifact, CI, and compatibility evidence. ChatGPT should challenge product logic, scope, architecture tradeoffs, alternatives, and cross-domain blind spots. Codex locally validates both layers. Local confirmation is not source-change authorization.

## Delivery Handoff

Before handing off to `repo-delivery`:

- inspect changed paths and diff stat
- identify the exact related paths for delivery
- create a separate sanitized durable review copy only when it is part of the requested artifact
- never stage the raw `.codex/reviews/` workspace
- state that broad staging is forbidden

`repo-delivery` owns staging, cached-diff verification, commit creation, and push.
Preserve exact user-supplied commit text; otherwise let that skill apply the
repository's commit convention.

## Artifacts

`.codex/reviews/<review-id>/review-package.md` is the outbound, manually sendable package. It contains the
task/scope, repository/branch/base/commit basis, review focus, selected evidence,
validation, exclusions/redactions, and requested response format.

The matching `.codex/reviews/<review-id>/review.md` is inbound only: external ChatGPT responses plus Codex verification
notes. Do not create it in Package-only mode unless the user explicitly requests
an empty response log. Keep the whole review directory local-private and ignored.
Repository delivery requires explicit authorization and a separate sanitized
durable copy under the repository's approved documentation structure.

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

Complete when the post-fix basis is stable, required validation passes, and final
`repo-review` has no actionable finding. Stop earlier when validation needs user
input, browser/account state is wrong, unrelated dirty work cannot be separated,
content would expose secrets, or the next external/delivery action lacks authorization.
ChatGPT agreement is neither necessary nor sufficient for completion.
