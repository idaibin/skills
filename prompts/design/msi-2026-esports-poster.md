# MSI 2026 Esports Poster Generation Prompt

Use this prompt to generate consistent `4:5` vertical match-result and match-preview posters for the 2026 League of Legends Mid-Season Invitational.

The prompt is designed for ChatGPT image generation or another image model that can use uploaded logo and key-art references. It prioritizes factual accuracy, clear hierarchy, restrained composition, and visual alignment with the approved MSI 2026 direction.

## Required Inputs

Provide as many of the following fields as possible:

```text
Mode: result | preview
Tournament: MSI 2026
Stage: e.g. Lower Bracket Round 3 / Lower Bracket Final
Team A: team name and abbreviation
Team B: team name and abbreviation
Score: required only for result mode
Winner: required only for result mode
Date: required only for preview mode
Time: required only for preview mode
Timezone: e.g. Beijing Time / JST / KST
Format: e.g. BO5
Next step: optional, e.g. winner advances to face BLG
Primary language: Chinese
Team logo references: uploaded files or verified official assets
MSI 2026 visual reference: uploaded official key art or verified official asset
```

## Source Verification

Before generating the poster:

1. Verify the result, schedule, stage, format, date, and time against an official or authoritative source.
2. Prefer LoL Esports official schedules, brackets, announcements, and broadcasts.
3. Convert time to the requested timezone explicitly.
4. Do not infer a final score from an in-progress match.
5. Do not invent a next opponent or advancement path.
6. If the result or schedule cannot be verified, stop and report the unresolved field instead of generating a misleading poster.

## Fixed Visual Direction

```text
Canvas: 1080 x 1350
Aspect ratio: 4:5 vertical
Primary background: warm gray-white or off-white paper
Primary text: near-black
Primary accent: signal red or red-orange brush stroke
Secondary accent: small acid-lime detail
Texture: subtle paper grain, restrained print noise, light scratches
Typography: extra-condensed, heavy, modern sans-serif
Composition: editorial sports graphic, flat and structured
Visual density: low to medium
```

The poster should feel related to the approved MSI 2026 visual language:

- oversized black typography
- gray-white printed-paper background
- red-orange painted bars or rough editorial marks
- sparse acid-lime highlights
- thin technical lines, target marks, or small coordinate-like details
- asymmetric but controlled layout
- strong whitespace and obvious reading order

Do not reproduce an official poster pixel-for-pixel. Use the reference as a visual system, not as a tracing target.

## Shared Layout Rules

- Generate one independent poster per image.
- Do not place result and preview posters on the same canvas.
- Use the real team logos supplied or retrieved from verified sources.
- Keep both team logo areas visually balanced.
- Team names, logos, and scores must refer to the same side consistently.
- Never swap a team logo, team abbreviation, or score after layout.
- Use Chinese for the primary information hierarchy.
- Short English labels such as `WINNER`, `SERIES RESULT`, `LOWER BRACKET FINAL`, or `BO5` may be used as secondary decoration.
- Keep the bottom area clean. Do not add `近两日焦点`, social-media slogans, hashtags, engagement prompts, or unrelated footer copy.
- Avoid long paragraphs. The poster should communicate the match in one glance.
- Do not use fabricated player faces. Only include players when verified photographs are explicitly provided and requested.

## Result Mode Rules

Result mode communicates a completed series.

### Information hierarchy

1. `MSI 2026`
2. stage and `赛果`
3. winner and losing team
4. final score
5. short Chinese result headline
6. optional advancement or elimination line

### Ordering contract

- The winner must appear first.
- The winner must be on the left unless the user explicitly requests another arrangement.
- The score must follow the same order as the teams.
- Example: `LYON 3:0 G2` means LYON is left, LYON has `3`, G2 is right, and G2 has `0`.
- Do not write `G2 vs LYON` above a `3:0` score when LYON is the winner.

### Recommended result structure

```text
Top left:
MSI 2026
CALL YOUR SHOT
MID-SEASON INVITATIONAL · DAEJEON

Top right:
[stage] · 赛果

Red-orange brush bar:
WINNER                                      SERIES RESULT

Main team row:
[winner logo]                               [loser logo]
[WINNER ABBR]                               [LOSER ABBR]

Main score:
[winner score] : [loser score]

Headline:
[WINNER ABBR] [short result statement]

Supporting line:
[optional advancement or elimination statement]
```

### Result headline examples

Use only when factually correct:

```text
LYON 横扫晋级
BLG 四局取胜
HLE 挺进下一轮
G2 止步 MSI
```

Do not force dramatic wording when the score does not support it. Use `横扫` only for a sweep such as `3:0`.

## Preview Mode Rules

Preview mode communicates an upcoming series.

### Information hierarchy

1. `MSI 2026`
2. stage and `预告`
3. Team A versus Team B
4. date and exact local time
5. timezone and series format
6. optional advancement implication

### Preview contract

- Do not display a score.
- Do not mark either team as winner.
- Do not place `WINNER` or `SERIES RESULT` on a preview poster.
- Keep both teams visually equal unless the user explicitly requests a narrative emphasis.
- Use `VS` only as the matchup separator.

### Recommended preview structure

```text
Top left:
MSI 2026
CALL YOUR SHOT
MID-SEASON INVITATIONAL · DAEJEON

Top right:
[stage] · 预告

Red-orange brush bar:
[English stage label]                              [format]

Main matchup row:
[Team A logo]                VS                [Team B logo]
[TEAM A]                                       [TEAM B]

Headline:
[short Chinese matchup title]

Time block:
[date] · [time]
[timezone] · [format]

Supporting line:
[optional advancement implication]
```

### Preview headline examples

```text
败者组生死战
决赛席位之争
晋级之战
强强对决
```

Use restrained wording. Do not claim a rivalry, revenge narrative, or historical significance unless it is verified.

## Direct Generation Prompt

Replace all bracketed variables before use.

```text
生成一张独立的 4:5 竖版英雄联盟电竞海报，尺寸 1080×1350，赛事为 MSI 2026。

模式：[result 或 preview]
赛段：[stage]
队伍 A：[team A]
队伍 B：[team B]
比分：[result 模式填写；preview 模式删除此行]
胜者：[result 模式填写；preview 模式删除此行]
比赛时间：[preview 模式填写；result 模式删除此行]
时区：[timezone]
赛制：[format]
后续信息：[optional next step]

严格参考提供的 MSI 2026 官方主视觉素材所体现的设计系统，但不要逐像素复刻：
灰白偏暖的纸张底色，黑色超粗窄体无衬线字体，信号红或红橙色粗粝笔刷条，极少量酸性黄绿色点缀，细线、靶心标记和轻微印刷颗粒。整体必须像官方国际电竞赛事编辑海报，简洁、平面、克制、有留白，不要复杂场景和电影级特效。

[result 模式规则]
胜者必须放在前面并默认位于左侧；败者位于右侧。队名、Logo 和比分必须左右完全对应。比分按“胜者分数 : 败者分数”显示。顶部标注赛段与“赛果”，红橙色笔刷条可放置 WINNER 和 SERIES RESULT。画面中央突出双方 Logo、队名和最终比分，下方使用一句简短中文赛果标题，并可补充真实的晋级或淘汰信息。

[preview 模式规则]
双方地位对等，左右平衡，中间只显示 VS，不显示任何比分、胜者标识或赛果词汇。顶部标注赛段与“预告”，红橙色笔刷条可放置英文赛段和 BO5。下方清晰显示日期、时间、时区和赛制，并可补充真实的晋级条件。

Logo 必须使用提供或核验过的真实战队 Logo，不要自行重新设计战队标志。Logo 区域尺寸均衡，背景保持统一，不要为左右战队分别制作两套主题底色。

主要文字使用中文，英文只作为短标签和装饰。文字必须清晰、无乱码、无重复。底部保持干净，不要添加“近两日焦点”、口号、话题标签、关注提示或无关信息。
```

## Negative Prompt

```text
不要黑金奢华风。
不要米金背景。
不要紫色科技模板。
不要蓝橙左右对撞背景。
不要火焰、闪电、爆炸、龙、凤凰、狮子写实场景。
不要电影海报式复杂合成。
不要选手大头拼贴。
不要虚构选手或错误队服。
不要三维金属字体。
不要玻璃拟态面板。
不要高密度 HUD。
不要长段文案。
不要在预告图中出现比分或胜者。
不要在赛果图中把败者放在胜者前面。
不要让队名、Logo 和比分左右错位。
不要生成错误或近似战队 Logo。
不要添加“近两日焦点”。
不要把两张海报拼在一张画布中。
```

## Final Validation

Before returning the image, verify all of the following:

- image is a single `4:5` vertical poster
- tournament is `MSI 2026`
- mode is clearly result or preview, never mixed
- stage label is correct
- team logos match the team names
- result mode places the winner first
- result score matches team order
- preview mode contains no score or winner marker
- date, time, timezone, and format are correct
- Chinese text is readable and not duplicated
- visual style uses gray-white, black, red-orange, and minimal acid-lime
- no black-gold fantasy treatment
- no `近两日焦点`
- no fabricated players, logos, score, schedule, or advancement claim
