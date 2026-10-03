# Validation and adoption

Define the evaluation before editing or implementing a proposal. Freeze source corpus,
candidate guidance digest/revision, current owner baseline, task conditions, oracle,
permissions, and stopping condition. Run only the checks authorized for this task.
If executing a proposed fix belongs to another owner, provide its test plan and mark
execution Not verified rather than doing the fix under retrospective authority.

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
