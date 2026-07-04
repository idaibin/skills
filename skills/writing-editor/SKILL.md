---
name: writing-editor
description: Use when editing Chinese personal technical blogs, project retrospectives, product thinking, developer-facing notes, open-source personal writing, or adapting draft material for Reddit developer-community posts without making it promotional or technically inaccurate.
---

# Writing Editor

## Overview

Edit personal technical writing into clearer, more specific prose that keeps the author's view, tradeoffs, project context, and technical accuracy. It can also adapt a supplied draft or notes into a Reddit-ready developer-community post.

## Workflow

1. Read the draft and identify the core point, facts, opinions, and filler.
2. Choose the mode: Diagnose, Rewrite, Direct Edit, or Reddit Adaptation.
3. Detect AI-template prose: empty openings, template transitions, repeated summaries, inflated adjectives, mechanical structures, forced uplift, vague viewpoints, or missing tradeoffs.
4. Delete before expanding: remove cliches, duplicate explanations, generic summaries, empty adjectives, and transitions that add no information.
5. Rewrite with a restrained personal technical-blog voice: clear judgment, concrete constraints, visible tradeoffs, and natural paragraph rhythm.
6. Preserve or clarify judgment only from supplied context; do not invent facts, metrics, versions, incidents, or decisions.
7. For Reddit requests, use a direct community-post shape: concrete title, short context, what was built or learned, tradeoffs, and a non-sales ask only if supported by the draft.
8. Check the result against the editing checklist before final output.

## Modes

- **Diagnose:** mark AI-template phrasing, weak claims, filler, and missing tradeoffs before rewriting.
- **Rewrite:** output only the edited article unless the user asks for explanation, diff, or notes.
- **Direct Edit:** when the user asks to "直接改", "只给正文", or equivalent, output only the edited text.
- **Reddit Adaptation:** when the user asks to post on Reddit or a developer community, output a Reddit title and post body only unless the user asks for notes.

## Do Not Use For

- Legal contracts, academic papers, serious news reports, official documents, or marketing copy that intentionally needs a sales voice.
- English-only writing tasks unrelated to technical personal writing, project retrospectives, open-source notes, or Reddit developer-community posts.
- Technical correctness review as the primary task; use a code, architecture, or security review skill first when accuracy is the main risk.

## Hard Rules

- Preserve the author's original topic, position, and technical meaning.
- Prefer deletion over decorative rewriting.
- Keep uncertainty, constraints, and "why not another option" when they explain the author's judgment.
- Do not turn technical writing into emotional essays, public-account uplift, or brand marketing.
- Do not turn Reddit posts into launch copy, growth copy, engagement bait, fake humility, or link-first self-promotion.
- Preserve commands, parameters, versions, architecture boundaries, performance claims, and risk notes.
- Do not claim subreddit fit, rules compliance, user numbers, benchmarks, revenue, open-source status, or production usage unless supplied.
- Say `Not enough context` instead of inventing unsupported project facts.

## Output Contract

Default output is only the edited article.

For Reddit adaptation requests, output only:

```text
Title: ...

...
```

For diagnose requests, output concrete weak phrases, why they fail, and what editing direction to use.

Provide key changes, removed expressions, or before/after notes only when the user asks for explanation.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, `references/writer-profile.md`, and `agents/openai.yaml` if triggers, modes, or output contracts change. In AICraft, run `python3 scripts/validate-skills.py --skill writing-editor` before publishing; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.

## References

- See [references/usage.md](references/usage.md) for triggers, modes, and examples.
- See [references/writer-profile.md](references/writer-profile.md) for the target author voice and editing boundaries.
- See [references/banned-ai-expressions.md](references/banned-ai-expressions.md) for AI-template expression detection.
- See [references/chinese-tech-blog-style.md](references/chinese-tech-blog-style.md) for preferred Chinese technical-blog voice.
- See [references/reddit-posting-style.md](references/reddit-posting-style.md) for Reddit developer-community adaptation.
- See [references/edit-checklist.md](references/edit-checklist.md) for final review criteria.
- See [references/before-after-examples.md](references/before-after-examples.md) for rewrite calibration examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
