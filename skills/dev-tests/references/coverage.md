# Contract-to-test coverage

Identify repository/revision (plus dirty patch digest when applicable), applicable
product/UI/API authorities and their acceptance status, feature/journey IDs and scope.
Early analysis may use drafts: label assumptions and disputed outcomes provisional,
route decisions to their authority, and refine examples with design/implementation.
Exploratory observations can reveal gaps but cannot settle business policy or pass an
acceptance row whose oracle is unresolved. Bind runtime/build identity before execution. Discover existing test directories, commands, fixtures,
coverage reports and project evidence conventions. Source inspection locates checks;
it does not demonstrate that the checks ran.

Build or update the project's existing matrix. Each row names its requirement or risk,
observable expected outcome, affected code or boundary, test layer, scenario, fixture,
role, environment, check and evidence. A missing or disputed expected outcome is a
contract gap: route it to its authority rather than deriving success from implementation.
A layer may contain multiple boundary-specific rows: an external protocol can pass
while the application adapter in the same layer remains not-run. Never collapse these
into an unqualified whole-layer pass.
Prioritize by likely failure and user/data impact, changed boundaries and prior defects.
Choose economical checks at the lowest boundary that can falsify each claim, then add
integration or critical-journey checks for risks those checks cannot cover. Preserve
required project gates; risk selection cannot silently waive them.
For a narrow request, cover requested and impacted layers without unrelated ceremony.
For full-flow acceptance, disposition the five views below with justified applicability.
They are neither chronological stages nor an exhaustive quality/completeness checklist:

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

Use positive, negative, edge, recovery and role scenarios where behavior or risk
requires them. Include cross-layer invariants: what the UI promises must match the API
and backend outcome. Keep visual acceptance and interaction correctness separate.

On PRD/UI/API changes, map changed acceptance IDs to tests, fixtures, roles and journeys.
On code/configuration changes, inspect affected call paths and consumers and add adjacent
regression risks. Record which results require rerun, which remain reusable and why.
A stale receipt is historical evidence with `not-run` on the new basis until validated.
Return affected missing checks to the code owner and ledger changes to `to-task`.

When resuming a campaign or receiving delegated results, reconcile each observation
against the existing requirement, case ID and evidence layer before selecting another
run. Reopen only rows whose consumed behavior, fixture or basis changed; preserve
usable raw evidence for unaffected rows. An agent's terminal state closes its assigned
execution, not the parent acceptance case or the campaign verdict. Do not create a
continuation case merely to record a retry or a handoff.

For relevant risks, check accessibility, authorization/data protection, reliability,
recovery and compatibility across these views rather than adding mandatory new layers.
Identify missing observable assertions, controllable fixtures or failure injection as
testability gaps for the implementation owner. Inspect actual inputs, exercised paths
and assertions: a test name, count or configured workload is not coverage evidence.
For a requested release-readiness assessment, identify missing version-bound health
signals and recovery/rollback evidence for the release owner. Test success alone cannot
prove deployment health or authorize monitoring configuration, rollout or rollback.
