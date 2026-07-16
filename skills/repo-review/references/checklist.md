# Repository Review Checklist

## 1. Basis and Scope

- [ ] Record repository and requested review goal.
- [ ] Resolve snapshot, base, and head to immutable SHAs.
- [ ] For PRs, read metadata and the complete changed-file set.
- [ ] For packages, verify manifest, order, count, coverage, hashes, exclusions, and final marker.
- [ ] Record included paths, excluded paths, submodules, generated outputs, and unavailable evidence.
- [ ] Stop if the basis is moving, truncated, mismatched, or otherwise unverifiable.
- [ ] If a `repo-map` artifact exists, use it only as navigation and verify finding facts at this basis.

## 2. Project Classification

- [ ] Read nearest repository guidance.
- [ ] Identify actual project classes, manifests, entry points, build systems, and validation commands.
- [ ] Consume `repo-map` entries only as read-set hints; independently verify every fact that affects a finding.
- [ ] Select only applicable profiles.
- [ ] Mark unselected profiles `Out of scope` rather than partially reviewing them.
- [ ] Start from changed paths or explicitly owned snapshot paths; do not repeat onboarding reads that cannot change a review decision.

## 3. Core Repository Profile

When applicable, inspect:

- [ ] manifests, workspace/package membership, feature flags, and lockfiles;
- [ ] entry points, registrations, routes, exports, callers, and consumers;
- [ ] public types, schemas, DTOs, error mappings, and compatibility;
- [ ] migrations, generated files, indexes, release artifacts, and stale references;
- [ ] tests, fixtures, commands, CI, deployment, rollback, and documentation;
- [ ] add/reuse/move/rename/delete lifecycle completeness.

When docs or commands reference a missing path:

- [ ] Resolve it at the immutable review basis, not from the current worktree.
- [ ] Record the documentation source, exact claim, assumed working directory, and revision.
- [ ] Test doc-relative and repository-root-relative interpretation; if the parent is missing, ascend one directory at a time to the nearest existing ancestor.
- [ ] Search only the relevant subtree using basename, symbol, manifest/config, registration, and generated-source evidence.
- [ ] Use history only when needed to classify moved, renamed, missing, ambiguous, generated, or branch-drift state.
- [ ] Report a finding only when the mismatch has concrete impact; otherwise record an alignment gap or `Not verified` evidence.
- [ ] Keep the review read-only and route repo-map repairs to `repo-map`.

## 4. Specialist Delegation

- [ ] Use `audit-frontend` only for a bounded frontend surface.
- [ ] Use `audit-rust` only for selected Rust profiles.
- [ ] Use `audit-security` only for a known security-sensitive surface.
- [ ] Give every specialist exact paths, diff/range, questions, exclusions, and return contract.
- [ ] Keep final scope, cross-domain integration, duplicate removal, severity, and report ownership in `repo-review`.
- [ ] Reject specialist findings that cannot be verified against the fixed basis.

## 5. Standards and Spec Axes

- [ ] Build the Standards source set from effective repository guidance, architecture/contribution docs, selected domain conventions, and non-mutating tool evidence.
- [ ] Locate the originating requirement, issue, PRD, decisions, and acceptance criteria without inferring intent from the diff.
- [ ] Review Standards and Spec independently; use parallel read-only passes only when delegation is available and the fixed scopes are auditable.
- [ ] Mark Spec `Not verified` when no trustworthy source exists.
- [ ] Consolidate duplicates, retain axis labels, and assign one impact-based P0-P3 severity under `repo-review` ownership.

## 6. Finding Quality

For every proposed finding:

- [ ] Identify one root cause rather than several duplicate symptoms.
- [ ] Cite exact file and line, symbol, config key, workflow, or package section.
- [ ] Prove reachability or material relevance.
- [ ] State concrete impact and affected boundary.
- [ ] Select P0-P3 from impact and urgency, not file size or style preference.
- [ ] Provide bounded remediation direction.
- [ ] Provide a verification command, test, runtime check, or artifact inspection.
- [ ] Mark unavailable runtime, CI, deployment, data, or consumer evidence `Not verified`.

## 7. Severity Calibration

- [ ] P0 is catastrophic, active/readily reachable, and immediately blocking.
- [ ] P1 should block merge or release because of high-impact correctness, security, migration, compatibility, or availability risk.
- [ ] P2 is material but bounded or has a practical workaround.
- [ ] P3 has concrete maintenance, test, documentation, or resilience cost.
- [ ] Personal preference, generic best practice, speculative misuse, and file length are not findings.

## 8. Read-Only Boundary

- [ ] No source/config/test/doc/generated-file edits.
- [ ] No formatter or fixer write mode.
- [ ] No staging, commit, checkout, branch, ref, PR, issue, or remote mutation.
- [ ] No PR comments without separate authorization.
- [ ] Accepted fixes are handed to the matching implementation skill.
- [ ] Delivery is handed to `repo-delivery` only after explicit authorization.

## 9. Final Report

- [ ] State immutable review basis.
- [ ] State whether a repo map guided navigation and which finding facts were independently verified.
- [ ] State selected profiles, specialist scopes, and exclusions.
- [ ] Present findings in P0-P3 order.
- [ ] Include location, evidence, impact, remediation, and verification for every finding.
- [ ] Consolidate duplicates.
- [ ] Say `No actionable findings` for empty requested groups.
- [ ] Report commands/evidence, failed checks, residual risks, and all `Not found`/`Not verified` gaps.
