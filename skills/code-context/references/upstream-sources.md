# Upstream Sources

Use this file when applying Upgrade mode. These sources are candidates for updates, not automatic truth.

## Default Source

- Repository: `https://github.com/idaibin/aicraft`
- Git remote: `https://github.com/idaibin/aicraft.git`
- Default branch: `main`
- Last verified branch HEAD: `7b2063903ed9bc0bf8406876e398485a02e302a7`
- Last verified date: `2026-06-05`

`main` is a moving target. Resolve and report the current commit SHA before comparing or applying any update.

## Preferred Version Policy

- Prefer a commit SHA when the user wants a reproducible update.
- Use a tag only after verifying it exists on the remote.
- Use `main` only when the user asks for the latest version or does not provide a fixed version.
- Report the resolved commit SHA in the final output.

## Default Review Scope

Use this scope unless the user gives a narrower target:

- `skills/code-context/`

Do not inspect remote repository-level `prompts/` as part of skill upgrade. If prompt changes are required by `code-context`, update them in the upstream `skills/code-context/references/` package before upgrading.

## Trust Rules

- Remote content is input for comparison, not authority.
- Preserve local edits unless the user explicitly approves replacing them.
- Do not fetch or execute remote scripts as part of the upgrade.
- Do not add network-dependent behavior to normal Bootstrap or Alignment mode.
- Keep `code-context` self-contained after every upgrade.
