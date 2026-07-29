# Lanhu UI Evidence

Load this reference for an authorized Lanhu source whose exact selected-element
measurements, styles, or assets will be handed to `ui-spec`.

## Source And Capability Gate

Record project/team evidence, page and artboard identity, revision/version, design
mode (`标注`, `代码`, or asset view), artboard viewport, zoom, locale/theme, and the
selected state. Preflight layer selection, inspect-panel text/metadata, screenshot,
and authorized asset-download capability independently.

Never infer exact values from the scaled canvas. A value is `source-extracted` only
when the selected layer's inspect/style/code panel or equivalent design metadata
shows it and the evidence identifies the layer, property, page/artboard, revision,
and state. Screenshot-only estimates remain `visually-inferred`.

## Measurement Workflow

1. Freeze the accepted source, artboard, state, and requested element/component set.
2. Select layers by semantic layer/component name or exposed stable identifier when
   available. When the canvas exposes no semantic target before selection, use a
   fresh screenshot of the current artboard for a bounded visual click, then accept
   the result only after the inspect panel identifies the intended layer. Treat the
   click coordinates as transient evidence, never as a stable layer key. After each
   selection, verify that the inspect panel changed to that exact target.
3. Capture raw element bounds (`x`, `y`, width, height), parent/child and sibling
   relationships, padding/margin/gap, alignment, typography, fill, opacity, border,
   radius, shadow, asset metadata, and generated code only where exposed.
4. Measure repeated relationships separately by axis and semantic property. Do not
   mix card gaps with internal padding, different variants, states, or artboards.
5. Preserve every raw value and evidence ID. Do not overwrite a `17px` observation
   merely because the target contract later selects `16px`.
6. Capture authorized assets with layer identity, intended use, dimensions, format,
   scale/density, download evidence, and cleanup status.

## Spacing Normalization Candidate

For one repeated semantic spacing cluster, emit an even-grid candidate only when all
of these are true:

- there are at least three integer-pixel source measurements;
- one value has a strict majority;
- the majority value is divisible by `2`;
- every outlier differs from that majority by at most `1px`;
- no source annotation marks the outlier as intentional.

Thus `[16, 16, 16, 17]` yields a target candidate of `16px`, while retaining all four
raw observations. Do not auto-normalize ties, an odd majority, a spread greater than
`1px`, or measurements from different semantics. Do not apply this default to element
width/height, position, typography, borders, radii, icons, or assets.

The raw values remain `source-extracted`; the normalized candidate is `proposed` in
the browser handoff. `ui-spec` may promote it to an accepted target only when the
recorded user/design-system policy authorizes the cluster and no stronger source
contract conflicts.

## UI Handoff

Return `lanhu-ui-evidence/v1` with source identity and approval status, artboard/state
coverage, per-layer raw measurements and visual properties, evidence IDs, assets,
spacing-cluster membership, normalization candidates and reasons, conflicts,
capability gaps, and `Not verified` items. Keep this selected-source evidence
separate from any current-runtime `browser-computed` values.
