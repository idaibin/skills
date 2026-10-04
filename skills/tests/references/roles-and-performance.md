# Roles, concurrent users and performance

Load only when contract or change impact requires these dimensions. Bind each scenario
to accepted role permissions and data boundaries; do not invent a universal role set.
Use authorized test identities and isolated fixtures. For relevant roles test allowed
and denied operations, ownership/tenant separation, and privilege changes or session
revocation. Validate through the real required boundary; hiding a button cannot prove
server authorization. Unknown policy goes to the product/API authority.

For multi-user behavior, identify distinct identities, initial state, concurrent
operation ordering, expected invariant and observable final state. Separate concurrency
bugs from serial correctness. Capture conflicts, retries, duplicate submissions and
isolation where applicable; deterministic local fixtures remain separate from real
multi-user transport evidence. Never switch identities to evade an access denial.

For performance, take budgets and workload from the accepted project requirement or
explicitly report missing budgets. Do not invent numeric pass thresholds. Declare:

- environment/hardware/runtime and comparable baseline revision;
- dataset size, role mix, concurrency or arrival rate, operation distribution;
- warmup, measured duration/sample count, repeat count and cache state;
- latency distribution (including tail percentiles), throughput and error rate;
- relevant CPU, memory, connection/storage/resource use;
- agreed budget, abort threshold and cleanup.

Check load authority, target ownership, resource/cost limit and stop conditions before
execution. Production or third-party load is never implied by a test request. If no
approved safe load target exists, return a plan and `blocked`, not a load claim. With no
accepted budget, measured observations can be reported but performance acceptance stays
`not-run` or `blocked` according to the missing prerequisite. A local microbenchmark
cannot establish full-path or production capacity. Compare improvement claims only on
comparable workloads/environments with uncertainty and observed errors disclosed.
