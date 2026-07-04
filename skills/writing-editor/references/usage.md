# Usage

Use `writing-editor` for personal technical writing where the goal is to keep the author's judgment while removing template prose. It also adapts supplied drafts or notes into Reddit-ready developer-community posts.

## Trigger Examples

- `用 writing-editor 帮我把这篇中文技术博客去 AI 化。`
- `这段太像 AI 写的，帮我压缩废话，保留我的判断，只给正文。`
- `把这篇项目复盘改得更像个人博客，不要公众号味。`
- `只改正文，别解释，把这篇 Feeds Hub 文章写得更真实。`
- `帮我找出里面的模板句、空话和不具体的判断。`
- `把这篇 Feeds Hub 复盘改成 Reddit 上能发的英文帖子。`
- `基于这段草稿/这些 notes 写一个 Reddit post，不要像 launch 广告，保留真实取舍。`
- `把这段中文草稿改成 r/selfhosted / r/webdev 风格的帖子。`

## Non-Trigger Examples

- `检查这段代码有没有权限漏洞。`
- `把这篇英文新闻稿改成正式公文。`
- `帮我写一个强营销落地页文案。`
- `校对论文引用格式。`
- `判断这个架构方案是否正确。`

## Mode Selection

- Use **Diagnose** when the user asks what is wrong, why it sounds like AI, or which parts need editing.
- Use **Rewrite** when the user asks to polish, optimize, remove AI style, or improve a draft. Output only the edited article by default.
- Use **Direct Edit** when the user asks for only the final text.
- Use **Reddit Adaptation** when the user asks for Reddit, subreddit, Hacker News-like community tone, or an English developer-community post. Output title and body only by default.
- Use **Diagnose** output only when the user asks what is wrong, asks for notes, or asks for before/after explanation.

## Editing Bias

Prefer:

- preserved or clarified judgment over abstract value claims
- real tradeoffs over balanced-sounding filler
- project context over generic industry language
- short direct sentences over symmetrical paragraph templates
- concrete Reddit title over clickbait or slogan
- transparent build notes over promotional claims

Avoid:

- "AI humanizer" framing
- anti-detection claims
- fake personal experience
- unsupported technical claims
- literary or promotional overcorrection
- link-first launch copy
- fake community questions such as "What do you think?" when there is no real ask

## Output Bias

- Default to the edited article only.
- For Reddit adaptation, default to `Title:` plus post body only.
- Add change notes, removed expressions, or before/after commentary only when requested.
- Preserve the author's judgment; clarify it when the draft already contains the evidence, but do not make the judgment stronger than the supplied context supports.
