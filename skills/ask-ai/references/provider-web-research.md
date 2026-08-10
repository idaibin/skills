# Web Research Provider Routing

## Contents

- [Boundary](#boundary)
- [Capability Routes](#capability-routes)
- [Provider Profiles](#provider-profiles)
- [Source Integrity Gate](#source-integrity-gate)
- [Completion And Recovery](#completion-and-recovery)
- [Official Sources](#official-sources)

## Boundary

Use this reference only when the user explicitly requests a named Web AI or an
independent external research result whose distinctive search/corpus/workflow adds
value beyond native Web research. Provider availability, an open tab, or a mode label
does not authorize submission.

Keep four routes distinct:

- `broad-deep-research`: multi-step current-Web investigation across source types;
- `source-bound-synthesis`: questions constrained to an approved source collection;
- `scholarly-discovery`: academic-paper discovery, filtering, and comparison;
- `citation-context-check`: whether later papers support, contrast, or merely mention
  a cited work.

Never select a provider from brand popularity alone. One task may use more than one
route only when the user authorizes every provider and the outputs remain separately
attributed.

## Capability Routes

| Need | Preferred Web profile | Why | Not a substitute for |
| --- | --- | --- | --- |
| Broad current Web research with inspectable citations | ChatGPT Deep Research, Gemini Deep Research, or Perplexity Research | multi-step search and cited report | opening and checking decision-critical originals |
| Research using Google Search plus selected Drive/Gmail/files/NotebookLM sources | Gemini Deep Research | explicit source selection and editable research plan | proof that every selected private source was read completely |
| Reusable synthesis over a controlled corpus | NotebookLM | source-bound chat with inline citations and importable Web/Drive sources | open-Web completeness or systematic-review methodology |
| Systematic-review workflow | Elicit | protocol refinement, search/import, screening, structured extraction, synthesis | human dual review or validation of extracted outcomes |
| Fast peer-reviewed evidence search and study comparison | Consensus Research Agent | scholarly corpus, academic filters, DOI/citation/author workflows | exhaustive systematic review or claim-validity proof |
| Citation stance and contradiction discovery | Scite Smart Citations | citation contexts classified as supporting, contrasting, or mentioning | independent replication, risk-of-bias assessment, or truth judgment |
| Canonical bibliographic verification | Crossref, OpenAlex, Semantic Scholar, PubMed/PMC, publisher/repository original | DOI/PMID/metadata and original-record resolution | an AI synthesis provider |

## Provider Profiles

### Broad Deep Research

- **ChatGPT Deep Research:** use for broad multi-source reports, connected sources,
  files, and exportable cited reports. Capture the report identity, activity/completion
  state, inline citation targets, sources-used section, and exported artifact hash.
- **Gemini Deep Research:** use when Google Search, files, Gmail/Drive, or NotebookLM
  source selection is material. Review the proposed plan and selected sources before
  starting. Record whether Google Search was enabled and which private source classes
  were selected without exposing their contents.
- **Perplexity Research:** use for a fast current-Web second research opinion with
  citations and export. Record the fixed Research mode; do not claim a chosen model
  because the mode may select models automatically.

### Source-Bound And Scholarly Research

- **NotebookLM:** use only after resolving the exact notebook and approved source set.
  Treat imported sources as static copies; record source identity, import date, and
  whether the cited location exists in that copy. Answers outside the approved corpus
  are unsupported.
- **Elicit:** use for a bounded literature-review protocol with explicit query,
  inclusion/exclusion criteria, databases/imports, screening decisions, extraction
  columns, and synthesis. Preserve DOI/PMID, study identity, supporting quote/figure,
  exclusion reason, and methods export. AI screening or extraction remains a candidate
  until checked against the paper.
- **Consensus:** use for peer-reviewed discovery, citation/author crawling, filters,
  study comparison, and gap analysis. Record whether analysis used full text or only
  an abstract when the interface exposes it. “Peer reviewed” does not prove a finding
  is correct or applicable.
- **Scite:** use after paper identity is known to inspect citation statements and find
  supporting/contrasting evidence. Preserve the citing paper, cited paper, quoted
  citation context, classification, and link. The machine classification is evidence
  for prioritizing manual inspection, not the final interpretation.

## Source Integrity Gate

Every material research claim enters a local Claim-Evidence Ledger with:

```yaml
claim_id: <stable local id>
claim: <one testable statement>
provider: <attributed Web provider>
provider_report_id: <stable URL/id>
citation_target: <original URL or bibliographic record>
persistent_id: <DOI|PMID|PMCID|arXiv|ISBN|repository SHA|not-available>
source_type: <official-doc|specification|paper|dataset|repository|secondary>
source_version_or_date: <exact value>
provider_support: <direct|partial|contextual|mismatched|missing>
local_verification: <verified|inference|not-verified>
limitations: <named gap>
```

For each decision-critical claim:

1. follow the citation to the original source, not a search snippet, AI summary,
   citation aggregator page, or another generated report;
2. verify title/author/date plus DOI, PMID, repository SHA, specification version, or
   another durable identity when available;
3. locate the passage, table, figure, code, dataset field, or official statement that
   supports the exact claim;
4. distinguish abstract-only, metadata-only, partial full text, and complete accessible
   full text;
5. check retraction/correction status and seek contradictory evidence when material;
6. record a mismatch, inaccessible source, unsupported extrapolation, or invented
   citation as `Not verified`; never repair it silently with a different source;
7. preserve provider attribution separately from the local conclusion.

A valid DOI proves bibliographic identity, not correctness. Citation count, journal
name, “peer reviewed,” provider confidence, and Scite stance labels do not replace
study-quality, methods, applicability, or replication assessment.

## Completion And Recovery

- Deep Research completes only on a provider-owned terminal report state, not elapsed
  time, a partial preview, or disappearance of a spinner alone.
- Capture the stable conversation/report/notebook/workflow identity before accepting
  output. Export when supported and hash the captured artifact.
- If generation is interrupted, inspect the same report/container read-only within a
  fixed retry/deadline bound. Never start a duplicate paid research job merely because
  capture failed.
- A Web report is complete only as provider output. Local research remains
  `Complete`, `Complete with gaps`, or `Incomplete` according to citation resolution
  and the decision-critical evidence ledger.
- Do not upload private papers, repository archives, Drive files, or customer material
  unless the current request authorizes that exact provider and data scope.

## Official Sources

Capability profile reviewed 2026-08-09. Recheck the active account and surface:

- ChatGPT Deep Research: <https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt>
- Gemini Deep Research: <https://support.google.com/gemini/answer/15719111>
- Perplexity Research: <https://www.perplexity.ai/help-center/en/articles/10738684-what-is-research-mode>
- NotebookLM: <https://support.google.com/notebooklm/answer/16164461>
- Elicit systematic review: <https://elicit.com/solutions/systematic-review>
- Consensus Research Agent: <https://help.consensus.app/en/articles/12641232-research-agent>
- Scite Smart Citations: <https://scite.ai/features>
- Semantic Scholar API: <https://www.semanticscholar.org/product/api>
- PubMed data/API: <https://pubmed.ncbi.nlm.nih.gov/download/>
