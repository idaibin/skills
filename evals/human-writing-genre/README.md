# Human Writing genre evaluation corpus

Version 2.0: 96 independently composed synthetic source texts. Each of eight stable
primary types has 10 development and 2 held-out inputs, 8 Chinese and 4 English.
Types are message/email, status/notice, tutorial/how-to, explanation/reference,
product/release, research/opinion, social/candidates, and personal nonfiction.
Proofreading, local editing and drafting are operations, not additional genres.
One input counts once, regardless of versions, output candidates or repeat runs.

## Files and use

`development-inputs.json` and `holdout-inputs.json` are writer-visible requests and
sources. Give the writer only its selected input plus the frozen skill version;
never expose `oracles.json`, grading scripts, sibling outputs or earlier reviews.
`oracles.json` is review-only and records fact units, scope, literal protection,
applicability and genre anchors. `review-result.schema.json` captures one independent
anonymous assessment per artifact. Every artifact needs two independent assessments;
condition, sibling output and other review results remain hidden from each assessor.
Disagreements and measurement defects require evidence-based adjudication.

Run `python3 evals/human-writing-genre/validate_corpus.py` for corpus structure and
hash integrity. Run `python3 evals/human-writing-genre/mechanical_checks.py output-map.json`
for literal constraints; the output map is a JSON object from case id to actual
artifact text. These checks neither establish semantic truth nor writing quality.
A schema pass, model judge, aggregate score or fluent text cannot clear a factual,
modality, scope, attribution or fabrication failure.

Freeze the skill bytes, case/oracle hashes, model/configuration, permissions, batching,
raw execution traces and outputs before comparison. Report independent inputs,
case executions, batches and assessor runs separately. Preserve failed artifacts.
Do not tune against held-out outputs or silently change frozen scoring after a run.
The maintained owner updates inputs, oracles, schemas and manifest together after a
reviewed corpus change; retire this version only after named consumers migrate.
Consumers are validate_corpus.py and mechanical_checks.py; the producer is the
repository's human-writing evaluation maintainer. Ordinary skill runtime never loads
this corpus. The skill remains self-contained without these maintenance assets.

## Scoring and limits

Mandatory hard assertions precede genre scores. On fail/indeterminate hard gate,
genre scores are empty. On pass, applicable dimensions receive 0–2; predeclared
inapplicable dimensions receive null with their reason. Exact no-op cases are
conservation tests, not opportunities to invent stylistic changes. Missing-operation
cases may correctly stop instead of fabricating a complete tutorial.

The independent design audit corrected necessary/sufficient-condition confusion,
option/exclusivity confusion and an unrequested identifier requirement before writer
runs. The corpus has 558 semantic/scope assertions, 104 literal string-count checks,
9 immutable-span checks and 8 exact no-op checks. A code-format delimiter issue in
three tutorial checks remains documented as a measurement dispute in the run report;
raw frozen failures are retained, not silently converted into evidence of corruption.

The method borrows edit-scope separation from ERRANT, multidimensional review from
SummEval and atomic supported-claim assessment from FActScore; fixed revisions, licenses
and boundaries are in methodology.md. Those tools or datasets are not redistributed
or presented as a universal writing benchmark. No detector, word frequency or
sentence-length score is an optimization target. Medium/long holdouts are Chinese;
English holdouts are mainly proofreading. Synthetic samples, shared batch context,
same-model generation/assessment and editorial judgments limit inference. Results do
not establish host auto-selection, cross-model generality, publication readiness or
efficiency improvements. No human acceptance is implied by agent review.

## Separate fresh held-out extension

`fresh-holdout/` adds 16 inputs frozen before original/v8 generation, two per
existing genre, with independently reviewed coverage versus optional-detail rules.
The original96 hashes and rubric are unchanged. Combined112 independent inputs
provide14 per genre; repeated versions still count once. Run outcomes, missing
assessments and execution failures belong in the task report, not this corpus
structure validator. This extension is not silently folded into the original
558/121 assertion totals. See its README for its distinct oracle format.
