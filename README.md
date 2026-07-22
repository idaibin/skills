# Skills

Independent Agent Skills for real software-engineering work.

Each published Skill is a self-contained package with its own trigger, workflow,
authority boundary, output contract, supporting references, and evaluation
cases. Skills can be installed separately and composed when a task crosses
owners; none requires another package or a repository-root runtime file to do
its basic job.

[![skills.sh](https://skills.sh/b/idaibin/skills)](https://skills.sh/idaibin/skills)

## Install

Browse and select Skills interactively:

```bash
npx skills@latest add idaibin/skills
```

List the catalog without installing:

```bash
npx skills@latest add idaibin/skills --list
```

Install selected Skills globally for Codex:

```bash
npx skills@latest add idaibin/skills \
  --skill repo-map domain-modeling repo-review \
  --global --agent codex
```

Install one Skill:

```bash
npx skills@latest add idaibin/skills \
  --skill ui-design \
  --global --agent codex
```

See [INSTALL.md](INSTALL.md) for project/global scope, updates, and removal.

## Catalog

### Repository Engineering

| Skill | Use when |
| --- | --- |
| `repo-map` | Current repository boundaries, commands, task routes, reusable owners, or a bounded native/optionally-generated protocol chain need a verified map. |
| `domain-modeling` | Shared business terms, rules, lifecycle conflicts, or domain boundaries are ambiguous across product work. |
| `repo-review` | Current Worktree/index, a fixed SHA/range (including resolved PR base/head), or a verified review package needs independent read-only review; Release is conditional. |
| `repo-delivery` | Reviewed changes need categorized commits, an explicit single commit, push/sync, evidence-based branch integration, or cleanup. |

### Product Definition

| Skill | Use when |
| --- | --- |
| `product-spec` | Product behavior, scope, rules, states, or acceptance must become one implementation-ready feature/foundation spec or an authorized product-fact update. |

### Design and Implementation

| Skill | Use when |
| --- | --- |
| `ui-design` | A concrete page or flow needs visual/interaction design, or shared tokens, component semantics, variants, or visual language must change. |
| `dev-frontend` | A requested frontend feature, component, page, or accepted UI design must be implemented and validated. |
| `dev-rust` | A requested Rust feature, refactor, or port must be implemented with ownership and behavior evidence. |

### Audit and Operations

| Skill | Use when |
| --- | --- |
| `audit-frontend` | A known frontend surface needs a bounded read-only architecture, accessibility, performance, state, or design audit. |
| `audit-rust` | A Rust workspace or surface needs a bounded ownership, concurrency, SQLite, unsafe/FFI, performance, or memory audit. |
| `audit-security` | A known security-sensitive code or configuration surface needs a bounded read-only assessment. |
| `ops-browser` | A browser page or bounded platform action must be operated or verified with capability, identity, authorization, and before/after evidence. |
| `ops-client` | A Tauri, Electron, or native desktop client must be verified against its real process and window. |

### ChatGPT and Writing Extensions

| Skill | Use when |
| --- | --- |
| `ask-chatgpt` | Codex needs to ask ChatGPT for a local request package or an explicitly authorized independent review, research result, visual exploration, or decision challenge. |
| `human-writing` | Source-grounded writing must be drafted, rewritten, diagnosed, or adapted in the requested final language while preserving facts, voice, attribution, and disclosures; English-first support for a Chinese final is optional. |

## Composition

Skills are composable owners, not a mandatory framework:

```text
unknown repository -> repo-map
unclear domain      -> domain-modeling
unclear product     -> product-spec
complex change      -> host planning and repository instructions
known failure       -> evidence-driven diagnosis under effective instructions
source work         -> dev-frontend / dev-rust
UI design           -> ui-design (Feature UI; Design System when shared) -> dev-frontend
review              -> repo-review (with bounded audit-* specialists when needed)
delivery            -> repo-delivery
```

The nearest applicable owner may start directly. Cross-Skill handoffs transfer
bounded evidence, never implicit authorization. Use one owner by default, load only
the selected references, reuse unchanged evidence, and add tasks or review rounds only
when they produce a required independent result.

## Package Contract

Every public package lives at `skills/<name>/` and contains:

```text
skills/<name>/
├── SKILL.md
├── agents/openai.yaml
└── references/
```

Packages add `assets/` or `scripts/` only when the capability needs them. A
published package may depend only on files inside its own directory and must not
require another Skill or an absolute local path at runtime.

Repository-level `docs/`, `protocols/`, and `scripts/` are maintainer surfaces;
published packages do not depend on them at runtime.

## Validate

Use the concise command matrix in [`skills/AGENTS.md`](skills/AGENTS.md#validation).
The validator checks the portable Agent Skills package, OpenAI metadata, direct
references, representative eval sections, and catalog consistency. Exercise behavior
changes on a few representative tasks.

## Design Principles

- Small, intent-based, and composable, following the useful catalog qualities
  demonstrated by `mattpocock/skills`.
- One public Skill per stable user intent and authority boundary; technology
  variants remain profiles when their owner and output contract are the same.
- Progressive disclosure: concise discovery metadata and `SKILL.md`, with
  detailed workflows and examples in package-local references.
- Repository truth and explicit authorization take priority over generic
  conventions.

## Contributing and License

Read [AGENTS.md](AGENTS.md), [skills/AGENTS.md](skills/AGENTS.md), and
[docs/skills/skill-standard.md](docs/skills/skill-standard.md) before changing a
package. Unless a file states otherwise, the collection is available under the
[Apache License, Version 2.0](LICENSE).
