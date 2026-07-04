# Eval Cases

Use these cases when changing `writing-editor` triggers, workflow, outputs, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `这篇中文技术博客太像 AI 写的，帮我改自然一点。` | Should trigger `writing-editor` and output only the edited article by default. | Chinese technical-blog editing and AI-template reduction. |
| `帮我压缩这篇项目复盘里的废话，保留我的判断。` | Should trigger `writing-editor`. | Project retrospective editing with viewpoint preservation. |
| `只给正文，把这篇 Feeds Hub 文章改得更像个人博客。` | Should trigger `writing-editor` in Direct Edit mode. | Direct-edit request for personal technical writing. |
| `找出这段里面的公众号味和模板句。` | Should trigger `writing-editor` in Diagnose mode. | AI-template and public-account style diagnosis. |
| `把这篇 Feeds Hub 复盘改成 Reddit 上能发的英文帖子。` | Should trigger `writing-editor` in Reddit Adaptation mode. | Reddit developer-community adaptation from supplied material. |
| `帮我写一个 Reddit post，不要像 launch 广告。` | Should trigger `writing-editor` only when draft material or concrete notes are supplied; otherwise ask for missing context. | Reddit adaptation must not invent facts. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `审查这个 API 有没有越权风险。` | Should not trigger `writing-editor`; prefer a security review skill. | Technical correctness and security are primary. |
| `把这份合同润色得更严谨。` | Should not trigger `writing-editor`. | Legal contract boundary. |
| `帮我写一个强营销首页文案。` | Should not trigger `writing-editor`. | Marketing voice is intentionally different. |
| `校对论文引用格式并统一参考文献。` | Should not trigger `writing-editor`. | Academic writing boundary. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Blog rewrite | Removes empty openings and generic summaries, keeps the author viewpoint, and clarifies only context-supported tradeoffs. | Invents project facts, overstates judgment beyond the evidence, or turns the text into marketing copy. |
| Default output | Outputs only the edited article for ordinary rewrite requests. | Adds explanation, change notes, removed-expression lists, or meta commentary without being asked. |
| Direct edit | Outputs only the edited article when the user asks for only final text. | Adds explanation, change notes, or meta commentary. |
| Diagnosis | Lists concrete weak phrases and explains why they are low-information or templated. | Gives generic advice without grounding in the draft. |
| Technical accuracy | Preserves commands, versions, architecture boundaries, and uncertainty. | Deletes constraints or changes technical meaning to sound smoother. |
| Reddit adaptation | Outputs `Title:` plus post body only, uses plain developer English, explains concrete build/workflow tradeoffs, and avoids launch copy. | Adds promotional slogans, fake feedback asks, unsupported metrics, subreddit-rule claims, or extra explanation. |
| Missing Reddit context | Says `Not enough context` when asked to write a Reddit post without draft material, project facts, or a clear point. | Invents project facts, user numbers, metrics, or a target community angle. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
