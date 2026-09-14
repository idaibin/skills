# Java Profile

## Contents

- [Selection](#selection)
- [Audit Profiles](#audit-profiles)
- [Conditional References](#conditional-references)
- [Modes](#modes)
- [Output Additions](#output-additions)
- [Trigger Examples](#trigger-examples)
- [Non-Triggers](#non-triggers)

Audit Java engineering from current repository evidence with explicitly
selected risk profiles. Use open-source projects and framework guidance to
form questions, not to declare target-repository defects by stylistic
comparison.

## Selection

1. Record the Git/build root and inspect only the selected manifests, source,
   tests, migrations, configuration ownership, CI, and runtime documentation.
2. Resolve the JDK, Maven/Gradle owner, Wrapper, parent/BOM/platform, modules,
   packaging, framework generation, executable entries, profiles, and quality
   commands from repository evidence, preserving reported conflicts.
3. Select one or more audit profiles; explicitly mark the rest `Out of scope`.
   Combine profiles when the invariant crosses them, such as transaction plus
   async event delivery or authorization plus tenant-filtered persistence.
4. Trace each candidate issue through trigger, reachable path, owner, state or
   data consequence, counterevidence, and a falsifiable validation seam.

## Audit Profiles

- **Build/architecture:** dependency direction, modules/packages,
  public/internal seams, build reproducibility, dependency authority,
  generated code, and lifecycle.
- **API/security:** routes, DTO validation, filters/interceptors,
  authentication, authorization/data scope, sessions/tokens, CSRF/CORS,
  upload/download, errors, secrets, and sensitive logging.
- **Persistence/transaction:** mappings, query shape, pagination, N+1 risk,
  locking, migrations, transaction boundaries/propagation, after-commit
  effects, and database compatibility.
- **Concurrency/integration:** executors, async/events, Redis/cache, messages,
  schedules, retries, idempotency, backpressure, distributed locks, and
  shutdown.
- **Performance/operations:** representative workload, database plans, pools,
  allocation/serialization, caches, remote calls, metrics, health, and failure
  modes.
- **Migration/compatibility:** JDK, Spring Boot, `javax`/`jakarta`, build
  tool, dependency, database, packaging, or configuration-generation
  transitions.

## Conditional References

- Load [Java engineering](java-engineering.md) for every audit: secure
  design, build, Spring, persistence, integration, testing, and comparative
  open-source lessons.
- Load [codebase design](codebase-design.md) for module/API/testability
  analysis and [code quality](code-quality.md) only when maintainability is in
  scope.
- Load [project grounding](project-grounding.md) only for semantic signals
  involving runtime/config precedence, packaged artifacts, public contracts,
  durable data, legacy replacement, auth/security, or cross-repository
  delivery. Use the grounding chain to bound adjacent evidence; do not scan
  every profile or repository merely because corresponding files exist.
- Load [protocol contracts](java-protocol-contracts.md) when the selected
  Java surface owns or implements an adopted OpenAPI contract, together with
  [OpenAPI governance](openapi-contract-governance.md) for synchronized
  cross-language contract rules.
- Apply [checklist](java-checklist.md) evidence and reporting gates to the
  selected profiles.

Treat source configuration, packaged configuration, and effective runtime as
separate evidence. A local boot or compilation cannot clear a target-profile,
service-registration, migration, or external-integration gap. Apply
authorization, transaction, integration, and persistence conclusions through
the selected Java engineering profile and require their matching
negative/runtime evidence before claiming consistency.

## Modes

- **Focused profile audit:** one or two bounded Java risk surfaces.
- **Combined risk audit:** interacting profiles such as transaction plus
  async events.
- **Baseline audit:** build, architecture, tests, documentation, and legacy
  exceptions.
- **Scoped specialist subreview:** Java evidence delegated by `repo-review`
  for a fixed basis.

## Output Additions

Lead with capability `java.surface.audit`, scope/basis, JDK/build/framework
facts, and before/after Worktree state. Report findings with impact, exact
location, evidence chain, counterevidence, remediation direction, and
validation seam; then commands, ephemeral resources, and cleanup. For each
profile, report applicability as `Applicable` or `Not applicable`, then
evidence status separately as `Verified`, `Failed`, or `Not verified`. Lead
with evidence-ranked findings, not a technology checklist: a missing
annotation, interface, test tool, module framework, or RuoYi-style component
is not a finding until its reachable consequence and target-owned requirement
are proven.

## Trigger Examples

- `Audit this Spring service's transaction and cache consistency risks.`
- `Review current route and method authorization coverage without editing.`
- `Audit Maven/Gradle toolchain reproducibility and private dependency risks.`
- `Assess this JPA query path for N+1, pagination, locking, and dialect risks.`
- `Audit this scheduler and Redis consumer for retries, idempotency, and shutdown.`

## Non-Triggers

- Repository Java orientation with no audit question; use `repo-map`.
- Implementing a confirmed fix; use `dev-java`.
- Diagnosing one failing command before a cause is established; use the host
  diagnosis flow.
- Reviewing a Worktree/commit for readiness; use `repo-review`.
- A vulnerability scan, exploit path, or PoC request; use a security workflow.
- Kotlin/Groovy/Scala language-semantics review; use a language-capable
  workflow. This profile may audit only explicitly bounded Java-owned
  Spring/build configuration with language-specific risks excluded.
- `Audit this Java DTO naming only; no runtime, persistence, public contract,
  or cross-repo behavior is in scope.` — keep project grounding inactive; do
  not scan profiles, schemas, or sibling repositories.
