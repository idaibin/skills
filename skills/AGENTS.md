# Skills

`skills/` stores runnable or reusable skill packages.

Before adding or updating a skill, read `../docs/skills/skill-standard.md`.

## Naming And Routing

- Implementation skills use `implement-<domain>` and own requested code changes.
- Domain audit skills use `audit-<domain>`, stay read-only by default, and route
  requested fixes to the corresponding implementation skill.
- `code-review` owns existing Git changes, dirty-tree classification, staging
  plans, and commit readiness; `code-delivery` owns staging, commits, pushes,
  and other Git mutations after review. Neither replaces a domain-wide audit.
- Do not reintroduce retired aliases such as `frontend-implementation`,
  `frontend-governance`, or `rust-engineering-governance` inside skill packages.

Before creating a new skill or package surface, search existing skills and
references for direct reuse or the nearest extension point. Create a new skill
only when its trigger and ownership boundary are distinct.

Each skill keeps its own internal structure, for example:

- `SKILL.md`
- `agents/`
- `references/`

Keep `SKILL.md`, `agents/openai.yaml`, `references/usage.md`,
`references/eval-cases.md`, and all linked references synchronized when triggers,
modes, routing, or output contracts change.

For add, reuse, move, rename, or delete operations, update the source package,
README skill table, `INSTALL.md` package list, `skills.sh.json`, local links,
tests, and stale-name checks in the same task.

Before review or delivery, run from the repository root:

```bash
python3 scripts/validate-skills.py
python3 scripts/test_validate_skills.py
git diff --check
```

Preserve unrelated local changes and stage only the files owned by the task.
