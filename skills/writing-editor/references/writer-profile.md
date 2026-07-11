# Writer Profile

Use this profile to keep edits aligned with the author's usual voice.

This profile is a style constraint, not a content source. It cannot supply
project facts, first-person opinions, experiences, decisions, or results that
are absent from the draft and authoritative conversation context.

## Voice

- Chinese personal technical-blog style.
- Direct, restrained, and specific.
- Practical rather than literary.
- Opinionated only when the draft already supports the opinion.
- Clear about tradeoffs, constraints, and why a choice was made.
- For Reddit, plain developer-community English: concrete, transparent, low-hype, and written like a builder explaining what actually happened.

## Preferred Moves

- Keep the author's original position.
- Clarify unclear judgment instead of making it louder.
- Replace empty value claims with the concrete project constraint or decision.
- Preserve uncertainty when the author is not claiming certainty.
- Preserve "why not another option" when it explains the author's reasoning.
- Delete filler before rewriting.
- For AICraft, Feeds Hub, Rustzen, and small-tool posts, keep the product boundary, repository/workflow context, and why the small scope matters.
- For Reddit adaptation, turn the post around one concrete thing: what was built, what was learned, what tradeoff was accepted, or what feedback is genuinely needed.

## Avoid

- "AI humanizer" framing.
- Public-account uplift.
- Inspirational endings.
- Stronger claims than the source material supports.
- Fake personal experience.
- Marketing polish.
- Overly literary phrasing.
- Official-report structure when the draft is a personal note.
- Reddit launch tropes: "I built X, check it out", fake virality, fake humility, vague "would love feedback", and title-case slogans.

## Default Output

Return only the edited article unless the user asks for diagnosis, change notes, or before/after explanation. For Reddit adaptation, return `Title:` and the post body only.
