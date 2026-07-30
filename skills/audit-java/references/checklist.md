# Java Audit Checklist

## Contents

- [Basis](#basis)
- [Build And Architecture](#build-and-architecture)
- [API And Security](#api-and-security)
- [Transactions And Persistence](#transactions-and-persistence)
- [Concurrency And Integration](#concurrency-and-integration)
- [Evidence And Reporting](#evidence-and-reporting)

## Basis

- Record Git/build root, revision, relevant dirty state, scope, and selected profiles.
- Resolve JDK, Maven/Gradle owner, Wrapper, parent/BOM/platform, packaging, framework
  generation, profiles, config ownership, commands, and missing runtime dependencies.
- Trace only reachable, in-scope code and representative consumers/tests.

## Build And Architecture

- Check module roles, dependency direction/cycles, public/internal access, generated
  code, duplicate owners, dependency authority, packaging, and structural lifecycle.
- Compare documentation/commands with manifests and CI; source authorities win.
- Do not require Spring Modulith, ArchUnit, interfaces, or a specific package tree unless adopted.

## API And Security

- Inventory routes, filters/interceptors, method permissions, anonymous exceptions,
  resource/tenant/data scope, credential lifecycle, validation, and error mapping.
- Verify negative authorization and ownership tests, not only happy-path authentication.
- Check CSRF/CORS/session/token decisions against actual clients and credential transport.
- Inspect upload/path/URL/query/serialization bounds, secrets, logging, auditability,
  rate limits, replay, and idempotency with concrete reachable paths.

## Transactions And Persistence

- Map transaction entry, proxy boundary, propagation, rollback, isolation, locking,
  retry, remote calls, async hops, and after-commit effects.
- Inspect entity/DTO separation, mappings, query counts/plans, pagination, N+1,
  tenant filters, bulk operations, indexes/constraints, and database dialect behavior.
- Check migration ordering, existing-data compatibility, recovery, and deployment sequencing.

## Concurrency And Integration

- Map executors, queues, pools, consumers, schedules, locks, caches, and clients to owners.
- Check capacity, backpressure, timeout, retry/backoff, poison/dead-letter, duplicate,
  ordering, lease expiry, cache invalidation, context propagation, and shutdown.
- Require representative workload/runtime evidence before performance conclusions.

## Evidence And Reporting

- For each finding prove trigger, reachable path, owner, consequence, counterevidence,
  exact location, remediation direction, and falsifiable verification.
- Reject stylistic preferences, annotation counting, and missing-tool claims without impact.
- Capture tracked status/diff before and after check-only commands. Do not run known
  apply/fix or tracked-source generation commands in the audited Worktree.
- Stop after unexpected tracked drift, report it as validation contamination, mark the
  affected evidence `Not verified`, and do not revert it without authorization.
- Keep runtime validation static unless explicitly authorized; use only task-owned
  ephemeral services, never shared/staging/production state, and verify cleanup.
- Record unavailable JDKs, artifacts, containers, databases, brokers, config centers,
  datasets, and deployed behavior as `Not verified`.
- Return applicability and evidence status separately, and no final fixed-basis verdict
  unless delegated by `repo-review`.
