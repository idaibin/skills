# Project Baseline And Lifecycle

## Contents

- [Classify The Rule Before Applying It](#classify-the-rule-before-applying-it)
- [Toolchain Baseline](#toolchain-baseline)
- [Structure And Feature Mapping](#structure-and-feature-mapping)
- [Reuse-First Discovery](#reuse-first-discovery)
- [Structural Lifecycle](#structural-lifecycle)
- [New And Established Projects](#new-and-established-projects)
- [Automation](#automation)

## Classify The Rule Before Applying It

Separate every proposed standard into one of these classes:

| Class | Meaning | Application |
| --- | --- | --- |
| Portable governance | evidence, ownership, lifecycle, validation, and scope rules | apply unless a higher-priority repository rule conflicts |
| Organization baseline | adopted toolchain, naming, commands, or documentation policy | apply only to repositories within that declared scope |
| New-project template | recommended starting structure and pinned versions | use for new projects after explicit selection |
| Repository contract | current manifests, code, docs, CI, deployment, and interfaces | treat as the local source of truth |
| Legacy exception | documented production structure retained for compatibility or migration cost | preserve until an in-scope change justifies migration |

Do not present a local baseline as a Rust or Cargo mandate. Record the source,
scope, adoption date or version, exceptions, and verification owner.

## Toolchain Baseline

Inspect `rust-toolchain*`, root and member manifests, CI images/actions,
packaging, deployment targets, and contributor docs before recommending:

- stable, beta, nightly, or a pinned toolchain
- edition and workspace resolver
- package `rust-version` and MSRV policy
- formatter and Clippy configuration
- workspace package, dependency, and lint inheritance
- supported targets, native libraries, and feature combinations

For a new project, edition 2024 and resolver 3 are reasonable current defaults
when supported by the chosen toolchain. Do not embed a moving “latest stable” or
universal MSRV into this skill. Choose a repository policy such as pinned stable,
latest stable, or an explicit release-window policy, then verify it in CI.

Workspace declarations do not automatically govern every member. Confirm that
members opt into inherited package fields, dependencies, and lints where Cargo
requires it. Detect unused workspace declarations rather than assuming adoption.

Do not enable all Clippy pedantic or restriction lints universally. Start from
the repository's lint policy, justify additions, and account for MSRV and
false-positive cost.

## Structure And Feature Mapping

Treat directory trees as templates, not universal architecture. `apps/`,
`crates/`, `domain/`, `application/`, `infrastructure/`, and `interface/` can be
useful when they match real ownership, but must not create forwarding layers or
duplicate existing conventions.

Do not force frontend and backend directories to mirror each other physically.
Maintain a logical feature map when a capability crosses boundaries:

```text
feature
→ Rust/domain owner
→ transport or command owner
→ frontend owner when present
→ schema or migration owner
→ tests
→ architecture or feature documentation
```

Keep the map in existing repository guidance (`AGENTS.md`, `CLAUDE.md`, or a
host-provided equivalent), project map, architecture docs, or feature index. Do
not invent a second index when one exists.

Names such as `common`, `utils`, `helper`, `manager`, or `service` are review
signals, not automatic violations. Check whether the module has a narrow stable
responsibility, real consumers, and a clear owner; reject only ambiguous junk
drawers or ceremonial forwarding layers.

## Reuse-First Discovery

Before adding a feature, API, crate, module, trait, command, migration, or helper:

1. Read the current project/architecture map and nearest guidance.
2. Search analogous types, handlers, commands, services, storage paths,
   migrations, tests, and docs.
3. Decide in order: reuse directly, extend or compose, adapt the nearest pattern,
   or create a justified new boundary.
4. Record why existing candidates are insufficient when creating a new owner.

## Structural Lifecycle

For every structural operation, update the full affected chain:

| Operation | Required checks |
| --- | --- |
| Add | owner, manifest/member, registration, feature flag, public export, config, tests, migration/schema, docs/index, packaging/deployment |
| Reuse or extend | existing contract, compatibility, all consumers, tests, docs, whether a new abstraction is actually needed |
| Move or rename | imports, re-exports, module declarations, Cargo paths, command/route registration, generated files, docs, scripts, deployment paths, stale-name search |
| Delete | callers, registrations, features, permissions, config, migrations/data compatibility, tests/fixtures, docs/indexes, packaging, generated artifacts |

Do not delete historical migrations that existing installations may still need.
Do not remove persisted data or compatibility paths without an explicit migration
and recovery decision.

## New And Established Projects

- Apply an adopted template strictly to new projects when it reduces choice and
  the organization owns its maintenance.
- Keep established production layouts as explicit exceptions when renaming would
  create broad import churn, packaging risk, or unclear value.
- Migrate incrementally when a real feature, dependency, ownership, or deployment
  change crosses the relevant boundary.
- Preserve history and behavior; visual directory consistency alone is not a
  sufficient migration benefit.

## Automation

Automate only deterministic, adopted rules: toolchain/edition policy, manifest
inheritance, required commands, forbidden stale paths, generated-file freshness,
and documentation/index consistency. Keep architecture judgments review-based;
CI should not enforce one universal directory tree or infer ownership from names
alone.
