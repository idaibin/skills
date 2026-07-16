# 2026-07-16 Codex Routing Infrastructure Failures

This record preserves the non-scoring disposition of three preregistered routing
campaigns. It contains identifiers, counts, and hashes only; it does not copy
held-out prompts, Skill package contents, or model responses.

## Disposition

- None of the campaigns is eligible for behavior scoring or a comparative claim.
- All three held-out datasets are consumed and must not be reused for formal
  evaluation or candidate tuning.
- The v2 and v3 runtime roots were not committed; their recorded hashes identify
  the files inspected at capture time but do not make those runs independently
  reproducible from this repository. The v4 root is retained in Git under
  `eval-results/routing/campaigns/`; it is historical failure evidence, not
  quality-manifest evidence.

## v2: local toolchain failure before model service

- Campaign: `3576e60d-7003-40a4-a0f6-1184f1fabac8`
- Campaign SHA-256:
  `9c6e2c6f617377d691a25036cb124174d659396161c011e258fec94b46a2bf6d`
- Evaluation anchor: `4f774168cbd8925ae4e2071a1d59c8c7d82320a1`
- Dataset commit: `1eaba50ad30016f5bfa25484a26ab8d3bcfebab3`
- Campaign commit: `8d8c7ecefcb1497a668fdda09890100db08892d4`
- Attempt directory:
  `9ba36867-0b71-48a8-84f4-cd58cf8f1d0c`
- Attempt ledger SHA-256:
  `14ed2627a95a767698400037224aadcdcd5acb404f1ea4a74a08d6873923de1a`
- Window start: `2026-07-16T06:29:17.148023Z`
- Complete bundles: `0`
- Persisted raw host records: `4`
- Local Volta shim starts: `5`
- OpenAI model-service calls: `0`

The attempt never entered a Codex model event stream. Two local launches timed
out and two exited `126` because the isolated environment could not resolve the
Codex executable through Volta; a fifth shim start was interrupted before raw
case evidence was written. Commit
`621ebc166f63d1a463733092cbb980906946d1a9` fixed the root cause by preserving
`VOLTA_HOME` in the isolated environment.

## v3: one capacity failure invalidated the campaign

- Campaign: `ba32710e-730b-4eb6-a6b0-9686e9741e4b`
- Campaign SHA-256:
  `75476964aaecf25f341f7891d835285e2b749087c6fba92e06f303c78f6670df`
- Evaluation anchor: `621ebc166f63d1a463733092cbb980906946d1a9`
- Previous revision: `9d86056cb2e3a7762232cf268beef3a12b1d99d7`
- Dataset commit: `8518653fdeb16cf1631d46c877c00534606cf646`
- Campaign commit: `ff7a913a8f95e4d53902a6ff091443059fb18497`
- Execution window:
  `2026-07-16T06:52:07.334859Z` through `2026-07-16T07:24:30.790219Z`
- Host/model: `codex-cli 0.144.5` / `gpt-5.6-sol`
- Model host calls: `210`
- Successful calls: `209`
- Exact capacity failures: `1`
- Complete bundles: `5` (`175` results)
- Successful raw results in the failed bundle: `34`
- Trial 3 slots started: `0`

The five complete bundle SHA-256 values, in trial/variant order, are:

1. trial 1 candidate:
   `31acd8d34672334665d800381b5edd00b7fe1073889e5a2bd56384bb7ee1fd29`
2. trial 1 previous:
   `0189a2a60c1b6f42719123e9fe46d1295d69abcdbb5d8f0380614d79939df8c8`
3. trial 1 baseline:
   `3fe3212c1814f48b333e3597bc4967e20c8fc0ef20a656a8bb574e9be96d4631`
4. trial 2 candidate:
   `9a4d14307fbb1659798d8eea0081c830ef5871100e992ca6e215a3ca7a656ed2`
5. trial 2 previous:
   `5aa2f8fee9c76a42ccd502552498751349bd302d26dc8f266c6f6f07c63c637e`

Trial 2 baseline failed on `v3-heldout-012` with exit code `1`, null token
metrics, and the exact host capacity message. Its raw evidence SHA-256 is
`5f5908ba1eb5210a4650dc33544466e24adcc2bc1d52223f53801fa076c02931`;
the complete `run-failure.json` SHA-256 is
`f45965b4b654f99321dac1cf4f029ec859010188ac985b727c49b5ceb7cf6fc7`.
Because the matched trial is incomplete and trial 3 never started, the 209
successful results cannot be selected or recombined into a comparison.

### v3 label erratum (historical only)

`v3-heldout-002` asks for a read-only review of a known dirty worktree and exact
staging guidance. Its correct owner is `repo-review`, not the committed
`repo-map` label. The consumed dataset remains unchanged so its committed hash
and historical record stay intact. This erratum does not authorize rescoring,
reuse, relabeling of captured results, or tuning against the prompt.

## v4: one timeout invalidated the campaign

- Campaign: `eb47a629-8c22-40f5-9c34-70f388f0b736`
- Campaign SHA-256:
  `156adcdecc73cfe34c5d512382e14e0947f1bec128641044d7fee69985294386`
- Evaluation anchor:
  `4a5be052c9b1cdf47557a4e0555c483d7abca95e`
- Previous revision:
  `9d86056cb2e3a7762232cf268beef3a12b1d99d7`
- Dataset commit: `2c4daca114b88655eb7620dae7bdeeef886e6036`
- Dataset SHA-256:
  `d68d2d8cf7777f35791250659af8ab873a506761d45f65df33f63cc0d9570217`
- Campaign commit: `68050020ff65f3abeb69edd6449dcbba60029f40`
- Evidence commit: `207e61c62df5fc044a68aa123707fe4caa56a7c7`
- Execution window:
  `2026-07-16T09:05:44.335506Z` through `2026-07-16T09:38:25.015668Z`
- Host/model: `codex-cli 0.144.5` / `gpt-5.6-sol`
- Attempt ledgers: `6`
- Persisted raw host records: `210`
- Successful exits: `209` with exit code `0`
- Failed exits: `1` with exit code `124`
- Complete bundles: `5`
- Failed bundles: `1`
- Retries: `0`
- Trial 3 slots started: `0`

Trial 2 candidate failed on `v4-heldout-034` after the preregistered 120-second
timeout. A timeout is not the exact capacity condition, so it was not retried.
The failed slot's `run-failure.json` SHA-256 is
`20e8678a877707fc53ccd2bee2cfdde912b3c56afa2593e999019d1129e0b52a`.
The incomplete trial prevented scoring and comparison; no comparison report or
quality-manifest entry was created. The v4 dataset is consumed and must not be
used by a successor campaign.

## Successor rule

Any successor must use a new post-anchor held-out dataset and campaign. A
bounded transient retry is permissible only if its classifier, attempt limit,
backoff, per-attempt evidence, and policy hash were committed before the first
model call. Previous successful results are not carried into the successor.
