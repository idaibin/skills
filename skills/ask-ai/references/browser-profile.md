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
        name: <user-editable review Project/notebook name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
        provider_targets:
          chatgpt: {surface: project, name: <optional ChatGPT Project name>}
          gemini: {surface: notebook, name: <optional Gemini Notebook name>}
      design:
        name: <user-editable design Project/notebook name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
      image:
        name: <user-editable image Project/notebook name>
        policy: prefer-verified-persistent | require-verified-persistent
        fallback: new-standard-chat | package-only
    standard_chat:
      policy: allow-default | explicit-current-request-only
    cli_monitoring:
      strategy: adaptive
      short_task_poll_hint_seconds: <positive seconds>
      long_task_poll_hint_seconds: <positive seconds>
      preferred_wait_observer: <user-selected read-only role | none>
      require_observer_runtime_identity: true
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
          prompt_transport: argument | stdin | file
          prompt_option: <verified option | none>
          base_args: [<verified argument>]
          review_args: [<verified no-write argument>]
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

`provider_aliases` and `model_aliases` are routing conveniences only. Resolve aliases
to a canonical recipient and an exact installed model identifier before invocation;
neither alias proves identity, availability, compatibility, or effective-model use.
`cli_profile` contains mutable machine-local facts and must not be copied into the
portable Skill. Build an exact argv array from the validated profile, preserve its
declared order, and reject missing or unknown fields. Null deadlines mean no configured
deadline, not infinite authorization. Provider-owned attribution selectors and terminal
values must be reverified after executable drift. Never store secrets or raw logs.

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

`provider_targets` is an optional per-route override for providers whose container
surface or configured name differs. Resolve the selected provider's exact override
first, then the route-level `name`; never copy a ChatGPT Project label into Gemini or
infer a Notebook name from another provider. Unknown provider or surface values block
that override without changing the configured recipient.

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
current project or conversation facts changes the outbound package, not the target
container; it does not by itself select a different surface.

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
