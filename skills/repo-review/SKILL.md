---
name: repo-review
description: "Use when current Worktree changes or a fixed snapshot/range, including a resolved pull request, need read-only findings; add commit-readiness only when requested and release checks only as a conditional profile."
---

# Repository Review

## Overview

Review repository changes without modifying files, Git, GitHub, or remote state. Select the basis first. Worktree reads current staged/unstaged/untracked changes; it does not manage worktrees. Fixed-basis review normalizes snapshots, ranges, and pull requests to immutable SHA evidence. Commit-readiness and release checks are conditional profiles, not default review ceremony.

## Review Basis

Select exactly one basis before conclusions:

- **Worktree/index:** current tracked, untracked, staged, and unstaged state.
- **Fixed snapshot/range:** one resolved SHA or explicit immutable `base..head`; a pull request is normalized to complete metadata plus resolved base/head SHAs.
- **Review package:** verified manifest, hashes, coverage, exclusions, and final marker.

Do not mix evidence between bases. Current-worktree content is contamination when reviewing another SHA unless explicitly included in the basis.

## Workflow

1. Read effective repository guidance and record the requested review object, scope, output, and non-goals.
2. Fix the basis before conclusions:
   - for Worktree, run status, diff stat/name-status, and cached equivalents when staged content exists;
   - for fixed-basis review, resolve full SHAs and complete changed-file evidence; for a package, verify its manifest and hashes.
3. Build the smallest complete read set from changed or explicitly owned paths. A `repo-map` artifact may guide navigation but is never review proof.
4. In Worktree mode, inventory full status but deeply classify only the requested scope and necessary interface closure. Classify every changed file and mixed hunk only for requested commit-readiness.
5. Trace relevant interfaces through registrations, callers, types, data shaping, persistence, generated artifacts, runtime config, tests, docs, CI/deploy, and stale references. Activate the protocol-contract profile only for an existing OpenAPI/generated-client pipeline or an explicitly requested contract gate.
6. Evaluate two independent axes:
   - **Standards:** repository guidance, architecture, correctness, security, performance, maintainability, and applicable domain conventions.
   - **Spec:** originating requirements, decisions, acceptance criteria, missing behavior, wrong behavior, and unrequested scope.
   If no trustworthy spec exists, mark Spec `Not verified`; do not infer one from the diff.
7. Keep the two evidence passes independent. They may run in parallel only when delegation is available, both scopes are read-only and fixed, and the coordinator can verify and integrate their results.
8. Select only applicable profiles. Delegate a bounded specialist audit only when the user requests it or an independently necessary evidence result cannot be obtained efficiently by the coordinator; otherwise apply the profile internally. Retain integration, deduplication, severity, and final ownership.
9. Resolve documented path mismatches at the selected basis. If a path or parent is absent, ascend to the nearest existing ancestor and search only the relevant subtree; route repo-map edits to `repo-map`.
10. Reject speculative, unreachable, style-only, duplicate, or already-resolved findings. Consolidate both axes into P0-P3 findings from concrete impact and urgency while retaining each finding's axis.
11. Run only non-mutating repository checks needed for the selected basis and risk.
12. Produce semantic groups, commit messages, and exact staging guidance only when the Worktree commit-readiness profile was requested. Add the Release profile only for an explicit release candidate/readiness question.
13. Report exclusions, residual risks, failed checks, and every `Not found` or `Not verified` gap.

## Modes

- **Worktree review:** full status inventory and bounded findings; optionally activate commit-readiness for ownership, mixed hunks, logical groups, exact staging guidance, and messages.
- **Fixed-basis review:** one immutable snapshot or `base..head` range; normalize a pull request to this basis before findings.
- **Review-package assessment:** package integrity and evidence coverage before findings.
- **Release profile (conditional):** for explicit release readiness, add compatibility, migrations, generated artifacts, packaging, CI, deployment, rollback, and security-sensitive configuration to a fixed basis.

## Do Not Use For

- Repository mapping or repo-map maintenance; use `repo-map`.
- Future implementation planning; use the host's built-in planning.
- Business-domain modeling without a change basis; use `domain-modeling`.
- Root-cause diagnosis of a concrete failure; use the host's built-in diagnosis under effective instructions.
- A direct bounded frontend-only, Rust-only, or security-only audit with no Worktree/index, immutable review basis, or cross-surface coordination; use the matching `audit-*` Skill. When such a basis exists, keep `repo-review` as coordinator and delegate only the bounded specialist surface when needed.
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
- Do not approve structural add/reuse/move/rename/delete work while manifests, exports, commands, tests, CI/deploy, docs, indexes, migrations, generated files, consumers, or stale references disagree.
- Treat runtime, CI, deployment, external services, branch policy, and package completeness as `Not verified` unless directly evidenced.
- Do not require OpenAPI for ordinary REST changes. When the protocol-contract
  profile applies, fix its Git/authority/artifact basis and replay write-mode
  generation only in an isolated copy; otherwise review the repository-native
  route/DTO/client/test chain and mark OpenAPI `Not applicable`.

## Output Contract

Lead with mode/profile, basis, scope, exclusions, and validation, then severity-ranked P0-P3 findings labeled `Standards`, `Spec`, or both. Every finding includes location, requirement when available, evidence, impact, remediation, and verification. Include Standards and Spec verdicts; mark missing specification evidence `Not verified`. Add ownership labels, staged risks, logical groups, staging, and messages only for Worktree commit-readiness. Fixed-basis review includes resolved SHAs; release implications appear only when the Release profile was selected. Finish with the verdict, residual risk, and gaps. An explicitly requested independent external challenge/research may hand the fixed basis/question to `ask-chatgpt`; it never implies sending.

## References

- See [references/usage.md](references/usage.md) for routing and mode examples.
- See [references/worktree-checklist.md](references/worktree-checklist.md) for dirty-tree ownership and commit-readiness review.
- See [references/checklist.md](references/checklist.md) for immutable basis, severity, and release review.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only for an existing or explicitly requested OpenAPI/generated-client review gate.
- See [references/standards-and-spec.md](references/standards-and-spec.md) for independent Standards and Spec review axes.
- See [references/codebase-design.md](references/codebase-design.md) only when the fixed change basis materially affects a public module/interface, seam, abstraction, locality, or testability.
- See [references/worktree-examples.md](references/worktree-examples.md) for commit grouping examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, boundary, scenario, and quality evals.
