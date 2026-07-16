---
name: repo-review
description: "Use when a local worktree/index or immutable snapshot, range, pull request, release candidate, or verified package needs read-only review; own local commit-readiness and exact staging guidance or immutable severity-ranked findings."
---

# Repository Review

## Overview

Review repository changes without modifying files, Git, GitHub, or remote state. Select the review basis first, then apply the matching mode. Worktree mode owns dirty-tree classification and commit-readiness guidance; immutable modes own fixed-SHA P0-P3 review. All modes share contract tracing, structural completeness, specialist coordination, evidence quality, and read-only authority.

## Review Basis

Select exactly one basis before conclusions:

- **Worktree/index:** current tracked, untracked, staged, and unstaged state.
- **Repository snapshot:** one tag, branch resolved to SHA, or commit.
- **Commit range:** explicit immutable `base..head` SHAs.
- **Pull request:** metadata plus complete changed-file evidence and resolved base/head SHAs.
- **Release candidate:** immutable candidate revision plus release/config/CI evidence.
- **Review package:** verified manifest, hashes, coverage, exclusions, and final marker.

Do not mix evidence between bases. Current-worktree content is contamination when reviewing another SHA unless explicitly included in the basis.

## Workflow

1. Read effective repository guidance and record the requested review object, scope, output, and non-goals.
2. Fix the basis before conclusions:
   - for Worktree, run status, diff stat/name-status, and cached equivalents when staged content exists;
   - for immutable modes, resolve full SHAs or verify the package manifest and hashes.
3. Build the smallest complete read set from changed or explicitly owned paths. A `repo-map` artifact may guide navigation but is never review proof.
4. In Worktree mode, classify every changed file as `task-owned`, `related-existing`, `unrelated-existing`, `mixed-hunk`, or `unknown` before proposing commit groups.
5. Trace relevant interfaces through registrations, callers, types, data shaping, persistence, generated artifacts, runtime config, tests, docs, CI/deploy, and stale references.
6. Select only applicable frontend, Rust, security, validation, and release profiles. Delegate bounded evidence to `audit-frontend`, `audit-rust`, or `audit-security`; retain scope, integration, deduplication, severity, and final report ownership.
7. Resolve documented path mismatches at the selected basis. If a path or parent is absent, ascend to the nearest existing ancestor and search only the relevant subtree; route repo-map edits to `repo-map`.
8. Reject speculative, unreachable, style-only, duplicate, or already-resolved findings. Rank actionable findings P0-P3 from concrete impact and urgency.
9. Run only non-mutating repository checks needed for the selected basis and risk.
10. In Worktree mode, produce semantic commit groups and exact path- or hunk-level staging guidance for `repo-delivery`. In immutable modes, report merge/release implications without staging guidance.
11. Report exclusions, residual risks, failed checks, and every `Not found` or `Not verified` gap.

## Modes

- **Worktree review:** dirty-tree ownership, mixed hunks, contract completeness, commit readiness, semantic groups, exact staging guidance, and commit messages.
- **Snapshot review:** bounded review of one fixed repository revision.
- **Range review:** `base..head` regressions, contracts, tests, docs, and structural lifecycle.
- **Pull-request review:** complete PR evidence without posting comments unless separately authorized.
- **Release review:** compatibility, migrations, generated artifacts, packaging, CI, deployment, rollback, and security-sensitive configuration.
- **Review-package assessment:** package integrity and evidence coverage before findings.

## Do Not Use For

- Repository mapping or repo-map maintenance; use `repo-map`.
- Future implementation planning; use `code-planner`.
- Root-cause diagnosis of a concrete failure; use `diagnose`.
- A bounded security-only audit when the target surface is already known; use `audit-security`.
- Implementing accepted fixes; use the matching `implement-*` skill.
- Staging, commits, pushes, squash, cleanup, or other Git mutation; use `repo-delivery` after explicit authorization.
- External ChatGPT sending or browser/client operation; use the matching operations skill.

## Hard Rules

- Keep every review read-only. Do not edit, format, stage, unstage, commit, push, change refs, post comments, or create issues/PRs.
- State the review basis and resolved SHAs before immutable conclusions; state complete status/index evidence before Worktree conclusions.
- Never use current-worktree files to clear a finding at another SHA.
- Inventory the full dirty tree even when Worktree scope is narrower, then preserve unrelated changes.
- Mark mixed files `mixed-hunk`; never recommend whole-file staging unless every hunk belongs to the group.
- Do not recommend `git add .`, `git add -A`, directory-wide adds, or broad wildcards unless explicitly approved.
- Do not claim whole-repository, PR, release, or package coverage from partial evidence.
- Do not report findings without reachable evidence and concrete impact.
- Do not approve structural add/reuse/move/rename/delete work while manifests, exports, commands, tests, CI/deploy, docs, indexes, migrations, generated files, consumers, or stale references disagree.
- Treat runtime, CI, deployment, external services, branch policy, and package completeness as `Not verified` unless directly evidenced.

## Output Contract

Lead with mode, basis, scope, exclusions, validation, and severity-ranked findings. Every finding includes exact location, evidence, impact, remediation, and verification. For Worktree mode, also report ownership labels, staged-state risks, semantic commit groups, exact staging approach, validation status, and concise commit messages. For immutable modes, include resolved SHAs, cross-domain integration, merge/release implications, and `No actionable findings` for empty requested groups. Finish with residual risk and all `Not found` or `Not verified` items.

## References

- See [references/usage.md](references/usage.md) for routing and mode examples.
- See [references/worktree-checklist.md](references/worktree-checklist.md) for dirty-tree ownership and commit-readiness review.
- See [references/checklist.md](references/checklist.md) for immutable basis, severity, and release review.
- See [references/worktree-examples.md](references/worktree-examples.md) for commit grouping examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, boundary, scenario, and quality evals.
