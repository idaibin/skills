# Contract-to-test coverage

## Contents

- [Existing-project default](#existing-project-default)
- [Reported failures and preserved behavior](#reported-failures-and-preserved-behavior)
- [Generated coverage boundaries](#generated-coverage-boundaries)

Identify repository/revision (plus dirty patch digest when applicable), applicable
product/UI/API authorities and their acceptance status, feature/journey IDs and scope.
Early analysis may use drafts: label assumptions and disputed outcomes provisional,
route decisions to their authority, and refine examples with design/implementation.
Exploratory observations can reveal gaps but cannot settle business policy or pass a
business-acceptance row whose oracle is unresolved. For native-app cases, bind platform and
installed artifact identity/version to the account, project and cold/warm startup
state in the existing case IDs and ledger. H5/browser or source evidence cannot
substitute for an applicable native artifact/device result. Bind runtime/build identity
before execution. Discover existing test directories, commands, fixtures,
coverage reports and project evidence conventions. Source inspection locates checks;
it does not demonstrate that the checks ran.

Build or update the project's existing matrix. Each row names its requirement or risk,
observable expected outcome, affected code or boundary, test layer, scenario, fixture,
role, environment, check and evidence. A missing or disputed expected outcome is a
business-contract gap: record it for its human owner without stopping independent
baseline regression or bounded exploration. Do not derive business acceptance from
implementation agreement; use the existing-project default below.
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

For asynchronous result/download journeys, map relevant faults to accepted states and
recovery: failed retrieval versus confirmed emptiness, stage-specific retry, retained
results after refresh failure, duplicate admission, close during work and late completion.
Include focus assertions across loading/failure/retry/busy/close when keyboard behavior
is in scope. A synthetic fault such as 503 is a selected fixture, not a universal code.
Record controllable failure points; route missing injection support to implementation.
Simulated faults do not prove a real service failed or recovered.

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

## Existing-project default

Without a complete PRD, automatically infer a bounded scenario inventory from the
current source, reachable routes/callers, native interfaces, state transitions,
validation branches, existing tests and available real-page observations. Do not
require a reconstructed specification or human approval of every inferred case before
planning, script generation and authorized execution. Use available confirmed rules
first and keep missing documentation local to the claims that actually need it.

Do not queue every inference for approval merely because documentation is missing;
queue only material conflicts or unknowns that change a scoped outcome, permission
or business-acceptance decision. Routine evidenced baseline cases proceed directly.

In the existing oracle/evidence notes, distinguish confirmed rules, recorded
current-behavior baselines and provisional inferences, with their source paths/ref
and observations. Freeze each expected outcome before the asserted run; never read
the actual result and use it as that run's expected value. A baseline pass proves
consistency with that baseline. An inference pass supports a hypothesis; neither
settles business policy. Naming alone is a hypothesis, not a verified behavior.

When sources conflict or code/runtime cannot establish business meaning, perform a
bounded discriminating check when safe. Record the question, competing meanings,
evidence, affected case IDs and human decision owner in the existing gap/issue record.
Continue independent tests without repeatedly requesting confirmation. Only the
dependent business verdict remains unresolved; safe exploratory steps may still run.
Unclear permissions or unsafe side effects stop the affected operation immediately.
Do not auto-approve a known defect, override a confirmed rule or repair product source
merely to match an inference. Preserve failures and later human decisions, update only
affected assumptions/tests, and rerun only affected cases plus required regressions.

## Reported failures and preserved behavior

Bind the reported defect to the original entry/action, role/data, runtime/source
identity and failing operation before selecting a repair retest. Missing original
request evidence blocks the incident-closure claim, not every independent check.
Keep a proposed cause separate from a reproduced defect and from an adjacent fix.
Repeated unsuccessful repairs under the same assumption need a check that can
distinguish explanations before another patch.

Do not promote a repair-specific claim within a layer from an aggregate suite
count, a plausible patch or a passing neighboring case. Credit the aggregate run
separately. A repair-specific pass requires the named executed assertion, relevant
input, basis and observed result; otherwise that subclaim remains not-run or
Not verified even when the suite passed.

For optimization or shared-component work, freeze request/field mappings, returned
membership, identity/selection, permissions and accepted failure behavior. Trace
different consumer modes and the parent page as well as the shared widget. Cover
independent list, detail, selection, confirmation and required persisted readback
outcomes; one passing selector cannot approve a blank parent list. Use the exact
requested full-tree historical revision for comparisons; legacy equivalence alone
does not settle correctness.

When later observations contradict a field assumption or prior pass, preserve the
original evidence and reopen only affected rows on the current basis. Reconcile
linked reports and corrections in time order; never ignore a later real sample
because an earlier summary says blocked, or promote an earlier real pass after a
relevant implementation/contract change. Unsettled semantics return to their owner.

## Generated coverage boundaries

Keep file/module dependencies separate from exported-symbol consumers. A shared import
does not establish a caller of every export; resolve the named symbol, alias, namespace
member and callback handoff, and retain computed/instance-dependent references as gaps.
Source-derived rows may generate and execute baseline regression and provisional
exploratory tests without an accepted business oracle. Keep their expectation source
and limits explicit under the existing-project default; only a business-acceptance
claim requires the corresponding confirmed rule. Unexecuted scaffolds remain not-run.
