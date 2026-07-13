# Repository Map Checklist

## Evidence Order

1. Keep the requested path as the initial working scope and resolve its containing Git root. If none exists, keep the requested directory as map root and discover child Git roots; if none exist, classify it as an ordinary non-Git directory project. Record nested-root containment and canonical ownership.
2. Record `versioned` or `local-unversioned`, read effective `AGENTS.md`, and run `git status --short` only in applicable Git roots.
3. Locate the existing map or consider `<map-root>/docs/repo-map/README.md`; choose one authoritative root index, record legacy migration, stop on unresolved competing candidates, and inspect target diffs before editing.
4. Apply the creation gate and classify workspace, repository, or scoped-map level.
5. List the exact navigation questions the map must answer.
6. Search manifests/config, entry points, registrations, and representative implementations before opening broad docs or directories.
7. Read only the owning app/package and directly relevant shared/provider boundaries.
8. Verify commands from executable sources such as manifests, task files, and CI config.
9. Verify reusable contracts through definitions, access/registration entries, representative callers, and tests where needed.
10. Update only sections whose evidence was checked and verify the final diff preserves unrelated hunks.

## Required Repo-Map Content

- Repository purpose and real project boundaries
- Directory structure with ownership, not an exhaustive file tree
- Technical architecture and runtime/deployment boundaries
- Runtime and package-manager requirements
- Install, start, test, lint, typecheck, and build commands
- Effective repository conventions and source documents
- Shortest reading order for common task types
- Typical page, API, backend, CLI, or worker change chains
- Verified reuse index for components, functions/helpers, hooks/composables, stores, services, endpoints, routes, handlers, repositories, traits/types/DTOs, and reference implementations
- Canonical definition, access or registration entry with actual visibility, representative consumers, reuse boundary, and verification evidence for each indexed contract
- Cross-boundary contracts including API clients, generated code, IPC, events, persistence, exports, and deployment edges when applicable
- Naming/placement patterns and the gate for creating new files or contracts
- Frequent edit areas, protected/high-risk areas, exceptions, and `Not verified` gaps

Do not include content obtainable from one directory listing, an exhaustive symbol catalog, or transient Git/local/runtime status.

## Incremental Navigation Repair

Treat an entry as stale when its path fails or when its definition, access/registration, command, schema, owner, or runtime role no longer matches current source. For semantic drift, patch the entry plus directly dependent map entries or declared edges reachable from that owner/contract, stopping when no changed dependency edge remains. When a documented path fails:

1. Resolve it from the documented or repository root.
2. Check the exact path and its immediate parent.
3. If the parent is absent, ascend one directory at a time until the nearest existing ancestor is found.
4. Search downward only from that ancestor for the missing basename, owning symbol, manifest/config registration, route/module registration, or generated source.
5. Use history only if current evidence cannot distinguish move, rename, deletion, generation, or branch drift.
6. Update the smallest stale unit: path, row, command, diagram edge, or section.
7. Recheck links and nearby references affected by the same move.
8. Preserve every still-verified section.

Rebuild the entire document only if it is missing, corrupt, structurally unusable, or explicitly requested.

## Reporting

- Document path and repository root
- Sections created, refreshed, or repaired
- Exact old and new paths for repairs
- Nearest existing ancestor used for a bounded rescan
- Shortest reading paths and reuse entry points
- Preserved sections and intentionally unchecked areas
- Checks run, failures, `Not found`, and `Not verified`
- For partial or stopped work: stop reason, completed evidence chain, unresolved boundary, artifact state, and required follow-up
