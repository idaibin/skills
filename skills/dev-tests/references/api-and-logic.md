# API and business logic

## Contract to observation

Use the API owner's formal contract, accepted feature behavior and actual frontend
consumer. Record the contract version/path and unresolved conflicts. Do not infer
wire semantics by reading an unauthorized backend repository or by copying Mock data.

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

## Fixtures and fault control

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
