# Portable Browser Provider Routing

## Contents

- [Supported Boundary](#supported-boundary)
- [Entry Points](#entry-points)
- [Login Classification](#login-classification)
- [Composer And Submit](#composer-and-submit)
- [Default Capability](#default-capability)
- [Provider Discovery Hints](#provider-discovery-hints)
- [Completion And Recovery](#completion-and-recovery)

## Supported Boundary

Use this reference for a named AI browser provider that has no dedicated host-native
contract in this package. It standardizes live preflight and evidence; it does not
make product interfaces interchangeable and does not promise that a free, regional,
account, model, quota, or capability tier is currently available.

Use semantic UI evidence discovered through ops-browser. Do not publish or persist
CSS selectors, generated class names, coordinates, cookies, local storage, account
identifiers, or other profile data. A canonical product URL is only a discovery entry
point. The final origin, route, identity, composer, submit, completion, and response
container must be verified again for every authorized external round.

## Entry Points

Start with the provider explicitly selected by the user. The canonical aliases in this
table mirror [provider-routing.md](provider-routing.md), which remains the selection
authority:

| Provider | Recognized aliases | Canonical web entry |
| --- | --- | --- |
| Claude | Anthropic Claude | `https://claude.ai/` |
| DeepSeek | Deep Seek, DeepSeek Chat | `https://chat.deepseek.com/` |
| Kimi | Moonshot Kimi | `https://www.kimi.com/` |
| Qwen | 通义千问, 千问, Qwen Chat, Qwen Studio | `https://chat.qwen.ai/` |
| GLM | 智谱, 智谱清言, ChatGLM | `https://chatglm.cn/` |
| Grok | xAI Grok | `https://grok.com/` |
| Perplexity | Perplexity Ask | `https://www.perplexity.ai/` |
| Doubao | 豆包 | `https://www.doubao.com/chat/` |
| Mistral Vibe | Mistral, Vibe Chat, Le Chat | `https://chat.mistral.ai/chat` |
| Tencent Yuanbao | 腾讯元宝, 元宝 | `https://yuanbao.tencent.com/` |
| ERNIE | 文心一言, 文心助手, 文心 | `https://wenxin.baidu.com/` |

Accept a different official route only when the user supplies it or visible navigation
from the canonical product proves it. Reject unrelated search results, clone sites,
API consoles, model playgrounds, and similarly named products as conversation targets.

## Login Classification

Classify the rendered route before touching the composer:

- `authenticated`: direct non-PII evidence shows an active account session and the
  intended conversation surface is usable;
- `anonymous-composer`: a clean conversation composer is visible, but anonymous
  submission and response capture have not yet been proven;
- `anonymous-conversation`: an explicitly authorized prompt produced one attributed
  response without authentication; this is the only state that proves direct anonymous
  conversation for the current route;
- `sign-in-gated`: the conversation route redirects to sign-in or exposes no usable
  composer until sign-in;
- `challenge-gated`: CAPTCHA, bot protection, consent, or another security challenge
  blocks the route;
- `unreachable`: navigation ends in a network, DNS, policy, or region error;
- `indeterminate`: the page is blank, partially rendered, or exposes contradictory
  identity and composer evidence.

A login or register button beside a usable composer does not by itself prove that
login is mandatory. Conversely, a visible composer does not prove free anonymous
conversation. When sign-in or a challenge is required, stop before credentials,
one-time codes, account choice, consent, CAPTCHA, or permission grants and ask the
user to complete that step on the selected browser surface.

## Composer And Submit

On a normal route:

1. Discover the prompt control semantically from a unique visible textbox, textarea,
   or contenteditable conversation field. A file input, search combobox, phone field,
   verification-code field, or hidden textarea is not the prompt composer.
2. Require the composer to be clean. Preserve unrelated drafts and existing
   conversations; use a new conversation only when current authorization permits it.
3. Inventory attachment and mode controls without activating them. Their visibility
   proves discovery only.
4. Fill only after external-send authorization and bind the exact text to the round
   ledger. Verify the rendered composer value before submit.
5. Resolve one unique enabled semantic send control from a fresh page observation.
   Login appearing after fill or submit returns `sign-in-gated`; it does not authorize
   authentication or provider fallback.
6. Accept submission only from a new rendered user message, a stable conversation
   identity, an active-generation signal, or another provider-owned postcondition.

Never use placeholder wording, DOM position, icon appearance, or a remembered button
location as the sole composer or submit identity.

## Default Capability

The default portable capability is one ordinary text conversation on a clean new or
explicitly selected chat. Search, deep research, thinking/reasoning, file upload,
images, video, voice, code, agents, presentations, data analysis, connectors,
projects, notebooks, and model selection are separate capabilities.

When the provider-neutral review-context preference is configured, inspect for one
true persistent Project/notebook/space/collection with that name before opening the
ordinary chat. Reuse it only with live container and stable-identity evidence. If the
provider does not support it or verification fails, open a clean new ordinary chat for
the authorized review. History groups and renamed conversations do not satisfy this
preference, and the preference never authorizes container creation.

Select a non-default capability only when the current request explicitly authorizes it
and live UI evidence proves that it is active before submit. Provider defaults never
upgrade ordinary text review into search, media, upload, agent, external-tool, code, or
other non-default work. A mode label or control proves availability at most; it does
not prove active selection, plan entitlement, quota, input limits, output quality, or
completion.

For aggregating products such as Perplexity or Tencent Yuanbao, record the active
underlying model when the UI exposes it. If it cannot be verified, attribute the
response to the product surface and mark model identity `Not verified`; never count it
as an independent model-family result merely because the product name differs.

## Provider Discovery Hints

These hints identify what to inspect, not what to claim. They were observed or
documented during package maintenance and may drift:

| Provider | Inspect first | Capability candidates requiring live proof |
| --- | --- | --- |
| Claude | challenge/login state, Chat versus Cowork, composer | files, code execution, Projects, Cowork |
| DeepSeek | sign-in redirect, composer after login | model, thinking, search, files |
| Kimi | anonymous composer and login-for-history boundary | Agent Swarm, Deep Research, Code, files |
| Qwen | anonymous composer, login/register boundary | files, thinking, images, active model |
| GLM | composer, active GLM label, account state | thinking, Agent, research report, PPT, data analysis, files |
| Grok | normal render and sign-in state | files, search, images/video, voice, connectors |
| Perplexity | network reachability, anonymous Ask composer | Pro Search, Research, model selector, files, Projects |
| Doubao | composer and account state | images, video, deep research, PPT, writing, transcription, music |
| Mistral Vibe | sign-in state and Chat mode | voice, files, research, Projects, Work, Code |
| Tencent Yuanbao | composer, login boundary, underlying model | files, search, thinking, Hunyuan/DeepSeek selection |
| ERNIE | final `wenxin.baidu.com` route, composer, account state | search, files, images, agents, active model |

ChatGPT and Gemini use their dedicated provider references. Do not weaken their
Project, notebook, App-native, or completion rules by applying this generic profile.

## Completion And Recovery

After submit, wait for a provider-owned completion signal and capture only the
attributed assistant response in the same resolved conversation. Record provider,
final URL or stable conversation ID, login class, requested and observed capability,
model identity or `Not verified`, operation state, completion evidence, and gaps.

Before submit, one same-URL refresh is allowed only for an abnormal or indeterminate
page, followed by full reclassification. Challenge-gated, sign-in-gated, unreachable,
and region/policy failures are blockers, not refresh loops. After submit, interruption
or missing completion becomes ambiguous or completion-not-verified; reconcile the same
conversation read-only and never resend, regenerate, change provider, or create a
replacement conversation automatically.
