# Feedback Recording

## Contents

- [Boundary](#boundary)
- [Terminal Chain](#terminal-chain)
- [Return Gate](#return-gate)
- [Completion And Failure](#completion-and-failure)

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
counts, strict opaque identifiers, SHA-256 values, and controlled evidence labels.
New events do not accept free-text summary, hypothesis, or experiment fields. Existing
append-only history remains readable but is not rewritten or used as authority. Never include raw prompts,
responses, source, secrets, account names, URLs, filesystem paths, or browser-profile
data.

Task-effect metadata is additive and optional, so existing v1 events remain valid.
Use `task_phase` (`plan`, `execute`, `review`, `verify`) and `task_class`
(`frontend`, `backend`, `test`, `architecture`, `bug-diagnosis`, `bug-fix`,
`design`, `tooling`, `cross-layer`, `other`) to classify comparable work. They may
appear in any terminal-chain event once the task basis is known.

Only a `verification-update` may record locally reconciled result fields:

- `first_pass_outcome`: `accepted`, `rework-required`, `incomplete`, `failed`, or
  `not-verified`;
- `rework_rounds` and `unresolved_attempts`: non-negative integers;
- `final_acceptance`: `accepted`, `accepted-with-gaps`, `rejected`, `incomplete`, or
  `not-verified`;
- `user_correction`: `none`, `clarification`, `scope-reset`, `boundary-reset`,
  `rollback`, `acceptance-change`, or `not-verified`.

These fields describe one verified round; they do not rank a model or provider. Do
not change routing from one event. Require at least three comparable verified rounds
across two distinct fixed bases inside the user-configured evidence window, and keep
runtime availability separate from task quality.

## Return Gate

After local reconciliation and before returning the assembled result:

1. Resolve the user-owned configuration once. Missing, invalid, or disabled feedback is
   `feedback-not-applicable`; do not create a default configuration.
2. If enabled, compare the round's deterministic event identities with the append-only
   log and attempt each applicable missing terminal-chain event exactly once, in order.
3. Report `feedback-recorded` only after successful recorder exit and matching log
   readback. Otherwise report `feedback-deferred` with the ordinary review artifact as
   the evidence owner.

Do not backfill attribution, terminal state, or acceptance from a requested alias,
response prose, host process exit, or the feedback log itself. The ordinary provider
ledger remains authoritative; this gate only prevents an enabled metadata recorder
from being silently skipped.

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
