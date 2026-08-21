# Repository Asset Graph usage

## Best for

- fixed-basis repository asset scans with explicit scope and exclusions;
- route, component, API, DTO, schema, database, workflow, test and contract lookup;
- forward/reverse relation and impact queries;
- coverage, unresolved relation, authority conflict, stale and tombstone inspection;
- an optional derived Markdown/HTML navigation view after a validated query.

Do not use for task-local source discovery, implementation, P0-P3 review, repository
guidance authoring, Git mutation, runtime verification or delivery claims.

## Examples

- `Scan src, tests and migrations into a versioned Repository Asset Graph and report extractor-bounded coverage.`
- `Query every page that renders FeedCard and every test that verifies those consumers.`
- `Against snapshot X, return the compact frontend implementation slice for changing
  FeedCard: owner, entry/render chain, nearest reuse, affected consumers, and focused
  checks.`
- `Show unresolved API/DTO edges and authority conflicts for this fixed snapshot.`
- `Compare the current scan with the previous basis and report renamed, deleted and stale records.`
- `Render a disposable project-map.md from this exact query result.`

If a compatible `repository.asset.scan` or `repository.asset.query` runtime is absent,
return `CAPABILITY_MISSING`. Do not substitute a hand-written map. A query miss means
`Not found in this snapshot`; it is bounded by the reported scope and extractor set.
Do not create, refresh, or query a snapshot solely to reconfirm an already known
same-file/owner/function source change; the implementation owner verifies current
source directly and may use bounded live-source discovery for an unresolved edge.

## Output

Return capability/version, repository identity, basis or PackageManifest reference,
scan/snapshot ID, scope, exclusions, extractor versions, coverage, issues, query result,
stale/tombstone counts and every `Not verified` boundary. A derived render additionally
names its input snapshot and regeneration capability, and remains outside all gates.
