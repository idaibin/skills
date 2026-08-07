# Skills Release Profile

Use this conditional profile when the fixed delivery scope is one or more public Skill packages plus the catalog surfaces required by the owning Skills repository. This profile does not own Skill design, source edits, validation policy, or runtime installation; it consumes accepted evidence, owns authorized Git delivery, and hands any separately authorized installation to its runtime owner.

## Required Basis

Before staging, require all of the following:

- the exact package allowlist and every required catalog/index/eval/documentation path;
- the effective repository instructions and current package standard;
- a cleanly identified fixed source basis, with unrelated dirty work excluded;
- the repository's canonical Skills gate passing on that basis, not only a direct validator or package-local test;
- package-specific executable tests when the package ships scripts;
- accepted fixed-basis review evidence;
- the intended Git target and separate authorization for stage, commit, push, integration, or cleanup.

If the canonical gate changes files, exposes catalog drift, or invalidates the review basis, stop and return to the source owner. Do not repair or broad-stage validation drift inside delivery.

## Delivery Sequence

1. Record source branch, HEAD, tree, status, exact package/catalog scope, canonical-gate command and result, and accepted review basis.
2. Classify the release as one semantic catalog intent unless the accepted basis contains independently releasable packages with explicit separate history requirements.
3. Stage exact accepted paths or hunks only. Inspect cached stat, name-status, and full diff; compare it with the declared allowlist.
4. Perform only the authorized Git actions. Verify the resulting local commit and, when authorized, the exact remote ref/SHA.
5. Do not create a tag, hosted release, pull request, or registry publication unless a separate owning workflow and explicit authorization cover it.

## Post-Delivery Runtime Handoff

Global installation or runtime refresh is not implied by Git delivery and is not performed by this profile. When the user separately authorizes installation, hand off:

- the immutable delivered source/ref, never an unreviewed Worktree;
- the exact package and runtime allowlist;
- the repository-documented install command and restart/reload expectation;
- required source/installed parity, discovery, and routing evidence.

Record the runtime owner's returned paths and parity evidence, or `Not verified`. Installation failure does not justify rewriting Git history or editing source inside this profile.

## Release Evidence Contract

Add these fields to the Delivery Report:

- `Packages`: exact package allowlist and catalog support paths;
- `Canonical Gate`: command, exit result, and fixed basis;
- `Package Tests`: executable package checks and results;
- `Review Basis`: immutable reviewed base/head or commit;
- `Git Proof`: commit and remote ref when pushed;
- `Runtime Install`: handoff owner and status, or `Not authorized`;
- `Parity`: returned comparison method and result, or `Not verified`;
- `Residual Gaps`: hosted publication, other runtimes, live host/model/browser behavior, or reload state.
