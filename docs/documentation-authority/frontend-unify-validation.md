# Frontend Documentation Authority Validation

## Basis and exclusions

The project basis was the current `unified-portal` Worktree at repository HEAD
`b3e6806b`, containing separately built user and administration applications, one
accepted shared visual system, product/UI specifications, repository maps, and
current backend/client contract owners. The authorized mutation scope was
documentation only; unrelated existing code and test changes in the Worktree were
excluded from attribution. Browser, deployment, SSO, production permission, and live
object access were excluded unless separately evidenced.

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

## Skill changes validated

`product-spec` treats durable specs as current terminal contracts, distinguishes
business-effective dates from edit/validation dates, and gates structured sidecars by
real lifecycle ownership. `ui-spec` resolves an approved `<design-root>`, keeps one
`DESIGN.md` per proven shared boundary, and stores visual evidence in ignored task
space by default. `repo-map` separates source owner, build/deploy owner, runtime
identity, and gateway alias while supporting explicitly authorized full-rebuild
closure. `repo-review` applies a conditional Documentation Authority Review and
requires a new fixed basis after repairs.

## Project outcome

The project has one product foundation with four registered slices, one shared visual
authority with five independently loadable UI slices, one current Repo Map, and
stable per-application development instructions. The extra `features/` wrapper,
dated integration snapshots, copied Skill/process standards, eight visual-evidence
JSON files, old UI indexes, and system metadata were removed from formal docs.

Independent review corrected resource-action overgeneralization, false App Store
integration readiness, an unregistered shell provider, a corrupted selected-source
identity, missing native App Center operations, and an invented schedule day view.
The Contract Map now records the still-visible major-category action as a current
non-conforming consumer rather than implying the UI already follows the native owner.

## Validation status

- Project Markdown: 26 formal files, 81 checked local links, 0 broken.
- Google DESIGN lint: 0 errors, 0 warnings, 0 infos for
  `frontend-unify/DESIGN.md` with `@google/design.md@0.3.0`.
- Formal project docs contain no JSON/YAML evidence, dated integration status,
  Skill-development plan, personal absolute path, or task validation timeline.
- Skill validation: 16 packages, 48/48 routing cases, and 174 tests passed; shared
  protocol synchronization and DESIGN contract guards passed.
- Independent mutual review on the repaired basis returned no actionable findings.
- Published `main` and local `main` resolve to the same commit.
- All files in globally installed `product-spec`, `ui-spec`, `repo-map`, and
  `repo-review` match their published source; empty source placeholders are not
  packaged by the installer.
- Updated-Skill project canary passed Product/UI/Repo Map/Documentation Authority
  static checks.

Static document checks do not prove browser rendering, deployment, authentication,
gateway registration, production permissions, media signing, or live object access;
those remain `Not verified`.
