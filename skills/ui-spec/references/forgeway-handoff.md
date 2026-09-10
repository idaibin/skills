# Forgeway Machine Handoff for DESIGN.md

Load this reference only when the active delivery consumer declares the compatible
`forgeway-ui-design-completeness/1` contract; do not create a parallel token schema or
copy Forgeway storage/traversal internals. Ordinary DESIGN.md creation, lint, diff, and
adoption work stays in [design-md-contract.md](design-md-contract.md).

- Producer capability: `ui.contract.specify@1.1.0`.
- Consumer policy: `forgeway-ui-design-completeness/1` consuming
  `ui-spec-design-completeness/1` and producing claim
  `gate:ui-design-complete`.
- Hand off the exact Result PackageManifest plus package-relative paths for
  `DESIGN.md`, completeness JSON, selected-source artifact, and approval record.
  Record the SHA-256 and byte length of every artifact; all paths must resolve inside
  that package and close against its manifest.
- Handoff evidence must include design hash, official spec commit, CLI version, format
  lint result, completeness policy version/result, token groups or omitted reasons,
  source/approval binding, and the exact result PackageManifest when integration is
  active. A PackageManifest binds bytes and basis; it does not prove completeness.
- The trusted approval adapter input binds `design_sha256`, `result_package_id`,
  `completeness_result_sha256`, `approval_record_sha256`, `approved_by_id`,
  `proposer_id`, and `implementer_id`. Its receipt must bind the same design,
  package, completeness result, approval record, and three distinct canonical
  principal IDs.
- The consumer may satisfy the claim only from producer status
  `awaiting-trusted-approval-verification`, exact official spec/CLI/lint evidence,
  the exact completeness policy, token-group or official-omission closure, source
  closure, local approval-record closure, and the host-trusted receipt.
- Fail closed for a candidate `ready-for-human-approval`, format-only or `not-ready`
  result, missing adapter, stale/new package, applicant/local record alone, or any
  hash, length, package, or principal mismatch. Preserve the consumer failure code
  rather than translating it into producer `complete`.
- Real host identity/receipt-adapter execution and a real target DESIGN runtime remain
  `Not verified` until separately exercised.
