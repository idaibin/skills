# Fact Integrity

Good prose cannot repair unsupported content. Build a source ledger before drafting or rewriting.

## Source Ledger

Classify material into four buckets:

### Supplied facts

Directly stated or evidenced by the user, repository, logs, code, documents, or verified sources.

Examples:

- a command that was run
- a branch or commit
- a project architecture
- a measured result
- an observed failure
- a date in the source

### Author judgments

Opinions, preferences, interpretations, and decisions clearly attributable to the author.

Examples:

- `我更倾向 SQLite-first`
- `这个边界对个人项目更合适`
- `我不想把它做成通用后台模板`

### Unknown or unverified claims

Plausible statements that are not supported in the current context.

Examples:

- user numbers
- performance improvements
- market rankings
- platform algorithm behavior
- exact causes of an incident
- current product or policy status

### Protected text

Content that must not drift during editing:

- code
- commands
- config
- paths
- identifiers
- API names
- version numbers
- URLs
- quotations
- legal or security warnings

## Source Precedence

When the draft, conversation, notes, or calibration material disagree, resolve content in this order:

1. current-turn explicit instructions, corrections, and any source the user names as authoritative
2. a later direct user correction that clearly supersedes an earlier statement
3. the current supplied draft
4. older relevant conversation only when it does not conflict with the winning source
5. writer profiles, style guides, public samples, and before/after examples for style calibration only

Do not silently blend contradictory versions of a framework, database, command, version, metric, result, product status, or author position. In Diagnose mode, report the conflict. In finished-artifact modes, use the winning source; return `Not enough context` only when no source wins and the unresolved conflict makes the requested artifact factually unsafe.

## Claim Trace

For every externally checkable claim that materially supports the article, record enough provenance to audit it:

- **Claim:** the exact statement being made.
- **Origin:** supplied by the user, directly observed, measured, official documentation, primary source, or secondary source.
- **Status:** verified, documented but not personally tested, source-reported, inferred, or unverified.
- **Semantics:** exact subject or component, action or state, implementation language, measured operation, metric, and baseline.
- **Scope:** environment, version, date, sample, or conditions under which the claim holds.
- **Author relationship:** whether the author, employer, sponsor, affiliate, or product owner benefits from the claim.
- **Source interest:** whether the cited source owns, sells, funds, employs, promotes, or otherwise benefits from the subject or conclusion.
- **Independence:** first-party statement, independently reproduced result, independent analysis, or not established.
- **Creation process:** any AI assistance or other platform-regulated creation process that must be disclosed, including the actual tool, extent, verification, correction, and placement requirement.

Prefer evidence according to the claim type:

1. repository state, logs, measurements, or direct observation for what actually happened in the author's work
2. official documentation or another primary source for release facts, specifications, documented behavior, and the source's own methodology
3. independent reproduction or analysis for comparative superiority, performance, reliability, market impact, and user outcomes
4. a reliable secondary source that names its evidence
5. community reports only as discovery leads or clearly attributed experience

A first-party source is often authoritative about what it released, documented, measured, or announced. It is not automatically independent proof that its product is faster, better, safer, more reliable, or more widely adopted.

Do not collapse these statuses. `The documentation says`, `the vendor reports`, `I tested`, `an independent test found`, and `I infer` are different claims.

## Rewrite Rules

- Apply source precedence before merging draft, conversation, notes, or examples.
- Preserve supplied facts from the winning source.
- Keep author judgments attributed and proportionate.
- Omit unknown claims, label them `Not verified`, or research them before use.
- Preserve protected text exactly unless the user explicitly requests a verified correction.
- Do not turn a plan into a completed result.
- Do not turn correlation into causation.
- Do not turn a single experience into a universal rule.
- Do not change `may`, `can`, `usually`, or `in my case` into certainty for rhetorical force.
- Do not present documented capability as personally tested behavior.
- Keep source dates and scope when a claim can change over time.
- Preserve attribution when the source has a material interest. `The vendor reports`, `according to the company's benchmark`, and `independently verified` are not interchangeable.
- Do not use a first-party benchmark alone as independent proof of superiority. Keep its method, baseline, sample, and source relationship visible, and state when no independent reproduction was performed.
- Ensure attribution survives titles, summaries, short-form compression, and platform adaptation. Do not move a qualifier into the body while leaving a broader headline.
- Preserve platform-required AI-use or creation-process disclosures through rewriting, summarization, and platform adaptation. Do not reduce substantial assistance to `proofreading only` or invent a model, prompt, verification step, or correction history.
- Do not replace a precise technical component with a broader proxy. `Compiler and language service`, `runtime`, `build step`, and `product` are not interchangeable.
- Do not detach a number from what was measured, the comparison baseline, or the tested sample. `Build time improved on listed repositories` is not the same claim as `the language runs faster`.
- When shortening text, split or omit claims whose scopes differ rather than merging them into one smoother but inaccurate sentence.
- Preserve supplied technical semantics, commands, flags, order, prerequisites, and version scope. Do not silently repair disputed technical material from memory.
- Available deterministic syntax, link, command, or repository checks may be run when they are part of the editing task. Mark unrun checks `Not verified`.
- Apply this technical-publication decision table instead of treating every unverified item as a blocker:

| Evidence or risk state | Editorial action |
| --- | --- |
| Clear supplied technical text | Preserve exact semantics and scope |
| Deterministically checked | State only the check that actually ran and its scope |
| Unverified or vendor-reported | Preserve attribution and status; do not imply independent proof |
| Disputed | Preserve the conflict or the winning source under source precedence |
| Correctness is required to complete the artifact | Block the affected claim or route to technical review |
| Destructive or irreversible action | Do not present as routine publication-ready advice until reviewed |
| Actual secret, token, password, or private key | Redact and block transmission or publication |
| Obvious placeholder, environment-variable name, or dummy credential | Preserve when it is clearly non-secret |
| Correctness review is the primary task | Route to the relevant technical review workflow |

Ordinary unexecuted, non-destructive examples may remain when clearly labeled as unverified. A syntax-only check proves syntax only, not safety, runtime behavior, or compatibility.

## Drafting From Sparse Notes

Sparse notes do not authorize plausible details.

Allowed:

```text
我开始把重复出现的执行要求整理成 Skill。
```

Not allowed without evidence:

```text
经过三个月和数十次失败，我终于把重复要求沉淀成 Skill。
```

If the missing detail is essential, return:

```text
Not enough context:
- the actual problem or incident
- what was tried
- the observed result
```

## Soft-Copy Integrity

Do not fabricate:

- testimonials
- customer counts
- waiting lists
- awards
- scarcity
- before/after numbers
- competitor comparisons
- guarantees
- urgency
- personal origin stories

Persuasion should come from a real scene, concrete mechanism, verifiable proof, limitation, and clear fit.

For product claims, separate three evidence layers:

- **Product facts:** official specifications, release notes, documentation, and stated capabilities.
- **Author evidence:** what the author actually tested, observed, or measured.
- **Independent evidence:** third-party reproduction, comparison, or analysis with visible method and scope.

Do not let an interested first-party claim silently cross from the first layer into the second or third.

## Material Relationships

When the author has a material relationship to the subject, disclose it in plain language near the first evaluation, recommendation, or product introduction.

Material relationships include:

- building or owning the product
- employment by the organization being discussed
- sponsorship or payment
- affiliate or referral benefit
- free access, travel, equipment, or review units supplied for coverage
- access to non-public information provided by an interested party

The disclosure must survive platform adaptation. Do not hide it in metadata, a vague `合作`, or a distant footer when it changes how the reader should interpret the article.

## Platform-Required Process Disclosures

A creation-process disclosure is different from a material-interest disclosure. It explains how the artifact was produced when the target platform requires that information.

Before claiming an artifact is platform-ready:

1. verify the current official platform rule and its effective scope
2. record the actual tool or technology used
3. record whether assistance was local, repeated, or part of the main creation process
4. record what the author verified, corrected, or rewrote
5. place the disclosure where the current rule requires it

Do not infer a model name, prompt, usage extent, human-review step, or correction history. If a required detail is missing, return `Not enough context` rather than producing a false disclosure. A disclosure also does not transfer responsibility for originality, completeness, or accuracy away from the author.

## Current External Claims

When the text depends on current prices, versions, policies, platform rules, laws, schedules, product status, or interface behavior:

1. verify with current reliable sources
2. prefer official or primary sources for release facts and documented behavior
3. prefer independent evidence for comparative, evaluative, performance, reliability, market-impact, or user-outcome claims
4. use exact dates when time matters
5. distinguish direct observation, documented behavior, source-reported results, independent reproduction, and inference
6. keep the exact component, operation, metric, baseline, version, environment, and scope that the source supports
7. preserve source interest and attribution in the headline, summary, and body
8. verify current platform disclosure and labeling rules before claiming platform compliance
9. use a stable permalink and note paywalls or archived copies when appropriate
10. cite the claim in the target format when appropriate

If research was not performed, use `Not verified` or omit the claim.
