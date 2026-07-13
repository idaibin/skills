# Browser Operation Protocol

This protocol is shared by `chatgpt-review` and `ops-browser`. Each
published package carries the same file so it remains self-contained. Repository
validation must reject any drift between the two copies.

## Capability Snapshot

`ops-browser` measures browser capabilities once for the requested route and
returns this snapshot to the caller. The bridge decides which capabilities are
required; the browser operator never infers authorization from availability.

```yaml
schema_version: browser-operation/v1
snapshot_id: cap-<stable-task-scope>
captured_at: <ISO-8601 or Not verified>
route:
  browser_mode: <desktop-built-in-browser|current-chrome-explicit|standalone-playwright-explicit|manual>
  browser_id: <stable id or Not verified>
  session_id: <stable id or Not verified>
identity:
  account_category: <personal|organization|Not verified>
  workspace_id: <stable id or Not verified>
  account_evidence:
    - <direct evidence or Not verified>
  workspace_evidence:
    - <direct evidence or Not verified>
state_fingerprint:
  login_state: <opaque one-way fingerprint or Not verified>
  target_origin: <origin>
  target_url: <exact URL or Not verified>
browser_profile:
  imported_data: <none|bookmarks|history|saved-credentials|mixed|unknown>
  authentication_state: <active-session-verified|unauthenticated|unknown>
  authentication_evidence: <direct current-route evidence or Not verified>
  session_freshness: <fresh|stale|unknown>
  provenance: <direct-observation|user-stated|tool-reported|unknown>
capabilities:
  session_enumeration: <available|unavailable|unknown>
  tab_control: <available|unavailable|unknown>
  stable_tab_identity: <available|unavailable|unknown>
  authenticated_session_reuse: <available|unavailable|unknown>
  dom_accessibility: <available|unavailable|unknown>
  console: <available|unavailable|unknown>
  network: <available|unavailable|unknown>
  storage: <available|unavailable|unknown>
  screenshot: <available|unavailable|unknown>
  viewport: <available|unavailable|unknown>
  upload: <available|unavailable|unknown>
  download: <available|unavailable|unknown>
  composer_inspection: <available|unavailable|unknown>
  response_completion: <available|unavailable|unknown>
  background_safe: <available|unavailable|unknown>
evidence:
  - <tool result, stable identifier, or direct observation>
gaps:
  - capability: <name>
    reason: <why unavailable or unknown>
```

Reuse a snapshot only while its route, browser/session identity, account and
workspace evidence, login-state fingerprint, target origin, and required
capability evidence remain unchanged. Re-capture after a session break, account
or workspace change, login change, route change, browser reconnect, target
origin change, or capability failure.

Imported browser data is initialization evidence only. Bookmarks and history may
help locate a target, and saved credentials may help a user authenticate, but
none proves an active session, the correct account/workspace, target
conversation identity, authorization, or whether an operation was submitted.
`active-session-verified` requires direct evidence from the current route and
must remain bound to the current login-state fingerprint. It must not be derived
from imported data, autofill, saved credentials, page load, avatar, account
hints, user statements, or stale tool observations.
Record only the category and provenance exposed by the active tool; never inspect
unrelated history or persist imported values. A stale or unknown imported state
requires fresh identity and target verification before any external action.

Fingerprint and identity evidence must be sanitized and non-reversible. Never
store an email address, account or workspace display name, cookie, access token,
session secret, browser profile data, or raw authentication state. Use only the
workspace category, stable non-secret IDs when required, one-way hashes, and
minimal direct evidence labels.

## Handoff Request

The bridge creates the request. `operation_id` identifies one intended
external side effect and must remain unchanged across inspection or a permitted
retry. A new review round or different submit action requires a new ID.

```yaml
schema_version: browser-operation/v1
operation_id: <task>:<round>:<action>
round_id: <stable external-review round id>
attempt: <positive integer; starts at 1>
caller: chatgpt-review
intent: <inspect|navigate|create-conversation|compose|attach|submit|capture-response|cleanup>
authorization:
  external_send: <authorized|not-authorized>
  scope: <exact package, round, and action>
route:
  surface: <standard-chat|project>
  project_or_chat_id: <stable id or Not verified>
  account_workspace: <personal|organization|Not verified>
  browser_mode: <verified mode>
target:
  conversation_id: <stable id|create-one-authorized|Not verified>
  expected_url: <exact URL or Not verified>
artifact:
  path: <path or none>
  sha256: <hash or none>
  sequence: <single|part n/N|final-marker>
capability_snapshot_id: <snapshot_id>
preconditions:
  - <required identity, composer, attachment, or completion state>
expected_postcondition:
  - <observable success evidence>
retry_policy: <never|only-if-no-side-effect-proven>
prior_evidence:
  - <evidence from an earlier attempt or none>
```

## Handoff Result

`ops-browser` returns facts only. It does not change authorization, add rounds,
switch routes, create packages, or decide whether an ambiguous action succeeded.

```yaml
schema_version: browser-operation/v1
operation_id: <same request id>
round_id: <same request round id>
attempt: <same request attempt>
capability_snapshot_id: <same snapshot id>
state: <preflighted|ready|created|attached|submitted|acknowledged|captured|cleaned|completed|failed-before-submit|blocked|ambiguous>
before:
  - <verified target/composer/attachment state>
action:
  attempted: <yes|no>
  description: <exact low-level action>
side_effect:
  observed: <yes|no|unknown>
  evidence: <direct evidence or Not verified>
after:
  - <verified URL, attachment, acknowledgement, response, or cleanup state>
retained_evidence:
  - <identifier or path>
cleanup:
  - <removed or retained task state>
error:
  kind: <none|capability|identity|composer|attachment|submission|completion|interruption>
  detail: <sanitized detail>
```

## Operation State Machine

The bridge records the previous state before accepting a result. Legal
transitions are:

| From | Allowed next states |
| --- | --- |
| `prepared` | `preflighted`, `blocked` |
| `preflighted` | `ready`, `blocked` |
| `ready` | `created`, `attached`, `submitted`, `captured`, `cleaned`, `failed-before-submit`, `blocked`, `ambiguous` |
| `created` | `acknowledged`, `completed`, `ambiguous` |
| `attached` | `acknowledged`, `completed`, `ambiguous` |
| `submitted` | `acknowledged`, `completed`, `ambiguous` |
| `acknowledged` | `completed`, `ambiguous` |
| `captured` | `completed`, `ambiguous` |
| `cleaned` | `completed`, `ambiguous` |
| `completed` | terminal |
| `failed-before-submit` | `ready` only for a new attempt with the same operation ID, incremented `attempt`, bridge authorization, and proof of no side effect; otherwise stop |
| `blocked` | terminal until required evidence or authority changes |
| `ambiguous` | terminal until the original target is reconciled; never retry directly |

`failed-before-submit`, `blocked`, and `ambiguous` stop the current attempt.
`blocked` and `ambiguous` stop the operation. `failed-before-submit` ends only
the attempt; the bridge may authorize `failed-before-submit -> ready` with the
same operation ID and incremented `attempt` after direct proof that no external
side effect occurred. The bridge keeps an operation ledger keyed by
`operation_id` and attempt number:

- create the ledger entry before delegating any state-changing browser action;
- assign a distinct operation ID to conversation creation, attachment, submit,
  final marker, and other external side effects;
- record the latest capability snapshot, request, result, and evidence;
- never issue a second submit for an ID already marked `submitted`,
  `acknowledged`, or `completed`;
- after interruption, inspect the same route and target for the expected
  postcondition before deciding whether the first action occurred;
- retry with the same ID only from `failed-before-submit` and only when direct
  evidence proves no external side effect occurred;
- mark uncertain submission state `ambiguous` and stop for reconciliation;
- use a new ID only for a genuinely new authorized action, never to bypass an
  ambiguous or already-submitted operation.

One `round_id` groups the many operation IDs that make up an external review
round. A round is complete only when every required package/send operation is
completed and its attributed response-capture operation is completed. Creating
a conversation is a separate state-changing operation; interruption after
creation is reconciled against the original Project before any new conversation
can be authorized.

## Degraded Mode

If a required capability is unavailable or unknown, return `blocked` without
the action and name the missing capability. If interruption prevents proving
whether a side effect occurred, return `ambiguous`; do not retry, switch
routes, or create a replacement conversation. Package-only work remains
available when external browser operation cannot be proven.
