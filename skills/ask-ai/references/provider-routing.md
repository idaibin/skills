# Provider Routing

## Contents

- [Selection](#selection)
- [Capability Contract](#capability-contract)
- [Defaults And Compatibility](#defaults-and-compatibility)
- [Fallback](#fallback)
- [User-Defined Review Instructions](#user-defined-review-instructions)
- [Multi-Provider Independence](#multi-provider-independence)
- [Portable Browser Providers](#portable-browser-providers)

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
Normalize common provider aliases only inside an external-AI selection context:

| Canonical provider | Recognized aliases |
| --- | --- |
| ChatGPT | `GPT`, `Chat GPT` |
| Gemini | `Google Gemini`; `Google` or `谷歌` only when the request clearly means an AI reviewer rather than Search or another Google product |
| Claude | `Anthropic Claude` |
| DeepSeek | `Deep Seek`, `DeepSeek Chat` |
| Kimi | `Moonshot Kimi` |
| Qwen | `通义千问`, `千问`, `Qwen Chat`, `Qwen Studio` |
| GLM | `智谱`, `智谱清言`, `ChatGLM` |
| Grok | `xAI Grok` |
| Perplexity | `Perplexity Ask` |
| Doubao | `豆包` |
| Mistral Vibe | `Mistral`, `Vibe Chat`, `Le Chat` |
| Tencent Yuanbao | `腾讯元宝`, `元宝` |
| ERNIE | `文心一言`, `文心助手`, `文心` |

Provider aliases select only the recipient. They do not imply a model version,
capability, route, round count, send authorization, or multi-provider workflow.

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

## User-Defined Review Instructions

Ask AI has no built-in multi-provider roster or phrase such as `三方会审`. A user may
explicitly create a durable review instruction at:

    ~/.agents/config/ask-ai/instructions.yaml

Use schema `ask-ai-instructions/v1`:

    schema_version: ask-ai-instructions/v1
    instructions:
      three-way-review:
        aliases: [进行三方会审]
        external_providers: [chatgpt, gemini]
        local_review: repo-review
        package_policy: identical-provider-neutral
        prompt_profiles: [architecture, adversarial, source-check]
        rounds_per_provider: 1
        authorization: send-on-exact-invocation
        stop_after: local-reconciliation

This is an example configuration, not a built-in default. Create, update, rename, or
delete an instruction only when the user explicitly asks to persist that definition.
Report the exact alias, participants, send behavior, rounds, and stop condition before
writing, and verify the complete record after an atomic write. Never infer a roster
from the instruction name.

`prompt_profiles` may contain only built-in IDs from `review-prompts.md`. Profiles
change review focus, not recipients, authorization, models, routes, rounds, mutation
scope, or delivery. Unknown profile IDs block instruction execution without rewriting
the record.

Resolve only an exact configured alias when the whole current request, after trimming
surrounding whitespace and normalizing case for Latin text, equals that alias. Do not
use a prefix, suffix, punctuation extension, substring, fuzzy, semantic, or translated
match for an executable alias. Provider-name aliases remain normal provider selection
and do not create a workflow instruction.

`authorization: send-on-exact-invocation` means that the user's current exact alias
invocation is current-request authorization for the saved recipients and round count;
the stored file alone never sends anything. `package-only` never sends. Unknown
authorization values, invalid providers, missing rounds, duplicate aliases, unknown
schema versions, or conflicting records block external action without rewriting the
file. Current-request constraints such as `不要发送`, an explicit provider roster, or
a lower round count override the stored instruction; any expansion of recipients,
rounds, data, capability, or mutation scope requires fresh explicit authorization.

When an exact instruction is invoked and its subject/basis is unambiguous, freeze one
package and execute the configured independent reviews without asking again for saved
recipients or send scope. If the subject/basis is ambiguous, ask once before package
creation. If a route is blocked, complete safe independent work, mark that participant
incomplete, and never silently substitute another provider. Codex/local review is not
an external provider and never receives a browser-operation ledger.

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

## Portable Browser Providers

For Claude, DeepSeek, Kimi, Qwen, GLM, Grok, Perplexity, Doubao, Mistral Vibe,
Tencent Yuanbao, ERNIE, or another named browser provider, load
[provider-browser.md](provider-browser.md). Its entry points and observed controls are
discovery hints, not current capability proof. Live preflight must still prove the
exact target, login class, clean composer, intended input, submit control, side effect,
completion signal, and response attribution. Do not assume upload, search, research,
image, model, API, MCP, project, notebook, or persistent-conversation behavior.

If any required step is unavailable, keep the provider result Package-only or Not
verified. Do not create speculative metadata or claim support from the provider name.
