# Prompt Templates

These templates are bundled with `repo-map` so the skill remains usable after publishing. Local `prompts/` files may supplement these templates, but they are never required.

## Template Selection

- Missing `AGENTS.md`: use the AGENTS.md bootstrap template.
- Missing `docs/repo-map/README.md`: apply the creation gate, then use the repo-map bootstrap template when justified.
- Existing docs present: use the doc/code alignment review template.
- New task before edits: use the task-start context template.

Templates provide structure only. Repository files, configs, commands, and code are the source of truth.

## AGENTS.md Bootstrap Template

Use after reading real project files. Preview the draft unless the user already explicitly requested creating or updating the file.

Required sections:

- Repository purpose
- Directory structure
- Working rules
- Code change constraints
- Required checks after changes
- Final report format
- Disallowed actions

Hard requirements:

- Use real paths and real command names.
- Write `Not found` for missing layers or commands.
- Keep rules specific to the repository.
- Do not include generic best-practice filler.
- Do not write after an unapproved preview unless the user already explicitly requested implementation.

## Repo Map Bootstrap Template

Use for `docs/repo-map/README.md` or an equivalent context map. Keep one `README.md` as the authoritative root index at the selected map root. Add linked sibling scoped pages only for independently owned, built, deployed, or operationally complex boundaries; do not change storage root for a scoped request or mirror source directories. If multiple current/legacy candidates cannot be reconciled from ownership and references, stop for clarification.

Required sections:

- Repository purpose and project boundaries
- Scope class: workspace, repository, or scoped boundary
- Initial working scope, map root, and containing/child Git roots
- Tech stack
- Install, start, test, lint, typecheck, and build commands
- Runtime and package manager requirements
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

## Task-Start Context Template

Use when the user is about to start implementation in a repo.

Required first pass:

- read relevant `AGENTS.md`
- inspect related docs and code
- resolve the containing Git root or classify the path as a multi-repo/non-Git workspace; run `git status --short` only in applicable Git roots
- identify allowed and disallowed edit scope
- identify existing commands needed for verification
- inventory relevant existing implementations before proposing a new page, component, endpoint, handler, service, repository, trait, type/DTO, hook, or helper

Output:

- current context in one short paragraph
- proposed edit boundary
- `reuse`, `extend`, `wrap`, or `new` decision with the canonical candidate; for `new`, include checked scope and justification
- verification commands to run after changes
- risks or blockers before editing
