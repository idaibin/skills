# Frontend Performance Change Review

Read for local or shared frontend loading, responsiveness, rendering, memory, request preparation, cache subscriptions or lifecycle changes. Review the selected patch read-only; reuse original Product/UI behavior rather than redefining it.

## Shared And Local Effects

Map the changed owner to actual consumers and data aliases. Check whether a shared correction applies across routes or only to one feature. Old trace measurements require deployed-source identity; static complexity proves work exists, not its cloud-device duration or its share of every observed delay.

## Regression Boundaries

- Encryption disabled may skip unused work; encryption enabled must retain proof fields, request/body placement, encoding and encryption inputs. Compare deterministic outputs with fixed time and record when crypto is replaced by a test double.
- Cache/root assignment searches are insufficient. Follow list/row handlers into nested objects shared with cached responses. Preserve nested read/optimistic states, pending hydration and the original storage JSON format.
- For entry-specific watchers, verify replacement, deletion, whole-root replacement, restored entries and disposal while live entries still exist. Testing disposal after clear does not exercise a live subscription. Retained old objects must not schedule new persistence.
- A first-start guard must not block manual refresh, pagination, changed URL context or resized page size. Check both orders: layout/query request before the initial queue, and initial request before a later legitimate layout/query change. Cache return and a fresh request for a changed context are different contracts.
- KeepAlive mounted and activated hooks can both run on initial entry. Verify one-time work, resume behavior, active-only listeners, timers and late responses. Keep drafts, selected people, detail caches and failure recovery; do not demand cancellation where preserving an in-flight cache update is the accepted behavior.
- Stable Popper options preserve positions/triggers and may reduce unrelated setOptions work; actual layout or floating visibility still needs runtime evidence. Transform/opacity, transition duration and perceived first feedback are separate questions.

## Evidence Closure

Check the supplied measurement plan, baseline/candidate identities, comparability and
uncertainty before crediting improvement. Separate improvement from budget attainment;
inspect affected recovery/keyboard evidence such as stage-specific retry, retained
results, duplicate admission and focus continuity against the accepted journey.
Local work reduction alone cannot prove user benefit. Use the testing owner's
measurement decision; review does not invent sampling rules.

Distinguish implementation-mirroring tests from observable race, cache or transport tests. A missing test dependency is a test gap, not proof of a production defect. A blank, unauthorized or failed-data browser state cannot prove the positive selection/reopen/cache flow. Request counts need complete captured events and the same relevant URL/page/size state. Report precise unexercised races and environments instead of claiming blanket safety or whole-product performance.
