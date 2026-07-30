# GitHub Branch Review Loop

## Before Review

Confirm:

- repository root and nearest guidance
- branch, upstream, base, and remote
- dirty state and unrelated changes
- allowed files and validation commands
- ignored review parent, normally `.codex/reviews/`
- outbound `<review-id>-package.md` and inbound `<review-id>-response.md` paths inside it, plus whether an existing artifact set may be replaced

Use local `git` first. Use `gh` or GitHub tooling only when PR, CI, compare URL, or remote metadata is needed. Mark unchecked remote metadata `Not verified`.

## Combined Loop

1. Fix the branch/commit/diff basis and write an unbiased `<review-id>-package.md`.
2. Stop for package-only requests.
3. Run a bounded `repo-review` and, only when authorized, independent selected-provider review. Neither receives another reviewer's conclusions before reporting.
4. Append attributed external-provider output to `<review-id>-response.md`; locally verify and deduplicate all finding sets.
5. Stop with locally confirmed/rejected findings unless the user also requested source fixes.
6. When fixes are authorized, route confirmed issues to the matching owner, rerun the original failure path and proportionate validation, freeze a new Worktree fingerprint, and run Worktree `repo-review`; use immutable fixed-basis review only after a commit exists.
7. Repeat a provider only with explicit authorization and an independently useful result; apply any task-defined high-risk gate.
8. If delivery is requested, hand exact verified paths to `repo-delivery`; this skill never stages, commits, or pushes.

Codex is strongest at exact code, call-chain, generated-artifact, CI, and compatibility evidence. External providers challenge product logic, scope, architecture tradeoffs, alternatives, and cross-domain blind spots. Codex locally validates every layer. Local confirmation is not source-change authorization.

## Delivery Handoff

For `review-publication`, use a GitHub branch as the reviewer input only when all of
these are true:

- the user explicitly authorized publishing the review basis;
- a verified GitHub remote exists;
- the current branch is not `main`, the default branch, or a protected branch;
- the exact review commit can be created and pushed without force.

Hand the exact paths, commit requirement, target remote/branch, and validation evidence
to `repo-delivery`. After it reports a successful push, record the canonical
repository URL, branch, and full SHA as the immutable provider basis. This skill never
stages, commits, pushes, opens a PR, merges, or force-pushes. If any condition is
missing, send or package only the necessary files and bounded plan instead; do not
expand Git authority to make repository review possible.

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

`.codex/reviews/<review-id>-package.md` is the outbound, manually sendable package. It contains the
task/scope, repository/branch/base/commit basis, review focus, selected evidence,
validation, exclusions/redactions, and requested response format.

The matching `.codex/reviews/<review-id>-response.md` is inbound only: attributed external-provider responses plus Codex verification
notes. Do not create it in Package-only mode unless the user explicitly requests
an empty response log. Keep the whole prefixed artifact set local-private and ignored.
Repository delivery requires explicit authorization and a separate sanitized
durable copy under the repository's approved documentation structure.

For repeated passes, append dated sections by default. Use numbered files only when the user asks for separate artifacts.

Each pass should include:

- pass timestamp or id
- branch and commit/diff basis
- provider plus conversation URL/stable identity or `Not verified`
- provider-specific surface/context, plus verified account workspace or `Not verified`
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
External-provider agreement is neither necessary nor sufficient for completion.
