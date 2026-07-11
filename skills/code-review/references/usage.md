# Code Review

## Summary

Review existing local git changes before commit. It protects unrelated edits, checks contract chains, handles mixed hunks safely, and turns a dirty tree into scoped commit groups.

## Best For

- Pre-commit review
- Dirty-tree ownership classification
- API or payload contract-chain review
- Structural add/reuse/move/delete completeness review
- Semantic commit grouping
- Exact staging plans and Conventional Commit messages
- Scoped frontend, Rust, or security specialist subreview orchestration for a changed surface

## Triggers

Use for prompts like:

- `Review all changes and split commits.`
- `Check whether these changes are safe to commit.`
- `Review only the current session changes and prepare exact staging instructions.`
- `Review the API contract chain.`
- `Review this crate move and confirm manifests, exports, CI, docs, and stale references are closed.`
- `Generate a commit message, but confirm file scope first.`

Do not use for repo onboarding or future implementation planning before code exists; prefer `code-context` or `code-planner` for those. Use `code-delivery` for staging, local commits, pushes, sync, squash, cleanup, or remote proof after review.
Use `audit-frontend` or `audit-rust` for domain-wide technical audits without an
existing Git change set; return to `code-review` after fixes exist and need
dirty-tree classification, completeness checks, staging plans, or commit readiness.

## Output

Expect findings first, ownership labels, mixed-hunk risks, contract and structural completeness, specialist evidence when required, exact commit groups, path-limited or hunk-level staging guidance, validation status, risks, and concise Conventional Commit messages. It never changes worktree files or Git state.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
