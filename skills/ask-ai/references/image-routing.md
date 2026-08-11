# Image Capability Routing

## Contents

- [Capability Selection](#capability-selection)
- [Authorization And Provider Boundary](#authorization-and-provider-boundary)
- [Google Gemini Image Mode](#google-gemini-image-mode)
- [Input And Output Evidence](#input-and-output-evidence)
- [Live Preflight And Completion](#live-preflight-and-completion)
- [Stop Conditions And Output](#stop-conditions-and-output)

## Capability Selection

Select exactly one capability from the current request:

- `image-review`: inspect declared images, visual artifacts, or screenshots and return
  attributed observations. It never creates, edits, or replaces an image.
- `image-generate`: create a new image or bounded set of variants from an approved
  prompt and declared references.
- `image-edit`: transform one declared baseline image while preserving the stated
  invariants and returning a distinct output.
- `visual-exploration`: generate bounded candidate directions for a product or design
  question. Candidates are exploratory assets, not accepted UI specifications or
  runtime proof.

Do not infer `image-generate` or `image-edit` from `image-review`. Do not call a
visual exploration a product decision, selected source, implementation approval, or
accessibility/runtime verification.

## Authorization And Provider Boundary

Package-only wording may prepare a redacted prompt and asset manifest, but never
opens a provider, uploads an input, creates an image, edits an image, or downloads an
output. `image-review` requires explicit authorization to send any image to an
external provider; local inspection stays with the local owner.

When no external provider is named, prefer an available host image tool for explicit
generation or editing. Route to that owner instead of opening an external-AI route.
When the user names a provider, that provider is a hard recipient and artifact
constraint: do not substitute a host image tool, a different provider, model, mode,
or transport. If the named route cannot prove the requested image capability, stop at
Package-only or Not verified.

Treat each upload, generation, edit, and download/export as a distinct external side
effect with its own operation ID. A request to create an image authorizes only the
declared asset and variant count; an edit authorizes only the declared baseline and
transformation. Never overwrite a baseline or an existing output without explicit
overwrite authorization.

## Google Gemini Image Mode

For Gemini `image-generate`, `image-edit`, or `visual-exploration`, load
`provider-gemini.md` and use only the Gemini tools-menu capability whose canonical
Chinese UI label is **「图片 — 图片生成与编辑」**. Selecting Gemini as the provider,
mentioning image creation in the prompt, attaching an image, seeing a generic image or
media control, or receiving an image-like response does not activate or prove this
capability.

Before filling the prompt or attaching an edit baseline, create a distinct mode-select
operation, open the Gemini tools menu, select **「图片 — 图片生成与编辑」**, and capture
direct visible evidence that this exact mode is active in the clean composer. Reverify
the active mode after attachment and immediately before submit. If the exact item or
active-state evidence is absent, ambiguous, disabled, reset, or unavailable on the
current account/region/UI, stop `Not verified` without submission. Do not fall back to
ordinary Gemini chat, image upload alone, another Gemini media mode, a different
provider, or a host image tool unless the current request separately authorizes that
fallback.

This hard mode gate does not apply to `image-review`: a review may use only a separately
verified visual-input route and must not select the generation/editing tool by
implication.

## Input And Output Evidence

Before a provider action, freeze and redact an asset manifest. Record only the minimum
needed to identify each authorized input:

- local path or sanitized stable identifier, content hash, type, dimensions, and scope;
- source/owner, rights or user authorization, and approved use/ignore rules;
- any visual references, prompt, exclusions, and aspect-ratio or delivery constraints;
- for edits, the baseline hash and the exact properties to preserve or change.

Do not upload secrets, private customer images, browser-profile data, unrelated assets,
or material whose source/rights boundary is unknown. A reference image does not grant
permission to reproduce a protected work, logo, person, or style beyond the stated
authorization.

For every generated or edited output, record provider/product surface, visible model or
mode or `Not verified`, operation ID, output identifier/path and hash when captured,
prompt identity, input/baseline identity, variant number, and observed completion
evidence. For review, record only the inspected input identity and the attributed
review response; no output asset is implied. Do not claim a seed, exact model, edit
fidelity, originality, rights clearance, or deterministic reproduction unless the
current provider surface exposes evidence for it.

## Live Preflight And Completion

Provider documentation, a visible Images label, or an upload icon proves discovery at
most. Before an external image side effect, freshly verify the authorized provider,
account/session category, final target, selected image capability, clean input state,
authorized input attachment, unique enabled submit control, and expected completion
signal. Verify active mode rather than inferring it from a stored preference or label.

For an edit, verify that the rendered attachment is the frozen baseline, not an
unrelated draft. For generation or exploration, verify that the prompt and requested
variant count are bounded. After submit, accept completion only from a provider-owned
output container or exported artifact bound to the same operation; a prompt echo,
spinner disappearance, toast, or gallery thumbnail alone is insufficient.

Capture the output before any follow-up operation. If upload, submit, output identity,
or completion is ambiguous, reconcile the original route read-only. Never resend,
regenerate, switch provider, or create a replacement output automatically. Treat a
failed-before-submit attempt as retryable only under the shared browser-operation
protocol with the same operation ID and direct proof of no side effect.

## Stop Conditions And Output

Stop before external action when authorization, provider, source/rights boundary,
baseline, active image capability, attribution, or completion cannot be verified. For
an image review, stop once the requested observations are captured; do not offer a
generation follow-up without separate authorization.

Report the selected capability, authorization boundary, provider or host-tool decision,
input manifest/redactions, operation states, output or response attribution, edit
baseline/output relationship, completion evidence, cleanup/retained assets, and every
Not found or Not verified gap. State clearly that generated visual candidates do not
prove runtime UI behavior, implementation fidelity, legal clearance, or product facts.
