# Review Chat History

Use this prompt for an end-of-day work review based only on conversations that are actually available.

## Schedule

- Default time: `23:00`
- Default timezone: `Asia/Shanghai`
- Review date: the current local calendar day unless another date is supplied

## Task

Review the accessible conversations from the target date and produce a concise, evidence-based reflection. This is a decision and follow-up aid, not a chronological transcript summary.

## Evidence Rules

- First state which conversations or date range were accessible.
- Never imply that all chats were reviewed unless complete history was actually available.
- Do not infer unseen work, completed actions, repository state, or decisions.
- Separate explicit decisions from your interpretation of recurring themes.
- Treat repository paths, commits, validation results, and unresolved tasks as factual only when they appear in the accessible record.
- Consolidate repeated discussions into one item and preserve the latest decision.

## Output

Write in the user's language unless another language is explicitly requested. Keep the result concise and work-oriented.

Return:

1. `Coverage`: accessible scope and any missing history
2. `Core focus`: the main goals behind the day's work
3. `Progress and decisions`: concrete outputs, decisions, and verified results
4. `Friction`: repetition, drift, unclear requirements, failed approaches, or avoidable back-and-forth
5. `Open loops`: unfinished work, unresolved choices, and explicit blockers
6. `Tomorrow`: the top `1–3` specific, high-leverage next actions
7. `Long-term signal`: one short, clearly labeled inference about the capability or system being built

Avoid generic encouragement, invented productivity judgments, and long narrative retelling. If there is too little evidence for a section, write `No supported item`.
