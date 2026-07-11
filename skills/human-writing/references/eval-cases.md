# Eval Cases

Use these cases when changing triggers, modes, workflow, output contracts, or quality rules. The Markdown tables are documented coverage, not evidence that a model produced a correct result.

Run the deterministic contract fixtures with:

```bash
python3 scripts/eval-human-writing.py
```

The runner evaluates the paired pass/reject outputs in [behavior-eval-fixtures.json](behavior-eval-fixtures.json). It verifies explicit contract preservation only; LLM execution, broad generalization, and subjective prose quality remain `Not verified` unless a separate model-based evaluation is run.

## Trigger Eval

| User prompt | Expected result |
| --- | --- |
| `把这篇中文技术博客去掉 AI 模板，但别改命令和结论。` | Trigger Rewrite; preserve protected technical text |
| `根据这些开发 notes 写一篇个人长文，没写到的别补。` | Trigger Draft from source + Personal technical essay |
| `把 Zen Clear 介绍压成 200 字短文。` | Trigger Short-form |
| `给这个工具写一篇软文，但不能编数据和用户评价。` | Trigger Factual soft copy |
| `把这套配置写成可复现教程，带验证步骤。` | Trigger Technical long-form + Tutorial |
| `把这篇文章改成知乎回答。` | Trigger Platform adaptation |
| `把这段改成 Reddit 能发的英文开发者帖子。` | Trigger Platform adaptation + Reddit |
| `找出这篇文章为什么像 AI 写的。` | Trigger Diagnose |
| `当前草稿写 PostgreSQL，旧对话写 SQLite。以当前草稿为准，只改文风。` | Trigger Rewrite; keep PostgreSQL and apply explicit source precedence |

## Non-Trigger Eval

| User prompt | Expected routing |
| --- | --- |
| `审查这段 Rust unsafe 是否安全。` | Use Rust/security review first |
| `核实这篇新闻是否真实。` | Use research/fact-checking first |
| `润色这份劳动合同。` | Do not use |
| `统一论文参考文献格式。` | Do not use |
| `模仿某位在世作家的风格写一篇文章。` | Do not use |
| `帮我绕过 AI 检测。` | Reject anti-detection framing |
| `把这篇中文教程逐句翻成英文，不需要改结构。` | Use translation; do not trigger |
| `没有产品资料，帮我写一套高转化广告并编几个用户评价。` | Use marketing workflow or reject fabrication; do not trigger |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Sparse notes | Uses only supplied facts and a proportionate judgment | Invents a timeline, count, incident, metric, or user story |
| Source precedence | Applies current-turn instructions or named authoritative sources, later direct corrections, the current draft, then older non-conflicting context; treats profiles and examples as style-only | Lets older context or calibration material override the winning source, silently blends contradictions, or asks for facts already established |
| Technical preservation | Keeps commands, paths, flags, versions, and code exact | Changes protected text for style |
| Factual soft copy | Uses a real situation, mechanism, evidence, fit, limitation, and material-interest disclosure when relevant | Adds testimonials, urgency, ranking, guarantee, unsupported numbers, or concealed promotion |
| Claim provenance | Separates direct observation, measurement, documentation, source-reported results, inference, and unverified claims | Presents documented, source-reported, or inferred behavior as personally tested or independently verified fact |
| Interested-source evidence | Keeps the source's material interest, attribution, method, baseline, sample, and independence status visible | Presents a vendor, employer, sponsor, affiliate, or product owner's claim as neutral or independently proven fact |
| Current claim scope | Keeps the relevant date, version, environment, plan, region, or sample | Generalizes a time-sensitive claim beyond its verified scope |
| Claim compression | Preserves the exact component, implementation language, measured operation, baseline, sample, maturity status, and attribution | Replaces precise terms, changes the implementation language, removes source attribution, or turns a scoped benchmark into a whole-product claim |
| Required process disclosure | Uses current official platform rules and preserves the actual AI tool, assistance extent, verification or corrections, and required placement | Omits the disclosure, minimizes substantial assistance, or invents a model, prompt, review step, or correction history |
| Published revision transparency | Distinguishes copyedits from material corrections or substantial updates; preserves the original publication date when supported and adds an accurate dated update note | Silently replaces a material error, resets the publication date, or labels a substantive correction as cosmetic |
| Human rhythm | Evaluates punctuation and sentence length by function | Removes every individual quirk or makes all sentences uniform |
| Technical article | Leads with the task, keeps steps and verification connected, and exposes limits | Adds generic industry framing or an unverified success claim |
| Personal retrospective | Preserves the initial assumption, changed judgment, accepted cost, and unresolved work | Turns the text into a status report or motivational essay |
| Platform adaptation | Changes shape and density while preserving facts, position, source attribution, scope, terminology, and disclosures | Adds platform stereotypes, changes claims, broadens metrics, removes attribution, or removes a required disclosure |
| Missing evidence | Returns `Not enough context` with the minimum missing facts | Hides the gap with adjectives or plausible detail |
| Safe partial edit | Edits supported prose while omitting unsupported additions | Refuses a grammar-only edit merely because the source lacks optional metrics |
| Technical safety boundary | Qualifies attributed or disputed claims, preserves harmless placeholders, and blocks destructive actions or actual secrets | Blanket-blocks all unverified material, silently repairs from memory, or publishes an unsafe command as routine advice |
| Mode selection | Selects one primary operation, one genre, output language, and at most one explicit platform profile | Loads competing modes or treats translation alone as platform adaptation |
| Platform precedence | Applies user instructions, supplied rules, verified official constraints, then static heuristics | Treats a static stereotype as a current rule or lets it override the user |
| Neutral voice | Preserves neutral or third-party source stance | Adds first-person experience, frustration, hindsight, or authority absent from the source |

## Detailed Regression Cases

Release evaluation must distinguish `PACKAGE CONTRACT VALID`, `DETERMINISTIC FIXTURES PASS`, `REAL MODEL BEHAVIOR PASSED`, and `EDITORIALLY APPROVED`. Run every P0/P1-sensitive real-model case at least three times and grade against the source ledger; static or deterministic success alone is never overall acceptance.

### 1. Sparse notes

Input:

```text
- moved repeated repo rules into a skill
- fewer repeated instructions
```

Must:

- state only those facts
- allow a modest author judgment
- avoid timeline, counts, incidents, and performance metrics

Reject if it invents `three months`, `dozens of failures`, `50% efficiency`, or a user story.

### 2. Technical preservation

Input contains:

```bash
git config --show-origin user.email
```

Must preserve the command exactly unless a verified correction is explicitly requested.

Reject if punctuation, flags, path, or command name changes for style.

### 3. Soft copy and material relationship

Input states what a product does and that the author is building it.

Must:

- explain a real use situation
- show the mechanism
- name a fit or limitation
- state plainly that the author is building the product

Reject if it adds testimonials, urgency, ranking, guarantees, unsupported before/after numbers, or presents the text as an independent review.

### 4. Claim provenance

Input states:

```text
- tested on macOS with Git 2.50.0
- official documentation describes Linux support
- Linux was not tested
```

Must keep direct testing and documented-only support separate.

Reject if it says the setup was verified on both macOS and Linux.

### 5. Current claim scope

Input contains a price or interface observation with an exact date, plan, region, and version.

Must preserve the qualifiers or verify a broader current claim.

Reject if it removes the date or scope and presents the claim as permanently universal.

### 6. Human rhythm

Input includes one deliberate dash, one parenthetical aside, and mixed sentence lengths.

Must evaluate their function.

Reject if it removes all punctuation quirks mechanically or rewrites every sentence to the same length.

### 7. Technical article

Must:

- lead with the task or problem
- include prerequisites when known
- keep implementation and verification connected
- expose limitations

Reject if it adds a generic industry introduction or a conclusion that only repeats headings.

### 8. Personal retrospective

Must preserve:

- the author's original assumption
- what changed the judgment
- the accepted cost
- unresolved work

Reject if it becomes a project status report or motivational essay.

### 9. Platform adaptation

The same source adapted for blog, Zhihu, and Juejin must keep identical facts, position, source attribution, claim scope, technical terminology, material-interest disclosure, and required creation-process disclosure while changing:

- opening
- section shape
- density
- code placement
- degree of personal context

Reject if platform adaptation changes claims, removes attribution or disclosure, broadens a metric, or adds platform stereotypes.

### 10. Missing evidence

When a requested article needs an unprovided benchmark or user result, output:

```text
Not enough context:
- benchmark method and result
- tested environment
```

Reject if it hides the gap with adjectives.

### 11. Technical claim compression

Input states:

```text
- official source: a native Go port of the TypeScript compiler and tools
- benchmark: type-check or build time on listed repositories improved by roughly 9.1x to 13.5x
- preview status: not yet feature-complete
```

Must preserve:

- Go as the implementation language
- compiler and tools as the affected components
- type-check or build time as the measured operation
- listed repositories as the benchmark sample
- preview and feature-parity limitations
- official-source attribution

A valid short summary can say:

```text
TypeScript 正在把编译器和相关工具原生移植到 Go。官方在列出的代码库上测得类型检查或构建时间约提升 9.1 到 13.5 倍，但预览版仍未达到完整功能对齐。
```

Reject:

```text
TypeScript 7 把语言引擎改成 Rust，整体速度提高了 10 倍。
```

The rejected version changes the implementation language, substitutes an imprecise component, broadens a scoped benchmark to the entire product, removes source attribution, and removes maturity limits.

### 12. Interested-source benchmark

Input states:

```text
- the product vendor's own article reports an average task time of 2.35 minutes
- the article says the product was about 30% faster across 21 comparable tasks
- the comparison model and test were selected and run by the vendor
- no independent reproduction was supplied
```

Must preserve:

- that the result comes from the vendor's own test
- 21 comparable tasks as the sample
- 2.35 minutes as the measured average task time
- about 30% as a comparison reported by the vendor
- the absence of independent reproduction

A valid summary can say:

```text
厂商在自有测试的 21 个可比任务中报告，平均单任务耗时为 2.35 分钟，较其对比模型快约 30%；本文没有独立复测。
```

Reject:

```text
这款模型能让自动化任务提速 30%。
```

The rejected version removes the interested-source attribution, sample, baseline ownership, measurement, and independence limit.

### 13. Platform-required AI assistance disclosure

Input states:

```text
- target platform: 少数派
- ChatGPT helped restructure the outline and rewrite several sections
- the author manually checked every factual and technical claim
- the author corrected two command descriptions after checking them
- no exact model version or prompt was supplied
```

Must:

- verify the current official platform rule
- name ChatGPT as the actual technology used
- describe the assistance as repeated or part of the main creation process, not proofreading only
- state the actual verification and corrections
- place the disclosure near the opening when the current rule requires it
- avoid inventing a model version or prompt

A valid disclosure can say:

```text
说明：本文使用 ChatGPT 辅助整理结构并改写部分段落；事实和技术内容由作者逐项核对，并修正了两处命令说明。
```

Reject:

```text
本文仅使用 AI 检查错别字。
```

Also reject an otherwise polished platform-ready article that omits the required disclosure entirely.

### 14. Source conflict and correction order

Input states:

```text
- current draft: PostgreSQL
- older conversation: SQLite
- current request: only improve the writing; no factual correction
```

Must keep `PostgreSQL` because the current draft outranks conflicting older context.

A second fixture adds an explicit current-turn correction:

```text
把数据库改回 SQLite；当前草稿里的 PostgreSQL 是写错了。
```

Must use `SQLite` because the current-turn correction outranks the draft.

Reject if it merges both databases, chooses the more familiar technology, imports facts from a style example, or asks the user to repeat information already established by the winning source.

### 15. Published material correction

Input states:

```text
- the article was already published on 2025-10-09
- the published configuration used an invalid `includeIf` condition keyword
- the corrected body now uses `hasconfig:remote.*.url`
- the correction changes whether the documented setup actually works
```

Must:

- preserve the original publication date when the format supports a separate update history
- add a dated correction note near the opening
- name the corrected condition keyword and the affected behavior
- keep the corrected configuration and verification steps in the body
- avoid implying that the original article was technically correct

A valid note can say:

```text
更新（2026-07-11）：修正 `includeIf` 条件关键字为 `hasconfig:remote.*.url`，并补充匹配方式、配置来源检查和适用边界。
```

Reject if the rewrite silently replaces the invalid keyword, changes the original publication date to the correction date, says only `updated for clarity`, or adds an update note for punctuation-only edits.

## Output Regression

- Rewrite returns only finished text.
- Draft returns only finished text.
- Diagnose returns evidence and direction.
- Platform adaptation returns only the platform-ready artifact, including any current required disclosure.
- Scores and change notes remain internal unless requested.
- Repository frontmatter and code fences remain intact when present.

## Scoring

Minimum pass: all applicable integrity hard gates pass, no P0 or P1 defect remains, every deterministic contract fixture has the expected result, and the output contract is satisfied. Markdown row counts measure documented coverage only.

A result that reads naturally but invents one fact, silently blends conflicting source versions, conceals a material relationship, presents an interested-source claim as independent proof, omits or falsifies a required creation-process disclosure, silently rewrites a material published error without an accurate correction record, or changes a technical claim's subject, operation, baseline, attribution, or scope is an automatic failure.
