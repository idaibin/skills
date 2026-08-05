# Standards and Spec Review

## Contents

- [Standards Axis](#standards-axis)
- [Security Evidence](#security-evidence)
- [Spec Axis](#spec-axis)
- [Conditional Frontend Design Compliance](#conditional-frontend-design-compliance)
- [Conditional Documentation Authority Review](#conditional-documentation-authority-review)
- [Independence and Integration](#independence-and-integration)
- [Verdict](#verdict)

## Standards Axis

Build the standard set from effective repository/host guidance, contribution and architecture docs, language/framework conventions selected by the changed surface, and enforced tool output. Check correctness, architecture, security, performance, maintainability, compatibility, and structural lifecycle only where evidence makes them applicable.

For each finding, cite the governing source when one exists. Treat general smells as judgment signals, not hard violations; repository rules and demonstrated local conventions win.

When code quality materially applies, load `code-quality.md`. Attribute each
issue to the fixed review basis: newly introduced, expanded, exposed,
pre-existing-but-blocking, or merely pre-existing. Only the first four can
affect the review verdict, and a blocking pre-existing issue must be directly
required by the changed path. Language/framework profiles refine reachability;
they do not replace the shared finding gate.

## Security Evidence

Apply this only when a security claim is material. Keep status separate from P0-P3:

- **suspected:** scanner match, dangerous primitive, or incomplete trace;
- **likely:** static evidence establishes input, control, sink, reachable path,
  supported boundary, preconditions, and impact without material counterevidence;
- **validated:** a bounded test, PoC, debugger/sanitizer trace, or realistic local
  interface reproduction confirms the original consequence;
- **fixed:** a new fixed basis replays the original validation path and focused
  regression evidence confirms the consequence no longer occurs.

Record source, control, sink or protected operation, path, trust boundary,
preconditions, supporting and counterevidence, proof gaps, confidence, and next
validation step. API names, dependency presence, strings, authentication, frontend
hiding, or a partial chain do not prove exploitability; a patch or new test alone does not prove `fixed`.

Ordinary static review stays self-contained. Route explicit security execution to
the matching host workflow: Git change set -> diff scan; current repository or path
-> standard scan; named candidate -> validation. Do not collapse that workflow into
this review. When integrating completed results, preserve provider-native artifacts,
verify their basis and evidence before mapping status, and expose missing runtime
proof. Dynamic checks require an authorized safe target and avoid destructive production use.

## Spec Axis

Locate the originating requirement in this order when available:

1. a user-supplied spec, issue, PRD, or acceptance criteria;
2. issue/requirement references bound to the branch, commits, or review package;
3. a repository spec artifact clearly matching the reviewed change;
4. explicit decisions and acceptance criteria retained in the current task context.

Check:

- required behavior missing or partial;
- implemented behavior that contradicts the requirement;
- acceptance criteria without evidence;
- unrequested behavior or scope creep;
- error, edge, migration, permission, compatibility, or rollback behavior the spec requires;
- docs/tests that claim different behavior from the spec.

If no trustworthy source exists, report `Spec Compliance: Not verified (no spec source)` and continue the Standards axis. Do not reconstruct intent from code and then claim compliance.

## Conditional Frontend Design Compliance

Use this subflow only when the fixed change basis affects frontend visual behavior or
a UI contract. Trace the smallest relevant chain in order:

```text
product requirements or product Feature Spec
  -> selected-source UI Feature Spec
  -> resolved design-root DESIGN.md
  -> implementation adapter/config
  -> runtime/browser evidence
```

`repo-map` may shorten navigation but never proves compliance. Check shared token and
component semantics, layout/pattern use, and the reachable consumer only to the
extent the change requires. The two Feature Spec types do not substitute for one
another: when both apply, read each. Missing optional artifacts do not add ceremony,
but a missing product authority or UI authority that affects behavior or acceptance is
separately `Not verified`; missing runtime/browser evidence is a distinct
rendered-behavior `Not verified`. Do not infer exact visual values from pixels, make
this a mandatory `audit-frontend` handoff, or open a parallel review entry point.

When the basis adds or changes motion, gesture behavior, transition ownership, or
user-visible interaction feedback, load `interaction-motion-review.md` inside this
same subflow. Do not infer that branch from `.tsx`, `.vue`, `.css`, component paths,
or a frontend dependency alone.

## Conditional Documentation Authority Review

Use this subflow only when the basis creates, restructures, moves, deletes, or claims
completion of authoritative documentation. Load
`documentation-authority-review.md`; keep Standards and Spec evidence independent.
Check current-only authority, index and link closure, Product/UI/DESIGN/Map ownership,
task evidence placement, structured-artifact lifecycle, source-owner/runtime-identity
separation, deleted and untracked files, and absence of Skill-development material
from the product repository. After a fix, freeze a new basis and replay the failing
check; do not reuse the old verdict.

## Independence and Integration

Keep evidence collection independent so standards quality cannot hide a requirement miss and requirement coverage cannot excuse unsafe code. Parallel read-only passes are optional, not mandatory. The `repo-review` coordinator verifies both reports, removes duplicates, assigns one P0-P3 severity from concrete impact, and labels each finding with its contributing axis.

## Verdict

Report:

```markdown
## Findings
### P0
### P1
### P2
### P3
## Standards Verdict
## Spec Compliance
## Final Verdict
## Residual Risk and Not Verified
```
