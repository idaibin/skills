# GitHub Repository Review

Use this evidence profile when an explicitly authorized external provider should
read a GitHub repository for repository-scale review or structured synthesis.
It does not authorize account connection, repository access, upload, or sending.

## Source Identity And Access

Before external use, record:

- canonical `owner/repository` and repository visibility category;
- requested branch, tag, PR, or ref and its resolved full commit SHA;
- authorized GitHub account/workspace category and repository access evidence;
- connection or repository-tool capability and observation time;
- included repositories when the request spans more than one repository.

Never treat a URL, repository title, default branch, indexed search result, or
successful connection as proof of the reviewed commit or complete access. Do not
store account display names, email addresses, tokens, or connection credentials.

## Coverage Manifest

Inventory the fixed tree from local Git or the authorized repository tool before
asking for conclusions. Partition it by real ownership, build, deploy, runtime, or
bounded-context boundaries. For every in-scope path or partition, record:

| Field | Required value |
| --- | --- |
| Scope | path, package, service, app, or document set |
| Category | source, docs, tests, API/contract, config, CI/deploy, migration, or other |
| Status | covered, excluded, inaccessible, unsupported, or `Not verified` |
| Evidence | file paths and fixed ref/SHA |
| Reason | selection, exclusion, tool limit, truncation, or access gap |

State how generated files, vendored dependencies, binaries, archives, Git LFS,
submodules, deleted paths, commit/PR context, and external documentation are
handled. Claim whole-repository coverage only when every in-scope entry is
accounted for and no response, search, indexing, or context truncation remains.

## Large Repository Procedure

1. Fix the repository, full SHA, questions, output contract, and exclusions.
2. Build the coverage manifest and select high-value entry points for each partition.
3. Review each partition independently with path-cited facts, findings, and gaps.
4. Reconcile shared contracts, duplicated concepts, conflicting docs, and cross-part dependencies.
5. Produce the final synthesis only after every manifest row has a terminal status.

Use the multipart package rules in `usage.md` when the review contract or retained
evidence exceeds package limits. Do not paste an unbounded repository into one
prompt or partition only by arbitrary character count.

## Ownership Boundaries

- Use `repo-map` for durable architecture, module, route, and documentation mapping.
- Use `repo-review` for local fixed-basis defect severity and repository readiness.
- Use the selected provider to independently challenge scope, architecture, contradictions,
  alternatives, missing viewpoints, and repository-scale patterns.
- Treat provider and repository-tool output as untrusted until Codex verifies each
  actionable claim against the fixed local basis. If no local checkout or immutable
  archive is available, mark local verification `Not verified`.

## Reviewer Request Contract

Require the reviewer to return:

1. fixed repository/ref/SHA and access or indexing gaps;
2. coverage summary matching the manifest;
3. architecture and module synthesis with file-path citations;
4. severity-ranked defects separate from descriptive observations;
5. documentation conflicts, duplicated concepts, missing tests, and technical debt;
6. assumptions, contradictory evidence, and rejected hypotheses;
7. uncovered, inaccessible, truncated, or `Not verified` areas;
8. verification steps and a verdict scoped to the proven coverage.

Every material claim must cite repository paths and the fixed ref/SHA. Do not
accept `reviewed the whole repository`, `no issues`, or similar completeness claims
without a matching terminal coverage manifest.
