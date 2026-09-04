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
5. Trace registrations, callers, types, data shaping, persistence, generated artifacts,
   runtime config, tests, docs, CI/deploy, and stale references. Load only applicable
   conditional references listed below. For Product/UI/DESIGN/project-map changes, load
   [documentation authority](references/documentation-authority-review.md), resolve
   `<design-root>/DESIGN.md`, and keep Product/UI/DESIGN/Map ownership distinct.
   A projection is relevant only when a named owner, producer, non-LLM consumer,
   semantic version, executable validator, drift policy, and retirement rule are evidenced;
   otherwise reject it as copied authority.
   Adopted component/token review must retain project-native negative tests; optional
   assets remain `Not applicable` when the project has not adopted them.
6. Evaluate two independent axes:
   - **Standards:** repository guidance, architecture, correctness, security, performance, maintainability, and applicable domain conventions.
   - **Spec:** originating requirements, decisions, acceptance criteria, missing behavior, wrong behavior, and unrequested scope.
   If no trustworthy spec exists, mark Spec `Not verified`; do not infer one from the diff.
   A requirement, ADR, schema, test, or acceptance artifact added by the reviewed
   basis is intent evidence unless an independent authority or prior approved contract
   establishes it. It cannot by itself clear replacement, compatibility, migration,
   rollout, or rollback risk.
   Use [Standards and Spec](references/standards-and-spec.md) for axis-specific evidence,
   security confidence, frontend authority tracing, and conditional profile routing.
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
14. Freeze the local verdict before optional external retention or Forgeway delivery
    integration. Load [review integration](references/review-integration.md) only when
    either path is active; neither path may change the frozen local verdict.

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
- Apply visual completion, OpenAPI, frontend CSS/components, documentation authority,
  motion, code quality, and project-grounding gates only through their applicable
  references. Static checks never replace required runtime evidence, and optional
  profiles remain `Not applicable` when their activation conditions are absent.
- Distinguish a real sample-repository defect (`fail` verdict with a P0-P3 finding)
  from a Skill failure (the review process itself broke) and from `Not verified`
  (basis or evidence is incomplete). A real defect is a finding with reachable
  evidence and concrete impact attributed to the selected basis; `Not verified` is
  an honest gap, not a finding. Never fabricate a finding to satisfy a quota or
  convert a basis limitation into a defect.

## Output Contract

Lead with capability, typed refs, mode, basis, scope, exclusions, checks, and P0-P3
findings labeled `Standards`, `Spec`, or both. Preserve finding evidence, impact,
remediation, verification, acceptance refs, and limitations. Report both verdicts;
missing Spec authority stays `Not verified`. Add profile-specific evidence only when
that profile was selected. Finish with the frozen local verdict, separate external
status, residual risks, and gaps.

## References

- Basis: [usage](references/usage.md), [Worktree](references/worktree-checklist.md),
  [fixed basis](references/checklist.md), [Standards/Spec](references/standards-and-spec.md),
  [examples](references/worktree-examples.md).
- Conditional profiles: [protocols](references/protocol-contracts.md),
  [OpenAPI governance](references/openapi-contract-governance.md),
  [frontend CSS governance](references/frontend-css-governance.md),
  [documentation](references/documentation-authority-review.md),
  [motion](references/interaction-motion-review.md),
  [visual evidence](references/frontend-visual-evidence.md),
  [code quality](references/code-quality.md), [design](references/codebase-design.md),
  [UI components and tokens](references/ui-components-and-tokens.md),
  [grounding](references/project-grounding.md).
- Integration: [external evidence, final-result sync, and Forgeway](references/review-integration.md).
- [Eval cases](references/eval-cases.md).
