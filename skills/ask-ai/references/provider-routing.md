# Provider Routing

## Contents

- [Selection](#selection)
- [Capability Contract](#capability-contract)
- [Defaults And Compatibility](#defaults-and-compatibility)
- [Fallback](#fallback)
- [Multi-Provider Independence](#multi-provider-independence)
- [Unsupported Providers](#unsupported-providers)

## Selection

Resolve provider recipients before transport:

1. Use every provider explicitly named in the current request and no others.
2. Treat legacy ask-chatgpt wording as an explicit ChatGPT selection.
3. When the user requests an external result but names no provider, read a valid
   provider-neutral default. If none exists, use one provider only when the task
   context already establishes it unambiguously; otherwise ask for the provider.
4. Never infer a provider from an open tab, installed app, available connector, prior
   response, or whichever route is easiest.

Provider names are external recipients, not interchangeable execution profiles.

## Capability Contract

For each selected provider record:

- provider and requested capability;
- target surface and stable identity when exposed;
- supported host/native/browser transports;
- account/workspace/session evidence without secrets or PII;
- input and attachment limits actually exercised;
- model/reasoning/tool selection evidence when required;
- submit postcondition, completion signal, response container, and attribution;
- reconciliation and retry boundary;
- live gaps marked Not found or Not verified.

A provider reference describes known routing rules but never proves the current page,
session, controls, quota, model, or capability.

## Defaults And Compatibility

New provider-neutral records live at:

    ~/.agents/config/ask-ai/defaults.yaml

Use schema_version ask-ai-defaults/v1 with:

- default_provider: one provider name or manual;
- provider-specific sections for transport, surface, project/notebook hint, model,
  reasoning, browser preference, and ordered fallbacks;
- last_verified_at as informational evidence only.

Explicit current-request values override defaults. Stored provider, project/notebook,
conversation, model, browser, or account hints never prove current selection.

The old path ~/.agents/config/ask-chatgpt/defaults.yaml and schemas without an Ask AI
schema remain ChatGPT-only legacy input. Read them only when ChatGPT is selected or
legacy ask-chatgpt wording is used. Do not reinterpret them as provider-neutral, copy
them automatically, or delete them. Persistent migration requires explicit user
authorization and an atomic before/after report.

## Fallback

Fallback may change transport inside the same provider only when:

- the current request did not make the route a hard constraint;
- the provider reference defines the fallback;
- the target identity and capability are freshly verified;
- no earlier submission is submitted, ambiguous, or unresolved.

Changing provider is never an implicit fallback. The current request may explicitly
authorize an ordered alternative such as "use DeepSeek only if Gemini is unavailable";
treat that as a separate conditional provider result with its own round and ledger,
not as transport recovery. A provider is unavailable only when, before any submit,
its required identity, clean authorized context, capability, or permitted route cannot
be verified after provider-defined same-provider fallbacks. An unrelated draft alone
does not make the provider unavailable when the send authorization permits a separate
clean conversation. If the condition or unavailability is not proven, stop at
Package-only or Not verified. Never activate an alternative after a submitted,
ambiguous, or unresolved operation for the primary provider.

## Multi-Provider Independence

For an explicitly authorized provider set:

1. Freeze one package hash and provider-neutral response contract.
2. Assign a distinct round_id and operation ledger to every provider.
3. Use separate conversations and tabs or verified task contexts.
4. Verify each provider's identity and composer independently; do not transfer cookie,
   account, tab, login, model, completion, or response evidence.
5. Send the same package without another provider's response, critique, or verdict.
6. Capture every response or explicit incomplete state before comparison.
7. Let Codex verify and deduplicate findings against the fixed local basis.

Parallel execution is optional. Independence comes from input, operation, attribution,
and evaluation isolation, not from concurrency or an assumed incognito browser.

## Unsupported Providers

DeepSeek, Kimi, or another named provider without a package reference may use a browser
route only after live preflight proves the exact target, authenticated state, clean
composer, intended input, submit control, side effect, completion signal, and response
attribution. Do not assume upload, search, research, image, model, API, MCP, project,
notebook, or persistent-conversation behavior.

If any required step is unavailable, keep the provider result Package-only or Not
verified. Do not create speculative metadata or claim support from the provider name.
