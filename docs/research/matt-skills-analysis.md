# Matt Skills Engineering Analysis

## Evidence Basis

- Repository: <https://github.com/mattpocock/skills>
- Reviewed revision: `9603c1cc8118d08bc1b3bf34cf714f62178dea3b`
- Publication index: <https://skills.sh/mattpocock/skills>
- Reviewed: `2026-07-16`

This is a method analysis, not a source import. The catalog keeps its own owners, authority boundaries, package format, and validation system.

The reviewed skills.sh page reported 55 published Skills and the install command `npx skills add mattpocock/skills`. Current source places `grill-me` and `handoff` under `skills/productivity/`, while the engineering chain uses `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `code-review`. This catalog's mapping follows current package names and behavior, not the older paths in the supplied proposal.

## Methods Worth Absorbing

| Upstream Skill | Useful method | Catalog destination |
| --- | --- | --- |
| `grill-me`, `grill-with-docs`, `to-spec` | Resolve requirements and decisions before implementation; separate synthesis from interviewing. | `product-spec` internal clarification and Ready-for-slice contract |
| `domain-modeling` | Ubiquitous language, scenario stress tests, state/rule clarification, sparse decision records. | Existing `domain-modeling` owner |
| `prototype` | One explicit question, materially different comparable variants, finite budget, and throwaway evidence. | Codex Product Design for visual/prototype exploration; keep `ui-spec` specification-only and logic experiments with the relevant decision owner |
| `writing-great-skills` | Context/cognitive load, checkable completion criteria, single-source rules, branch disclosure, pruning, and leading words. | Skill standard and affected entrypoints |
| `to-tickets` | Tracer-bullet vertical slices and explicit blocking edges. | Host planning under effective repository instructions |
| `diagnosing-bugs` | Tight red-capable loop, minimization, falsifiable hypotheses, one-variable probes, regression seam. | Global diagnosis instructions; no public diagnosis Skill |
| `tdd` | Behavior tests at public seams and vertical red-green slices. | Internal references in `dev-frontend` and `dev-rust` |
| `implement` | Consume a spec, validate continuously, and review before delivery. | Existing `dev-* -> repo-review` chain |
| `code-review` | Keep Standards and Spec review independent so one cannot hide the other. | Two-axis evidence inside `repo-review` |
| `codebase-design`, `improve-codebase-architecture` | Deep modules, small interfaces, locality, leverage, and interface-as-test-seam. | Host planning plus existing audit/review profiles; no duplicate public review skill |
| `handoff` | Compact references, continuation state, and redaction discipline. | Global continuation/task coordination; no public handoff Skill |

## Methods Not Imported

- `ask-matt` and `setup-matt-pocock-skills`: the catalog already has a public routing graph, repository guidance, portable package rules, and install flow.
- A generic `implement`: the catalog keeps domain owners `dev-frontend` and `dev-rust`.
- A second `code-review` or architecture-review owner: `repo-review` and bounded `audit-*` skills already own those decisions.
- Upstream tracker-specific publishing, labels, `CONTEXT.md` location, automatic commits, and mandatory subagents: these are repository-specific policies, not portable catalog defaults.
- Upstream prototype capture may use a throwaway commit, but this catalog never derives commit/push authorization from prototyping; artifacts stay disposable unless separately delivered.
- Upstream `handoff` writes a temporary conversation-continuation document; the catalog keeps continuation in host coordination rules rather than a Git delivery owner.
- Upstream source text and templates: concepts are re-expressed against the catalog authority and validation contracts.

## Current Upstream Drift From The Supplied Proposal

- Current source and skills.sh list `domain-modeling`; the older `domain-model` package is no longer present.
- Current upstream uses `to-spec` and `to-tickets`; `to-prd` is not present at the reviewed revision.
- Upstream `code-review` mandates parallel Standards and Spec subagents. The catalog keeps the two axes independent but only delegates when scopes are bounded, tools exist, and repository/user rules permit it.
