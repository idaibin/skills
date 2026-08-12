# Graph request templates

These are request shapes, not repository document templates. Native source and
contracts remain authoritative; the Graph stores identity, location, hash and edges.

## Asset scan

```text
Run repository.asset.scan version <version> for repository <id> at basis <basis>.
Includes: <symbolic scopes>
Exclusions: <symbolic exclusions>
Required extractors: <ids/versions>
Return: snapshot/scan ID, coverage, unresolved, conflicts, stale and tombstones.
Do not export source bodies or infer runtime/delivery state.
```

## Bounded query or impact

```text
Run repository.asset.query against snapshot <snapshot-id> at basis <basis>.
Question: <asset/relation/consumer/reverse-impact/authority/drift query>
Limits: <kinds, relation types, depth, maximum rows>
Return exact stable IDs, locators, evidence status and unresolved boundaries.
Do not silently refresh a stale snapshot.
```

## Derived navigation render

```text
Run repository.map.render from query result <result-id>.
Format/path: <Markdown or HTML output>
Include snapshot ID, basis, coverage and regeneration capability.
Mark the output derived and prohibit it as a gate input.
```

An explicit request to create `AGENTS.md` or other repository guidance must be routed
to a separately authorized artifact-writing owner. Repo-map itself stays read-only.
Do not add a structured sidecar without a proven lifecycle named owner, producer,
non-LLM consumer, semantic version, executable validator, drift policy, and retirement rule.
