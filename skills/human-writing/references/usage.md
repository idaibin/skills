# Usage

Use `human-writing` when the main job is to turn supplied facts, notes, or a draft into publishable writing with a recognizably human voice.

## Contents

- [Trigger Examples](#trigger-examples)
- [Non-Trigger Examples](#non-trigger-examples)
- [Mode Selection](#mode-selection)
- [Language Strategy](#language-strategy)
- [Required Context](#required-context)
- [Editing Priority](#editing-priority)
- [Output Behavior](#output-behavior)
- [Validation Boundary](#validation-boundary)

## Trigger Examples

- `用 human-writing 把这篇技术博客重写得像我自己写的，保留所有命令和结论。`
- `根据这些真实开发记录写一篇长文，不要补我没说过的经历。`
- `把这段改成 200 字以内的短文，只保留一个观点。`
- `给这个开发者工具写一篇克制的软文，不要编用户评价和数据。`
- `把这篇项目复盘改得更像个人博客，不要汇报体。`
- `把这个教程改成掘金能直接发布的版本，保留版本、命令和验证步骤。`
- `把这篇文章改成知乎回答，先直接回答问题，再展开理由。`
- `把这段产品介绍改成公众号文章，但不要标题党和强行升华。`
- `把这篇复盘改成 Reddit / Hacker News 风格的英文帖子。`
- `先用英文理清这组开发记录的论点和结构，再写成自然的中文终稿；英文中间稿不用给我。`
- `找出这篇文章里的 AI 模板、事实风险和口吻漂移。`

## Non-Trigger Examples

- `审查这段 Rust 代码有没有并发问题。`
- `核对这篇新闻里的事实是否准确。`
- `把合同改得更严谨。`
- `统一论文引用格式。`
- `把这篇英文逐句翻成中文，不需要调整结构、语气或平台表达。`
- `模仿某位在世作家的文风写一篇新文章。`
- `帮我骗过 AI 检测器。`

Route these to the relevant review, research, legal, academic, or creative-writing workflow.

## Mode Selection

| Request | Mode | Default output |
| --- | --- | --- |
| What sounds wrong or AI-like? | Diagnose | Evidence-based issues and editing direction |
| Improve an existing draft | Rewrite | Finished text only |
| Write from notes, logs, or evidence | Draft from source | Finished text only |
| Caption, tweet, announcement, brief opinion | Short-form | Platform-ready text only |
| Product or service article with persuasion | Factual soft copy | Finished copy only |
| Tutorial, architecture note, retrospective | Technical long-form | Finished article only |
| Same content for another platform | Platform adaptation | Target-platform artifact only |

A request has one primary operation. Genre, language, platform, disclosure, and revision handling are orthogonal selections:

| Axis | Selection rule |
| --- | --- |
| Primary operation | One per artifact: Diagnose, Rewrite, Draft from source, or Platform adaptation; a bounded secondary operation may directly support it |
| Genre | One primary profile per artifact when material; bounded secondary elements may support it without blending incompatible contracts |
| Language | Preserve source language unless another final language is requested; an English-first intermediate may support a Chinese final, while translation-only work routes elsewhere |
| Platform | Zero or one named target; load calibration only for explicit adaptation |
| Evidence state | Complete, safely partial, conflicting, or blocked |
| Claim state | Observed past, current state, committed plan, candidate direction, or unresolved question |
| Conditional modules | Load disclosure and published-revision rules only when applicable |

## Language Strategy

- Prefer direct editing when the source is already a usable Chinese draft or the user supplied a strong Chinese voice sample.
- For a requested Chinese final built from notes, logs, or mixed-language evidence, prefer a private English claim-and-structure pass when it makes reasoning or organization clearer.
- Treat English as a provisional composition layer, not as evidence. Translate editorially rather than sentence by sentence, then verify the Chinese final against the original source ledger.
- Keep exact commands, identifiers, quotations, metrics, attribution, modality, and claim scope stable across the language boundary.
- Return only the requested final language unless the user asks to inspect the intermediate.

Load only what the request needs:

- always apply `fact-integrity.md`
- load `content-modes.md` when form changes structure or evidence requirements
- load `reasoning-and-explanation.md` when long-form value depends on changing a mental model, deriving a decision, explaining a boundary, or preserving a diagnostic witness
- load `platform-calibration.md` only for a named platform adaptation
- load `revision-transparency.md` only for already-published material with substantive changes
- use style references and examples for calibration, never as sources of facts or author experience

## Required Context

Use what the user has already supplied. Infer only low-risk editorial choices such as paragraph length. Do not infer facts.

Recover context from the current draft, supplied notes, named repository files, and already-established decisions before asking follow-up questions. Ask only when a missing answer would change the claim, audience, action, format, or safety of the artifact. Do not turn a reusable brief into a ritual questionnaire.

The useful context fields are:

- source material
- target reader
- purpose
- platform
- desired length
- final language and whether an intermediate should be exposed
- author sample
- protected text
- desired action
- claims that require verification

Classify visibility separately from transformation:

- **Visibility:** artifact-visible, artifact-visible with attribution, background-only, or do-not-disclose.
- **Transformation:** verbatim, meaning-preserving edit, summarize-only, or do-not-use.

`Read these records before writing` normally requests better analysis, not an article about the records. Promote background evidence into the artifact only when the user asks to show the method, the source is itself the topic, or attribution is necessary for trust.

Apply claim status, actor role, directive precedence, and claim authority from `fact-integrity.md`. A style request does not change factual confidence or commitment status.

For follow-up edits, use the latest authoritative draft under `fact-integrity.md`. Locate the argument the instruction changes, integrate it there, then scan the opening, adjacent section, and ending for stale framing, duplication, or contradiction. Create a new section only when the idea has enough independent weight or the user explicitly asks for one.

Classify missing context:

- **Safely partial:** edit the supported material and omit unsupported additions.
- **Blocked:** return `Not enough context:` plus the minimum missing fields when completion would require invention or unjustified certainty.
- **Diagnose:** identify unsupported claims and missing evidence.
- **Placeholder-enabled:** retain explicit placeholders only when the user requested them or the artifact contract permits them.

Use the technical-publication decision table in `fact-integrity.md`. Attributed unverified or disputed claims may remain with visible status; harmless placeholders and non-destructive unexecuted examples do not require blanket blocking. Destructive or irreversible actions, actual secrets, and claims whose correctness is required to complete the artifact must be blocked or handed to the relevant technical review skill. Do not silently correct them from memory.

## Editing Priority

Use this order:

1. factual and technical integrity
2. author's actual position
3. reader comprehension
4. information density
5. structure and rhythm
6. platform fit
7. surface polish

Do not trade a higher-priority item for a smoother sentence.

## Planning Boundary

For a new long-form or multi-claim artifact, use a private outline that pairs each section's job with supported claims, evidence, limits, and transitions. Convert that outline into the requested prose; do not return planning bullets unless the user asks for an outline. Skip the outline for short-form, straightforward rewrites, and bounded local edits where it adds no decision value.

The outline may organize evidence but cannot upgrade it. A blank evidence slot stays blank, qualified, omitted, or blocked under `fact-integrity.md`; it is never filled with a plausible example, metric, quotation, scene, or experience.

## Output Behavior

- Do not announce the workflow.
- Do not explain that the text was "humanized."
- Do not expose the source ledger, inspection process, prompt interpretation, or editorial analysis unless requested.
- Do not expose an English intermediate when only a Chinese final was requested.
- Do not append a change log, score, or offer unless requested.
- Preserve repository frontmatter, links, code fences, and headings when editing a content file.
- When the user asks for multiple variants, make each variant solve a distinct editorial goal rather than swapping synonyms.
- In iterative editing, return the updated artifact or edit the requested file; do not narrate the sequence of additions inside the artifact.

## Validation Boundary

`validate-skills.py --quality-report` reports documented Eval coverage. `eval-human-writing.py` runs deterministic fixtures. Report these only as `PACKAGE CONTRACT VALID` and `DETERMINISTIC FIXTURES PASS`. `REAL MODEL BEHAVIOR PASSED` requires repeated production-model runs with semantic grading; `EDITORIALLY APPROVED` requires blind source-relative editorial review. Only all four layers justify `HUMAN WRITING ACCEPTED`.
