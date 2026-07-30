# Java Audit Usage

## Best For

- Read-only Java/Spring build and architecture assessment.
- Bounded API, authentication, authorization, validation, or sensitive-log audits.
- Transaction, JPA/JDBC/MyBatis, migration, query, locking, or consistency audits.
- Redis/cache, messaging, scheduling, async, retry, idempotency, or shutdown audits.
- JDK/Spring/build/database migration-readiness audits.

## Trigger Examples

- `Audit this Spring service's transaction and cache consistency risks.`
- `Review current route and method authorization coverage without editing.`
- `Audit Maven/Gradle toolchain reproducibility and private dependency risks.`
- `Assess this JPA query path for N+1, pagination, locking, and dialect risks.`
- `Audit this scheduler and Redis consumer for retries, idempotency, and shutdown.`

## Non-Triggers

- Repository Java orientation with no audit question; use `repo-map`.
- Implementing a confirmed fix; use `dev-java`.
- Diagnosing one failing command before a cause is established; use the host diagnosis flow.
- Reviewing a Worktree/commit for readiness; use `repo-review`.
- A vulnerability scan, exploit path, or PoC request; use a security workflow.
- Kotlin/Groovy/Scala language-semantics review; use a language-capable workflow. This
  Skill may audit only explicitly bounded Java-owned Spring/build configuration.

## Profile Selection

Select only profiles supported by the request and evidence. Combine profiles when the
invariant crosses them, such as transaction plus async event delivery or authorization
plus tenant-filtered persistence. List all unselected profiles as out of scope.

## Output

Lead with evidence-ranked findings, not a technology checklist. A missing annotation,
interface, test tool, module framework, or RuoYi-style component is not a finding until
its reachable consequence and target-owned requirement are proven.
