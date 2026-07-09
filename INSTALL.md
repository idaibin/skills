# Install Skills

This file is for AI agents or users who want to install or update skills from this repository.

Install only these skill package directories:

- `skills/code-context`
- `skills/code-planner`
- `skills/diagnose`
- `skills/code-review`
- `skills/chatgpt-review-bridge`
- `skills/code-delivery`
- `skills/frontend-implementation`
- `skills/code-security`
- `skills/ops-browser`
- `skills/ops-client`
- `skills/writing-editor`

Do not install the repository root, `prompts/`, `docs/`, or legacy skill names such as `repo-context`, `commit-reviewer`, or `planner`.

## Recommended Install

Use the standard `skills` npm CLI flow shown on skills.sh:

```bash
npx skills add https://github.com/idaibin/aicraft
```

List available skills without installing:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

Install selected skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill code-context code-planner diagnose code-review chatgpt-review-bridge code-delivery frontend-implementation code-security ops-browser ops-client writing-editor
```

For multiple selected skills, pass the names after `--skill` as shown above.

Install only the operations skills:

```bash
npx skills add https://github.com/idaibin/aicraft --skill ops-browser ops-client
```

## Update

Update installed skills:

```bash
npx skills update
```

Update only selected skills:

```bash
npx skills update ops-browser ops-client
```

For updates, selected skill names are positional arguments.

After installing or updating skills, restart any long-running agent app so updated skill metadata and descriptions are loaded.

## Reproducible Project Installs

The `skills` CLI also exposes `skills-lock.json` restore support through `skills experimental_install`. Treat it as experimental for now; prefer the standard install flow for normal use.

## Maintainer Validation

Use this only when developing this repository:

```bash
python3 scripts/validate-skills.py
```

This validates source packages without installing them. End-user installation and updates should use `npx skills add` and `npx skills update`.
