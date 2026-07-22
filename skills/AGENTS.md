# Skills

`skills/` contains the published packages. Before changing one, read
[`../docs/skills/skill-standard.md`](../docs/skills/skill-standard.md) and the
effective repository instructions.

## Design Rules

- Keep one public Skill per stable user intent and authority boundary.
- Use profiles for framework or technology variants that share the same owner,
  workflow, mutation boundary, and output.
- Keep `SKILL.md` concise. Link detailed checklists, examples, and variants directly
  from it; keep references one level deep.
- Packages must be self-contained. They may use their own `scripts/`, `references/`,
  and `assets/`, but must not depend on repository-root maintenance files at runtime.
- Keep provider-specific metadata in its provider surface. This catalog includes
  `agents/openai.yaml` for OpenAI without treating it as portable frontmatter.
- Do not put installation, update, changelog, or repository-maintenance guidance in
  published packages.
- Preserve unrelated changes and keep Git mutation in `repo-delivery`.

Shared package protocols are authored under `protocols/` and synchronized with
`python3 scripts/sync-shared-protocols.py`; do not hand-edit generated copies.

When adding, renaming, or removing a package, update `README.md`, `INSTALL.md`, and
`skills.sh.json` in the same change.

## Validation

For a bounded prose correction in one package:

```bash
python3 scripts/validate-skills.py
git diff --check -- skills/<name>
```

For metadata, package structure, shared protocols, multiple packages, or delivery:

```bash
python3 scripts/sync-shared-protocols.py --check
python3 scripts/validate-skills.py
python3 -m unittest discover -s scripts -p 'test_*.py'
git diff --check
```

For behavior changes, exercise the affected Skill on roughly three representative
tasks: a normal use, a nearby non-trigger or boundary, and an important edge case.
Keep raw outputs only when they help improve the Skill. A formal benchmark is optional,
not a publishing requirement.
