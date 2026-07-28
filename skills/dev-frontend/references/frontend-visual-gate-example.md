# Generic Frontend Visual Gate Example

This fully synthetic example demonstrates the evidence shape and verdict discipline
for a failed selected-source-to-runtime workflow. Names, paths, copy, identifiers,
dates, and measurements are fictional and do not identify a person, organization,
repository, product, or external design.

## Failure Cause

The first implementation reused an existing component and placeholder data, treated
visual similarity as sufficient, and marked the slice `Ready` before source targets,
asset roles, and runtime acceptance values were traceable. It also omitted an
immediate same-viewport comparison and computed-style review after implementation.

The corrective rule is general: exact source targets come from inspectable source
metadata. Screenshot observations remain `visually-inferred`, and browser-computed
values describe only the captured runtime. A runtime value must never be promoted to
a source target merely because it looks plausible.

## Synthetic Delta Table

| Acceptance | Selected-source target | Current runtime | Target contract | Priority | Evidence |
| --- | --- | --- | --- | --- | --- |
| `AS-GRID-001` | synthetic inspected grid: `360 + 24 + 360 + 24 + 360 + 48 + 300` | synthetic runtime uses different column widths | reproduce inspected grid at the target viewport | P1 | source-extracted plus browser-computed |
| `AS-PRIMARY-CARD-002` | synthetic inspected `360x112`, radius `8` | synthetic runtime `352x112`, radius `10` | match inspected geometry; icon size remains `Not verified` | P1 | source-extracted plus browser-computed |
| `AS-SECONDARY-CARD-003` | distinct image, name, and metadata | placeholder icon and generic action label | preserve source semantics and inspected geometry | P1 | source-extracted and visually-inferred |
| `AS-ASSETS-004` | distinct per-item images | one placeholder for every item | approved item asset; fallback only for one failed item | P1 | visual observation plus runtime asset inspection |
| `AS-TYPE-005` | readable application typography | unintended fallback font and insufficient contrast | inherit the application font and meet the accepted contrast threshold | P1 | visually-inferred, browser-computed, proposed |
| `AS-ALIGN-006` | paired sections align | synthetic vertical mismatch | accepted heading-offset tolerance | P1 | visual observation plus runtime rectangles |

The values are intentionally synthetic. Their purpose is to show that the source
target and current runtime occupy separate columns with separate evidence IDs.

## Implementation Mapping

| Acceptance | Generic owner | Decision | Verification |
| --- | --- | --- | --- |
| `AS-GRID-001` | `src/pages/CatalogPage.vue` grid | extend | bounding rectangles plus overlay |
| `AS-PRIMARY-CARD-002` | `src/pages/catalog-page.css` card style | extend | size, radius, font, asset fallback, hover, and focus |
| `AS-SECONDARY-CARD-003` | page-owned secondary card | extend | rendered semantics, geometry, and keyboard action |
| `AS-ASSETS-004` | item asset adapter | wrap | normal asset plus one intentionally failed item |
| `AS-TYPE-005` | page-local typography | extend | computed font chain and composited contrast |
| `AS-ALIGN-006` | paired content sections | extend | populated and empty heading offsets |

The mapping preserves an established page owner and avoids changing shared design
tokens for local geometry.

## Two-Pass Review

Pass 1 captures the selected source and runtime at the same viewport and state,
creates a side-by-side artifact, reads computed geometry, font, contrast, assets, and
alignment, and records P1 findings. Implementation changes only confirmed rows.

Pass 2 repeats the same capture and computed checks after fixes. It is not a source
code reread. The `fixture://` artifacts are synthetic protocol-test records and do not
prove any real interface was implemented or accepted.

## Final Verdict

The example verdict remains `Partial` because responsive behavior, long-text
truncation, complete keyboard order, and loading, empty, and error states remain
`Not verified`. Build or lint success cannot change that verdict.

## Machine-Checkable Fixture

Validate [the sanitized JSON fixture](../assets/frontend-visual-evidence.example.json)
against [the package schema](../assets/frontend-visual-evidence.schema.json) without
network or third-party modules:

```bash
python3 scripts/validate-frontend-visual-evidence.py \
  assets/frontend-visual-evidence.example.json
```

The artifact exercises `spec-ready`, `mapped`, `pass-1`, and `final` structure,
cross-evidence references, implementation mapping, pass-scoped runtime evidence,
coverage, and final reporting. It does not authenticate screenshots or claims.
