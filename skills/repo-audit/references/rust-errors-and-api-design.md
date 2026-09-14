# Errors And API Design

## Public Invariants

- Use types and constructors to make invalid states difficult to represent.
- Keep public struct fields private when callers must not bypass invariants.
- Prefer semantic enums, newtypes, builders, or configuration structs over
  ambiguous booleans and long positional argument lists.
- Preserve semver and feature behavior for libraries. Trace downstream callers
  before changing public traits, error variants, re-exports, or default features.
- Document panic, error, safety, cancellation, and blocking behavior where it is
  part of the contract.

## Error Classes

Classify errors before choosing a representation:

| Class | Expected handling |
| --- | --- |
| User input | explain the invalid field/value without exposing internals |
| Business state | typed conflict or unavailable-state result |
| External dependency | preserve source/context; classify retryability |
| Data corruption or incompatible schema | stop unsafe progress and provide recovery evidence |
| Retryable busy/timeout/transient failure | bounded attempts, backoff, idempotency, cancellation |
| Broken internal invariant | assertion or panic only when recovery is not meaningful |

## Boundary Rules

- Libraries return errors; they do not call `process::exit` for recoverable
  conditions. CLI and application boundaries choose exit codes or UI messages.
- Expected errors do not use `panic!`, `unwrap`, or `expect`. An `expect` is
  acceptable only when a nearby invariant makes failure impossible and the
  message explains that invariant.
- Preserve typed sources and useful context. Do not collapse all errors into
  strings merely to share one type.
- Recommend adding context once at the boundary where it becomes meaningful and logging once at the
  owner that can act; avoid logging and rethrowing the same failure at every
  layer.
- Redact tokens, credentials, personal data, SQL values, paths, and payloads as
  required by repository policy.
- Keep retry bounded by count or deadline. Define backoff, jitter when needed,
  idempotency, overload amplification, cancellation, and terminal error.
- Convert domain and infrastructure errors to stable CLI, HTTP, or Tauri
  transport errors at the outer boundary. Do not expose database-library or
  internal enum layout accidentally.

## Review Evidence

Trace each changed error through producer, conversion, log/tracing event,
retry/cancellation logic, caller match, user-visible mapping, tests, and docs.
Mark uninspected branches `Not verified`.
