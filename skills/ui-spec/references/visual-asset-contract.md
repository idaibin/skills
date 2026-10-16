# Parameterized Visual Asset Contract

Load this reference only when an accepted UI slice uses a parameterized gradient,
texture, generated raster/vector, or animated background whose source or recipe
materially affects acceptance. An ordinary token background does not need this contract.
It specifies the asset's use and acceptance; it does not generate, edit, license, or
redistribute an asset. Route exploration or generation to the authorized Product Design
or image owner, then return with a selected source.

## Contents

1. Source and rights gate
2. Recipe and readable-content contract
3. Motion and preview contract
4. Export and component handoff
5. Target-surface acceptance

## Source And Rights Gate

Before specifying the asset, record its stable source ID/revision, selection status,
creator or provider, rights status, permitted product use, attribution or redistribution
requirements, and explicit `use`/`ignore` scope. A palette, prompt, screenshot, or
similarity claim does not establish rights. If the source is unselected or its required
use is unlicensed, stop this asset slice `Not Ready`; a CSS-only approximation is not a
way to bypass the source boundary.

Keep source identity separate from every derivative/export identity. Record whether the
accepted normal presentation is authored CSS, SVG, JSON/Lottie or another declared
runtime format, and which formats are merely preview or fallback exports. Do not copy
third-party branding, copy, or implementation merely because it is visible in a source.

## Recipe And Readable-Content Contract

Write one compact, named recipe for each accepted asset state. Each field is either
source-backed with its evidence ID, `proposed` with the approving owner, or `Not
verified`; do not turn a screenshot estimate into an exact implementation value.

| Field | Contract question |
| --- | --- |
| `palette` | Which semantic colors, stops, opacity, and compositing order are permitted? |
| `geometry` | What gradient family, paths, masks, texture primitive, or layer order establishes the composition? |
| `focus` | Which normalized focal point, exclusion area, or subject region must remain stable across crop/reflow? |
| `scale` | What reference canvas, repeat/cover behavior, density, and responsive scale rule apply? |
| `noise` | What source/type, opacity, blend mode, and quality ceiling make texture perceptible without obscuring content? |
| `soften` | What blur, feathering, vignette, or edge treatment is permitted, and which content/edges must stay sharp? |

Pair the recipe with a text-safe-area contract: named region(s), minimum usable width
and height or responsive rule, protected focal/content exclusions, foreground role,
and final composited contrast requirement for every applicable theme/state. Test
contrast against the actual layers beneath each foreground role, not a nominal palette
swatch. If a responsive crop can move the focus into copy or lower contrast, specify
the breakpoint adaptation or reject that crop.

The Feature Spec names the component role and maps its required states, but live source
and types remain the authority for its real props, slots, events, DOM, and accessibility.
Do not create a shared token/component just because one page needs a decorative asset.

## Motion And Preview Contract

Motion is conditional. State its communication purpose and the exact animated parameter
(for example focus drift, opacity, or texture offset); use static output when no purpose
is accepted. Specify duration/easing/range only from accepted evidence, make rapid
navigation or dismissal interruptible, and define the `prefers-reduced-motion` result:
static recipe, paused final frame, or another accepted non-motion presentation. Reduced
motion must preserve readability, focus behavior, and task completion.

Define a small preview matrix only for material crops or states. It pairs a canonical
asset identity with the same viewport/state evidence model used by the slice; it does
not silently create generic device coverage.

| Preview ID | Viewport/theme/state | Crop/focus and safe-area assertion | Motion mode | Expected export or runtime identity |
| --- | --- | --- | --- | --- |
| `required` | exact slice condition | observable focus, readable region, composited contrast | normal or reduced | source/export/runtime ID and evidence status |
| `optional` | additional accepted condition | useful non-blocking assertion | normal or reduced | same identity rules |
| `excluded` | explicitly out-of-scope condition | why it is not accepted here | not applicable | excluding authority |

## Export And Component Handoff

For every export, record format (`SVG`, `CSS`, `JSON`, `PNG`, or another accepted
format), stable asset ID/revision or content hash, intrinsic/reference dimensions,
color-space/transparency assumptions, intended role (`runtime`, `preview`, or
`fallback`), and source/rights linkage. An export filename or MIME type alone is not
identity proof. Prefer the format that the existing stack can render and validate
without a new dependency; do not ship several equivalent formats without a distinct
runtime or fallback reason.

Handoff to `dev-frontend` includes the exact component owner/reuse decision and the
smallest public contract needed by the accepted recipe, normally named semantic props
such as `variant`, `density`, `motion`, and an asset identity/reference. It also states:

- which values are fixed by the UI contract versus caller-selectable;
- fallback trigger, appearance, and accessibility behavior for an individual failed or
  unsupported asset, without substituting it for the normal product asset;
- rendering budget and measurement method appropriate to the chosen format (for
  example, no unbounded filters/canvas redraws, bounded animation work, and no new
  library unless the existing owner requires it);
- static owner check plus target-surface runtime check for recipe, contrast, motion,
  fallback, and performance behavior.

`dev-frontend` reuses the declared component/style/animation owners, preserves the
contracted safe area, and reports measured performance rather than promising it from
format choice. `ops-browser` or `ops-client` supplies authorized runtime evidence.

## Target-Surface Acceptance

Add acceptance IDs for source/rights, recipe, export identity, safe area, final
composited contrast, reduced motion, fallback, and each required preview-matrix row.
Map each to an owner and evidence method in the normal selected-source delta table.

Static source, an exported PNG, CSS/SVG inspection, or a successful build can verify
only their own declarations or bytes. The UI contract may be `Ready for dev-frontend`
when its source, rights, recipe, owners, acceptance IDs and evidence methods are settled;
record pending runtime checks as `Not verified` without blocking that handoff. Close
the separate target-surface acceptance only after the approved runtime is observed at
every required viewport/state: correct asset identity and crop, readable safe area and
final contrast, normal and reduced-motion behavior where applicable, isolated fallback,
and the agreed performance measurement. If that surface or measurement is unavailable,
keep only the affected runtime acceptance IDs `Not verified`.
