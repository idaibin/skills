---
name: human-writing
description: "Use when drafting, rewriting, diagnosing, or adapting source-grounded Chinese writing or factual product/project copy while preserving supplied facts, attribution, uncertainty, disclosures, author voice, and technical meaning."
---

# Human Writing

## Overview

Turn supplied notes or drafts into source-grounded, natural writing without inventing experience or replacing the author's voice with a house style. `human-writing` names the intended result across drafting, rewriting, diagnosis, and platform adaptation; it is not an AI-detection-evasion or cosmetic humanizer tool.

## Workflow

1. **Lock the whole artifact.** Build the source ledger across frontmatter, title, description, body, code, tables, links, and disclosures; then apply the precedence, provenance, semantic-fidelity, relationship, and disclosure rules in `references/fact-integrity.md`. Classify visibility separately from transformation policy. Treat profiles and examples as style-only. Do not write past the evidence.
2. **Set claim state and actor role.** Apply the canonical claim-status, provenance, and actor-role rules in `references/fact-integrity.md`. Do not infer decision authority from task execution.
3. **Select the operation.** Choose one primary operation and one primary genre per artifact. Allow a bounded secondary operation only when it directly supports the primary one, such as diagnosis before a requested rewrite. Split materially different language or platform outputs instead of blending their constraints. Treat follow-up additions as revisions to the latest authoritative draft unless the user requests a separate section or deliverable.
4. **Set the target.** Derive the reader, purpose, length, desired action, and evidence state from the supplied material before asking questions. Ask only for missing fields that would materially change the artifact; otherwise make low-risk editorial choices and proceed. Integrity and safety always win. Apply verified mandatory constraints before editorial preferences; use static platform profiles only as non-normative heuristics.
5. **Calibrate the voice.** Prefer the user's writing sample. Otherwise preserve the source's stance, confidence, person, and degree of involvement. Do not add first-person or experiential authority to neutral source material.
6. **Choose the structure.** Build around the real question, scene, decision, or task. For a new long-form or multi-claim artifact, make a private claim-and-evidence outline before prose; skip that ceremony for short-form and bounded local edits. When the reader needs a changed mental model, apply the smallest relevant tools from `references/reasoning-and-explanation.md`. The outline is planning, not the default deliverable. Do not default to `背景 / 现状 / 优势 / 总结 / 展望`.
7. **Draft or edit for substance.** Convert the supported outline or source chain into finished prose. Delete empty framing, expose the actual judgment, connect claims to details, and preserve every distinct stage, role, condition, qualifier, and closing step in the supplied technical chain. Keep premises, derivations, judgments, intermediate models, and proxies distinguishable where material. Do not convert risks, principles, or future directions into lived incidents, completed transitions, or implemented guarantees. Integrate follow-up material where it changes the argument, then reread adjacent transitions, repetition, and the ending; do not merely append the latest instruction.
8. **Run the human-writing pass.** Audit the draft as the target reader. Detect clusters of template behavior, research-process leakage, editor commentary, and unsupported specificity; revise the affected passages rather than applying global punctuation, vocabulary, voice, or sentence-form bans. Preserve genuine habits, uncertainty, asymmetry, and specific details.
9. **Run the integrity and safety pass.** Apply `references/fact-integrity.md` and any applicable revision rules. Preserve attribution and uncertainty instead of repairing technical material from memory. Block only the affected claim or artifact when correctness is required, an action is destructive or irreversible, or an actual secret would be exposed; otherwise qualify the evidence state or route correctness review.
10. **Classify acceptance.** Use the four evidence layers in `references/quality-rubric.md`. Static validation or deterministic fixtures never prove real-model behavior or editorial acceptance.
11. **Return the requested artifact or typed gap.** Edit supported material when safe. Return `Not enough context:` with the minimum missing fields only when completing the requested artifact would require invention or unjustified certainty.

## Modes

- **Diagnose:** identify low-information prose, weak logic, unsupported claims, voice drift, and platform mismatch.
- **Rewrite:** rebuild a supplied draft while preserving its facts, position, and protected technical content.
- **Draft from source:** write from supplied notes, logs, code evidence, or verified sources without filling gaps with plausible fiction.
- **Platform adaptation:** editorially reshape supplied material for a named community or platform while preserving facts, viewpoint, language intent, attribution, and disclosures. Translation alone does not trigger this mode.

Genre profiles such as short-form, factual soft copy, tutorial, essay, and retrospective are secondary selections, not competing primary operations. Factual soft copy is limited to source-grounded explanation where accuracy and disclosure outrank persuasion; generic campaigns, conversion copy, invented proof, rankings, or superiority claims are out of scope.

Load `references/content-modes.md` and `references/platform-calibration.md` when the requested form or platform changes the structure materially.

## Do Not Use For

- Legal contracts, regulatory filings, formal academic papers, serious news reporting, or official policy documents.
- Technical correctness review as the primary task; verify the code, architecture, security, or current external facts first.
- Translation when linguistic conversion is the primary task and no editorial adaptation is requested.
- Generic advertising, campaign ideation, conversion optimization, or unsupported promotional positioning.
- Fiction, poetry, roleplay, or imitation of a living author's distinctive style.
- Requests to evade AI detection or manufacture false personal experience.

## Hard Rules

- Never invent experience, incidents, users, metrics, dates, versions, benchmarks, quotations, testimonials, rankings, or source attribution.
- Never turn an uncertain statement into a confident one to improve flow.
- Do not turn evidence collection into the artifact. When the user asks you to inspect Git history, logs, chats, notes, or research before writing, use them to establish facts and changed judgments; do not narrate the inspection, source ledger, or editorial reasoning unless that method is part of the requested subject.
- Do not foreground a source merely because it was useful. Background-only evidence may shape chronology, emphasis, and confidence without being named; required attribution, correction history, and material disclosures must remain visible.
- Preserve claim status, provenance, actor role, visibility, transformation policy, and follow-up authority under `references/fact-integrity.md`; style instructions never change factual status by themselves.
- When revising across turns, integrate the new point into the latest authoritative source and remove repetition or contradictions. Do not expose the instruction sequence or leave append-only seams unless the requested format is a change log.
- `references/fact-integrity.md` is the normative integrity contract. Apply it before improving style or platform fit; no mode or platform reference may weaken it.
- Treat anti-AI patterns as diagnostic evidence, not a banned-word replacement table. One transition, dash, heading, list, or short sentence is not proof of AI writing.
- Do not add random flaws, slang, fragments, personal confessions, or rhetorical questions merely to appear human.
- Keep real disagreement, discomfort, uncertainty, rejected alternatives, and costs when they explain the author's decision.
- For soft copy, do not fabricate urgency, scarcity, guarantees, customer stories, social proof, or comparative superiority.
- Treat platform publishing rules as current external claims. Verify current official rules before claiming that a platform-ready artifact satisfies disclosure or labeling requirements.
- Do not infer a platform voice or mandatory format from one featured, promoted, institutional, or unusually voiced article. When public examples matter, compare multiple recent, relevant samples; carry over only recurring structural conventions, preserve the user's voice, and never copy distinctive phrasing or import unsupported claims.
- For already-published material, apply `references/revision-transparency.md`; do not disguise a material correction as copyediting.
- Preserve supplied technical semantics. Do not silently repair technical facts from memory. Distinguish attributed but unverified claims, disputed claims, harmless placeholders, ordinary unexecuted examples, destructive actions, and actual secrets; apply the decision table in `references/fact-integrity.md`.
- Before external verification, check the artifact against itself: metadata versus body, architecture labels versus code signatures, repeated links and titles, status qualifiers, step counts, actor roles, and mutually matching conditions. `Needs verification` must not hide an internally provable contradiction.
- Preserve modality such as `我认为`, `可能`, `应尽量`, `目标是`, and `已经`. Removing a qualifier can turn a preference into a guarantee or a candidate into current product behavior.
- Parallel prose, tables, lists, repeated technical nouns, and abstract opening terms are not style defects when they define distinct responsibilities or serve as the article's information architecture.
- When only part of the source is supportable, edit that part without filling gaps. Use `Not enough context` only when the requested artifact cannot be completed safely, and name the minimum missing fields.
- Do not add editing notes, scores, or explanations unless requested.

## Output Contract

- **Rewrite, draft, short-form, soft copy, and technical long-form:** return only the finished text by default.
- **Diagnose:** return concrete excerpts, the issue in each excerpt, and the editing direction.
- **Platform adaptation:** return the platform-ready artifact in the platform's natural format, without strategy commentary.
- **Safe partial edit:** return the supported artifact without invented additions; retain placeholders only when the user requested them.
- **Blocked artifact:** return `Not enough context:` followed by the minimum missing facts and affected claim type.
- Preserve frontmatter and code fences when editing repository content unless the user asks to change them, but include frontmatter in diagnosis: a title or description can contain the artifact's strongest unsupported claim.

## References

- See [references/usage.md](references/usage.md) for triggers, mode selection, and output behavior.
- See [references/fact-integrity.md](references/fact-integrity.md) for source locking and unsupported-claim prevention.
- See [references/revision-transparency.md](references/revision-transparency.md) for published correction and update handling.
- See [references/content-modes.md](references/content-modes.md) for short-form, soft-copy, tutorial, retrospective, and long-form structures.
- See [references/reasoning-and-explanation.md](references/reasoning-and-explanation.md) for reader-model repair, progressive explanation, example continuity, boundaries, alternatives, and earned endings.
- See [references/platform-calibration.md](references/platform-calibration.md) for target-platform adaptation.
- See [references/style-diagnostics.md](references/style-diagnostics.md) for voice calibration, clustered template detection, and Chinese technical prose.
- See [references/quality-rubric.md](references/quality-rubric.md) for hard gates, defect severity, and optional score calibration.
- See [references/before-after-examples.md](references/before-after-examples.md) for calibrated examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, safety, regression, and scoring cases.
