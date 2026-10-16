# Portable input and result contract

## Input: work-retro-request/v1

Accept prose or structured data containing:
- question, requested_scope, cutoff, audience, output_destination;
- source_inventory: connector/export labels, enumeration method, pagination/end state,
  accessible/inaccessible/empty status, and retrieval limitations;
- source_records: source_id, canonical_id if known, source_kind, surface when proven,
  timestamp/version, project/domain, record_form (full/excerpt/summary), locator,
  content, sensitivity, truncation/attachment gaps;
- current_authorities and known corrections, with provenance;
- permitted_effects: normally read and one requested report artifact.

Do not invent missing fields. Use unknown plus its consequence. Full record text with
missing attachments or execution traces is not a complete session transcript.

## Result: work-retro-result/v1

Emit these fields as clear report sections or structured data:
1. basis: request, cutoff, supplied versions and authority, output audience.
2. coverage: requested/discovered/read/empty/blocked sources, pages/cursors, counts
   before/after dedupe, full/excerpt/summary distinctions, exclusions, unresolved gaps.
3. findings: stable ID; observation; exact evidence source IDs/locators; evidence status
   (Verified / Inference / Not verified); context; consequence; independent episode
   count where known; counterevidence; confidence rationale.
4. proposals: ID, finding IDs, narrow scope, applicability, exceptions, target owner,
   existing authority, minimal change, expected effect, validation, rollback/retirement,
   and authorization/decision still needed.
5. conflicts_and_deprecations: old claim/rule, current evidence, superseding authority,
   affected scope, proposed lifecycle (candidate/pilot/stable/revise/deprecated), and
   decision owner. Proposed deprecation is not an applied edit.
6. validation: frozen basis, oracle, actual cases/commands/evidence, passed/failed/not-run,
   safety/owner failures separately, limitations, adoption recommendation.
7. next_action and completion_state: completed for the declared bounded corpus;
   partial for unavailable required coverage; blocked only for the dependent action;
   no-finding when evidence yields no justified improvement. A bounded report may be
   completed while explicitly leaving account-wide history coverage Not verified.

Use Verified only for what the cited evidence proves: a user's correction can verify
that the request changed, not that a fix passed. Absence of an artifact in a current
listing does not prove it never existed. Summaries may support a provisional finding
but cannot establish the underlying run's success, count, cost, or causality.

## Public/private split

A private report may retain necessary original references for the requesting user.
A public export contains only reusable methods, public-source citations, synthetic
cases, and non-identifying aggregate coverage when safe. Exclude personal/account
identifiers, credentials, private URLs, real prompts/transcripts, customer/project
payloads, and hidden operational instructions. Generalizing an example must preserve
the failure mechanism; otherwise withhold it and report the missing publication basis.
