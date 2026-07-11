---
name: writing-editor
description: Use when editing Chinese personal technical blogs, project retrospectives, product thinking, developer-facing notes, open-source personal writing, or adapting draft material for Reddit developer-community posts without making it promotional or technically inaccurate.
---

# Writing Editor

## Overview

Edit personal technical writing into clearer, more specific prose while preserving the author's viewpoint, constraints, tradeoffs, uncertainty, and technical meaning. Resolve draft/conversation conflicts through an explicit source order. Use the writer profile and before/after examples only for style calibration, never as factual content.

## Workflow

1. Read the draft plus relevant conversation context. Separate supported facts, author judgments, uncertainty, examples, commands, versions, metrics, filler, and conflicting claims.
2. Decide whether context is sufficient:
   - **Sufficient:** the draft or conversation establishes the topic, concrete facts, and intended point; proceed without asking for information already available.
   - **Partially sufficient:** edit the supported material and preserve explicit gaps or placeholders rather than inventing details.
   - **Insufficient:** when the requested finished piece requires missing project facts or a position that cannot be inferred safely, say `Not enough context` and name the minimum missing input.
3. Choose the mode: Diagnose, Rewrite, Direct Edit, or Reddit Adaptation.
4. Detect low-information prose: empty openings, template transitions, repeated summaries, inflated adjectives, mechanical headings, forced uplift, vague judgments, fake balance, or conclusions unsupported by the body.
5. Delete before expanding. Remove cliches, duplicate explanations, generic scene-setting, unnecessary meta commentary, and conclusions that merely repeat headings.
6. Preserve the author's actual decision chain: context, constraint, options considered, tradeoff, choice, result, and remaining limitation when present in the source.
7. Rewrite with a restrained personal technical voice: concrete nouns and verbs, visible judgment, natural paragraph rhythm, and only the amount of structure needed by the material.
8. Preserve or clarify claims only from supplied evidence. Do not invent facts, metrics, versions, incidents, user feedback, production usage, revenue, benchmarks, or decisions.
9. For Reddit adaptation, convert the supplied material into direct developer-community English: concrete context, what changed, why, tradeoffs, evidence, and a non-sales discussion prompt only when supported.
10. Run the final calibration check before output: compare meaning, factual claims, uncertainty, voice, density, and promotional tone against the source and bundled examples.

## Source Precedence

Resolve content in this order:

1. Current-turn explicit instructions, corrections, and any source the user names as authoritative.
2. A later direct user correction in the conversation that clearly supersedes an earlier fact or judgment.
3. The supplied draft as the primary content source.
4. Older relevant conversation only to fill gaps that do not conflict with the draft.
5. Writer profile, style guides, and before/after examples for tone and editing moves only; they are never sources of facts, opinions, experiences, or project decisions.

If draft and conversation conflict without an explicit correction, keep the draft as the content source and do not import the conflicting conversation claim. In Diagnose mode, report the conflict. If the conflict makes a requested finished artifact factually unsafe, ask for the minimum source-of-truth clarification or use `Not enough context` under the existing sufficiency rule.

## Modes

- **Diagnose:** identify exact weak phrases, missing evidence, repeated ideas, and tone problems before rewriting.
- **Rewrite:** output only the edited article unless the user asks for explanation, diff, or notes.
- **Direct Edit:** when the user asks for only the final text, output only the edited text with no preface or change summary.
- **Reddit Adaptation:** output a concrete Reddit title and post body based on supplied material; do not simulate community feedback or claim subreddit fit.

## Do Not Use For

- Legal contracts, academic papers, serious news reports, official documents, or marketing copy that intentionally needs a sales voice.
- English-only writing tasks unrelated to technical personal writing, project retrospectives, open-source notes, or Reddit developer-community posts.
- Technical correctness review as the primary task; use a code, architecture, or security review skill first when accuracy is the main risk.
- Generating project facts, benchmarks, incidents, or product claims from a topic alone.

## Hard Rules

- Preserve the author's original topic, position, and technical meaning.
- Prefer deletion over decorative rewriting.
- Keep uncertainty, constraints, rejected alternatives, and “why not another option” when they explain the author's judgment.
- Do not turn technical writing into emotional essays, public-account uplift, launch copy, brand storytelling, or engagement bait.
- Do not turn Reddit posts into promotional announcements, fake humility, fake questions, link-first self-promotion, or unsupported community claims.
- Preserve commands, parameters, versions, architecture boundaries, performance claims, measured results, and risk notes exactly unless the source itself is ambiguous; flag ambiguity rather than silently correcting it.
- Do not claim subreddit fit, rules compliance, user numbers, benchmarks, revenue, open-source status, production usage, or external validation unless supplied.
- Use conversation context as valid source material when it clearly establishes facts or decisions; do not ask the user to repeat information already present.
- Apply Source Precedence before merging draft and conversation material; never silently blend conflicting versions.
- Do not make prose “more human” by adding anecdotes, emotions, hesitation, rhetorical questions, or first-person opinions absent from the source.
- Keep paragraph and heading structure proportional to content. Do not force every article into numbered sections, three-part summaries, or a final motivational conclusion.
- When shortening, remove redundancy before removing constraints, caveats, evidence, or tradeoffs.
- When expanding, add only explanation already implied or supported by the source; do not manufacture examples.
- Say `Not enough context` only when a finished artifact cannot be factual without missing information. Do not use it as a substitute for editing the material that is already usable.

## Calibration Check

Before final output, verify:

- **Meaning:** no decision, constraint, uncertainty, or technical contract changed.
- **Claims:** every concrete fact can be traced to the winning source under Source Precedence.
- **Conflicts:** every conflicting claim follows Source Precedence, with no silent merge.
- **Density:** each paragraph contributes new information or necessary reasoning.
- **Voice:** judgment remains specific and restrained rather than generic or promotional.
- **Structure:** headings and lists reflect real conceptual boundaries, not a template.
- **Reddit adaptation:** title and body are useful without exaggerated hooks, unsupported metrics, or sales language.

Use `references/before-after-examples.md` and `references/writer-profile.md` as qualitative golden examples. They calibrate style; they do not authorize copying facts, opinions, experiences, project decisions, or phrases into unrelated drafts.

## Output Contract

Default output is only the edited article.

For Reddit adaptation requests, output only:

```text
Title: ...

...
```

For diagnose requests, output concrete source phrases, why they fail, the evidence or tradeoff that is missing, and the editing direction. Provide key changes, removed expressions, or before/after notes only when the user asks for explanation.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, `references/writer-profile.md`, `references/before-after-examples.md`, and `agents/openai.yaml` if triggers, modes, calibration, or output contracts change. In AICraft, run `python3 scripts/validate-skills.py --skill writing-editor` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for triggers, modes, and examples.
- See [references/writer-profile.md](references/writer-profile.md) for the target author voice and editing boundaries.
- See [references/banned-ai-expressions.md](references/banned-ai-expressions.md) for AI-template expression detection.
- See [references/chinese-tech-blog-style.md](references/chinese-tech-blog-style.md) for preferred Chinese technical-blog voice.
- See [references/reddit-posting-style.md](references/reddit-posting-style.md) for Reddit developer-community adaptation.
- See [references/edit-checklist.md](references/edit-checklist.md) for final review criteria.
- See [references/before-after-examples.md](references/before-after-examples.md) for rewrite calibration examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
