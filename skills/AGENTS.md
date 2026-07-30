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
- Do not invent parallel per-provider files. Add another provider surface only when
  that provider documents a real machine-readable contract that this catalog ships.
- Do not put installation, update, changelog, or repository-maintenance guidance in
  published packages.
- Preserve unrelated changes and keep Git mutation in `repo-delivery`.

Shared package protocols are authored under `protocols/` and synchronized with
`python3 scripts/sync-shared-protocols.py`; do not hand-edit generated copies.

When adding, renaming, or removing a package, update `README.md`, `INSTALL.md`,
`skills.sh.json`, and `skills-index.json` in the same change. When routing meaning,
nearest neighbors, or capability keywords change, update the semantic index even when
the package set stays the same.

## Validation

Use `bash scripts/check-skills.sh` as the single local validation entry point. On
macOS it resolves and verifies Homebrew Python, refuses `/usr/bin/python3`, and uses
`uv` with the pinned `requirements-dev.txt` when available. Other platforms use their
configured `PYTHON_BIN` or `python3`.

For a bounded prose correction in one package:

```bash
bash scripts/check-skills.sh
git diff --check -- skills/<name>
```

For metadata, package structure, shared protocols, multiple packages, or delivery:

```bash
bash scripts/check-skills.sh
```

For behavior changes, exercise the affected Skill on roughly three representative
tasks: a normal use, a nearby non-trigger or boundary, and an important edge case.
Keep raw outputs only when they help improve the Skill. A formal benchmark is optional,
not a publishing requirement.
