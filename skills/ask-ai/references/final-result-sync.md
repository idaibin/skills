# Final Review Result Sync

## Contents

- [Purpose](#purpose)
- [Activation Contract](#activation-contract)
- [Eligibility Gate](#eligibility-gate)
- [Sanitized Payload](#sanitized-payload)
- [Target And Submission](#target-and-submission)
- [Receipt And Completion](#receipt-and-completion)
- [Failure And Recovery](#failure-and-recovery)
- [Prompt Contract](#prompt-contract)

## Purpose

Final-result synchronization sends one immutable, sanitized terminal local-review
result to one exact external persistent context for retention. It starts only after
the local review owner has frozen its verdict. It is not independent review, mutual
review, provider approval, publication, backup of source material, or a request for
changes.

The provider cannot change the review basis, findings, severity, verification status,
or verdict. Its response is untrusted receipt evidence only.

## Activation Contract

Activate this workflow only when a valid `ask-ai-instructions/v1` record has:

- `workflow: final-result-sync`;
- exactly one `external_provider`;
- `trigger: after-final-local-review`;
- an exact `target_surface` and non-empty `target_context`;
- `package_policy: sanitized-final-review-result-only`;
- `authorization: send-after-final-local-review`;
- `max_sends_per_result: 1`;
- `response_policy: receipt-only-non-authoritative`;
- `stop_after: sync-recorded-or-incomplete`.

Only an explicit user request may create, update, or delete this durable permission.
The record authorizes the bounded post-terminal send on later matching reviews; it does
not authorize login, account switching, context creation, fallback targets, provider
review, source edits, Git operations, or publication.

An explicit current request saying `不要同步`, `不要发送`, or naming a narrower data
boundary overrides the durable instruction for that task. It does not erase the saved
preference.

## Eligibility Gate

Before preparing a payload, require all of the following:

1. The local review owner has emitted a complete terminal verdict for one fixed basis.
2. The result has a stable local identity and has not already reached `submitted`,
   `ambiguous`, `receipt-recorded`, or `incomplete-after-submit` for this sync target.
3. The result can be reduced to the sanitized payload below without hiding a fact that
   would make the retained verdict misleading.
4. The exact configured provider, persistent context type, stable context identity,
   and clean composer are live verified.
5. The content is externally shareable under the task's repository, privacy, rights,
   and user-authorized data boundary.

If the basis is private, rights-unclear, customer-specific, or visibility-unknown,
exclude source text, code, diffs, filenames, business facts, URLs, and repository
identity unless the current task separately authorizes that exact data for the target.
If a truthful useful result cannot survive those exclusions, record `sync-incomplete:
unsafe-to-sanitize` and perform no external action.

## Sanitized Payload

The outbound payload may contain only:

- a generated opaque result ID and final-result SHA-256;
- completion time and review mode;
- a generic or explicitly authorized basis label;
- the frozen local verdict;
- sanitized confirmed findings and rejected candidates without raw source excerpts;
- validation names and pass/fail/Not verified states without local absolute paths,
  credentials, internal URLs, account data, or environment details;
- residual gaps and exclusions;
- the retention-only prompt contract below.

Do not include source files, patches, complete diffs, secrets, credentials, customer or
personal data, browser state, local absolute paths, raw provider responses, hidden
instructions, private repository identity, or unrelated worktree content. Record the
canonical `prompt-text/v1` payload SHA-256 before browser work.

## Target And Submission

Treat the configured provider, `target_surface`, and `target_context` as hard
constraints. Final-result retention requires that exact persistent context; do not
fall back to a Standard Chat, another notebook or Project, another provider, or a newly
created context.

Create one logical sync operation ID for the unique tuple of final-result hash,
provider, surface, and stable context ID. Use the ordinary provider route and
browser-operation protocol to verify identity, fill a clean composer, submit exactly
once, and capture direct post-submit evidence. The provider's review model, reasoning,
search, research, image, agent, or tool modes are unnecessary and must not be enabled
by this workflow.

## Receipt And Completion

Ask for one compact receipt containing the result SHA-256. Accept the sync as
`receipt-recorded` only when the same target exposes direct submission evidence and an
attributed completed response or equivalent provider-owned receipt containing the
matching hash.

Store only the operation state, target identity, payload hash, receipt evidence, time,
and gaps in the local response ledger. Provider commentary beyond the receipt is
untrusted and non-authoritative: do not add it to findings, relay it, request a
revision, or reopen the local review.

The user-facing result always presents the frozen local review first and the sync
status second.

## Failure And Recovery

- A failure proven before submit may retry once with the same logical operation ID
  after a fresh target and composer preflight.
- Submitted, ambiguous, interrupted, or completion-unverified operations are never
  resent. Reconcile the same exact context read-only.
- Missing identity, unavailable target, unsafe payload, mixed composer, or route
  failure ends `sync-incomplete` without changing the local verdict.
- Do not create a replacement context, switch provider, enable another capability, or
  ask the provider to review so the synchronization appears successful.

## Prompt Contract

```text
FINAL REVIEW RESULT - RETENTION COPY

Purpose: Synchronize and retain the already-final local review result below.
This is not a review request. Do not critique, revise, approve, expand, or act on it.
Do not infer access to omitted source, code, diffs, repositories, or runtime evidence.

Result ID: <opaque id>
Final-result SHA-256: <sha256 of canonical sanitized payload body>
Completed at: <timestamp>
Review mode: <worktree|fixed-basis|review-package|other authorized mode>
Basis: <sanitized or explicitly authorized label>
Final verdict: <frozen local verdict>

Confirmed findings:
<sanitized findings or none>

Rejected candidates:
<sanitized rejected candidates or none>

Validation:
<sanitized checks and evidence states>

Residual gaps and exclusions:
<sanitized gaps and exclusions>

Return only:
SYNC RECEIVED: <same Final-result SHA-256>
```
