---
name: repo-audit
description: "Use when a known frontend, Java, or Rust surface needs a scoped, read-only audit of existing architecture, ownership, state, transactions, concurrency, persistence, performance, accessibility, visual fidelity, build/tooling, or unsafe boundaries without a change basis; select one or more language profiles; use repo-review when a Worktree or immutable change basis needs coordination."
---

# Repository Audit

Audit existing engineering from repository evidence rather than a universal
template or an external reference repository. Detect the real languages,
frameworks, and local contracts, then select only the profiles required by the
request. This Skill is read-only: use it directly for bounded domain audits or
as a bounded specialist under `repo-review`; use the matching `dev-*` owner for
requested changes.

Consume `urn:skills:audit-request:v1`; the portable output is
`urn:skills:audit-findings:v1`. When supplied, consume an exact
PackageManifest/basis plus compatible graph asset/consumer/impact results. The
audit produces findings and validation Observations, not Task/Requirement
status or a delivery Receipt. It audits the current state of a declared scope
and never attributes findings to a change; `repo-review` owns fixed-basis
change attribution.

## Rule Priority

Resolve conflicts in this order:

1. The user's current explicit request.
2. Effective repository guidance, including `AGENTS.md`, `CLAUDE.md`, and
   host-provided instructions when present.
3. Declared and applicable product/UI contracts: product requirements or
   product Feature Specs define behavior and acceptance; selected-source UI
   Feature Specs and resolved `<design-root>/DESIGN.md` define applicable UI
   and shared visual semantics.
4. Live code, toolchain, configuration, and the repository-declared system
   define current implementation facts. They do not override an applicable
   contract; report a conflict as implementation drift.
5. This Skill and its selected profiles.
6. External reference repositories.

Never rewrite a working local structure merely to match this Skill or an
external repository. Open-source references form questions, not
target-repository defects by stylistic comparison.

## Workflow

1. Resolve the audit scope: repository/build root, module, surface, and the
   requested outcome. Read effective guidance, record the inspected revision
   plus relevant Worktree state for reproducibility, and run `git status
   --short`. This inspection snapshot does not turn the audit into change
   attribution. When `repo-review` delegates paths or a diff, record the exact
   boundary and keep the caller as review coordinator. Stop with
   `scope-ambiguous` when the target surface cannot be determined.
2. Select exactly one or more language profiles for the audited surface and
   load only those profiles:
   - [frontend profile](references/frontend-profile.md) for a browser-facing
     frontend surface;
   - [java profile](references/java-profile.md) for Java source or Java-owned
     Spring/build configuration;
   - [rust profile](references/rust-profile.md) for a Rust workspace or
     subsystem.
   A repository containing multiple languages gets one profile per audited
   surface, not a default whole-repository sweep. Do not audit language
   semantics that no profile owns, such as Kotlin, Groovy, or Scala source; a
   bounded framework/configuration audit may proceed only when those language
   risks are explicitly excluded.
3. Within each selected language profile, follow its framework, runtime, and
   risk-profile selection rules. State every selected profile and mark every
   unselected profile `Out of scope`. A query miss never proves absence, and a
   derived Markdown view is not audit evidence.
4. Map each selected responsibility to its concrete owner: page, feature,
   primitive, service, store, schema, module, crate, command, migration, or
   adapter. Consume a compatible graph asset/consumer/impact query when
   supplied; reject stale or mismatched graph results and reproduce a bounded
   targeted inventory instead.
5. Gate every candidate finding on: reachable path or material relevance,
   concrete impact, precise owner and location, attribution limited to the
   declared audit scope, counterevidence, and a falsifiable validation seam.
   Checklist-only matches, style preferences, and external-repository
   comparison do not satisfy this gate. When code-quality concerns materially
   apply, load [code quality](references/code-quality.md) with audit
   semantics; load [codebase design](references/codebase-design.md) for a
   selected module/API/testability audit.
6. When the selected surface crosses reachable runtime/configuration,
   packaging, public contracts, durable data, replacement compatibility,
   auth/security, deployment, or another repository, load
   [project grounding](references/project-grounding.md) and bound the audit
   through its signal-to-evidence chain. Activate it from semantic
   reachability, never from directories, framework presence, or literals
   alone.
7. Validate with non-mutating repository-defined commands and representative
   data. Do not run known apply/fix or tracked-source generation commands in
   the audited Worktree. If the repository offers only write-capable
   validation, skip it and report the gap or hand it to a workflow with an
   isolated Worktree. With explicit authorization, use only test-owned
   ephemeral containers, databases, brokers, or processes; never write shared,
   staging, or production state. Recheck status/diff afterward. If an
   otherwise non-mutating command creates tracked drift, stop validation,
   report the exact contamination, mark affected evidence `Not verified`, and
   do not revert it without explicit authorization. Request browser or
   real-client evidence through `ops-browser`/`ops-client` only when a
   selected claim cannot be proven statically. Compilation alone does not
   prove authorization, rollback, migration, query, concurrency, or runtime
   behavior.
8. Stop when the selected profiles are supported by evidence or explicitly
   blocked. Do not perform shallow checks for excluded profiles merely to
   imply coverage.
9. Report severity-ranked P0-P3 findings with exact location, profile-specific
   evidence, impact, remediation owner/direction, validation gap, selected
   profiles, and excluded profiles. In specialist mode, return findings to the
   coordinating `repo-review` without issuing the final readiness verdict.
10. When Forgeway delivery integration is active, bind the audit to an
    immutable Run, exact input/result PackageManifest, and typed input refs.
    Attach each finding or validation result as an Observation against that
    exact package. Do not hand-edit a Gate, rewrite prior Observations after a
    retry, or infer reviewed/delivered state.

## Hard Rules

- Resolve toolchain, layout, ownership, and API expectations from repository
  evidence, not machine defaults, framework convention, or a reference
  project's structure. Treat annotations, dependencies, scanner matches,
  lints, and code shape as signals that still require reachability, impact,
  and counterevidence.
- Select profiles before applying detailed checklists and load only the
  selected language, framework, and risk references. Do not cross-apply an
  unselected profile or imply its coverage.
- Separate source/config evidence from packaged and rendered-runtime proof;
  report unsupported claims as `Not verified`, not generic defects. Use `Not
  found` only for a searched-for repository fact that is absent.
- Do not claim dependency vulnerability, exploitability, secret exposure, or
  complete security coverage without the matching evidence. When a selected
  profile exposes a security-relevant condition, return the domain evidence,
  authoritative control boundary, counterevidence, and proof gap without
  claiming exploit validation or fix completion; route an explicit
  vulnerability scan, attack-path, or PoC-validation request to an available
  host security workflow.
- Do not edit, stage, commit, post review comments, or deliver code in audit
  mode. Route accepted remediation to the matching `dev-*` owner.
  `repo-review` owns Worktree and immutable review coordination;
  `repo-delivery` alone owns Git mutation.

## Do Not Use For

- Repository orientation, commands, reuse inventory, or docs/code alignment
  without an audit request; use `repo-map`.
- Implementation, modification, refactoring, or migration in any profiled
  language; use `dev-frontend`, `dev-typescript`, `dev-java`, or `dev-rust`.
- Root-cause diagnosis of a concrete failure; use the host's built-in
  diagnosis under effective instructions.
- Owning Worktree readiness or immutable repository/range/PR/release
  coordination; use `repo-review`, which may delegate a bounded surface here.
- Actual staging, commit, rebase/squash, push, or delivery; use
  `repo-delivery`.
- Browser or real desktop runtime operation; use `ops-browser` or
  `ops-client`.
- Creating a resolved `<design-root>/DESIGN.md` or selected-source Feature
  Specs; use `ui-spec`.
- A general repository/path vulnerability scan or explicit exploit validation;
  use an available host security workflow.

## Output Contract

Lead with one capability ID per selected language profile
(`frontend.surface.audit`, `java.surface.audit`, `rust.surface.audit`), typed
audit-findings/Observation refs, Run and PackageManifest refs when integration
is active, the inspection snapshot, selected language/framework/risk profiles,
explicitly excluded profiles, and the coordinating owner when delegated. For
each finding, report impact, exact location, profile-specific evidence,
counterevidence, remediation owner/direction, and validation gap. Then
summarize inspected guidance/manifests/source/tests/commands, existing reuse
candidates, the ownership map, selected-profile evidence, commands and
ephemeral resources used, cleanup, and all `Not found` or `Not verified`
residual risks. Mark each profile's applicability (`Applicable`/`Not
applicable`) separately from its evidence status (`Verified`/`Failed`/`Not
verified`).

## References

- Language profiles: [frontend](references/frontend-profile.md),
  [Java](references/java-profile.md), [Rust](references/rust-profile.md).
- Shared depth: [code quality](references/code-quality.md),
  [codebase design](references/codebase-design.md),
  [grounding](references/project-grounding.md),
  [OpenAPI governance](references/openapi-contract-governance.md).
- Frontend specialty: [architecture](references/frontend-architecture-and-ownership.md),
  [frameworks](references/frontend-framework-profiles.md),
  [components](references/frontend-component-system.md),
  [state/data/forms](references/frontend-state-data-and-forms.md),
  [layout/style](references/frontend-styling-and-layout.md),
  [styling systems](references/frontend-styling-systems.md),
  [CSS governance](references/frontend-css-governance.md),
  [layout governance](references/frontend-layout-governance.md),
  [visual evidence](references/frontend-visual-evidence.md),
  [visual direction](references/visual-direction-and-anti-slop.md),
  [DESIGN.md](references/frontend-design-md-compliance.md),
  [specs](references/specification-authorities.md),
  [protocol contracts](references/frontend-protocol-contracts.md),
  [Tauri](references/frontend-desktop-tauri.md),
  [accessibility/performance](references/frontend-accessibility-and-performance.md),
  [build](references/frontend-build-tooling.md),
  [checklist](references/frontend-review-checklist.md),
  [anti-patterns](references/frontend-anti-patterns.md),
  [sources](references/frontend-reference-corpus.md).
- Java specialty: [Java engineering](references/java-engineering.md),
  [protocol contracts](references/java-protocol-contracts.md),
  [checklist](references/java-checklist.md).
- Rust specialty: [architecture](references/rust-architecture-and-modules.md),
  [baseline/lifecycle](references/rust-project-baseline-and-lifecycle.md),
  [ownership](references/rust-ownership-and-resources.md),
  [errors/API](references/rust-errors-and-api-design.md),
  [web/desktop boundaries](references/rust-web-and-desktop-boundaries.md),
  [agent runtime](references/rust-agent-runtime-profile.md),
  [async/concurrency](references/rust-async-and-concurrency.md),
  [performance](references/rust-performance.md),
  [memory](references/rust-memory.md),
  [SQLite](references/rust-sqlite.md),
  [testing](references/rust-testing-and-quality.md),
  [unsafe/security](references/rust-unsafe-and-security.md),
  [checklist](references/rust-review-checklist.md),
  [anti-patterns](references/rust-anti-patterns.md),
  [sources](references/rust-reference-corpus.md).
- Evaluation: [eval cases](references/eval-cases.md),
  [frontend scenarios](references/frontend-eval-scenarios.md),
  [Java scenarios](references/java-eval-scenarios.md),
  [Rust scenarios](references/rust-eval-scenarios.md).
