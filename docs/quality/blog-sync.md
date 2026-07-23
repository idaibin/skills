# Blog Sync Record: AICraft Skill Boundaries

Date: 2026-07-21

## Current drift

On 2026-07-22, AICraft renamed `ui-design` to `ui-spec` and narrowed it to
selected-source specification. The Blog files listed below have not been
reverified or resynchronized for that rename in the current task. Blog sync and
publication therefore remain `Not verified`.

## Applied scope

The public explanation in `/Users/daibin/Projects/repo-github/blog` was updated
in the bilingual catalog and catalog-evolution articles:

- `src/content/skills/skills-catalog.zh.mdx`
- `src/content/skills/skills-catalog.en.mdx`
- `src/content/blog/from-aicraft-to-skills-catalog.zh.mdx`
- `src/content/blog/from-aicraft-to-skills-catalog.en.mdx`

## Verified AICraft facts to synchronize

- The catalog has 14 public packages after the current source validation.
- `ui-spec` translates a selected visual source into a Feature Spec for one page or
  flow by default; shared tokens, component semantics, variants, or shared visual
  rules activate the conditional Design System Spec profile. Visual exploration,
  image generation, critique, and prototypes belong to Codex Product Design.
- `domain-modeling` defaults to shared business terms, ambiguity, rules, and
  boundary scenarios. Lifecycle and bounded-context work are conditional; API,
  database, frontend, and backend structure remain outside its ownership.
- `product-spec` owns user-visible product behavior and acceptance, not API or
  interface authority. `repo-map` records the current authority, consumers, and
  validation entry points when a durable map is requested.
- `repo-review` reads the current Worktree/index, a fixed immutable SHA/range,
  or a verified review package and remains read-only. `repo-delivery` owns separately authorized Git
  mutations, groups local commits by semantic intent unless one commit is
  explicitly requested, chooses branch integration from evidence, and does not
  infer push from a commit request.
- `ask-chatgpt` is the single explicitly authorized ChatGPT collaboration
  surface for review, research, visual exploration, and decision challenge.
  Codex chooses the theme, route, and boundaries; external advice must be
  verified against local evidence before it changes the implementation.
- Planning, concrete-failure diagnosis, and task handoff stay in host/global
  instructions rather than becoming new public Skills.
- Static package validation is evidence of structure only. Real routing,
  cross-Skill workflow, external ChatGPT, UI prototype, global handoff triggers,
  and Blog publication remain `Not verified` until their applicable Live Gates
  run.

## Public wording contract

Both languages must identify `ask-chatgpt` as the user-facing action name,
cover review, research, visual exploration, and decision challenge, retain the
Codex-first gate, and state that ChatGPT output is verified against the relevant
local basis. Exact prose may differ between the catalog and the longer article.

## Validation gate

Run the Blog repository's required `npm run build` and
`npm run astro -- check` commands before publication. This record does not
authorize publication or any other external write.
