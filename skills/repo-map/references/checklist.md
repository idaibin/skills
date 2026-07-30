# Repository Map Checklist

## Evidence Order

1. Keep the requested path as the initial working scope and resolve its containing Git root. If none exists, keep the requested directory as map root and discover child Git roots; if none exist, classify it as an ordinary non-Git directory project. Record nested-root containment and canonical ownership.
2. Record `versioned` or `local-unversioned`, read effective repository guidance (`AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present), and run `git status --short` only in applicable Git roots.
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
- Build and dependency authorities: owning manifests, runtime/toolchain source,
  internal module edges, and routing-relevant direct external dependencies; for a
  Java/JVM project, apply `java-build-and-dependency-map.md`
- Runtime and package-manager requirements
- Install, start, test, lint, typecheck, and build commands
- Effective repository conventions and source documents
- Shortest reading order for common task types
- Links to verified specialist maps with their ownership boundary and live source
  revalidation path; summarize only the routing facts needed at the root
- Typical page, API, backend, CLI, or worker change chains
- Verified reuse index for components, functions/helpers, hooks/composables, stores, services, endpoints, routes, handlers, repositories, traits/types/DTOs, and reference implementations
- For reusable UI components: product/design term, visual cue or semantic job,
  canonical path, symbol, export/registration path, owner/provider root,
  representative consumers, states/variants, reuse boundary, and current-source evidence
- For other indexed contracts: canonical definition, access or registration
  entry with actual visibility, owner/provider root, representative consumers,
  reuse boundary, and current-source evidence
- Cross-boundary contracts including API clients, generated code, IPC, events, persistence, exports, and deployment edges when applicable
- For a requested API Contract Map: native authority/path, registration,
  request/success/error/auth owners, client and representative consumers,
  duplicate-DTO boundary, checks, and `Not verified` results. Include normalized
  OpenAPI/generator/generated client only for an existing or explicitly introduced
  pipeline; otherwise record them `Not applicable`.
- Naming/placement patterns and the gate for creating new files or contracts
- Frequent edit areas, protected/high-risk areas, exceptions, and `Not verified` gaps

Do not include content obtainable from one directory listing, an exhaustive symbol or
dependency catalog, configuration values, credentials, or transient Git/local/runtime
status.
Do not flatten specialist maps into the root index. If a UI component map, API
contract map, deployment map, or similar artifact already owns bounded detail,
verify it, link it, and keep the root entry to authority, purpose, and reading order.

## Incremental Navigation Repair

Treat an entry as stale when its path fails or when its definition, access/registration, command, schema, owner, or runtime role no longer matches current source. For semantic drift, patch the entry plus directly dependent map entries or declared edges reachable from that owner/contract, stopping when no changed dependency edge remains. When a documented path fails:

1. Resolve it from the documented or repository root.
2. Check the exact path and its immediate parent.
3. If the parent is absent, ascend one directory at a time only within the
   recorded owner/provider root and stop at that root.
4. Search downward only from that ancestor for the missing basename, owning
   symbol, manifest/config registration, route/module registration, or generated source.
5. If the root itself is absent, mark stale and return to ordinary bounded live
   discovery; never cross the old root boundary.
6. Use history only to explain a move/rename already proven in current source;
   never use historical definitions or consumers as current reuse evidence.
7. Update the smallest stale unit: path, row, command, diagram edge, or section.
8. Recheck links and nearby references affected by the same move.
9. Preserve every still-verified section.

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
