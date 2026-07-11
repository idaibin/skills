# Before and After Examples

These examples are non-normative calibration fixtures for package maintenance. Never use them as a source of facts, author experience, or mandatory phrasing.

## Short Product Post

Source facts:

- Zen Clear analyzes macOS developer disk usage.
- It distinguishes caches, build outputs, dependencies, and data that needs caution.
- The principle is understand first, clean second.
- The author is building Zen Clear.

Before:

```text
Zen Clear 是一款强大、智能、高效的 macOS 清理工具，能够全面赋能开发者磁盘管理，带来更安全、更透明、更极致的使用体验。
```

After:

```text
我在做 Zen Clear，一个面向开发者的 macOS 磁盘分析工具。

它先解释空间来自哪里：Cargo target、node_modules、Docker、Xcode，还是不该直接删除的数据。能不能重建、清理后会影响什么，也要说清楚。

我不想再做一个黑盒“一键清理”。先看懂，再决定删不删。
```

Why it works:

- uses only supplied facts
- discloses that the author is building the product
- shows the mechanism
- contains one real product judgment
- avoids unsupported performance claims

## Factual Soft Copy

Source facts:

- The author is building Zen Clear.
- The tool explains developer disk usage before cleanup.
- No benchmark, user count, testimonial, or comparison was supplied.

Before:

```text
在开发工具快速演进的今天，磁盘空间管理已经成为每位开发者必须面对的重要问题。Zen Clear 以创新技术打造智能清理闭环，让开发环境焕然一新。
```

After:

```text
Mac 的空间快满时，普通清理工具通常只告诉我哪个目录大。对开发环境来说，这还不够。

我正在做的 Zen Clear 想补的是这层解释：`target`、`node_modules`、Docker 镜像和 Xcode 数据分别属于什么工具，能不能重建，删除后会影响什么。

它更适合想自己做决定的开发者，不适合只想点一次按钮的人。
```

Why it works:

- starts from a recognizable situation
- makes the author's material interest explicit
- explains value through a concrete distinction
- names the fit and limitation
- avoids fake urgency and social proof

## Technical Retrospective

Before:

```text
AICraft 的建设具有重要意义。通过 Prompt、Skills 和标准文档的深度融合，实现了 AI 协作能力的全面升级，为后续发展奠定了坚实基础。
```

After:

```text
我最初把仓库规则写在每次对话里：先读 AGENTS，不要改 main，验证后再提交。规则没有变，重复输入却经常漏项。

AICraft 是我对这个问题的处理。一次任务的要求留在 Prompt，反复出现的执行顺序和边界放进 Skill，跨仓库都要遵守的规则再单独版本化。

它没有让 AI 自动变可靠，只是把“靠我每次记得提醒”改成了“先读取仓库里的固定资产”。这个变化更小，也更实际。
```

Why it works:

- identifies the original friction
- explains the boundary by contrast
- avoids claiming that the system solved more than it did

## Tutorial Opening

Before:

```text
在现代软件开发中，多仓库身份管理是一个非常重要且值得深入研究的话题。本文将从背景、原理、配置和总结四个方面详细介绍 Git includeIf。
```

After:

```text
我同时维护 GitHub 公共仓库和公司内部仓库，提交邮箱不能混用。每个仓库手动执行 `git config user.email ...` 能解决问题，但很容易忘。

Git 的 `includeIf` 可以按仓库目录或远程地址加载不同身份配置。下面这套配置覆盖 HTTPS 和 SSH，并给出验证命令。
```

Why it works:

- states the actual problem
- tells the reader what the tutorial delivers
- removes generic background
- preserves the technical term

## Tested Versus Documented

Source facts:

- The author ran the command on Git 2.50.0 on macOS.
- The product documentation also describes Linux support.
- The author did not test Linux.

Invalid draft:

```text
这套配置已经在 macOS 和 Linux 上验证可用。
```

Valid draft:

```text
我在 macOS 的 Git 2.50.0 上验证了这套配置。官方文档也说明该条件适用于 Linux，但本文没有在 Linux 环境复测。
```

The valid draft keeps direct observation, documentation, and untested scope separate.

## Technical Claim Compression

Source facts:

- An official source describes a native Go port of the TypeScript compiler and related tools.
- Its listed repository benchmarks measure type-check or build time, with speedups ranging from roughly 9.1x to 13.5x.
- The preview is not yet feature-complete.

Invalid compression:

```text
TypeScript 7 把语言引擎改成 Rust，整体速度提高了 10 倍。
```

Valid compression:

```text
TypeScript 正在把编译器和相关工具原生移植到 Go。官方在列出的代码库上测得类型检查或构建时间约提升 9.1 到 13.5 倍，但预览版仍未达到完整功能对齐。
```

Why the valid version works:

- keeps Go as the implementation language
- names the affected component instead of inventing `语言引擎`
- attaches the number to type-check or build time and the listed sample
- preserves official-source attribution
- preserves the preview and maturity limitation

## Interested Source Versus Independent Evidence

Source facts:

- A product vendor's own article reports an average task time of 2.35 minutes.
- The article says the product was about 30% faster across 21 comparable tasks.
- The vendor selected and ran the comparison.
- No independent reproduction was supplied.

Invalid draft:

```text
这款模型能让自动化任务提速 30%。
```

Valid draft:

```text
厂商在自有测试的 21 个可比任务中报告，平均单任务耗时为 2.35 分钟，较其对比模型快约 30%；本文没有独立复测。
```

Why the valid version works:

- keeps the vendor's material interest visible
- attaches the number to the measured task time and sample
- does not turn a first-party benchmark into independent proof
- states the missing independent reproduction instead of implying it

## Platform-Required AI Assistance Disclosure

Source facts:

- The target platform is 少数派.
- ChatGPT helped restructure the outline and rewrite several sections.
- The author manually checked every factual and technical claim.
- The author corrected two command descriptions.
- No exact model version or prompt was supplied.

Invalid disclosure:

```text
本文仅使用 AI 检查错别字。
```

Valid disclosure:

```text
说明：本文使用 ChatGPT 辅助整理结构并改写部分段落；事实和技术内容由作者逐项核对，并修正了两处命令说明。
```

Why the valid version works:

- names the actual technology
- describes the real extent of assistance
- records the author's verification and corrections
- does not invent a model version or prompt
- can be placed near the opening when current platform rules require it

## Human Habit Preservation

Source draft:

```text
这个方案能用——我也用了半年——但每次排错都要跨三个服务，我后来不想继续加了。
```

Bad mechanical rewrite:

```text
这个方案可以使用。我使用了半年。每次排错都需要跨三个服务，因此我决定不再继续扩展。
```

Better edit:

```text
这个方案能用，我也用了半年。但每次排错都要跨三个服务，后来我不想再往上加东西了。
```

The dash was not the real problem. The edit keeps the author's cadence and decision while making the sentence easier to read.

## Sparse Notes

Notes:

```text
- switched to SQLite
- deployment became simpler
```

Invalid draft:

```text
经过三个月的线上事故和大量用户反馈，我最终迁移到 SQLite，部署时间降低了 70%。
```

Valid draft:

```text
我后来把存储改成了 SQLite。对这个项目来说，最直接的变化是部署少了一个外部依赖。
```

The valid draft does not invent a timeline, incident, user feedback, or metric.
