# Layered Repository Guidance

Use this profile only when the user explicitly requests creating, bootstrapping, or
repairing repository guidance such as `AGENTS.md`. Mapping a repository does not by
itself authorize guidance-file writes.

## Placement Gate

Start with the requested scope and map root. Build a placement matrix before writing:

| Candidate | Create or update when | Keep at parent when |
| --- | --- | --- |
| Map-root `AGENTS.md` | Shared task routing, safety boundaries, workspace structure, or validation entry points are durable and evidence-backed. | An existing effective file already covers the facts accurately. |
| Nested Git root | The child repository has its own effective guidance, commands, ownership, or delivery lifecycle. | The containing repository genuinely owns the files and one rule set applies. |
| Frontend/backend/desktop/CLI/worker subproject | It has an independent manifest plus distinct start/build/test/deploy/runtime or ownership boundaries. | The directory is only an organizational folder or inherits all commands and constraints. |
| Package/crate/module | It has durable local rules that materially differ from its parent and repeatedly change task execution. | The difference is task-local, obvious from one manifest, or better kept in source documentation. |

A directory name is never enough evidence. Confirm boundaries from files such as
workspace manifests, `package.json`, `Cargo.toml`, build/task files, deployment config,
entry points, CI paths, or current ownership documentation. A single repository may
therefore have root guidance plus nearer files such as `apps/web/AGENTS.md` and
`services/api/AGENTS.md`; a simple repository may need only the root file.

## Workflow

1. Resolve the requested scope, map root, containing and nested Git roots, and every
   existing `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, or equivalent host file.
2. Read effective guidance from root to leaf. Record which file currently owns each
   shared or boundary-specific rule and inspect local diffs before editing it.
3. Search manifests and executable command sources. Group candidate directories by
   proven ownership, build, runtime, deploy, and validation boundaries rather than by
   directory shape.
4. Build the placement matrix. For every candidate, record `root`, `nearer file`, or
   `skip`, with the evidence that decides placement.
5. Put only cross-repository rules at the map root: purpose, real project boundaries,
   task-to-owner routing, shared safety constraints, common validation entry points,
   artifact locations, and final reporting expectations.
6. Put only the delta in each nearer file: local working root, manifest/entry points,
   exact install/start/test/lint/typecheck/build commands, generated or protected
   paths, framework-specific conventions, and checks required after local changes.
7. Preserve existing rules and unrelated edits. Repair stale commands or paths from
   their executable source; never replace a file wholesale merely to normalize prose.
8. Re-read the effective root-to-leaf chain for one representative task in each
   selected boundary. Confirm that it reaches the right working root and commands
   without contradiction or needless duplication.
9. Run repository-defined documentation checks and `git diff --check`, then report
   every created, updated, and skipped candidate plus `Not found` or `Not verified`
   gaps.

## File Contract

Use the smallest applicable sections; omit empty or generic filler:

- scope and precedence;
- repository or subproject purpose;
- real working/Git root and owned paths;
- task routing and source-of-truth documents;
- exact commands and runtime/package-manager requirements;
- edit, generated-file, security, and external-action constraints;
- validation required for local change types;
- artifact/handoff locations when the repository defines them;
- final report expectations and explicit `Not verified` boundaries.

Use exact repository-relative paths and commands. Say `Not found` for a missing command
or layer and `Not verified` for an unchecked runtime, deploy, CI, or external claim.
Do not copy personal global preferences, generic programming advice, or the complete
root guidance into a child file.

## Stop Conditions

Stop without writing a candidate when ownership is ambiguous, multiple existing
guidance authorities cannot be reconciled, the target has unsafe overlapping edits,
or the evidence does not justify a durable local rule. Report the completed placement
evidence and the decision needed to continue.
