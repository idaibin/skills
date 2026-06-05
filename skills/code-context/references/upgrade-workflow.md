# Upgrade Workflow

Use this workflow when updating `code-context` from GitHub, another remote repository, or a supplied branch, tag, commit, directory, or file URL.

## 1. Local Preflight

- Read the local `code-context` files first.
- Run `git status --short`.
- Identify unrelated local changes and preserve them.
- Confirm the requested remote source, version, and scope.

## 2. Resolve Upstream

- Read `references/upstream-sources.md` for known source defaults.
- Resolve the remote branch, tag, or commit.
- Prefer commit SHA over moving branches.
- If the remote is unavailable, stop and report the blocker.

## 3. Inspect Remotely, Read-Only

Inspect only the requested or default scope:

- remote `skills/code-context/`

Do not execute remote scripts or install remote dependencies.

## 4. Compare and Classify

Compare remote content against local files and classify candidates:

- skill-core: changes to `SKILL.md`, mode rules, trigger wording, or hard rules
- bundled-reference: reference files needed for published use
- agent-interface: metadata such as `agents/openai.yaml`
- reject: content that is stale, too project-specific, duplicates local truth, or makes the skill depend on external files

## 5. Prompt Template Rules

- Upgrade mode reads the remote skill package only.
- If prompt-derived templates are required by the skill, they must already exist in the remote `skills/code-context/references/` files.
- Do not pull directly from remote repository-level `prompts/` during skill upgrade.
- Do not embed project-specific paths, private URLs, or one-off task details into the published skill.

## 6. Preview Before Writing

Before editing files, show:

- upstream URL and resolved commit SHA
- compared paths
- proposed file changes
- risks and rejected candidates

Write files only after the user explicitly confirms the preview or asks for implementation.

## 7. Verification After Writing

Run checks that match the edit:

- stale-name check for old skill names or obsolete source references
- self-contained check for required external prompt dependencies
- Markdown whitespace check
- `git diff --check` for touched paths
- `git status --short` to report final worktree state

Final output must state what was updated, which remote version was used, which checks ran, and what remains unverified.
