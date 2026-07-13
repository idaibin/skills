# Repository Map Reuse Index

Use this reference when the map must help later implementation avoid parallel components, helpers, types, services, or API clients.

## Inclusion Gate

Index an item when at least one condition holds:

- it is an explicit shared contract or registered extension point;
- it has two or more independently maintained consumers, crosses a meaningful boundary, or indexing it materially prevents duplication;
- it is the repository-designated reference implementation for a repeated task;
- crossing it incorrectly would duplicate transport, state, persistence, IPC, or domain behavior.

Do not index every local function, component, endpoint, or type. Source search remains responsible for leaf-local details.

## Verification Chain

Verify only the useful hops:

1. canonical definition or owner;
2. access or registration entry with its actual visibility: public export, module-private import, framework registration, route, schema, or generated-source declaration;
3. one or two representative real consumers;
4. tests or validation entrypoint when they define the contract;
5. constraints such as runtime, framework, domain, ownership, or deprecation state.

For APIs, prefer the chain `route/schema -> handler/service -> client function -> request/response type -> representative caller`. Record the shortest decisive subset rather than every layer.

## Entry Shape

| Capability | Kind | Canonical owner | Access or registration entry | Representative consumers | Reuse boundary | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| user search | API client | `packages/api/src/users.ts` | `searchUsers` export | admin picker; audit filter | reuse typed client; do not duplicate URL or DTO | route, export, two callers |

Use map-root-relative paths and identify the owning Git root when one exists. Name symbols when they are more stable and precise than directory names.

## New-Declaration Gate

Before a new declaration:

1. Search map entries by capability and domain language.
2. Search live source by likely symbols, UI text, endpoint path/method, schema/type names, access/registrations, and callers across the owning root, first-order mapped provider/shared roots, and only transitive roots explicitly identified as canonical owners by those contract edges. Stop when no new owner edge appears or the dependency is declared external; do not scan unrelated dependency graphs.
3. If an applicable provider/shared root is unavailable, unchecked, or ambiguously owned, return `Not verified`; do not approve `new`.
4. Inspect the nearest candidate's contract and consumers.
5. When candidates conflict, rank canonical ownership, active compatible consumers, validation evidence, boundary compatibility, and non-deprecated status. If evidence cannot identify an authority, return `Not verified` rather than selecting arbitrarily.
6. Decide:
   - `reuse`: use the contract unchanged;
   - `extend`: evolve the canonical owner while preserving consumers;
   - `wrap`: adapt at a boundary without cloning the underlying behavior;
   - `new`: create only after documenting why the nearest candidates cannot serve the need.
7. For `new`, record every checked root, closest candidate or `Not found`, incompatibility, intended owner, and expected consumers.

Report this decision for the current task. Add it to the durable map only when it creates or changes a stable canonical owner, reuse boundary, or reusable contract.

Do not extract a speculative shared abstraction solely to make code look uniform. Prefer a named owner and proven consumers; follow stricter repository rules when present.

## Drift Repair

Verify an entry's definition, access/registration entry, representative consumers, and constraints independently. Treat changed semantics as stale even when paths resolve, and patch the changed entry plus directly dependent entries or declared edges reachable from its owner/contract; stop when no changed dependency edge remains. For a missing path, ascend to the nearest existing ancestor, search only the owning subtree, and patch the affected row plus the same bounded dependents. Do not invalidate unrelated reuse entries.
