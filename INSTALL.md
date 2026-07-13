# Install Skills

This file is for AI agents or users who want to install or update skills from this repository.

Install only these skill package directories:

- `skills/repo-map`
- `skills/code-planner`
- `skills/diagnose`
- `skills/repo-review`
- `skills/repo-delivery`
- `skills/audit-security`
- `skills/chatgpt-review`
- `skills/implement-frontend`
- `skills/implement-rust`
- `skills/audit-frontend`
- `skills/audit-rust`
- `skills/ops-browser`
- `skills/ops-client`
- `skills/human-writing`

Do not install the repository root, `prompts/`, `docs/`, or legacy skill names such as `repo-context`, `code-context`, `code-review`, `code-delivery`, `chatgpt-review-bridge`, `code-security`, `commit-reviewer`, `planner`, `frontend-implementation`, `frontend-governance`, or `rust-engineering-governance`.

## Recommended Install

Use the standard `skills` npm CLI flow shown on skills.sh:

```bash
npx skills add https://github.com/idaibin/aicraft
```

This installs into the current project and lets the CLI detect compatible
agents. To install globally for both OpenAI Codex and Anthropic Claude Code:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --global --agent codex claude-code
```

Use the same `--global` and `--agent` selection when adding only a subset of
skills. The current CLI agent identifiers are `codex` and `claude-code`.

List available skills without installing:

```bash
npx skills add https://github.com/idaibin/aicraft --list
```

Install selected skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map code-planner diagnose repo-review repo-delivery audit-security chatgpt-review implement-frontend implement-rust audit-frontend audit-rust ops-browser ops-client human-writing
```

For multiple selected skills, pass the names after `--skill` as shown above.

Install the repository-engineering workflow skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map code-planner diagnose repo-review repo-delivery
```

Add bounded domain-audit specialists when the repository work needs them:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill audit-frontend audit-rust audit-security
```

Install only the operations skills:

```bash
npx skills add https://github.com/idaibin/aicraft --skill ops-browser ops-client
```

## Update

`skills update` checks CLI-tracked source versions and updates changed skills.
Update skills installed in the current project:

```bash
npx skills update --project
```

Update global skills, including global Codex and Claude Code installations:

```bash
npx skills update --global
```

Update only selected skills:

```bash
npx skills update repo-map repo-review audit-security
```

For updates, selected skill names are positional arguments. `update` supports
project or global scope, but does not expose an `--agent` filter; it refreshes
the tracked installation in the selected scope. Use `--yes` to accept the
detected scope without an interactive prompt:

```bash
npx skills update --yes
```

Inspect installed skills before or after an update:

```bash
npx skills list
npx skills list --global
npx skills list --global --agent codex claude-code
```

After installing or updating skills, restart any long-running agent app so updated skill metadata and descriptions are loaded.

### Update Requirements And Limits

Automatic updates depend on installation metadata recorded by
`npx skills add`. They are reliable when the source repository remains
reachable and the skill keeps the same published name and path.

`npx skills update` is not a universal repair or migration command:

- manually copied or downloaded skill folders may not have a tracked source;
- deleted local skill folders may need `npx skills add` again;
- private, removed, or inaccessible source repositories cannot be refreshed;
- renamed or moved skills require explicit remove-and-add migration;
- local-path or other non-remote sources may not support remote version checks.

Do not maintain separate OpenAI and Anthropic copies by hand. Install both
through one CLI command so their agent directories point to the same tracked
skill source and use the same update flow.

### Rename Migration

The current suite includes these public-name migrations:

| Retired name | Replacement | Change |
| --- | --- | --- |
| `repo-context` | `repo-map` | clearer semantic repository-map ownership |
| `code-review` | `repo-review` | local and immutable review unified as review-basis modes |
| `code-delivery` | `repo-delivery` | repository workflow naming aligned |
| `chatgpt-review-bridge` | `chatgpt-review` | shorter intent-based review entrypoint |

An update cannot remove retired names automatically. Existing project-scope
users should remove the old packages and add the replacements:

```bash
npx skills remove repo-context code-review code-delivery chatgpt-review-bridge
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map repo-review repo-delivery chatgpt-review
```

For global Codex and Claude Code installations, preserve both scope and remove
the retired names from each agent target:

```bash
npx skills remove --global --agent codex \
  repo-context code-review code-delivery chatgpt-review-bridge
npx skills remove --global --agent claude-code \
  repo-context code-review code-delivery chatgpt-review-bridge
npx skills add https://github.com/idaibin/aicraft \
  --global --agent codex claude-code \
  --skill repo-map repo-review repo-delivery chatgpt-review
```

Restart long-running agent apps afterward and use `npx skills list` or
`npx skills list --global` to confirm that only the replacement names remain.

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
python3 scripts/validate-skills.py --skill repo-map
python3 scripts/validate-skills.py --skill repo-review
python3 scripts/validate-skills.py --skill diagnose
python3 scripts/validate-skills.py --skill audit-frontend
python3 scripts/validate-skills.py --skill audit-security
```

This validates source packages without installing them. End-user installation and updates should use `npx skills add` and `npx skills update`.
