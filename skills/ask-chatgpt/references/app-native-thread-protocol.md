# App-Native Thread Operation Protocol

## Contents

- [Scope](#scope)
- [Ledger Schema](#ledger-schema)
- [Operation State Machine](#operation-state-machine)
- [Completion State Machine](#completion-state-machine)
- [Identity Reconciliation](#identity-reconciliation)
- [Follow-Up Reconciliation](#follow-up-reconciliation)
- [Recovery And Retry Rules](#recovery-and-retry-rules)
- [Round Completion](#round-completion)

## Scope

Use `app-native-thread-operation/v1` only for host-exposed ChatGPT Project/thread
operations. It is independent from `browser-operation/v1`, which remains the sole
protocol for browser actions. Persist one ledger under the task's ignored review
directory before any App-native state change.

The supported operation types are:

- `create-and-initial-submit`: one `create_thread` call that creates the conversation
  and submits the initial prompt;
- `follow-up-message`: one separately authorized `send_message_to_thread` call against
  an already resolved conversation.

Never model response reads as external state changes. Record bounded `read_thread`
evidence in the same ledger's completion fields.

## Ledger Schema

```yaml
schema_version: app-native-thread-operation/v1
review_id: <stable local review id>
round_id: <one authorized external round>
operation_id: <unique intended state change>
operation_type: <create-and-initial-submit|follow-up-message>
attempt: <positive integer>
state: <prepared|invoking|submitted|submission-uncertain|blocked>
call:
  tool: <create_thread|send_message_to_thread>
  count: <0|1>
  window:
    started_at: <timestamp>
    ended_at: <timestamp|null>
project:
  id: <stable host Project id>
  identity_evidence: <sanitized direct evidence or Not verified>
conversation:
  client_thread_id: <id|null>
  thread_id: <id|null>
identity:
  state: <not-started|client-pending|resolved|identity-not-verified>
  evidence: <direct sanitized evidence or Not verified>
prompt:
  sha256: <sha256>
  path: <ignored local path or inline-inspected>
before:
  observed_at: <timestamp|null>
  last_message_id: <id|null>
  message_or_turn_count: <non-negative integer|null>
completion:
  state: <not-started|response-pending|captured|completion-not-verified>
  read_bound: <count or deadline>
  reads_used: <non-negative integer>
  response_evidence: <attributed evidence or Not verified>
reconciliation:
  status: <not-needed|pending|unique-match|no-match|multiple-matches|Not verified>
  evidence: <direct sanitized evidence>
model_reasoning_evidence: <direct metadata or Not verified>
updated_at: <timestamp>
```

For `follow-up-message`, require `conversation.thread_id` before `invoking`, set
`call.tool: send_message_to_thread`, capture the latest exposed message ID or
message/turn count in `before`, and do not reuse the initial-submit operation ID.

## Operation State Machine

Persist every transition before the next external action. Legal transitions are:

| From | Allowed next states |
| --- | --- |
| `prepared` | `invoking`, `blocked` |
| `invoking` | `submitted`, `submission-uncertain` |
| `submission-uncertain` | `submitted` only after later direct evidence proves the same operation submitted |
| `blocked` | `prepared` only after authority/capability evidence changes and the state-changing call count is still `0`; increment `attempt` |
| `submitted` | terminal for the external state change; use completion state for response capture |

Before the selected state-changing call, persist `prepared`, then persist `invoking`
and set `call.count: 1`. A process that resumes from `invoking` must treat submission
as `submission-uncertain` and enter reconciliation; it must not call the state-changing
tool again.

`submission-uncertain` stops the bounded execution without proving failure. Later
read-only evidence may resolve the same operation to `submitted`; it never authorizes
a new conversation, prompt resend, transport switch, or replacement operation ID.

Track conversation identity separately from submission state:

| From | Allowed next identity states |
| --- | --- |
| `not-started` | `client-pending`, `resolved`, `identity-not-verified` |
| `client-pending` | `resolved`, `identity-not-verified` |
| `identity-not-verified` | `resolved` only after later direct unique evidence for the same operation |
| `resolved` | terminal |

A normal `create_thread` return containing only `clientThreadId` produces operation
`submitted` plus identity `client-pending`. Identity failure never regresses the known
submission state or grants retry permission.

## Completion State Machine

Completion starts only after `submitted`:

| From | Allowed next states |
| --- | --- |
| `not-started` | `response-pending` |
| `response-pending` | `captured`, `completion-not-verified` |
| `completion-not-verified` | `captured` only when a later attributed response appears in the same conversation |
| `captured` | terminal |

`completion-not-verified` ends the current bounded read, not the review round and not
the external operation's submission. It never grants retry permission.

## Identity Reconciliation

Resolve `client_thread_id` to one real conversation using, in order:

1. a direct host link between client and conversation identifiers;
2. one unique candidate in the same Project matching the persisted call window
   and prompt/task fingerprint.

Title alone is insufficient. Zero or multiple candidates set identity to
`identity-not-verified` without changing a confirmed `submitted` operation. Preserve
the original Project, operation ID, prompt hash, call window, and candidate evidence
for a later read-only reconciliation.

## Follow-Up Reconciliation

For an interrupted or result-less `send_message_to_thread`, inspect only the already
resolved original conversation. Accept submission only from:

1. a direct host operation/message identifier tied to this operation; or
2. exactly one new user message after the persisted `before` marker whose complete
   normalized content hash matches `prompt.sha256` and whose timestamp falls inside the
   persisted call window.

If the host omits complete message content, timestamps, or a stable before/after marker,
or if zero or multiple messages match, keep the operation `submission-uncertain` and
record reconciliation `Not verified`, `no-match`, or `multiple-matches`. Thread activity,
title changes, message count alone, or a later assistant response without an attributed
matching user message is insufficient. Never resend the follow-up.

After a unique follow-up match, move the operation to `submitted`; capture completion
only from an assistant response attributable to that matched user message. An absent
response becomes `response-pending` and then `completion-not-verified` at the read bound,
never retry permission.

## Recovery And Retry Rules

- The initial `create_thread` call count must remain at most `1` for the operation.
- Missing return data, disconnect, timeout, client restart, or absent assistant output
  never proves that submission failed.
- Resume `invoking`, `submission-uncertain`, `client-pending`, or
  `identity-not-verified` by inspecting the original Project only; never call
  `create_thread` or resend the prompt.
- Retry from `blocked` only when no state-changing call began, the same authorization
  remains valid, changed evidence removes the blocker, and `attempt` is incremented.
- A follow-up requires its own authorization and operation ID. Never use it to repair
  or repeat the initial prompt.

## Round Completion

The App-native round is complete only when every authorized state-changing operation
is `submitted`, required conversation identity is `resolved`, and the required response
is `captured`. If submission is uncertain, identity is unresolved, or completion is
`completion-not-verified`, report the local review verdict separately and keep the
external round `Not verified`.
