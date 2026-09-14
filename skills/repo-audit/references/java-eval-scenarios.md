# Java Eval Scenarios

Load with the Java profile only.

## Quality Eval

Score these Java rows together with the shared rows in [eval cases](eval-cases.md).



| Case | Pass | Fail |
| --- | --- | --- |
| Toolchain | Resolves manifest/Wrapper/CI JDK and build ownership, preserving conflicts. | Infers from local `java -version` or latest framework convention. |
| RuoYi comparison | Uses RuoYi to ask about permissions, data scope, scheduling, async, and modules. | Reports missing RuoYi structures as defects. |
| Authorization | Proves reachable route/resource/data-scope bypass or missing negative coverage. | Equates login, role annotation count, or hidden UI with authorization. |
| Transaction | Proves proxy/rollback/async/after-commit consequence. | Flags annotations generically or assumes they work. |
| Query/performance | Uses representative data, query shape/plan, frequency, and impact. | Labels every repository method, full scan, or large class a defect. |
| Security boundary | Returns domain evidence and proof gaps for security-relevant conditions. | Claims complete scan, exploitability, or remediation verification. |
| Ephemeral runtime | Uses an explicitly authorized test-owned container, verifies cleanup, and preserves tracked files. | Writes shared/staging data or treats read-only as forbidding all representative runtime evidence. |
| Reactive performance | Separates static WebFlux evidence from runtime workload proof and checks event-loop blocking, demand, cancellation, context, and retry behavior. | Claims reactive performance from annotations or compilation. |
| Context isolation | Traces async context propagation and proves missing finally-path ThreadLocal/MDC cleanup on a pooled thread before reporting a leak. | Recommends a propagation library by default or ignores pooled-thread cleanup. |

## Edge Cases


- A Java 8 legacy service is judged against its pinned supported stack, not Java 17/25 style.
- A documentation coverage threshold that differs from the POM is reported as authority
  drift, without claiming actual test quality from either number alone.
- Missing private Maven artifacts block dependency/runtime conclusions but not bounded
  source analysis; the exact remainder stays `Not verified`.
- A fixed SHA or Worktree readiness request stays owned by `repo-review`; `repo-audit`
  may return only a bounded Java evidence packet and never the final readiness verdict.
- An applicable Persistence profile whose vendor-dialect check cannot run reports
  applicability `Applicable` and evidence status `Not verified` separately.
