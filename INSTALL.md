# Install Skills

Use the standard `skills` CLI. The public source is `idaibin/skills`.

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
ui-design
dev-frontend
dev-rust
audit-frontend
audit-rust
audit-security
ops-browser
ops-client
ask-chatgpt
human-writing
```

The publishable source directories are:

- `skills/repo-map`
- `skills/domain-modeling`
- `skills/product-spec`
- `skills/repo-review`
- `skills/repo-delivery`
- `skills/ui-design`
- `skills/dev-frontend`
- `skills/dev-rust`
- `skills/audit-frontend`
- `skills/audit-rust`
- `skills/audit-security`
- `skills/ops-browser`
- `skills/ops-client`
- `skills/ask-chatgpt`
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

Frontend design and implementation:

```bash
npx skills@latest add idaibin/skills \
  --skill ui-design dev-frontend audit-frontend ops-browser repo-review
```

Rust implementation and audit:

```bash
npx skills@latest add idaibin/skills \
  --skill dev-rust audit-rust repo-review
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
npx skills@latest add . --list
```

Then run the repository validation commands documented in [README.md](README.md).
