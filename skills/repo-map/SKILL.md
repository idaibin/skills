---
name: repo-map
description: "Use when a Git or non-Git workspace needs a machine-queryable repository asset scan, impact/relationship query, coverage or drift check, or an optional derived navigation view; not for task-local discovery, source changes, repository-guidance authoring, or change review."
---

# Repository Map

## Overview

Own two read-only capabilities, `repository.asset.query` and
`repository.map.render`, plus the artifact-writing `repository.asset.scan` capability.
The scan never changes repository source, documentation, or Git, but its host adapter
must own an isolated run-local SQLite/cache path and declare that write explicitly.
The authoritative result is a
versioned Repository Asset Graph snapshot with stable asset and edge references,
explicit basis, scope, exclusions, coverage, conflicts, and unresolved records. A
Markdown or HTML map is an optional derived view over that snapshot; it is never the
gate, completeness proof, or source of truth.

Project source, contracts, configuration, Product Markdown, `DESIGN.md`, and local UI
contracts retain their native authority. The graph indexes identity and relationships
without copying their bodies. Runtime claims and delivery status belong to typed
delivery observations, not the asset graph.

Keep canonical/source owner, build/deploy owner, runtime service identity, and
gateway/registration alias as separate fields when they differ.

## Workflow

1. Resolve the requested capability, repository root, nested Git roots, symbolic scan
   scope, exclusions, and current basis. Reject absolute, parent-escaping, or symlink-
   escaping scope. Read effective repository guidance and inspect Worktree state before
   broad reads.
2. Preflight a compatible graph runtime for the selected capability and schema version.
   If none exists, return `CAPABILITY_MISSING` with the missing capability/version and
   recovery hint. Do not fall back to a hand-written Markdown map and imply equivalent
   coverage.
3. For `repository.asset.scan`, require a host-owned, repository-excluded run-local
   store and run bounded extractors against source, contracts,
   manifests, configuration, tests, and declared authorities. Record extractor identity
   and version, confidence, evidence status, content hash, and last-seen basis for every
   record. Keep runtime observations out of the graph.
4. Persist the local `urn:forgeway:repository-asset-snapshot:v1` snapshot and emit a
   portable `urn:skills:asset-map-result:v1` envelope containing its compatible
   snapshot/scan ID,
   basis, included scope, exclusions, coverage denominator and numerator, unresolved
   records, conflicts, stale/tombstoned records, and validation result. A partial scan
   remains partial even when all attempted extractors succeed.
5. For `repository.asset.query`, consume an exact compatible snapshot reference and a
   bounded query such as asset lookup, relationship traversal, consumer lookup, reverse
   impact, authority conflict, or drift. Preserve the snapshot basis in the result; a
   query against a stale basis is labeled stale rather than silently refreshed. If the
   caller already has a maintained record that matches the exact current file, owner,
   and function for the requested feature, return control without running a query; the
   implementation owner verifies that target directly in current source. For an
   unresolved cross-owner implementation edge, return only one compact slice: owner,
   entry, decisive registration/call path, affected consumers, focused check, basis,
   scope/exclusions, and unresolved conflicts. This is navigation, not a new sidecar or
   implementation authority.
6. Before any absence claim, report the searched scope, extractor coverage, unresolved
   records, and exclusions. A query miss means `Not found in this snapshot`, not proof
   that no implementation exists.
7. For `repository.map.render`, consume an exact snapshot/query result and render only
   the requested navigation projection. Include snapshot ID, basis, coverage, and a
   regeneration command or capability reference. Do not add facts that are absent from
   the machine result.
8. Validate schema, references, authority uniqueness, edge endpoints, path containment,
   and snapshot/basis consistency. Report drift and conflicts as typed failures; do not
   repair source, approve authorities, or mutate Git.
9. When the host provides Forgeway delivery integration, bind the invocation to an
   immutable Run input reference and PackageManifest/basis reference, then attach the
   typed result as an Observation. Provider, model, executable, and session attribution
   remain run-local facts. Absence of that integration does not weaken graph validation,
   but delivery state remains `Not verified`.

## Modes

- **Asset scan:** produce or incrementally refresh a validated graph snapshot.
- **Asset query:** answer bounded identity, relation, authority, reuse, consumer, impact,
  coverage, unresolved, conflict, or drift questions against one snapshot.
- **Implementation navigation query:** answer one unresolved owner, reuse, consumer,
  or impact edge from an existing compatible snapshot; never scan or implement.
- **Derived render:** create a disposable Markdown/HTML navigation view from a typed
  result. Deleting the view must not lose graph facts.

## Hard Rules

- Keep this Skill read-only with respect to repository source, documentation, and Git;
  only the bounded scan store or requested derived view may be written.
- Never make Markdown the authoritative scan result or a required delivery gate.
- Never treat directory enumeration or a selective reading path as complete repository
  cognition.
- Never scan, refresh, or render a map merely because a task-local implementation needs
  navigation. Use an existing compatible snapshot for one bounded unresolved edge; if
  none exists, let the implementation owner use targeted current source.
- Never query merely to reconfirm an already matched same-file, same-owner, same-function
  record.
- Never copy Product, design, UI, source-contract, schema, or runtime bodies into the
  graph; store stable identity, location, hash, authority role, and edges.
- Never infer runtime success, review approval, delivery, deployment, or production
  verification from static graph records.
- Never hand-author stable IDs or relationship edges to compensate for a missing or
  failed extractor. Emit unresolved/conflict records and the responsible extractor.
- Never erase renamed or deleted assets needed by historical Runs; use tombstones or
  versioned snapshot history according to the graph retention policy.
- Never accept a snapshot whose basis, schema version, producer, validator, drift
  policy, or retirement rule is absent.
- If an already maintained non-LLM structured projection is encountered, treat it as
  navigation only and require its named owner, producer, non-LLM consumer, semantic
  version, executable validator, drift policy, and retirement rule. Otherwise ignore
  it and use the validated graph/native source chain.
- Do not create map sidecars for machine convenience without a named owner, producer,
  non-LLM consumer, semantic version, executable validator, drift policy, and
  retirement rule.
- Preserve unrelated local changes and secrets. Do not export source bodies, credentials,
  or sensitive configuration into graph snapshots or derived views.
- Say `Not verified` for unchecked runtime or delivery claims and distinguish it from
  `false`, `conflict`, `stale`, and `Not found in this snapshot`.

## Output Contract

Return the selected capability ID/version, repository and Git roots, basis/PackageManifest
reference when available, scan scope and exclusions, snapshot/scan ID, typed result
schema, validation, coverage, unresolved/conflict/stale counts, query and bounded result,
derived-view path when requested, and every `Not verified` boundary. If Forgeway
integration is active, also return Run and Observation references; never claim a Receipt
or delivery level that this read-only owner did not produce.

## References

- See [references/checklist.md](references/checklist.md) only for ambiguous root and
  bounded source-resolution procedures.
- See [references/project-grounding.md](references/project-grounding.md) when static
  repository relations cross packaging, integration, compatibility, or deployment-
  target boundaries; runtime results still belong to delivery observations.
- See [references/frontend-inventory.md](references/frontend-inventory.md) only to
  select frontend extractor/query scope; do not emit its legacy Markdown inventory as
  authority.
- See [references/api-contract-map.md](references/api-contract-map.md) only to locate
  native API authority and consumer edges without copying schemas.
- See [references/java-build-and-dependency-map.md](references/java-build-and-dependency-map.md)
  only to select Java build/dependency extractor scope; any tabular examples are query
  projections, not an authoritative output contract.
- See [references/reuse-index.md](references/reuse-index.md) only to translate legacy
  reuse questions into graph consumer/registration queries; do not author its old
  Markdown rows.
- See [references/project-guidance.md](references/project-guidance.md) only to identify
  and reroute an explicit repository-guidance authoring request; this read-only Skill
  does not perform that write mode.
- See [references/prompt-templates.md](references/prompt-templates.md) only when
  composing a bounded scan/query/render request.
- See [references/usage.md](references/usage.md) and
  [references/eval-cases.md](references/eval-cases.md) for usage and routing checks.
