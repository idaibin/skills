# Upgrade Workflow

Use this workflow when updating `code-planner` from GitHub, another remote repository, or a supplied branch, tag, commit, directory, or file URL.

## 1. Local Preflight

- Read the local `code-planner` files first.
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

- remote `skills/code-planner/`

Do not execute remote scripts or install remote dependencies.

## 4. Compare And Classify

Compare remote content against local files and classify candidates:

- skill-core: changes to `SKILL.md`, workflow rules, trigger wording, hard rules, or output contract
- bundled-reference: reference files needed for published use
- agent-interface: metadata such as `agents/openai.yaml`
- reject: content that is stale, too project-specific, duplicates local truth, or requires external files

## 5. Prompt And Reference Rules

- Upgrade mode reads the remote skill package only.
- If prompt-derived templates are required by the skill, they must already exist in remote `skills/code-planner/references/`.
- Do not pull directly from remote repository-level `prompts/` during skill upgrade.
- Do not embed private project paths, one-off task details, or historical session notes into the published skill.

## 6. Preview Before Writing

Before editing files, show:

- upstream URL and resolved commit SHA
- compared paths
- proposed file changes
- risks and rejected candidates

Write files only after the user explicitly confirms the preview or asks for implementation.

## 7. Verification After Writing

Run checks that match the edit:

- structure check with `find skills/code-planner -maxdepth 3 -type f | sort`
- metadata check with `rg -n "^name:|^description: Use when" skills/code-planner/SKILL.md`
- stale-name check for old skill names or obsolete source references
- self-contained check for required external prompt dependencies
- Markdown whitespace check
- `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub
- `git diff --check -- skills/code-planner`
- `git status --short` to report final worktree state

Final output must state what was updated, which remote version was used, which checks ran, and what remains unverified.
