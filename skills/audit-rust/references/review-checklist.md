# Review Checklist

Run Common Grounding and Common Evidence for every audit. Run only the checklist
sections for selected profiles. Mark every unselected profile `Out of scope`;
do not partially review or score it. A Combined audit uses the union of selected
sections plus the interaction checks. If required evidence is unavailable, keep
the profile selected and mark the exact claim `Not verified`.

## 1. Common Grounding

- [ ] Read nearest repository guidance and current `git status --short`.
- [ ] State whether this is a standalone audit or a scoped specialist subreview
      coordinated by `code-review`. In the latter case, preserve its read-only
      Git-change review coordination boundary.
- [ ] Record selected profiles, why each was selected, and excluded profiles as
      `Out of scope` before loading domain references or running commands.
- [ ] Classify CLI, library, Tokio service, Tauri backend, SQLite-first app,
      single binary, workspace, or combined project.
- [ ] Inspect only the manifests, toolchain, features, profiles, entry points,
      code, tests, benches, CI, docs, migrations, and runtime config required by
      the selected profiles.
- [ ] Find the nearest analogous modules, APIs, traits, tasks, queries,
      migrations, tests, and docs needed to evaluate the selected claims.

## 2. Architecture/Baseline Profile

- [ ] Record applicable MSRV, edition, resolver, targets, feature policy,
      repository-defined commands, and inherited workspace settings.
- [ ] Classify proposed rules as portable governance, organization baseline,
      new-project template, repository contract, or legacy exception.
- [ ] Assign relevant responsibilities to stable crate/module/boundary owners;
      keep binary, command, and transport entry points thin.
- [ ] Justify relevant traits, common types, crates, managers, services,
      repositories, runtimes, pools, caches, and global state.
- [ ] Trace public invariants, feature and compatibility impact, callers, and
      structural lifecycle across manifests, exports, tests, CI/deploy, and docs.

## 3. Ownership/Errors Profile

- [ ] Trace creation, sharing, mutation, close/wait, and drop for selected
      resources; quantify clone, allocation, and retention impact before finding.
- [ ] Check bounds on selected collections, channels, tasks, caches, buffers,
      and input-driven growth.
- [ ] Classify relevant user, business, dependency, corruption, retryable, and
      invariant errors; trace conversion, logging, retry, and user mapping.
- [ ] Keep expected failures recoverable and sensitive data out of logs.

## 4. Concurrency/Runtime Profile

- [ ] Prove async is needed and locate relevant blocking file, CPU, SQLite, and
      native work.
- [ ] Record task owner, join/panic path, cancellation points, shutdown wait,
      and cleanup for each in-scope background task.
- [ ] Record channel capacity/backpressure, concurrency limit, timeout scope,
      retry amplification, lock scope/order, and `.await` interaction.
- [ ] Identify deterministic lifecycle tests and a focused Loom or stress model
      only when supported and relevant to the selected claim.

## 5. Performance/Memory Profile

- [ ] Define representative workload, release-equivalent profile, environment,
      repetitions, variance, and baseline.
- [ ] Profile the claimed CPU, allocation, RSS, I/O, lock, task, binary, compile,
      or cold-start cost before recommending optimization.
- [ ] Distinguish leak, live owner, cache, allocator retention, mmap, SQLite page
      cache, OS cache, and index reader/writer retention.
- [ ] Define one-factor experiment evidence and regression protection; route any
      requested code/config edit to `implement-rust`.

## 6. SQLite Profile

- [ ] Verify runtime version, compile options, linkage, connection/thread model,
      busy policy, foreign keys, journal/synchronous mode, and async boundary.
- [ ] Check transaction batching, duration, rollback, reader lifetime, writer
      coordination, busy/locked handling, and external work in transactions.
- [ ] Check WAL checkpoint policy, starvation, file growth, backup/shutdown, and
      filesystem assumptions.
- [ ] Review migration upgrade/failure/recovery; schema constraints and index
      order; representative `EXPLAIN QUERY PLAN` and timing when claimed.
- [ ] Assess applicable freelist, optimize, vacuum, backup restore, and integrity evidence.

## 7. Unsafe/FFI Profile

- [ ] Verify each in-scope unsafe/FFI invariant, ABI, ownership, alignment,
      lifetime, thread affinity, panic containment, and cleanup.
- [ ] Review relevant native dependency features, build code, runtime version,
      platform packaging, advisories, MSRV, license, binary, and compile impact.
- [ ] Run Miri, sanitizers, leak, fuzz, target, or repeated-lifecycle checks only
      when supported and relevant; state unsupported required paths `Not verified`.

## 8. Combined Profile Interactions

- [ ] Keep the evidence and validation obligations from every selected profile;
      do not let one profile stand in for another.
- [ ] Trace shared owners and boundary behavior, such as Tokio task cancellation
      around SQLite transactions or FFI callbacks holding database resources.
- [ ] Validate interaction failures, cleanup, shutdown/restart, and recovery in
      addition to each profile's isolated invariants.

## 9. Common Evidence And Reporting

- [ ] Run only non-mutating repository-defined commands that support selected
      claims; record the exact command, result, and what it did not prove.
- [ ] For selected structural lifecycle claims, trace manifests, registrations,
      imports/re-exports, features, tests, migrations, generated files,
      deployment paths, docs, indexes, and stale references as applicable.
- [ ] Report exact evidence and mark missing files `Not found`, unavailable
      required evidence `Not verified`, and unselected profiles `Out of scope`.
- [ ] Leave code and Git state unchanged. Return scoped findings to
      `code-review` when it is the coordinating owner; never stage or commit.
