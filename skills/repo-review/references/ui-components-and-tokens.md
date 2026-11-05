# Reviewing Adopted UI Components And Tokens

Load this reference only when the selected basis changes or directly relies on a
project-owned UI component boundary, token/variable source, third-party UI adapter,
structured token pipeline, Component Registry, or adoption record. Do not require
optional assets in a project that has not adopted them.

## Review Closure

- Verify applicable project component guidance and any adopted records against live
  public imports, component files, exports, consumers, adapter roots, restricted
  dependencies, and complete bounded escape hatches.
- Keep real component source and types authoritative over Registry metadata. For an
  adopted Registry, verify that its project-native validator catches missing, stale,
  or duplicate source and public import drift instead of accepting a documentation
  marker check.
- Trace the project's actual token dependency graph, value owner, and permitted
  consumers. Enforce `Component -> Semantic -> Primitive`, business-only Semantic
  consumption, or component-token containment only when the project adopts that rule.
  Check applicable project-native negative tests for unknown references, cycles, bypasses, and
  authored CSS self-reference; verify generated parity only for actual generated
  consumers. Plain maintained CSS variables do not require a generator or extra tier.
- Attribute findings only when the basis introduces, expands, exposes, or directly
  relies on the mismatch. An unadopted optional Registry or token pipeline is `Not
  applicable`, not a defect.
- Keep static gates separate from runtime. Whole-image similarity is diagnostic only;
  critical state, accessibility, computed-style, and geometry claims require their own
  evidence at the accepted viewport/state and contract-owned tolerance.

- Verify that prose owns semantic purpose and the token source owns exact values;
  reject parallel value authorities or one-off values promoted to shared semantics
  without stable consumers.
- Trace base-control, shared-composition, Layout and page responsibilities where the
  change moves state, permissions, scrolling, spacing or workflow ownership.
- For newly introduced external component, icon, motion or template sources, verify
  source/version, license and permitted redistribution before accepting them in a
  public Skill, reusable template or distributable fixture.

When a validator supplies evidence, review it and its relevant negative fixtures,
not only its passing output. A green marker-only test proves document presence,
not project governance behavior.
