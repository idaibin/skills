# Repository Graph Operation Gates

Read this reference for every snapshot build/refresh and graph query.

## Basis And Scope

- Require a compatible graph runtime and freeze repository identity, basis, scope,
  exclusions, extractor versions, and coverage denominator before execution.
- Resolve symbolic roots to contained repository-relative paths; reject absolute,
  parent, and symlink escape. Keep run-local cache outside and excluded from the scan.
- If root ownership or bounded source resolution is ambiguous, stop this baseline gate
  and load `checklist.md` before continuing.

## Snapshot Gate

Validate schema/version, path containment, stable-ID uniqueness, edge endpoints,
authority uniqueness, hashes, coverage arithmetic, exclusions, unresolved/conflict
records, stale identities, and tombstones. A successful scan proves only its declared
basis, scope, and extractor coverage.

## Query Gate

Require a compatible validated snapshot and bind the query to its immutable identity.
Return only requested owners, relations, consumers, impact, conflicts, drift, or
coverage. A miss is `Not found in this snapshot`, never repository-wide absence.

## Output

Return operation/capability version, repository and basis identity, scope/exclusions,
snapshot/query ID, extractor coverage, validation result, unresolved/conflict/stale
state, and every `Not verified` boundary.
