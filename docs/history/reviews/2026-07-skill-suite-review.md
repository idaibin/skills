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

## Review Pass 7 — human-writing Six-Round Study and Closeout

- Timestamp: 2026-07-13T21:29:47+08:00
- Review basis: isolated worktree at `fac9f4efbb27e07094812114a042bc4937e2222c`
- Scope: `skills/human-writing/` and synchronized metadata/eval surfaces
- Artifact visibility: `repository-sanitized`
- Surface: standard ChatGPT conversation
- Conversation reference: `suffix-c8f9b5a2`
- Account workspace: `personal`
- Browser route: Codex in-app Browser (Experimental)
- Final cumulative package SHA-256: `b4bf129808ec0a1c445be0b05793323d45630674a190b8473b556c07e121eba1`
- Authorized/completed rounds: 6 / 6 in one stable conversation

### First Three Review Rounds

| Round | Operation IDs | External verdict | Local disposition |
| --- | --- | --- | --- |
| 1 | `hw-initial-1:submit`, `hw-initial-1:capture` | `needs changes` | Confirmed source-visibility, acceptance-authority, claim-state, actor-role, partial-output, and diagnostic false-positive gaps; repaired them and expanded fixtures |
| 2 | `hw-initial-2:submit`, `hw-initial-2:capture` | `needs changes` | Separated editing directives from claim authority; removed assistant wording as evidence; propagated restrictions through derived claims; consolidated normative ownership in `fact-integrity.md` |
| 3 | `hw-initial-3:submit`, `hw-initial-3:capture` | `No actionable findings`; `pass` | No further change |

### External Writing-Skill Study

Repository star counts were checked on 2026-07-13 as popularity signals only. Each concrete writing asset was read before deciding what to adopt.

| Repository and writing asset | Stars | Applied learning | Deliberately not copied |
| --- | ---: | --- | --- |
| [anthropics/skills — internal-comms](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md) | 161k | type-based routing and selective genre references | company-specific formats as universal structure |
| [coreyhaines31/marketingskills — copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) | 38k | reuse established context; define reader, purpose, action, evidence, voice, and output | conversion scope, formulaic variants, mandatory annotations |
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) | 29k | supplied-sample voice calibration and draft-audit-final iteration | universal dash removal and default personality injection |
| [K-Dense-AI/scientific-agent-skills — scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scientific-writing/SKILL.md) | 26.2k | private claim-and-evidence outline before complex prose | IMRAD, mandatory research tooling, universal no-bullets output |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/blob/main/SKILL.md) | 13.7k | concise checks for filler, vague agency, specificity, rhythm, and reader trust | absolute bans on adverbs, passive voice, dashes, and three-item lists |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh/blob/main/SKILL.md) | 13k | Chinese checks for vague conclusions, excessive qualification, concrete detail, and cadence | deliberate messiness, automatic first-person promotion, and default change summaries |

Study-driven changes reuse supplied context before asking, apply private outlines only to new long-form or multi-claim work, keep planning scaffolds out of final prose, prevent outline gaps from becoming invented evidence, and treat common AI-writing forms as contextual cluster signals rather than lexical violations.

### Final Three Discussion Rounds

| Round | Operation IDs | Focus | External verdict |
| --- | --- | --- | --- |
| 4 | `hw-research-1:submit`, `hw-research-1:capture` | coherence, scope control, private-outline/output boundary, contextual diagnostics | `No actionable findings`; `pass` |
| 5 | `hw-research-2:submit`, `hw-research-2:capture` | adversarial failures in context reuse, outline leakage, diagnostic underreach, voice copying, and contract duplication | `No actionable findings`; `pass` |
| 6 | `hw-research-3:submit`, `hw-research-3:capture` | final correctness and execution-weight closeout | `No actionable findings`; `pass` |

Each round was submitted once and counted only after the completed assistant response was captured with the stop control absent. No full conversation URL, account display name, or unrelated repository content is stored here.

### Local Verification Boundary

- External suggestions were checked against current source before application; star count and reviewer agreement were not treated as correctness proof.
- Deterministic fixtures prove only finite contract behavior. Production-model repetition and blind editorial acceptance remain separate evidence layers.
- No files were staged, committed, pushed, installed globally, or published in this review pass.

## Review Pass 8 — human-writing Real-Article Evaluation

- Timestamp: 2026-07-13
- Scope: 10 frozen public articles from `idaibin/blog`; blog repository remained read-only
- Artifact visibility: `repository-sanitized`
- Surface: standard ChatGPT conversation
- Conversation reference: `suffix-48f9d4`
- Account workspace: `personal`
- Browser route: Codex in-app Browser (Experimental)
- Authorized/completed rounds: 10 / 10 in one stable conversation

| Round | Source artifact | Package SHA-256 | External decision | Local finding |
| --- | --- | --- | --- | --- |
| 1 | `feeds-hub-editorial-system-lessons.zh.mdx` | `d8225d9cab8b0093bf70023ec49622a489b136bc29bf9e71013b308a67d3c563` | bounded edit; `needs changes` | Confirmed claim-state issue; added whole-artifact metadata checks after the diagnosis missed the stronger `description` claim and its own edit introduced absolutes |
| 2 | `why-rust-admin.zh.mdx` | `fd1d9975ac216bc26490e3767d3bd142446021ca64d443f493b13c5da70ac527` | original; `needs changes` | Candidate weakened precise engineering terms; strengthened unchanged-source comparison and stop behavior |
| 3 | `rustzen-series-product-notes.zh.mdx` | `1bd3e36610cae6cbbdbff29614df258c5540028bdc401d2d873d35279fb3c09f` | original; `needs changes` | Candidate invented a lived direction change from a prospective risk and misdiagnosed a useful table |
| 4 | `aicraft-skills-as-ai-assets.zh.mdx` | `95d6a4206f3a5a4647b9075b98ddaebfa6464008f0cb83c38ac7fec5ef094fca` | technical verification first; `needs changes` | Expanded verification from one command to the complete executable workflow and lowered unsupported error assumptions |
| 5 | `feeds-hub-information-automation.zh.mdx` | `c2962bc710f171961d36d4bbdbb2777823fc3b46af88cc5f887fdffe1e6bea8d` | original; `needs changes` | Candidate collapsed `verify` and `validate` roles and omitted the submit/rollback closure |
| 6 | `git-multi-repo-identity.zh.mdx` | `a6531ccfb40fdba713ceb50ba912776158cf76b2eda57d54a174b411abd1db56` | technical verification first; `needs changes` | Added combination-state and precedence checks after a multi-remote silent identity conflict was identified |
| 7 | `where-macos-developer-disk-space-goes.zh.mdx` | `86bc806cb57040f67f46e5330505653a5548108226569dc4195cf44abba9b2eb` | original; `needs changes` | Candidate dropped `应尽量` and upgraded a product principle into an implemented privacy guarantee |
| 8 | `rustzen-architecture-guide.zh.mdx` | `262493df32d8cea90cb9f2028bc5f24b1fa5cba57b10bf8bba3fa7e11e4d7293` | technical verification first; `needs changes` | Added source-internal consistency checks for architecture/code, authentication semantics, and performance wording before live-repository verification |
| 9 | `rust-learning.zh.mdx` | `7027bcdb5990c14acbdd91cb1962657f4e099a8f90caa57b6582d80088e77404` | technical verification first; `needs changes` | Separated visible duplicate/title/completeness defects from volatile link and maintainer checks; refined resource provenance |
| 10 | `zen-clear-tweet.zh.mdx` | `453300b422417439bd9ea208e28a30801c2a21a9b8822fa7310b90b6f2a609c1` | original; `pass` | Confirmed that a short, bounded, disclosed product note should remain unchanged |

### Resulting Contract Changes

1. Audit frontmatter, title, description, body, code, tables, links, and disclosures as one artifact.
2. Treat modal words as claim evidence; do not turn principles, risks, capabilities, or candidate directions into guarantees, incidents, or current implementation.
3. Check source-internal contradictions and duplicates before using `Not verified` for genuinely external or volatile facts.
4. Verify runnable instructions as a complete workflow, including combination states, precedence, failure behavior, and expected results.
5. Preserve distinct workflow responsibilities and closing trace/rollback steps even when parallel prose looks repetitive.
6. Compare every candidate against the unchanged source; `original` is a valid finished result when the edit has no concrete benefit.

Ten new deterministic fixtures cover metadata/body mismatch, modality preservation, workflow responsibility, internal consistency, and unchanged-source stopping. ChatGPT findings were treated as independent review evidence and checked against each frozen source; they were not accepted solely on reviewer authority.

### Evidence Boundary

- This pass is a genre-diverse, single-run behavioral sample, not the three repetitions per P0/P1-sensitive case required for `HUMAN WRITING ACCEPTED`.
- Link reachability, live repository correctness, and every technical claim in the ten source articles were outside this writing-behavior test unless the contradiction was visible inside the frozen artifact.
- No blog article was changed, and no files were staged, committed, pushed, installed globally, or published.

## Review Pass 9 — human-writing Overreacted Corpus Study and Forward Writing Test

- Timestamp: 2026-07-14T00:26:59+08:00
- Skill scope: `skills/human-writing/` and synchronized metadata, examples, rubric, and eval surfaces
- Forward-writing artifact: `idaibin/blog/src/content/blog/what-i-do-after-ai-implementation.zh.mdx`
- Artifact visibility: `repository-sanitized`
- Surface: standard ChatGPT conversation
- Conversation reference: `suffix-c8f9b5a2`
- Account workspace: `personal`
- Browser route: Codex in-app Browser (Experimental)
- Corpus: 58 public articles from `gaearon/overreacted.io`
- Frozen source commit: `ac1ad4fe9168b350d3dc59ac0cbe0d53405702bf`
- Corpus index SHA-256: `b63cdaad42bbc5bc65867e7e34de3c31f4f9fecb8761092c431e19dddfbe9dfc`
- Final reasoning reference SHA-256: `9e2a2f6c7659fdad081c1f38db821f233fb4e7173e15250a12c34bdc1d637909`
- Final article SHA-256: `5929efe1ead356b8107c68959c6c6e4620c2d0a3fc8cffdd3d13ebb7dbd306a4`

### Complete Corpus Study

The official source repository was frozen before analysis. Its 58 article sources were divided chronologically into six batches of `10 / 10 / 10 / 10 / 10 / 8`. Codex inspected every source locally; ChatGPT independently inspected every public article or its matching frozen official source and returned one evidence-anchored card per article.

| Batch | Articles | External response SHA-256 | Verdict |
| ---: | ---: | --- | --- |
| 1 | 10 / 10 | `4193b119542c72500784965d06f9afac3691b2ab5dae0e66a4ef2bf6fac43294` | `learning complete` |
| 2 | 10 / 10 | `d287ec2d38fc2a4d4b1db10082b82cb2ff4f804799d0ce43730fc43d73ba7e7b` | `learning complete` |
| 3 | 10 / 10 | `9046d70ad2fa44015bf59f4e23637b2018e71c6a02387bd8e6520265f3b498ad` | `learning complete` |
| 4 | 10 / 10 | `e8d23525b7929f2b17fbb5c13aed25e3de590b801be69bbd8f48877a13ad7439` | `learning complete` |
| 5 | 10 / 10 | `e5d6faa8108744cdf0266c60fb1b0d37e25c56018f9557d0baded031e3379c0c` | `learning complete` |
| 6 | 8 / 8 | `f1d66ca7ed23713c50f144b9ecb73b9dedf10f53a0c32406dacfcb13a7f8dc4f` | `learning complete` |

Cross-corpus synthesis retained only recurring, executable capabilities: reader-model repair, dependency- and constraint-led progression, premise/derivation/judgment separation, controlled examples, boundary and lifecycle explanation, criterion-led alternatives, bounded analogies, evidence-earned naming, conceptual compression, and earned endings. It explicitly rejects copying the reference author's phrasing, jokes, rhetorical cadence, autobiographical authority, personal history, heading pattern, or long-form manner.

### Skill Synthesis Review

The first external review found no P0/P1 but reported five P2 overreach risks: unconditional architecture routing, silent question replacement, retrospective over-scoping of reproducible witnesses, collectively mandatory boundary dimensions, and missing context-economy fixtures. Each was confirmed and repaired locally. Eight new deterministic fixtures cover routing economy, question reframing, selective boundary dimensions, and non-debugging retrospectives.

The second review returned `No actionable P0-P2 findings` and `pass`. Local checks then reported `85 / 85` finite behavior fixtures, valid package/quality coverage, 34 validator tests passing, successful Skill Creator quick validation, and clean `git diff --check`. These results do not claim complete real-model generalization or editorial acceptance beyond the recorded forward test.

### Active Writing and Adversarial Comparison

The revised Skill drafted a new Chinese technical essay from verified author experience: implementation and preliminary verification are increasingly delegated to AI, while task selection, constraint definition, communication, correction, evidence interpretation, and final acceptance become more important. The article uses the verified `rustzen-admin` PostgreSQL-to-SQLite-first history as its central engineering example and does not invent metrics, incidents, users, or universal productivity claims.

The candidate was compared structurally, not stylistically, with three task-relevant references: `My Wishlist for Hot Reloading`, `What Are the React Team Principles?`, and `My Decade in Review`.

| Round | Purpose | External verdict | Local disposition |
| ---: | --- | --- | --- |
| 1 | Independent source and structure review | `below` | Confirmed opening, anchoring, overclaim, and compression issues; verified the repository history before editing disputed facts |
| 2 | Remediation comparison | `comparable — pass` | Accepted provisionally |
| 3 | Adversarial attempt to falsify `comparable` | `below` with two P2 findings | Corrected an unverified completed frontend sequence and a circular implementation-entry condition |
| 4 | Full final closure | `No actionable P0-P2; comparable confirmed; pass` | Accepted |

`Comparable` here means the candidate reaches the same structural reasoning tier for its narrower purpose. It does not mean stylistic similarity, equivalent length, equivalent subject importance, or imitation of the reference author.

### Delivery Boundary

- The blog build and Astro check pass with zero errors; existing Zod deprecation messages remain hints.
- The pre-existing `blog/src/site.ts` modification and all existing `rustzen-admin` worktree changes were preserved untouched.
- No files were staged, committed, pushed, installed globally, submitted to Juejin, or published.
