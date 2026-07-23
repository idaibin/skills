# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Turn the selected Product Design mockup into an implementation-ready contract for this Token popover, preserving its real data and 338x286 size.` | Trigger `ui-spec` Feature Spec; bind the selected source and specify layout, states, mappings, responsive/accessibility rules, and acceptance without generating images or editing source. |
| `Use this accepted settings screenshot and current components to specify loading, validation, error, success, focus, and reduced-motion behavior before implementation.` | Trigger Feature Spec and label source-derived versus proposed decisions. |
| `Our accepted shared Button semantics, variants, and spacing-token contract must change across four surfaces; specify the revision and rollback.` | Trigger Design System Spec. |
| `Extract the existing token names, component variants, and state vocabulary into the accepted shared contract.` | Trigger Design System Spec extraction without claiming pixels or screenshots prove live semantics. |
| `The shared manifest exists but approval is null; specify this local dialog using verified live owners without promoting the shared baseline.` | Trigger Feature Spec and preserve the approval boundary. |
| `Specify updater failure feedback without hiding the current local archive-operation status.` | Trigger Feature Spec and assign separate feedback owners to the two async domains. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Generate three visual directions for this dashboard and let me choose one.` | Prefer the host's Product Design capability; `ui-spec` requires a selected source. |
| `Critique this onboarding flow and produce an improved visual mockup.` | Prefer Product Design audit/ideation. |
| `Build a disposable interactive prototype from this idea.` | Prefer Product Design; do not create prototype code in `ui-spec`. |
| `Implement the accepted UI specification in React.` | Prefer `dev-frontend`; consume `ui-spec` artifacts. |
| `Specify this feature's users, permissions, failure behavior, and product acceptance.` | Prefer `product-spec`. |
| `Audit the implemented frontend for accessibility and token drift.` | Prefer `audit-frontend`. |
| `Map where Button tokens are defined, exported, and consumed without changing their contract.` | Prefer `repo-map`. |
| `Open the page and capture console, network, and screenshots.` | Prefer `ops-browser`. |
| `Commit and push the accepted UI changes.` | Prefer `repo-delivery`. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Source gate | records a selected/accepted source with stable identity, revision, approval, rights, use, and ignore boundaries | starts specifying an unselected visual idea or silently invokes image generation |
| Grounding | records product, audience, job, facts, actions, states, current owners, exclusions, and gaps | invents a generic UI contract |
| Evidence precision | distinguishes verified, extracted, proposed, and `Not verified` decisions | treats pixels as exact token, behavior, ownership, accessibility, or runtime proof |
| Profile gate | defaults one page/flow to Feature Spec and activates Design System Spec only for shared semantics/contracts | treats every page as a system revision |
| States and interaction | covers applicable states, transitions, feedback ownership, focus, and reduced motion | specifies only the happy appearance |
| Responsive/accessibility | defines reflow, overflow, targets, keyboard/focus, semantics, contrast, localization, and exclusions | hands implementation a desktop screenshot only |
| Reuse mapping | records `reuse`, bounded `adapt`, or justified `new` against live owners | creates a parallel kit or token layer |
| Approval boundary | revalidates live owners and requires approval before shared promotion | treats a pending, rejected, or stale manifest as accepted |
| Handoff | supplies source revision, layouts, states, interactions, assets, mappings, shared deltas, acceptance, and gaps to `dev-frontend` | hands over visual mood language without implementable decisions |
| Authority | writes specification artifacts only | generates/edits images, builds prototypes, edits product source, operates runtime tools, or mutates Git |

## Scoring

Score each quality case 0–10. Minimum pass: routing is correct, every quality case scores at least 8, no authority violation exists, and applicable shared-package templates validate.
