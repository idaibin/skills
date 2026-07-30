# Java Implementation Usage

## Best For

- Implementing or refactoring Java/Spring application behavior.
- Changing Maven/Gradle modules, dependencies, plugins, annotation processors, or packaging.
- Adding or changing controllers, DTOs, services, repositories, mappings, jobs, listeners, or clients.
- Modifying authentication, authorization, validation, transaction, migration, cache,
  messaging, scheduling, async, or configuration behavior.
- Migrating JDK, Spring Boot, `javax`/`jakarta`, persistence, database, or build generations.
- Removing Java declarations while closing registrations, consumers, tests, docs, and build references.

## Trigger Examples

- `Implement this Spring Boot endpoint and preserve the existing DTO/error contract.`
- `Add this Java 8 Gradle feature without upgrading the pinned platform.`
- `Fix the transaction and after-commit event behavior, including rollback tests.`
- `Migrate this service from Spring Boot 2 to 3 and account for javax/jakarta compatibility.`
- `Add Redis idempotency to this consumer and prove retry and expiry behavior.`
- `Refactor this Maven module boundary without changing external API behavior.`

## Non-Triggers

- `Map all Maven/Gradle roots and dependencies.` Use `repo-map`.
- `Why did this one test start failing?` Use the host diagnosis flow until a fix is authorized.
- `Audit current Spring Security and transaction risks without edits.` Use `audit-java`.
- `Review this Worktree or commit.` Use `repo-review`.
- `Implement this Kotlin/Scala/Groovy service.` Use the matching host capability; this
  Skill does not claim non-Java JVM language ownership.
- `Scan the repository for exploitable vulnerabilities.` Use a security workflow.
- `Commit and push these changes.` Use `repo-delivery` after review.

## Overlay Examples

- Private pure-Java rule: Baseline only.
- Controller/DTO change: Baseline + Web/security when trust or authorization changes.
- JPA migration: Baseline + Persistence/transaction.
- Redis consumer: Baseline + Integration/runtime; add Persistence when durable state changes.
- Spring Boot 2 to 3: Baseline + Migration/compatibility plus every affected domain overlay.
- Build plugin only: Baseline + Build/toolchain.

## Output

Use `SKILL.md`'s implementation report. Do not claim successful build, database,
authorization, container, private-repository, or runtime verification when the owning
toolchain or dependency was unavailable.
