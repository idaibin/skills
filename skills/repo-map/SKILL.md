---
name: repo-map
description: "Use when the user asks to map current Git or non-Git workspace truth into a durable repo map: real roots and boundaries, architecture, commands, shortest task routes, and verified reusable components, functions, types, or APIs, or to repair stale navigation incrementally."
---

# Repository Map

## Overview

Map stable workspace or repository semantics into a concise navigation layer rooted at `<map-root>/docs/repo-map/README.md`, unless the project already defines an equivalent. The map should let later work reach the correct working root, Git root when present, canonical owner, reusable contract, and verification source without rediscovering the project. Source remains proof; the map is a verified index, not a copied directory tree or substitute for task-time checks. It does not judge changes for defects or declare review readiness.

## Workflow

1. Resolve roots from the requested or current path before reading broadly:
   - keep the requested path as the initial working scope; if `git rev-parse --show-toplevel` succeeds, record the returned path as its containing Git root and map root. Keep one root index at `<map-root>/docs/repo-map/README.md` (or the project-defined equivalent); when step 5 proves an independent boundary, link a scoped sibling page from that index rather than changing storage root or creating a competing map;
   - otherwise use the requested directory as the workspace/map root and search below it for child Git roots by `.git` directory or file markers, pruning dependency, generated, cache, and build-output directories;
   - if child Git roots exist, classify the container as a multi-repo workspace and record each in-scope Git root; for nested or overlapping Git roots, record containment, treat the deepest root as canonical owner of files inside its boundary, and treat an ancestor root as container owner unless current manifests or contracts prove otherwise; if none exist, classify it as an ordinary non-Git directory project and map its real structure and content normally;
   - record map persistence as `versioned` when the artifact belongs to a Git root, otherwise `local-unversioned`. Never reject mapping merely because no Git repository exists.
2. Read effective `AGENTS.md` guidance from the map root and each child Git root actually opened. Run `git status --short` in every applicable Git root before editing a document there; do not run Git commands as if a non-Git container were a repository.
3. Locate the existing repo-map artifact. Prefer a project-defined equivalent; otherwise consider `<map-root>/docs/repo-map/README.md`. If multiple current or legacy candidates exist, inspect their ownership and references, select one authoritative root index, record any migration, and stop for clarification when evidence cannot choose safely; never silently overwrite or create a competing map. If the target artifact is inside Git and already modified, inspect its staged and unstaged diff, preserve unrelated hunks, and stop on an unsafe overlap.
4. Apply the creation gate: create or expand a map only when it will reduce wrong-root routing, repeated semantic discovery, duplicate implementation, or cross-boundary inference. If one directory listing or manifest answers the need, read it directly and keep the map absent or smaller.
5. Classify the scope before reading broadly:
   - workspace map when the primary routing problem is multiple independently governed child Git roots, whether or not their container is itself a Git repository;
   - repository map for a Git root with meaningful module/runtime boundaries;
   - scoped map only for an independently owned, built, deployed, or operationally complex boundary.
   Do not split merely because directories such as `src/`, `src-tauri/`, `frontend/`, or `backend/` exist.
6. Define the questions the map must answer: real boundaries and owners, architecture, command sources, shortest task routes, reusable contracts, cross-boundary relationships, and validation entry points. Treat canonical owner as the definition or contract owner; record build/deploy, runtime/operations, or data/schema ownership only when it changes routing.
7. Search before opening files. Start with manifests/config, entry points, exports/registrations, and the nearest representative implementation. Read only evidence that can change the map.
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
   - known exceptions, high-risk boundaries, and `Not verified` gaps.
10. Before recording or recommending a new declaration, search the map and live source by capability, domain term, symbol, access/registration, endpoint shape, and representative caller. Search the owning root, first-order mapped provider/shared roots, and only transitive roots explicitly named as canonical owners by those contract edges. Stop when no new owner edge is found or an edge is declared external; do not recursively scan unrelated dependencies. Rank multiple candidates by canonical ownership, active compatible consumers, validation evidence, boundary compatibility, and non-deprecated status; if no authoritative candidate remains, return `Not verified` rather than choosing arbitrarily. If an applicable root is unavailable, unchecked, or ambiguously owned, also return `Not verified` and do not approve `new`. Otherwise choose and report `reuse`, `extend`, `wrap`, or justified `new`, and persist only stable owner, boundary, or contract changes.
11. Before relying on an existing entry, verify its canonical definition and access, registration, command, schema, or runtime entry in current source. Treat a semantic mismatch as stale even when every path still resolves, then patch the smallest consistency closure: the changed entry and directly dependent map entries or declared edges reachable from that owner/contract. Stop when no changed dependency edge remains; do not rewrite unrelated sections.
12. When a documented path no longer resolves, repair it incrementally:
   - test the exact path from the documented working directory;
   - if it or its parent is missing, ascend one directory at a time until reaching the nearest existing ancestor;
   - scan downward only from that ancestor and only for the relevant owner;
   - identify moved or renamed targets through basename, owning symbol, manifest/config, route/module registration, generated-source declaration, or history when still ambiguous;
   - patch only the stale path, table row, or affected section and preserve verified sections.
13. Rebuild the whole repo-map artifact only when it is missing, corrupt, structurally unusable, or the user explicitly requests a rebuild.
14. Stop when each selected common task reaches the correct working/Git root through the minimum decisive evidence chain, normally 1-8 unique entries per task. Reuse shared entries across tasks; exceed eight only when distinct required ownership or runtime boundaries cannot be represented safely with fewer entries, and record the reason. Mark unchecked areas `Not verified`.
15. Run project-defined documentation or skill checks that match the edit, then verify the final diff contains only intended changes.

## Modes

- **Repo map:** create the smallest useful workspace, repository, or scoped navigation artifact.
- **Targeted update:** add or refresh one architecture, command, ownership, component, or interface area.
- **Reuse inventory:** map the shortest chain to existing reusable or reference implementations before new development.
- **Navigation repair:** recover stale documented paths by ascending to the nearest existing ancestor and repairing only affected entries.

## Do Not Use For

- Ordinary implementation when no separate repo-map deliverable was requested; implementation skills perform their own bounded discovery and live reuse search.
- Local diff readiness or immutable snapshot/range/PR/release review; use the matching `repo-review` basis mode.
- Future implementation planning; use `code-planner`.
- Root-cause investigation of a concrete failure; use `diagnose`.

## Hard Rules

- Project files, configs, commands, and effective guidance are the source of truth.
- Use exact map-root-relative paths and state the working root plus every relevant Git root when ambiguity is possible.
- Prefer the shortest accurate reading path over a complete file inventory.
- Do not mirror the source directory structure, enumerate every leaf file/function/API, or store transient branch, dirty-tree, local-environment, or runtime status.
- Do not recommend a new component, function, endpoint, service, repository, trait, DTO, hook, composable, store, or helper before verifying the nearest reusable or reference implementation in live source.
- Treat the reuse index as high-value navigation, not an exhaustive symbol catalog. Include explicit shared contracts or proven reusable candidates; keep leaf-local details in source.
- Never treat a map miss as proof that no implementation exists. Record the live search scope before allowing a new declaration.
- Say `Not found` for missing items and `Not verified` for unchecked or runtime claims.
- Keep current truth separate from history, plans, and aspirational architecture.
- Repair stale navigation locally. Never rebuild the whole document merely because one path or parent directory disappeared.
- Preserve unrelated local changes.
- Do not produce P0-P3 findings or claim review approval.

## Output Contract

Report the repo-map path, initial working scope, scope class, map root, discovered Git roots and containment, persistence state, relevant worktree state, sections created or updated, and validation performed. Summarize task routes, reuse decisions and canonical entries, duplicate-declaration risks avoided, semantic or path repairs, preserved sections, and remaining `Not found` or `Not verified` gaps. For stopped or partial execution, also report the stop reason, completed evidence chain, unresolved boundary, artifact state, and required follow-up. Do not duplicate the full map in chat.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, `references/checklist.md`, `references/reuse-index.md`, `references/prompt-templates.md`, and `agents/openai.yaml` when their contract changes. In AICraft, run `python3 scripts/validate-skills.py --skill repo-map` before publishing.

## References

- See [references/usage.md](references/usage.md) for routing and examples.
- See [references/checklist.md](references/checklist.md) for evidence and incremental repair details.
- See [references/reuse-index.md](references/reuse-index.md) when mapping components, functions, types, or APIs and deciding whether a new declaration is justified.
- See [references/prompt-templates.md](references/prompt-templates.md) for the repo-map structure.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
