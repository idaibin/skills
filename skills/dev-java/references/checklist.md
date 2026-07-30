# Java Implementation Checklist

## Contents

- [Required Context](#required-context)
- [Design And Reuse](#design-and-reuse)
- [Security And API](#security-and-api)
- [Transactions And Data](#transactions-and-data)
- [Integration And Runtime](#integration-and-runtime)
- [Validation](#validation)

## Required Context

- Resolve the owning Git/build root, authorized target module, and intended JDK
  contract; stop before edits if the intended owner cannot be established. If repairing
  an authority conflict is the explicit task, limit edits to the approved target.
- Record the initial `git status --short` and relevant diff without absorbing unrelated work.
- Read the nearest instructions, manifest, Wrapper/toolchain, entry point, config owner,
  directly related code, tests, migrations, and command source.
- Record JDK, build-tool, framework, packaging, profiles, parent/BOM/platform, internal
  modules, private dependencies, generated sources, and missing authorities.
- Select Baseline plus each applicable overlay before editing.

## Design And Reuse

- Trace route/listener/job -> DTO/message -> application/service -> domain -> repository/client.
- Search the nearest analogous feature and classify reuse, extension, adaptation, or new.
- Keep dependency direction and module visibility consistent with current architecture.
- Justify new interfaces, base classes, generic wrappers, events, executors, or shared utilities.
- Load `codebase-design.md` for public seam/testability changes and `code-quality.md`
  only for material maintainability work.

## Security And API

- Record authentication, operation/resource authorization, tenant/data scope, anonymous
  routes, credential lifecycle, validation, error mapping, and negative tests.
- Check CSRF and CORS against the actual browser/credential model.
- Bound uploads, paths, URLs, pagination, queries, and serialized inputs.
- Preserve log redaction and external secret/config ownership.
- Keep one API/schema authority and update every owned consumer when it changes.

## Transactions And Data

- Define transaction owner, propagation, isolation, rollback, timeout, lock, and retry behavior.
- Check Spring proxy/self-invocation and async/remote boundaries.
- Validate migrations against existing data, constraints, indexes, and target dialect.
- Check N+1, pagination, tenant filters, unbounded loads, entity/DTO separation, and concurrency.
- Coordinate after-commit events, cache invalidation, outbox/reconciliation, and duplicate handling.

## Integration And Runtime

- Bound executor/queue/pool sizes, timeouts, retries, backoff, overload, and shutdown.
- Align idempotency and distributed-lock keys with durable uniqueness.
- Define cache source of truth, TTL, invalidation, serialization, and degraded behavior.
- Propagate correlation/security context deliberately and clear thread-local state.
- Preserve metrics, health, logs, and operational recovery for new failure modes.

## Validation

- Run a red-capable focused check before or with the implementation when a stable seam exists.
- Run repository-owned format/static/compile and focused tests with the pinned toolchain.
- Prefer check-only validation; capture status/diff before and after commands and
  classify expected task output, unexpected validation drift, and unrelated changes.
- Add slice, integration, real-database/container, security, concurrency, or migration
  checks only when selected risk requires them.
- Verify no tests/gates were weakened, skipped, or replaced by smoke assertions.
- Recheck generated sources, manifests, registrations, docs, CI/deploy paths, consumers,
  and dirty files. Report applicability and evidence status as separate dimensions.
