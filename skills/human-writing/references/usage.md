# Usage

Use `human-writing` when the main job is to turn supplied facts, notes, or a draft into publishable writing with a recognizably human voice.

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
- `找出这篇文章里的 AI 模板、事实风险和口吻漂移。`

## Non-Trigger Examples

- `审查这段 Rust 代码有没有并发问题。`
- `核对这篇新闻里的事实是否准确。`
- `把合同改得更严谨。`
- `统一论文引用格式。`
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
| Primary operation | Exactly one of Diagnose, Rewrite, Draft from source, Platform adaptation |
| Genre | Exactly one primary profile when material: short-form, factual soft copy, essay, tutorial, retrospective, architecture note, resource list |
| Language | Preserve source language unless the user requests another; translation-only work routes elsewhere |
| Platform | Zero or one named target; load calibration only for explicit adaptation |
| Evidence state | Complete, safely partial, conflicting, or blocked |
| Conditional modules | Load disclosure and published-revision rules only when applicable |

Load only what the request needs:

- always apply `fact-integrity.md`
- load `content-modes.md` when form changes structure or evidence requirements
- load `platform-calibration.md` only for a named platform adaptation
- load `revision-transparency.md` only for already-published material with substantive changes
- use style references and examples for calibration, never as sources of facts or author experience

## Required Context

Use what the user has already supplied. Infer only low-risk editorial choices such as paragraph length. Do not infer facts.

The useful context fields are:

- source material
- target reader
- purpose
- platform
- desired length
- author sample
- protected text
- desired action
- claims that require verification

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

## Output Behavior

- Do not announce the workflow.
- Do not explain that the text was "humanized."
- Do not append a change log, score, or offer unless requested.
- Preserve repository frontmatter, links, code fences, and headings when editing a content file.
- When the user asks for multiple variants, make each variant solve a distinct editorial goal rather than swapping synonyms.

## Validation Boundary

`validate-skills.py --quality-report` reports documented Eval coverage. `eval-human-writing.py` runs deterministic fixtures. Report these only as `PACKAGE CONTRACT VALID` and `DETERMINISTIC FIXTURES PASS`. `REAL MODEL BEHAVIOR PASSED` requires repeated production-model runs with semantic grading; `EDITORIALLY APPROVED` requires blind source-relative editorial review. Only all four layers justify `HUMAN WRITING ACCEPTED`.
