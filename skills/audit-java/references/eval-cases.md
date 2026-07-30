# Java Audit Eval Cases

## Trigger Eval

| Request | Expected behavior |
| --- | --- |
| `Audit this Java service's current transaction and Redis consistency.` | Trigger `audit-java` with Persistence and Integration profiles. |
| `Audit whether source profiles, packaged resources, startup exclusions, and target service registration resolve consistently.` | Trigger Build/Migration plus project grounding; keep source, artifact, and runtime evidence distinct. |

## Non-Trigger Eval

| Request | Expected behavior |
| --- | --- |
| `Implement the confirmed Java fix.` | Route to `dev-java`. |
| `Review this exact commit for merge readiness.` | Route to `repo-review`, optionally delegating bounded Java evidence. |
| `Prove this dependency is exploitable.` | Route to an available security validation workflow. |
| `Audit this Kotlin Spring coroutine service.` | Do not claim Kotlin semantics; route to a language-capable workflow unless the request explicitly limits scope to Java-owned Spring/build configuration. |
| `Audit this Java DTO naming only; no runtime, persistence, public contract, or cross-repo behavior is in scope.` | Keep project grounding inactive; do not scan profiles, schemas, or sibling repositories. |

## Quality Eval

| Case | Pass | Fail |
| --- | --- | --- |
| Toolchain | Resolves manifest/Wrapper/CI JDK and build ownership, preserving conflicts. | Infers from local `java -version` or latest framework convention. |
| RuoYi comparison | Uses RuoYi to ask about permissions, data scope, scheduling, async, and modules. | Reports missing RuoYi structures as defects. |
| Authorization | Proves reachable route/resource/data-scope bypass or missing negative coverage. | Equates login, role annotation count, or hidden UI with authorization. |
| Transaction | Proves proxy/rollback/async/after-commit consequence. | Flags annotations generically or assumes they work. |
| Query/performance | Uses representative data, query shape/plan, frequency, and impact. | Labels every repository method, full scan, or large class a defect. |
| Security boundary | Returns domain evidence and proof gaps for security-relevant conditions. | Claims complete scan, exploitability, or remediation verification. |
| Ephemeral runtime | Uses an explicitly authorized test-owned container, verifies cleanup, and preserves tracked files. | Writes shared/staging data or treats read-only as forbidding all representative runtime evidence. |
| Validation drift | Avoids known write-capable commands; stops on unexpected tracked drift, marks evidence contaminated and `Not verified`, and does not revert it. | Silently changes the review basis or reports the command as valid read-only evidence. |
| Reactive performance | Separates static WebFlux evidence from runtime workload proof and checks event-loop blocking, demand, cancellation, context, and retry behavior. | Claims reactive performance from annotations or compilation. |
| Context isolation | Traces async context propagation and proves missing finally-path ThreadLocal/MDC cleanup on a pooled thread before reporting a leak. | Recommends a propagation library by default or ignores pooled-thread cleanup. |

## Edge Cases

- A Java 8 legacy service is judged against its pinned supported stack, not Java 17/25 style.
- A documentation coverage threshold that differs from the POM is reported as authority
  drift, without claiming actual test quality from either number alone.
- Missing private Maven artifacts block dependency/runtime conclusions but not bounded
  source analysis; the exact remainder stays `Not verified`.
- A fixed SHA or Worktree readiness request stays owned by `repo-review`; `audit-java`
  may return only a bounded Java evidence packet and never the final readiness verdict.
- An applicable Persistence profile whose vendor-dialect check cannot run reports
  applicability `Applicable` and evidence status `Not verified` separately.
