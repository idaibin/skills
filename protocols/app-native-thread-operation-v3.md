# App-Native Thread Operation Protocol

## Contents

- [Scope](#scope)
- [Capability Preflight](#capability-preflight)
- [Ledger Schema](#ledger-schema)
- [Prompt Fingerprint And Readback](#prompt-fingerprint-and-readback)
- [Operation State Machine](#operation-state-machine)
- [Completion State Machine](#completion-state-machine)
- [Identity Reconciliation](#identity-reconciliation)
- [Follow-Up Reconciliation](#follow-up-reconciliation)
- [Recovery And Retry Rules](#recovery-and-retry-rules)
- [Round Completion](#round-completion)

## Scope

Use `app-native-thread-operation/v3` only for host-exposed ChatGPT Project/Quick Chat
operations whose capability preflight has passed. It is independent from
`browser-operation/v1`, which remains the sole protocol for browser actions. Persist
one ledger under the task's ignored review directory before any App-native state
change.

Existing `app-native-thread-operation/v1` and `app-native-thread-operation/v2` ledgers
remain valid only for read-only recovery. Resume the same operation ID, legacy `call.count`, prompt hash, call window,
Project/Quick Chat scope, submission state, and candidate evidence. Never migrate a
legacy uncertain operation into a new v3 state-changing operation and never resend it.
A recovery implementation may attach v3 preflight/read-bound evidence as an extension
to the same ledger, but must preserve its original `schema_version` and idempotency
identity.

One relay turn owns a stable `round_id`, `relay_turn_id`, and a list of logical
operations. `create_thread` may atomically create the conversation and submit the
initial message, but that host call must correlate distinct logical `create-conversation`
and `submit-initial` operation IDs. `capture-response` is a separate, read-only,
idempotent logical operation. A later turn against the verified conversation has no
create operation: it records only `submit-follow-up` and `capture-response`.

## Capability Preflight

Before `prepared`, record a fresh read-only capability snapshot from the exact host:

- required operations and exact `create_thread.target` variants from live schemas;
- sanitized `list_projects` and `list_threads` evidence, including the explicit
  `unavailableSources` value;
- ChatGPT source state: `active`, `activation-required`, `inconsistent`, or
  `Not verified`;
- requested surface: `project`, `quick-chat`, or `standard-chat`;
- exact target mapping or `none`;
- browser fallback state before submission.
- the maximum complete user-message content that `read_thread` can return, plus a
  bounded list/page/candidate/read plan for reconciliation.

Only `active` plus a legal mapping may advance to `prepared`. A verified ChatGPT
Project requires `projectKind: chatgpt` and maps to `chatgptWorkCloud` with its exact
`projectId`. Quick Chat requires an explicit current request and maps to
`chatgptWorkCloud` without `projectId`. Generic Standard Chat has no mapping on the
current host schema. `project` and `projectless` are Codex targets and never satisfy
this protocol.

If the exact canonical prompt cannot be fully returned by `read_thread` within the
live per-item limit, App-native cannot safely reconcile an identity-less create.
Before submission, use an authorized browser route that can prove the conversation
identity or stop at Package-only. Do not truncate the prompt merely to make Native
reconciliation pass.

When the ChatGPT source is absent or `unavailableSources` contains `chatgpt`, require
the user to open or switch to ChatGPT/Quick Chat once, then rerun both read-only list
calls. Do not create a ledger operation or submit while activation is pending.

## Ledger Schema

```yaml
schema_version: app-native-thread-operation/v3
review_id: <stable local review id>
round_id: <one authorized external round>
relay_turn_id: <one sequential provider turn>
provider: <chatgpt>
preflight:
  observed_at: <timestamp>
  host_schema_fingerprint: <opaque hash>
  required_operations: <verified|missing>
  chatgpt_source: <active|activation-required|inconsistent|Not verified>
  source_evidence: <sanitized direct evidence>
  requested_surface: <project|quick-chat|standard-chat>
  target:
    type: <chatgptWorkCloud|null>
    project_id: <stable ChatGPT Project id|null>
  mapping_evidence: <sanitized direct evidence or Not verified>
  browser_fallback: <available|unavailable|Not verified>
operations:
  - operation_id: <unique logical create|submit|capture action>
    kind: <create-conversation|submit-initial|submit-follow-up|capture-response>
    state: <prepared|invoking|submitted|submission-uncertain|response-pending|captured|completion-not-verified|blocked>
    attempt: <positive integer; starts at 1>
    idempotent: <true for capture-response; false otherwise>
    host_call:
      tool: <create_thread|send_message_to_thread|read_thread>
      correlation_id: <one persisted host-call correlation id>
      count: <0|1 for writes; bounded for reads>
      window:
        started_at: <timestamp>
        ended_at: <timestamp|null>
project:
  id: <stable ChatGPT Project id|null for Quick Chat>
  identity_evidence: <sanitized direct evidence or Not verified>
conversation:
  client_thread_id: <id|null>
  thread_id: <id|null>
identity:
  state: <not-started|client-pending|resolved|identity-not-verified>
  evidence: <direct sanitized evidence or Not verified>
prompt:
  hash_scheme: prompt-text/v1
  sha256: <sha256>
  utf8_bytes: <non-negative integer>
  characters: <non-negative integer>
  path: <ignored local path or inline-inspected>
  readback_limit_characters: <positive integer>
  complete_readback_possible: <true|false>
before:
  observed_at: <timestamp|null>
  last_message_id: <id|null>
  message_or_turn_count: <non-negative integer|null>
completion:
  read_bound: <count or deadline>
  reads_used: <non-negative integer>
  response_evidence: <attributed evidence or Not verified>
reconciliation:
  status: <not-needed|pending|unique-match|no-match|multiple-matches|Not verified>
  list_page_bound: <positive integer>
  list_pages_used: <non-negative integer>
  list_bound_exhausted: <true|false|Not verified>
  candidate_bound: <positive integer>
  candidate_read_bound: <positive integer>
  candidate_reads_used: <non-negative integer>
  candidate_bound_exhausted: <true|false|Not verified>
  truncation_seen: <true|false|Not verified>
  evidence: <direct sanitized evidence>
model_reasoning_evidence: <direct metadata or Not verified>
updated_at: <timestamp>
```

For `submit-follow-up`, require `conversation.thread_id` before `invoking`, capture
the latest exposed message ID or message/turn count in `before`, and do not reuse an
initial submit ID. `capture-response` has its own operation ID and may be resumed with
the same ID after interruption because it is read-only; it never authorizes resend.

## Prompt Fingerprint And Readback

`prompt-text/v1` canonicalizes only line endings: replace CRLF and bare CR with LF.
Preserve every other Unicode code point, whitespace character, and final newline.
Encode that canonical string as UTF-8 without a byte-order mark, send that exact
canonical string as the host tool's `prompt`, and record SHA-256, UTF-8 byte length,
and Unicode character count before `invoking`.

Use the same scheme for initial and follow-up prompts. Never hash a path, title,
summary, truncated preview, JSON wrapper, or a differently normalized copy.
Reconciliation accepts content only when the complete returned user message has the
same scheme, hash, byte length, and character count. A missing/truncated content flag,
content length beyond the recorded readback limit, or an inability to request the
complete message prevents a match and keeps the operation uncertain.

Persist the list/page, candidate, and candidate-read bounds before the first
reconciliation read. Reaching any bound ends that bounded attempt as `no-match` or
`Not verified`; it never grants retry permission.

## Operation State Machine

Apply this state machine independently to each write operation in the relay turn. The
first `create_thread` call has one host-call correlation ID shared by exactly two
logical records: `create-conversation` and `submit-initial`. Persist both records as
`prepared`, then both as `invoking`, before that one call. A normal return marks both
`submitted`; an uncertain return marks both `submission-uncertain`. It is still called
at most once. Do not merge their logical operation IDs or mistake the atomic host call
for permission to retry either action. `capture-response` is not a state-changing call:
it has its own read-only, idempotent logical operation ID and moves between `prepared`,
`response-pending`, `captured`, and `completion-not-verified` under its persisted read
bound.

Persist every transition before the next external action. Legal transitions are:

| From | Allowed next states |
| --- | --- |
| `prepared` | `invoking`, `blocked` |
| `invoking` | `submitted`, `submission-uncertain` |
| `submission-uncertain` | `submitted` only after later direct evidence proves the same operation submitted |
| `blocked` | `prepared` only after authority/capability evidence changes and the state-changing call count is still `0`; increment `attempt` |
| `submitted` | terminal for the external state change; use completion state for response capture |

Before a selected state-changing call, persist its logical `prepared`, then logical
`invoking`, and set the correlated `host_call.count: 1`. For atomic `create_thread`,
do this to both correlated write records and project one normal or uncertain host result
to both. A process that resumes from `invoking` must treat the affected logical writes
as `submission-uncertain` and enter reconciliation; it must not call the state-changing
tool again.

`prepared` is illegal when `preflight.chatgpt_source` is not `active`, the requested
surface has no exact Native mapping, or the mapped target does not match the recorded
live schema. A later activation or schema change requires a fresh preflight snapshot;
it does not repair or authorize a previously started operation.

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

A normal `create_thread` return containing only `clientThreadId` produces both logical
`create-conversation: submitted` and `submit-initial: submitted`, plus identity
`client-pending`. `client-pending` belongs only to the independent identity machine;
identity failure never regresses either known submission state or grants retry permission.

## Completion State Machine

The distinct `capture-response` operation starts only after the corresponding submit is
`submitted` and uses its own operation state:

| From | Allowed next states |
| --- | --- |
| `prepared` | `response-pending`, `blocked` |
| `response-pending` | `captured`, `completion-not-verified` |
| `completion-not-verified` | `captured` only when a later attributed response appears in the same conversation |
| `captured` | terminal |

`completion-not-verified` ends the current bounded capture, not the review round and
not the external operation's submission. It never grants retry permission; a later
bounded read reuses the capture operation ID.

## Identity Reconciliation

Resolve `client_thread_id`, or a missing identity after an uncertain create return, to
one real conversation using, in order:

1. a direct host link between client and conversation identifiers;
2. a bounded candidate set from `kind: chatgpt`, the same Project when applicable,
   the persisted call window, and prompt/task discovery hints, followed by read-only
   `read_thread` inspection using the initial user-message timestamp rather than the
   thread's later activity timestamp;
3. exactly one candidate whose complete initial user message hash matches
   the full `prompt-text/v1` fingerprint and whose timestamp falls inside the
   persisted call window.

Title, summary, recency, screenshot presence, or Project membership alone is
insufficient. Zero or multiple content-confirmed candidates set identity to
`identity-not-verified` without changing a confirmed `submitted` operation. Preserve
the original Project or projectless Quick Chat scope, operation ID, prompt hash, call
window, and candidate evidence for a later read-only reconciliation.

Candidate scope is exact: Project reconciliation accepts only the recorded
`projectId`; projectless Quick Chat accepts only candidates whose `projectId` is
absent/null. A missing or non-boolean content-completeness/truncation flag is
`Not verified`, never equivalent to `truncated: false`. Any in-scope truncated or
completeness-unknown candidate prevents a uniqueness claim for that bounded read.

An HTML attestation/challenge response from `create_thread` is a result-less,
possibly-side-effecting return. Record `submission-uncertain`; do not classify it as
failed-before-submit. If the ChatGPT source is unavailable, a later user activation
may restore only the read-only list/read reconciliation path. It never permits resend,
a replacement operation ID, or a browser-created replacement conversation.

## Follow-Up Reconciliation

For an interrupted or result-less `send_message_to_thread`, inspect only the already
resolved original conversation. Accept submission only from:

1. a direct host operation/message identifier tied to this operation; or
2. exactly one new user message after the persisted `before` marker whose complete
   `prompt-text/v1` fingerprint matches the ledger and whose timestamp falls inside
   the persisted call window.

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
  `identity-not-verified` by inspecting only the original Project or projectless
  Quick Chat candidate scope; never call `create_thread` or resend the prompt.
- Resume a v1 or v2 uncertain ledger under its original schema and operation identity.
  Missing legacy preflight fields restrict recovery to bounded read-only inspection;
  they never authorize a v3 replacement operation.
- Browser fallback is legal only before a state-changing App-native call, or for
  read-only inspection of the same proven conversation after an uncertain call. It
  never authorizes resubmission or replacement.
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

The validator reads this compact fixture to prevent a host-level atomic
`create_thread` call from collapsing the review-round -> relay-turn -> logical-operation
ledger hierarchy:

```yaml
app_native_relay_contract:
  schema_version: app-native-thread-operation/v3
  hierarchy:
    review_round: round_id
    relay_turn: relay_turn_id
    operation: logical-operation-id
  initial_turn:
    host_call: create_thread
    create_submit_atomic: true
    host_call_correlation: required
    logical_operations: [create-conversation, submit-initial, capture-response]
    logical_write_projection:
      before_host_call: invoking
      normal_host_return: submitted
      uncertain_host_return: submission-uncertain
  later_turn:
    require_same_verified_conversation: true
    create_operation: forbidden
    logical_operations: [submit-follow-up, capture-response]
  capture_response:
    state_change: false
    idempotent: true
    operation_id: required
```
