# Provider Adapter Contract

## Contents

- [Purpose](#purpose)
- [Adapter Record](#adapter-record)
- [Capability States](#capability-states)
- [Required Operations](#required-operations)
- [Reuse And Recovery](#reuse-and-recovery)
- [Conformance Evaluation](#conformance-evaluation)
- [Adapter Levels](#adapter-levels)

## Purpose

Use `ask-ai-provider-adapter/v1` to add a named external AI without changing the
provider-neutral orchestration rules. The contract standardizes discovery, identity,
conversation reuse, submit/capture attribution, and interruption recovery. It does not
standardize provider products, selectors, models, Projects, notebooks, Deep Research,
or other capabilities.

An adapter record is a task-time evidence record, not a persistent claim that a
provider still supports a feature. Populate it from live host/native or browser
evidence. Unknown and stale capability claims fail closed for actions that require
them.

## Adapter Record

```yaml
schema_version: ask-ai-provider-adapter/v1
provider: <canonical provider name>
adapter_level: <generic-browser|dedicated>
transport: <app-native|browser|api|manual>
verified_at: <ISO-8601|Not verified>
identity:
  provider_origin: <verified origin|not-applicable>
  account_workspace: <personal|organization|Not verified>
  persistent_context_id: <stable project/notebook/space id|not-applicable|Not verified>
  conversation_id: <stable id|create-one-authorized|Not verified>
capabilities:
  standard_chat: <supported|unsupported|not-verified>
  persistent_context: <supported|unsupported|not-verified>
  conversation_reuse: <supported|unsupported|not-verified>
  files: <supported|unsupported|not-verified>
  search: <supported|unsupported|not-verified>
  deep_research: <supported|unsupported|not-verified>
  model_selection: <supported|unsupported|not-verified>
operations:
  discover_target: <verified operation|unavailable>
  verify_identity: <verified operation|unavailable>
  resolve_context: <verified operation|unavailable>
  create_conversation: <verified operation|unavailable|not-required>
  submit: <verified operation|unavailable>
  capture_response: <verified operation|unavailable>
  reconcile_submission: <verified operation|unavailable>
reuse:
  conversation: <verified-id-only|unsupported>
  persistent_context: <verified-container-only|unsupported>
  new_conversation_fallback: <allowed-before-submit|not-allowed>
completion:
  signal: <direct provider-owned evidence|Not verified>
  attribution: <stable response container evidence|Not verified>
gaps:
  - <capability or operation>: <reason>
```

Provider aliases are resolved before creating this record. The adapter may not change
the provider, authorization, package, round, relay limit, model requirement, or
fallback order selected by the coordinator.

## Capability States

- `supported` means the required path was verified on the current provider, account,
  surface, and transport. It is not a permanent compatibility statement.
- `unsupported` requires direct current evidence or an authoritative provider
  contract for the exact surface.
- `not-verified` covers missing, stale, inaccessible, contradictory, or untested
  capability evidence.

Only `supported` satisfies a required non-default capability. Ordinary text chat may
continue only when `standard_chat` and its required operations are supported.

## Required Operations

Every executable adapter must prove `discover_target`, `verify_identity`, `submit`,
`capture_response`, and `reconcile_submission`. `resolve_context` is required when a
Project, notebook, space, or other persistent container is requested.
`create_conversation` is required only when the authorized route needs a new
conversation.

Each state-changing operation receives its own `operation_id`. The adapter returns
direct precondition, action, side-effect, postcondition, completion, and attribution
evidence. Provider success text is not evidence of completion or correct attribution.

## Reuse And Recovery

- Reuse a conversation only from a stable verified ID bound to the same provider,
  account/workspace, persistent context, and task scope.
- Reuse a Project/notebook/space only from its stable verified container ID. A name,
  title, recent-history item, or saved URL is discovery evidence only.
- A verified existing conversation is preferred for authorized follow-up turns.
- A clean new conversation is a fallback only before any submit and only when the
  current request permits it.
- After an uncertain create or submit, run `reconcile_submission` read-only against
  the original target and operation ID. Never resend, regenerate, switch provider, or
  create a replacement conversation to manufacture completion.

## Conformance Evaluation

Run the applicable cases before declaring a new or materially changed adapter usable:

1. discover and verify the exact provider/account/surface without exposing PII;
2. create one conversation when authorized and capture its stable identity;
3. submit once and attribute one completed response;
4. continue in the same verified conversation;
5. recover that conversation after a new host observation or reconnect;
6. resolve a verified persistent context, or prove that it is unsupported;
7. simulate or observe an uncertain submit and reconcile without duplicate send;
8. prove a different account/workspace or ambiguous target is rejected;
9. verify every claimed non-default capability independently;
10. confirm unsupported capabilities degrade to Package-only or a named blocked state.

Record each case as `pass`, `fail`, or `not-run` with provider, transport, date,
surface/version evidence, and gaps. Schema validation alone is not conformance.

## Adapter Levels

- **Generic browser:** supports only capabilities proven through the portable browser
  provider route. Default to ordinary text chat. Projects, files, Search, Deep
  Research, model selection, and durable reuse remain `not-verified` until exercised.
- **Dedicated:** may use provider-specific native operations or stronger browser
  contracts and may declare additional supported capabilities after live conformance.

Promote a generic adapter to dedicated only when provider-specific behavior is both
repeatedly needed and validator/eval-backed. Keep selectors and volatile UI details in
runtime discovery, not this contract.
