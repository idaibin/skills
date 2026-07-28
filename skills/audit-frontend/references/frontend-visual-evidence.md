# Frontend Visual Evidence Protocol

Use this protocol when a selected visual source materially controls frontend
appearance or when a review claims visual completion. It joins specification,
implementation, browser evidence, audit, and fixed-basis review without changing
their owners or mutation boundaries.

## Contents

- [Owner Gates](#owner-gates)
- [Evidence Levels](#evidence-levels)
- [Selected-Source Freeze](#selected-source-freeze)
- [Delta And Implementation Mapping](#delta-and-implementation-mapping)
- [Two-Pass Runtime Gate](#two-pass-runtime-gate)
- [Required Runtime Coverage](#required-runtime-coverage)
- [Degraded Evidence](#degraded-evidence)
- [Handoff Artifact](#handoff-artifact)
- [Completion Rule](#completion-rule)

## Owner Gates

- `ui-spec` fixes the selected source, evidence limits, target viewport/state,
  traceable deltas, local-versus-shared ownership, acceptance, and readiness.
- `dev-frontend` maps every applicable acceptance item to source ownership and a
  verification method before editing, preserves correct structure, implements P1
  structure/assets/typography/alignment before P2 polish, and closes two runtime
  comparison passes.
- `ops-browser` captures source/runtime evidence and computed DOM/CSS facts at the
  requested viewport and state. It does not approve a source, change a spec, edit
  code, or decide the final verdict.
- `audit-frontend` uses this evidence for a bounded current-surface visual audit and
  leads with P0-P3 findings. It remains read-only and does not attribute findings to
  a change basis.
- `repo-review` checks the handoff and reachable implementation on its selected
  Worktree or immutable basis, attributes findings to that basis, and decides
  whether a visual-completion claim is supported.

## Evidence Levels

Use exactly these labels:

| Level | Meaning | Allowed claim |
| --- | --- | --- |
| `source-extracted` | Value comes from inspectable design metadata, annotation, local export, or accepted source file. | Exact only with source identifier and location. |
| `browser-computed` | Value comes from rendered DOM geometry, computed style, accessibility tree, or final color calculation at a recorded viewport/state. | Exact for that captured runtime only. |
| `visually-inferred` | Value is estimated from a visible image or side-by-side observation. | Directional comparison, never an exact verified token. |
| `proposed` | Value is a target adaptation not proven by the selected source or current runtime. | Contract candidate requiring named owner approval before implementation. |
| `Not verified` | Required fact or state was not observed with fit evidence. | Gap only; never completion proof. |

Every exact value must cite one or more evidence IDs. A screenshot alone cannot prove
exact CSS, font fallback, contrast, hidden state, responsive behavior, or component
ownership. A source file or SCSS declaration cannot prove the final rendered value.
For design targets, prefer a design tool's selected-element inspect/style panel or an
equivalent source annotation over visual measurement. Current runtime computed styles
prove only the current runtime and must never be copied into the selected-source or
target-contract column merely because the page looks close.

## Selected-Source Freeze

Before a visual contract or implementation starts, record:

- stable source identity, revision or image/frame ID, approval state and approver;
- rights/use boundary, redistribution status, explicit `use` and `ignore` scopes;
- target viewport dimensions, page/component state, locale, theme, zoom, and any
  scroll position that changes the visible comparison;
- available design evidence and its limitations;
- current runtime URL/surface and matching state when a runtime already exists.

Capture the selected source and current runtime in the same evidence round whenever
both exist. They must use the same target viewport and state for comparison. A crop
or scaled browser screenshot must record its transform and cannot silently become a
same-viewport artifact.

If the source cannot be viewed, approval is absent, a material state/viewport is
uncertain, or rights are insufficient, stop the affected visual slice. Do not
implement from a prose summary alone.

When a design element cannot be selected or inspected, a 200% visual check may help
compare alignment and hierarchy. Record it as `visually-inferred`; keep exact values
`proposed` or `Not verified`. Zooming a screenshot does not promote it to
`source-extracted` evidence.

## Delta And Implementation Mapping

The UI contract must include a delta table with one row per material difference:

| Field | Requirement |
| --- | --- |
| `acceptance_id` | Stable ID shared by spec, implementation, evidence, and review. |
| selected source | Value plus traceable evidence IDs. |
| current runtime | Value plus traceable evidence IDs or `Not verified`. |
| target contract | Exact accepted value or explicitly `proposed` value with approval. |
| priority | P0-P3 from user impact and blocking order. |
| owner | Shared `DESIGN.md` owner or page/component-local owner. |
| validation | Observable comparison, computed check, state, and viewport. |

Keep selected-source target and current-runtime values in separate columns even when
they happen to match. Never summarize current dimensions as an "already aligned" or
"safe to preserve" design target until independent selected-source evidence supports
the same value.

Do not change shared `DESIGN.md` tokens for a single-page adaptation. Use shared
authority only when shared semantics, reusable component contracts, or cross-surface
rules actually change.

Before editing, `dev-frontend` must map each applicable `acceptance_id` to:

- owner file and component/symbol;
- `reuse`, `extend`, `wrap`, or justified `new`;
- affected asset/data owner;
- focused static check and runtime verification method.

Pause implementation when the selected source is unavailable, the slice verdict is
`Partial` or `Not Ready`, a P1 asset is missing without an accepted per-item fallback,
or target viewport/state is unresolved. Preserve already-correct layout and ownership;
do not replace a working page wholesale to close local visual deltas.

## Two-Pass Runtime Gate

After implementation, perform at least two closed comparison passes:

1. capture selected source and implementation at the same viewport/state; create a
   reviewable side-by-side, overlay, or deterministic diff; read applicable computed
   styles and DOM geometry; record findings;
2. fix confirmed findings; repeat the same capture and computed checks; record the
   post-fix verdict.

Additional passes are allowed, but pass 2 cannot be replaced by a static re-read. Keep
the design capture and implementation capture independently inspectable even when an
overlay/diff is produced. Record tool, viewport, state, zoom, scroll position, artifact
path/ID, and evidence limitations for every capture.

## Required Runtime Coverage

Record each category as `verified`, `failed`, `Not verified`, or `not-applicable`, with
evidence IDs and a reason:

- real per-item assets and isolated fallback behavior;
- actual font inheritance and fallback, including native controls;
- truncation/wrapping/localization behavior;
- final composited foreground/background contrast;
- cross-section and main/sidebar alignment;
- card/control dimensions and hit areas;
- hover and visible keyboard focus;
- applicable loading, empty, error, permission, and disabled states;
- responsive behavior at the desktop target and every key breakpoint named by the
  slice contract.

Generic placeholders are not normal product assets. A fallback may cover one missing
or failed item only when the contract permits it; it must not replace all product
logos, thumbnails, covers, or QR codes.

Build, lint, typecheck, tests, source scans, or DESIGN.md lint do not satisfy the
runtime visual gate. They remain independent evidence.

## Degraded Evidence

When design collaboration tools block original export, local-network access, CORS, or
resource download:

1. retain the failed capability and exact limitation as evidence;
2. use only authorized visible screenshots, local exports, annotations, or supplied
   assets that remain available;
3. downgrade unsupported claims to `visually-inferred` or `Not verified`;
4. never switch silently to another visual source or call the unavailable original
   asset verified.

Browser work must preserve user state. Record initial tab, viewport, zoom, scroll, and
target identity; restore user-owned tabs to their prior viewport/scroll where possible,
close task-only tabs, and leave one explicitly identified delivery tab/artifact in an
inspectable state when requested.

## Handoff Artifact

Use `frontend-visual-evidence/v1`. The package-local
`assets/frontend-visual-evidence.schema.json` is the machine-checkable contract. The
artifact has a required `stage` and advances without inventing future evidence:

| Stage | Producer and allowed closure |
| --- | --- |
| `spec-ready` | `ui-spec`: selected source, evidence, deltas, and readiness only. No implementation/runtime/final fields. |
| `mapped` | `dev-frontend` before editing: adds complete implementation mapping. No visual-review/final fields. |
| `pass-1` | `dev-frontend` plus `ops-browser`: adds exactly one qualifying comparison pass. No runtime-coverage/final verdict. |
| `final` | `dev-frontend` after pass 2: adds two or more passes, runtime coverage, and final verdict for review. |

`Ready` requires an approved selected source and an empty blocker list. `Partial`
or `Not Ready` requires at least one explicit blocker and may exist only at
`spec-ready`; `mapped`, `pass-1`, and `final` require `Ready`. A producer must not
self-declare readiness to bypass pending, rejected, or unverified source approval.

Across its stages the artifact contains:

- selected-source freeze and evidence inventory;
- traceable delta rows;
- acceptance-to-owner implementation mapping;
- two or more runtime review passes;
- required runtime coverage;
- findings, fixed items, remaining gaps, `Not verified`, and final verdict.

Validate from an installed package without network or third-party Python modules:

```bash
python3 scripts/validate-frontend-visual-evidence.py <artifact.json>
```

The package-local validator applies the JSON Schema plus cross-reference, stage,
viewport/state, evidence-level, and completion semantics. Validity does not prove the
truth of evidence or UI quality. Reviewers must still inspect cited artifacts and
reachable source.

Every delta comparison value must cite evidence matching its declared evidence level;
selected-source and target-contract columns cannot cite `browser-computed` evidence as
their authority. Each computed check and each `verified` runtime coverage record must
cite final-pass browser evidence tagged with the same runtime category, viewport, and
state. One geometry observation cannot satisfy assets, font, contrast, focus, states,
or responsive coverage.

## Completion Rule

Visual completion requires all of:

1. accepted source identity and traceable target contract;
2. complete implementation mapping for applicable acceptance items;
3. two same-viewport/state runtime comparison passes;
4. computed geometry/style evidence for applicable exact claims;
5. desktop target plus every specified key breakpoint exercised;
6. no unresolved P0/P1 finding and no required category marked `failed` or
   `Not verified`.

A `Complete` artifact additionally requires an approved source, `Ready` readiness,
final-pass `browser-computed` evidence matching the pass viewport/state for every
verified runtime category, a passing final review, empty remaining-gap and
`not_verified` lists, and closure of every P0/P1 finding.

Otherwise report `Partial` or `Not Ready`. Final reporting lists fixed items, remaining
deltas, `Not verified`, changed files, evidence artifacts, validation, branch/commit,
and Worktree state.
