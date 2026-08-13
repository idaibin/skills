# Documentation Authority Review

Use this conditional review only when the selected basis creates, restructures,
moves, deletes, or claims completion of authoritative project documentation.

## Authority closure

1. Resolve the current document index and the smallest read path for product
   behavior, UI semantics, repository topology, contracts, and development facts.
2. Keep Product Specs behavioral, UI Specs visual, `DESIGN.md` shared-semantic, and
   Repo Maps navigational. A map or test added by the basis is not independent proof.
3. Verify every move and deletion across indexes, relative links, guidance,
   consumers, and untracked files. Scan the complete Worktree, not only `git diff`.
4. Require durable normative documents to describe the current terminal contract.
   Git retains their history. Local captures, review passes, handoffs, migration
   notes, and environment snapshots belong under a verified ignored `.codex/` path.
5. Allow time-bound status in durable docs only for a named team consumer, fixed
   environment/source basis, revalidation owner, and expiry or refresh condition.

## Structured artifact gate

Before accepting YAML, JSON, Schema, OpenAPI, or another sidecar as durable project
authority, verify a named owner, producer, non-LLM consumer, semantic version,
executable validator, drift policy, and retirement rule. “AI may read it” is not a
consumer. A deployed
Swagger document is environment evidence unless the API owner maintains an adopted
generation and compatibility pipeline.

## UI documentation closure

For a UI documentation change, verify the chain in order: Product Markdown for
behavior, page/component UI Markdown for UI meaning, resolved `DESIGN.md` for shared
visual semantics, project-map Markdown for navigation, and live source for routes,
components, states, and consumers. Identify repeated facts, stale derived maps, and
source/document drift. A YAML/JSON projection is reviewed only when its named owner,
producer, non-LLM consumer, semantic version, executable validator, drift policy, and
retirement rule are evidenced; otherwise its absence is not a defect and Markdown
remains authoritative.

For first adoption, adopted shared-authority maintenance, or a Design System Spec,
review official format lint and UI Spec completeness as separate gates. Require the
official spec commit and CLI version, `ui-spec-design-completeness/1` result, machine
token groups or concrete official omissions, source binding, and exact design-hash
human approval for adopted status. Local `awaiting-trusted-approval-verification`
without a satisfied consumer completeness claim is blocking. Require a host-trusted
approval receipt bound to the same exact Result Package; it clears the consumer gate
without rewriting the producer result. Lint zero and a matching PackageManifest prove
neither completeness nor approval.

## Ownership identities

Review canonical/source owner, build/deploy owner, runtime service identity, and
gateway/registration alias independently. Verify current definitions, adapters,
representative consumers, and tests. Do not infer source ownership from a legacy
runtime name.

## Verdict

Report stale or duplicate authority, historical evidence leakage, missing closure,
and owner/identity conflation as Standards, Spec, or both with concrete impact. A
fix requires a newly frozen basis and replay of the original failing check.
