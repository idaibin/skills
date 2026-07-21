# Skills

`skills/` stores runnable or reusable skill packages.

Before adding or updating a skill, read `../docs/skills/skill-standard.md` and `../docs/standards/skill-routing.md`.
Also read effective repository or host guidance. Claude Code receives this
directory's rules through `CLAUDE.md`; runtime Skill text must not assume that
every host reads `AGENTS.md` directly.

## Naming And Routing

- Implementation skills use `dev-<domain>` and own requested source changes.
- Domain audit skills use `audit-<domain>`, stay read-only by default, select only applicable profiles, and route requested fixes to the corresponding implementation skill.
- `repo-map` owns separate repository mapping, reuse inventory, bounded
  protocol-authority/consumer maps, and docs/code alignment; it does not rank defects
  or claim runtime/compatibility results from topology alone.
- `domain-modeling` owns shared business language, ambiguity, rules, and boundary scenarios; lifecycle and bounded contexts are conditional depth. It does not own technical DDD, repository mapping, APIs, databases, frontend/backend structure, or implementation planning.
- Planning and diagnosis use the host's built-in capabilities plus effective personal and repository instructions; do not recreate them as public catalog Skills unless they later gain non-trivial domain knowledge, tooling, or a distinct authority boundary.
- `repo-review` owns three read-only bases: current Worktree/index, fixed immutable SHA/range, and verified review package. Pull requests resolve to fixed base/head SHAs; Release is a conditional profile over a fixed basis.
- `audit-security` owns bounded read-only security assessment and may act as a specialist under `repo-review`.
- `ask-chatgpt` owns local ChatGPT request packages and explicitly authorized ChatGPT web collaboration only after a Codex-first gate; it selects content theme separately from Standard Chat, Search, Deep Research, Images, or reviewer-browser capability. `ops-browser` owns only delegated low-level browser operations.
- `repo-delivery` owns categorized commits by default, explicit single commits, pushes, evidence-based branch integration, cleanup, and other Git mutations after review.

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
[`../contracts/skill-validation.json`](../contracts/skill-validation.json), not
as new prose literals in the validator.
Repository package-maintenance rules and generic source-validation commands
belong only here. Repository standards and root documentation must link here
instead of copying commands. Do not repeat them in published package files or
`skills.sh.json`; the latter is display metadata only.
Keep execution economical: one primary owner by default, selected references and
profiles only, the smallest decisive evidence set, focused checks before broader
gates, and no task, review, or handoff expansion without a required outcome.

## Validation

Validation is risk-tiered:

- **Targeted:** for one package's bounded prose/reference correction with no routing,
  metadata, eval, contract, shared protocol, validator, or package-set change, run
  `python3 scripts/validate-skills.py`, focused tests when applicable, and
  `git diff --check -- skills/<name>`.
- **Full:** for routing/metadata/eval/contract/protocol/validator changes, package
  add/remove/rename, multiple packages, or any review, commit, or publish, run:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/eval-skill-contracts.py --validate-only
python3 scripts/measure-skill-footprint.py --baseline-ref HEAD
git diff --check
```

Do not run both tiers or repeat unchanged commands in one basis. Re-run only failed
or invalidated checks during iteration, then run the selected tier once on the final
basis.

Preserve unrelated local changes and stage only the files owned by the task.
