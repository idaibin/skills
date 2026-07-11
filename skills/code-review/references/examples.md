# Split Examples

## Example 1: Mixed Feature and Docs

Input:

- Backend code changes for one feature.
- Updated tests for the same behavior.
- README and guide updates for the new API contract.

Split:

- Commit 1: code + tests.
- Commit 2: docs only, if the docs are not required to understand the code diff.
- Staging: list the exact code/test paths for Commit 1 and exact docs paths for Commit 2.
- Report validation run for code separately from docs-only checks.

## Example 2: Build and Deploy Rename

Input:

- `justfile`
- Dockerfiles
- CI workflows
- Deployment templates
- Old deployment paths removed

Split:

- One deploy commit when the file names, artifact paths, and workflow steps are all changing together.
- Include the exact artifact names and workflow paths that make the files contractually linked.

## Example 3: Generated or Local Files

Input:

- `target/`
- logs
- screenshots
- editor caches

Split:

- Do not commit these files.
- Mention them only in the "not suitable for commit" section.
- Exclude them from the staging plan even if they sit under the same feature directory.

## Example 4: Schema Change

Input:

- backend persistence code
- database migration
- API or docs that describe the same schema change

Split:

- Keep the migration with the implementation.
- Add docs in the same commit only if they describe the same contract change.
- Verify the API/types/front-end consumers that depend on the schema when they are in scope.

## Example 5: Mixed Runtime and Docs Cleanup

Input:

- Runtime config refactor.
- Service template update.
- README and architecture docs update.

Split:

- Commit 1: runtime/config code.
- Commit 2: deployment and workflow files.
- Commit 3: docs only, if the docs are not required to explain the runtime change.

## Example 6: Dirty Worktree With Unrelated User Edits

Input:

- Task files under `src/feature-a/`.
- Existing user edits under `src/feature-b/`.
- A modified `README.md` unrelated to the requested task.

Split:

- Plan a commit containing only the `src/feature-a/` files when they form one semantic unit.
- Exclude `src/feature-b/` and `README.md`; report them as preserved unrelated changes.
- Require exact path-limited staging and staged-file verification during `code-delivery`.

## Example 7: Current-Context Commit Request

Input:

- Full worktree has several unrelated local changes.
- User says: "only commit the current session changes."

Response:

- First inventory the complete local change scope.
- Identify the current-context subset from conversation and diffs.
- Default to a commit plan and staging scope for only the current-session files.
- Report the rest of the reviewed local changes as preserved out-of-scope changes.
- Ask for scope clarification only if the current-session subset is ambiguous, needs files outside it, or conflicts with pre-existing staged files.

## Example 8: Direct Full Commit Request

Input:

- Full worktree has several changed feature, docs, and config files.
- User says: "review and commit my changes."

Response:

- First inventory and review the complete local change scope.
- Default to commit plans that cover the full reviewed scope, split by semantic unit.
- Exclude only unsafe generated/local files or unrelated files that the review clearly identifies.

## Example 9: AI Sub-Workflow Invocation

Input:

- Another AI agent invokes this skill to review only files from its task before delivery.
- Full worktree also has unrelated user edits.

Response:

- First inventory and review the complete local change scope.
- Follow the caller's stated task scope for the commit plan and staging instructions.
- Report out-of-scope local changes and any safety concerns that affect the scoped commit.
