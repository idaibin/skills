# Skill Live Canary Summary

## Tests candidate basis

- Digest scope: all 19 packages declared by `skills-index.json`.
- Package digest: `sha256:d6547a0079060c0238c59dede573073e4228d866d8dd9b3877c11f1ba71aa360`
- Added tests is candidate-only. Its package and deterministic routing checks pass;
  seven independent decision cases and the full catalog gate pass (19 packages,
  72 routing cases, 452 tests and DESIGN.md regressions). Real-project
  end-to-end use and stable promotion remain unverified.
- Evaluation and remaining adoption gates: [tests candidate evaluation](tests-evaluation.md).
- The results below belong to the earlier 18-package basis, not the new candidate.


## Basis

- Digest scope: all 18 packages declared by `skills-index.json`; the index owns the package set.
- Package digest: `sha256:74d15429efc268191248069df54549c2d86c8f87a2f89eb425e5deca85681a26`
- Change focus: conditional native Rust UI/GPUI Kit guidance in dev-rust, native-source ownership clarification in ops-client, and targeted discovery/evaluation coverage, based on `10b4d61351eb21bdb1b015841a3f79219731f052`. No new owner, package, dependency migration or runtime installation.
- Current retrospective evaluation details are in [work-retro evaluation](work-retro-evaluation.md).

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | 18 self-contained packages; links and metadata validate. |
| Deterministic routing | Pass | 69/69 cases; no regressions against the immutable base. |
| Full catalog gate | Pass before narrow source-note correction | 18 packages, 69 routing cases, 452 tests, synchronized protocols, DESIGN.md contracts and whitespace; zero context warnings. The later per-package dependency-pin clarification receives focused validation below. |
| Native UI decisions | Pass within supplied decision scope, then focused recheck | Seven fixed synthetic cases cover explicit/contextual Rust UI work, comparison and native-operation boundaries, valid no-op, missing-runtime honesty and authorization stop. See the scoped result below. |
| Reduced-motion decisions | Historical decision scope | Three independent plan-only responses preserve owner-scoped diagnosis, a valid no-change case and missing-runtime honesty. No browser execution, installation or comparative improvement measured. |
| Interaction-owner behavior | Historical basis only | Six independent synthetic requests met their oracles on output review; see [interaction-owner evaluation](interaction-owner-evaluation.md). This is native-agent decision evidence, not executed UI or API proof. |
| work-retro behavior | Historical, unchanged package | Eight independently executed synthetic requests met the oracle on output review; full structured output retained locally. This is a native-agent run, not CLI JSONL or a real-world improvement measurement. |
| Prior selection/API forward-tests | Historical basis only | Base commit records these results; they were not rerun in this change and do not establish current native-UI behavior. |
| CLI evaluation | Not verified | The targeted native-UI ephemeral CLI attempt failed during app-server initialization before model startup with a read-only-filesystem error. |
| Runtime installation, real-world benefit, model comparison, efficiency | Not verified | Catalog changes and synthetic behavior cannot prove these claims. |

## Native UI Decision Evidence

One independent native agent evaluated seven fixed synthetic requests corresponding
to the [native UI scenarios](../../skills/dev-rust/references/eval-cases.md#native-ui-profile-eval).
It received runtime skill files and each case's supplied facts, with expected
answers, evaluation references and prior findings withheld. Runtime reads were
batched; these were not seven isolated model invocations. Model identity was not
independently attested, and no external model comparison was requested.

The author inspected all seven outputs: source/operation/selection ownership,
bounded lifetime correction, reuse/no-op behavior, per-layer evidence and the
missing-authorization stop matched their case oracles. The only write was the
requested ignored result artifact; no source, dependency, Git, browser, app, test
or build action was taken by the evaluator. Its complete output and read-operation
record have SHA-256 `b0dae668585354c917a8c8921eb99023bf58a3db53ac6f83ef1ab669f96ad86d`.

After independent review corrected the source note to require per-package pins,
the same evaluator reread the final reference and reconsidered all seven cases;
no owner/outcome/stop decision changed. The preserved original result is not
rewritten as if it used the corrected basis. The separate focused recheck has
SHA-256 `764d757028b0316c1f446a5cc4a1210db32d4897614d63015a6a8eefe63565f9`,
binding the final native-UI reference SHA-256
`ebb2e6ef9a433dc8abdc8136c8a553dd723c64adc7afcfa4595c1716fc0b570d`.
This is a same-worker reread, not a fresh isolated evaluation or upstream audit.
Final focused validation passed 18-package structure/link checks, 134
validator/routing/search regressions, 69/69 routing cases and exact-path whitespace;
the context report retains zero warnings. The unchanged full-suite tooling was
not rerun after this bounded source-note correction.

This establishes observed planning decisions only. Actual Rust implementation,
headless tests, native/platform/screen-reader behavior, performance, runtime
installation and efficiency remain `Not verified`. The attempted CLI invocation
never reached model execution and produced no successful JSONL behavior trace.
The initial catalog run encountered an unwritable default npm cache in an existing
DESIGN.md parser test; the retry uses the already available writable task cache,
without changing parser code or project dependencies.

## Boundary

Static package/routing gates establish catalog consistency. Native independent behavior
results establish only observed decisions on their supplied fixtures. Neither proves
all-account history access, production operation, exact token savings, or stable adoption.
