# Scheduled Topic Digest

Use this prompt for a recurring, source-backed information digest. Edit the configuration below when the topic changes; keep the research and verification rules stable.

## Configuration

- Focus topics: `[list the subjects, products, repositories, companies, or questions to track]`
- Intended use: `[news monitoring / engineering decisions / reusable asset discovery / other]`
- Schedule: `[default: daily at 09:00]`
- Timezone: `[default: Asia/Shanghai]`
- Lookback window: `[default: 72 hours]`
- Maximum items: `[default: 8]`
- Existing local inventory, if relevant: `[index, repository, or local path]`
- Output language: `[default: user's language]`

## Task

Search current primary sources for meaningful developments within the configured topics. Select only items that can affect the intended use.

If web access is unavailable, stop and state that current information cannot be verified. If the configured topic has no meaningful update, return a short `No significant update` result instead of filling the digest with weak material.

## Research Rules

1. Prefer official documentation, changelogs, papers, technical reports, original repositories, and maintainers' engineering posts.
2. Use reputable secondary reporting only when no primary source exists or independent context is necessary.
3. Open and verify every selected source; never rely on search-result snippets.
4. Record the event or release date when available, not only the publication date.
5. Deduplicate by event, release, repository, and canonical URL; retain the strongest original source.
6. Exclude marketing-only announcements, reposts, rumors without clear labeling, generic summaries, and items without a practical implication.
7. Clearly distinguish confirmed releases, research results, previews, inference, and speculation.
8. When an existing local inventory is provided, inspect it and identify overlap before recommending a new asset or workflow.

## Evaluation

For each candidate, determine:

- what changed and its current status
- why it matters to the configured topic and intended use
- evidence, limitations, dependencies, and maintenance cost when relevant
- whether it suggests an action, experiment, reusable asset, reference update, or no action

Popularity and novelty alone are not evidence of value.

## Output

Start with the covered date range, configured topics, sources inspected, and any limitations.

For each selected item, provide:

- title, type, status, and event date
- primary source name and direct URL
- concise factual summary
- practical relevance
- recommended next action, or `No action`

Finish with:

1. `关键结论`: up to three cross-item conclusions
2. `值得验证`: concrete claims, tools, or decisions worth testing
3. `可沉淀资产`: candidates for a prompt, skill, workflow, reference, or `No action`

Do not invent citations, dates, benchmarks, availability, local overlap, or verification results. Do not copy large source materials verbatim; summarize the durable information and link to the original source.
