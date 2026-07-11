# Content Modes

Select one primary mode. Combine modes only when the user asks for a platform adaptation or mixed artifact.

All modes inherit `fact-integrity.md`. The rules below describe only mode-specific structure and emphasis; they do not redefine source precedence, attribution, semantic fidelity, relationship disclosure, or external-claim handling.

## Short-Form

Use for a social post, caption, announcement, concise opinion, or product note.

### Shape

- one central claim
- one concrete detail, scene, contrast, or mechanism
- one ending that completes the thought
- optional link or tag only when useful

### Editing rules

- Start with the point, not a title-like preamble.
- Do not squeeze a full article into bullets.
- Avoid stacked slogans, hashtag piles, and three consecutive punchlines.
- Keep one human turn: a decision, hesitation, contrast, or specific observation.
- Remove any sentence that only repeats the claim.
- If the post recommends the author's own product or an interested party's product, state that relationship directly.
- Compression must preserve the exact technical subject, operation, metric, baseline, qualifier, and source attribution. Omit a secondary claim rather than merge different scopes into one inaccurate sentence.
- When the only evidence is a vendor, employer, sponsor, or product owner's report, keep `官方称`, `厂商测试`, or equivalent attribution in the post itself rather than hiding it behind a link.

## Factual Soft Copy

Use when the text should persuade without becoming deceptive marketing.

### Shape

1. a real situation the reader recognizes
2. the cost or friction in that situation
3. the product, service, or idea as a response
4. a plain relationship disclosure when the author has a material interest
5. the concrete mechanism or evidence
6. the fit and limitation
7. an honest next step, only if requested

### Rules

- Lead with lived or observed friction, not a manufactured hook.
- Show how the thing works instead of calling it powerful.
- State who it is for and who may not need it.
- Use proof that exists: code, workflow, screenshots, documented behavior, verified results, or independently reproduced evidence.
- Distinguish `I tested this`, `the documentation says this`, `the vendor reports this`, and `an independent test found this`.
- Use official sources for specifications, release facts, documentation, and the vendor's stated methodology. Do not treat a first-party benchmark as independent proof of superiority.
- Make the source, source interest, date, version, or scope visible when the proof can change or the source benefits from the claim.
- For performance, price, reliability, or comparison claims, name the measured operation, baseline, sample, environment, source, and whether the result was independently reproduced.
- Disclose self-promotion, employment, sponsorship, affiliate benefit, free access, or supplied review units near the first product evaluation or recommendation.
- Give the reader useful knowledge beyond the product pitch.
- Keep the product name out of every paragraph.
- Never invent testimonials, urgency, or performance numbers.
- A call to action should be specific and low-pressure.

## Personal Technical Essay

Use for project decisions, architecture thinking, product boundaries, and learning notes.

### Shape

- the problem as experienced
- the first assumption
- what changed the author's view
- the chosen boundary or implementation
- the cost of that choice
- what remains unresolved

The article can move chronologically or by decision. It should not read like a status report.

## Tutorial

Use when the reader should reproduce a result.

### Shape

1. outcome and scope
2. prerequisites and tested environment
3. minimal working steps
4. explanation close to the step it supports
5. verification commands and expected evidence
6. common failure modes
7. limitations or version boundaries

### Rules

- Keep code and prose synchronized.
- Do not hide prerequisites.
- Do not claim a command was verified unless it was.
- Label behavior that comes only from documentation, a vendor report, or another source.
- Name the exact component and operation being configured, built, measured, or verified; do not replace them with broader labels for readability.
- For volatile products or interfaces, include the tested date, version, region, plan, or environment that matters.
- Prefer a complete small path over an exhaustive catalog.
- Put warnings before the risky step, not after it.

## Engineering Retrospective

Use when the value lies in the decision process.

### Shape

- original goal
- actual constraint
- attempts and evidence
- decision
- tradeoff
- follow-up consequence

Avoid the project-report sequence `background / achievements / lessons / outlook` unless that is the requested format.

## Architecture Note

Use when explaining a system boundary.

### Shape

- the specific problem
- current context and constraints
- chosen boundary
- data/control flow
- rejected alternatives
- failure modes
- verification and maintenance implications

A diagram or table is useful only when it carries information that prose would obscure.

## Resource List

Use when the artifact is primarily a curated list.

- State the organizing principle and intended reader.
- Prefer a smaller annotated path over a long unranked inventory.
- Mark official, maintained, archived, outdated, interested, independent, or unverified status when it affects interpretation.
- Add a recommended order or decision rule.
- Do not pad every item with the same generic description.
