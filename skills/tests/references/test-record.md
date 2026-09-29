# Test record

Adapt the project's existing record rather than creating a second ledger. With no
existing record, use a concise Markdown report in its authorized evidence location.
Keep normative specs separate from run results. No extra machine schema is required.

## Scope and basis

Record: objective and included/excluded modules; authority paths/revisions; source
SHA plus relevant dirty-file fingerprints; runtime process/cwd/address/proxy; browser
surface/tab; sanitized role/account category; data source/fixture version; viewport,
theme and time; allowed writes and cleanup. Identify missing identity rather than
filling it from an older report.

## Inventory and cases

Keep an explicit page/function inventory when testing a whole application. For each
included function list applicable roles, states and journeys, with exclusions justified.
Keep one current result per case and evidence layer, linking its latest basis and raw
evidence; historical attempt notes are not the current status. Reconcile that row when
a result changes instead of adding a competing summary or a new continuation case.

| ID / requirement | Route / journey / role | Preconditions and input | Steps | Expected result | Layer / evidence | Result |
| --- | --- | --- | --- | --- | --- | --- |
| stable project ID | exact owned surface | dataset and initial state | real actions in order | observable assertions | linked current evidence | PASS / FAIL / BLOCKED / NOT RUN / N/A |

For writes include the readback and cleanup step. A case passes only if every required
assertion has matching evidence. Split independently useful layers when one is blocked;
for example Mock UI PASS and formal-service integration BLOCKED, never a combined pass.
For preservation or equality assertions retain both before/after values and the route,
not only a pass boolean. Keep sanitized method/path/body and response evidence for API
assertions, and actual readback for cleanup; a report's assertion is not its own proof.

## Defects

Each defect includes case ID, impact/severity, classification (product, contract,
fixture, environment or automation), owner, reproduction, expected versus actual,
evidence and next step. Distinguish confirmed facts from suspected causes. On retest
retain original failure and bind the new result to the changed basis and affected cases.

## Summary and resume

Report both page coverage and case coverage. Show the denominator and counts for
PASS/FAIL/BLOCKED/NOT RUN/N/A. Do not count N/A as passed or delete missing cases to
improve a percentage. A sample report names exactly the sample and untested inventory.

List source/static, test runner, Mock, real API, UI/interaction, artifact and deployment
results only when applicable. Missing required proof is `Not verified`; unrelated
release/build checks are N/A unless requested. Record restoration of test data,
fault settings, tabs and files separately from business success.

End with the finite recovery queue: case, dependency/decision, precise resume action.
An honest completed run may find defects or remain partial; it cannot claim whole
system acceptance until the agreed coverage and required evidence are complete.
