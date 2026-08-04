---
name: dev-java
description: "Use when Java source or Java-owned Maven/Gradle configuration must be implemented, migrated, or refactored across Spring services, HTTP/security boundaries, persistence, transactions, messaging, scheduling, caches, tests, or configuration; owns source edits and validation, not non-Java JVM work, audit-only, fixed-basis review, or Git delivery."
---

# Java Implementation

## Overview

Implement Java changes against the repository's pinned JDK, build owner, framework
generation, module boundaries, security model, transaction semantics, and runtime
contracts. Treat reference projects such as RuoYi as comparative evidence, never as a
template that overrides current source.

## Workflow

1. Read effective repository guidance and run `git status --short` in the owning Git
   root before edits.
2. Resolve the owning Maven or Gradle build root, target module, executable or library
   role, effective JDK source, Wrapper, parent/BOM/platform, profiles, and
   repository-defined commands. Stop before source edits when the Git/build root,
   target module, or intended JDK contract cannot be resolved. When an existing
   authority conflict is the explicit task target and user intent or an approved
   contract establishes the intended authority, permit only the bounded changes needed
   to resolve that conflict. Record other missing build/runtime authorities as
   `Not verified` and do not make changes that depend on them.
3. Classify the project: compact service, modular monolith, multi-module application,
   shared library/SDK, batch or scheduler, CLI, or legacy platform application.
4. Read the approved behavior/specification when one exists. Confirm compatibility,
   affected modules and public seams, data/security impact, non-goals, and validation
   expectations.
   When runtime/configuration, packaging, API/integration, persistence, legacy
   replacement, auth/security, or cross-repository delivery signals apply, load
   [project grounding](references/project-grounding.md) and close each activated
   `signal -> invariant -> owner/authority -> evidence category and evidence ->
   verification state -> disposition -> next action and action owner` chain before
   edits. A spec, schema, and tests added with the implementation prove
   intent and selected behavior, not independent approval or migration safety.
5. Inspect only the relevant manifests, entry points, configuration ownership,
   routes/controllers, DTOs, application services, domain rules, repositories,
   entities/mappers, migrations, clients, security chain, tests, and analogous feature.
6. Start with **Baseline** and select every applicable overlay:
   - **Build/toolchain:** JDK, Maven/Gradle, Wrapper, parent/BOM/platform, annotation
     processing, generated sources, packaging, or dependency-resolution changes.
   - **Web/security:** Spring MVC/WebFlux, filters, interceptors, authentication,
     authorization, validation, upload/download, session, token, or API error contracts.
   - **Persistence/transaction:** JPA, JDBC, MyBatis, migrations, queries, locking,
     transaction propagation, after-commit behavior, or durable compatibility.
   - **Integration/runtime:** cache, Redis, messaging, scheduling, async execution,
     remote clients, retries, idempotency, shutdown, or observability.
   - **Migration/compatibility:** JDK, Spring Boot, `javax`/`jakarta`, database,
     framework, packaging, or language-port changes.
7. Load [Java engineering](references/java-engineering.md) for every task. Load
   [behavior-first](references/behavior-first.md) when a stable public seam supports a
   red-capable vertical slice. Load [codebase design](references/codebase-design.md)
   for public module/interface or testability changes, and [code quality](references/code-quality.md)
   only when duplication, dead code, coupling, or maintainability materially applies.
8. Decide in order: reuse, extend, adapt the nearest reference, or create new. Record
   why an existing controller, service, repository, DTO, mapper, event, client, or
   configuration owner cannot safely own a new declaration.
9. Trace the complete contract and dependency chain before editing. Keep one native
   API/schema authority; do not introduce OpenAPI, a new persistence abstraction, or a
   module framework merely because it appears in a reference project.
10. Implement the smallest coherent slice using local naming, dependency direction,
    exception, logging, transaction, security, configuration, and test conventions.
11. Update every affected manifest, registration, generated source, migration,
    configuration example, test, command, documentation, CI/deploy path, and consumer.
12. Capture tracked Worktree state before validation. Prefer check-only commands over
    apply/fix modes, run focused checks after each slice, then the repository Baseline
    and every selected overlay. Recheck status/diff afterward; classify expected task
    output, unexpected validation drift, and unrelated user changes without
    auto-reverting any of them. Do not substitute compilation for behavioral,
    database, authorization, concurrency, migration, or runtime evidence.

## Modes

- **Targeted implementation:** add or fix bounded Java behavior.
- **Structure alignment:** repair package/module/build ownership against an adopted contract.
- **Contract migration:** change an API, DTO, schema, event, or consumer boundary.
- **Platform migration:** preserve behavior across JDK, Spring, namespace, build, or database generations.
- **Implementation validation:** run repository-owned build, static, and test evidence
  for the edited Java surface; this is not an audit or readiness review.

## Hard Rules

- Use the repository-pinned JDK and build commands. Do not replace an old supported
  JDK, Wrapper, Gradle, Maven, Spring, or dependency set with the machine default.
- Do not copy RuoYi, Petclinic, Spring Modulith, or another project's directory tree,
  base classes, response wrappers, security chain, or dependencies into the target.
- Keep controllers and transport adapters thin when the current architecture provides
  an application/service owner; keep deterministic rules independent of IO where the
  established design supports it.
- Preserve deny-by-default authorization, route and method permission coverage,
  tenant/data-scope constraints, input validation, safe error mapping, and secret/log
  boundaries. Never weaken CSRF, CORS, authentication, or authorization without an
  explicit threat-modelled contract and matching tests.
- Make transaction ownership, propagation, rollback rules, remote-call boundaries,
  event timing, retries, and idempotency observable. Do not assume `@Transactional`
  works through self-invocation, private methods, or unmanaged instances.
- Do not expose persistence entities as public API DTOs merely for convenience. Keep
  mapping and validation at the existing boundary.
- Do not invent a repository/service/manager layer, generic base class, global
  singleton, event bus, cache, thread pool, or abstraction without a proven owner and
  consumer.
- Never put credentials, tokens, private keys, connection strings, or production
  identifiers in source, examples, tests, logs, or reports.
- Preserve unrelated changes. Do not stage, commit, push, or open a pull request;
  route Git mutation to `repo-delivery`.
- Do not hide a local startup workaround in a global entry point, tracked shared
  profile, or packaging rule without proving its intended environment boundary and
  target-runtime effect. A framework annotation or exclusion is a signal, not an
  automatic defect; decide from effective precedence, reachability, and contract.

## Validation Model

- **Baseline:** repository-defined format/static checks, compilation, and focused
  behavior tests using the owning Wrapper or documented build command.
- **Selected overlays:** add only the build, security, persistence, integration, and
  migration evidence required by the changed surface.
- **Runtime gaps:** private artifact access, containers, databases, brokers,
  configuration centers, external services, unsupported JDKs, or missing Wrappers are
  explicit `Not verified` gaps, never simulated success. When vendor database or
  migration semantics are essential and only an in-memory substitute is available,
  implementation may continue only within the resolved source contract, but completion
  and release readiness remain `Not verified`.

## Do Not Use For

- First-pass Java build/dependency mapping; use `repo-map`.
- Diagnosis-only work with no authorized source change; use the host diagnosis flow.
- A bounded read-only Java/Spring audit; use `audit-java`.
- Worktree/index or immutable change-basis review; use `repo-review`.
- Security-only repository scanning or exploit validation; use an available security workflow.
- Git staging, commit, push, integration, or cleanup; use `repo-delivery`.

## Output Contract

Report scope, Git/build root, project class, JDK/build/framework evidence, selected
overlays, reuse/new decision, changed contract chain, security and transaction impact,
Baseline/overlay validation, before/after Worktree state, and exact gaps. For each
overlay, report applicability as `Affected` or `Not applicable`, then report evidence
status separately as `Verified`, `Failed`, or `Not verified`. Use `Not found`
only for a searched-for repository fact that is absent.

## References

- See [usage](references/usage.md) for triggers and boundaries.
- See [checklist](references/checklist.md) for implementation and validation gates.
- Read [Java engineering](references/java-engineering.md) for secure design, build,
  Spring, persistence, integration, testing, and comparative open-source lessons.
- Read [behavior-first](references/behavior-first.md) when a stable public seam exists.
- Read [codebase design](references/codebase-design.md) for public design/testability changes.
- Read [code quality](references/code-quality.md) for material maintainability work.
- Read [project grounding](references/project-grounding.md) when a change activates
  runtime/config, packaging, public contract, durable data, replacement,
  auth/security, or cross-repository risks.
- See [eval cases](references/eval-cases.md) for routing and quality scenarios.
