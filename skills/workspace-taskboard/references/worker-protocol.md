# Workspace Taskboard Worker Protocol

## Instruction And Notification

Each worker instruction includes control ID, project/root binding and roots version,
controller ID, exact worker cwd, reuse key, responsibility, authorization profile,
dependencies, and notification protocol. Title is display only.

For completed, blocked, decision-needed, basis-drift, ready-for-delivery, or delivered,
read the current manifest; verify the open mapping, exact worker cwd, project controller,
and both tasks' project-root containment; then emit an idempotent board event before the
worker's full report. Only the registry adapter may atomically re-read the project control
and record it once. A stale digest, controller rebind, or replay records nothing. Never write
a synthetic worker message into the overview conversation, and never notify a predecessor
or closed mapping.

```yaml
type: worker-status
schema_version: workspace-taskboard-worker-status/v1
control_id: <stable ID>
canonical_project_root: <resolved path>
allowed_roots_version: <host readback version>
reuse_key: <project:exact worker cwd:responsibility>
worker_thread_id: <ID>
status: <business semantic state>
event_sequence: <monotonic integer for this worker mapping>
observed_at: <ISO-8601>
worker_basis_digest: <stable digest of this worker identity, project roots, and roots version>
canonical_cwd: <exact worker cwd>
basis: <immutable basis or Not verified>
changed_paths: []
validations: []
external_effects: []
unverified_residual_risks: []
git_state: <live summary or Not verified>
recommended_next_action: <bounded action>
event_kind: <informational|decision|authorization>
last_read_event_sequence: <integer or 0>
```

Host turn `completed` does not mean business `finished` or `delivered`. Status projection
uses only a valid worker envelope for those semantic states.
Card rank, controller succession, or unrelated dependency-edge CAS does not invalidate a
worker envelope. A change to worker cwd, reuse identity, project roots, or roots version
changes `worker_basis_digest` and requires a new envelope.

Informational events update the card and unread marker. Decision events carry the bounded
question, mutually exclusive choices, impacts, and optional recommendation. Authorization
events carry the exact side effect, target, risk, and one-time authorization scope. A panel
choice routes directly to the worker. When the host has no cross-task structured approval,
the panel navigates to the worker's native approval prompt instead of relaying the question
through the overview conversation.

## Dependency Handoff

Edges connect only mapped workers in the same verified project domain. Include producer
repository, branch, immutable head, contract version, changed paths, validations,
unverified boundaries, consumer sync requirements, and forbidden internal copying. The
consumer reads actual source/artifacts; summaries are navigation, not authority.

## Authorization

`implementation` permits source changes/tests but not commit, push, merge, deployment,
or external business writes. `controlled-delivery` adds ordinary fetch, task branch,
commit, integration, local merge, ordinary push, and remote SHA/CI readback; it still
forbids force push, history rewrite, remote deletion, deployment, and external business
writes. External effects require separate explicit authorization. Default delegation and
project containment never expand authority.
