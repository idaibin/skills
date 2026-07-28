# Execution Durability

Use this profile only when the user has authorized local commits while a large task is
still in progress. Authorization may name one action or establish a bounded standing
plan for the task branch. Implementation wording, task size, elapsed time, or a risky
next command never creates a plan by itself.

## Bounded Task Plan

At task start or before the first milestone, one authorization may record:

- the non-default task branch and owned path/hunk boundary;
- allowed semantic milestones, targeted fixups, and whether exceptional checkpoints
  are permitted;
- event triggers such as a completed validated slice, module handoff, or named
  high-risk operation;
- focused validation floor and commit-message policy;
- whether remote push is forbidden or separately authorized for the task branch.

Matching commits may proceed without repeated confirmation. Reconfirm when the branch,
owned scope, commit type, validation floor, remote action, or risk changes materially.

## Select One Commit Type

- **Semantic milestone:** one completed, independently understandable slice whose
  implementation, tests, docs, migrations, and generated outputs are synchronized for
  that slice. Focused validation passes or its exact limitation is recorded.
- **Targeted fixup:** one correction belongs to exactly one reachable milestone and a
  later normalization step is intended. Otherwise create a normal semantic correction.
- **Safety checkpoint:** incomplete task-owned work faces a concrete loss or difficult
  recovery risk. This is exceptional and cannot run on a default/protected branch.

Prefer milestone over fixup, fixup over checkpoint, and any authorized semantic commit
over leaving a separable validated slice indefinitely mixed into later work. Never
create commits on a timer or from implementation authorization alone.

## Commit Gate

1. Verify a non-default task branch, per-action or still-valid bounded-plan authority,
   task-owned paths or hunks, and no unrelated staged content.
2. Record staged, unstaged, untracked, and unrelated content before staging.
3. Reuse slice evidence and run focused validation when possible. A checkpoint may
   record failure or `Not verified`; it must not disguise incomplete work as passing.
4. Stage exact paths or hunks and inspect cached stat, name-status, and full diff.
5. Use a durable semantic message. A checkpoint message identifies the preserved
   scope; repository policy still controls message format.
6. Commit, recheck the full Worktree, and report what the commit protects, what remains
   uncommitted, and what unrelated content was preserved.
7. Stop. Push requires separate authorization and remote proof.

## Required State

Record `lifecycle: execution-durability`, authorization basis, commit type/SHA, exact scope, validation,
`review_state: slice-validated|checkpoint-only`, normalization disposition, remaining
Worktree content, and `durability: local-only|pushed`. Local-only never means machine-
or remote-level backup.

A checkpoint disposition is always `split-or-absorb-required` until final history is
normalized. A fixup records one target SHA. A milestone is only a preserve candidate;
final review may still require it to be split, folded, reordered, or corrected.
