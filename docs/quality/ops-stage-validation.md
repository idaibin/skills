# Ops failure-stage validation

Basis: `309d5ebcb5e204911645cc8bf596d595d895850e`, isolated local branch;
original dirty source files were not incorporated. These results qualify the changed
contracts only and do not certify real client/browser work or comparative efficiency.

## Executable regression

A synthetic `review-attempt` event explicitly marked `failed-before-submit` was
accepted by the prior feedback recorder. The new negative regression failed against
the prior implementation (15 tests, one failure). A narrow guard rejects explicit failed-before-submit state for all three feedback
event types before persistence; subtests cover review-attempt, response-captured and
verification-update. Positive cases retain `submitted` and `ambiguous`
attempts. Legacy events without this field remain accepted; the recorder cannot
infer missing transport proof or establish provider submission from metadata alone.
This does not prove that any past live invocation emitted an invalid event.

## Decision cases

Four fresh Codex CLI 0.163.0 invocations used the same eight synthetic prompts in
B/C/C/B order, configured `gpt-6.1-sol` / medium, read-only mode and the same requested
tool surface. B supplied baseline references; C supplied the additional original-
configuration discovery preflight. All four naturally exited 0. Raw JSONL, exact
prompts, command arrays, timings, usage, separate oracles and readback are retained
under ignored `.codex/artifacts/ops-stage-*20261022*` evidence.

Cases cover registry versus process creation, transport recovery timeout, directly
proven pre-submit initialization failure, nonzero exit without submission proof,
accepted-turn reconciliation, historical/caller-local and truncated evidence,
untrusted authority, and a valid completed no-op/source-owner boundary.
Codex readback found no invented recovery, resend, permission bypass or completion;
the first baseline used unverified rather than explicitly not-run for downstream
acceptance. Independent grading is retained in the ZCode evidence, not implied by
these expected results.

These are supplied-rule text decisions, not automatic Skill selection, executed
business workflows, or real reconnect acceptance. Effective provider snapshot and
global-context isolation were not independently proven. Input usage differed more
than the supplied rule delta, so timing/token comparisons are confounded. CLI-reported
cache-write zero lacks billing/TTL corroboration. No efficiency gain is claimed.

## Scope and retention

The seven maintainer cases reuse existing submission, authorization, evidence and
completion rules. ZCode preflight checks existence/readability of the original
installed resources using a verified build binding; it does not dump credentials,
replace configuration, or change accounts. Canonical protocol files and synchronized
copies are unchanged. The historical six writing runs / 36 answers were not rerun
and are not proof of this candidate; only their public regression inputs are retained.

Full fixed-basis gate results and independently attributed ZCode findings are recorded
in the task evidence. Research adoption decisions remain in the fixed Handbook record.

## Asset mapping and preservation

The seven new maintainer rows are contract scenarios rather than a one-to-one run
count. Registry, transport, initialization and accepted-turn rows map to their named
live cases; the initialization row also has the inverse exit-only-ambiguous control.
Historical/caller-local and truncated-evidence rows are combined in old-lock-and-partial.
The denied-operation row is exercised by untrusted-authority. Valid-noop-owner is an
additional positive control for the existing evidence-reuse and source-owner boundary.

Writing assets are five semantic-quality rows plus one adjacent-owner JSON case,
six public inputs total. The older six runs × six answers are historical; none of
those six inputs was rerun on this candidate. Their JSON status remains candidate.

The original 11 dirty files and this candidate's file count belong to different
worktrees, not an 11-minus-three selection. All 11 original dirty files remain in
place; none was staged from that working tree. Candidate hunks were authored from
the clean fixed HEAD, including its original metadata and 92-case routing basis.
