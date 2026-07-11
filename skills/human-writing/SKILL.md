---
name: human-writing
description: Use when drafting, rewriting, diagnosing, or adapting source-grounded Chinese personal and technical writing, factual project or product copy, and developer-community posts while preserving evidence, voice, disclosures, and technical meaning.
---

# Human Writing

## Overview

Turn supplied notes or drafts into source-grounded, natural writing without inventing experience or replacing the author's voice with a house style. `human-writing` names the intended result across drafting, rewriting, diagnosis, and platform adaptation; it is not an AI-detection-evasion or cosmetic humanizer tool.

## Workflow

1. **Lock the source.** Build the source ledger and apply the precedence, provenance, semantic-fidelity, relationship, and disclosure rules in `references/fact-integrity.md`. Treat profiles and examples as style-only. Do not write past the evidence.
2. **Select the operation.** Choose exactly one primary operation: Diagnose, Rewrite, Draft from source, or Platform adaptation. Then select one genre profile, the output language, and at most one platform profile. Activate disclosure and revision modules only when applicable; integrity rules always win.
3. **Set the target.** Identify the reader, purpose, length, desired action, and evidence state. Integrity and safety always win. Apply verified mandatory constraints before editorial preferences; use static platform profiles only as non-normative heuristics.
4. **Calibrate the voice.** Prefer the user's writing sample. Otherwise preserve the source's stance, confidence, person, and degree of involvement. Do not add first-person or experiential authority to neutral source material.
5. **Choose the structure.** Build around the real question, scene, decision, or task. Do not default to `背景 / 现状 / 优势 / 总结 / 展望`.
6. **Draft or edit for substance.** Delete empty framing, expose the actual judgment, connect claims to details, and preserve the supplied technical chain.
7. **Run the human-writing pass.** Detect clusters of template behavior, not isolated words or punctuation. Preserve genuine habits, uncertainty, asymmetry, and specific details.
8. **Run the integrity and safety pass.** Apply `references/fact-integrity.md` and any applicable revision rules. Preserve attribution and uncertainty instead of repairing technical material from memory. Block only the affected claim or artifact when correctness is required, an action is destructive or irreversible, or an actual secret would be exposed; otherwise qualify the evidence state or route correctness review.
9. **Classify acceptance.** Use the four evidence layers in `references/quality-rubric.md`. Static validation or deterministic fixtures never prove real-model behavior or editorial acceptance.
10. **Return the requested artifact or typed gap.** Edit supported material when safe. Return `Not enough context:` with the minimum missing fields only when completing the requested artifact would require invention or unjustified certainty.

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
- `references/fact-integrity.md` is the normative integrity contract. Apply it before improving style or platform fit; no mode or platform reference may weaken it.
- Treat anti-AI patterns as diagnostic evidence, not a banned-word replacement table. One transition, dash, heading, list, or short sentence is not proof of AI writing.
- Do not add random flaws, slang, fragments, personal confessions, or rhetorical questions merely to appear human.
- Keep real disagreement, discomfort, uncertainty, rejected alternatives, and costs when they explain the author's decision.
- For soft copy, do not fabricate urgency, scarcity, guarantees, customer stories, social proof, or comparative superiority.
- Treat platform publishing rules as current external claims. Verify current official rules before claiming that a platform-ready artifact satisfies disclosure or labeling requirements.
- Do not infer a platform voice or mandatory format from one featured, promoted, institutional, or unusually voiced article. When public examples matter, compare multiple recent, relevant samples; carry over only recurring structural conventions, preserve the user's voice, and never copy distinctive phrasing or import unsupported claims.
- For already-published material, apply `references/revision-transparency.md`; do not disguise a material correction as copyediting.
- Preserve supplied technical semantics. Do not silently repair technical facts from memory. Distinguish attributed but unverified claims, disputed claims, harmless placeholders, ordinary unexecuted examples, destructive actions, and actual secrets; apply the decision table in `references/fact-integrity.md`.
- When only part of the source is supportable, edit that part without filling gaps. Use `Not enough context` only when the requested artifact cannot be completed safely, and name the minimum missing fields.
- Do not add editing notes, scores, or explanations unless requested.

## Output Contract

- **Rewrite, draft, short-form, soft copy, and technical long-form:** return only the finished text by default.
- **Diagnose:** return concrete excerpts, the issue in each excerpt, and the editing direction.
- **Platform adaptation:** return the platform-ready artifact in the platform's natural format, without strategy commentary.
- **Safe partial edit:** return the supported artifact without invented additions; retain placeholders only when the user requested them.
- **Blocked artifact:** return `Not enough context:` followed by the minimum missing facts and affected claim type.
- Preserve frontmatter and code fences when editing repository content unless the user asks to change them.

## Maintenance

When changing triggers, modes, or output behavior, update `references/eval-cases.md`, the quality rubric, platform calibration, examples, and `agents/openai.yaml`. In AICraft, run `python3 scripts/validate-skills.py --skill human-writing`, `python3 scripts/eval-human-writing.py`, and `python3 scripts/test_validate_skills.py` before publishing.

## References

- See [references/usage.md](references/usage.md) for triggers, mode selection, and output behavior.
- See [references/fact-integrity.md](references/fact-integrity.md) for source locking and unsupported-claim prevention.
- See [references/revision-transparency.md](references/revision-transparency.md) for published correction and update handling.
- See [references/content-modes.md](references/content-modes.md) for short-form, soft-copy, tutorial, retrospective, and long-form structures.
- See [references/platform-calibration.md](references/platform-calibration.md) for target-platform adaptation.
- See [references/style-diagnostics.md](references/style-diagnostics.md) for voice calibration, clustered template detection, and Chinese technical prose.
- See [references/quality-rubric.md](references/quality-rubric.md) for hard gates, defect severity, and optional score calibration.
- See [references/before-after-examples.md](references/before-after-examples.md) for calibrated examples.
- See [references/eval-cases.md](references/eval-cases.md) for trigger, safety, regression, and scoring cases.
