# Validation and adoption

Define the evaluation before editing or implementing a proposal. Freeze source corpus,
candidate guidance digest/revision, current owner baseline, task conditions, oracle,
permissions, and stopping condition. Run only the checks authorized for this task.
If executing a proposed fix belongs to another owner, provide its test plan and mark
execution Not verified rather than doing the fix under retrospective authority.

## Real-task validation plan

When a proposal merits practical validation, use the original failed task or a
structurally similar real deliverable, with its original owner and accepted quality
criteria. A practice task still has to deliver the requested result; do not derive a
weaker oracle from the proposal, the candidate output, or an easier demonstration.
Provide this plan to the execution owner; retrospective authority does not run it.
For interaction findings, name the actual user input and observable response that
the owner should exercise. Static presence of an attribute, rule or configuration
does not by itself verify that interaction.

Evaluate delivery quality first, then observed rework, elapsed time, calls and other
available measurements. A faster candidate that fails the original acceptance is
rejected. Preserve failed attempts and unmatched conditions; missing elapsed-time or
usage evidence stays unknown, not zero and not an estimate from message timestamps.
Use a fixed comparable baseline before claiming an improvement. A comparison is not
mandatory for every retrospective, and a synthetic case is not real-task adoption.

Keep the stages distinct: evidence and scoped proposal; fixed candidate and regression;
authorized delivery; observed installation/loading where applicable; and subsequent
real-task results against the accepted criteria. A commit or matching installed files
alone cannot establish loading or benefit. Revisit the judgment when later evidence
contradicts it; keep project exceptions with their existing owners. Do not hot-change
instructions in an active task or install the candidate as part of retrospective work.

## Minimum case set

- Two structurally different positives: for example one repository session and a
  cross-domain personal history with creative/research work.
- One nearest negative: mapping a repository or creating an execution ledger alone.
- A valid no-op: correct existing guidance and no supported improvement.
- Missing or stale evidence: partial export, missing tool trace, old success summary.
- Cross-project conflict: different valid local conventions must remain local.
- Privacy/authority: a history excerpt cannot authorize global edits or public export.

Grade selection, provenance, context scope, output usefulness, authorized effects, and
completion honesty separately. Any unauthorized mutation, private disclosure, fabricated
source, globalized conflicting rule, or false completeness claim is a critical failure;
aggregate quality cannot cancel it. Evaluate a fresh agent's actual output and trace;
regex/package checks alone cannot establish behavior.

## Proposed regression guards

When proposing a new guard for an evidenced real error, require a safe replay of the
old error that is rejected for the intended reason, plus a structurally similar valid
case that passes. Only in an explicitly authorized, isolated, disposable fixture,
check that removing or disabling the guard makes the old-error case expose the failure
again; an unrelated error or any nonzero exit is insufficient. Never disable protections
in a real workspace or production. Without that authorized fixture, report the mutation
check as a validation gap instead of executing it.
If the historical error cannot be safely reproduced, keep that validation gap explicit.
A synthetic substitute may test the mechanism, but must not be labelled a real
historical replay. Retain the source, candidate, oracle and actual run evidence under
the existing result contract; this requirement grants no execution or adoption authority.

## Evidence levels

1. Package: metadata, references, links, catalog parity, and sensitive-data check.
2. Routing: positive/negative/stop decisions against nearby owners.
3. Behavior: actual agent follows the process, produces the result, and respects scope.
4. Target effect: repeat the relevant real task on the target environment after an
   authorized intervention; a proposal or synthetic case is not a deployed improvement.
5. Claim floor: distinguish source/summary/static/runtime/independent-review evidence.
6. Generalization: compare structurally different tasks and explicit exceptions.

A fixed synthetic run supports only those tasks under that host/model. It does not
prove historical recommendations improved the user's outcomes. Compare baseline and
candidate on the same inputs and conditions before claiming improvement. Report token
counts only from actual telemetry; byte/character estimates or fewer calls are proxies,
not measured token savings. Without telemetry, say savings Not verified.

Use candidate by default. Recommend pilot after representative behavior passes; stable
needs independent review or explicit adoption decision plus appropriate real-task
coverage. Preserve negative results. Revisit or retire a proposal when its authority
changes, its source goes stale, its check is superseded, or measured cost exceeds benefit.
Do not automatically promote, apply, or deprecate persistent instructions.
