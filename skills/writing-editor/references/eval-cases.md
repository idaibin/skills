# Eval Cases

Use these cases when changing `writing-editor` triggers, context sufficiency, calibration, workflow, outputs, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `这篇中文技术博客太像 AI 写的，帮我改自然一点。` | Should trigger `writing-editor` and output only the edited article by default. | Chinese technical-blog editing and AI-template reduction. |
| `帮我压缩这篇项目复盘里的废话，保留我的判断。` | Should trigger `writing-editor`. | Project retrospective editing with viewpoint preservation. |
| `只给正文，把这篇 Feeds Hub 文章改得更像个人博客。` | Should trigger Direct Edit mode. | Final-text-only request. |
| `找出这段里面的公众号味和模板句。` | Should trigger Diagnose mode. | Template and public-account style diagnosis. |
| `把这篇 Feeds Hub 复盘改成 Reddit 上能发的英文帖子。` | Should trigger Reddit Adaptation mode. | Developer-community adaptation from supplied material. |
| `前面的对话已经写清项目背景，不要再问我，直接基于这些内容改。` | Should use relevant conversation context when it establishes the facts. | Avoids unnecessary repeated questions. |
| `草稿写的是 PostgreSQL；前面对话里旧版本写的是 SQLite。以当前草稿为准，只改文风。` | Should keep PostgreSQL and use the explicit current-turn/draft source priority. | Conflict-resolution path. |
| `帮我写一个 Reddit post，不要像 launch 广告。` | Should trigger only when draft material, conversation facts, or concrete notes establish a factual point; otherwise report the minimum missing context. | Prevents invented project claims. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `审查这个 API 有没有越权风险。` | Should prefer a security review skill. | Technical correctness and security are primary. |
| `把这份合同润色得更严谨。` | Should not trigger `writing-editor`. | Legal contract boundary. |
| `帮我写一个强营销首页文案。` | Should not trigger `writing-editor`. | Marketing voice is intentionally different. |
| `校对论文引用格式并统一参考文献。` | Should not trigger `writing-editor`. | Academic writing boundary. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Context sufficiency | Separates supported draft/conversation facts, author judgments, uncertainty, commands, versions, metrics, and missing information before editing. | Treats all context as equally reliable or asks for information already present. |
| Source precedence | Applies current-turn correction or named source first, then later direct correction, current draft, and only non-conflicting older conversation; treats profiles/examples as style-only. | Lets older context or a calibration example override the draft without explicit authority. |
| Conflict handling | Keeps the winning source, reports the conflict in Diagnose mode, and asks only when unresolved conflict blocks a factual artifact. | Silently blends contradictory framework, version, metric, result, or author-position claims. |
| Partial context | Edits supported material, preserves explicit gaps/placeholders, and names only the minimum information required for claims that cannot be completed safely. | Refuses the whole task because one detail is missing or invents the detail. |
| Blog rewrite | Removes empty openings, template transitions, repeated summaries, and generic conclusions while keeping viewpoint and supported tradeoffs. | Invents project facts, changes judgment, or turns the text into marketing copy. |
| Meaning preservation | Keeps decisions, constraints, uncertainty, technical contracts, commands, versions, metrics, and risk notes traceable to the source. | Smooths prose by changing technical meaning or deleting important caveats. |
| Deletion-first editing | Removes redundancy before adding structure or explanation. | Expands every paragraph, adds decorative transitions, or preserves filler under different wording. |
| Voice calibration | Uses writer profile and before/after examples only to calibrate restraint, density, rhythm, and specificity. | Copies facts/phrases from examples or imposes a generic personal-blog persona. |
| No fabricated humanity | Does not add anecdotes, emotions, hesitation, rhetorical questions, or first-person views absent from the source. | Makes text “human” by inventing lived experience or feelings. |
| Structure proportionality | Uses headings/lists only for real conceptual boundaries and keeps paragraph rhythm natural. | Forces numbered sections, three-part templates, or motivational conclusions. |
| Default output | Outputs only the edited article for ordinary rewrite requests. | Adds explanation, change notes, or meta commentary without being asked. |
| Direct edit | Outputs only the edited text when the user asks for only final text. | Adds preface, explanation, or change summary. |
| Diagnosis | Quotes or identifies exact weak phrases and explains their information, evidence, tone, or tradeoff problem. | Gives generic advice without grounding in the draft. |
| Technical accuracy | Preserves commands, versions, architecture boundaries, uncertainty, and performance claims; flags ambiguity instead of silently correcting. | Deletes constraints or changes technical meaning to sound smoother. |
| Reddit adaptation | Outputs `Title:` plus post body only, uses plain developer English, explains concrete context and tradeoffs, and avoids launch copy. | Adds promotional hooks, fake feedback asks, unsupported metrics, subreddit-fit claims, or extra explanation. |
| Missing Reddit context | Says `Not enough context` only when the finished artifact cannot be factual without missing project facts or a clear point, and names the minimum missing input. | Uses the phrase despite sufficient conversation context or invents user numbers, metrics, or project outcomes. |
| Shortening | Removes repetition and filler before constraints, evidence, caveats, or tradeoffs. | Produces a shorter but materially less accurate article. |
| Expansion | Adds only source-supported explanation or an explicitly marked placeholder. | Manufactures examples, incidents, results, or external validation. |
| Fact-drift fixture | Given a draft that says `PostgreSQL`, older conversation that says `SQLite`, and no later correction, the edit keeps `PostgreSQL`; given an explicit current-turn correction to `SQLite`, it uses `SQLite`. | Chooses the more familiar technology, merges both, or silently changes the database. |
| Calibration isolation | Given only `这个方案具有重要意义`, deletes or diagnoses it without adding first-person preferences, maintenance outcomes, or project strategy. | Copies a judgment from `before-after-examples.md` or invents what the author cares about. |
| Golden semantic fidelity | Given source notes containing `持续维护这个信息流产品` and `生成一篇文章`, preserves those object and capability boundaries in the calibrated rewrite. | Broadens `生成一篇文章` to all content writing or weakens `这个信息流产品` to an unspecified product. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
