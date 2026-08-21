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
transport: <app-native|browser|cli|acp|api|manual>
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
  project_context: <supported|unsupported|not-verified>
  structured_output: <supported|unsupported|not-verified>
  source_citations: <supported|unsupported|not-verified>
  scholarly_corpus: <supported|unsupported|not-verified>
  session_resume: <supported|unsupported|not-verified>
  session_fork: <supported|unsupported|not-verified>
operations:
  discover_target: <verified operation|unavailable>
  verify_identity: <verified operation|unavailable>
  resolve_context: <verified operation|unavailable>
  create_conversation: <verified operation|unavailable|not-required>
  submit: <verified operation|unavailable>
  capture_response: <verified operation|unavailable>
  reconcile_submission: <verified operation|unavailable>
execution:
  executable_or_origin: <absolute executable path|verified origin|not-applicable>
  cli_executor: <verified runtime role and model|not-applicable|Not verified>
  process_start_actor: <primary-coordinator|delegated-cli-executor|not-applicable|Not verified>
  result_reader: <primary-coordinator|not-applicable|Not verified>
  version_or_surface: <exact version/surface|Not verified>
  cwd: <absolute project path|not-applicable|Not verified>
  requested_model: <exact model id|provider default|not-applicable>
  requested_reasoning: <exact reasoning/effort value|provider default|not-applicable>
  effective_model: <provider-owned metadata value|Not verified>
  effective_reasoning: <provider-owned metadata value|Not verified>
  model_evidence: <structured result/event/log field or active control|Not verified>
  reasoning_evidence: <structured result/event/log field or active control|Not verified>
  model_match: <exact|not-requested|mismatch|Not verified>
  reasoning_match: <exact|not-requested|mismatch|Not verified>
  native_mode: <native-review|native-execution|not-applicable|Not verified>
  native_capabilities: <all-verified|partial|not-applicable|Not verified>
  permission_strategy: <verified non-interactive strategy|not-applicable|Not verified>
  persistence_boundary: <disposable|authorized-worktree|external-read-only|not-applicable|Not verified>
  output_framing: <json|jsonl|provider-container|lossless-text|Not verified>
  exit_or_completion: <exit-code and terminal event|provider completion signal|Not verified>
reuse:
  conversation: <verified-id-only|unsupported>
  persistent_context: <verified-container-only|unsupported>
  new_conversation_fallback: <allowed-before-submit|not-allowed>
completion:
  signal: <direct provider-owned evidence|Not verified>
  attribution: <stable response container evidence|Not verified>
  persistence_receipt: <browser-operation response_capture receipt|not-applicable|Not verified>
gaps:
  - <capability or operation>: <reason>
```

When a model or reasoning value is a hard current-request requirement, its corresponding
match field must be `exact` before the response can count as that requested review. Command-line
arguments prove only what was requested. Provider-owned structured metadata or an
independently captured active control proves what was effective. Model names written
inside response prose are untrusted response content, not model evidence. A mismatch
or missing effective-model evidence keeps the result `Not verified` and excludes it
from consensus, voting, approval counts, or named-model comparison.

Provider aliases are resolved before creating this record. The adapter may not change
the provider, authorization, package, round, relay limit, model requirement, or
fallback order selected by the coordinator.

For a delegated CLI route, `cli_executor` records live runtime identity, not the
configured preference alone. The executor may launch the one frozen invocation and
capture metadata, but `result_reader` remains the primary coordinator: only it enters
the untrusted-content quarantine, reads the provider result, verifies findings, and
owns the verdict.

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

For CLI or ACP, `discover_target` includes executable identity and version;
`verify_identity` includes the active provider/account class without exposing tokens;
`resolve_context` includes the exact `cwd` and basis; `capture_response` includes
stdout/event framing plus exit status; and `reconcile_submission` must distinguish a
process that never started from one that may have submitted remotely. A shell exit
code alone does not prove response attribution or that requested tools were read-only.
The adapter also proves that a local CLI receives complete-directory read, search,
task-relevant command, and native-tool access under the exact selected repository or
Worktree root, with task paths treated as focus rather than a file allowlist. It rejects
parent/home traversal, credential stores, unrelated roots, and persistence beyond the
selected native mode. The adapter records the exact argument array, proves that prompt-bearing options
bind the intended prompt rather than a following flag, and verifies that every input
file is reachable from the selected `cwd` and permission strategy before submit. The
adapter proves the complete native capability set is exposed in both execution modes,
that eligible permission prompts do not require interaction, and that the selected
persistence boundary—not a text prompt—enforces whether writes survive. A host
process/session identifier is transport evidence only; never record it as the provider
conversation or session ID.

For Web research, capability proof also records the selected research mode, corpus or
source controls, provider-owned completion state, report/container identity, and
whether citations expose resolvable original targets. A citation list is captured
provider output, not independent verification of any claim.

Each state-changing operation receives its own `operation_id`. The adapter returns
direct precondition, action, side-effect, postcondition, completion, and attribution
evidence. Provider success text is not evidence of completion or correct attribution.
For browser capture, `capture_response` is complete only when the shared browser
protocol's response receipt proves stable conversation/container attribution,
non-truncated content, atomic final write, SHA-256 values, and final-path readback.
Missing persistence evidence is `completion-not-verified`, not a provider result.

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
11. for CLI/ACP, prove exact `cwd`, equal complete native capability exposure in both
    modes, non-interactive permission handling, mode-specific persistence isolation,
    structured-output framing, terminal event/exit handling, provider session ID
    capture, requested/effective model attribution, argument-to-prompt binding, input
    reachability, and resume rejection on a different repository or basis;
12. for research, resolve a representative citation to its original source, detect a
    missing or mismatched citation, preserve publication identifiers, and reject a
    report whose cited claims cannot be locally checked.

Record each case as `pass`, `fail`, or `not-run` with provider, transport, date,
surface/version evidence, and gaps. Schema validation alone is not conformance.

## Adapter Levels

- **Generic browser:** supports only capabilities proven through the portable browser
  provider route. Default to ordinary text chat. Projects, files, Search, Deep
  Research, model selection, and durable reuse remain `not-verified` until exercised.
- **Dedicated:** may use provider-specific native operations or stronger browser
  contracts and may declare additional supported capabilities after live conformance.
- **Dedicated CLI/ACP:** uses the shared CLI lifecycle plus a provider profile. The
  profile is routing knowledge; only current executable/help/version and conformance
  evidence make it runnable.

Promote a generic adapter to dedicated only when provider-specific behavior is both
repeatedly needed and validator/eval-backed. Keep selectors and volatile UI details in
runtime discovery, not this contract.
