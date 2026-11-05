# Documentation Authority Review

Use this conditional review only when the selected basis creates, restructures,
moves, deletes, or claims completion of authoritative project documentation.

## Authority closure

1. Resolve the current document index and the smallest read path for product
   behavior, UI semantics, repository topology, contracts, and development facts.
2. Keep Product Specs behavioral, UI Specs visual, and Repo Maps navigational.
   Project-declared shared guidance owns shared visual semantics; use `DESIGN.md`
   when adopted. A map or test added by the basis is not independent proof.
3. Verify every move and deletion across indexes, relative links, guidance,
   consumers, and untracked files. Scan the complete Worktree, not only `git diff`.
4. Require durable normative documents to describe the current terminal contract.
   Git retains their history. Local captures, review passes, handoffs, migration
   notes, and environment snapshots belong under a verified ignored `.codex/` path.
5. Allow time-bound status in durable docs only for a named team consumer, fixed
   environment/source basis, revalidation owner, and expiry or refresh condition.

## Structured artifact gate

Before accepting YAML, JSON, Schema, OpenAPI, or another sidecar as durable project
authority, verify a named owner, non-LLM consumer, semantic version, executable
validator, drift policy, and retirement rule. Require a producer only when an actual
generated derivative exists. “AI may read it” is not a consumer. A deployed
Swagger document is environment evidence unless the API owner maintains an adopted
generation and compatibility pipeline.

## UI documentation closure

For a UI documentation change, resolve the applicable product and slice UI contracts,
project-declared shared visual guidance, actual token/value owner, and component
interfaces. Use `DESIGN.md` only when the project adopts that owner; an existing map
provides navigation. Cross-check live routes, components, states, and consumers for
repeated facts, stale derived maps, and source/document drift. A YAML/JSON projection
is reviewed only when its named owner, producer, non-LLM consumer, semantic version,
executable validator, drift policy, and retirement rule are evidenced; otherwise its
absence is not a defect. Declared guidance and live source retain their respective
authority.

Apply Google DESIGN.md format checks only when that format is adopted or its adoption
is explicitly in scope; verify the selected official spec, CLI version, and applicable
lint evidence. A shared token or component change does not itself require adopting
this format or moving an existing authority.

Apply `ui-spec-design-completeness/1` and its trusted-approval requirements only when
the project explicitly adopts that additional policy or an established accepted consumer
requires it. For that policy, verify the
result, required token groups or reasoned omissions, source binding, and exact
design-hash approval. Local `awaiting-trusted-approval-verification` without a
satisfied consumer completeness claim remains blocking: independently trusted human
approval must bind the exact immutable result identity and basis without rewriting
the producer result. Lint zero or content integrity does not satisfy an adopted
completeness or approval requirement. Preserve applicable project requirements;
neither a filename nor format adoption alone establishes the additional policy.

## Ownership identities

Review canonical/source owner, build/deploy owner, runtime service identity, and
gateway/registration alias independently. Verify current definitions, adapters,
representative consumers, and tests. Do not infer source ownership from a legacy
runtime name.

## Verdict

Report stale or duplicate authority, historical evidence leakage, missing closure,
and owner/identity conflation as Standards, Spec, or both with concrete impact. A
fix requires a newly frozen basis and replay of the original failing check.
