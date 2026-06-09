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

Run the same command to upgrade the installed packages from GitHub. After installing or upgrading skills, restart Codex so the new descriptions and metadata are loaded.

## Local Clone Sync

Use this only when working from a local clone of this repository:

```bash
python3 scripts/sync-skills.py --validate-only
python3 scripts/sync-skills.py
python3 scripts/sync-skills.py --apply
python3 scripts/sync-skills.py --validate-only --check-target
```

The first command validates source packages without touching local installed skills. The dry run previews the sync. The apply command writes to `${CODEX_HOME:-~/.codex}/skills` and validates the installed target. The final command re-checks that the selected packages are installed and that legacy names are absent.
