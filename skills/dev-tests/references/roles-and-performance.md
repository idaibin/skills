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
multi-user transport evidence. Report observed overlap/actor behavior separately from
configured worker counts or arrival rate; scheduling intent does not prove concurrency.
Never switch identities to evade an access denial.

For performance, take budgets and workload from the accepted project requirement or
explicitly report missing budgets. Do not invent numeric pass thresholds. Declare:

- environment/hardware/runtime and comparable baseline revision;
- dataset size, role mix, concurrency or arrival rate, operation distribution;
- warmup, measured duration/sample count, repeat count and cache state;
- latency distribution (including tail percentiles), throughput and error rate;
- relevant CPU, memory, connection/storage/resource use;
- agreed budget, abort threshold and cleanup.

## Frontend Measurement Interpretation

Distinguish field user-experience metrics, laboratory diagnostics, business-interaction
timings and resource/complexity signals. Record what each can prove; a laboratory
score, request count or component duration cannot substitute for a user-task outcome.
Separate external reference thresholds, accepted project gates and provisional budgets.

Define each interaction's start and observable end before comparing results: first
feedback, usable controls and completed content can have different boundaries. A DOM
flush or callback before repaint is not proof of presentation. For SPA measurements,
bind normalized route/context and navigation identity; pathname may not distinguish
hash routes, and visit metrics need not describe each route. Observe browser/library
support before claiming soft-navigation coverage. Keep sensitive query values out of
telemetry; a plan grants no collection endpoint or transmission authority.

Preserve raw samples, count, aggregation, spread and reasons for exclusions. Keep
role/data, browser/tool versions, network/CPU settings, cold/warm cache and observer
overhead comparable. A small lab sample percentile is not a field-population percentile.
If variance, identity or changed conditions can explain the difference, report improvement
as inconclusive rather than selecting the fastest run or inventing a significance
threshold. Planned repeated measurements are samples, not retries of failed product
assertions; the existing execution stops still govern failures.

Report improvement, budget attainment, protected business/recovery/keyboard outcomes
and regression protection separately. A faster broken journey is not accepted. Stop
optimization at the agreed outcome or when evidence shows no meaningful benefit; new
goals need scope. Reuse effective regression checks and route missing assertions to
their implementation owner. Deployment observation and rollback remain release work
under separate authorization.

Check load authority, target ownership, resource/cost limit and stop conditions before
execution. Production or third-party load is never implied by a test request. If no
approved safe load target exists, return a plan and `blocked`, not a load claim. With no
accepted budget, measured observations can be reported but performance acceptance stays
`not-run` or `blocked` according to the missing prerequisite. A local microbenchmark
cannot establish full-path or production capacity. Compare improvement claims only on
comparable workloads/environments with uncertainty and observed errors disclosed.
