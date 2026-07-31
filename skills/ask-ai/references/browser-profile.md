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
    review_context:
      name: <user-editable default persistent context name>
      policy: prefer-verified-persistent
      fallback: new-standard-chat
    providers:
      chatgpt:
        default_transport_mode: codex-app-native | desktop-built-in-browser | manual
        default_browser_mode: desktop-built-in-browser | capability-auto | manual
        surface: standard-chat | quick-chat | project
        project_name: <discovery hint>
        interface: chat | work
        model: <preference>
        reasoning_mode: <preference>
        reasoning_fallbacks: [<ordered preferences>]
        default_url: <discovery hint>
      gemini:
        default_transport_mode: desktop-built-in-browser | manual
        surface: standard-chat | notebook | conversation
        notebook_name: <discovery hint>
        model: <preference>
        default_url: <discovery hint>
    last_verified_at: <informational timestamp>

Do not write an unsupported provider, transport, surface, model, or capability merely
because the schema can represent it. Current Chrome and standalone automation require
current-request selection and are not durable authorization.

Never store secrets, cookies, tokens, browser storage, email addresses, display names,
or raw profile data. A Project/notebook name, URL, conversation identifier, model,
reasoning mode, tab, or timestamp is a hint until reverified.

`review_context` is a provider-neutral selection preference, not a claim that every
provider supports Projects, notebooks, spaces, or collections. For each authorized web
review, first look for one live, uniquely identified persistent container with the
configured name. Reuse it only after provider, account class, container type, and stable
identity are verified. If the provider does not expose such a container, the container
is unavailable, or its identity cannot be verified, use a clean new Standard Chat for
that review. A history group or ordinary conversation title is not a persistent
container. The record does not authorize creating a container, sending content, or
changing accounts; those remain current-request actions.

`review_context.name` is the single provider-neutral default name. Users may change
that one field at any time; all provider routes inherit the new value on their next
authorized review. Provider-specific `project_name` or `notebook_name` fields are
optional explicit overrides, not required mirrors of the global name. A stored URL is
eligible only when its live container name still matches the currently resolved name;
otherwise ignore it and rediscover by name. The example placeholder is not a built-in
name restriction.

## ChatGPT Legacy Record

The old ~/.agents/config/ask-chatgpt/defaults.yaml record remains ChatGPT-only input.
Recognize schema ask-chatgpt-defaults/v2 and older unversioned records only after the
provider is resolved to ChatGPT.

For ask-chatgpt-defaults/v2, default_transport_mode is required:

- codex-app-native or desktop-built-in-browser selects which verified ChatGPT route
  is tried first;
- manual stops before external action;
- missing or unknown values block external action pending explicit repair.

For an unversioned legacy record:

- missing mode, desktop-built-in-browser, and capability-auto remain built-in-first;
- manual stops before external action;
- current-chrome-explicit and standalone-playwright-explicit remain non-authorizing
  hints and otherwise retain built-in-first fallback;
- chatgpt-cloud-browser or an unknown value stops for explicit migration;
- default_transport_mode without a schema version is ambiguous and blocks.

Do not reinterpret, copy, rewrite, or delete a legacy record automatically. Migration
is a persistent external configuration change and requires explicit authorization.
When authorized, write one complete Ask AI v1 record, report before/after route
meaning, verify it, and retain or remove the legacy record only as separately directed.

## Route Evidence

Browser fields apply only to their provider and browser route. Keep built-in,
cloud/agent reviewer, Chrome, standalone, provider, account, and conversation
identities separate. Do not transfer cookies, login, tab, model, or capability
evidence. A profile path remains Not verified unless the active surface exposes it.

## Reset

Update, migrate, reset, or delete defaults only after explicit instruction. Reset
clears bridge records, not real browser data, conversations, review artifacts, source,
commits, or installed Skills.
