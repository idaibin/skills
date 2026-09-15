---
name: human-writing
description: "Use when drafting, rewriting, proofreading/校对, diagnosing, or adapting source-grounded prose while preserving facts, attribution, uncertainty, voice, and meaning; not for translation-only work, fiction, external publication, product/technical decisions, or AI-detection evasion."
---

# Human Writing

## Entry Gate

Produce writing that preserves the requested meaning, audience, authority, and evidence boundary. Require source material or clearly label assumptions; do not convert a style request into unauthorized publication or new factual/product decisions.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Draft/rewrite/adapt by deliverable type | [content modes](references/content-modes.md) | Audience-fit output |
| Facts, sources, uncertainty, or attribution matter | [fact integrity](references/fact-integrity.md) | Evidence-bound prose |
| Tone/style/platform calibration matters | [style diagnostics](references/style-diagnostics.md) and/or [platform calibration](references/platform-calibration.md) | Calibrated revision |
| Explain reasoning or make revisions transparent | [reasoning/explanation](references/reasoning-and-explanation.md) and/or [revision transparency](references/revision-transparency.md) | Traceable rationale |
| Quality check/examples are needed | [quality rubric](references/quality-rubric.md) and/or [before/after examples](references/before-after-examples.md) | Bounded quality pass |

## Invariants

- Preserve source fact/claim boundaries and name uncertainty; never fabricate citations or experience.
- Keep writing, product/technical decisions, external sends, and Git delivery separate.
- Return the requested format and scope without silently expanding the audience or claim.

## Output Map

For draft, rewrite, proofreading, or adaptation, return the requested finished artifact
only. For diagnosis, return the concrete problem, impact, and editing direction. Add
source/assumption disposition, unresolved facts, alternatives, or revision rationale
only when the user requests them or the safe supported artifact requires a named gap.

## Reference Map

- Load each condition-specific reference named in the Route Map only when applicable.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
