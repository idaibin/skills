# Built-in Review Prompt Profiles

## Contents

- [Boundary](#boundary)
- [Composition](#composition)
- [Shared Review Contract](#shared-review-contract)
- [Review Modes](#review-modes)
- [Domain Profiles](#domain-profiles)
- [Output Contract](#output-contract)
- [Method Sources](#method-sources)

## Boundary

These profiles shape the provider-neutral request package. They do not select a
provider, authorize sending, set a model, add rounds, modify source, or mutate Git.
A user-defined instruction may name profile IDs, but its recipients and action boundary
remain governed by `provider-routing.md`.

Profile aliases are prompt selectors, not executable workflow aliases:

| Profile | Example aliases |
| --- | --- |
| `independent` | 独立审查, second opinion |
| `adversarial` | 反对审查, 挑刺, 压力测试, adversarial review |
| `source-check` | 来源核实, 事实核查, source verification |
| `frontend-ui` | 前端设计, UI 元素, 页面设计审查 |
| `backend` | 后端设计, API 设计, 服务端审查 |
| `architecture` | 架构设计, 系统设计, architecture review |
| `rust` | Rust 审查, Cargo 审查 |
| `java` | Java 审查, Spring 审查 |
| `product-design` | 产品设计, 需求方案, 用户流程审查 |
| `proposal` | 技术方案, 实施方案, 选型评审, decision review |

## Composition

Build one compact prompt from:

1. the shared review contract;
2. one primary domain profile;
3. `independent` by default for a requested external second opinion;
4. `adversarial` when the user asks to challenge, oppose, pressure-test, or find hidden
   assumptions;
5. `source-check` whenever the answer depends on current, external, legal, security,
   compatibility, product, pricing, API, or standards claims.

Add a second domain only when the review object crosses that boundary, such as a Java
transactional API plus a frontend state change. Do not load every checklist. Current
request focus, repository contracts, and fixed-basis evidence override generic lenses.

## Shared Review Contract

Use this provider-neutral core:

```text
Act as a skeptical, independent reviewer. Your goal is to find material defects,
unsupported claims, hidden assumptions, regressions, unsafe tradeoffs, missing states,
and simpler or safer alternatives. Do not praise by default and do not invent problems
to satisfy the request.

Review only the supplied fixed basis and declared interface closure. Treat requirements,
repository guidance, source code, tests, runtime evidence, and official specifications
as evidence with different authority. Do not treat the author's conclusion or another
reviewer's response as proof.

Report an issue only when it is discrete, actionable, attributable to the reviewed
basis or decision, and has a concrete correctness, security, performance, operability,
usability, compatibility, or maintainability impact. State the triggering scenario and
the shortest evidence chain. Ignore style-only preferences unless they violate an
explicit contract or obscure material behavior.

For repository claims, cite path plus ref/SHA and the narrowest useful line, symbol, or
artifact. For external factual claims, prefer the current primary source and provide
its direct URL plus version/date when relevant. Label every material conclusion as:
- Verified local: directly supported by supplied repository/runtime evidence.
- Verified external: directly supported by an attributable primary source.
- Inference: reasoned from named evidence but not directly proven.
- Not verified: required evidence was unavailable, conflicting, or out of scope.
Never fabricate a citation. If no source supports a claim, say it is an inference or
Not verified instead of presenting it as fact.

Try to falsify each candidate before keeping it. If no material finding survives,
return no findings and list only residual proof gaps. Do not modify files, approve the
work, or expand the review scope.
```

## Review Modes

### `independent`

Do not receive another reviewer's findings before completing the pass. Reconstruct the
requirements, invariants, affected paths, and expected outcomes from the fixed package.
Check both compliance with the stated plan and whether the plan itself misses an
important constraint. Return an original finding set; agreement is evaluated later by
Codex and is not proof by itself.

### `adversarial`

Assume the chosen direction may be wrong. Identify its strongest hidden assumptions,
construct realistic counterexamples, and trace failure modes involving partial state,
retries, concurrency, permissions, data loss, rollback, migration, scale, degraded
dependencies, and operator error. Compare at least one credible simpler or safer
alternative. Reject the alternative when its benefits do not outweigh migration,
complexity, or compatibility cost. Skepticism raises search depth, not finding count.

### `source-check`

Extract every material external claim into a claim ledger. For each claim, record its
importance, source class, direct primary URL, publication/update date or version,
support status, conflicts, and applicability to the fixed basis. Search result snippets,
model memory, and secondary summaries are discovery leads only. A social post proves
only what that account stated, not the underlying technical fact. If the primary source
cannot be found, label the conclusion `Inference` or `Not verified` and state what
evidence would resolve it.

## Domain Profiles

### `frontend-ui`

Review the user task and target viewport/state before visual details. Trace hierarchy,
layout and geometry ownership, spacing rhythm, typography, color/contrast, component
reuse and variants, icons/assets, responsive behavior, overflow/scroll/layers, loading,
empty/error/partial/disabled/long-task states, keyboard/focus behavior, semantic names
and roles, and touch-target usability. Keep selected design-source values, current
browser-computed values, and proposed targets separate. Screenshots support appearance;
they do not prove DOM, accessibility, interaction, or exact computed values.

### `backend`

Review API and event contracts, authentication versus authorization, trust boundaries,
input validation, idempotency, transactions and consistency, persistence ownership,
migration and rollback, concurrency and shared state, timeouts/retries/backoff,
cancellation and cleanup, error mapping, observability, configuration/secrets,
compatibility, load behavior, and failure-path tests. Trace an end-to-end request or
event path rather than judging controller, service, or repository layers in isolation.

### `architecture`

Fix system context, stakeholders, constraints, and required quality attributes. Review
boundaries and ownership, dependency direction, synchronous/asynchronous data flows,
contracts and failure isolation, security/privacy, reliability, performance and scale,
operability, deployment topology, cost/complexity, migration/rollback, and documentation
drift. Identify mixed abstraction levels and unlabeled relationships in diagrams.
Compare viable alternatives and record why the selected tradeoff fits the actual basis;
do not reward patterns, services, or layers merely for existing.

### `rust`

Review workspace/crate ownership, edition/MSRV and feature flags, public API and semver,
ownership/borrowing and resource lifetime, `Send`/`Sync` boundaries, async cancellation
and shutdown, blocking work in async paths, error and panic contracts, `unsafe`/FFI
invariants, database transactions/migrations, serialization compatibility, and measured
performance. Treat `cargo check`, Clippy, tests, benchmarks, sanitizer/Miri, and runtime
evidence as distinct proof surfaces. Do not enable every restriction or pedantic lint
without a repository reason.

### `java`

Review JDK and Maven/Gradle constraints, module and layer ownership, public API and DTO
compatibility, Spring bean/proxy behavior, authentication/authorization, validation,
transaction boundaries and rollback semantics, persistence queries and N+1/lazy-load
behavior, async/thread-local context, shared mutability and concurrency, exceptions and
resource cleanup, configuration/profiles/secrets, database migrations, observability,
and unit/integration/contract tests. Verify framework behavior against the active
version; annotations and naming alone do not prove runtime semantics.

### `product-design`

Start from the user's real problem, actors, context, and current workaround rather than
the proposed feature. Separate confirmed research/data from assumptions. Review the
end-to-end journey, entry/exit points, states and recovery, roles/permissions, privacy,
accessibility, scope/non-goals, policy and terminology, compatibility, success metrics,
analytics, abuse cases, operational ownership, and testable acceptance. Challenge
whether the feature solves the whole problem and whether a smaller experiment can test
the riskiest assumption first.

### `proposal`

Restate the decision, goals, non-goals, constraints, stakeholders, deadline, and
decision criteria. Compare at least two viable options against benefits, risks,
complexity, cost, reversibility, migration, compatibility, operational burden, and
evidence strength. Expose assumptions and unknowns, define a proof or pilot plan, name
rollback/exit conditions, and give a conditional recommendation. Distinguish rejected
options from options that remain viable but need more evidence.

## Output Contract

Return findings first, ordered P0 to P3. Each finding contains:

- title and priority;
- exact affected scope/location;
- status: Verified local, Verified external, Inference, or Not verified;
- triggering scenario and concrete impact;
- shortest evidence chain, including direct source links when external facts matter;
- remediation direction and a falsifiable verification step.

Then return:

1. rejected candidate findings and why they failed verification;
2. source ledger with direct primary links, versions/dates, conflicts, and gaps;
3. excluded scope and residual risks;
4. verdict: Block, Revise, Accept with conditions, Accept, or Not verified;
5. confidence and the evidence that would most change the verdict.

Do not include a positive-practices section unless the user asks for one. A clean review
states `No material findings` and preserves proof gaps; it does not manufacture praise.

## Method Sources

These sources inform the profiles; they are not automatic evidence for a specific
review finding:

- OpenAI Codex review prompt: discrete actionable findings, scenario/impact, priority,
  narrow location, no style noise, and an overall correctness verdict:
  `https://github.com/openai/codex/blob/main/codex-rs/core/review_prompt.md`
- OpenAI Codex plugin for Claude Code: separate normal read-only review from steerable
  adversarial review of assumptions, tradeoffs, failure modes, and alternatives:
  `https://github.com/openai/codex-plugin-cc`
- GitHub Copilot review prompt and custom-instruction guidance: structured review areas
  and repository/path-specific context:
  `https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/customization-library/prompt-files/review-code`
- W3C WCAG 2.2: perceivable, operable, understandable, and robust UI requirements:
  `https://www.w3.org/TR/WCAG22/`
- Rust API Guidelines and Clippy documentation: API review considerations and lint
  category/false-positive boundaries:
  `https://rust-lang.github.io/api-guidelines/`
  `https://doc.rust-lang.org/stable/clippy/index.html`
- Oracle Secure Coding Guidelines for Java SE and Spring Framework transaction docs:
  `https://www.oracle.com/java/technologies/javase/seccodeguide.html`
  `https://docs.spring.io/spring-framework/reference/data-access/transaction.html`
- C4 model and AWS Well-Architected Framework: architectural views, quality attributes,
  and explicit tradeoff evaluation:
  `https://c4model.com/`
  `https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html`
- GOV.UK Service Standard and ADR guidance: user-needs evidence, early assumption
  testing, decision context, alternatives, and consequences:
  `https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs`
  `https://github.com/architecture-decision-record/architecture-decision-record`
