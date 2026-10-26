# human-writing expanded evaluation methodology

Frozen corpus: 2026-10-23. This is a source-bounded writing evaluation, not a test of external world knowledge. All 96 sources were independently composed synthetic records. No private or benchmark source prose was copied. The designer read only the target SKILL.md contract and did not inspect its existing 14 development / 4 holdout outputs, candidate patches, or eval-cases reference. No writer or judge model was run in this design task.

## Three fixed open-source methods consulted

### 1. ERRANT: edit-level grammatical error analysis

Fixed implementation: [ERRANT v3.0.2, commit 2840b84cf15c6a1d3f04e9d316aea1aa716e6000](https://github.com/chrisjbryant/errant/tree/2840b84cf15c6a1d3f04e9d316aea1aa716e6000). [2017 method paper](https://aclanthology.org/P17-1074/). Code license: [MIT at that revision](https://github.com/chrisjbryant/errant/blob/2840b84cf15c6a1d3f04e9d316aea1aa716e6000/LICENSE.md), verified from the pinned file.

Actual method: extract and classify edits between original and corrected English text, with reference-based edit evaluation. We borrow the separation of error correction from unrestricted rewriting: proofreading cases permit only demonstrable errors; local-edit cases preserve surrounding spans. We do not run ERRANT or use an M2/F-score target. Multiple valid corrections exist, Chinese morphology differs, quoted misspellings may be intentional, and agreement with a single edited reference cannot establish truth or voice. The corpus therefore has no expected finished draft. Exact immutable-span tests supplement semantic review rather than replace it.

### 2. SummEval: independent multidimensional human evaluation

Fixed implementation: [SummEval commit 81b59ad53d63cb6009764240853c91235a44e238](https://github.com/Yale-LILY/SummEval/tree/81b59ad53d63cb6009764240853c91235a44e238), resolved from the repository's master commit on 2026-10-23. [TACL 2021 method paper](https://aclanthology.org/2021.tacl-1.24/). Code license: [MIT at that revision](https://github.com/Yale-LILY/SummEval/blob/81b59ad53d63cb6009764240853c91235a44e238/LICENSE), verified from the pinned file.

Actual method: obtain separate human judgments for consistency, coherence, fluency and relevance, and compare automatic metrics with human judgments on news summaries. We borrow dimension separation and independent judgments, not the news task, original rating scale, metric bundle, or published correlations. Here factual/scope integrity is a prior hard gate; genre-specific structure, voice and useful detail use anchored 0–2 judgments. Social alternatives add substantive diversity. News-summary judgments do not validate personal nonfiction, email relationships, or Chinese writing. Dataset contents and external metric/model dependencies have their own rights and conditions; the repository license is not a blanket license for original news articles. None of those data or models is redistributed here.

### 3. FActScore: atomic supported-claim assessment

Fixed implementation: [FActScore v0.2.0, commit 03ff67253028337a7d26a33515aa647d98c7898b](https://github.com/shmsw25/FActScore/tree/03ff67253028337a7d26a33515aa647d98c7898b). [EMNLP 2023 method paper](https://aclanthology.org/2023.emnlp-main.741/). Code license: [MIT at that revision](https://github.com/shmsw25/FActScore/blob/03ff67253028337a7d26a33515aa647d98c7898b/LICENSE), verified from the pinned file.

Actual method: split generated text into atomic factual claims and assess support against a knowledge source; the implementation offers retrieval/model-assisted estimates. We borrow atomic source support checks and require evidence spans. We do not retrieve Wikipedia, import biography scores, use the original factual-precision percentage as an acceptance threshold, or assume the paper's automatic-judge accuracy transfers. Precision alone can reward omitting all useful content; this evaluation also checks retention of required source constraints, edit scope, uncertainty and genre quality. Code licensing does not determine licenses or access terms for optional external models, corpora or APIs. Our authoritative source is each supplied synthetic source_text, so a plausible outside fact cannot override a toy contract.

## Hard gate and genre review

1. Writer receives only the case prompt and source_text, plus the skill/runtime condition selected by the evaluator. Metadata such as id may be retained by the runner but must not expose review criteria. Neither oracles.json nor this document, the generator, review files, coverage tags, or expected responses belongs in a writer message. There are no expected response drafts in the corpus.
2. Freeze model identifier, system/skill snapshot, decoding settings, tool availability and source hash before running each condition. Use the identical input bytes across conditions. Tool-free writing is sufficient for these closed-source cases. Do not silently use a different source to fix an apparent product or command oddity.
3. Perform mechanical checks only where the oracle supplies concrete check_mode/data. Exact string counts, equality to input, and immutable prefixes/suffixes establish literal preservation only. They cannot establish whether a person has approval, a negation changed scope, or a numerical denominator is correct. All semantic assertions require review.
4. Two reviewers independently see a random artifact identifier, prompt, source, complete output and keyed oracle. Hide condition, skill version, writer identity, sibling outputs and the other review. Reviewers must not infer truth from a regex or a plausible outside convention. Each mandatory semantic assertion receives pass/fail/indeterminate with source/output evidence. Also inspect added claims not enumerated in the fact list.
5. All mandatory assertions must pass for hard_gate=pass. A definite violation gives fail. Unresolved ambiguity gives indeterminate, not pass. A response that safely identifies a missing essential operation may pass only where the case allows that stop state. A capable source-bounded artifact should not be replaced by needless questions merely because an optional fact is absent.
6. Only after hard pass, assign each genre dimension 0, 1 or 2 with a cited span and short reason. If a dimension is genuinely inapplicable to the requested narrow operation, use null with a reason, not an invented low or high score. Exact no-change cases predeclare all genre dimensions inapplicable/null. Other proofreading tasks are judged only on the requested correction, not an unrequested rewrite.
7. Social cases permitting selection do not require every optional source detail in every candidate. Each candidate must remain supported, preserve the core event and satisfy all explicit constraints. Diversity means materially different angle and organisation, assessed semantically; adjective swaps or different punctuation do not suffice. Single-post cases must not be expanded into extra alternatives.
8. Persist both independent reviews before adjudication. A third reviewer resolves disagreements against source evidence; preserve original votes. No majority inference may convert an unsupported claim into fact. Record reviewer identity and conflicts; the writer may not be its own sole reviewer. Human adjudication remains appropriate where automated reviewers disagree or miss context.
9. Report hard pass/fail/indeterminate counts by type, split, language, operation and input-length profile. Report distributions of each 0–2 dimension among hard-passed cases and how many were inapplicable. Preserve failures alongside style results. Do not create a single averaged leaderboard that hides a factual failure behind fluent prose. With 2 holdouts per type, avoid population-level precision claims.

## Splits and contamination controls

Each type has 10 development and 2 holdout cases. Holdout sources are different events/subjects, never renamed variants of a development source. Do not tune wording or skills against holdout outputs or modify holdout oracles after inspecting them. The corpus designer supplied holdout oracles for reviewers, not for the writer. If developers inspect them for operational reasons, disclose that exposure and stop describing that cohort as a pristine blind holdout. The design freezes before output generation and includes SHA-256 hashes.

All 96 sources are distinct under literal and alphanumeric-normalized equality. The nearest character-alignment pairs were screened manually for different events and reader tasks. Lexical similarity is only a duplicate-input screen; it is not a quality measure, a detector or proof of semantic independence.

## Coverage and limits

Every type contains rewriting/drafting, a local edit, proofreading, a correct no-change source, missing/uncertain facts, modal or negative scope, and protected literal material. Each contains two substantial multi-paragraph sources. Technical explanation, tutorial, research and personal nonfiction include 500+ Han-character Chinese sources and 250–500-word English sources. Social sources are shorter, matching the genre and supporting distinct candidate selection.

This is a deliberately bounded synthetic suite. It does not estimate real-world prevalence, cover every dialect or platform, test translation-only work/fiction, evaluate external publication tools, validate actual API semantics, or measure medical/legal expertise. Only Chinese and English are represented. Revision 2 includes one medium/long Chinese holdout per type; English holdouts remain predominantly proofreading. This is not a complete language × operation × length factorial design. There are no multi-turn source corrections, conflicting authoritative documents, Word/PDF layout deliverables, or unbounded research tasks. Those are declared gaps, not hidden successes.

No AI-detection scores, forbidden-word lists, target word frequencies, target sentence lengths, or aesthetic regexes are used. Source length profiles in the published input JSON files describe corpus coverage only. No model evaluation outcome is claimed by this design.

## Documentation alignment

This public copy aligns two r1 descriptions with the actual r2 corpus and applicability rules before publication. The original runtime freeze remains retained with its original hashes. No input, oracle, assertion, output or score was changed by this documentation alignment.

## Separate extension accounting

The fresh16 extension uses its own frozen required/conditional oracle format.
Its exact-body conservation anchors describe compliance; report those separately
from genre-quality comparisons. Original96 exact-no-op genre dimensions remain
inapplicable/null. This clarification does not alter either frozen oracle or any
raw score. See fresh-holdout/README.md; do not pool unlike denominators.
