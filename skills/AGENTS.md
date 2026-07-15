# Skills

`skills/` stores runnable or reusable skill packages.

Before adding or updating a skill, read `../docs/skills/skill-standard.md` and `../docs/standards/skill-routing.md`.

## Naming And Routing

- Implementation skills use `implement-<domain>` and own requested source changes.
- Domain audit skills use `audit-<domain>`, stay read-only by default, select only applicable profiles, and route requested fixes to the corresponding implementation skill.
- `repo-map` owns separate repository mapping, reuse inventory, and docs/code alignment; it does not rank defects.
- `diagnose` owns reproduction and root-cause confirmation; permanent remediation transitions to the matching implementation skill.
- `repo-review` owns read-only review of current local Git changes and immutable snapshots, ranges, pull requests, release candidates, and review packages through basis-specific modes.
- `audit-security` owns bounded read-only security assessment and may act as a specialist under `repo-review`.
- `chatgpt-review` owns local review packages and explicitly authorized external ChatGPT review rounds; `ops-browser` owns only delegated low-level browser operations.
- `repo-delivery` owns staging, commits, pushes, squash, cleanup, and other Git mutations after review.
- Do not reintroduce retired aliases such as `repo-context`, `code-context`, `code-review`, `code-delivery`, `chatgpt-review-bridge`, `code-security`, `frontend-implementation`, `frontend-governance`, or `rust-engineering-governance` inside skill packages.

Before creating a new public skill, search existing skills and references for direct reuse or an internal profile extension point. Create a new skill only when user intent, authority, workflow, output contract, and nearest non-trigger boundary are materially distinct. Framework names or checklist categories alone are not sufficient.

Each skill keeps its own internal structure, for example:

- `SKILL.md`
- `agents/`
- `references/`

Keep `SKILL.md`, `agents/openai.yaml`, `references/usage.md`, `references/eval-cases.md`, and all linked references synchronized when triggers, modes/profiles, routing, mutation boundaries, or output contracts change.

For add, reuse, move, rename, or delete operations, update the source package, README skill table, `INSTALL.md` package list, `skills.sh.json`, local links, tests, and stale-name checks in the same task.

Shared cross-skill protocols are authored under `protocols/` and synchronized
into self-contained published packages with
`python3 scripts/sync-shared-protocols.py`. Do not hand-edit a generated copy.
Skill-specific validation thresholds and cross-artifact term contracts belong in
`contracts/skill-validation.json`, not as new prose literals in the validator.

Before review or delivery, run from the repository root:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
git diff --check
```

Preserve unrelated local changes and stage only the files owned by the task.
