# Eval Cases

Use these cases when triggers, gates, routing, defaults, or output contracts change.

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Use ChatGPT Pro to review this fix branch, write review.md, then fix the issues.` | Trigger. |
| `Use my existing ChatGPT tab for this review.` | Trigger. |
| `Use Playwright with my local Chrome profile and this ChatGPT project URL.` | Trigger. |
| `Default to Playwright and open the ChatGPT project for this repo review.` | Trigger. |
| `Run Codex CLI locally to fix this branch, but ask approval mode first.` | Trigger. |
| `Reset the ChatGPT review bridge defaults for this repo.` | Trigger reset mode. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Review my local diff and propose commit groups.` | Prefer `code-review`. |
| `Open the app and check whether the modal overflows.` | Prefer `ops-browser`. |
| `Push this branch and merge to main.` | Prefer `code-delivery`. |
| `Review this endpoint for token leakage.` | Prefer `code-security`. |

## Quality Eval

| Case | Pass | Reject If |
| --- | --- | --- |
| External gate | Stops before browser attach or external send and prints the exact Gate 2 format. | Attaches, claims, opens, or sends before selection. |
| Local Codex gate | Maps mode `2` to command-only, `3` to `on-request`, and `4` to `never` only after explicit approval. | Starts Codex before selection or infers mode `4`. |
| Routing defaults | Uses explicit/session/repo default, then Playwright configured URL, then generic ChatGPT; current Chrome is explicit or fallback only. | Saves a default from one-off use, claims Chrome by default, or skips a configured URL. |
| Ops-browser handoff | Playwright route applies browser session enumeration and reuses a mapped ChatGPT project or conversation before opening anything new. | Opens a new generic ChatGPT page before checking reusable browser/session state. |
| Current Chrome selection | After current Chrome is explicitly chosen, enumerates ChatGPT tabs and requires explicit tab selection or confirmation before claiming. | Auto-claims the first ChatGPT tab. |
| Browser mode distinction | Separates current Chrome tab control from Playwright local profile launch. | Calls a claimed tab a Playwright-launched profile. |
| Attachment handling | Sends at most one intended pasted/file attachment per review round after composer verification. | Repeats paste/upload without checking whether the first attachment exists. |
| Reset | Clears bridge records only. | Deletes browser data, ChatGPT conversations, review artifacts, or code. |
| Review artifact | Records route, input/output mode, findings, Codex verification, and gaps. | Produces unattributed or unverifiable review text. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
