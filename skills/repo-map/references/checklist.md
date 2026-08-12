# Repository Asset Graph Checklist

Use this checklist only when root ownership or bounded source resolution is ambiguous.

## Root And Basis Resolution

1. Keep the requested path as the initial scope and resolve its containing Git root.
   If none exists, keep it as the repository root and discover only directly contained
   child Git roots relevant to the request.
2. Assign a file to the deepest containing Git root unless a current manifest or
   contract proves another owner. A non-Git container is not itself a child repository.
3. Read effective guidance for every opened root. Record `versioned` or
   `local-unversioned`, current commit when present, dirty/untracked identity through a
   PackageManifest when available, and exclusions.
4. Resolve symbolic scopes to repository-relative real paths. Reject absolute paths,
   `..` escape, and symlink targets outside the resolved root.
5. Record extractor versions and the coverage denominator before scanning. Do not
   redefine the denominator after unresolved files appear.

## Bounded Source Resolution

Search manifests/config, entry points, exports/registrations, definitions,
representative consumers, and tests in that order. For every emitted Asset or Edge:

- preserve repository/component, owner-relative path, symbol, kind, content hash,
  basis, extractor/version, evidence status, confidence, and last-seen scan;
- keep canonical/source owner, build/deploy owner, runtime target identity, and
  gateway/registration alias distinct;
- store native contract/authority identity and hash, never copied body content;
- classify unresolved candidates and competing active authorities explicitly;
- use a tombstone for a confirmed rename/delete needed by historical snapshots.

If a recorded path is stale, ascend only to the nearest existing ancestor inside its
owner root and search the relevant subtree for the symbol/registration. Use Git history
only to corroborate a move already proven by current source. Never cross the old owner
root to rescue an identity.

## Validation And Reporting

Validate schema/version, snapshot basis, path containment, stable-ID uniqueness,
edge endpoints, authority uniqueness, hashes, coverage arithmetic, exclusions,
unresolved/conflict records, and tombstones. Report:

- capability/version, repository and Git roots, basis/PackageManifest ref;
- scan scope, exclusions, extractor versions, snapshot/scan ID;
- covered/total units and the denominator definition;
- unresolved, conflict, stale, and tombstoned counts;
- validator result and every `Not found in this snapshot` or `Not verified` boundary.

Do not write source or repository documentation, issue P0-P3 findings, or infer runtime,
review, delivery, deployment, or production state.
Do not create structured map sidecars without a named owner, producer, non-LLM
consumer, semantic version, executable validator, drift policy, and retirement rule.
