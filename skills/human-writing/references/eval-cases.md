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
| `看 Git 记录和之前的沟通，分析我的思路变化后重写文章；这些记录只用于理解，不要把分析过程写进正文。` | Trigger Rewrite + Personal technical essay; keep Git/chat evidence background-only |
| `在刚才那篇文章里补充：我现在主要规划，实施和验证交给 AI；把它自然融进去，不要写成补丁。` | Trigger Rewrite; revise the cumulative artifact and remove iterative-edit seams |
| `后续可以做前端改造、工程优化、集成新模块之类的。` | Trigger Rewrite or Draft from source; preserve examples as candidate directions, not commitments |
| `把 Zen Clear 介绍压成 200 字短文。` | Trigger Short-form |
| `给这个工具写一篇软文，但不能编数据和用户评价。` | Trigger Factual soft copy |
| `把这套配置写成可复现教程，带验证步骤。` | Trigger Technical long-form + Tutorial |
| `把这篇文章改成知乎回答。` | Trigger Platform adaptation |
| `把这段改成 Reddit 能发的英文开发者帖子。` | Trigger Platform adaptation + Reddit |
| `根据这些开发记录写一篇文章；先用英文理清论点和结构，再给我自然的中文终稿，不要展示英文中间稿。` | Trigger Draft from source with the English-first Chinese-final language path; return Chinese only |
| `重写这篇现有草稿；先用英文理清论点和结构，再给我自然的中文终稿，不要展示英文中间稿。` | Trigger Rewrite with the English-first Chinese-final language path; return Chinese only |
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
| `把这篇英文逐句翻成中文，不需要调整结构或语气。` | Use translation; do not trigger |
| `没有产品资料，帮我写一套高转化广告并编几个用户评价。` | Use marketing workflow or reject fabrication; do not trigger |
| `先确认这个仓库的真实命令、入口和文档归属，不要改写内容。` | Prefer `repo-map`; repository mapping is not writing transformation |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Sparse notes | Uses only supplied facts and a proportionate judgment | Invents a timeline, count, incident, metric, or user story |
| Source precedence | Applies current-turn instructions or named authoritative sources, later direct corrections, the current draft, then older non-conflicting context; treats profiles and examples as style-only | Lets older context or calibration material override the winning source, silently blends contradictions, or asks for facts already established |
| Source visibility and transformation | Classifies whether material may appear separately from how permitted material may change; lets Git, logs, chats, searches, and editorial notes shape the result without automatically naming them | Treats verbatim text as automatically publishable, exposes background-only or do-not-disclose material, drops required attribution, or changes protected semantics |
| Follow-up authority | Separates editing instructions from claim authority; treats assistant wording as provisional and scopes acceptance to what the user supplied, corrected, or explicitly approved | Lets a style request change factual confidence, lets a local edit accept untouched assistant claims, or lets provisional wording outrank user evidence |
| Derived claims | Propagates the strictest indispensable visibility and attribution requirements through paraphrase, synthesis, and inference while allowing independently supported visible claims | Launders restricted details through fluent paraphrase, suppresses a separately supported visible claim, or applies one document-wide label to mixed spans |
| Iterative integration | Revises the cumulative accepted artifact, places the new point where it changes the argument, and updates nearby transitions and the ending | Mechanically appends `补充` or `后续计划`, repeats earlier claims, leaves stale framing, or narrates the user's instruction sequence |
| Plan status | Keeps observed, current, committed, candidate, and unresolved material distinct; gives future work a reason, priority, or validation rule when supplied | Turns `可以`, `考虑`, `候选`, `之类`, or a question into a promise, active implementation, completed result, or invented deadline |
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
| English-first Chinese final | Uses English only as a private provisional structure when useful, skips it for a stronger existing Chinese draft unless requested, checks the natural Chinese final against the original evidence, and preserves exact commands, identifiers, numeric ranges, attribution, modality, and status | Treats English as new evidence, exposes an unrequested intermediate, translates literally, or changes any protected source field, terminology, metric, status, or scope |
| Missing evidence | Returns `Not enough context` with the minimum missing facts | Hides the gap with adjectives or plausible detail |
| Safe partial edit | Edits supported prose while omitting unsupported additions | Refuses a grammar-only edit merely because the source lacks optional metrics |
| Technical safety boundary | Qualifies attributed or disputed claims, preserves harmless placeholders, and blocks destructive actions or actual secrets | Blanket-blocks all unverified material, silently repairs from memory, or publishes an unsafe command as routine advice |
| Mode selection | Selects one primary operation and genre per artifact, allowing only bounded supporting operations/elements and an optional language path; splits materially different outputs | Blends incompatible modes or platform constraints, under-delivers a requested diagnose-and-rewrite, treats translation alone as platform adaptation, or turns English-first composition into a separate primary mode |
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

### 16. Background evidence visibility

Input states:

```text
- read Git history and prior chats before rewriting
- verified change: the author moved from PostgreSQL-first expansion to SQLite-first scope reduction
- the records are for analysis only
- target: a personal retrospective about the author's changed judgment
```

Must:

- express the initial ambition, changed priority, chosen boundary, and remaining tradeoff
- keep PostgreSQL and SQLite technically accurate
- keep Git history, chats, source ledger, and the editor's analysis process out of the article

A valid passage can say:

```text
我最初想把后台能力尽量补齐，后来更在意本地能不能直接运行，以及每增加一个外部依赖要付出什么维护成本。改用 SQLite，是我开始收缩项目边界，而不是宣布哪种数据库更好。
```

Reject:

```text
## Git 记录没有替我美化过程

如果只看 README，很容易误判项目。Git 和聊天记录显示，我的方向从 PostgreSQL 变成了 SQLite。
```

Also reject source-ledger labels, commit/file counts used as decorative proof, or repeated statements that the article was generated from verified records.

### 17. Iterative revision and plan status

Existing draft states:

```text
最初，我把 AI 当老师和代码生成器。现在它更像一个执行很快的协作者。
```

Follow-up instruction states:

```text
补充一下：现在我更多思考做什么、怎么做，实施和验证交给 AI。后续可以优化工程基线、改造前端、集成新模块之类的。
```

Must:

- integrate the role change into the existing AI-collaboration argument
- preserve implementation and verification as work delegated to AI, not work that happens without human review
- preserve engineering optimization and frontend work as intended directions
- keep unspecified new modules as candidates unless the source commits to them
- update nearby transitions or the ending if they still describe AI only as a code generator

A valid passage can say:

```text
现在我会先判断做什么、为什么做、准备怎么拆，再把具体实施和验证交给 AI，最终验收仍由我负责。接下来可以继续评估工程基线、前端改造和新的功能模块；它们目前都是候选，只有端到端边界走通以后才进入实现。
```

Reject:

```text
## 补充

AI 负责全部实施和验证。接下来我们将完成前端全面重构，并上线多个新模块。
```

Also reject invented module names, deadlines, completion claims, a detached appendix that repeats the original section, or an unchanged conclusion that contradicts the new role description.

### 18. Follow-up authority and derived-source policy

Input sequence:

```text
User source: 新模块只是候选。
Assistant draft: 新模块已经进入实施。
User follow-up: 把开头缩短一点。
```

Must restore or preserve candidate status. The local editing request does not accept the untouched assistant claim and does not change its authority.

A second input contains one mixed chat message:

```text
Artifact-visible: 我们调整了架构。
Background-only: 具体失败过程和内部成本。
Do-not-disclose: 责任人身份。
Verbatim: cargo check
```

Must:

- publish only claims with permitted provenance
- keep the command exact only if its visibility allows publication
- omit background-only details that are the sole provenance of a claim
- prevent the do-not-disclose identity and uniquely inferable details from appearing
- classify the smallest practical claims or spans rather than the whole message

Reject if paraphrasing exposes the internal cost, if `verbatim` is treated as disclosure permission, or if the visible architecture statement is suppressed despite independent visible support.

### 19. Context reuse and planning boundary

The current draft and supplied notes already establish:

```text
- reader: Rust developers considering an admin framework
- purpose: explain the author's boundary change
- length: roughly 1,500 Chinese characters
- evidence: verified project decisions and commands
```

Must reuse these fields without asking the user to repeat them. For a new multi-claim article, the writer may privately map sections to claims and evidence, but the default output must be finished prose rather than an outline or questionnaire.

Reject a response that asks again for the audience, purpose, length, or evidence merely because a generic brief template lists those questions. Also reject a final artifact that exposes `Section 1 / evidence slot / transition` planning scaffolding.

For a 120-character local rewrite with the same established context, skip the outline and return the edited text directly.

### 20. Contextual style diagnostics

Input includes this source-shaped sentence:

```text
这个方案能用——我也用了半年——但每次排错都要跨三个服务，我后来不想继续加了。
```

Must preserve its meaning, involvement, and cadence while editing only what materially helps. A dash, first person, passive construction, adverb, rhetorical question, or three-item list is not independently a defect.

Reject a mechanical rewrite justified only by a global ban such as `never use dashes`, `remove every adverb`, `always use active voice`, or `two items always beat three`. Also reject invented incidents, metrics, or emotions added to make the passage feel more human.

### 21. Whole-artifact audit and unchanged-source baseline

The source has a conservative body but its `description` says `完全自动更新`. Diagnose the metadata/body mismatch even when the requested bounded edit targets the opening. Do not preserve an unsupported metadata claim merely because frontmatter is normally left unchanged.

A second source says `清理判断应尽量在本机完成`. Reject a smoother rewrite that becomes `扫描结果不会上传云端`; the missing modal term upgrades a principle into an implementation and privacy guarantee.

A workflow assigns separate roles to `verify`, `validate`, and `commit/push`. Preserve each gate and the closing trace/rollback step. Parallel phrasing is legitimate when it defines different responsibilities.

When an abstract opening accurately previews the sections immediately below and the candidate has no concrete reader benefit, prefer the unchanged source. `original` plus a stop decision is a complete editorial result.

### 22. Internal proof before external verification

An architecture article calls its service layer framework-independent, while the included method signature directly accepts `PgPool`. Report this as a source-internal contradiction before checking the live repository.

A resource list repeats a URL under two titles and calls itself `完整`. Fix the visible duplicate, title-target mismatch, and unbounded completeness claim immediately; separately mark current reachability and maintainer status for live verification.

For configuration tutorials, test simultaneous matching conditions and their override order in addition to ordinary HTTPS/SSH happy paths. A command family, prerequisites, version scope, failure behavior, and expected result form one verification unit.

### 23. Reasoning and explanation

An architecture draft says two components are `opposites`, then lists generic pros and cons. The supplied evidence instead shows that one protects local interactivity while the other protects server-owned data access.

Must identify both locally valid invariants, locate the boundary where they need to compose, and explain what crosses that boundary, in which representation, under whose authority. Reject a rewrite that chooses a side before stating the shared criterion or treats a remote value as though it retained local executable identity.

A tutorial progressively explains a protocol with one record that changes from source data to serialized payload, cached copy, and rendered view. Must preserve the same conceptual anchor, label intermediate models as partial, state which component owns the canonical record, and distinguish copied or derived views from the source of truth. Reject unrelated examples at every stage, an animated reconstruction presented as the original event, or a valid derivation built on an unsupported premise.

A debugging retrospective contains a reproducible scrolling symptom and many unrelated UI elements. Must keep one observable witness while reducing the case, change one relevant condition at a time, and state the invariant revealed by the smallest failing and passing cases. Reject a simplified example that no longer reproduces the symptom or a metric that is easier to collect but does not represent the user-visible failure.

A conceptual essay proposes a new term. Must first show a recurring pattern the term compresses, then use the name to support later reasoning. Reject a catchy label unsupported by repeated evidence, a borrowed analogy without a stated limit, or an ending that adds a universal moral instead of the corrected model, bounded conclusion, remaining tradeoff, or next test.

Routing economy is part of the contract. Load `reasoning-and-explanation.md` for an architecture explanation whose conclusion depends on ownership and serialization boundaries or for a conceptual article whose reader starts from a broken model. Do not load it for a direct factual correction, a short technical definition with no material misconception, an architecture inventory with no explanatory claim, or a bounded source-preserving edit. Reject a response that expands those artifacts into a conceptual tutorial.

When only one boundary dimension matters, explain only that dimension. Reject an execution-phase explanation that adds unrelated identity, authority, and source-of-truth sections. Prefer one continuous example when it carries the reasoning, but preserve several examples when each is necessary; do not force them into one artificial anchor. One decisive counterexample may break the old model without an objection catalogue.

If a requested metric mismatches the architecture, state the mismatch, preserve the user's underlying intent, answer with architecture-aligned measurements, and retain any part of the original metric that remains relevant. Reject silent substitution of a different question or discarding a still-material request count merely because it is incomplete.

Apply witness-preserving reduction only to reproducible failures. A debugging retrospective must retain the failure while reducing the case; a project retrospective based on changing constraints must preserve its actual evidence chain without fabricating a technical symptom or failing/passing pair.

### 24. Template clusters and protected secondhand text

An evergreen configuration guide says `we added project.toml`, `replaced config.json`, and `improved overrides`. The supplied facts define the current file, precedence rule, and a version-scoped migration. Rewrite the evergreen guide around the current contract and keep the historical replacement only in the migration context. Reject prose that requires the reader to know the previous diff to understand present behavior. Keep change narration when the requested artifact is a release note, migration guide, correction note, or another version-scoped record.

A draft opens with `说实话？`, calls caching `性能的货币`, then stacks `很快。很强。也很危险。` before asking whether the team is ready. Diagnose the cluster: fake intimacy, unsupported aphorism, and manufactured staccato. Replace it with the concrete cache mechanism, risk, and decision criterion. Do not reject one candid phrase, metaphor, rhetorical question, or short emphatic sentence when it belongs to the supplied voice and adds information.

The source quotes the exact log text `No configuration file needed` and asks why it misleads users. Preserve the quote verbatim and edit only the surrounding analysis. Apply the same protection to titles, proper names, code, fixtures, and examples when their exact wording is evidence or protected text. Reject a rewrite that edits the quoted phrase because it resembles an AI-writing pattern.

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
