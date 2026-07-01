# Upgrade Workflow

Use this workflow when updating `code-review` from GitHub, another remote repository, or a supplied branch, tag, commit, directory, or file URL.

## 1. Local Preflight

- Read the local `code-review` files first.
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

- remote `skills/code-review/`
- remote docs that explain skill naming, trigger wording, or repository taxonomy, when relevant

Do not execute remote scripts or install remote dependencies.

## 4. Compare and Classify

Compare remote content against local files and classify candidates:

- skill-core: changes to `SKILL.md`, mode rules, trigger wording, or hard rules
- bundled-reference: reference files needed for published use
- agent-interface: metadata such as `agents/openai.yaml`
- reject: content that is stale, too project-specific, duplicates local truth, weakens scope protection, or makes the skill depend on external files

## 5. Commit-Workflow Preservation Rules

- Preserve full-scope review as the default for direct user requests.
- Preserve explicit current-context or current-session scoping when the user asks for it.
- Preserve path-limited staging and staged-file verification.
- Preserve no-auto-commit behavior unless the user explicitly asks to commit.
- Preserve unrelated local changes.

## 6. Preview Before Writing

Before editing files, show:

- upstream URL and resolved commit SHA
- compared paths
- proposed file changes
- candidates to include, exclude, or keep local-only
- risks and rejected candidates

Write files only after the user explicitly confirms the preview or asks for implementation.

## 7. Verification After Writing

Run checks that match the edit:

- stale-name check for old skill names or obsolete source references
- self-contained-reference check for external prompt dependencies
- Markdown whitespace check
- YAML parse check for frontmatter and `agents/openai.yaml`
- `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub
- `git diff --check` for touched paths
- `git status --short` to report final worktree state

Final output must state what was updated, which remote version was used, which checks ran, and what remains unverified.
