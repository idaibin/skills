# Matt Skills Engineering Analysis

## Evidence Basis

- Repository: <https://github.com/mattpocock/skills>
- Reviewed revision: `9603c1cc8118d08bc1b3bf34cf714f62178dea3b`
- Publication index: <https://skills.sh/mattpocock/skills>
- Reviewed: `2026-07-16`

This is a method analysis, not a source import. AICraft keeps its own owners, authority boundaries, package format, and validation system.

The reviewed skills.sh page reported 55 published skills and the install command `npx skills add mattpocock/skills`. Current source places `grill-me` and `handoff` under `skills/productivity/`, while the engineering chain uses `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `code-review`. The AICraft mapping follows current package names and behavior, not the older paths in the supplied proposal.

## Methods Worth Absorbing

| Upstream skill | Useful method | AICraft destination |
| --- | --- | --- |
| `grill-me`, `grill-with-docs`, `to-spec` | Resolve requirements and decisions before implementation; separate synthesis from interviewing. | `code-planner` readiness and specification contract |
| `domain-modeling` | Ubiquitous language, scenario stress tests, state/rule clarification, sparse decision records. | New `domain-modeling` owner |
| `to-tickets` | Tracer-bullet vertical slices and explicit blocking edges. | `code-planner` task packages |
| `diagnosing-bugs` | Tight red/green loop, minimization, falsifiable hypotheses, one-variable probes, regression seam. | `diagnose` |
| `tdd` | Behavior tests at public seams and vertical red-green slices. | Internal references in `implement-frontend` and `implement-rust` |
| `implement` | Consume a spec, validate continuously, and review before delivery. | Existing `implement-* -> repo-review` chain |
| `code-review` | Keep Standards and Spec review independent so one cannot hide the other. | Two-axis evidence inside `repo-review` |
| `codebase-design`, `improve-codebase-architecture` | Deep modules, small interfaces, locality, leverage, and interface-as-test-seam. | `code-planner` deep-module reference plus existing audit/review profiles; no duplicate public review skill |
| `handoff` | Compact references, continuation state, and redaction discipline. | Adapt inside the AICraft-owned `repo-delivery` report contract |

## Methods Not Imported

- `ask-matt` and `setup-matt-pocock-skills`: AICraft already has a public routing graph, repository guidance, portable package rules, and install flow.
- A generic `implement`: AICraft keeps domain owners `implement-frontend` and `implement-rust`.
- A second `code-review` or architecture-review owner: `repo-review` and bounded `audit-*` skills already own those decisions.
- Upstream tracker-specific publishing, labels, `CONTEXT.md` location, automatic commits, and mandatory subagents: these are repository-specific policies, not portable AICraft defaults.
- Upstream `handoff` writes a temporary conversation-continuation document; it does not define a Git delivery report. The Delivery Report structure comes from the supplied AICraft v2 plan.
- Upstream source text and templates: concepts are re-expressed against AICraft authority and validation contracts.

## Current Upstream Drift From The Supplied Proposal

- Current source and skills.sh list `domain-modeling`; the older `domain-model` package is no longer present.
- Current upstream uses `to-spec` and `to-tickets`; `to-prd` is not present at the reviewed revision.
- Upstream `code-review` mandates parallel Standards and Spec subagents. AICraft keeps the two axes independent but only delegates when scopes are bounded, tools exist, and repository/user rules permit it.
