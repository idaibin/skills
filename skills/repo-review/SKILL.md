---
name: repo-review
description: "Use when Worktree changes or a fixed snapshot/range need coordinated read-only Standards and Spec findings, documentation-authority review, completed provider-evidence integration, or selected-source visual-completion review; use audit-* for bounded domain audits and a host security workflow for security-only review."
---

# Repository Review

## Overview

Review changes read-only. Select the basis first: Worktree reads current changes;
fixed-basis review normalizes snapshots, ranges, and pull requests to immutable SHAs.

Consume `urn:skills:review-request:v1`; the portable output is
`urn:skills:review-findings:v1`. A compatible immutable
PackageManifest is the preferred dirty/untracked review identity; graph impact queries
bound consumers, while native source/contracts and the selected package remain proof.
The review produces typed findings/Observations, not Requirement state or a Receipt.

## Review Basis

Select exactly one basis before conclusions:

- **Worktree/index:** current tracked, untracked, staged, and unstaged state.
- **Fixed snapshot/range:** one resolved SHA or explicit immutable `base..head`; a pull request is normalized to complete metadata plus resolved base/head SHAs.
- **Review package:** immutable PackageManifest with base/result identity, every
  in-scope file status/hash/mode/bytes including untracked files, aggregate hash,
  exclusions, and validation marker.

Do not mix evidence between bases. Current-worktree content is contamination when reviewing another SHA unless explicitly included in the basis.

## Workflow

1. Read effective repository guidance and record the requested review object, scope, output, and non-goals.
2. Fix the basis before conclusions:
   - for Worktree, run status, diff stat/name-status, and cached equivalents when staged content exists;
   - for fixed-basis review, resolve full SHAs and complete changed-file evidence; for a package, verify its manifest and hashes.
   - For every fixed commit or range, apply the immutable parent/object procedure in
     [references/checklist.md](references/checklist.md). A root-style review is valid
     only when raw commit metadata has no parent and the commit is not a shallow-clone
     boundary that truncates parent history. Missing basis objects fail closed as
     `Not verified`; keep current-source observations separate from basis attribution.
3. Build the smallest complete read set from changed or explicitly owned paths. Use a
   compatible graph reverse-impact/consumer query when available, verify its snapshot
   basis matches the package, and recheck referenced source. A stale graph, query miss,
   or derived map view is never review proof or proof of no downstream impact.
4. In Worktree mode, inventory full status but deeply classify only the requested scope and necessary interface closure. Classify every changed file and mixed hunk only for requested commit-readiness.
5. Trace relevant registrations, callers, types, data shaping, persistence, generated
   artifacts, runtime config, tests, docs, CI/deploy, and stale references. Select the
   protocol-contract profile only for an existing OpenAPI/generated-client pipeline or
   an explicit contract gate. For a selected-source or visual-completion claim, load
   [frontend visual evidence](references/frontend-visual-evidence.md) and validate the
   required handoff plus cited artifacts. For Product/UI/DESIGN/project-map authority
   changes, load [documentation authority](references/documentation-authority-review.md),
   resolve `<design-root>/DESIGN.md`, and keep Product/UI/DESIGN/Map ownership distinct.
   A projection is relevant only when a named owner, producer, non-LLM consumer,
   semantic version, executable validator, drift policy, and retirement rule are evidenced;
   otherwise reject it as copied authority.
   For applicable runtime, packaging, integration, durable-data, replacement,
   auth/security, or cross-repository risk, load
   [project grounding](references/project-grounding.md) and bind its evidence to this
   basis; do not widen scope from signals alone.
6. Evaluate two independent axes:
   - **Standards:** repository guidance, architecture, correctness, security, performance, maintainability, and applicable domain conventions.
   - **Spec:** originating requirements, decisions, acceptance criteria, missing behavior, wrong behavior, and unrequested scope.
   If no trustworthy spec exists, mark Spec `Not verified`; do not infer one from the diff.
   A requirement, ADR, schema, test, or acceptance artifact added by the reviewed
   basis is intent evidence unless an independent authority or prior approved contract
   establishes it. It cannot by itself clear replacement, compatibility, migration,
   rollout, or rollback risk.
   For material security claims, apply
   [Standards and Spec](references/standards-and-spec.md), keeping evidence confidence
   separate from severity. For visual/UI-contract changes, trace product authority ->
   selected-source UI authority -> DESIGN.md -> adapters -> runtime evidence. Load
   [interaction and motion](references/interaction-motion-review.md) only for changed
   motion, gesture, transition ownership, or user-visible feedback. Load
   [code quality](references/code-quality.md) only when its maintainability signals
   materially apply, and attribute them to the fixed basis. Use compatible graph
   queries only for navigation/impact bounding; keep missing authority and runtime
   proof independently `Not verified`.
7. Keep the two evidence passes independent. They may run in parallel only when delegation is available, both scopes are read-only and fixed, and the coordinator can verify and integrate their results.
8. Select only applicable profiles. Delegate bounded frontend, Java, or Rust work only
   when requested or necessary. Route security-only work to a host security workflow.
   Verify completed provider evidence against this basis before integrating it.
9. Resolve documented path mismatches at the selected basis. If a path or parent is
   absent, ascend to the nearest existing ancestor and search only the relevant
   subtree; report graph drift for a later `repository.asset.scan` refresh without
   mutating graph or documentation during review.
10. Reject speculative, unreachable, style-only, duplicate, or already-resolved findings. Consolidate both axes into P0-P3 findings from concrete impact and urgency while retaining each finding's axis.
11. Run only non-mutating repository checks needed for the selected basis and risk.
    After any fix, freeze a new complete Worktree or immutable basis and replay the
    affected checks; a verdict from the old basis cannot clear new changes.
12. Produce semantic groups, commit messages, and exact staging guidance only when the Worktree commit-readiness profile was requested. Add the Release profile only for an explicit release candidate/readiness question.
13. Report exclusions, residual risks, failed checks, and every `Not found` or `Not verified` gap. Keep an authorized external-review status separate from the local verdict: a submitted request with no attributed response neither creates nor clears a finding.
14. Freeze the local verdict before optional post-terminal action. An explicitly
    persisted `ask-ai` `final-result-sync` receives only that sanitized frozen result;
    its outcome is not review evidence and cannot change the verdict.
15. When Forgeway delivery integration is active, bind the review capability, exact
    input/result PackageManifest, graph snapshot/query refs, scope, and spec refs to an
    immutable Run. Import every local or accepted external finding/result as a typed
    Observation against that exact package. A new Attempt/result package makes prior
    downstream review observations stale; never rewrite them or hand-edit a Gate.

## Modes

- **Worktree review:** full status inventory and bounded findings; optionally activate commit-readiness for ownership, mixed hunks, logical groups, exact staging guidance, and messages.
- **Fixed-basis review:** one immutable snapshot or `base..head` range; normalize a pull request to this basis before findings.
- **Review-package assessment:** package integrity and evidence coverage before findings.
- **Release profile (conditional):** for explicit release readiness, add compatibility, migrations, generated artifacts, packaging, CI, deployment, rollback, and security configuration to a fixed basis.

## Do Not Use For

- Repository mapping or repo-map maintenance; use `repo-map`.
- Future implementation planning; use the host's built-in planning.
- Business-domain modeling without a change basis; use `domain-modeling`.
- Root-cause diagnosis of a concrete failure; use the host's built-in diagnosis under effective instructions.
- A direct bounded frontend-only, Java-only, or Rust-only audit with no Worktree/index, immutable review basis, or cross-surface coordination; use the matching `audit-*` Skill. When a review basis exists, keep `repo-review` as coordinator.
- Security-only repository/path scans or Git change scans; use the matching host
  security workflow. Keep this Skill when security is one axis of a broader review or
  when integrating completed scan evidence into its fixed-basis verdict.
- Implementing accepted fixes; use the matching `dev-*` skill.
- Staging, commits, pushes, squash, cleanup, or other Git mutation; use `repo-delivery` after explicit authorization.
- External ChatGPT sending or browser/client operation; use the matching operations skill.

## Hard Rules

- Keep every review read-only. Do not edit, format, stage, unstage, commit, push, change refs, post comments, or create issues/PRs.
- State the review basis and resolved SHAs before immutable conclusions; state complete status/index evidence before Worktree conclusions.
- Never use current-worktree files to clear a finding at another SHA.
- Inventory full Worktree status, preserve unrelated changes, and reserve complete ownership/mixed-hunk classification for commit-readiness.
- Mark mixed files `mixed-hunk`; never recommend whole-file staging unless every hunk belongs to the group.
- Do not recommend `git add .`, `git add -A`, directory-wide adds, or broad wildcards unless explicitly approved.
- Do not claim whole-repository, PR, release, or package coverage from partial evidence.
- Do not report findings without reachable evidence and concrete impact.
- Do not block or approve from diff size, annotations, file names, literals, or scanner
  matches alone; use them only to activate bounded evidence checks.
- Treat scanner matches, dangerous APIs, dependency presence, and incomplete
  source-to-sink paths as candidates, not validated vulnerabilities. Verify any
  provider result against this review basis before it affects the verdict.
- Do not turn unchanged repository debt, optional lint advice, code size, or a
  language/framework signal into a finding against the selected basis. Prove
  whether the basis introduces, expands, exposes, or directly depends on it. Label
  the relationship as `introduced`, `expanded`, `exposed`, `pre-existing but
  blocking`, or `Not verified`; do not attribute nearby debt to the basis.
- Do not approve structural add/reuse/move/rename/delete work while manifests, exports, commands, tests, CI/deploy, docs, indexes, migrations, generated files, consumers, or stale references disagree.
- Treat runtime, CI, deployment, external services, branch policy, and package completeness as `Not verified` unless directly evidenced.
- A pending, timed-out, empty, or unattributed external review cannot change the local
  verdict; report that axis separately `Not verified`. Final-result retention is not
  an external review axis and cannot add, clear, or reprioritize findings.
- Do not activate frontend design compliance merely because a repository contains
  frontend files. It is conditional on visual or UI-contract change scope, does not
  create another review profile, and does not require `audit-frontend`.
- Do not approve a selected-source visual-completion claim from build/lint/typecheck, source CSS, current-runtime similarity, or one screenshot. Require traceable source targets, complete implementation mapping, two same-viewport/state comparison passes, computed runtime evidence, and every specified breakpoint/state required by the contract; otherwise report `Partial` or `Not Ready`.
- Do not require OpenAPI for ordinary REST changes. When the protocol-contract
  profile applies, fix its Git/authority/artifact basis and replay write-mode
  generation only in an isolated copy; otherwise review the repository-native
  route/DTO/client/test chain and mark OpenAPI `Not applicable`.
- Do not approve a documentation rebuild while durable docs still contain
  superseded decisions, task-time evidence, duplicate authorities, stale indexes,
  Skill-development reports, or machine sidecars without proven lifecycle owners.
- Distinguish a real sample-repository defect (`fail` verdict with a P0-P3 finding)
  from a Skill failure (the review process itself broke) and from `Not verified`
  (basis or evidence is incomplete). A real defect is a finding with reachable
  evidence and concrete impact attributed to the selected basis; `Not verified` is
  an honest gap, not a finding. Never fabricate a finding to satisfy a quota or
  convert a basis limitation into a defect.

## Output Contract

Lead with capability `repository.change.review`, typed review-findings/Observation refs,
Run, PackageManifest and graph query refs when integration is active, then mode/profile,
basis, scope, exclusions, and validation, followed by severity-ranked P0-P3 findings
labeled `Standards`, `Spec`, or both. Every finding includes location, requirement when
available, evidence, impact, remediation, and verification. Security findings also
state evidence status, proof gaps, and any provider/method used; `fixed` requires a new
reviewed basis and replay of the original validation path. Include Standards and Spec
verdicts; mark missing specification evidence `Not verified`. For the visual-completion
profile, report schema validation, source/revision/approval, evidence coverage, both
comparison passes, runtime geometry/style checks, breakpoint/state gaps, and whether
the completion claim is supported. Add ownership labels, staged risks, logical groups,
staging, and messages only for Worktree commit-readiness. Fixed-basis review includes
resolved SHAs; release implications appear only when the Release profile was selected.
Finish with the local verdict, separate external-review status when applicable,
residual risk, and gaps. An explicitly requested independent external
challenge/research may hand the fixed basis/question to `ask-ai`; it never implies
sending. When a valid persisted final-result sync applies, report its separate
receipt/incomplete state only after the frozen local verdict.

## References

- See [references/usage.md](references/usage.md) for routing and mode examples.
- See [references/worktree-checklist.md](references/worktree-checklist.md) for dirty-tree ownership and commit-readiness review.
- See [references/checklist.md](references/checklist.md) for immutable basis, severity, and release review.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only for an existing or explicitly requested OpenAPI/generated-client review gate.
- See [references/standards-and-spec.md](references/standards-and-spec.md) for independent Standards and Spec review axes.
- Read [references/documentation-authority-review.md](references/documentation-authority-review.md)
  when the basis changes authoritative documentation structure or claims a terminal
  documentation rebuild.
- Read [references/interaction-motion-review.md](references/interaction-motion-review.md)
  only when the selected basis adds or changes motion, gesture behavior, transition
  ownership, or user-visible interaction feedback.
- Read [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) for the conditional visual-completion profile; validate staged handoffs offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json).
- Read [references/code-quality.md](references/code-quality.md) when the basis
  materially involves duplication, dead or unused code, abstractions, hidden
  coupling, or maintainability.
- See [references/codebase-design.md](references/codebase-design.md) only when the fixed change basis materially affects a public module/interface, seam, abstraction, locality, or testability.
- Read [references/project-grounding.md](references/project-grounding.md) when the
  review basis activates runtime/config, packaging, public integration, durable data,
  replacement, auth/security, or cross-repository delivery risk.
- See [references/worktree-examples.md](references/worktree-examples.md) for commit grouping examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, boundary, scenario, and quality evals.
