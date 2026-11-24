# API and business logic

## Contents

- [Contract to observation](#contract-to-observation)
- [Case selection](#case-selection)
- [Shared contracts and service limits](#shared-contracts-and-service-limits)
- [Fixtures and fault control](#fixtures-and-fault-control)
- [Evidence limits](#evidence-limits)

## Contract to observation

Use available confirmed API rules, feature behavior and the actual frontend consumer.
When a formal contract is unavailable, use the [existing-project default](coverage.md#existing-project-default)
to derive regression/exploration cases from authorized source and live observations.
Missing documentation alone does not block those cases. Freeze expectations and label
their basis; a baseline or inferred pass does not establish wire-contract acceptance.
Record source/contract paths and revisions plus material conflicts in the existing
gap notes; continue independent cases. Do not infer wire semantics by reading an
unauthorized backend repository or by copying Mock data.

Execute direct requests only through a host-owned API runner whose permission
contract independently allows the exact environment, method, resource and read/write
effects. This Skill's browser-control maximum does not grant direct service mutation;
command-runner availability or a test request alone is insufficient. Without a
compatible authorized runner, leave direct API cases BLOCKED and continue other
reachable cases. Browser actions use their separately authorized browser route.

For an exercised request verify method/path, query/body, required and nullable fields,
types, IDs, pagination, filters, sorting and relevant headers without exposing secrets.
Record transport status separately from application success/error codes; HTTP 200
with `success:false` is a failure when the contract says so. Distinguish `null`, empty,
zero, false and omitted fields. Inspect response mapping into rendered values.

For an authorized write, trace input → payload → persisted fields → independent
detail/list query → visible values. Test replacement versus patch semantics: fields
not shown in a form may still need preservation in a full-object update. Assert
invariants in affected consumers rather than accepting a success message.

## Case selection

| Behavior | Useful discriminating checks |
| --- | --- |
| Query/list | zero/one/many, page boundary, stable total and order, combined filters, reset, missing optional values |
| Create/update | required/length/format boundaries, duplicates, full/partial update, unknown outcome reconciliation, refresh readback |
| State machine | permitted and rejected transitions, dependent counts, selected/disabled state, cancellation and no mutation |
| Permissions | visible control and actual API permission, own/other records, role change only with authorization; hidden button alone proves neither security nor authorization |
| Failure/recovery | HTTP failure, HTTP-success business failure, timeout, invalid/missing data, retry, stale state and reactivation |
| Concurrent input | double submit, fast filter/page changes, out-of-order responses, stale version; preserve real timing evidence |
| Files | chosen bytes/metadata, returned reference, reload/preview, download event and actual file content |
| Dates/numbers | timezone/date boundaries, inclusive ranges, units/precision and default values from the owning contract |

Select cases that apply; this is not authority for security probes, load testing,
credential changes or destructive data operations. Discover read-versus-write behavior
even for GETs such as mark-read or launch endpoints before invoking them.

## Shared contracts and service limits

| Risk | Discriminating checks |
| --- | --- |
| Contract drift | Compare the owner's shared schema and accepted exceptions with the operation's request, success/error responses, raw observations and consumer mapping. Check direction, nesting, nullability and scalar type. Use different non-default page numbers; request and response may use different names. For options, use independently seeded label/value pairs. Swap two same-typed IDs as a failing control and reorder intact pairs when order is free. Attribute response shape, pair matching, visible selection and submitted ID to their respective observations. Vary dynamic source independently in two samples, including error responses where it applies. An example literal alone cannot establish a constant. |
| Authorization | Use an approved decision table with synthetic owner, peer and other tenant. Check allowed and denied decisions, returned fields, side effects and independent readback. Distinguish policy-unit checks from enforcement by a running service. |
| Pagination and sorting | With fixed rows exercise first, full, partial last and empty pages. Put tied sort values across a boundary; check documented tie-breaker, direction and null handling. Compare all ordered IDs with an independent list. For changing data use the accepted cursor/snapshot or offset consistency guarantee. |
| Concurrency | Coordinate independent operations at a known boundary. Cover both orders, duplicate versus separate intent, conflicting versions, rollback, and timeout after commit. Count durable effects and re-read by business key. Bind the expected outcome to the agreed idempotency scope and consistency window. |
| Query cost and overflow | At two bounded cardinalities record query count, rows examined/returned, bytes, elapsed time and applicable plan or budget. Compare equal filters and cache states. Test page offsets, counts, IDs and money at their representation boundaries through storage, wire and consumer. |
| Cache lifecycle | Scope keys by tenant, identity and query. Exercise miss, hit, expiry, update/delete, late repopulation and authoritative readback under the accepted freshness rule. Distinguish an expired old session key from overlapping rotations. Root cause requires correlated server observations. |

## Fixtures and fault control

For transaction, locking or uniqueness claims, execute the relevant storage behavior on
an isolated instance of the target engine. Inject failure between dependent writes and
read the committed outcome independently. For migrations, seed records in the previous
format, apply the migration and verify existing data and a new write through supported
entry points. Record which storage and migration paths the test actually exercised.

Label Mock, intercepted, test-service and real-service results separately. Inspect
the fixture's schema, status semantics, pagination/filter behavior and persistence
scope. Use independent filter values: accidentally correlated fixture fields can make
an incorrect AND/OR filter appear correct. Enough rows to cross the page boundary
matters more than an arbitrary record count.

Never globally change a shared fault switch, reset datasets or restart shared services
to isolate a case. Use already supported task-scoped mechanisms where authorized;
otherwise leave the fault branch BLOCKED. Report contract gaps in fixtures without
rewriting them simply to obtain a green test.

For a parameter or response-semantics claim, inspect the fixture matcher as well
as the response. A path-only success rule cannot prove identifier presence,
placement or meaning; accepting two different identifiers with identical samples
cannot prove which one the real service accepts. Vary relevant identifiers and
metadata independently, exercise the declared missing/empty/whitespace behavior,
and pair an invalid input with a structurally similar valid case where applicable.
Do not require a parameter in a branch whose accepted contract permits omission.
If field metadata describes child collections, independently verify whether it
says anything about directly attached records before deriving an empty-state oracle.

Stopping interception is not cleanup evidence. When switching from synthetic to
real verification, inspect the applicable interception hooks, in-memory/framework
state, persistent caches and rendered records. Remove only explicitly authorized,
identifiable synthetic entries, preserve business/authentication data, and verify
the real response reaches the page after permitted refresh or re-entry. Report
unknown provenance or unapproved cleanup as a gap rather than clearing all storage.

## Evidence limits

For asynchronous result/download journeys, map relevant faults to accepted states and
recovery: failed retrieval versus confirmed emptiness, stage-specific retry, retained
results after refresh failure, duplicate admission, close during work and late completion.
A synthetic fault such as 503 is a selected fixture, not a universal code. Record
controllable failure points; route missing injection support to implementation.
Simulated faults do not prove a real service failed or recovered. Keyboard assertions
remain in [page walkthrough](page-walkthrough.md).

Direct API tests prove API results, not whether the page sent the same payload.
Browser network evidence must bind the tested action to its own request and response.
Independent API readback strengthens persistence proof but does not replace actual UI
interaction. Retain only necessary sanitized values; redact tokens, cookies, personal
data and sensitive callback query parameters from durable evidence.
