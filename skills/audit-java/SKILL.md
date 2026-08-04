---
name: audit-java
description: "Use when a known Java source surface or Java-owned Spring/build configuration needs a scoped, read-only audit of selected architecture, API/security, transaction, persistence, concurrency, integration, performance, or migration risks; not for non-Java JVM semantics, and use repo-review when a Worktree or immutable change basis needs coordination."
---

# Java Audit

## Overview

Audit Java engineering from current repository evidence with explicitly selected risk
profiles. Use open-source projects and framework guidance to form questions, not to
declare target-repository defects by stylistic comparison.

## Rule Priority

Apply current user intent, effective repository guidance, manifests/source/tests,
project contracts, this Skill, then external references. A reference architecture
never outranks a working local contract.

## Workflow

1. Record the Git/build root, revision and relevant Worktree state; read effective
   guidance and inspect only the selected manifests, source, tests, migrations,
   configuration ownership, CI, and runtime documentation.
2. Resolve the JDK, Maven/Gradle owner, Wrapper, parent/BOM/platform, modules,
   packaging, framework generation, executable entries, profiles, and quality commands.
3. Select one or more audit profiles:
   - **Build/architecture:** dependency direction, modules/packages, public/internal
     seams, build reproducibility, dependency authority, generated code, and lifecycle.
   - **API/security:** routes, DTO validation, filters/interceptors, authentication,
     authorization/data scope, sessions/tokens, CSRF/CORS, upload/download, errors,
     secrets, and sensitive logging.
   - **Persistence/transaction:** mappings, query shape, pagination, N+1 risk,
     locking, migrations, transaction boundaries/propagation, after-commit effects,
     and database compatibility.
   - **Concurrency/integration:** executors, async/events, Redis/cache, messages,
     schedules, retries, idempotency, backpressure, distributed locks, and shutdown.
   - **Performance/operations:** representative workload, database plans, pools,
     allocation/serialization, caches, remote calls, metrics, health, and failure modes.
   - **Migration/compatibility:** JDK, Spring Boot, `javax`/`jakarta`, build tool,
     dependency, database, packaging, or configuration-generation transitions.
   Activate [project grounding](references/project-grounding.md) only for semantic
   signals involving runtime/config precedence, packaged artifacts, public contracts,
   durable data, legacy replacement, auth/security, or cross-repository delivery.
   Use the grounding chain to bound adjacent evidence; do not scan every profile or
   repository merely because corresponding files exist.
4. Load [Java engineering](references/java-engineering.md) for every audit. Load
   [codebase design](references/codebase-design.md) for module/API/testability analysis
   and [code quality](references/code-quality.md) only when maintainability is in scope.
5. Consume a current `repo-map` or reproduce a bounded inventory of entries, callers,
   permissions, services, repositories, entities/mappers, migrations, configuration,
   jobs/listeners, and tests. A missing map entry never proves missing code.
6. Trace each candidate issue through trigger, reachable path, owner, state or data
   consequence, counterevidence, and a falsifiable validation seam. Reject checklist-only
   findings and style preferences without concrete impact.
7. Capture tracked Worktree state before validation. Do not run known apply/fix or
   tracked-source generation commands in the audited Worktree. If the repository offers
   only write-capable validation, skip it and report the gap or hand it to a workflow
   with an isolated Worktree. Prefer check-only repository commands and representative
   data. With explicit authorization,
   use only test-owned ephemeral containers, databases, brokers, or processes; never
   write shared, staging, or production state. Recheck status/diff afterward. If an
   otherwise non-mutating command creates tracked drift, stop validation, report the
   exact contamination, mark affected evidence `Not verified`, and do not revert it
   without explicit authorization. Clean up only task-created runtime resources.
   Compilation alone does not prove authorization, rollback, migration, query,
   concurrency, or runtime behavior.
8. Stop when the selected profiles are supported or explicitly blocked. Mark all
   other profiles out of scope.

## Modes

- **Focused profile audit:** one or two bounded Java risk surfaces.
- **Combined risk audit:** interacting profiles such as transaction plus async events.
- **Baseline audit:** build, architecture, tests, documentation, and legacy exceptions.
- **Scoped specialist subreview:** Java evidence delegated by `repo-review` for a fixed basis.

## Hard Rules

- Resolve effective build/runtime facts from repository evidence, not machine defaults,
  framework convention, or a reference project's structure. Treat annotations,
  dependencies, scanner matches, and code shape as signals: prove ownership,
  reachability, impact, and counterevidence, and redact sensitive values.
- Treat source configuration, packaged configuration, and effective runtime as
  separate evidence. A local boot or compilation cannot clear a target-profile,
  service-registration, migration, or external-integration gap.
- Apply authorization, transaction, integration, and persistence conclusions through
  the selected Java engineering profile and require their matching negative/runtime
  evidence before claiming consistency.
- Do not claim dependency vulnerability, exploitability, secret exposure, or complete
  security coverage without the matching evidence. Route explicit vulnerability scans,
  attack-path analysis, or PoC validation to an available security workflow.
- Remain Git/source read-only: do not edit tracked source, stage, commit, push, or post
  comments. Runtime validation is static by default; explicitly authorized test-owned
  ephemeral state is permitted only under Workflow step 7.

## Do Not Use For

- Repository/build orientation without a Java audit; use `repo-map`.
- Java implementation, refactoring, or migration; use `dev-java`.
- Root-cause diagnosis of one concrete failure; use the host diagnosis flow.
- Non-Java language semantics in Kotlin, Groovy, Scala, or other JVM source; use a
  language-capable workflow. A bounded Spring framework/configuration audit may proceed
  only when language-specific risks are explicitly excluded.
- Worktree/index or immutable change readiness; use `repo-review`.
- Git or external publication actions; use their owning workflows.

## Output Contract

Lead with severity-ranked findings, each with impact, exact location, evidence chain,
counterevidence, remediation direction, and validation seam. Then report scope/basis,
JDK/build/framework facts, before/after Worktree state, commands and ephemeral resources,
and cleanup. For each profile, report applicability as `Applicable` or
`Not applicable`, then report evidence status separately as `Verified`, `Failed`,
or `Not verified`. Use `Not found` only for a searched-for repository fact that is
absent. In specialist mode return evidence to `repo-review` without issuing the final
readiness verdict.

## References

- See [usage](references/usage.md) for triggers and profile selection.
- See [checklist](references/checklist.md) for evidence and reporting gates.
- Read [Java engineering](references/java-engineering.md) for secure design, build,
  Spring, persistence, integration, testing, and comparative open-source lessons.
- Read [codebase design](references/codebase-design.md) for module/API/testability audits.
- Read [code quality](references/code-quality.md) for material maintainability audits.
- Read [project grounding](references/project-grounding.md) when the selected audit
  activates runtime/config, packaging, public contract, durable data, replacement,
  auth/security, or cross-repository risks.
- See [eval cases](references/eval-cases.md) for routing and finding-quality scenarios.
