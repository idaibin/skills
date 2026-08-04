# Prompt Templates

These templates are bundled with `repo-map` so the Skill remains usable after
publishing. Do not resolve templates outside this package at runtime.

## Contents

- [Template Selection](#template-selection)
- [Repo Map Bootstrap](#repo-map-bootstrap-template)
- [Doc/Code Alignment Review](#doccode-alignment-review-template)

## Template Selection

- Missing effective repository guidance: load the directly linked layered repository-guidance profile from `SKILL.md` when the user explicitly requests creating or repairing it.
- Missing `docs/repo-map/README.md`: apply the creation gate, then use the repo-map bootstrap template when justified.
- Existing docs present: use the doc/code alignment review template.

Templates provide structure only. Repository files, configs, commands, and code are the source of truth.

## Repo Map Bootstrap Template

Use for `docs/repo-map/README.md` or an equivalent context map. Keep one `README.md` as the authoritative root index at the selected map root. Add linked sibling scoped pages only for independently owned, built, deployed, or operationally complex boundaries; do not change storage root for a scoped request or mirror source directories. If multiple current/legacy candidates cannot be reconciled from ownership and references, stop for clarification.

Required sections:

- Repository purpose and project boundaries
- Scope class: workspace, repository, or scoped boundary
- Initial working scope, map root, and containing/child Git roots
- Tech stack
- Install, start, test, lint, typecheck, and build commands
- Runtime and package manager requirements
- Build authority, runtime/toolchain source, internal module edges, and critical
  direct dependency routes
- Directory structure
- Typical file chain for page, API, backend, CLI, or worker changes
- Components, services, state, styles, tests, and config locations
- Verified reusable pages, layouts, components, functions, hooks, services, and shared UI relevant to common tasks
- Existing Rust/API routes, handlers, services, repositories, traits/types, DTOs, errors, migrations, callers, and tests relevant to common tasks
- Reference implementations, naming/placement patterns, and new-file decision rule
- Reuse index entries with canonical owner, access or registration entry, actual visibility, representative consumers, boundary, and evidence
- Cross-boundary contracts and generated-source ownership
- Frequent edit areas
- High-risk areas
- Recommended reading order for new tasks

For each common task type, prefer a short ordered reading path over a broad inventory. Point to the owning manifest/config, entry or registration, reusable contract, representative caller, and matching test only when each hop is useful.

When Maven, Gradle, or JVM source sets are present, apply
`java-build-and-dependency-map.md`. Record the owning build root, Wrapper or verified
command source, JDK evidence, module roles and declared internal edges, dependency
management authority, executable entry points, configuration ownership, and only the
external dependencies that change routing. Do not copy dependency trees or
configuration values.

Stop when each mapped common task reaches the correct working/Git root through the minimum decisive chain, normally 1-8 unique entries per task. Reuse shared entries; exceed eight only for distinct required boundaries and record the reason. Omit any section that merely repeats a directory listing or manifest.

Hard requirements:

- Use grouped path tables when that is clearer than prose.
- Separate current truth from historical docs or plans.
- Mark unchecked items as `Not verified`.
- Do not invent commands.
- Preserve the requested path as initial working scope and resolve its containing Git root. For a non-Git container, discover child Git roots; when none exist, map the ordinary directory project normally and mark the artifact `local-unversioned`. Record nested-root containment and default file ownership to the deepest Git root unless current evidence overrides it.
- When updating an existing map, patch only evidence-backed stale sections. If a path is gone, ascend to the nearest existing ancestor, rescan the relevant subtree, and preserve verified sections.
- Treat still-resolving entries as stale when their definition, access/registration, command, schema, owner, or runtime role changed; update dependent routes and edges in the same consistency closure.

## Doc/Code Alignment Review Template

Use when context docs already exist.

Review against:

- manifests and lockfiles
- command sources such as `package.json`, `justfile`, `Makefile`, or CI configs
- workspace membership and package boundaries
- source entry points, routes, modules, services, and tests
- current repo guidance files
- repository-defined project class, directory, naming, reuse, and structural lifecycle rules

Classify findings:

- stale: old paths, commands, package managers, or architecture
- missing: important current commands, paths, constraints, or risks are absent
- incorrect: docs contradict code or config
- duplicated: command truth is repeated in multiple docs and likely to drift
- structural drift: manifests, exports, commands, tests, CI/deploy paths, architecture docs, or indexes disagree after add/reuse/move/delete work
- unverifiable: claim could not be checked from current repo evidence

Output:

- findings first, ordered by impact
- exact doc file or section when possible
- suggested replacement wording when useful
- validation performed and remaining `Not verified` items
