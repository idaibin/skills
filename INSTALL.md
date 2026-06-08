# Install Skills

This file is for AI agents or users who want to install Codex skills from this repository.

Install only these skill package directories:

- `skills/code-context`
- `skills/code-planner`
- `skills/code-review`

Do not install the repository root, `prompts/`, `skills/skill-standard.md`, or legacy skill names such as `repo-context`, `commit-reviewer`, or `planner`.

## Direct GitHub Install

Use this when the user provides `https://github.com/idaibin/aicraft` and asks to install skills:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo idaibin/aicraft \
  --path skills/code-context \
  --path skills/code-planner \
  --path skills/code-review
```

After installing or upgrading skills, restart Codex so the new skills are loaded.

## Local Clone Sync

Use this only when working from a local clone of this repository:

```bash
python3 scripts/sync-skills.py
python3 scripts/sync-skills.py --apply
```

The first command previews the sync. The second writes to `${CODEX_HOME:-~/.codex}/skills`.
