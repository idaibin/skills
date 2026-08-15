# Java Implementation Eval Cases

## Trigger Eval

| Request | Expected behavior |
| --- | --- |
| `Implement this Spring service transaction and tests.` | Trigger `dev-java`; resolve build/JDK and select Persistence/transaction. |
| `Make this Spring service's local startup work by changing service discovery and packaged profile behavior; production must remain registered.` | Trigger Runtime/config grounding, resolve precedence and artifact/target boundaries, and block a global workaround until its scope is proven. |

## Non-Trigger Eval

| Request | Expected behavior |
| --- | --- |
| `Map every Maven module and private dependency.` | Route to `repo-map`; do not edit source. |
| `Audit the current Java service without changes.` | Route to `audit-java`. |
| `Review and commit this Java Worktree.` | Route fixed-basis review to `repo-review`, then authorized Git mutation to `repo-delivery`. |
| `Implement this Kotlin service in a mixed JVM monorepo.` | Do not trigger from JVM/build-tool proximity alone; route to a Kotlin-capable owner. |
| `Change only a Java comment; no behavior, build, config, or contract changes.` | Keep project-grounding risk classes `Not applicable`; do not run environment or migration checks. |

## Quality Eval

| Case | Pass | Fail |
| --- | --- | --- |
| Validation proportionality | Starts with the owning module's focused compile/test seam, adds only affected consumers and selected overlays, and reserves full multi-module/release gates for final lifecycle stages, explicit requests, or missing credible focused coverage. | Runs every module by default for a bounded Java edit, or calls a focused pass release proof. |
| Legacy toolchain | Uses the pinned Java 8/Gradle Wrapper and preserves legacy configurations. | Runs the machine's latest JDK/Gradle or performs an unrelated upgrade. |
| Reference project | Uses RuoYi/Spring projects as questions and adopts only target-proven patterns. | Copies RuoYi modules, wrappers, JWT/CSRF decisions, or dependencies by default. |
| Security boundary | Traces route and method authorization, data scope, credentials, validation, errors, and negative tests. | Treats authentication or hidden UI as complete authorization. |
| Transaction behavior | Verifies proxy, rollback, async/remote, after-commit, retry, and idempotency semantics. | Adds `@Transactional` and assumes consistency. |
| Test strategy | Uses unit/slice/integration/real-service evidence according to risk. | Claims runtime correctness from compilation or coverage alone. |
| Missing infrastructure | Reports private artifacts, JDK, Wrapper, Docker, database, broker, or config center as `Not verified`. | Simulates a successful build or integration. |
| Unresolved authority | Stops when Git/build root, authorized target module, or intended JDK contract cannot be resolved. | Picks a convenient module or machine JDK and edits anyway. |
| Authority repair | When the task explicitly resolves conflicting toolchain authorities and the intended target is approved, edits only the bounded authority files. | Treats every existing conflict as an unconditional blocker or broadens into an unrelated upgrade. |
| Validation drift | Captures before/after tracked state and separates generated task output, unexpected command drift, and unrelated work. | Runs an apply-mode formatter and silently absorbs or reverts resulting files. |
| Reactive boundary | Checks blocking calls, Reactor Context, transaction model, demand/cancellation, retry, and cleanup for an affected WebFlux path. | Treats MVC thread-local and transaction assumptions as valid in Reactor. |
| Thread context | Propagates only required context and restores or removes manually managed ThreadLocal/MDC state in a finally path. | Leaves tenant/security context attached to pooled threads. |

## Edge Cases

- A Spring Boot 2 to 3 migration inventories `javax`/`jakarta`, Hibernate, validation,
  security configuration, serialization, generated code, tests, and deployment runtime.
- A cache-only change that also updates durable state selects both Integration/runtime
  and Persistence/transaction.
- A security-sensitive source fix remains `dev-java`; an explicit vulnerability scan
  remains owned by the security workflow.
- PostgreSQL/MySQL-specific persistence changed with only H2 available may proceed as a
  scoped source edit, but database behavior and release readiness remain `Not verified`.
- An affected Security overlay with unavailable negative tests reports applicability
  `Affected` and evidence status `Not verified`, rather than collapsing them.
