# AICraft Skills Review

> Historical record archived from the repository root. Conclusions, branch
> names, revisions, and runtime evidence below describe the original review
> passes and are not current repository guidance.

## Review Pass 1

- Timestamp: 2026-07-10T23:39:55+08:00
- Repository: `idaibin/aicraft`
- Branch: `refact/skill-quality-hardening`
- Base: `23d30ccd1362d177943dbb39c79abebbd1c36f97`
- Head: `0eab9ef951292485c5ece5e0ca6727d048f50db1`
- Artifact visibility: `repository-sanitized`
- Surface: ChatGPT Project
- Conversation reference: `suffix-8348f12b`
- Account workspace: `personal`
- Browser route: Codex in-app Browser
- Input: one pasted-text attachment, 762,944 characters, intended to contain the fixed-range diff and 47 complete core files
- Reviewer workflow requested: `repo-review`

### Reviewer Verdict

`PASS` — no actionable findings. No P0, P1, P2, or P3 findings were reported.

### Skill Scores

| Skill | Trigger/Routing | Boundary/Safety | Workflow | Metadata Sync | Eval Quality | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| code-context | 10 | 10 | 9 | 10 | 9 | 9.6 |
| code-planner | 10 | 10 | 10 | 10 | 10 | 10.0 |
| diagnose | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-review | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-delivery | 10 | 10 | 10 | 10 | 10 | 10.0 |
| implement-frontend | 10 | 10 | 10 | 10 | 10 | 10.0 |
| audit-frontend | 10 | 10 | 10 | 10 | 10 | 10.0 |
| implement-rust | 10 | 10 | 10 | 10 | 10 | 10.0 |
| audit-rust | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-security | 10 | 10 | 10 | 10 | 10 | 10.0 |
| ops-browser | 10 | 10 | 9 | 10 | 10 | 9.8 |
| ops-client | 10 | 10 | 9 | 10 | 10 | 9.8 |
| chatgpt-review | 10 | 10 | 9 | 10 | 10 | 9.8 |
| human-writing | 10 | 10 | 10 | 10 | 10 | 10.0 |

All dimensions are at least 9.

### Reviewer Residual Risks

- Host-provided browser and desktop adapter behavior remains environment-dependent.
- Static metadata validation cannot prove actual model routing behavior.
- Windows UI Automation and Linux AT-SPI adapters were not executed.
- Rust Miri, sanitizer, fuzz, stress, and target-adapter checks were not applicable to this documentation review.

### Codex Verification

- Confirmed the reviewed branch and head are unchanged from the submitted package.
- `python3 scripts/validate-skills.py`: passed.
- `python3 scripts/test_validate_skills.py`: passed, 7 tests.
- `python3 scripts/validate-skills.py --quality-report`: passed for all 14 skill packages.
- `git diff --check 23d30ccd1362d177943dbb39c79abebbd1c36f97..HEAD`: passed.
- No reviewer finding required a code fix.
- The Project conversation, sanitized conversation reference, single attachment, composer state, submission, and response completion were verified in the live bridge run.
- Multipart integrity was not verified because this legacy pass used one oversized attachment; its coverage claim is superseded by Review Pass 3.

## Review Pass 2

- Timestamp: 2026-07-10T23:41:44+08:00
- Review range: unchanged at `23d30ccd1362d177943dbb39c79abebbd1c36f97..0eab9ef951292485c5ece5e0ca6727d048f50db1`
- Reviewer workflow: `repo-review`
- Verdict: `SECOND PASS: PASS`
- Findings: no actionable findings and no P0, P1, P2, or P3 findings.
- Scores: unchanged from Review Pass 1; every dimension for all 14 skills remains at least 9.
- Bridge evidence: the Project route, personal workspace category, sanitized conversation reference, single attachment, composer state, submission, and response completion were included in the second-pass assessment.
- Conclusion at that time: the branch appeared to meet the threshold, but the oversized single-attachment protocol was later found insufficient and this conclusion is superseded by Review Pass 3.

### Remaining Non-Blocking Verification Gaps

- Windows UI Automation and Linux AT-SPI desktop adapters were not executed.
- Actual LLM routing precision remains a runtime behavior that static validators cannot prove.

## Review Pass 3

- Review basis: `23d30ccd1362d177943dbb39c79abebbd1c36f97..810d3a208bc5f1b15e3076501f27af1d7836f35b`
- Repository visibility: `public` (verified through GitHub repository metadata on 2026-07-11)
- Reviewer workflow: final independent `repo-review`
- Verdict: `Actionable findings found`
- Findings: one P1, two P2, and one P3.
- Score impact: `chatgpt-review` scored 8.4 for Boundary/Safety, 7.2 for Workflow Executability, and 8.2 for Eval Quality; the other 13 skills remained at or above 9 in every dimension.

### Locally Confirmed Findings

1. The oversized-package rules required multiple parts while allowing only one attachment per round, but did not define a multi-message state machine.
2. The committed review artifact contained a full conversation URL and a concrete personal workspace display name without a visibility or sanitization policy.
3. The validator checked generic eval-table shape but not the specialized Rust, frontend, or bridge eval contracts.
4. The Skill Standard overstated automated metadata semantic synchronization; the validator checks structure and route references, while semantic synchronization still needs human review.

### Remediation

- Defined a manifest/hash/acknowledgement/final-marker multipart sequence with one attachment per send action and one completed sequence per review round.
- Added `local-private`, `repository-private`, and `repository-sanitized` review artifact modes and sanitized this repository copy.
- Added specialized eval-contract validation and mutation regression tests for Rust overlays, Rust audit scenarios and profile scope, frontend framework scenarios, and bridge multipart/visibility cases.
- Clarified the automated versus human metadata synchronization boundary.
- Sanitized the current `review.md`; the explicitly authorized branch rewrite replaces commit `810d3a2`, and delivery must verify that commit is no longer in the rewritten task branch ancestry.
- Validation status: `python3 scripts/validate-skills.py`, `python3 scripts/test_validate_skills.py`, `python3 scripts/validate-skills.py --quality-report`, and `git diff --check` passed after remediation.

## Review Pass 4

- Timestamp: 2026-07-11T10:02:44+08:00
- Review basis: `23d30ccd1362d177943dbb39c79abebbd1c36f97..d1c5f0d89cd8830de3f02195c9aaff14e8d6d01c`
- Artifact visibility: `repository-sanitized`
- Surface: ChatGPT Project
- Conversation reference: `suffix-8348f12b`
- Account workspace: `personal`
- Browser route: Codex in-app Browser
- Reviewer workflow: final independent `repo-review`
- Input method: multipart manifest followed by eight single-attachment messages and a separate `FINAL PART` marker.
- Completion evidence: all eight acknowledgements matched the manifest SHA-256 values; no analysis began before `FINAL PART`; the final response completed with no active generation state.

### Multipart Integrity

| Part | SHA-256 |
| --- | --- |
| `review-package.part-001.md` | `7eb0f16878830a830aa202d45aa9d2ec04a9a782d579ec45f49348d0214bc938` |
| `review-package.part-002.md` | `ec0a3c95ac8d38d527a0d82d0ee665bbb857be950401310e6f617d2080e7c846` |
| `review-package.part-003.md` | `c7b3ba7abaa4e73e1a1e4001eeb055f485540ca42f22025ec0060e08a0a6385f` |
| `review-package.part-004.md` | `e89a12c6faac6db176cf460ddbb20f6250f8a434b156658714b7a060105504b3` |
| `review-package.part-005.md` | `02532a751a493b1178f0c68c94c66e48369ef9fe8289e616660813b007284866` |
| `review-package.part-006.md` | `e257023a0e96525b565f9e339632892ab91b96896ba35f817fd53f4fd9501bde` |
| `review-package.part-007.md` | `39e3aa349b19328b6a82f74a941fbe00351ffadc9009afbc1ccd2f0abfa41bf7` |
| `review-package.part-008.md` | `8afeb03e7a6f3f4b000e5b32259dcb68d3e1a60c86ef2c15303dd93419b1f9f6` |

### Reviewer Verdict

`FINAL INDEPENDENT REVIEW: PASS`

- P0: none.
- P1: none.
- P2: none.
- P3: none.
- `No actionable findings.`
- All four Review Pass 3 findings were verified as fixed.
- `ALL SKILL DIMENSIONS >= 9.`

### Skill Scores

| Skill | Trigger/Routing | Boundary/Safety | Workflow | Metadata Sync | Eval Quality | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| code-context | 10 | 10 | 10 | 10 | 9 | 9.8 |
| code-planner | 10 | 10 | 10 | 10 | 10 | 10.0 |
| diagnose | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-review | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-delivery | 10 | 10 | 10 | 10 | 10 | 10.0 |
| implement-frontend | 10 | 10 | 10 | 10 | 10 | 10.0 |
| audit-frontend | 10 | 10 | 10 | 10 | 10 | 10.0 |
| implement-rust | 10 | 10 | 10 | 10 | 10 | 10.0 |
| audit-rust | 10 | 10 | 10 | 10 | 10 | 10.0 |
| code-security | 10 | 10 | 10 | 10 | 10 | 10.0 |
| ops-browser | 10 | 10 | 9 | 10 | 10 | 9.8 |
| ops-client | 10 | 10 | 9 | 10 | 10 | 9.8 |
| chatgpt-review | 10 | 10 | 10 | 10 | 10 | 10.0 |
| human-writing | 10 | 10 | 10 | 10 | 10 | 10.0 |

### Residual Non-Defect Gaps

- Windows UI Automation and Linux AT-SPI runtime adapters remain `Not verified` in this repository-only review.
- Actual model routing accuracy remains `Not verified`; static validation proves metadata references and eval contracts, not every runtime selection.
- Long-running external browser reliability remains environment-dependent.

### Attribution Note

The browser connection briefly interrupted after the eighth submit action. The same Project conversation URL was revalidated, and the existing conversation already contained the matching eighth-part acknowledgement; no replacement conversation, duplicate upload, retry, or extra review round was created.

## Review Pass 5

- Timestamp: 2026-07-13T17:08:32+08:00
- Review basis: Worktree at `84ea1ba533f6b129e00ee905a84e74d8ba70dc0b`
- Scope: `skills/repo-map/` and its synchronized routing/standard surfaces
- Artifact visibility: `repository-sanitized`
- Surface: ChatGPT Project (`AI Review`)
- Conversation reference: `suffix-7289f830`
- Account workspace: `personal`
- Browser route: Codex in-app Browser
- Capability snapshot: `cap-repo-map-rereview-iab-1`
- Package: `review-package.md`, SHA-256 `1359827c7e8c1e7ee6ea9afebde1b6d21b1b7a174295e0bd173dd2d7988a3c77`
- Operation IDs: `repo-map-rereview:r1:submit`, `repo-map-rereview:r1:capture-response`
- Completion evidence: stable Project conversation assigned; one user message and one assistant response observed; response length 9,103 characters; stop control absent after completion.

### External Reviewer Verdict

`needs changes`

The reviewer reported four P1 and four P2 concerns:

1. A non-Git workspace container has no defined durable owner for its workspace map.
2. Semantic staleness is not explicitly repaired when a documented path still resolves.
3. A new-declaration search may miss reusable contracts in sibling provider/shared roots.
4. Dirty-worktree preservation is stated but lacks an explicit diff-overlap procedure.
5. `Owner` is required without separately defining code, deploy, runtime, and data ownership.
6. The `3-8` decisive-entry rule has an ambiguous denominator and may encourage padding.
7. `Public entry` can exclude valid internal shared contracts, while two consumers alone can over-index local helpers.
8. The supplied validation summary did not demonstrate cases for the newly identified decision boundaries.

### Codex Verification

- **Confirmed, priority P1:** the new-declaration gate searches the current map and live source but does not require every mapped provider/shared root reachable through API, IPC, schema, generated-code, dependency, or runtime-contract edges. This can permit a cross-root duplicate.
- **Confirmed, priority P2:** workspace scope permits a non-Git container while the default durable artifact path and owner are not resolved explicitly.
- **Confirmed, priority P2:** incremental repair is path-failure-specific; a still-resolving path whose export, registration, owner, command, schema, or runtime role changed lacks an explicit semantic-staleness closure rule.
- **Confirmed, priority P2:** `roughly 3-8` does not say whether the count is per task or per artifact and can conflict with the smallest-map creation gate.
- **Confirmed, priority P2:** `Public entry` is too narrow for valid module-private imports, framework registrations, generated entries, Rust `pub(crate)`, or Java package/module visibility. The existing inclusion gate already prevents some catalog growth, so only the access-entry terminology and meaningful-boundary test need adjustment.
- **Confirmed as eval gap:** current evals do not directly exercise the non-Git owner, resolving-but-semantically-stale entry, sibling-provider search, internal shared visibility, or one-entry/greater-than-eight stop cases.
- **Rejected as a separate defect:** unrelated-change preservation is already a hard rule in the skill and a repository-facing requirement in the Skill Standard. A targeted dirty-map eval would strengthen enforcement, but the claimed missing authority boundary is not present.
- **Rejected as stated:** the skill's canonical owner means the definition/contract owner used for navigation, not mandatory team ownership across code, deployment, operations, and data. Those dimensions may be recorded when they change routing, but requiring all four would make the map heavier than its creation gate allows.

### Additional Local Findings

- **P2:** `references/prompt-templates.md` always requires user approval before writing an `AGENTS.md`, conflicting with the Skill Standard exception when the user explicitly requested implementation.
- **P3:** `references/usage.md` and `docs/standards/skill-routing.md` still describe `repo-review` as immutable-only even though it now owns both Worktree and immutable basis modes.

### Validation

- `python3 scripts/validate-skills.py --skill repo-map`: passed.
- Skill Creator `quick_validate.py` for `repo-map`: passed.
- `git diff --check`: passed before this review artifact append.
- Runtime execution of repo-map against representative monorepo, multi-repo, and non-Git workspace fixtures: `Not verified`.

No fixes were applied in this review pass.

### Post-Review Remediation

Implemented after Review Pass 5:

- resolved containing-Git, non-Git-with-child-repositories, and ordinary non-Git directory roots without rejecting unversioned workspaces;
- required cross-root provider/shared searches before approving a new declaration;
- added semantic-staleness repair for still-resolving paths and dependent routes/edges;
- replaced the ambiguous `3-8` artifact rule with a minimum chain, normally 1-8 unique entries per selected task;
- replaced `Public entry` with actual access/registration visibility and covered internal shared contracts;
- made generated-document preview approval conditional on whether implementation was already explicitly requested;
- aligned `repo-review` references with Worktree and immutable basis modes;
- added root-resolution, cross-root reuse, semantic repair, internal visibility, dirty-target preservation, and evidence-chain evals.

Validation after remediation: targeted and full skill validation passed, Skill Creator `quick_validate.py` passed, all 34 validator regression tests passed, and `git diff --check` passed.

## Review Pass 6 — repo-map Three-Round Closeout

- Timestamp: 2026-07-13T17:30:34+08:00
- Review basis: Worktree at `84ea1ba533f6b129e00ee905a84e74d8ba70dc0b`
- Scope: `skills/repo-map/` and synchronized repo-map routing/documentation surfaces
- Artifact visibility: `repository-sanitized`
- Surface: ChatGPT Project
- Conversation reference: `suffix-7d8efaf6`
- Account workspace: `personal`
- Browser route: Codex in-app Browser (Experimental)
- Capability snapshot: `cap-repo-map-3round-iab-1`
- Authorized/completed rounds: 3 / 3 in one Project conversation

### Review Artifacts

| Round | Artifact | SHA-256 | External verdict |
| --- | --- | --- | --- |
| 1 | `review-package-repo-map-round-1.md` | `d5ece8ecdba355081af6c90991aa7005ebe0e59d2e670178ad8d9b305fb60148` | `needs changes` |
| 2 | `review-package-repo-map-round-2.md` | `795b978c92d31448edffc8ee689c2d1d489f8f30e4aeb8494c2b3b6f063030ab` | `needs changes` |
| 3 | `review-package-repo-map-round-3.md` | `a7be883268c1bd78997ea98e74d1f8e1ebe5abbdee9869799ee52faa5d16d04f` | `No findings`; `pass` |

Each submit operation was executed once with retry policy `never`; one pasted-text attachment was observed before each submission and the same stable Project conversation was retained through all rounds.

### Round 1 — Confirmed and Remediated

1. Separated the requested path as initial working scope from the containing Git/map root.
2. Added deterministic nested-Git containment and deepest-root default file ownership.
3. Bounded provider/shared discovery to first-order contract roots and explicitly owned transitive edges, with external/exhausted stop conditions.
4. Added mandatory stopped/partial execution reporting: reason, completed evidence chain, unresolved boundary, artifact state, and follow-up.

### Round 2 — Verified Disposition

- The reviewer quoted obsolete Round 1 wording that was absent from the Round 2 package and current source. That evidence claim was rejected. Its valid underlying storage question was addressed by requiring one authoritative root index and linked scoped sibling pages without changing storage root.
- Added a stopping boundary for semantic consistency closure: changed entry plus directly dependent declared edges until no changed dependency remains.
- Added deterministic ranking for conflicting reusable candidates and `Not verified` on unresolved authority.
- Added explicit first-creation, legacy migration, competing-map, scoped-page, and non-Git persistence behavior/evals.

### Round 3 — Final Verdict

The external reviewer returned no P0, P1, P2, or P3 findings and verdict `pass`.

### Local Verification Boundary

- External suggestions were not accepted solely on reviewer authority; each was checked against the supplied package and current local source.
- Representative runtime execution against real monorepo, nested-Git/submodule, multi-repo, and ordinary non-Git fixtures remains `Not verified`; the current evidence is static contract, validator, and eval coverage.
- No files were staged, committed, pushed, or otherwise delivered in this review pass.
