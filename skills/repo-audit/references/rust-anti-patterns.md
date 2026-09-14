# Anti-Patterns

| Signal | Why it is risky | Required investigation | Preferred correction |
| --- | --- | --- | --- |
| Trait for every module | indirection without polymorphic need | implementations, consumers, test seam, public contract | use concrete type or retain only proven boundary |
| Repository/service/manager shells | ownership and errors become ceremonial hops | behavior and invariant owner | collapse forwarding layers into real owner |
| Global runtime or connection pool | hidden lifetime, shutdown, and test interference | creation, users, teardown, thread model | explicit application owner and scoped handles |
| Sync SQLite or file work in async handler | executor starvation | duration, runtime worker behavior, concurrency | serial/dedicated worker or bounded blocking boundary |
| Unbounded channel or task spawn | memory and overload growth | item size/rate, consumer throughput, shutdown | bounded capacity/concurrency and explicit shedding |
| Lock held across `.await` | deadlock and contention | invariant, await path, lock order, profile | shorten critical section or redesign ownership |
| All errors become strings | lost classification and source | producers, callers, retry and user mapping | typed errors with boundary conversion |
| Pervasive `Arc<Mutex<_>>` | unclear owner and coarse contention | access pattern, consistency, contention | direct owner, actor, narrower state, or measured sharding |
| Complex lifetimes solely to remove clone | fragility without measured gain | clone size/frequency/profile | keep simple ownership unless benchmark justifies change |
| Allocator, SIMD, inline, unsafe, or mmap by intuition | portability and safety cost | representative profile and baseline | retain safe baseline; add only measured optimization |
| One transaction per row | fsync/locking overhead | batch semantics and failure boundary | bounded batch transaction |
| Network call inside transaction | long locks and uncertain rollback | transaction duration and idempotency | fetch/compute outside, write atomically inside |
| One index per filtered column | write/storage cost and poor composite use | actual queries, cardinality, plans | workload-shaped composite/partial/covering index |
| WAL treated as multi-writer | busy failures remain | connection/writer/checkpoint model | coordinate one writer and handle busy outcomes |
| Periodic full `VACUUM` after deletes | I/O, locks, and disk demand | freelist, file needs, outage, free space | reuse freelist; targeted maintenance from evidence |
| Query loads all rows | unbounded latency/memory | consumer and result cardinality | page, stream, or batch |
| Empty database performance test | unrealistic plans and cardinality | representative data distribution | seeded or captured representative workload |
| Large file split by line count | new navigation without new ownership | responsibilities and change reasons | split at stable invariant/lifecycle boundary only |
| Code changes without docs/migrations | source-of-truth drift | architecture, schema, commands, runbooks | update all affected lifecycle artifacts |
| Unrelated cleanup in same change | review and regression risk | dependency of cleanup on requested task | exclude and report separately |

These are review signals, not automatic findings. Confirm repository context,
impact, and evidence before prescribing a change.
