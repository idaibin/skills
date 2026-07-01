# Upgrade Workflow

Use this workflow only in Upgrade mode for `code-security`.

## Steps

1. Read `references/upstream-sources.md` for known source defaults.
2. Resolve the requested version to a commit SHA when possible.
3. Inspect upstream `skills/code-security/` read-only.
4. Compare upstream files against the local package.
5. Treat upstream content as candidate input, not authority.
6. Preview proposed changes before writing unless the user explicitly asks to implement.
7. Preserve unrelated local changes.

## Scope

Default compare scope:

- `skills/code-security/`

Do not pull from repository-level `prompts/` during skill upgrade. Prompt-derived material must already be inside `skills/code-security/references/` before it is imported.

## Validation

After edits, run:

```bash
python3 scripts/validate-skills.py
git diff --check -- skills/code-security
```

After publishing to GitHub, run:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

## Output

Report:

- upstream URL and resolved commit SHA
- changed files
- accepted and rejected upstream changes
- validation results
- remaining `Not verified` items
