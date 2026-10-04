# Contract-to-test coverage

Freeze repository/revision (plus dirty patch digest when applicable), accepted PRD,
UI/Feature Spec/DESIGN and API contract identities, feature/journey IDs, runtime/build
identity, and requested scope. Discover existing test directories, commands, fixtures,
coverage reports and project evidence conventions. Source inspection locates checks;
it does not demonstrate that the checks ran.

Build or update the project's existing matrix. Each row names an accepted requirement,
observable expected outcome, affected code or boundary, test layer, scenario, fixture,
role, environment, check and evidence. A missing or disputed expected outcome is a
contract gap: route it to its authority rather than deriving success from implementation.
A layer may contain multiple boundary-specific rows: an external protocol can pass
while the application adapter in the same layer remains not-run. Never collapse these
into an unqualified whole-layer pass.
For a narrow request, cover its requested and impacted layers; do not impose unrelated
whole-product ceremony. For full-flow acceptance, explicitly disposition all five layers:

| Layer | What must be observable | Insufficient substitute |
| --- | --- | --- |
| Backend | Domain rules, state transitions, persistence/transaction/error behavior at the declared unit or integration boundary | Compilation or endpoint shape alone |
| API/interface | Real selected transport, request/response/error contracts, authorization and side effects when required | Direct handler calls or mocks labeled real HTTP |
| Frontend page | Actual rendering, route, layout/states, viewport and applicable visual/accessibility oracle | Source code, build output or a screenshot of another revision |
| Frontend function | Interactions and state transitions, validation/error/loading behavior, navigation and persisted outcomes where required | Static page presence or clicks without outcome assertions |
| Full E2E | Real entry surface through declared API/backend/storage/provider boundaries to externally observable outcome and cleanup | Unit totals, mocked service success or a disconnected CLI probe |

A CLI or headless service need not invent a frontend. Mark that layer `excluded` only
with the accepted scope/architecture source and reason. Record provider/test doubles
for each actual boundary. An E2E through a stub is an explicitly named simulated
journey, never proof of the substituted real boundary. Distinguish the first real E2E
from later regression coverage: one passing journey establishes that journey only.

Use positive, negative, edge, recovery and role scenarios where the accepted behavior
requires them. Include cross-layer invariants: what the UI promises must match the API
and backend outcome. Keep visual acceptance and interaction correctness separate.

On PRD/UI/API changes, map changed acceptance IDs to tests, fixtures, roles and journeys.
On code/configuration changes, inspect affected call paths and consumers and add adjacent
regression risks. Record which results require rerun, which remain reusable and why.
A stale receipt is historical evidence with `not-run` on the new basis until validated.
Return affected missing checks to the code owner and ledger changes to `to-task`.
