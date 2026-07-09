# GitHub Branch Review Loop

## Before Review

Confirm:

- repository root and nearest guidance
- branch, upstream, base, and remote
- dirty state and unrelated changes
- allowed files and validation commands

Use local `git` first. Use `gh` or GitHub tooling only when PR, CI, compare URL, or remote metadata is needed. Mark unchecked remote metadata `Not verified`.

## Loop

1. Prepare the fix branch and review package.
2. Send the package to ChatGPT only after the relevant gate.
3. Write or append ChatGPT output to `review.md`.
4. Verify every finding locally.
5. Fix confirmed issues only.
6. Run matching validation.
7. Commit only if requested and only for approved scope.
8. Repeat only when requested or workflow-defined.

ChatGPT may review and suggest patches, but Codex applies changes locally after inspection.

## Commit Rules

Before committing:

- inspect changed paths and diff stat
- stage only related files
- inspect cached diff
- include `review.md` only when it is part of the requested artifact
- avoid broad staging

Use a concise Conventional Commit message unless the user supplies exact text.

## `review.md`

For repeated passes, append dated sections by default. Use numbered files only when the user asks for separate artifacts.

Each pass should include:

- pass timestamp or id
- branch and commit/diff basis
- ChatGPT URL or `Not verified`
- input method and size
- reviewer findings
- Codex verification notes
- fix commit SHA when available
- unresolved attribution gaps

## Stop Conditions

Stop when ChatGPT has no actionable findings and Codex agrees, validation needs user input, browser/account state is wrong, unrelated dirty work cannot be separated, content would expose secrets, or the next review/commit/push was not authorized.
