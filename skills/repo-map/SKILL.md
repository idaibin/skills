---
name: repo-map
description: "Use when current Git or non-Git workspace truth needs a durable map of roots, ownership, architecture, commands, dependency routes, reusable contracts, Maven/Gradle Java boundaries, or layered AGENTS.md guidance at real root and subproject boundaries, or when an existing map or guidance file needs evidence-based repair; do not use for ordinary task-local discovery or change review."
---

# Repository Map

## Overview

Map stable workspace or repository semantics into either a concise navigation layer rooted at `<map-root>/docs/repo-map/README.md`, unless the project already defines an equivalent, or explicitly requested layered repository guidance in `AGENTS.md`. A map should let later work reach the correct working root, Git root when present, canonical owner, reusable contract, protocol authority, generated consumer, and verification source without rediscovering the project. Layered guidance should put shared rules at the map root and narrower commands or constraints at independently owned subproject boundaries. Source remains proof; neither artifact substitutes for task-time checks or judges changes for defects.

## Workflow

1. Resolve the requested scope, containing Git root, child/nested Git roots, map root, and `versioned` or `local-unversioned` persistence before reading broadly. Keep the deepest Git root as file owner unless current manifests prove otherwise; non-Git projects remain valid map targets. Use the root-resolution procedure in `references/checklist.md` only when boundaries are ambiguous.
2. Read effective repository guidance from the map root and each child Git root actually opened, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present. Run `git status --short` in every applicable Git root before editing a document there; do not run Git commands as if a non-Git container were a repository.
3. Select the requested artifact. For a repo map, locate the existing project-defined equivalent or consider `<map-root>/docs/repo-map/README.md`; reconcile competing candidates and federated specialist maps without copying their detail. For explicitly requested repository-guidance creation or repair, load `references/project-guidance.md`, follow its placement gate and workflow through artifact validation, then resume at step 15; do not also create a repo map unless requested. If any target artifact is already modified, inspect its staged and unstaged diff, preserve unrelated hunks, and stop on an unsafe overlap.
4. For repo-map artifacts, apply the creation gate: create or expand a map only when it will reduce wrong-root routing, repeated semantic discovery, duplicate implementation, or cross-boundary inference. If one directory listing or manifest answers the need, read it directly and keep the map absent or smaller.
5. Select workspace, repository, or scoped level from real ownership, build, deploy, or runtime boundaries; never split from directory names alone.
6. Define the questions the map must answer: real boundaries and owners, architecture, command sources, shortest task routes, reusable contracts, cross-boundary relationships, and validation entry points. When product positioning changes task routing, link the smallest verified product-fact authority set without restating or deciding product behavior. Treat canonical owner as the definition or contract owner; record build/deploy, runtime/operations, or data/schema ownership only when it changes routing. When the user supplies an external project or framework as a design reference, use it to identify candidate architecture, documentation, and validation questions, then retain only conclusions verified against the target repository; never turn the reference into a target-repository authority or a framework-specific execution branch.
7. Search before opening files. Start with manifests/config, entry points, exports/registrations, and the nearest representative implementation. Read only evidence that can change the map. When Maven, Gradle, or JVM source-set evidence appears, load `references/java-build-and-dependency-map.md` and resolve the owning build root, JDK source, module graph, and critical dependency routes without dumping the full dependency tree.
8. For monorepos or multi-repo workspaces, map the routing boundary first, then only the owning child repository or package needed. Do not scan every child by default.
9. Write or update the repo-map artifact with:
   - current directory and ownership map;
   - technical architecture and runtime boundaries;
   - install, start, test, lint, typecheck, and build commands from their real sources;
   - repository-specific conventions and effective guidance;
   - shortest reading path for common task types;
   - a verified reuse index for shared components, functions/helpers, hooks/composables, stores, services, API clients/endpoints, routes, handlers, repositories, traits/types/DTOs, and reference implementations;
   - each reusable entry's canonical owner/definition, access or registration entry with actual visibility, representative real consumers, usage boundary, and live verification source;
   - cross-boundary contracts such as frontend-to-API, Tauri IPC, package exports, generated clients, events, persistence, and deployment edges;
   - a bounded dependency map covering internal owner-to-consumer edges and only those external platforms, BOMs, frameworks, stores, transports, generators, or build plugins that change build, runtime, contract, deployment, or task routing;
   - known exceptions, high-risk boundaries, and `Not verified` gaps.
   For reusable UI components, record the product/design term, visual cue or
   semantic job, canonical path and symbol, export/registration path, owning
   provider root, representative consumers, states/variants, reuse boundary,
   and current-source evidence. When the repository adopts root `DESIGN.md`,
   also record its exact map-root-relative path plus anchor or semantic binding;
   do not copy token values or design rules. Keep this a high-value index, not a
   catalog. Load `references/frontend-inventory.md` only for a requested frontend
   inventory or code-context index.
   For a requested HTTP API inventory, use `references/api-contract-map.md`. Record
   the repository-native authority/consumer chain and only existing or explicitly
   requested generated artifacts; do not introduce or copy schemas.
10. Before recommending a new declaration, search bounded live source through explicit owner/provider edges, rank current candidates, and report `reuse`, `extend`, `wrap`, justified `new`, or `Not verified`. Do not scan unrelated dependency graphs or persist task-local choices.
11. Revalidate an entry's current definition, access/registration, command, schema, and runtime role before use. Repair only the changed entry and directly dependent declared edges.
12. Repair stale paths only inside their recorded owner/provider root. If that root is absent, mark stale and restart bounded live discovery from newly proven ownership. Git history may explain only a move already proven by current source; see `references/checklist.md` for the bounded repair procedure.
13. Rebuild the whole repo-map artifact only when it is missing, corrupt, structurally unusable, or the user explicitly requests a rebuild.
14. Stop when each selected common task reaches the correct working/Git root through the minimum decisive evidence chain, normally 1-8 unique entries per task. Reuse shared entries across tasks; exceed eight only when distinct required ownership or runtime boundaries cannot be represented safely with fewer entries, and record the reason. Mark unchecked areas `Not verified`.
15. Run project-defined documentation or skill checks that match the edit, then verify the final diff contains only intended changes.

## Modes

- **Repo map:** create the smallest useful workspace, repository, or scoped navigation artifact.
- **Project guidance baseline:** create or repair explicitly requested layered `AGENTS.md` files at the map root and at independently owned frontend, backend, desktop, CLI, worker, or other subproject boundaries; load `references/project-guidance.md`.
- **Targeted update:** add or refresh one architecture, command, ownership, component, or interface area.
- **Reuse inventory:** map the shortest chain to existing reusable or reference implementations before new development.
- **Frontend inventory profile (on demand):** index only the routes/pages,
  components, hooks/state, API, styles, and design bindings that materially guide
  a requested frontend surface. It is a reference for later work, not a required
  implementation phase.
- **API Contract Map profile:** record a bounded native or generated authority/consumer chain and its available checks.
- **Navigation repair:** recover stale documented paths by ascending to the nearest existing ancestor and repairing only affected entries.

## Do Not Use For

- Ordinary implementation when no separate repo-map deliverable was requested; implementation skills perform their own bounded discovery and live reuse search.
- Local diff readiness or fixed immutable review; use `repo-review` with Worktree/index, resolved SHA/range (including PR base/head), or verified package basis, plus the conditional Release profile when applicable.
- Future implementation planning; use the host's built-in planning.
- Generic policy generation with no current repository evidence or no explicit request to create or update repository guidance.
- Root-cause investigation of a concrete failure; use the host's built-in diagnosis under effective instructions.

## Hard Rules

- Project files, configs, commands, and effective guidance are the source of truth.
- Treat external example repositories and framework documentation as comparative
  design input only. Separate adopted current-source facts from proposed patterns and
  rejected differences; do not copy their directory layout, commands, dependencies,
  or conventions into the target map without target-repository evidence.
- Use exact map-root-relative paths and state the working root plus every relevant Git root when ambiguity is possible.
- Prefer the shortest accurate reading path over a complete file inventory.
- Keep one root navigation authority while allowing verified specialist maps to own
  bounded detail. Do not duplicate their rows, tokens, schemas, or component
  inventories into the root map.
- Keep root and subproject guidance layered: root `AGENTS.md` owns shared rules and
  task routing; a nearer file owns only commands, paths, checks, and constraints that
  differ for its proven boundary. Do not duplicate the root file into every directory.
- Do not infer a subproject boundary from names such as `frontend`, `backend`, `src`,
  or `apps` alone. Require evidence such as an independent manifest, build/start/test
  surface, deploy/runtime unit, nested Git root, or explicit ownership boundary.
- Never overwrite an existing guidance file wholesale. Preserve its effective rules,
  inspect local diffs, and patch only evidence-backed gaps or stale statements.
- Do not mirror the source directory structure, enumerate every leaf file/function/API, or store transient branch, dirty-tree, local-environment, or runtime status.
- Do not copy a lockfile, dependency tree, effective build model, repository credentials,
  or application configuration values into the map. Record manifest authorities,
  direct routing-relevant edges, configuration ownership, and verification commands;
  mark unresolved remote configuration or transitive behavior `Not verified`.
- Do not generate or copy an executable API schema into the map. Record authority,
  paths, symbols, commands, consumers, and evidence references only.
- Do not recommend a new component, function, endpoint, service, repository, trait, DTO, hook, composable, store, or helper before verifying the nearest reusable or reference implementation in live source.
- Treat the reuse index as high-value navigation, not an exhaustive symbol catalog. Include explicit shared contracts or proven reusable candidates; keep leaf-local details in source.
- Prefer verified existing components during implementation, but do not make a
  repo map or Component Map a mandatory implementation prerequisite.
- A frontend inventory or code-context index is selective navigation. Its absence
  or a map miss never proves that a route, component, style, hook, state owner,
  API client, or design binding does not exist; perform bounded live discovery.
- Never treat a map miss as proof that no implementation exists. Record the live search scope before allowing a new declaration.
- Say `Not found` for missing items and `Not verified` for unchecked or runtime claims.
- Keep current truth separate from history, plans, and aspirational architecture.
- Repair stale navigation locally. Never rebuild the whole document merely because one path or parent directory disappeared.
- Never ascend or search outside a recorded owner/provider root to rescue a stale
  component entry. If that root no longer exists, mark the entry stale and use a
  fresh bounded live search with newly proven ownership.
- Use Git history only as corroboration for a current-source-proven move or rename;
  historical definitions and consumers do not prove current reusability.
- Preserve unrelated local changes.
- Do not produce P0-P3 findings or claim review approval.

## Output Contract

Report every created or updated repo-map or guidance path, initial working scope, scope class, map root, discovered Git roots and containment, persistence state, relevant worktree state, sections created or updated, and validation performed. For layered guidance, include the placement decision for each root/subproject candidate and why a nearer file was created or skipped. Summarize task routes, reuse decisions and canonical entries, duplicate-declaration risks avoided, semantic or path repairs, preserved sections, and remaining `Not found` or `Not verified` gaps. For stopped or partial execution, also report the stop reason, completed evidence chain, unresolved boundary, artifact state, and required follow-up. Do not duplicate full artifacts in chat.

## References

- See [references/usage.md](references/usage.md) for routing and examples.
- See [references/checklist.md](references/checklist.md) for evidence and incremental repair details.
- See [references/reuse-index.md](references/reuse-index.md) when mapping components, functions, types, or APIs and deciding whether a new declaration is justified.
- See [references/frontend-inventory.md](references/frontend-inventory.md) only
  for a requested frontend inventory or code-context index.
- See [references/api-contract-map.md](references/api-contract-map.md) only for a requested HTTP authority/consumer map.
- Read [references/java-build-and-dependency-map.md](references/java-build-and-dependency-map.md) when Maven, Gradle, or JVM source-set evidence appears.
- See [references/project-guidance.md](references/project-guidance.md) only for explicitly requested root or layered subproject `AGENTS.md` creation or repair.
- See [references/prompt-templates.md](references/prompt-templates.md) for the repo-map structure.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
