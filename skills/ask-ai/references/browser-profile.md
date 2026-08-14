# Provider And Transport Defaults

## Contents

- [Purpose](#purpose)
- [Ask AI Record](#ask-ai-record)
- [ChatGPT Legacy Record](#chatgpt-legacy-record)
- [Route Evidence](#route-evidence)
- [Reset](#reset)

## Purpose

A local defaults record stores provider and route preferences. It is never send
authorization or proof of current provider, identity, model, browser, or capability.
Current-request values always win.

## Ask AI Record

Store new records at ~/.agents/config/ask-ai/defaults.yaml using:

    schema_version: ask-ai-defaults/v1
    default_provider: chatgpt | gemini | manual
    browser_preference:
      primary: codex-in-app-browser | user-local-browser | manual
      local_browser: <user-selected browser name>
      fallback: user-local-browser | codex-in-app-browser | package-only
    context_routes:
      review:
        name: <optional generic review container name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
        conversation_policy: reuse-verified | new-per-task
        provider_targets:
          chatgpt: {surface: project, name: <user-selected ChatGPT Project name>}
          gemini: {surface: notebook, name: <user-selected Gemini Notebook name>}
      design:
        name: <user-editable design Project/notebook name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
        conversation_policy: reuse-verified | new-per-task
      image:
        name: <user-editable image Project/notebook name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
        conversation_policy: reuse-verified | new-per-task
    standard_chat:
      policy: allow-default | explicit-current-request-only
    cli_monitoring:
      strategy: adaptive
      short_task_poll_hint_seconds: <positive seconds>
      long_task_poll_hint_seconds: <positive seconds>
      preferred_wait_observer: <user-selected read-only role | none>
      require_observer_runtime_identity: true
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
    provider_aliases:
      <user alias>: <canonical provider>
    providers:
      <canonical CLI provider>:
        default_transport_mode: cli
        model_aliases:
          <user model alias>: <installed model identifier>
        cli_profile:
          executable_candidates: [<absolute path or command name>]
          identity_markers: [<installed identity marker>]
          version_args: [<argument>]
          help_args: [<argument>]
          argument_order: <ordered option categories>
          workspace:
            option: <verified option>
            value_source: current-task-repository
            semantics: change-directory | add-directory
          prompt_transport: argument | stdin | file
          prompt_option: <verified option | none>
          base_args: [<verified argument>]
          modes:
            native-review:
              args: [<verified provider-specific argument>]
              permission_strategy: <verified non-interactive strategy>
              isolation: disposable-worktree | sandbox | external-read-only
              persistent_mutation: deny
            native-execution:
              args: [<verified provider-specific argument>]
              permission_strategy: <verified non-interactive strategy>
              isolation: authorized-worktree | provider-worktree
              persistent_mutation: allow-within-task-scope
          native_capabilities: all
          profile_fingerprint: <executable/version/mode-profile fingerprint>
          conformance_verified_at: <ISO-8601 | Not verified>
          model_option: <verified option | none>
          reasoning_option: <verified option | none>
          output_format: <configured machine format | text>
          attribution_paths:
            session: <provider-owned field or log selector | none>
            model: <provider-owned field or log selector | none>
            terminal: <provider-owned field or log selector | none>
          terminal_values: [<verified terminal value>]
          resume_option: <verified option | none>
          require_repository_binding: true
          provider_deadline_seconds: <positive integer | null>
          hard_process_deadline_seconds: <positive integer | null>
          redact_log_fields: [<field or pattern>]
      chatgpt:
        default_transport_mode: codex-app-native | browser | manual
        surface: standard-chat | quick-chat | project
        project_name: <discovery hint>
        interface: chat | work
        model: <preference>
        reasoning_mode: <preference>
        reasoning_fallbacks: [<ordered preferences>]
        default_url: <discovery hint>
      gemini:
        default_transport_mode: browser | manual
        surface: standard-chat | notebook | conversation
        notebook_name: <discovery hint>
        model: <preference>
        default_url: <discovery hint>
    last_verified_at: <informational timestamp>

`browser_preference` is provider-neutral. When omitted, use
`primary: codex-in-app-browser` and `fallback: package-only`. A
`user-local-browser` primary or fallback is valid only with a non-empty
`local_browser`; store the browser product name, never a profile, tab, executable path,
or URL. Primary and fallback must differ; `manual` performs no fallback.
`desktop-built-in-browser` remains a compatible Ask AI v1 alias for
`browser` plus `codex-in-app-browser` and should be normalized only during an explicitly
authorized config edit.

The primary route is retried from a fresh capability preflight on every new task. A
fallback applies only to the current task and never rewrites, demotes, or learns a new
default. An explicit current-request route skips probing other routes. Thus an explicit
local-browser request or a saved `user-local-browser` primary starts with that named
browser, while a built-in-first preference probes Codex in-app again even when the
previous task fell back locally.

A configured `user-local-browser` fallback is eligible only when the current request
explicitly authorizes that visible user-owned surface and the task requires state or a
capability unavailable on the in-app browser, such as an exact existing login, tab,
profile-bound extension, or user download context. Primary unavailability alone does
not authorize touching Chrome. Otherwise stop at Package-only. Never use the fallback
to bypass missing provider, recipient, account/workspace, model, conversation,
authorization, or idempotency evidence.

Do not write an unsupported provider, transport, surface, model, or capability merely
because the schema can represent it. A durable preference selects order only: external
send authorization and fresh route, identity, target, and capability evidence remain
required.

Never store secrets, cookies, tokens, browser storage, email addresses, display names,
or raw profile data. A Project/notebook name, URL, conversation identifier, model,
reasoning mode, tab, or timestamp is a hint until reverified.

`cli_monitoring` is optional user configuration for observation cadence, not a timeout
or retry policy. `strategy: adaptive` selects intervals from the task's estimated
duration and observed progress. The short and long values are positive scheduling
hints, not success deadlines. `preferred_wait_observer` may name one user-selected
read-only role; verify that role's effective runtime identity before attributing it,
and keep the primary coordinator as the operation owner.

`artifact_handoff` is optional user configuration for durable CLI task/result exchange.
Every role is user-configurable and resolves under one verified ignored task-local
parent; `flat-prefixed` keeps related files under that parent without creating a task
subdirectory. Exactly one writer owns each progress/result role. The setting changes
artifact transport only: it does not authorize invocation, mutation, retry, or Git
delivery. Load `cli-artifact-handoff.md` for its launch, recovery, and completion gates.

`provider_aliases` and `model_aliases` are routing conveniences only. Resolve aliases
to a canonical recipient and an exact installed model identifier before invocation;
neither alias proves identity, availability, compatibility, or effective-model use.
`cli_profile` contains mutable machine-local facts and must not be copied into the
portable Skill. Build an exact argv array from the validated profile, preserve its
declared order, and reject missing or unknown fields. Null deadlines mean no configured
deadline, not infinite authorization. Provider-owned attribution selectors and terminal
values must be reverified after executable drift. Never store secrets or raw logs. Both
CLI modes expose the same verified provider-native capability set and resolve eligible
permission prompts non-interactively. Their only semantic difference is whether
task-scoped mutation may persist. Provider-specific flags and isolation mechanisms stay
inside each mode record and require an isolated runtime canary for the current profile
fingerprint. A stale or `Not verified` profile returns Package-only until that canary
passes; it never submits formal work with old or guessed arguments.
The `workspace` record is required for a repository-scoped CLI: inject the current
task's canonical repository through the configured option and verify the provider's
active workspace before submit. A host process `cwd` alone is not provider workspace
evidence, especially when the configured semantics add a directory instead of changing
the provider's primary working directory.

`context_routes` is user configuration that maps task intent to provider-neutral
persistent-container names. Common route IDs are `review` for critique/audit/verification,
`design` for product/UI/UX/architecture creation, and `image` for generation, editing,
or visual exploration. Classify by the requested operation, so architecture review and
architecture creation may resolve differently. Additional user-defined route keys may
follow the same contract. The Skill never supplies personal container names.

Normalize product terminology before routing:

| Canonical surface | Provider presentation examples |
| --- | --- |
| `standard-chat` | ChatGPT Standard Chat, Gemini new chat, another provider's ordinary chat |
| `persistent-context` | ChatGPT Project, Gemini Notebook, or a verified provider Project, Space, or Collection |

These are functional mappings, not claims that every provider implements equivalent
storage, tools, context limits, or permissions. Require live provider capability and
stable container identity. Preserve the user's exact container name independently for
each provider when configured names differ.

`provider_targets` is required for the `review` route and is the authority for its
selected provider. Other routes may use it as an override when provider container
surface or configured name differs; only those other routes fall back to route-level
`name`. Never copy a ChatGPT Project label into Gemini or
infer a Notebook name from another provider. Unknown provider or surface values block
that override without changing the configured recipient.

Even when the two configured review targets have the same label, they remain different
identities: ChatGPT uses a Project and Gemini uses a Notebook. The label is only
configuration. Verify each provider's stable container ID, URL origin, account, and
conversation independently. Never copy one provider's ID, URL, tab, or evidence into
the other provider's adapter.

`conversation_policy` controls conversation reuse inside the resolved persistent
container. `new-per-task` creates exactly one new conversation for the authorized task
inside that verified container; `reuse-verified` reuses only an explicitly mapped
conversation. It never changes the provider or container and does not authorize a
second submit when creation or submission is ambiguous.

Before any browser operation, serialize the selected provider, current request,
complete defaults, and fresh transport/target observations, then run
`python3 skills/ask-ai/scripts/resolve_browser_transport.py <input.json>`. Its
`ask-ai-transport-resolution/v1` output is the machine authority for
`selected_transport` and `forbidden_transports`. An available Codex in-app Browser is
still selected when `openTabs: []`; open only a task-owned tab after target discovery,
or stop Package-only. This browser route requires `chatgptWorkCloud: 0` calls.
Gemini browser work always forbids ChatGPT App-native and AGY CLI transports.

For each authorized external action, first apply an explicit current-request target,
then a matching configured route. If neither selects `persistent-context`, use
`standard-chat`. For a persistent route, reuse only one live provider-specific
container whose configured name, provider account class, type, and stable identity are
verified. `require-verified-persistent` makes it a hard target and requires
`fallback: package-only`. `prefer-verified-persistent` may use
`fallback: new-standard-chat` when the Standard Chat policy permits it. Missing,
unknown, or conflicting policy/fallback combinations fail closed.

`standard_chat.policy` is also user configuration. When it is absent, default to
`allow-default`. `explicit-current-request-only`
means a new, blank, ordinary, Quick, or Standard Chat is legal only when the current
request explicitly selects that surface; `allow-default` permits a matched
`new-standard-chat` fallback and ordinary default routing. Wording that excludes
current conversation facts, asks for a clean-slate design, or says not to be influenced
by the current discussion changes the outbound package, not the target container. It
must not be interpreted as permission to use Standard Chat, Quick Chat, another
Project/notebook, or another account. Apply `conversation_policy` inside the verified
container.

A `final-result-sync` target may name the same persistent container as a normal route.
Keep the sync payload and receipt in their own verified conversation and preserve the
sync workflow's sanitization and one-send boundary; sharing the container does not turn
ordinary review into retention or vice versa.

Provider-specific `project_name` or `notebook_name` fields are optional exact overrides
for a route, not current identity proof. A stored URL is eligible only when its live
container name still matches the resolved route; otherwise stop and rediscover by name.
The record does not authorize creating a container, sending content, changing accounts,
or selecting a different route.

## ChatGPT Legacy Record

The old `~/.agents/config/ask-chatgpt/defaults.yaml` record remains ChatGPT-only input.
Recognize `ask-chatgpt-defaults/v2` and older unversioned records only after the
provider is resolved to ChatGPT or the request explicitly uses legacy ask-chatgpt
wording.

For `ask-chatgpt-defaults/v2`, require `default_transport_mode`:

- `codex-app-native` or `desktop-built-in-browser` selects which verified ChatGPT
  route is tried first;
- `manual` stops before external action;
- missing or unknown values block external action pending explicit repair.

For an unversioned legacy record, preserve built-in-first behavior for missing mode,
`desktop-built-in-browser`, and `capability-auto`; stop for `manual`,
`chatgpt-cloud-browser`, an unknown value, or an ambiguous versioned field. Treat
`current-chrome-explicit` and `standalone-playwright-explicit` as non-authorizing hints.

Do not reinterpret, copy, rewrite, or delete a legacy record automatically. Migration
to one complete Ask AI v1 record is a persistent configuration change and requires
explicit authorization, readback verification, and an explicit retain/remove decision
for the legacy record.

## Route Evidence

Browser fields apply only to their provider and browser route. Keep built-in,
cloud/agent reviewer, Chrome, standalone, provider, account, and conversation
identities separate. Do not transfer cookies, login, tab, model, or capability
evidence. A profile path remains Not verified unless the active surface exposes it.

## Reset

Create, update, migrate, reset, or delete defaults only after explicit instruction.
For an authorized change, validate the complete target record, preserve unrelated
valid fields, write it atomically, then read back and report the effective provider,
browser preference, route policies, and provider hints. The configuration write never
proves or changes current login, browser state, tabs, conversations, or capabilities.
Reset clears bridge records, not real browser data, conversations, review artifacts,
source, commits, or installed Skills.
