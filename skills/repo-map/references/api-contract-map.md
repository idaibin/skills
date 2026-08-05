# API Contract Map Profile

Use this profile only when a durable map of an HTTP service or bounded operation
will prevent duplicate contracts or repeated discovery. It supports repository-native
clients and optional generated pipelines; it is not an implementation prerequisite.

## Evidence Chain

Verify the shortest decisive current-source chain:

1. canonical source/module owner and provider root;
2. build/deploy owner when it differs;
3. runtime service identity and gateway/registration alias when they differ;
4. repository-native authority and canonical path;
5. route or registration entry, method/path, and operation ID when present;
6. request, success, error, authentication, and authorization declaration owners;
7. executable exchange artifact and generator details only when current source owns them;
8. native or generated client package/path and access command when applicable;
9. one or two representative real consumers and the touched DTO ownership boundary;
10. validation, compatibility, contract-test, frontend-check, and CI entrypoints that
   exist in current source.

Use `Not applicable` when no generated contract pipeline is intended. Record a
missing expected generator, artifact, client, consumer, or command as `Not found`.
Record unchecked execution, runtime behavior, compatibility, browser behavior, and
clean-state reproducibility as `Not verified`.

## Entry Shape

Use one row per bounded operation or independently governed service contract:

| Field | Required content |
| --- | --- |
| Product/contract term | Stable business or capability name; link the product fact source instead of copying it |
| Source/module owner | Canonical source root and provider boundary that limit discovery and stale repair |
| Build/deploy owner | Owning manifest/module/pipeline, or `same as source owner` |
| Runtime identity | Service/discovery name used at runtime; never treated as source ownership by itself |
| Gateway/registration alias | External context, route prefix, registration alias, or `Not applicable` |
| Authority | Repository-native owner/path/symbol; code-first or contract-first only when an executable exchange pipeline exists |
| Registration | Route/schema registration, method/path, operation ID, and actual visibility |
| Request/success/error owners | Canonical DTO/envelope/error declaration paths or symbols |
| Auth boundary | Authentication and authorization declaration owners; do not infer policy from UI visibility |
| Exchange artifact | Existing normalized artifact/generator, or `Not applicable` |
| Client boundary | Native or generated client path/package, access/generation command, and wrapper when present |
| Representative consumers | One or two real callers and their loading/success/error ownership when relevant |
| DTO boundary | Generated DTO owner, duplicate handwritten DTO search scope, result, and justified exceptions |
| Validation entries | Existing validation, idempotence, compatibility, contract-test, frontend, and CI commands or `Not found` |
| Current-source evidence | Paths/symbols inspected and unchecked/runtime gaps |

Keep artifact hashes, Git bases, command results, screenshots, traces, and transient
branch state in a versioned trial/review evidence record, not the durable repo map.
The map may link that record as evidence but must recheck current source before use.

## Authority And Drift Rules

- One contract boundary has one authority. If current source contains competing
  authorities, record `Authority ambiguous`, list the bounded conflicting owners,
  and stop short of selecting one.
- When OpenAPI is active, generated artifacts are derived in code-first mode. Backend declarations
  and an independently edited OpenAPI file cannot both be authorities.
- In contract-first mode, implementation annotations and generated clients conform
  to the authoritative OpenAPI; they do not become new authorities.
- Treat a resolving path as stale when authority type, registration, generator,
  consumer, DTO ownership, or command semantics changed.
- Repair only within the recorded owner/provider root. If that root is absent, mark
  the entry stale and perform fresh bounded discovery; never cross the old root.
- Use Git history only to explain a current-source-proven rename or move. Never use a
  historical artifact or consumer to prove current authority or reusability.
- A module may move while retaining a legacy runtime service name. Record both facts
  without reporting a conflict when current registration, adapters, and tests agree.

## Verification Boundary

The Contract Map answers what owns the contract, how derived artifacts are reached,
who consumes them, where duplication may exist, and which checks are available. It
does not:

- define product behavior; use `product-spec` for unresolved intent or acceptance;
- require, generate, or own executable OpenAPI;
- judge a diff or fixed revision for defects; use `repo-review`;
- implement backend/client changes; use the matching `dev-*` owner;
- prove generation idempotence, compatibility, runtime conformance, browser states,
  or clean CI merely because commands or artifacts are present.
