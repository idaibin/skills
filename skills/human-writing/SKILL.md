---
name: human-writing
description: "Use when drafting, rewriting, proofreading, diagnosing, or adapting source-grounded prose, especially technical articles, essays, tutorials, product notes, and social posts, while preserving facts, attribution, uncertainty, voice, and meaning. Supports private English-first reasoning for Chinese finals; not translation-only, fiction, or AI-detection evasion."
---

# Human Writing

## Outcome Contract

- **Outcome:** natural, source-grounded writing shaped for the requested reader and surface.
- **Evidence:** supplied text, notes, verified sources, author samples, and explicit task constraints.
- **Done when:** the artifact preserves meaning and protected details, solves the reader's task, and contains no concrete factual, structural, or voice defect worth another edit.
- **Output:** the requested artifact only, unless the user asks for diagnosis, alternatives, or editing notes.

## Core Stance

- Treat writing patterns as diagnostic signals, not a checklist or banned-word table.
- The author's supported voice wins over a generic house style.
- Over-editing is failure. Prefer fewer, stronger changes; leave already effective prose alone.
- Most useful polish is subtraction: remove repetition, empty framing, synthetic emphasis, and process narration without thinning the argument.
- Never trade factual precision, uncertainty, attribution, or a stable technical term for smoother prose.

## Workflow

1. **Lock the source.** Identify authoritative facts, judgments, unknowns, protected text, visibility limits, and claim status across the whole artifact. When research is requested, also freeze its question, source boundary, and stop condition. Apply `references/fact-integrity.md` when the task contains multiple sources, technical claims, external facts, attribution, disclosures, or research-backed drafting.
2. **Set the target.** Infer the primary operation, reader, purpose, language, length, platform, and genre from the request and source. Ask only about missing information that would materially change the result.
3. **Calibrate voice.** Prefer a supplied author sample, then the stance and confidence visible in the source, then a neutral precise voice. Never manufacture first-person experience or quirks.
4. **Choose the smallest useful structure.** Use a private outline for new long-form or multi-claim work. For an existing long artifact, map sections and repetition before restructuring. Skip planning ceremony for short or local edits.
5. **Draft or edit for substance.** Lead with the real question, scene, mechanism, or decision. Keep evidence near claims, integrate follow-up material where it changes the argument, and adapt for a platform rather than merely reformatting or translating.
6. **Run two passes.** First check facts, status, protected text, disclosures, and safety. Then diagnose clusters of template residue, weak logic, repetition, manufactured cadence, and voice drift. Fix only confirmed reader problems.
7. **Stop and return.** Compare with the source and stop when another change would only normalize preference-level wording. Return the requested artifact or `Not enough context:` with the minimum missing facts when completion would require invention.

## Modes

- **Draft from source:** create prose from supplied or verified material without filling gaps with plausible fiction.
- **Rewrite or proofread:** improve a supplied artifact while preserving its position, meaning, structure, and protected content unless broader change was requested.
- **Diagnose:** identify concrete factual, logical, structural, voice, or platform problems without rewriting unless asked.
- **Platform adaptation:** reshape supported content for a named community or surface while preserving claims, attribution, disclosures, and author voice.

For a requested Chinese final from notes or mixed-language evidence, a private English claim-and-structure pass may help. Skip it for an existing Chinese draft or stronger Chinese sample unless requested. Treat the English intermediate as provisional phrasing, never as a new source, and check the Chinese final against the original evidence.

## Boundaries

Do not use for translation-only work, fiction or poetry, imitation of a living author's distinctive style, formal legal or regulatory writing, serious news reporting, technical correctness review as the primary task, unsupported advertising, or AI-detection evasion.

Hard requirements:

- Never invent experience, incidents, users, metrics, dates, versions, benchmarks, quotations, testimonials, results, rankings, or attribution.
- Preserve uncertainty, modality, claim status, actor role, and exact commands, paths, flags, identifiers, versions, code, and numeric ranges.
- Keep background research in the reasoning layer unless visible provenance is required or requested.
- Treat platform rules and other current external claims as volatile; verify them before presenting the artifact as compliant.
- Preserve frontmatter, links, code fences, quotations, and structural assets unless the task authorizes changing them.
- Integrate later instructions into the latest authoritative artifact; do not expose the editing sequence or leave append-only seams.
- Block only the affected unsafe or unsupported claim when a safe partial artifact remains possible.

## Output Contract

- Draft, rewrite, proofread, and adaptation: return the finished artifact only.
- Diagnose: return the excerpt or location, concrete problem, impact, and editing direction.
- Chinese final with private English support: return Chinese only unless both versions were requested.
- Unsupported artifact: return `Not enough context:` followed by the minimum missing facts.

## Reference Loading

- Load [fact-integrity.md](references/fact-integrity.md) for source precedence, claim status, attribution, disclosures, external claims, technical preservation, or a research-to-draft loop.
- Load [content-modes.md](references/content-modes.md) only when a genre changes the structure materially.
- Load [platform-calibration.md](references/platform-calibration.md) only for a named publishing surface; use profiles as heuristics, not current platform policy.
- Load [style-diagnostics.md](references/style-diagnostics.md) when voice, rhythm, Chinese technical prose, or AI-like template residue is the problem.
- Load [reasoning-and-explanation.md](references/reasoning-and-explanation.md) for mental-model repair, progressive explanation, boundaries, alternatives, or an earned conclusion.
- Load [revision-transparency.md](references/revision-transparency.md) only for already-published material with substantive changes.
- Use [quality-rubric.md](references/quality-rubric.md) for final editorial review, [before-after-examples.md](references/before-after-examples.md) when a concrete calibration example helps, and [eval-cases.md](references/eval-cases.md) when changing Skill behavior.
