# Java Engineering Protocol

## Contents

- [Evidence And Reference Priority](#evidence-and-reference-priority)
- [Development Philosophy](#development-philosophy)
- [Build And Compatibility](#build-and-compatibility)
- [Code And Module Design](#code-and-module-design)
- [Web And Security](#web-and-security)
- [Transactions And Persistence](#transactions-and-persistence)
- [Concurrency And Integration](#concurrency-and-integration)
- [Testing And Verification](#testing-and-verification)
- [Comparative Open-Source Lessons](#comparative-open-source-lessons)
- [Source References](#source-references)

## Evidence And Reference Priority

Use this order:

1. current user intent and effective repository instructions;
2. owning build manifests, source, tests, migrations, configuration schema, and CI;
3. current project contracts and documented legacy exceptions;
4. official JDK, build-tool, Spring, database, and security documentation matching the
   repository's actual versions;
5. fixed open-source reference snapshots and coding guidelines.

A reference project supplies questions and candidate patterns. It does not prove that
the target needs the same modules, libraries, annotations, base classes, response
shape, authentication scheme, or directory layout. Prefer an existing target pattern
when it is coherent and verified; migrate only for an explicit requirement or proven
failure.

## Development Philosophy

- Deliver one observable vertical behavior at a time: boundary, application workflow,
  domain rule, persistence/integration adapter, and verification. Avoid horizontal
  framework scaffolding with no completed consumer path.
- Make policy explicit at the narrowest stable owner: business decisions in domain or
  application code, transport conversion at the web boundary, persistence mechanics in
  repositories/mappers, and infrastructure failure handling in adapters.
- Prefer simple modules with explicit APIs and inward dependency direction. Introduce a
  framework, interface, event, or abstraction only when it enforces a current invariant
  or serves a real replacement/test/consumer need.
- Keep compatibility intentional. A legacy Java 8/Spring Boot 2 service may require a
  different correct solution from a Java 17+/Spring Boot 3/4 service.
- Treat tests, migrations, configuration, observability, shutdown, and rollback as part
  of the feature, not post-implementation decoration.

## Build And Compatibility

- Resolve the owning `pom.xml`, `settings.gradle[.kts]`, `build.gradle[.kts]`, Wrapper,
  parent/BOM/platform, module graph, profiles, toolchains, annotation processors,
  generated sources, packaging tasks, and CI command before changing dependencies.
- Use repository-owned Wrappers when complete. A globally installed newer JDK, Maven,
  or Gradle does not override the pinned project toolchain.
- Preserve Maven scopes and Gradle configurations according to the pinned build
  generation. Do not mechanically modernize legacy `compile`/`runtime` declarations in
  an unrelated task.
- Treat private repositories, local JARs, plugins, BOMs, and transitive exclusions as
  architecture inputs. A declared dependency proves an edge, not successful resolution
  or runtime use.
- For JDK, Spring Boot, Hibernate, or `javax` to `jakarta` migration, inventory source,
  generated code, serialization, validation, persistence, security configuration,
  tests, deployment runtime, and external consumers before bulk replacement.

## Code And Module Design

- Identify executable/bootstrap, web/API, application workflow, domain, persistence,
  integration, shared library, and test-fixture roles from current source—not names.
- Keep controllers, filters, listeners, scheduled jobs, and command runners focused on
  boundary work. Place orchestration in the established application/service owner and
  keep deterministic rules independent of infrastructure where the project supports it.
- Expose explicit module APIs and keep internals private by convention or verification.
  Avoid cycles and deep cross-module access. Use ArchUnit or Spring Modulith only when
  adopted or explicitly requested; the invariant matters more than the tool.
- Use composition and concrete local types by default. Add interfaces at real
  integration, replacement, public module, or test seams—not one per class.
- Keep DTOs, domain models, persistence entities, configuration properties, and wire
  formats distinct when they have different validation, lifecycle, compatibility, or
  visibility requirements.
- Exceptions must retain actionable context without leaking secrets. Map transport
  errors centrally when the project has an error contract; do not turn every exception
  into HTTP 200 or silently catch and continue.

## Web And Security

- Inventory every route, filter/interceptor chain, method authorization rule, data or
  tenant scope, anonymous exception, and negative test before changing access control.
- Default to least privilege. Authentication proves identity; authorization separately
  proves operation, resource, tenant, and data-scope access. UI hiding is not authorization.
- Choose session, bearer token, API signature, OAuth/OIDC, or other credentials from the
  real trust model. Define issuance, storage, rotation, expiry, revocation, replay,
  logout, clock-skew, and failure behavior.
- Keep Spring Security defaults unless the application model justifies a change. In
  particular, disabling CSRF is a decision tied to credential transport and browser
  behavior, not a universal requirement for JSON APIs. Verify CORS separately.
- Validate and normalize at trust boundaries. Apply allowlists and bounded sizes to IDs,
  filenames, paths, URLs, uploads, pagination, search, and serialized content. Use
  parameterized queries and safe object mapping; prevent mass assignment and insecure
  direct-object access.
- Treat deserialization as code-execution and data-integrity risk: do not enable broad
  polymorphic/default typing for untrusted input, including unconstrained Jackson
  `enableDefaultTyping` / `activateDefaultTyping` or Fastjson AutoType. Allowlist
  concrete types when polymorphism is required, and bound object depth, collection size,
  and parser features.
- Store passwords with current adaptive one-way encoders supported by the repository.
  Never log credentials, tokens, session IDs, authorization headers, private keys,
  sensitive request bodies, or raw exception payloads.
- Keep secrets in the repository's external configuration/secret owner. Examples and
  tests use unmistakable non-secret placeholders. Scan changed configuration and history
  separately when exposure is suspected.
- Rate limits, idempotency keys, replay protection, audit logs, and account lockout must
  define key scope, atomicity, TTL/window, concurrency behavior, and operational recovery.

## Transactions And Persistence

- Put a transaction around one consistency boundary, usually an application workflow.
  Record propagation, isolation, read-only intent, rollback rules, timeout, locking, and
  retry behavior when they affect correctness.
- Verify Spring proxy semantics: self-invocation, private/final methods, unmanaged
  objects, checked exceptions, async hops, and remote calls can invalidate assumed
  transaction behavior.
- Avoid holding database transactions across slow remote calls. For effects that must
  follow commit, use the repository's after-commit event/outbox/reconciliation design
  and define duplicate, retry, ordering, and failure handling.
- Treat migrations as versioned compatibility contracts. Validate forward migration,
  existing data, indexes/constraints, rollback or recovery policy, repeatability, and
  target database dialect. ORM schema generation is not a production migration plan.
- Inspect generated SQL or query plans for data-sensitive paths. Bound pagination,
  prevent N+1 and unbounded loads, preserve tenant filters, and make optimistic or
  pessimistic locking decisions explicit.
- Never use an in-memory test database as sole proof of behavior that depends on MySQL,
  OceanBase, PostgreSQL, Oracle, Dameng, or another production dialect.

## Concurrency And Integration

- Give every executor, scheduler, consumer, listener, cache, distributed lock, and
  client a named owner, bounded capacity, timeout, overload behavior, observability,
  and shutdown path.
- Define message and job idempotency, ordering, retry/backoff, poison/dead-letter,
  redelivery, checkpoint, and transaction interaction. A retry must not multiply
  non-idempotent effects.
- Align distributed-lock keys and TTLs with the protected business invariant and durable
  uniqueness constraints. Define lease expiry and recovery; a lock alone is not data integrity.
- Define cache key scope, serialization compatibility, TTL, invalidation, stampede
  behavior, source of truth, and degraded-mode semantics. Do not hide stale or partial
  state behind silent fallbacks.
- Propagate correlation and security context deliberately across async boundaries. For
  manually managed `ThreadLocal` or MDC state in filters, interceptors, executors, or
  async tasks, restore or `remove()` it in a `finally` path so pooled threads cannot
  leak tenant/security context; avoid unbounded global singleton managers.
- For WebFlux/Reactor paths, keep blocking calls off event-loop threads, propagate
  security/tracing state through Reactor Context rather than incidental thread locals,
  and verify the actual reactive transaction mechanism. Define demand/backpressure,
  cancellation cleanup, timeout, retry/re-subscription, and resource lifetime semantics;
  do not reuse Spring MVC thread-per-request assumptions.

## Testing And Verification

- Start with a red-capable check at the narrowest public seam that proves the requested
  behavior. Use plain unit tests for deterministic rules, Spring slices for one boundary,
  and full-context/integration tests only when component interaction is the subject.
- Test positive and negative authorization, validation, error mapping, rollback,
  duplicate/retry behavior, cache invalidation, concurrency invariants, migrations, and
  shutdown according to the selected risk.
- Use Testcontainers or repository-supported real services when vendor behavior matters.
  Make missing Docker, private artifacts, profiles, or infrastructure an explicit gap.
- Coverage is a signal, not proof. Do not lower gates, disable tests, over-mock the
  behavior owner, or replace assertions with smoke checks to make a build green.
- Run focused tests first, then repository baseline commands and risk-specific checks.
  Record exact commands, environment boundaries, failures, and skipped evidence.

## Comparative Open-Source Lessons

The fixed RuoYi-Vue snapshot demonstrates a Maven aggregator with explicit application,
framework, system, scheduler, generator, and common modules; centralized Spring Security
configuration; route/method permissions; data-scope handling; transactional scheduler
updates; Redis-backed behavior; bounded executors; and shutdown coordination. Use these
as prompts to inspect equivalent ownership and lifecycle in the target. Do not inherit
RuoYi's JWT, CSRF, MyBatis, base-controller, response-wrapper, utility, generator, or
module decisions without target-specific proof.

The fixed Spring Petclinic snapshot demonstrates Wrapper-owned Maven/Gradle commands,
JDK enforcement, formatting/static gates, focused MVC/JPA tests, full-context tests, and
real-database integration through containers. Copy neither its domain nor package tree;
reuse the principle of risk-matched, executable validation.

Spring Modulith demonstrates explicit module APIs, acyclic dependency verification, and
module-scoped integration tests. Apply the design questions without adding the library
unless the target adopts it.

OWASP Java guidance and Spring Security documentation define security questions and
framework semantics. Alibaba Java Coding Guidelines provide maintainability, exception,
logging, concurrency, MySQL, and security review prompts. Project evidence still decides
which rules are applicable and whether a deviation is a defect or documented exception.

## Source References

- [RuoYi-Vue fixed source snapshot](https://github.com/yangzongzhuan/RuoYi-Vue/tree/41720e624c5a668c7d3777835e4c87095a7a1dfd)
- [Spring Petclinic fixed source snapshot](https://github.com/spring-projects/spring-petclinic/tree/f182358d02e4a68e52bdbabf55ca7800288511e7)
- [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Spring Modulith verification](https://docs.spring.io/spring-modulith/reference/verification.html)
- [Spring Boot application testing](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)
- [Spring transaction management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)
- [Spring Security password storage](https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html)
- [Spring Security CSRF guidance](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html)
- [OWASP Java Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html)
- [Alibaba Java Coding Guidelines](https://alibaba.github.io/Alibaba-Java-Coding-Guidelines/)
