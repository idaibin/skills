# Repository Map

## Summary

Create or maintain a durable semantic repo map from current source truth. It should reduce wrong-root routing, repeated discovery, duplicate declarations, and cross-boundary guesswork.

## Best For

- Initial `docs/project-map.md` or repository-equivalent creation
- Explicitly requested root and subproject `AGENTS.md` bootstrapping from proven
  workspace, frontend, backend, desktop, CLI, worker, or nested-repository boundaries
- Workspace routing across multiple child Git roots
- Ordinary non-Git directory projects with no containing or child Git repository
- Directory ownership and technical architecture mapping
- Maven/Gradle build roots, Java runtime/toolchain evidence, module roles, and bounded
  dependency routing
- Real command, runtime, and repository-convention documentation
- Shortest reading paths for common frontend, API, backend, CLI, or worker tasks
- Verified component, function, service, API client, route, handler, trait, type, or DTO reuse inventories
- Bounded API Contract Maps that connect native authority, client, consumers,
  duplicate-DTO ownership, and checks; add normalized OpenAPI/generated clients only
  for an existing or explicitly introduced pipeline
- Reuse/extend/wrap/new decisions before adding another contract
- Incremental repair when documented paths or parent directories have moved or disappeared

## Triggers

- `Map the current project's directory structure and technical architecture into the repo map.`
- `Map this Java workspace's Maven and Gradle roots, JDK requirements, module roles, critical dependency routes, and executable services without copying full dependency trees.`
- `Organize the real commands, standards, components, and interface entry points into navigation for later development.`
- `Identify the shortest set of directories and components to read before developing this page.`
- `Update the APIs and reusable components in the repo map.`
- `Verify and record this service's single OpenAPI authority, generation chain, frontend consumers, and duplicate-DTO boundary.`
- `The documented directory is missing; scan locally from the nearest existing ancestor and repair the map.`
- `Create or update docs/project-map.md from current repository truth.`
- `Create root guidance and nearer AGENTS.md files for independently built frontend and backend subprojects.`
- `The current directory is not a Git repository; check for child repositories, or map it as an ordinary project if none exist.`

Do not use for generic implementation, local dirty-tree review, immutable repository/range/PR review, or defect diagnosis. Use the matching Worktree or immutable basis mode in `repo-review` for review.

## Output

Expect updated repo-map or guidance paths plus a compact summary of initial working scope, map root, discovered Git roots and containment, `versioned` or `local-unversioned` persistence, scope level, changed sections, shortest task routes, verified reuse entries and decisions, mapped protocol authority/derived-consumer chain when requested, root/subproject guidance placement decisions, semantic/path repairs, preserved sections, validation, and `Not found` or `Not verified` gaps. Partial work also reports its stop reason, completed evidence, unresolved boundary, artifact state, and follow-up.
