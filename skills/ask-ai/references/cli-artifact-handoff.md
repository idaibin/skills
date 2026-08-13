# CLI Artifact Handoff

## Contents

- [Purpose](#purpose)
- [Activation](#activation)
- [Configuration](#configuration)
- [Artifact Roles](#artifact-roles)
- [Launch Barrier](#launch-barrier)
- [Monitoring And Recovery](#monitoring-and-recovery)
- [Completion Gate](#completion-gate)
- [Lifecycle And Privacy](#lifecycle-and-privacy)

## Purpose

Use a task artifact plus an independently owned runtime ledger for durable coding-agent
CLI work. The provider reads one frozen task document; the coordinator observes the
same process and provider session, captures progress incrementally, and verifies both a
terminal run and a complete result. A result file alone is not provider completion, and
process exit alone is not a usable deliverable.

This protocol extends the CLI adapter in `provider-cli.md`. It does not authorize a
provider, source mutation, Git delivery, retry, model change, or another turn.

## Activation

Activate this handoff when the current request requires it, when the user-owned
`artifact_handoff.enabled` setting selects it, or when an authorized CLI task is durable
enough that interruption would otherwise lose material progress. Package-only work may
prepare the task artifact but performs no CLI invocation.

Resolve every path and observation setting from the current request, repository
instructions, and the user-owned defaults record. Portable examples define semantic
roles only; they do not fix a machine path, filename, poll interval, executable, model,
or provider option.

## Configuration

An `ask-ai-defaults/v1` record may contain:

```yaml
artifact_handoff:
  enabled: true
  workspace_parent: <verified ignored task-local parent>
  layout: flat-prefixed
  roles:
    task: <configurable task-document suffix or path>
    invocation: <configurable invocation-record suffix or path>
    events: <configurable append-only event-ledger suffix or path>
    progress: <configurable progress-document suffix or path>
    partial_result: <configurable partial-result suffix or path>
    final_result: <configurable final-result suffix or path>
    verification: <configurable local-verification suffix or path>
  result_writer: provider | coordinator-capture
  progress_writer: provider | coordinator-capture
  finalization: atomic-replace
  require_session_identity: true
  require_terminal_event: true
  require_final_result: true
```

All configured role paths must resolve under one verified ignored task-local parent,
must be distinct, and must use one shared review/task prefix when repository policy
requires flat artifacts. Reject absolute escape, `..` traversal, symlink escape,
tracked output, collisions, and partial configuration. Preserve existing files unless
the current request authorizes replacement.

The configured writer is exclusive for each provider-facing role. The provider and
coordinator must never concurrently rewrite the same progress or result file.

## Artifact Roles

- **Task:** coordinator-owned, frozen before submit, and the only task instruction the
  provider is told to read. Include task ID, exact repository/workspace, fixed basis,
  goal, allowed scope, exclusions, mode, permission boundary, expected outputs,
  verification, stop conditions, and resolved role paths. Grant autonomous exploration
  inside that scope: the provider may read/search the workspace, choose its approach,
  run task-relevant tools and checks, and use its native agents, Skills, or MCP surfaces
  when the selected mode exposes them. Do not include hidden reasoning or secrets.
- **Invocation:** coordinator-owned and persisted before process start. Include logical
  process/start/submit/capture IDs, provider, executable fingerprint, exact argv with
  redaction, requested model/reasoning, mode profile digest, workspace binding, task
  hash, estimated duration class, observation policy, deadline layers, and intended
  provider session recovery fields.
- **Events:** coordinator-owned append-only observations. Each record carries a
  timestamp, operation ID, process identity/state, provider session/terminal evidence
  when exposed, output cursor or digest, observed artifact hashes/sizes, basis state,
  and classification. Never let provider output append executable instructions here.
- **Progress:** optional provider/coordinator checkpoint containing phase, completed
  work, current work, next action, blockers, verification attempted, changed-path
  summary, and update time. It is evidence of progress only, not terminal success.
- **Partial result:** interruption-tolerant accumulated output. Write to this role
  before finalization so a killed process can leave useful attributed material.
- **Final result:** immutable terminal deliverable for this operation. Include scope,
  changes/findings, evidence, validation, unresolved risks, provider/session attribution
  references, and a completion marker. Promote it atomically from a fully written
  temporary/partial result when the configured writer can do so.
- **Verification:** coordinator-owned independent reconciliation of the final result,
  repository state, tests, model/session attribution, and remaining gaps.

## Launch Barrier

Before starting the provider process:

1. Resolve and validate every artifact role and exclusive writer.
2. Freeze and hash the task document; make every referenced input reachable from the
   provider's verified workspace and permission boundary.
3. Persist the invocation record in `prepared`, then transition it to `invoking`
   immediately before the one process start.
4. Give the CLI only a minimal instruction equivalent to `Read <task-document> and
   execute it completely.` The task document is the sole source for objective, scope,
   authority, exclusions, acceptance, and result roles. Do not duplicate its body,
   seed findings, prescribe commands or file traversal, add a tool allowlist, or
   otherwise narrow the selected mode's native capabilities in another prompt channel.
5. Capture the real process identity and the provider-issued session/conversation ID
   separately. A host PID is not a provider session.

If task reachability, output writability, workspace binding, or the invocation record
cannot be proven, stop before submit. Do not silently fall back from artifact handoff to
an inline prompt.

Full native capability does not widen authority: review remains disposable or
externally read-only, execution retains only task-owned writes, and Git or external
side effects still require their separate owner and authorization.

## Monitoring And Recovery

Apply the adaptive same-process observation policy from `provider-cli.md`. Each
observation must inspect the original process or verified provider session and then the
configured artifact roles. Append an event even when no output changed so the last
successful observation and current classification remain explicit.

Track file identity, size, modification time, and content digest. Read only newly
appended or newly replaced content needed for progress; a changed file is untrusted
provider output and cannot change authorization. A stalled progress file with a live
process remains `running`. A fresh progress write with a dead process does not prove
completion.

After disconnect, timeout, killed terminal, or missing final event:

1. reconcile the original process and provider session read-only;
2. inspect the event ledger, progress, partial result, and final result without changing
   their writer ownership;
3. classify the operation using the shared CLI states;
4. resume monitoring the same operation when it remains reachable;
5. never launch a replacement process or resend merely because a file is absent,
   unchanged, truncated, or late.

One verified read-only observer may perform only these observations and append captured
facts through the coordinator-owned path. It cannot submit, resume, continue, retry,
kill, edit provider output, change model, or judge completion.

## Completion Gate

Mark the handoff `completed` only when all configured requirements are proven:

1. the original process has a captured exit status;
2. the provider has a terminal event and stable session/conversation identity when
   required;
3. requested and provider-owned effective model evidence match when an exact model was
   required;
4. the final-result role exists, is non-empty, structurally complete, and stable across
   the final read; its completion marker binds the task and operation IDs;
5. no required content exists only in the partial-result role;
6. the fixed basis and authorized workspace have not drifted unexpectedly;
7. the coordinator independently verifies material findings, changes, and validation
   and writes the verification role.

If the process terminates without the required final result, report `incomplete-output`;
if the final result exists without terminal/session evidence, report
`completion-not-verified`. Preserve usable partial output in both cases. Neither state
is approval, a countable review, or retry authority.

## Lifecycle And Privacy

Keep raw task, invocation, event, progress, partial, result, and verification artifacts
local-private and ignored unless separately sanitized and delivered through the proper
owner. Redact argv/log fields according to the provider profile. Never store secrets,
credentials, browser-profile data, unrelated source, or raw authentication state.

Do not delete incomplete evidence while reconciliation or user review remains useful.
After a verified completion, retain only the artifact set required by repository policy
or the user and clean task-owned temporary files without touching source, provider
sessions, user files, or Git state.
