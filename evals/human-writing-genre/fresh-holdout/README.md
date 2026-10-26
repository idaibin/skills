# Fresh held-out extension

Sixteen independently designed synthetic inputs, two per original genre: one Chinese
and one English, with short/long assignments crossed. They were frozen after
independent pre-output scope review and the v8 candidate snapshot, before either
original or candidate writer ran. The older96 inputs and criteria stay unchanged.

Give writers only cases.json and a frozen skill, never oracles.json. The oracle
separates required coverage from conditional fidelity: an optional detail may be
omitted; if retained its facts must remain faithful. Literal modes are exact_body,
immutable_span, must_include and if_referenced. The last requires semantic review
when a name is omitted or paraphrased; it is not a mandatory substring. Check each
social candidate against the requested role and applicable limits separately.

Required facts, unsupported additions and operation boundaries are hard gates.
Assess the anchored genre dimensions only after a hard pass. Synthetic labels are
not part of requested finished artifacts. Exact-no-op and local-span boundaries
are explicit in each input. No output or grading key was used to revise the frozen
r4 design. Later use for repairs makes this a regression set, not fresh holdout.

Run the parent validate_corpus.py for hash, identity and type counts. The original
mechanical_checks.py accepts the original96 format only; it does not grade this
extension. A reviewer must evaluate these explicit constraints against sources;
no detector or scalar model score establishes correctness or general improvement.

## Exact-no-op reporting boundary

The original96 rubric declares genre quality inapplicable/null on exact no-op
cases. This extension has explicit completion/integrity anchors for its exact-body
case: keep those frozen anchors, but report them as conservation/compliance checks,
not stylistic quality or improvement. Do not pool their automatic post-hard-pass
2-point values with genre-quality scores. Neither criterion nor output changes.
