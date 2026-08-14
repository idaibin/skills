# Workspace Taskboard Control Contract

## Manifest

Use `assets/control-manifest.v1.schema.json`. Store only stable control/project IDs,
canonical project root, versioned host-verified allowed roots, current/predecessor
controller IDs, nullable authorization profile, worker mappings, dependency edges,
numeric card rank, panel visibility, and closed policy. A mapping stores exact canonical worker cwd,
responsibility, project identity, task ID, and reuse key. Read titles live. Do not store progress,
Git SHA, test logs, reports, runtime evidence, or task-body copies.

- Owner: `workspace-taskboard` capability contract.
- Producer and non-LLM consumer: configured user-local registry adapter with atomic CAS,
  create-operation reconciliation, and board rank/closed updates outside project repos.
- Version: `workspace-taskboard-control/v1` plus `allowed_roots_version` from host project
  readback.
- Validator: `scripts/task_control.py validate-manifest` and bundled JSON Schema.
- Drift: validate/hash, re-read project/task evidence and registry digest, then CAS;
  mismatch returns `BASIS_DRIFT` without partial mutation.
- Retirement: replace only after an actual successor consumer can migrate and read back
  every active control; because this version is unshipped, no legacy alias/migration is
  provided.

Without a reliable adapter, return `REGISTRY_UNAVAILABLE`, mark persistence Not verified,
and emit a recovery handoff for control operations. Read-only status still returns a
live-only project/task projection without rank, closed policy, controller mapping, or
semantic terminal status. Do not pretend model memory is a registry.

## Multi-project Overview

Keep one validated control manifest per project. An overview stores only ordered references
to those controls plus its own monotonic version; it never copies roots, workers, authority,
or status into a global task pool. Project-column reorder uses overview digest and version
CAS. A stale reorder reloads the overview. Selecting a project emits a one-shot scope token;
the project manifest and host readback remain the routing authority.

The overview task may be pinned in the Codex sidebar. Message content itself is not sticky:
emit the newest panel as the final item of each Taskboard turn instead of claiming permanent
top or bottom positioning.

## Project Membership

Resolve the primary project root and each host-declared attached folder with realpath.
Require a saved local project readback with one per-root membership receipt tied to the
same version as `allowed_roots[]`; a single global boolean is insufficient. Containment is equality or component-aware descendant membership via
the resolved path. Common ancestors, raw string prefixes, titles, project ID alone, and
repository remotes cannot add roots. Any membership/version mismatch stops before send,
create, close, or rebind.

## Resume And Rebind

Read/validate the manifest and project, verify the new controller is a local Codex task
within allowed roots, read every mapping, reconcile current authority, then CAS the
controller ID while preserving predecessors. Rebind every live/completed open worker;
account for delivered/archived/deleted/unavailable/closed workers without sending. Record
send/readback receipts. Failed or uncertain receipt is `rebind-incomplete`, never a
completed takeover. Do not archive predecessors without separate authorization.

## Concurrency And Board Metadata

The adapter owns optimistic CAS (compare-and-swap) for manifest, rank, unread sequence, and
close transitions. Notification returns an idempotent board-event command, never permission
for a direct host send. The adapter atomically reads the current registry, resolves the
project controller, compares the expected manifest digest, and records one event under the
operation ID; a rebind or replay produces no duplicate. Close requires the same freshly read
manifest digest to equal the current registry digest immediately before its side
effect; stale snapshots return `BASIS_DRIFT`. Drag reorder
uses expected manifest digest plus monotonic registry version; a stale version reloads
the board instead of overwriting concurrent order. Closing requires explicit user intent,
host archive, an attributed archive readback (`status=archived` or the host's
`archived=true` receipt combined with verified task project/cwd identity), then CAS
`closed=true`; a bare boolean receipt is insufficient, and failure keeps the card open
or marks the transition unresolved. Closed mappings remain displayable but never reusable,
notifiable, or rebindable.

Hiding a card is a presentation-only CAS transition on `hidden=true`. It never archives,
closes, interrupts, or removes the worker mapping, and hidden workers remain eligible for
verified reuse and dependency handoff. A later explicit show action may set `hidden=false`.

Worker envelopes bind a stable worker status basis made from control/project identity,
verified roots/version, and the worker's reuse identity/cwd/responsibility. Rank,
controller, or unrelated edge CAS does not invalidate semantic status; identity or root
changes do. Persisted canonical worker paths remain lexically valid after their
directory is deleted so archived/unavailable cards stay readable. Every live task path
is still resolved with realpath before reuse, send, close, or rebind.

Creation uses a stable operation from control ID, manifest digest, and reuse key. The
adapter atomically consumes one caller-bound claim and makes exactly one host call.
Replays or submission uncertainty reconcile by list/read; they never issue a second call.
The mapping is finalized only after thread/host/cwd/state readback and scope validation.
