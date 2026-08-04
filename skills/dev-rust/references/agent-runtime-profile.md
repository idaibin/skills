# Agent Runtime Profile

## Contents

- [Activation And Boundary](#activation-and-boundary)
- [Minimal Correlation Model](#minimal-correlation-model)
- [Typed Protocol And Schema](#typed-protocol-and-schema)
- [Async Lifecycle And Backpressure](#async-lifecycle-and-backpressure)
- [Approval Policy And Sandbox](#approval-policy-and-sandbox)
- [Durable Log And Projection](#durable-log-and-projection)
- [Tauri And Local App-Server IPC](#tauri-and-local-app-server-ipc)
- [Implementation Sequence](#implementation-sequence)
- [Validation And Output](#validation-and-output)

## Activation And Boundary

Load this profile only when the requested Rust change introduces or materially
changes a stateful local-agent workflow, a typed agent protocol, async task
lifecycle/backpressure, durable operation history or recovery, approval/policy/
sandbox enforcement, or Tauri/local app-server IPC. A Tauri app, SQLite crate, or
async function alone does not activate it.

This is a focused implementation profile, not a mandate to copy a large agent
runtime. Keep the existing project class, crate owners, runtime, persistence, and
transport. Use the smallest state and protocol surface that proves the requested
behavior. Approval, sandbox, deployment, and real-client behavior remain host or
product responsibilities; source code and schema checks do not prove them.

## Minimal Correlation Model

Use three nested identifiers only when the workflow has their corresponding
lifecycle. Here, **Thread**, **Turn**, and **Operation** name workflow levels, not
an OS thread or a mandatory runtime abstraction:

| Level | Meaning and minimum state | Identity rule |
| --- | --- | --- |
| `thread_id` | One durable workflow/session. A minimal lifecycle is `new -> active -> completed`, with `paused`, `failed`, or `cancelled` only when the product can resume or report them. | Stable across turns and recovery; never use a display title as identity. |
| `turn_id` | One bounded user intent or agent response inside a thread: `queued -> running -> awaiting-approval|completed|failed|cancelled`. | A turn has one owner and one terminal outcome; retries do not create a second turn unless the product explicitly starts a new intent. |
| `operation_id` | One side effect, tool call, IPC write, or durable commit: `prepared -> invoking -> succeeded|failed|uncertain`. | Persist before the side effect; distinguish it from the grouping `thread_id`/`turn_id`. |

The exact enum names may follow the repository, but illegal transitions and
uncertain writes must remain explicit. An `uncertain` operation is not a failure:
reconcile it with bounded read-only evidence under the same ID before retrying.
Never resend a non-idempotent operation merely because a response, process, or
connection disappeared. Record attempt count, idempotency, deadline, and evidence
where the existing project contract supports them.

Do not add this hierarchy to a stateless command or a one-shot parser. If only a
turn exists, keep one turn identifier and make the lower-level call's ownership
explicit rather than manufacturing a thread store.

If the host or repository already names grouping levels as a round, relay turn, or
session, map those identifiers to this model and preserve their existing semantics;
do not create a parallel ledger merely to rename them.

## Typed Protocol And Schema

1. Trace the existing authority first: Rust types, a checked schema, or a
   repository-native wire contract. Select exactly one authoring authority; generated
   JSON Schema/OpenAPI/TypeScript or bindings are derived artifacts.
2. Define a versioned envelope for durable or cross-process messages. At minimum it
   should carry `protocol_version`, the applicable correlation IDs, an operation
   kind, a typed payload, and a typed error/status shape. Keep internal Rust state
   separate from the wire representation when their compatibility needs differ.
3. Validate nullability, unknown fields, size limits, error mapping, and enum
   evolution at the boundary. Preserve unknown values when the protocol is open;
   do not model an open foreign integer enum as an exhaustive Rust enum.
4. Generate schemas or clients only through the repository's existing command and
   toolchain. Record the generator/version and prove clean, repeatable output;
   never maintain a hand-edited schema beside a generated authority.
5. Add round-trip, malformed-input, version-compatibility, duplicate-operation,
   and error-envelope tests at the owned boundary. If generation, a consumer, or a
   target runtime is unavailable, report that gate as `Not verified`.

The profile does not require OpenAPI, `schemars`, a TypeScript client, or a new
serialization crate. Add one only when the target repository already owns that
contract or the requested migration names it.

## Async Lifecycle And Backpressure

Select this part only when tasks, channels, blocking work, or cancellation are
reachable. Record the runtime owner, blocking boundary, task owner, and shutdown
coordinator before changing code.

- Bound every input-driven channel, task fan-out, retry loop, buffer, and blocking
  queue. Derive capacity from item size, burst, consumer throughput, and acceptable
  latency; document the chosen overload behavior: await, reject, coalesce, shed,
  or drop with independent metrics.
- Keep synchronous SQLite, filesystem, native, and CPU-heavy work off async workers
  using the existing bounded owner. A `spawn_blocking` wrapper is not itself
  backpressure and already-running blocking work may not be cancellable.
- For each spawned task, choose joined, supervised, runtime-owned, or intentionally
  detached. Observe result, returned error, cancellation, and panic when durable
  work, resources, shutdown, correctness, or caller-visible output depends on it.
- Define cancellation points and partial-state cleanup. In `select!`, preserve an
  in-progress non-cancellation-safe operation instead of restarting it and risking
  duplicate side effects or lost protocol state.
- A detached task is acceptable only when it is bounded, non-critical, retains no
  uncontrolled resource, and its failure is irrelevant or independently observable.
  Do not add a task set, cancellation-token crate, or async mutex mechanically.

## Approval Policy And Sandbox

Keep these controls separate:

| Layer | Owner and question | Implementation consequence |
| --- | --- | --- |
| Approval | An authorized user/product actor decided that a high-impact action may proceed. | Persist the decision and scope when the action needs it; absence or expiry stops the operation. |
| Policy | A deterministic rule evaluates identity, scope, input, and requested effect. | Enforce it at the Rust owner; a UI flag or prompt text is not authorization. |
| Sandbox | The host enforces filesystem, process, network, or resource isolation. | Verify the host capability and configured scope; Rust must stop or degrade safely when the sandbox is unavailable. |

The layers are complementary, not substitutes. A passing policy check cannot
invent user approval or a sandbox. A sandbox cannot decide product authorization.
Record which layer supplied each decision and mark host/runtime proof `Not verified`
when this implementation cannot observe it. Never claim a Skill or Rust command
created a sandbox merely because it limits paths in application code.

## Durable Log And Projection

Add a JSONL source log and SQLite projection only when durable replay, recovery,
audit history, or query latency is a demonstrated requirement. If SQLite already
is the durable source of truth and no append-only replay is needed, do not add a
second log for architectural fashion.

When selected:

- Make the source authority explicit. Each append-only event carries a stable
  `event_id`, monotonic sequence (per stream or source), schema version, event kind,
  timestamp, and correlation IDs. Define record framing, append atomicity, flush/
  fsync policy, rotation, and corruption handling from the target deployment.
- Treat the SQLite projection as derived. Apply events idempotently by event ID or
  sequence inside a transaction, persist a projection watermark, and prevent two
  writers from becoming competing authorities.
- On restart, replay from the last durable source record or rebuild the projection
  deterministically. A crash between source append and projection commit must be
  recoverable without duplicating an external side effect.
- Version event payloads and migrations independently. Test duplicate delivery,
  truncation/corruption, interrupted projection, replay, supported upgrades, and
  backup/restore when those paths are part of the contract.

The log records intent and observed outcomes; it does not make an external effect
idempotent. Correlate an operation ledger with the event stream and reconcile
`uncertain` operations before issuing a new write.

## Tauri And Local App-Server IPC

For Tauri, trace registration, `build.rs`, generated app-command permissions,
capability assignment, configured scope, Rust domain authorization, typed request /
result / error mapping, and the actual caller. Custom commands registered through
`invoke_handler` are application-wide by default; do not claim per-window or
per-webview ACL without generated allow/deny permissions and capability evidence.
Validate all frontend-controlled paths, URLs, identifiers, payload sizes, and
resource limits in Rust. CSP is defense in depth, not command authorization.

For a local app-server, inspect the real transport (loopback HTTP, Unix socket,
named pipe, or another host API), peer/token/permission checks, bind scope, request
limits, disconnect and cancellation behavior, and startup/shutdown ownership. A
loopback listener is not automatically trusted. Use the same typed envelope and
`thread_id -> turn_id -> operation_id` correlation where a request can be retried
or streamed. Keep UI/JS adaptation with its owner; keep Rust policy and domain
authorization in the Rust owner.

Do not claim IPC or real-client behavior from compile-time registration alone. Run
the repository's client/target checks when available; otherwise report target,
webview, remote-content, and deployment evidence `Not verified`.

## Implementation Sequence

1. Record project class, toolchain, existing runtime/transport/persistence owners,
   current commands, and a clean or preserved Worktree baseline.
2. Decide whether this profile is active and which sections apply. Write down the
   minimum lifecycle and one source-of-truth decision before adding types.
3. Reuse or extend the nearest state, protocol, task owner, storage, command, or
   IPC contract. Justify any new envelope, ledger, generator, log, or projection.
4. Implement one vertical behavior slice: persist legal state before the side
   effect, execute through the owned boundary, observe the outcome, and reconcile
   or stop on uncertainty.
5. Add only the selected async, approval/policy/sandbox, durable, and IPC guards;
   keep product rules out of transport glue and host capabilities out of prose.
6. Update tests, generated artifacts, registration, manifests, docs, and indexes
   for the reachable boundary. Do not update unrelated repositories or fabricate
   runtime evidence.

## Validation And Output

Start with Baseline, then add only the relevant overlays. For an active profile,
the minimum focused checks are:

- legal/illegal state transitions, duplicate and uncertain-operation recovery;
- typed round-trip, malformed/versioned envelope, and clean schema/client generation
  when a generator is an existing contract;
- bounded overload, channel close, cancellation, panic/result observation, deadline,
  and shutdown checks for selected async paths;
- append/replay/projection idempotence and interruption/restart checks for selected
  durable paths;
- Tauri/app-server negative authorization, scope, malformed-input, disconnect,
  timeout, and payload-limit checks when the target supports them.

Report the selected Agent Runtime sections, authority and owner, state transitions,
changed contract chain, baseline/overlay evidence, and every target/host/consumer
claim that remains `Not verified`. Do not call a static schema, unit test, or local
compile a sandbox, deployed IPC, or recovery proof.
