# Scoped Frontend Network Mock

Use an existing rendered page and its actual interactions. Mock supplies inputs;
it does not implement missing UI or prove real-service integration. Keep business
fixtures, API envelopes, transport-proof validation and expected scenarios in the
target project. Do not import Mock into production components or API clients.

## Contextual Selection And Local Reuse

During browser testing or verification, use the task context and established user
preferences to select this workflow; no Skill-name invocation is required. Observe
real APIs first. When an API fails or cannot supply the required test data, use a
project-local scenario automatically if synthetic inputs are within the task's
accepted scope. Record valid empty business results separately; they are not defects.
Do not ask again for the same authorized fallback. Mock never broadens production
write authority or proves real-service integration. If a required contract is missing,
retain that gap rather than inventing a formally valid response.

Keep reusable synthetic fixtures and scenario code in the project's existing test
location. Record their contract source/version, wire shape, scenario purpose and
known gaps in its maintained scenario/notes; keep per-run evidence in the ignored
artifact location. Reuse a fixture only after checking the current contract, request
and consumer; stale fixture success is not acceptance. Store no credentials, login
state, transport signatures or unsanitized personal records in reusable data.
Observed response samples, when needed, stay locally redacted and retain their
provenance; a consumer-derived shape remains distinct from a formal contract.
Business envelopes and test data do not belong in generic Skill packages.

## Execute

1. The caller supplies an authorized test target, project contract/scenario,
   version-bound external runner and allowed effects. Verify the task-owned tab,
   account, frame/target, actual request placement and tool capabilities. Record
   real results before substituting missing or failed interfaces. Authentication
   and initial page loading are distinct from the protected test interval.
2. Probe the adapter rather than assuming protocol documentation guarantees host
   support. Cover both XHR and Fetch where available. List uncovered Document,
   beacon, worker/SW, popup, WebSocket and server-side traffic; stop interactions
   whose safety depends on unverified coverage. A new tab does not prove isolated
   cookie/storage/cache. Prefer explicit test-target cache/SW controls when supported.
   Validate a native Fetch request through actual network events rather than treating
   filter acceptance as transport evidence. Repeated URLs must hit the current fixture
   rather than an older cache entry; use a fresh engine and page to check state leakage.
   Target-local HTTP cache/SW bypass does not isolate shared cookie or localStorage.
   If acceptance requires an isolated context and the host cannot verify one, block
   that invocation instead of clearing user storage or downgrading the requirement.
   When explicitly using Playwright, create fresh nonpersistent BrowserContexts;
   do not import storageState or copy the user's authentication. Validate same-context
   positive controls and cross-context negative controls for cookie, localStorage
   and CacheStorage. A warm HTTP cache hit followed by a cold read in the other
   context validates cache partitioning; route/cache disabling alone cannot do so.
3. Before the business interaction, enable request-stage protection. Match exact
   origin, method, path, query multiplicity, body and authorized frame/target.
   Each controlled request has exactly one decision: Mock, an explicit real permit,
   or deny. Unknown rules, invalid fixtures and handler errors never fall back to
   the real network. Do not infer a permit from GET or a read-looking path.
4. Use one event consumer/cursor and an atomic pause claim tied to connection epoch
   and target/session. Ignore replay; record stale IDs without retrying them.
   Apply a fixture state proposal once, after the terminal command is acknowledged;
   uncertain command outcomes invalidate dependent acceptance. Keep all delayed
   callbacks cancellable. Logs omit credentials, headers and opaque proof values.
5. Assert API rule hits and actual UI together: expected content/error, loading
   transition, controls and state, with no unresolved controlled requests. Distinguish
   delay, actual client timeout, cancellation and response loss. Negative-test
   unknown operations and event replay before relying on a runner for writes.

## Close and Report

Stop new actions; keep protection active while cancelling pending work and closing
the owned disposable target. Verify closure and zero pending/timers. Do not equate
an empty interception-pattern array with complete cleanup. If the target must stay
open, require a separately verified quiescent release procedure.

Return separate results for Mock UI behavior, real integration, covered request
isolation and environment/visual evidence. Claims of zero real writes require
claim-matched upstream evidence; a screenshot or denied-request counter alone is
insufficient. Keep external-review status unverified until an actual review returns.
The coordinator owns composition, version binding and promotion of an external
prototype into maintained scripts; browser execution does not authorize promotion.
Use the coordinator's existing host adapter discovery/selection seam. Bind the actual
executor, scenario and native contract versions/hashes before execution; reject drift.
Registry compatibility is separate from host loading, invocation, UI and real-service
evidence. Keep external adapter code and project business fixtures under their owners.
