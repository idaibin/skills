# Quality Rubric

Evaluate the finished text, not the intention. Defect severity and hard gates decide readiness; numeric scores are optional calibration, not proof.

## Acceptance Layers

Do not collapse these states:

1. **PACKAGE CONTRACT VALID:** package structure, routing, precedence, references, and documented cases validate. This says nothing about output quality.
2. **DETERMINISTIC FIXTURES PASS:** machine-checkable fixtures and semantic mutations pass. This finite sample does not prove complete contract conformance or production-model behavior.
3. **REAL MODEL BEHAVIOR PASSED:** frozen inputs run against the production model at least three times per P0/P1-sensitive case, with recorded model settings, semantic source-ledger grading, and zero P0/P1 defects.
4. **EDITORIALLY APPROVED:** blind source-relative reviewers find no credible P0/P1 issue and prefer the candidate over unnecessary rewriting or the minimally edited baseline.

Report `HUMAN WRITING ACCEPTED` only when all four layers pass. A fluent draft cannot score its way past an integrity failure, and static validation cannot prove that no behavior defect exists.

## Defect Levels

- **P0 — misleading or unsafe:** invented or materially wrong fact, changed technical meaning, concealed material relationship, false attribution, or unsafe command. Blocks output.
- **P1 — publication blocker:** unresolved source conflict, missing required disclosure or material correction note, lost author position, background research replacing the requested author narrative, a candidate presented as committed or completed, a visible metadata/body or architecture/code contradiction, unusable tutorial step, or structure that changes the argument. Blocks publication.
- **P2 — substantive edit:** generic structure, repeated reasoning, weak evidence placement, append-only revision seams, over-editing, platform mismatch, or noticeably flattened voice. Fix unless the user accepts it.
- **P3 — preference edit:** local wording, rhythm, naming, or formatting improvement with no effect on meaning or trust.

## Dimensions

| Dimension | Weight | 10-point standard |
| --- | ---: | --- |
| Factual and technical integrity | 20% | Every claim follows source precedence and is supported, qualified, or clearly opinion; provenance, status, source interest, independence, exact subject, operation, metric, baseline, scope, material relationships, required creation-process details, and applicable revision history are accurate; protected text is exact |
| Intent and reader fit | 10% | The text solves the requested reader task without irrelevant coverage or unrequested research-process narration |
| Author voice fidelity | 10% | The voice matches supplied samples or the calibrated default without imitation theater |
| Specificity and evidence | 10% | Claims are grounded in concrete mechanisms, examples, constraints, observations, or traceable sources; numbers remain attached to the operation, comparison, source, and evidence status they actually represent |
| Logic and structure | 10% | The reader's starting model, supported premises, derivation, constraints, examples, boundaries, and conclusion form a visible path where material; partial models and proxies keep their limits; follow-up additions are integrated without stale transitions, repetition, missing steps, or artificial templates |
| Information density | 10% | Nearly every paragraph adds information; repetition, editorial framing, and background-source leakage are minimal |
| Natural rhythm | 10% | Sentence and paragraph length vary with meaning; emphasis is not manufactured |
| Platform fit | 5% | Opening, length, formatting, density, sourcing, terminology, attribution, material-interest disclosure, required creation-process disclosure, and any required correction notice fit the target platform without changing claim meaning |
| Persuasion and trust | 5% | The text earns belief through honest proof, limitations, source transparency, material-interest disclosure, truthful process disclosure, and transparent correction history rather than pressure |
| Language and editing | 10% | Grammar, punctuation, terminology, headings, and formatting are clean, precise, and consistent |

## Score Anchors

### 10.0

Publishable without material edits. Distinct voice, exact facts, traceable evidence, correct source precedence and attribution, precise terminology, complete applicable disclosures, transparent material revisions, strong structure, natural rhythm, and no visible template residue.

### 9.5

Publishable. A demanding editor may make a preference-level change, but no factual, source-conflict, attribution, disclosure, correction-history, terminology, structural, voice, or reader problem remains.

### 9.0

Strong but still has one noticeable weakness: a generic sentence, compressed explanation, slightly broad technical label, slightly weak source attribution, slightly incomplete applicable disclosure, slightly incomplete correction note, slightly uniform rhythm, or minor platform mismatch.

### 8.0

Competent but generic. The text communicates correctly but reads like a polished template, weakens a precise claim through compression, blurs first-party and independent evidence, silently blends conflicting source versions, misses a required process disclosure, silently replaces a material published error, or misses an important tradeoff.

### 7.0

Usable only after editing. Repetition, weak structure, vague claims, incomplete sourcing, imprecise terminology, unresolved source conflict, missing attribution, disclosure, or correction history, or voice drift is obvious.

### Below 7.0

Unreliable, unsupported, misleading, hard to follow, or materially misaligned with the task.

## Assessment Procedure

1. Read once as the target reader.
2. Check source precedence, unresolved conflicts, the whole publishable surface, internal consistency, the source ledger, claim trace, source interest, evidence independence, semantic fidelity, material relationships, current platform rules, required creation-process disclosures, published revision history, and protected text.
3. List concrete defects with severity and evidence.
4. Resolve P0 and P1 items before optimizing lower-severity prose.
5. If a numeric score is requested, score each dimension independently with one evidence sentence and state that it is editorial calibration, not behavioral validation.
6. Reassess the finished draft, not the change history, and stop only when the hard gate passes.

Do not expose internal assessment unless the user asks. Never inflate a score to manufacture readiness.

## Final Gate

- Confirm source precedence, claim scope, attribution, disclosures, protected text, and revision history.
- Confirm title, description, body, code, tables, links, numbering, and workflow summaries do not contradict or silently omit one another.
- Confirm past, current, committed, candidate, and unresolved material retain their actual status.
- Confirm background-only evidence shaped the result without becoming visible editorial scaffolding.
- Confirm follow-up additions were integrated into the argument and did not leave stale framing, repetition, contradiction, or an outdated ending.
- Confirm the opening answers the reader's task and each section adds information.
- For explanatory work, confirm the draft repairs or extends a plausible reader model; separates premise, derivation, and judgment; and ends with the model, criterion, tradeoff, question, or next test it actually earned.
- For long-form or multi-claim work, confirm the private outline became prose and no planning scaffold leaked into the artifact; for short or local edits, confirm no unnecessary planning ceremony expanded the task.
- Diagnose template behavior only as a cluster; preserve genuine voice and asymmetry.
- Confirm parallel structure and repeated technical terms were changed only when a concrete information or reader problem existed.
- Confirm specificity came from evidence rather than plausible gap-filling, and no style heuristic became a global punctuation, vocabulary, or syntax ban.
- Confirm platform hard constraints separately from editorial preferences.
- Resolve every P0/P1 defect. Compare against the unchanged source and stop when the candidate has no concrete benefit or weakens terminology, modality, workflow closure, or source-shaped voice.
