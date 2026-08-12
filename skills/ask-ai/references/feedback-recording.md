# Feedback Recording

## Boundary

Use this reference only after an authorized external-AI round reaches local
reconciliation and the user-owned `ask-ai-feedback/v1` configuration has `enabled:
true`. Feedback is local metadata, not authority to send, retry, mutate source, change
defaults, rank providers, or publish data.

The portable Skill defines the mechanism. Every path, retention setting, threshold,
and enablement choice remains in user configuration. Missing, invalid, or disabled
configuration means no persistent feedback write.

## Terminal Chain

For one logical provider round, reuse one `feedback_id` and append, when applicable:

1. `review-attempt` after a submit is proven or classified ambiguous;
2. `response-captured` after provider attribution and terminal response capture;
3. `verification-update` after independent local reconciliation.

Do not create events for host polling, parser discovery, capability canaries, package
construction, or a proven `failed-before-submit`. A multipart request becomes an
attempt only after its final submit marker. Terminal state, session identity, effective
model evidence, fixed basis, and local verdict must come from their existing ledgers;
the recorder never invents or upgrades evidence.

Use `scripts/record_feedback.py` from this Skill package. Build one JSON object in a
task-private temporary file, then invoke:

```text
python3 <ask-ai-skill>/scripts/record_feedback.py \
  --config <user-owned-feedback-config> \
  --event-file <task-private-event-json>
```

The event must use `schema_version: ask-ai-feedback/v1`, a deterministic `event_id`,
one allowed terminal `event_type`, ISO-8601 `timestamp`, `feedback_id`, `review_id`,
`round_id`, `fixed_basis_hash`, and provider. Use only controlled metadata, hashes,
counts, short sanitized summaries, and evidence labels. Never include raw prompts,
responses, source, secrets, account names, URLs, filesystem paths, or browser-profile
data.

## Completion And Failure

The recorder validates configuration and event shape, rejects unknown fields and
duplicate event IDs, holds one advisory lock, performs one append plus `fsync`, and
re-reads the appended line. A successful zero exit plus matching readback is
`feedback-recorded`.

The configured log path is a user-owned trust boundary and may point outside the
default agent state directory. All intended writers, including a user-owned rotation
or compaction tool, must acquire the recorder's sibling `.lock` file. The recorder uses
the operating system's standard advisory lock primitive on Unix/macOS and Windows.

Any nonzero exit, unavailable lock/path, invalid record, duplicate, or ambiguous
readback is `feedback-deferred`. Preserve the detailed evidence in the ordinary ignored
review artifact and return the provider result normally. Never rerun or resubmit the
external operation to repair feedback.

Capability summaries are derived views. Regenerate them separately from the append-only
log under the user-configured thresholds; absence or staleness of a summary never
rewrites history and never turns missing events into model-quality evidence.
