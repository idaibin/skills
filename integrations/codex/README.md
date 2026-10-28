# Codex custom agents

This directory is the maintained source for reusable Codex custom agents. Installed
files under `${CODEX_HOME:-$HOME/.codex}/agents/` are runtime copies. Change and review
the tracked source first, then install it and verify parity. Keep personal model
routing, credentials, account settings and project paths in their existing owners.

These are Codex-specific configurations, separate from the portable `skills/`
catalog. The `skills` CLI installs Skill packages; it does not install these agents.
Forgeway owns delivery standards; the Handbook owns learning material. Neither owns
these installed agent copies.

## Available agents

| Source | Purpose | Runtime settings |
| --- | --- | --- |
| [agents/qa.toml](agents/qa.toml) | Risk-based software acceptance across UI, APIs and business journeys; preserves raw evidence and separates runner success from case verdicts. | Model and effort follow the parent or explicit task selection; no permission or provider overrides. |

`qa` uses available Skills and tools within the assigned scope. Product changes stay
with the implementation owner, and storage cleanup requires the host's scoped
authority. Instructions constrain behavior; they do not create a read-only sandbox.

## Install and verify

From this repository root, inspect any existing local difference before replacing
the installed file:

```bash
diff -u "${CODEX_HOME:-$HOME/.codex}/agents/qa.toml" integrations/codex/agents/qa.toml
```

If the target does not exist, install it directly. If it differs, reconcile any
intentional local changes into the reviewed source before the authorized update.
Install only this agent:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/agents"
install -m 600 integrations/codex/agents/qa.toml "${CODEX_HOME:-$HOME/.codex}/agents/qa.toml"
cmp integrations/codex/agents/qa.toml "${CODEX_HOME:-$HOME/.codex}/agents/qa.toml"
```

`cmp` exit 0 proves filesystem parity. Use the current Codex client's reload or new
session flow and verify that it exposes `qa`; installed bytes alone do not establish
that an existing session reloaded the instructions or that an agent followed them.
Do not copy an entire user configuration or overwrite other agents.

## Maintenance checks

Validate the source with Python 3.11 or later and check the exact changed paths:

```bash
python3 -c 'import pathlib, tomllib; d = tomllib.loads(pathlib.Path("integrations/codex/agents/qa.toml").read_text()); assert all(isinstance(d.get(k), str) and d[k].strip() for k in ("name", "description", "developer_instructions")); assert d["name"] == "qa"'
git diff --check -- integrations/codex README.md AGENTS.md
```

Add corresponding behavioral evidence when changing instructions; syntax and parity
checks do not prove live acceptance quality. Retire an agent only after checking its
runtime users and removing its installed copies within explicit authorization.

Configuration format and personal/project discovery paths follow the
[official OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
