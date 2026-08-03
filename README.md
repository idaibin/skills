# Skills

Independent Agent Skills for real software-engineering work.

Each published Skill is a self-contained package with its own trigger, workflow,
authority boundary, output contract, supporting references, and evaluation
cases. Skills can be installed separately and composed when a task crosses
owners; none requires another package or a repository-root runtime file to do
its basic job.

## Install

Set `CATALOG_SOURCE` to the published catalog coordinate for the environment. The
documentation intentionally does not embed an owner, account, or repository name.

Browse and select Skills interactively:

```bash
npx skills@latest add "$CATALOG_SOURCE"
```

List the catalog without installing:

```bash
npx skills@latest add "$CATALOG_SOURCE" --list
```

Search this checkout by task, capability, stack, or boundary before installing:

```bash
python3 scripts/search-skills.py "create AGENTS.md for frontend and backend"
python3 scripts/search-skills.py "review release risk" --json
```

The search reads [`skills-index.json`](skills-index.json). Each package's portable
`SKILL.md` description remains the runtime activation authority.

Install selected Skills globally for Codex:

```bash
npx skills@latest add "$CATALOG_SOURCE" \
  --skill repo-map domain-modeling repo-review \
  --global --agent codex
```

Install one Skill:

```bash
npx skills@latest add "$CATALOG_SOURCE" \
  --skill ui-spec \
  --global --agent codex
```

See [INSTALL.md](INSTALL.md) for project/global scope, updates, and removal.

## Catalog

### Repository Engineering

| Skill | Use when |
| --- | --- |
| `repo-map` | Current repository boundaries, architecture, commands, critical dependency routes—including Maven/Gradle Java boundaries—reusable owners, or explicitly requested layered root/subproject `AGENTS.md` guidance needs evidence-based creation or repair. |
| `domain-modeling` | Shared business terms, rules, lifecycle conflicts, or domain boundaries are ambiguous across product work. |
| `repo-review` | Current Worktree/index, a fixed SHA/range (including resolved PR base/head), or a verified review package needs independent read-only review; Release and selected-source visual completion are conditional profiles. |
| `repo-delivery` | Reviewed changes need categorized commits, an explicit single commit, push/sync, evidence-based branch integration, or cleanup. |

### Product Definition

| Skill | Use when |
| --- | --- |
| `product-spec` | Product behavior, scope, rules, states, or acceptance must become one implementation-ready feature/foundation spec or an authorized product-fact update. |

### Design and Implementation

| Skill | Use when |
| --- | --- |
| `ui-spec` | A selected visual source or accepted UI surface must become a traceable implementation-ready contract; keep source targets separate from current runtime and use root DESIGN.md only for shared visual authority. |
| `dev-frontend` | A requested frontend feature, component, page, build/tooling migration, or accepted UI specification must be implemented and validated, including two-pass runtime comparison for selected-source visual work. |
| `dev-java` | A requested Java source or Java-owned Spring/build change must be implemented against the repository's JDK, Maven/Gradle, security, transaction, and runtime contracts. |
| `dev-rust` | A requested Rust feature, refactor, or port must be implemented with ownership and behavior evidence. |

### Audit and Operations

| Skill | Use when |
| --- | --- |
| `audit-frontend` | A known frontend surface needs a bounded read-only architecture, build/tooling, accessibility, performance, state, or selected-source visual fidelity audit. |
| `audit-java` | A known Java source or Java-owned Spring/build configuration surface needs a bounded read-only architecture, API/security, transaction, persistence, integration, performance, or migration audit. |
| `audit-rust` | A Rust workspace or surface needs a bounded ownership, concurrency, SQLite, unsafe/FFI, performance, or memory audit. |
| `ops-browser` | A browser page or bounded platform action must be operated or verified, including same-viewport/state source/runtime capture and computed visual evidence. |
| `ops-client` | A Tauri, Electron, or native desktop client must be verified against its real process and window. |

### External AI and Writing Extensions

| Skill | Use when |
| --- | --- |
| `ask-ai` | Codex needs a local request package, built-in domain review prompt, user-defined review instruction, or another explicitly authorized independent external-AI review, research result, image review/generation/edit, visual exploration, or decision challenge. |
| `human-writing` | Source-grounded writing must be drafted, rewritten, diagnosed, or adapted in the requested final language while preserving facts, voice, attribution, and disclosures; English-first support for a Chinese final is optional. |

`ask-chatgpt` was renamed to `ask-ai`. Legacy wording and ChatGPT-only defaults remain
compatible through `ask-ai`; the old package is not maintained as a second owner.

## Composition

Skills are composable owners, not a mandatory framework:

```text
unknown repository -> repo-map
unclear domain      -> domain-modeling
unclear product     -> product-spec
complex change      -> host planning and repository instructions
known failure       -> evidence-driven diagnosis under effective instructions
source work         -> dev-frontend / dev-java / dev-rust
visual exploration  -> Codex Product Design -> selected visual source
UI specification    -> ui-spec (source/runtime delta + per-slice Feature Spec) -> dev-frontend
visual evidence     -> ops-browser (same viewport/state + computed evidence per pass)
review              -> repo-review (including security risks on the selected basis)
delivery            -> repo-delivery
```

The nearest applicable owner may start directly. Cross-Skill handoffs transfer
bounded evidence, never implicit authorization. Use one owner by default, load only
the selected references, reuse unchanged evidence, and add tasks or review rounds only
when they produce a required independent result.

Selected-source frontend work uses the shared `frontend-visual-evidence/v1` contract;
see [the migration and owner-gate summary](docs/quality/frontend-visual-gate-migration.md).

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

`SKILL.md` is the portable Agent Skills contract. `agents/openai.yaml` is the only
provider-specific per-Skill surface currently shipped; Anthropic consumes the portable
package directly and does not require a parallel `agents/anthropic.yaml`. Additional
provider adapters are added only for documented machine-readable contracts, not as
copies of the Skill instructions.

Repository-level `docs/`, `protocols/`, and `scripts/` are maintainer surfaces;
published packages do not depend on them at runtime.

`skills-index.json` is the repository-level semantic discovery source for local search
and catalog consistency. It records categories, intents, keywords, exclusions, and
related owners without adding unsupported fields to portable Skill frontmatter.

## Validate

Use the concise command matrix in [`skills/AGENTS.md`](skills/AGENTS.md#validation).
The validator checks the portable Agent Skills package, OpenAI metadata, direct
references, representative eval sections, semantic-index integrity, and catalog
consistency. Exercise behavior changes on a few representative tasks.

```bash
bash scripts/check-skills.sh
```

## Design Principles

- Small, intent-based, and composable, following established public catalog
  practices without embedding a personal source identity.
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
