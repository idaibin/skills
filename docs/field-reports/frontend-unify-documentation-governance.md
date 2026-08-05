# Frontend Documentation Authority Field Report

## Basis and exclusions

The fixed project basis was a shared frontend aggregate containing separately built
user and administration applications, one accepted shared visual system, product/UI
specifications, repository maps, and current backend/client contract owners. The
exercise changed documentation only. Browser, deployment, SSO, production permission,
and live object access were excluded unless separately evidenced.

## Observed failures

- One feature wrapper mixed a product index with page and administration details.
- Durable UI docs exposed several contradictory evidence files all labelled final.
- Product and UI specs retained edit-date versions, approval timestamps, superseded
  decisions, and multi-pass validation narratives.
- A dated integration snapshot copied an older backend revision and advertised write
  routes absent from the current native controller.
- A UI spec contradicted itself about current-page filtering versus server-paginated
  search.
- A source module owner and its retained runtime service identity were easy to
  collapse into one incorrect ownership claim.
- General Skill/process guidance and a system metadata file remained inside product
  documentation.

## Skill failure modes and adopted changes

`product-spec` now treats durable specs as current terminal contracts, distinguishes
business-effective dates from edit/validation dates, and gates structured sidecars by
real lifecycle ownership. `ui-spec` resolves an approved `<design-root>` instead of
assuming the Git root, keeps one `DESIGN.md` per proven shared boundary, and stores
visual evidence in ignored task space by default. `repo-map` separates source owner,
build/deploy owner, runtime identity, and gateway alias while supporting explicitly
authorized full-rebuild closure. `repo-review` adds a conditional Documentation
Authority Review and requires a new fixed basis after repairs.

## Project outcome

The project now has one product foundation with four registered slices, one shared
visual authority with five independently loadable UI slices, one current Repo Map,
and stable per-application development instructions. The extra `features/` wrapper,
dated integration snapshots, copied Skill/process standards, eight visual-evidence
JSON files, old UI indexes, and system metadata were removed from formal docs.

Independent review found and the final rewrite corrected additional material issues:
resource-type actions no longer collapse into a generic details route; App Store
integration readiness is blocked by known gateway/path conflicts; the management shell points to its
real routed owner, marks the unregistered `AsideMenu.vue` dormant, and records current 210px/no-active-Header drift; missing native
App Center writes are explicit contract conflicts; and schedule UI no longer invents
a day view. A corrupted selected-source identity was repaired against the retained
source record. UI specs retain stable selected-source identities, named approvers, use/ignore boundaries,
viewport scope, and honest readiness without restoring dated review logs.

## Validation status

- Project Markdown links: 81 checked, 0 broken by resolving relative links across the
  26 formal Markdown files while excluding dependency and task-artifact trees.
- Google DESIGN lint: 0 errors, 0 warnings, 0 infos for
  `frontend-unify/DESIGN.md` with `@google/design.md@0.3.0`.
- Formal project docs contain no JSON/YAML evidence, dated integration status,
  Skill-development plan, personal absolute path, or task validation timeline.
- Skill package validation: `bash scripts/check-skills.sh` passed for 16 packages and
  174 tests after synchronized protocol regeneration; package digest is recorded in
  `docs/quality/live-canary-summary.md`.
- Routing: 48/48 catalog cases passed; 7/7 documentation-authority contract tests passed.
- Independent mutual review: completed on the repaired basis; material project,
  cross-Skill design-root, metadata-routing, and source-truth findings were corrected.
- Source-to-global-install package parity: Pending.
- Updated-Skill project canary: static Product/UI/Repo Map/Documentation Authority
  checks passed on the rewritten tree; browser and deployment canaries remain out of scope.

Static document checks do not prove browser rendering, deployment, authentication,
gateway registration, production permissions, media signing, or live object access;
those remain `Not verified`.
