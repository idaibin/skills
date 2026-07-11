# Install Skills

This file is for AI agents or users who want to install or update skills from this repository.

Install only these skill package directories:

- `skills/repo-context`
- `skills/code-planner`
- `skills/diagnose`
- `skills/code-review`
- `skills/repo-review`
- `skills/code-delivery`
- `skills/audit-security`
- `skills/chatgpt-review-bridge`
- `skills/implement-frontend`
- `skills/implement-rust`
- `skills/audit-frontend`
- `skills/audit-rust`
- `skills/ops-browser`
- `skills/ops-client`
- `skills/human-writing`

Do not install the repository root, `prompts/`, `docs/`, or legacy skill names such as `code-context`, `code-security`, `commit-reviewer`, `planner`, `frontend-implementation`, `frontend-governance`, or `rust-engineering-governance`.

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
  --skill repo-context code-planner diagnose code-review repo-review code-delivery audit-security chatgpt-review-bridge implement-frontend implement-rust audit-frontend audit-rust ops-browser ops-client human-writing
```

For multiple selected skills, pass the names after `--skill` as shown above.

Install only the review workflow skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-context diagnose code-review repo-review audit-frontend audit-rust audit-security
```

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
npx skills update repo-context repo-review audit-security
```

For updates, selected skill names are positional arguments.

After installing or updating skills, restart any long-running agent app so updated skill metadata and descriptions are loaded.

## Reproducible Project Installs

The `skills` CLI also exposes `skills-lock.json` restore support through `skills experimental_install`. Treat it as experimental for now; prefer the standard install flow for normal use.

## Maintainer Validation

Use this only when developing this repository:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
```

Useful targeted checks:

```bash
python3 scripts/validate-skills.py --skill repo-context
python3 scripts/validate-skills.py --skill repo-review
python3 scripts/validate-skills.py --skill diagnose
python3 scripts/validate-skills.py --skill audit-frontend
python3 scripts/validate-skills.py --skill audit-security
```

This validates source packages without installing them. End-user installation and updates should use `npx skills add` and `npx skills update`.
