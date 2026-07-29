# Reference Skill Catalog Analysis

## Evidence Basis

This is a generalized method analysis of public Skill catalogs, not a source import.
Repository names, owner accounts, revisions, dates, URLs, and personally named package
identifiers are intentionally omitted. This catalog keeps its own owners, authority
boundaries, package format, and validation system.

## Methods Worth Absorbing

| Method | Useful behavior | Catalog destination |
| --- | --- | --- |
| Requirements challenge | Resolve requirements and decisions before implementation; separate synthesis from interviewing. | `product-spec` clarification and Ready-for-slice contract |
| Domain modeling | Use shared language, scenario stress tests, state and rule clarification, and sparse decision records. | Existing `domain-modeling` owner |
| Prototype comparison | Ask one explicit question, create materially different comparable variants, keep a finite budget, and retain disposable evidence. | Product-design tooling for exploration; `ui-spec` remains specification-only |
| Skill writing | Minimize context load, define checkable completion, co-locate rules and stops, keep one source of truth, disclose branches, prefer positive steering, and delete no-op or stale prose. | Skill standard and affected entrypoints |
| Task slicing | Use tracer-bullet vertical slices and explicit blocking edges. | Host planning under effective repository instructions |
| Failure diagnosis | Use a tight red-capable loop, minimization, falsifiable hypotheses, one-variable probes, and a regression seam. | Global diagnosis instructions |
| Behavior testing | Test public seams and use vertical red-green slices. | Internal references in implementation Skills |
| Document co-authoring | Gather source context, refine for the target reader, and re-read the finished artifact without imposing one document ceremony on every output. | `human-writing`; product decisions and acceptance remain in `product-spec` |
| React composition | Prefer explicit variants, slots or compound composition when boolean mode combinations create invalid states; preserve simple independent props when they remain clear. | React profiles in `dev-frontend` and `audit-frontend` |
| Web interface guidelines | Keep stable component, layout, accessibility, and performance checks versioned with the catalog; require runtime evidence for rendered claims. | `audit-frontend`, with accepted fixes routed to `dev-frontend` |
| Dependency source inspection | Read installed-version documentation or source only when public types, contracts, and local usage cannot answer the task; keep fetching tools optional. | The active implementation or audit owner, not a new public Skill |
| Implementation | Consume a specification, validate continuously, and review before delivery. | Existing implementation-to-review chain |
| Review | Keep Standards and Spec review independent so one cannot hide the other. | Two-axis evidence inside `repo-review` |
| Codebase design | Prefer deep modules, small interfaces, locality, leverage, and testable seams. | Host planning plus existing audit/review profiles |
| Handoff | Use compact references, explicit continuation state, and redaction discipline. | Host coordination; no duplicate public handoff Skill |

## Methods Not Imported

- Personally branded assistants, installers, or routing packages.
- Provider-specific invocation fields in portable frontmatter; use the supported
  provider adapter while retaining the portable description contract.
- A generic implementation owner that duplicates domain implementation Skills.
- A second review or architecture-review owner.
- Tracker-specific publishing, labels, fixed context-file locations, automatic commits,
  or mandatory delegation.
- Source text or templates from another catalog.

Repository-specific policy is not a portable catalog default. Prototype or handoff
activity never implies commit, push, publication, or external-write authorization.

## Drift Discipline

Public catalogs change names, paths, and workflow composition over time. Recheck a
reference at a fixed revision before using it as evidence, but record only reusable
methods in durable public documentation. Keep source-specific notes in temporary,
ignored review artifacts rather than published Skill packages.
