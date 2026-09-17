# Agent Skills for Software Engineering

Reusable Agent Skills for practical software-engineering work.

Install only the capabilities you need, or use the complete catalog. Each Skill owns
one clear kind of work—such as repository mapping, implementation, review, browser
operation, or external-AI collaboration—and keeps its authority boundary explicit.

## Quick Start

Browse the 17 available Skills:

```bash
npx skills@latest add idaibin/skills --list
```

Choose Skills interactively:

```bash
npx skills@latest add idaibin/skills
```

Install selected Skills globally for Codex:

```bash
npx skills@latest add idaibin/skills \
  --skill repo-map repo-review ask-ai \
  --global --agent codex
```

Install the complete catalog:

```bash
npx skills@latest add idaibin/skills \
  --skill '*' --global --agent codex --yes
```

See [INSTALL.md](INSTALL.md) for project installs, suggested sets, updates, removal,
and other supported agents.

## Catalog

| Skill | What it helps with |
| --- | --- |
| `repo-map` | Scan, query, and render repository asset relationships, ownership, coverage, and drift. |
| `domain-modeling` | Resolve shared business terms, rules, lifecycles, and domain boundaries. |
| `product-spec` | Turn product decisions into implementation-ready behavior, states, and acceptance criteria. |
| `api-spec` | Design or revise native API contracts and validate OpenAPI against accepted business behavior. |
| `ui-spec` | Turn an accepted visual source into a traceable UI contract. |
| `to-task` | Create and reconcile a durable project task ledger from accepted contracts and findings. |
| `dev-frontend` | Implement and validate frontend features, refactors, tooling, and selected-source UI work. |
| `dev-typescript` | Implement non-browser TypeScript and JavaScript services, CLIs, workers, MCP servers, libraries, and scripts across Node.js, Bun, and Deno. |
| `dev-java` | Implement Java and Spring changes against the repository's real build and runtime contracts. |
| `dev-rust` | Implement Rust features and refactors with ownership, safety, and behavior evidence. |
| `repo-audit` | Audit an existing frontend, Java, or Rust surface read-only through language profiles. |
| `repo-review` | Review a Worktree, commit, range, or verified package on a fixed evidence basis. |
| `repo-delivery` | Commit, integrate, push, and clean up reviewed changes with explicit Git authorization. |
| `ops-browser` | Operate and verify browser pages while preserving target and evidence boundaries. |
| `ops-client` | Operate and verify real desktop-client processes and windows. |
| `ask-ai` | Prepare or run explicitly authorized external-AI review, research, relay, and image workflows. |
| `human-writing` | Draft, rewrite, diagnose, and adapt source-grounded writing without changing its facts or voice. |

## How They Work Together

Start with the Skill closest to the requested outcome. Add another owner only when the
task genuinely crosses an authority boundary.

```text
unknown repository -> repo-map
unclear product     -> domain-modeling / product-spec
API contract        -> api-spec -> matching implementation owner
UI contract         -> ui-spec -> dev-frontend
accepted contracts  -> to-task -> matching implementation owner
source change       -> matching dev-* owner (`dev-typescript` for non-browser TS/JS)
bounded audit       -> repo-audit (frontend / Java / Rust profile)
change review       -> repo-review
Git delivery        -> repo-delivery
browser/client proof -> ops-browser / ops-client
external AI         -> ask-ai
```

Handoffs transfer scoped evidence, not permission. For example, implementation does
not authorize a commit, and an external review does not authorize source changes.
Every package is self-contained at runtime and can be installed independently.

## Find the Right Skill

From a source checkout, search by task, stack, capability, or boundary:

```bash
python3 scripts/search-skills.py "review release risk"
python3 scripts/search-skills.py "implement a Java migration" --json
```

The search uses [`skills-index.json`](skills-index.json). Runtime discovery continues
to use each package's portable `SKILL.md` metadata.

## Documentation

- [Installation and updates](INSTALL.md)
- [Skill authoring standard](docs/skills/skill-standard.md)
- [Routing and ownership](docs/standards/skill-routing.md)
- [Repository contribution rules](AGENTS.md)
- [Package contribution rules](skills/AGENTS.md)

## Development

Run the repository's complete validation entry point before publishing changes:

```bash
bash scripts/check-skills.sh
```

Detailed validation rules live in [skills/AGENTS.md](skills/AGENTS.md#validation).

## License

Licensed under the [Apache License 2.0](LICENSE).
