# Browser Operation Protocol

This protocol is shared by `ask-ai` and `ops-browser`. Repository authors
maintain its canonical source at `protocols/browser-operation-v1.md` and use the
synchronization script to copy it into each published package, so installed
skills remain self-contained. Repository validation rejects stale or modified
generated copies.

## Contents

- [Capability Snapshot](#capability-snapshot)
- [Handoff Request](#handoff-request)
- [Handoff Result](#handoff-result)
- [Attachment Failure Evidence](#attachment-failure-evidence)
- [Stable Response Evidence](#stable-response-evidence)
- [Operation State Machine](#operation-state-machine)
- [Degraded Mode](#degraded-mode)

## Capability Snapshot

`ops-browser` measures browser capabilities once for the requested route and
returns this snapshot to the caller. The bridge decides which capabilities are
required; the browser operator never infers authorization from availability.

```yaml
schema_version: browser-operation/v1
snapshot_id: cap-<stable-task-scope>
captured_at: <ISO-8601 or Not verified>
route:
  provider: <chatgpt|gemini|deepseek|kimi|other|not-applicable>
  browser_mode: <codex-in-app-browser|user-local-browser|desktop-built-in-browser|current-chrome-explicit|chatgpt-cloud-browser|standalone-playwright-explicit|isolated-managed-session|manual>
  browser_name: <user-selected browser product or not-applicable>
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
  session_selection: <available|unavailable|unknown>
  stable_session_identity: <available|unavailable|unknown>
  group_enumeration: <available|unavailable|unknown>
  group_selection: <available|unavailable|unknown>
  stable_group_identity: <available|unavailable|unknown>
  group_creation: <available|unavailable|unknown>
  group_placement: <available|unavailable|unknown>
  tab_control: <available|unavailable|unknown>
  stable_tab_identity: <available|unavailable|unknown>
  managed_session_creation: <available|unavailable|unknown>
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
  preconnected_browser_control: <available|unavailable|unknown>
  prepared_endpoint_available: <available|unavailable|unknown>
  background_safe_transport_reconnect: <available|unavailable|unknown>
  background_safe_browser_setup: <available|unavailable|unknown>
  background_safe_tab_enumeration: <available|unavailable|unknown>
  background_safe_page_control: <available|unavailable|unknown>
  cdp_loopback_only: <available|unavailable|unknown>
  cdp_dedicated_profile: <available|unavailable|unknown>
  cdp_prelock_roundtrip_verified: <available|unavailable|unknown>
  dedicated_profile_identity: <available|unavailable|unknown>
  loopback_endpoint_ready: <available|unavailable|unknown>
  deterministic_automation: <available|unavailable|unknown>
  agentic_navigation: <available|unavailable|unknown>
  direct_cdp: <available|unavailable|unknown>
evidence:
  - <tool result, stable identifier, or direct observation>
gaps:
  - capability: <name>
    reason: <why unavailable or unknown>
```

Use `chatgpt-cloud-browser` for the ChatGPT cloud/agent browser surface and
`isolated-managed-session` for an agent-owned managed session whose state does
not come from a user browser profile.
Use `codex-in-app-browser` for the host-controlled Codex browser and
`user-local-browser` only for the exact browser product resolved by the current
request or durable preference. Existing `desktop-built-in-browser` and
`current-chrome-explicit` values remain valid for read-only recovery; normalize them
to `codex-in-app-browser` or a named `user-local-browser` before a new action.

Reuse a snapshot only while its route, browser/session identity, account and
workspace evidence, login-state fingerprint, target origin, and required
capability evidence remain unchanged. Re-capture after a session break, account
or workspace change, login change, route change, browser reconnect, target
origin change, or capability failure.

For a user-local route whose acceptance depends on foreground safety, retain one
ordered pre-action evidence chain. The local-workspace preflight must finish before
the requested page operation. If the exact background-safe operation can only be
established by a live canary, first require a ready preflight and an identity-matched
existing target, then run one non-mutating canary through the same profile, endpoint,
target, and backend. Capture or refresh the Capability Snapshot after that canary and
before the requested operation. The fixed evidence package must preserve timestamps,
the preflight input/result and exit state, canary method/result, snapshot ID, target
identity, requested action, after-state, and cleanup. A preflight or snapshot produced
after the requested operation cannot retroactively verify that operation.

For a configured user-local-browser workspace, a group label observed on a tab is
not group enumeration or stable group identity. Require independent session and
group enumeration, stable IDs, exact selection, and placement control whenever the
resolved policy requires verified reuse or placement. If any required capability is
`unavailable` or `unknown`, return `blocked` with `capability-unavailable` before
`nameSession`, tab creation, group creation, navigation, or page operation. A browser
reconnect invalidates evidence bound to the prior browser ID and requires a fresh
snapshot; matching display names never bridge the two identities.

Local Chrome control-session and tab-group policy applies only to
`user-local-browser`. It never applies to the Codex in-app Browser, cloud/agent
browser, or an isolated managed browser. A locked local route reuses or reconnects
first. When the validated policy permits browser launch and debug initialization,
`background_safe_browser_setup` may authorize exactly one dedicated-profile background
setup before page action. It must not unlock or wake the screen, activate or foreground
a window, import profile state, or use GUI input. The preflight returns `setup-required`
and permits only `background_browser_setup`; after the attempt, recapture all capability
and identity evidence and rerun preflight. A failed attempt is not retried. Direct CDP
requires a loopback-only endpoint and dedicated automation profile; require a pre-lock
round trip only when the active policy sets `require_prelock_roundtrip: true`.

When an enabled configured workspace is proven absent and `create_if_missing: true`,
the preflight may return `creation-required` and authorize only the exact configured
session or group creation supported by `managed_session_creation` or `group_creation`.
Re-enumerate and rerun preflight before selection, placement, tab creation, navigation,
or page action. A same-name observation without a stable ID is ambiguity, not absence.

When a locked dedicated browser is absent and background setup is explicitly allowed,
the preflight may return `setup-required` and authorize only one background browser/CDP
setup. It must return `capability-unavailable` after an unsuccessful or already-attempted
setup, and it must return `ready` only after fresh profile, endpoint, target, tab
enumeration, and page-control evidence succeeds.

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

The bridge creates the request. `operation_id` identifies exactly one intended
external side effect and must remain unchanged across inspection or a permitted
retry. `round_id` groups an external review round; `relay_turn_id` groups the
create, attach, submit, and response-capture operations for one sequential relay
turn. A new review round, relay turn, or different side effect requires a new ID.

For a sequential relay, resolve the provider's conversation before allocating an
operation. On that provider's first turn, reuse an already verified conversation when
one is authorized; create a conversation only when there is no verified conversation
and a new session is required. That creation has its own `create-conversation`
operation ID. Later turns for that same provider reuse that verified conversation: do
not invent or reserve a create operation. Allocate IDs only for actual later side
effects, such as an attachment when needed, submit, and response capture. If the first
creation is interrupted or ambiguous, reconcile its original create operation ID and
target; never create a replacement conversation to continue the same relay.

```yaml
schema_version: browser-operation/v1
operation_id: <task>:<round>:<relay-turn|not-applicable>:<action>
round_id: <stable external-review round id>
relay_turn_id: <stable sequential-relay turn id|not-applicable>
attempt: <positive integer; starts at 1>
caller: ask-ai
intent: <inspect|navigate|create-conversation|compose|attach|submit|capture-response|cleanup>
authorization:
  external_send: <authorized|not-authorized>
  scope: <exact package, round, and action>
route:
  provider: <chatgpt|gemini|deepseek|kimi|other>
  surface: <standard-chat|project|quick-chat|notebook|conversation|provider-specific>
  context_id: <stable project, notebook, or conversation id|Not verified>
  account_workspace: <personal|organization|Not verified>
  browser_mode: <verified mode>
  provider_interface: <chat|work|provider-specific|not-applicable|Not verified>
  provider_model: <requested label or stable id|not-applicable|Not verified>
  reasoning_mode: <preferred label|not-applicable|Not verified>
  reasoning_fallbacks:
    - <ordered authorized fallback label or none>
local_workspace_policy:
  policy_source: <validated local record|current-request override|not-applicable>
  control_session_name: <resolved configured name|not-applicable>
  tab_group_name: <resolved configured name|not-applicable>
  allow_name_session: <true|false>
  allow_group_creation: <true|false>
  controller_requires_task_specific_session_name: <true|false|unknown>
target:
  conversation_id: <stable id|create-one-authorized|Not verified>
  expected_url: <exact URL or Not verified>
artifact:
  path: <path or none>
  sha256: <hash or none>
  sequence: <single|part n/N|final-marker>
capability_snapshot_id: <snapshot_id>
execution_constraints:
  action_shape: <fixed|open-ended|low-level-chromium>
  external_write: <authorized|not-authorized>
  allowed_origins:
    - <origin or none>
  allowed_action_classes:
    - <read|navigate|compose|attach|submit|capture|cleanup>
  max_steps: <positive integer|not-applicable>
  max_actions: <positive integer|not-applicable>
preconditions:
  - <required identity, composer, attachment, or completion state>
expected_postcondition:
  - <observable success evidence>
retry_policy: <never|only-if-no-side-effect-proven>
prior_evidence:
  - <evidence from an earlier attempt or none>
```

`execution_constraints` narrows an already authorized operation; it never grants
authority. When `external_write` is `not-authorized`, exclude `attach` and `submit`
from `allowed_action_classes`; include `compose` only after proving that typing cannot
persist a server draft or notify another party. An LLM browser agent handoff must use
`external_write: not-authorized` and only read, navigate, and capture classes. If
exploration discovers a later write, end the agentic handoff and require a new
deterministic handoff with fresh identity, target, authorization, and operation ID.

`provider: other`, `surface: provider-specific`, and
`provider_interface: provider-specific` are labels, not capability evidence. When no
dedicated provider reference exists, the request must name the exact provider and its
live Capability Snapshot and preconditions must prove current target identity, a clean
authorized composer, intended input, unique submit control, observable side effect,
completion signal, and response attribution. A missing or `Not verified` required
field blocks every state-changing handoff; schema acceptance never makes the provider
route executable.

The bridge owns provider, recipient, interface, model, reasoning preferences, and
their authorized fallback order. `ops-browser` verifies rendered controls and
returns direct selection evidence. Stored labels are not capability proof. If a
same-provider preference is unavailable, use only the first verified configured
fallback or return `blocked`. Never change provider as an implicit fallback.

For `user-local-browser`, the bridge must populate `local_workspace_policy` from the
validated `ops-browser` policy before handoff. Provider, task, agent, emoji, page, and
conversation labels never populate either name. If the controller requires a
task-specific session name while the policy forbids naming or requires unified reuse,
return `blocked` with `capability-unavailable` before controller setup or page action.
Do not rename the configured session or create a provider-specific group to continue.

## Handoff Result

`ops-browser` returns facts only. It does not change authorization, add rounds,
switch routes, create packages, or decide whether an ambiguous action succeeded.

```yaml
schema_version: browser-operation/v1
operation_id: <same request id>
round_id: <same request round id>
relay_turn_id: <same request relay turn id>
attempt: <same request attempt>
capability_snapshot_id: <same snapshot id>
state: <preflighted|ready|created|attached|submitted|acknowledged|captured|completion-not-verified|cleaned|completed|failed-before-submit|blocked|ambiguous>
execution:
  backend: <host-browser-api|playwright|llm-browser-agent|cdp|manual>
  worker_role: <primary-coordinator|delegated-worker-role|not-applicable>
  worker_runtime_model: <provider-owned runtime model|Not verified|not-applicable>
  ownership_key: <provider/browser/session/tab/operation binding|not-applicable>
  selection_reason: <direct capability and task-shape evidence>
  budget_used: <steps/actions or not-applicable>
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
response_capture:
  conversation_id: <stable conversation id|Not verified|not-applicable>
  response_container_id: <stable assistant-response container id|Not verified|not-applicable>
  content:
    complete: <true|false|Not verified>
    truncated: <true|false|Not verified>
    character_count: <non-negative integer|Not verified>
    sha256: <64 lowercase hex|Not verified>
  artifact:
    path: <exact persisted response path|Not verified|not-applicable>
    file_sha256: <64 lowercase hex|Not verified|not-applicable>
    atomic_write: <verified|failed|Not verified|not-applicable>
    readback_verified: <true|false|Not verified|not-applicable>
retained_evidence:
  - <identifier or path>
cleanup:
  - <removed or retained task state>
error:
  kind: <none|capability|identity|composer|attachment|submission|completion|interruption>
  detail: <sanitized detail>
```

## Attachment Failure Evidence

Classify an attachment failure by the last directly observed phase: before file
selection, after selection or while upload state is unresolved, or attached. A
before-selection failure may return `failed-before-submit` only when direct evidence
on the same reverified browser/session, tab, target, and composer proves all of the
following: no file was selected or uploaded, the intended input remains empty or
unchanged, no submit postcondition occurred, and no other side effect was observed.
Record those facts in `before`, `action`, `side_effect`, and `after`; a chooser timeout
or tool error alone is not proof.

If selection/upload state or target binding cannot be reverified, return `ambiguous`
and do not retry that operation. If the action was proven not to start but a required
identity, tab, target, or composer precondition is now missing, return `blocked` until
fresh evidence changes that condition. A later separately authorized task is a new
operation; it must not allocate a new ID merely to bypass an ambiguous attachment.

## Stable Response Evidence

Provider-specific completion controls are evidence signals, not universal oracles.
When the selected provider contract permits stable-response completion, `ops-browser`
may return direct completion evidence from separated samples of the same attributed
assistant response in the same reverified conversation. Before the first sample, fix a
finite observation window and sampling cadence. Take at least two samples according to
that cadence, including one at the end of the window; immediate consecutive snapshots
do not qualify. The samples must contain a non-empty, non-truncated response, have the
same sanitized content hash, and show no material response mutation. Record the fixed
window and cadence, sample count and times, response-container identity, hashes, and
any still-visible generation or stop control in `after` or `retained_evidence`.

A lingering control remains a separate `Not verified` terminal-UI gap; it does not
invalidate an otherwise permitted stable-response capture and never authorizes a
resend. Empty, truncated, changing, differently attributed, or target-drifted samples
remain completion `Not verified` or `ambiguous` as required by the route state. Capture
the accepted response once and stop.

For `capture-response`, browser observation alone cannot enter `captured`. Before any
submit, the bridge must have created and read back the fixed package, invocation,
events, response-partial, and response-final paths under one verified ignored parent.
If that persistence gate fails, stop at Package-only before external action. The
browser operator may write only the pre-authorized response-partial artifact; the
bridge owns atomic promotion to the response-final path and the final receipt.

The bridge accepts `captured` only when `response_capture` contains a stable
conversation ID and response-container ID, `complete: true`, `truncated: false`, the
exact Unicode character count and captured-content SHA-256, plus the final artifact
path, its file SHA-256, `atomic_write: verified`, and `readback_verified: true`.
Compute the content hash from the exact captured visible response bytes and the file
hash from the final persisted bytes; do not substitute one without checking both.
Missing, contradictory, truncated, empty, non-atomic, unreadable, or hash-mismatched
evidence returns `completion-not-verified`, never `captured` or `completed`. Use
`ambiguous` instead only when the target, attribution, or external side effect itself
cannot be reconciled.

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
| `submitted` | `acknowledged`, `completion-not-verified`, `ambiguous` |
| `acknowledged` | `captured`, `completion-not-verified`, `ambiguous` |
| `captured` | `completed`, `ambiguous` |
| `completion-not-verified` | `captured`, `ambiguous` only after read-only reconciliation of the same conversation and response container |
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
  response capture, final marker, and every other external side effect; never use
  one operation ID for multiple actions merely because they belong to one relay turn;
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

`completion-not-verified` never permits resend, regeneration, a replacement
conversation, or a new capture operation ID. Resume only the original read-only
capture against the same provider, account, conversation, response container, tab,
and precreated artifact paths. For a `capture-response` operation, `completed` is
legal only after `captured` with the complete persistence receipt above.

One `round_id` groups the many operation IDs that make up an external review
round. For sequential relay, one `relay_turn_id` nests inside that round and
groups the distinct create, attach, submit, and capture operations for one
provider turn. A round is complete only when every required package/send
operation and its attributed response-capture operation are completed. Creating
a conversation is a separate state-changing operation; interruption after
creation is reconciled against the original Project before any new conversation
can be authorized.

## Degraded Mode

If a required capability is unavailable or unknown, return `blocked` without
the action and name the missing capability. If interruption prevents proving
whether a side effect occurred, return `ambiguous`; do not retry, switch
routes, or create a replacement conversation. Package-only work remains
available when external browser operation cannot be proven.
