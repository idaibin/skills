# Agent Runtime Audit Profile

## Contents

- [Activation And Scope](#activation-and-scope)
- [Evidence Model](#evidence-model)
- [Thread Turn And Operation](#thread-turn-and-operation)
- [Typed Protocol And Schema](#typed-protocol-and-schema)
- [Async Lifecycle And Backpressure](#async-lifecycle-and-backpressure)
- [Approval Policy And Sandbox](#approval-policy-and-sandbox)
- [Durable Log And Projection](#durable-log-and-projection)
- [Tauri And Local App-Server IPC](#tauri-and-local-app-server-ipc)
- [Audit Sequence And Findings](#audit-sequence-and-findings)
- [Validation And Report](#validation-and-report)

## Activation And Scope

Select this profile only when the audit reaches a stateful local-agent workflow,
typed agent protocol, async task/backpressure lifecycle, durable operation history
or recovery, approval/policy/sandbox enforcement, or Tauri/local app-server IPC. A
Rust async crate, SQLite dependency, or Tauri directory is a signal, not scope.

This is a bounded read-only profile. Preserve `audit-rust` ownership and selected
profile boundaries; route approved remediation to `dev-rust`. Do not require a
generic agent platform, JSONL log, SQLite projection, or event-sourcing model when
the repository has no reachable replay, recovery, audit, or query requirement.
Mark host sandbox, target IPC, deployment, and real-client behavior `Not verified`
unless the named runtime evidence was actually inspected or exercised.

Compose this profile with Concurrency/runtime, SQLite, Ownership/errors,
Unsafe/FFI, Target/platform, or project grounding only when the selected path makes
their claims reachable. Mark every unselected profile `Out of scope`.

## Evidence Model

For every decisive claim, record:

`signal -> invariant -> owner/authority -> path and evidence -> verification state -> disposition -> next action`

Keep evidence categories distinct:

- **Declared:** docs, configuration, comments, or schema intent. It does not prove
  effective execution, authorization, or compatibility.
- **Source-resolved:** current code/build/configuration proves a reachable static
  path at the recorded basis.
- **Automated:** a named test or check exercised the stated seam with known inputs.
- **Artifact-resolved:** generated schema, package, event log, database, or binary
  output was inspected.
- **Runtime-resolved:** an authorized local/target-like/deployed path was exercised;
  qualify the environment and limits.

Do not convert a display ID, type derivation, successful unit test, `cargo check`,
or local loopback bind into identity, authorization, sandbox, recovery, or deployed
IPC evidence. A missing capability, unavailable target, truncated log, or uncertain
operation is a proof gap, not a successful fallback.

## Thread Turn And Operation

Trace the smallest state model that the code actually owns. The names may differ,
but a stateful agent path should make these boundaries observable:

| Level | Audit questions | Minimum evidence |
| --- | --- | --- |
| Thread | What durable workflow/session owns turns? How are pause, resume, completion, failure, and cancellation represented? | Stable identity, owner, persistence boundary, and legal transition tests or source evidence. |
| Turn | What one bounded intent/response is in progress? Who records approval, deadline, result, or cancellation? | One owner and terminal outcome; no accidental duplicate turn on retry. |
| Operation | Which one side effect, tool/IPC write, or durable commit is being attempted? | `operation_id` persisted before the effect; idempotency and attempt policy; `prepared -> invoking -> succeeded|failed|uncertain` or an equivalent explicit model. |

Check that `thread_id`, `turn_id`, and `operation_id` are correlation identities,
not interchangeable display labels. For an uncertain non-idempotent write, look for
bounded read-only reconciliation under the original ID and a stop path; a timeout or
missing response is not evidence of failure. Report duplicate sends, illegal state
transitions, retry without reconciliation, and absent ownership as findings only when
the reachable side effect and impact are established.

If the host or repository uses names such as round, relay turn, or session, map those
existing grouping identifiers to the inspected model. Do not report a naming
difference as architectural drift or recommend a second ledger solely to rename it.

## Typed Protocol And Schema

Identify one authoring authority: repository-native Rust/wire types, a checked schema,
or an existing contract tool. Inspect the route/command/message, DTOs, serializers,
generated markers, generator command/version, compatibility fixtures, consumers, and
CI. Distinguish generated artifacts from hand-maintained copies.

Verify that a durable or cross-process envelope carries the applicable protocol
version, correlation IDs, operation kind, typed payload, and typed error/status. Check
nullability, unknown/open enum handling, size limits, malformed input, version
compatibility, duplicate operations, and error mapping. If schemas or clients are
generated, verify clean repeatability/idempotence and the owning source; otherwise
report generation evidence `Not found` or `Not verified`, not failed.

Do not activate Protocol automation merely because an HTTP endpoint exists. Do not
recommend OpenAPI, `schemars`, a TypeScript client, or another generator without a
real owner, consumer, and validation path.

## Async Lifecycle And Backpressure

When the selected path is async, record runtime flavor/owner, blocking work, task
owner, channel capacity, fan-out/concurrency bound, timeout/retry scope, lock/await
interaction, cancellation source, and shutdown coordinator.

- Establish whether each task is joined, supervised, runtime-owned, or intentionally
  detached, and why that policy matches correctness, resources, durability, shutdown,
  and caller-visible outcomes.
- Check result, returned error, cancellation, and panic observation for responsible
  tasks. Dropping a `JoinHandle` alone is neither proof of a defect nor proof of safe
  detachment.
- Derive bounded queue capacity from item size, burst, throughput, and latency. Verify
  full-channel behavior (await, reject, coalesce, shed, or metric-backed drop) and
  bounded blocking work; `spawn_blocking` is not automatic backpressure.
- For `select!` or restart loops, inspect cancellation safety and whether losing a
  branch can duplicate side effects, lose messages, or corrupt protocol state.
- Verify shutdown stops intake, signals cancellation, waits for critical work under a
  deadline, cleans partial state, and reports unfinished work.

Accept intentional detachment when work is bounded/non-critical, owns no uncontrolled
resource, and failure is irrelevant or independently observable. Do not mandate a
specific token, tracker, channel, or runtime from an external example.

## Approval Policy And Sandbox

Trace three independent layers and their owner:

| Layer | Evidence to inspect | Failure boundary |
| --- | --- | --- |
| Approval | Authorized actor, scope, expiry, persisted decision, and the operation it covers. | Missing/expired/ambiguous approval must stop the high-impact operation. |
| Policy | Rust/domain rule over identity, scope, input, requested effect, and current state. | UI flags, prompt text, or frontend types are not enforcement. |
| Sandbox | Host-enforced capability, filesystem/process/network/resource scope, and target proof. | Rust path checks do not prove a host sandbox; unavailable host evidence is `Not verified`. |

Check that one layer is not being used as a substitute for another. A policy pass
does not create approval or isolation; a sandbox does not decide business
authorization. Report only reachable protected operations, trust boundaries,
counterevidence, and proof gaps.

## Durable Log And Projection

Select this section only when replay, recovery, audit history, or query performance is
part of the requested claim. Establish the source of truth before inspecting files.
If SQLite is already authoritative and no event replay is required, record JSONL as
`Not applicable`, not as missing modernization.

When a JSONL source log exists, inspect stable event ID, sequence, schema version,
event kind, timestamp, correlation IDs, append atomicity, flush/fsync/rotation, one
writer, truncation/corruption handling, and whether events record intent and outcome
separately. When a SQLite projection exists, inspect transaction boundaries,
idempotency by event/sequence, watermark, schema migrations, and whether it is
derived rather than a second writer.

Validate the recovery invariant: a crash between source append and projection commit
can replay deterministically; duplicate delivery does not duplicate state or external
effects; interrupted projection resumes from a durable watermark; supported upgrades,
backup/restore, and corrupt/truncated records have an explicit outcome. A successful
append or one restart test is not full recovery proof. If failure injection, target
runtime, or representative data is unavailable, mark that claim `Not verified`.

## Tauri And Local App-Server IPC

For Tauri, trace command registration, `build.rs`, generated app-command
allow/deny permissions, capability/window/webview assignment, configured resource
scope, Rust domain authorization, typed request/result/error mapping, caller, and
tests. Custom commands registered only through `invoke_handler` are application-wide
by default; do not infer per-window ACL from registration, frontend types, or CSP.
Verify Rust-side validation of paths, URLs, identifiers, payload sizes, and resource
limits. Treat CSP as defense in depth.

For a local app-server, identify the actual transport (loopback HTTP, Unix socket,
named pipe, or host API), bind scope, peer/token/permission checks, request limits,
disconnect/cancellation/deadline behavior, startup/shutdown owner, and target
consumer. A loopback listener is not automatically trusted. Correlate retries and
streamed messages with the same operation identity; do not infer deployed or remote
client proof from static route registration.

When a command crosses Tauri and an app-server, keep platform capability, configured
scope, Rust domain policy, and user approval as separate findings/evidence. Route JS/
TS behavior to its owner and return only the bounded Rust evidence here.

## Audit Sequence And Findings

1. Record revision, Worktree state, project class, selected profiles, excluded
   profiles, and coordinating owner (including `repo-review` when delegated).
2. Build a targeted inventory from entry point through state store, task/channel,
   serializer/schema, approval/policy/sandbox owner, persistence, command/IPC, tests,
   CI, packaging, and runtime configuration. Stop at the requested boundary.
3. Map source-of-truth and legal state transitions before judging architecture.
4. Run non-mutating repository commands and inspect representative artifacts/data;
   keep static, automated, artifact, and runtime evidence separate.
5. Report only evidence-backed findings. Each finding includes severity, exact
   location/path, violated invariant, reachable impact, evidence, counterevidence,
   remediation direction for `dev-rust`, and a `Not verified` proof gap where needed.

Do not edit source, stage, commit, post comments, or create a durable runtime artifact
from audit mode. Do not turn absence of a large runtime design into a finding without
an actual lifecycle, recovery, authorization, or boundary requirement.

## Validation And Report

For a selected Agent Runtime audit, cover only the applicable checks:

- state transition and duplicate/uncertain-operation tests or source evidence;
- protocol envelope, schema authority, malformed/version/compatibility, and clean
  generation evidence when a generator exists;
- overload, cancellation, panic/result observation, deadline, and shutdown evidence
  for selected async paths;
- source-log append/replay/projection idempotence, interruption/restart, migration,
  and backup/recovery evidence for selected durable paths;
- Tauri/app-server authorization, scope, malformed input, disconnect, timeout,
  payload-limit, and target-client evidence for selected IPC paths.

Final report sections are:

```text
Decision and selected Agent Runtime sections:
Inspection snapshot and coordinating owner:
Source-of-truth and owners:
Thread/Turn/Operation state and recovery evidence:
Typed protocol/schema authority and generation:
Async/backpressure/cancellation evidence:
Approval/Policy/Sandbox evidence:
Durable log/projection evidence:
Tauri/local app-server IPC evidence:
Severity-ranked findings with remediation direction:
Excluded profiles: Out of scope
Not found / Not verified evidence:
Residual risks:
```

Do not claim a sandbox, target runtime, deployed IPC, durable recovery, or generated
consumer compatibility gate passed unless its evidence was actually inspected or
executed at the named basis.
