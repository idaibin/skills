# Repository Asset Graph eval cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Scan routes, components, APIs and tests into a queryable graph with coverage and unresolved records.` | `repository.asset.scan` |
| `Which pages render this component and which tests verify those pages?` | `repository.asset.query` |
| `Against snapshot X, give dev-frontend only the owner, entry chain, nearest reuse, affected consumers and focused checks for this component change.` | One bounded `repository.asset.query` implementation-navigation slice; no scan or render. |
| `Show the reverse impact of changing OrderDto at snapshot X.` | `repository.asset.query` |
| `Render a Markdown navigation page from snapshot X.` | `repository.map.render`; derived only |
| `Map the stable owners and verification entry points for profiles, packaged resources, schema compatibility, gateway contracts, and cross-repo delivery; do not claim the target runtime was tested.` | Trigger Repo Map with project grounding for stable routing facts. |
| `Create docs/project-map.md even if no graph runtime exists.` | `CAPABILITY_MISSING`; no manual fallback |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Implement the login page.` | `dev-frontend`, not repo-map |
| `Implement this one-owner CSS fix, and create or refresh a repository map first.` | `dev-frontend` should use direct bounded source discovery; do not scan/render merely for implementation. |
| `Review this diff for P0-P3 defects.` | `repo-review`, not repo-map |
| `Create root and child AGENTS.md files.` | separate artifact-writing/guidance owner |
| `Prove the endpoint works in production.` | runtime/evidence owner; static Graph is insufficient |
| `List the top-level directories and owning manifests; do not map runtime, data, integration, compatibility, or delivery authorities.` | Keep project grounding inactive and return the bounded navigation answer. |
| `The maintained record already names the exact current file, owner, and function; edit that local feature.` | Return to the implementation owner without a repo-map query, scan, or render. |

## Quality Eval

| Case | Pass | Reject |
| --- | --- | --- |
| Basis | Snapshot binds repository/package identity and extractor versions. | Mutable branch name or prose-only basis. |
| Scope | Includes, exclusions and supported extractors bound every coverage claim. | Global completeness from attempted files. |
| Identity | Stable asset IDs survive an unambiguous rename; ambiguous matches become issues. | Path-only permanent IDs or guessed reconciliation. |
| Relations | Both endpoints close or the edge is explicitly unresolved with source locator. | Silent missing target or hand-authored edge. |
| Drift | Changed content, extractor version, deletion and rename affect snapshot state. | Resolving path treated as fresh without hash/basis check. |
| Tombstones | Deleted identities remain queryable for historical Runs. | Hard deletion destroys historical refs. |
| Authority | Native Product/DESIGN/source/contract remains owner; duplicate active claims conflict. | Graph copies bodies or chooses precedence silently. |
| Query | Reverse/forward impact is bounded by relation/depth/row limits. | Unbounded traversal or unrelated repository scan. |
| Implementation handoff | Returns one basis-bound slice with owner/entry, canonical and reuse candidates, decisive chain, proven consumers, focused checks, and unresolved/conflicts. | Returns a broad inventory, creates a sidecar, refreshes without request, or presents map records as live source authority. |
| Exact implementation match | Does not query when current context already matches file, owner, and function; current source verification stays with the implementation owner. | Requeries or rescans merely to reconfirm the same known feature. |
| Miss | Reports scope, coverage, exclusions and unresolved records with `Not found in this snapshot`. | Claims implementation does not exist. |
| Runtime boundary | Static records never prove execution, review, delivery, deployment or production. | Path existence upgrades a delivery gate. |
| Derived render | Render names input snapshot and can be deleted/rebuilt. | Markdown becomes authority or gate input. |
| Security | Symbolic scopes resolve inside repository root; symlink escapes and source-body export are rejected. | Lexical-only containment or secret/config body export. |
| Lifecycle | Owner, producer, non-LLM consumer, version, validator, drift and retirement are named. | Adds an AI-only sidecar. |
| Structured map admission | Adds a sidecar only with a named owner, producer, non-LLM consumer, semantic version, executable validator, drift policy, and retirement rule. | Adds an AI-only structured projection. |
| Capability missing | Returns machine-readable `CAPABILITY_MISSING` plus recovery. | Falls back to legacy Markdown-primary behavior. |

Minimum pass: every routing case is correct, all required quality cases pass, and the
consumer demonstrates at least one scan, query, drift reconciliation and validated
exchange/readback operation. Schema validity alone is insufficient.
