# Install Skills

This file is for AI agents or users who want to install or update skills from this repository.

Install only these skill package directories:

- `skills/repo-map`
- `skills/domain-modeling`
- `skills/code-planner`
- `skills/design-ui`
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
  --skill repo-map domain-modeling code-planner diagnose repo-review repo-delivery design-ui audit-security chatgpt-review implement-frontend implement-rust audit-frontend audit-rust ops-browser ops-client human-writing
```

For multiple selected skills, pass the names after `--skill` as shown above.

Install the repository-engineering workflow skills:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map domain-modeling code-planner diagnose repo-review repo-delivery
```

## Installation Bundles

Install the Core Read-only bundle for mapping, planning, diagnosis, and review
without implementation or Git delivery ownership:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map domain-modeling code-planner diagnose repo-review
```

Install the Engineering bundle for the normal implementation lifecycle:

```bash
npx skills add https://github.com/idaibin/aicraft \
  --skill repo-map domain-modeling code-planner diagnose repo-review repo-delivery implement-rust implement-frontend
```

Install the Full bundle with the repository's normal all-skills command:

```bash
npx skills add https://github.com/idaibin/aicraft
```

Bundles describe install scope only. They do not imply behavior or workflow
verification. Current evidence is recorded in
[`docs/quality/status.md`](docs/quality/status.md).

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

The `skills` CLI exposes `skills-lock.json` restore support through the command
currently named `skills experimental_install`. This is an external CLI command
name, not an AICraft maturity label. Use the standard `skills add` flow for
normal installs; lockfile restore behavior is not verified by this repository.

## Maintainer Validation

Use this only when developing this repository:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
python3 scripts/eval-skill-contracts.py --validate-only
git diff --check
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
