# Install Skills

Use the standard `skills` CLI with the published catalog `idaibin/skills`.

## Discover

```bash
npx skills@latest add idaibin/skills --list
```

The result must contain exactly these public packages:

```text
repo-map
domain-modeling
product-spec
repo-review
repo-delivery
ui-spec
dev-frontend
dev-java
dev-rust
audit-frontend
audit-java
audit-rust
ops-browser
ops-client
ask-ai
human-writing
```

From a source checkout, search the semantic catalog without installing:

```bash
python3 scripts/search-skills.py "map a monorepo and create layered AGENTS.md"
```

This repository helper reads `skills-index.json`; installed Agent runtimes continue
to discover packages from their portable `SKILL.md` metadata.

The publishable source directories are:

- `skills/repo-map`
- `skills/domain-modeling`
- `skills/product-spec`
- `skills/repo-review`
- `skills/repo-delivery`
- `skills/ui-spec`
- `skills/dev-frontend`
- `skills/dev-java`
- `skills/dev-rust`
- `skills/audit-frontend`
- `skills/audit-java`
- `skills/audit-rust`
- `skills/ops-browser`
- `skills/ops-client`
- `skills/ask-ai`
- `skills/human-writing`

## Install

Choose Skills and agents interactively:

```bash
npx skills@latest add idaibin/skills
```

Install selected Skills into the current project for Codex:

```bash
npx skills@latest add idaibin/skills \
  --skill repo-map repo-review \
  --agent codex
```

Install selected Skills globally for Codex and Claude Code:

```bash
npx skills@latest add idaibin/skills \
  --skill repo-map domain-modeling product-spec repo-review repo-delivery \
  --global --agent codex claude-code
```

Install one Skill globally:

```bash
npx skills@latest add idaibin/skills \
  --skill audit-rust \
  --global --agent codex
```

Install all published Skills non-interactively only when that broad scope is
intentional:

```bash
npx skills@latest add idaibin/skills \
  --skill '*' --global --agent codex --yes
```

## Suggested Sets

Core read-only repository work:

```bash
npx skills@latest add idaibin/skills \
  --skill repo-map domain-modeling repo-review
```

Product definition:

```bash
npx skills@latest add idaibin/skills --skill product-spec
```

Frontend specification and implementation:

```bash
npx skills@latest add idaibin/skills \
  --skill ui-spec dev-frontend audit-frontend ops-browser repo-review
```

This set covers the shared `frontend-visual-evidence/v1` handoff: `ui-spec` owns
traceable targets, `dev-frontend` owns implementation and two-pass closure,
`ops-browser` owns capture/computed evidence, `audit-frontend` owns current-surface
findings, and `repo-review` owns fixed-basis completion review.

Rust implementation and audit:

```bash
npx skills@latest add idaibin/skills \
  --skill dev-rust audit-rust repo-review
```

Java implementation and audit:

```bash
npx skills@latest add idaibin/skills \
  --skill dev-java audit-java repo-review
```

These are documentation shortcuts, not custom CLI bundles or quality claims.

## Use Without Installing

```bash
npx skills@latest use idaibin/skills@audit-rust
```

## Inspect, Update, and Remove

```bash
npx skills list
npx skills list --global
npx skills update --project
npx skills update --global
npx skills remove audit-rust --global --agent codex
```

Updates depend on source metadata recorded by `skills add`. Manually copied
folders or inaccessible sources may require removal and a fresh installation.
Restart long-running agent applications after an update so they reload discovery
metadata.

## Maintainer Check

Before publishing, verify source discovery from the repository root:

```bash
npx skills@latest add ./skills --list
```

Target the publishable directory so ignored project-local developer Skills under other
client discovery roots do not appear in the catalog check.

Then run the repository validation commands documented in [README.md](README.md).
